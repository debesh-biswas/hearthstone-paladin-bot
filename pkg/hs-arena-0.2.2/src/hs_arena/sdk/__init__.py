"""Student SDK: a polling loop around the state.json / action.json protocol, typed state access, action builders.

    from hs_arena.sdk import Agent, State, Action, run

    class MyAgent(Agent):
        def decide(self, state: State) -> Action:
            return Action.end_turn()

    if __name__ == "__main__":
        run(MyAgent)

The SDK contains no LLM client and no network code; call your model with any HTTP library you like.
The Agent instance lives for the whole game, so memory is simply instance state (plus HS_WORK_DIR for files).
"""

from __future__ import annotations

import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .._fileio import atomic_write_json, read_text
from .text import event_text, state_to_text

__all__ = ["Agent", "State", "Action", "GameInfo", "Result", "View", "run", "event_text"]


def _wrap(value: Any) -> Any:
    if isinstance(value, dict) and not isinstance(value, View):
        return View(value)
    if isinstance(value, list):
        return [_wrap(v) for v in value]
    return value


class View(dict):
    """A dict with attribute access (recursively): ``state.you.hand[0].name == state["you"]["hand"][0]["name"]``."""

    def __init__(self, data: dict[str, Any] | None = None):
        super().__init__()
        for k, v in (data or {}).items():
            dict.__setitem__(self, k, _wrap(v))

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name) from None


class State(View):
    """Wraps one state.json. Every field of the protocol is available as an attribute (see docs/protocol.md)."""

    @property
    def deadline(self) -> float:
        """Wall-clock deadline (time.time() epoch seconds) by which action.json must exist."""
        return float(self["deadline_epoch_s"])

    def seconds_left(self) -> float:
        return self.deadline - time.time()

    def legal(self, type_: str | None = None) -> list[View]:
        """Legal-action templates, optionally only those of one type."""
        return [t for t in self["legal_actions"] if type_ is None or t["type"] == type_]

    def entity(self, entity_id: int) -> View | None:
        """Find a visible entity (heroes, hero powers, weapons, hand, boards, secrets) by entity id."""
        for side in (self["you"], self["opponent"]):
            if side is None:
                continue
            for key in ("hero", "hero_power", "weapon"):
                e = side.get(key)
                if e and e.get("entity_id") == entity_id:
                    return e
            for key in ("hand", "board", "secrets"):
                for e in side.get(key) or []:
                    if e.get("entity_id") == entity_id:
                        return e
        return None

    def to_text(self) -> str:
        """Compact, deterministic text rendering of the state and legal actions (suitable for a prompt)."""
        return state_to_text(self)


class GameInfo(View):
    """game_id, player (1|2), protocol_version, work_dir, hero_class, deck (your 30 card ids, sorted)."""


class Result(View):
    """winner (1|2|None), you_won (True|False|None), reason; `state` is the final State."""


def _ref_id(x: Any) -> Any:
    if isinstance(x, dict):
        return x.get("entity_id")
    return x


class Action(dict):
    """A concrete action (a dict, serialised as the "action" object of action.json)."""

    @staticmethod
    def submit_deck(hero_class: str, cards: Iterable[str]) -> "Action":
        return Action(type="submit_deck", hero_class=hero_class, cards=list(cards))

    @staticmethod
    def play_card(card: Any, target: Any = None, position: int | None = None, choose: Any = None) -> "Action":
        a = Action(type="play_card", card=_ref_id(card))
        if target is not None:
            a["target"] = _ref_id(target)
        if position is not None:
            a["position"] = int(position)
        if choose is not None:
            a["choose"] = _ref_id(choose)
        return a

    @staticmethod
    def attack(attacker: Any, target: Any) -> "Action":
        return Action(type="attack", attacker=_ref_id(attacker), target=_ref_id(target))

    @staticmethod
    def hero_power(target: Any = None, choose: Any = None) -> "Action":
        a = Action(type="hero_power")
        if target is not None:
            a["target"] = _ref_id(target)
        if choose is not None:
            a["choose"] = _ref_id(choose)
        return a

    @staticmethod
    def end_turn() -> "Action":
        return Action(type="end_turn")

    @staticmethod
    def concede() -> "Action":
        return Action(type="concede")

    @staticmethod
    def mulligan(replace: Iterable[Any] = ()) -> "Action":
        return Action(type="mulligan", replace=[_ref_id(x) for x in replace])

    @staticmethod
    def choose(options: Any) -> "Action":
        if not isinstance(options, (list, tuple)):
            options = [options]
        return Action(type="choose", options=[_ref_id(x) for x in options])

    def to_dict(self) -> dict[str, Any]:
        return dict(self)


class Agent:
    """Subclass and implement decide(). One instance lives for the whole game."""

    def on_game_start(self, info: GameInfo) -> None:
        """Optional: called once before the first decide()."""

    def decide(self, state: State) -> Action:  # pragma: no cover - abstract
        raise NotImplementedError

    def on_game_over(self, result: Result) -> None:
        """Optional: called with the final result; the process exits right after."""


def _env_path(name: str) -> Path:
    value = os.environ.get(name)
    if not value:
        sys.stderr.write(
            f"hs_arena.sdk.run: environment variable {name} is not set; agents are started by the hs-arena runtime\n"
        )
        raise SystemExit(2)
    return Path(value)


def _read_state(path: Path) -> dict[str, Any] | None:
    import json

    text = read_text(path)
    if text is None:
        return None
    try:
        data = json.loads(text)
    except ValueError:
        return None
    return data if isinstance(data, dict) else None


def _game_info(state: dict[str, Any], work_dir: Path) -> GameInfo:
    you = state.get("you") or {}
    deck = Counter(you.get("deck_remaining_counts") or {})
    for c in you.get("hand") or []:
        deck[c["card_id"]] += 1
    cards = sorted(deck.elements())
    return GameInfo(
        {
            "game_id": state.get("game_id"),
            "player": state.get("player"),
            "protocol_version": state.get("protocol_version"),
            "work_dir": str(work_dir),
            "hero_class": (you.get("hero") or {}).get("hero_class"),
            "deck": cards,
        }
    )


def run(agent: Any, *, poll_interval: float = 0.05) -> int:
    """Play one game: poll state.json, call decide(), write action.json atomically, return on game_over.

    `agent` is an Agent subclass (instantiated with no arguments) or an Agent instance.
    Exceptions raised by your code are not caught: the process exits and immediately forfeits
    the game (forfeit_exit). The runtime does not restart it.
    """
    if isinstance(agent, type):
        agent = agent()
    state_path = _env_path("HS_STATE_FILE")
    action_path = _env_path("HS_ACTION_FILE")
    work_dir = Path(os.environ.get("HS_WORK_DIR", "."))
    parent = os.getppid() if os.name == "posix" else None
    last_seq = 0
    started = False
    while True:
        data = _read_state(state_path)
        if data is None or not isinstance(data.get("seq"), int) or data["seq"] <= last_seq:
            if parent is not None and os.getppid() != parent:
                return 1  # the runtime is gone
            time.sleep(poll_interval)
            continue
        last_seq = data["seq"]
        state = State(data)
        if not started:
            started = True
            agent.on_game_start(_game_info(data, work_dir))
        if state["phase"] == "game_over":
            r = dict(state.get("result") or {})
            r["state"] = state
            agent.on_game_over(Result(r))
            return 0
        action = agent.decide(state)
        if isinstance(action, dict):
            payload = dict(action)
        else:
            raise TypeError(f"decide() must return an Action (dict), got {type(action).__name__}")
        atomic_write_json(action_path, {"seq": state["seq"], "action": payload})
