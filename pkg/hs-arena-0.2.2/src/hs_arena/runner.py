"""Plays one game between two Players and writes the game directory (PLANNING.md §5.2, §7.5)."""

from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any

from . import FIREPLACE_COMMIT, POOL_VERSION, PROTOCOL_VERSION, RUNTIME_VERSION
from ._fileio import write_json
from ._fp import init_engine
from .agents import make_player
from .agents.base import Player, SeatInfo
from .deck import Deck, validate_deck_data
from .engine import Engine, EngineCrash
from .pool import DECK_SIZE, HERO_CLASSES, MAX_COPIES, MAX_LEGENDARY_COPIES
from .protocol import Config

__all__ = ["run_game", "play_game", "build_state", "build_deck_state"]


def build_deck_state(game_id: str, i: int, seq: int, last_result, config: Config, *,
                     events=None, result=None) -> dict[str, Any]:
    """A seat-neutral setup view: no engine, first player or opponent deck exists yet."""
    timeout = float(config.exit_grace_s if result else config.decision_timeout_s)
    state = {
        "protocol_version": PROTOCOL_VERSION, "game_id": game_id, "seq": seq, "player": i,
        "turn": 0, "phase": "game_over" if result else "deck_submission", "timeout_s": timeout,
        "deadline_epoch_s": round(time.time() + timeout, 3), "you": None, "opponent": None,
        "choice": None, "events": list(events or []), "last_action_result": last_result,
        "result": result,
        "legal_actions": [] if result else [{"type": "submit_deck"}, {"type": "concede"}],
    }
    if result is None:
        state["deck_rules"] = {
            "pool_version": POOL_VERSION, "hero_classes": list(HERO_CLASSES), "deck_size": DECK_SIZE,
            "max_copies": MAX_COPIES, "max_legendary_copies": MAX_LEGENDARY_COPIES,
        }
    return state


def build_state(engine: Engine, game_id: str, i: int, seq: int, last_result, config: Config) -> dict[str, Any]:
    v = engine.view(i)
    over = v["phase"] == "game_over"
    timeout = float(config.exit_grace_s if over else config.decision_timeout_s)
    return {
        "protocol_version": PROTOCOL_VERSION,
        "game_id": game_id,
        "seq": seq,
        "player": i,
        "turn": v["turn"],
        "phase": v["phase"],
        "timeout_s": timeout,
        "deadline_epoch_s": round(time.time() + timeout, 3),
        "you": v["you"],
        "opponent": v["opponent"],
        "choice": v["choice"],
        "legal_actions": v["legal_actions"],
        "events": engine.take_events(i),
        "last_action_result": last_result,
        "result": engine.result_for(i),
    }


class _Replay:
    def __init__(self, path: Path):
        self.f = open(path, "w", encoding="utf-8", newline="\n")
        self.lock = Lock()

    def write_event(self, event: dict[str, Any]) -> None:
        with self.lock:
            self.f.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")
            self.f.flush()

    def flush(self, engine: Engine) -> None:
        for ev in engine.take_public_events():
            self.write_event(ev)

    def close(self) -> None:
        self.f.close()


def play_game(
    players: dict[int, Player],
    *,
    game_dir: Path,
    game_id: str,
    seed: int,
    config: Config,
) -> dict[str, Any]:
    """Run one game between two constructed Players; returns the result dict (also written to result.json)."""
    game_dir = Path(game_dir)
    game_dir.mkdir(parents=True, exist_ok=False)
    for i in (1, 2):
        (game_dir / f"p{i}").mkdir()
    init_engine()  # one-time card database load, not counted in duration_s
    t_start = time.monotonic()
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    engine: Engine | None = None
    setup_result: tuple[int | None, str] | None = None

    def write_metadata() -> None:
        write_json(game_dir / "game.json", {
            "game_id": game_id,
            "seed": seed,
            "created_at": created_at,
            "runtime_version": RUNTIME_VERSION,
            "protocol_version": PROTOCOL_VERSION,
            "pool_version": POOL_VERSION,
            "fireplace_commit": FIREPLACE_COMMIT,
            "decision_timeout_s": config.decision_timeout_s,
            "illegal_limit": config.illegal_limit,
            "players": [
                {
                    "index": i,
                    "name": players[i].name,
                    "kind": players[i].kind,
                    "hero_class": players[i].deck.hero_class if players[i].deck else None,
                    "deck": list(players[i].deck.cards) if players[i].deck else None,
                }
                for i in (1, 2)
            ],
        })

    write_metadata()
    replay = _Replay(game_dir / "replay.jsonl")
    seq = {1: 0, 2: 0}
    illegal = {1: 0, 2: 0}
    timeouts = {1: 0, 2: 0}
    accepted = {1: 0, 2: 0}
    last_result: dict[int, Any] = {1: None, 2: None}
    crash: EngineCrash | None = None
    started: list[int] = []

    def reject(i: int, d, code: str, message: str, active_engine: Engine | None = None) -> bool:
        illegal[i] += 1
        ev = {"event": "illegal_action", "player": i, "error": code, "illegal_count": illegal[i]}
        if active_engine is None:
            replay.write_event(ev)
        else:
            active_engine.add_event(ev)
        last_result[i] = {
            "accepted": False, "error": code, "message": message,
            "illegal_count": illegal[i], "illegal_limit": config.illegal_limit,
        }
        if illegal[i] >= config.illegal_limit:
            return True
        return False

    def terminal_failure(i: int, d, active_engine: Engine | None = None) -> str | None:
        if d.kind not in ("timeout", "exited", "forfeit"):
            return None
        reason = "forfeit_timeout" if d.kind == "timeout" else "forfeit_exit"
        if d.kind == "timeout":
            timeouts[i] += 1
        event = {"event": "agent_failure", "player": i,
                 "error": "TIMEOUT" if d.kind == "timeout" else "AGENT_EXITED"}
        if active_engine is None:
            replay.write_event(event)
        else:
            active_engine.add_event(event)
        return reason

    def check_exits() -> bool:
        for player in (1, 2):
            stopped = players[player].poll_exit()
            if stopped is not None:
                reason = terminal_failure(player, stopped, engine)
                if reason:
                    engine.forfeit(player, reason)
                    return True
        return False

    def decision_error(i: int, d) -> str:
        return {"seq_mismatch": "SEQ_MISMATCH"}.get(d.kind, "BAD_JSON")

    def submit_deck(i: int) -> tuple[int | None, str] | None:
        events: list[dict[str, Any]] = []
        while not players[i]._decision_cancelled.is_set():
            seq[i] += 1
            state = build_deck_state(game_id, i, seq[i], last_result[i], config, events=events)
            d = players[i].decide(state)
            if players[i]._decision_cancelled.is_set() or d.kind == "cancelled":
                return None
            message = d.message
            failure = terminal_failure(i, d)
            if failure:
                return 3 - i, failure
            if d.kind == "action":
                action = d.action
                if not isinstance(action, dict):
                    code, message = "BAD_JSON", "action must be an object"
                elif action.get("type") == "concede":
                    accepted[i] += 1
                    return 3 - i, "concede"
                elif action.get("type") != "submit_deck":
                    code, message = "WRONG_PHASE", "submit_deck (hero_class, cards) or concede is required before play"
                else:
                    errors = validate_deck_data({"hero_class": action.get("hero_class"), "cards": action.get("cards")})
                    if not errors:
                        # Deck is immutable; only this setup path assigns it. Never read a submission's deck.json.
                        players[i].deck = Deck(action["hero_class"].upper(), tuple(action["cards"]))
                        accepted[i] += 1
                        last_result[i] = None
                        replay.write_event({"event": "deck_submitted", "player": i})
                        return None
                    code, message = "INVALID_DECK", "; ".join(errors)
            else:
                code = decision_error(i, d)
            if reject(i, d, code, message):
                return 3 - i, "forfeit_illegal"
            events = [{"event": "illegal_action", "player": i, "error": code, "illegal_count": illegal[i]}]
        return None

    try:
        for i in (1, 2):
            players[i].start(SeatInfo(game_id=game_id, player=i, seed=seed, player_dir=game_dir / f"p{i}", config=config))
            started.append(i)
        pending_decks = [i for i in (1, 2) if players[i].requires_deck_submission]
        # Both seats receive the setup request without waiting for the other seat's answer.
        with ThreadPoolExecutor(max_workers=2, thread_name_prefix="arena-deck") as pool:
            futures = [pool.submit(submit_deck, i) for i in pending_decks]
            try:
                for future in as_completed(futures):
                    outcome = future.result()
                    if outcome is not None:
                        setup_result = outcome
                        break
            finally:
                if setup_result is not None or any(not f.done() for f in futures):
                    for i in started:
                        players[i].cancel_pending()
        write_metadata()
        if setup_result is None:
            if any(players[i].deck is None for i in (1, 2)):
                raise RuntimeError("both decks must be submitted before the engine starts")
            engine = Engine(players[1].deck, players[2].deck, seed, max_turns=config.max_turns)
        while engine is not None and not engine.over:
            if check_exits():
                break
            i, _phase = engine.pending()
            seq[i] += 1
            state = build_state(engine, game_id, i, seq[i], last_result[i], config)
            replay.flush(engine)
            d = players[i].decide(state)
            message = d.message
            failure = terminal_failure(i, d, engine)
            if failure:
                engine.forfeit(i, failure)
                break
            if check_exits():
                break
            if d.kind == "action":
                try:
                    res = engine.step(i, d.action)
                except EngineCrash as e:
                    crash = e
                    engine.void()
                    break
                if res.accepted:
                    accepted[i] += 1
                    last_result[i] = None
                    replay.flush(engine)
                    continue
                code, message = res.error, res.message
            else:
                code = decision_error(i, d)
            if reject(i, d, code, message, engine):
                engine.forfeit(i)
                break
            replay.flush(engine)
    finally:
        if engine is not None and not engine.over:  # interrupted: agents still get a final state
            engine.abort()
        if engine is None:
            setup_result = setup_result or (None, "aborted")
            replay.write_event({"event": "game_over", "winner": setup_result[0], "reason": setup_result[1]})
        for i in started:
            players[i].cancel_pending()
        for i in started:
            seq[i] += 1
            try:
                if engine is not None:
                    final = build_state(engine, game_id, i, seq[i], last_result[i], config)
                else:
                    winner, reason = setup_result
                    result = {"winner": winner, "you_won": None if winner is None else winner == i, "reason": reason}
                    final = build_deck_state(game_id, i, seq[i], last_result[i], config, result=result,
                                             events=[{"event": "game_over", "winner": winner, "reason": reason}])
                players[i].game_over(final)
            except Exception:
                pass
        for i in started:
            try:
                players[i].stop()
            except Exception:
                pass
        if engine is not None:
            replay.flush(engine)
        replay.close()
        write_metadata()

    result: dict[str, Any] = {
        "game_id": game_id,
        "seed": seed,
        "winner": engine.winner if engine else setup_result[0],
        "reason": engine.reason if engine else setup_result[1],
        "first_player": engine.first_player if engine else None,
        "turns": engine.turn if engine else 0,
        "illegal_counts": {"1": illegal[1], "2": illegal[2]},
        "restarts": {"1": players[1].restarts, "2": players[2].restarts},
        "timeouts": {"1": timeouts[1], "2": timeouts[2]},
        "duration_s": round(time.monotonic() - t_start, 3),
        "decisions": {"1": accepted[1], "2": accepted[2]},
        "players": [{"index": i, "name": players[i].name, "kind": players[i].kind} for i in (1, 2)],
    }
    notes = {str(i): list(players[i].notes) for i in (1, 2) if players[i].notes}
    if notes:
        result["notes"] = notes
    if crash is not None:
        result["engine_error"] = {"message": str(crash), "card_ids": crash.card_ids}
        with open(game_dir / "engine_errors.log", "w", encoding="utf-8", newline="\n") as f:
            f.write(f"game_id: {game_id}\nseed: {seed}\n")
            f.write(f"action: {json.dumps(crash.action)}\n")
            f.write(f"card_ids: {' '.join(crash.card_ids)}\n")
            f.write(f"error: {crash}\n\n{crash.traceback}\n")
    write_json(game_dir / "result.json", result)
    return result


def run_game(
    p1: str,
    p2: str,
    *,
    game_dir: str | Path,
    game_id: str,
    seed: int,
    config: Config | None = None,
) -> dict[str, Any]:
    """Build players from specs (see hs_arena.agents) and play one game."""
    config = config or Config()
    players = {1: make_player(p1, 1, seed), 2: make_player(p2, 2, seed)}
    return play_game(players, game_dir=Path(game_dir), game_id=game_id, seed=seed, config=config)
