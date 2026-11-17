"""Engine-level helpers for the property and stability tests (importable by spawned worker processes)."""

from __future__ import annotations

import copy
import random
import tempfile
from pathlib import Path
from typing import Any

from hs_arena._fp import init_engine
from hs_arena.agents.random_bot import instantiate
from hs_arena.deck import random_deck
from hs_arena.engine import Engine, EngineCrash


def all_instantiations(t: dict[str, Any]) -> list[dict[str, Any]]:
    """Every allowed parameter value of a template at least once."""
    tt = t["type"]
    out: list[dict[str, Any]] = []
    if tt in ("play_card", "hero_power"):
        base: dict[str, Any] = {"type": tt}
        if tt == "play_card":
            base["card"] = t["card"]
        variants = []
        if t.get("choose"):
            for o in t["choose"]:
                variants.append(({"choose": o["entity_id"]}, o.get("targets")))
        else:
            variants.append(({}, t.get("targets")))
        positions = t.get("positions")
        for extra, targets in variants:
            if targets:
                for x in targets:
                    out.append(dict(base, **extra, target=x))
            else:
                out.append(dict(base, **extra))
            if positions:
                for p in positions:
                    a = dict(base, **extra, position=p)
                    if targets:
                        a["target"] = targets[0]
                    out.append(a)
        return out
    if tt == "attack":
        return [{"type": tt, "attacker": t["attacker"], "target": x} for x in t["targets"]]
    if tt == "mulligan":
        opts = t["options"]
        subsets = [[], list(opts)] + [[o] for o in opts]
        return [{"type": tt, "replace": s} for s in subsets if t["min"] <= len(s) <= t["max"]]
    if tt == "choose":
        return [{"type": tt, "options": [o["entity_id"]]} for o in t["options"]]
    return [{"type": tt}]


def invalid_actions(engine: Engine, i: int, legal: list[dict[str, Any]]) -> list[tuple[Any, str]]:
    """(action, expected error code) pairs that must be rejected at this decision point."""
    _, phase = engine.pending()
    pl = engine.player(i)
    bad = 999_999
    out: list[tuple[Any, str]] = [
        ("end_turn", "BAD_JSON"),
        ({"type": "dance"}, "UNKNOWN_ACTION_TYPE"),
        ({}, "UNKNOWN_ACTION_TYPE"),
    ]
    if phase == "mulligan":
        t = next(t for t in legal if t["type"] == "mulligan")
        out += [
            ({"type": "end_turn"}, "WRONG_PHASE"),
            ({"type": "play_card", "card": t["options"][0]}, "WRONG_PHASE"),
            ({"type": "mulligan", "replace": [bad]}, "ILLEGAL_CHOICE"),
            ({"type": "mulligan", "replace": [t["options"][0], t["options"][0]]}, "ILLEGAL_CHOICE"),
            ({"type": "mulligan", "replace": "all"}, "ILLEGAL_CHOICE"),
            ({"type": "choose", "options": [t["options"][0]]}, "WRONG_PHASE"),
        ]
        return out
    if phase == "choice":
        t = next(t for t in legal if t["type"] == "choose")
        out += [
            ({"type": "end_turn"}, "WRONG_PHASE"),
            ({"type": "choose", "options": [bad]}, "ILLEGAL_CHOICE"),
            ({"type": "choose", "options": []}, "ILLEGAL_CHOICE"),
            ({"type": "choose"}, "ILLEGAL_CHOICE"),
            ({"type": "mulligan", "replace": []}, "WRONG_PHASE"),
        ]
        return out
    out += [
        ({"type": "mulligan", "replace": []}, "WRONG_PHASE"),
        ({"type": "choose", "options": [1]}, "WRONG_PHASE"),
        ({"type": "play_card", "card": bad}, "NOT_YOUR_ENTITY"),
        ({"type": "play_card", "card": "88"}, "NOT_YOUR_ENTITY"),
        ({"type": "play_card", "card": pl.opponent.hero.entity_id}, "NOT_YOUR_ENTITY"),
        ({"type": "attack", "attacker": bad, "target": pl.opponent.hero.entity_id}, "NOT_YOUR_ENTITY"),
    ]
    for m in pl.opponent.field:
        out.append(({"type": "attack", "attacker": m.entity_id, "target": pl.hero.entity_id}, "NOT_YOUR_ENTITY"))
        break
    playable = {t["card"] for t in legal if t["type"] == "play_card"}
    for c in pl.hand:
        if c.entity_id not in playable:
            out.append(({"type": "play_card", "card": c.entity_id}, "CARD_NOT_PLAYABLE"))
            break
    attackers = {t["attacker"] for t in legal if t["type"] == "attack"}
    for ch in pl.characters:
        if ch.entity_id not in attackers:
            out.append(({"type": "attack", "attacker": ch.entity_id, "target": pl.opponent.hero.entity_id}, "CANNOT_ATTACK"))
            break
    if not any(t["type"] == "hero_power" for t in legal):
        out.append(({"type": "hero_power"}, "HERO_POWER_UNUSABLE"))
    for t in legal:
        if t["type"] == "play_card":
            if t["choose"]:
                out.append(({"type": "play_card", "card": t["card"]}, "CHOOSE_REQUIRED"))
                out.append(({"type": "play_card", "card": t["card"], "choose": bad}, "ILLEGAL_CHOICE"))
                continue
            out.append(({"type": "play_card", "card": t["card"], "choose": 1}, "ILLEGAL_CHOICE"))
            if t["targets"]:
                out.append(({"type": "play_card", "card": t["card"]}, "TARGET_REQUIRED"))
                out.append(({"type": "play_card", "card": t["card"], "target": bad}, "ILLEGAL_TARGET"))
            else:
                out.append(({"type": "play_card", "card": t["card"], "target": pl.hero.entity_id}, "ILLEGAL_TARGET"))
            if t["positions"] is None:
                if not t["targets"]:
                    out.append(({"type": "play_card", "card": t["card"], "position": 0}, "ILLEGAL_POSITION"))
            elif not t["targets"]:
                out.append(({"type": "play_card", "card": t["card"], "position": 99}, "ILLEGAL_POSITION"))
                out.append(({"type": "play_card", "card": t["card"], "position": -1}, "ILLEGAL_POSITION"))
        elif t["type"] == "attack":
            out.append(({"type": "attack", "attacker": t["attacker"]}, "TARGET_REQUIRED"))
            out.append(({"type": "attack", "attacker": t["attacker"], "target": bad}, "ILLEGAL_TARGET"))
            out.append(({"type": "attack", "attacker": t["attacker"], "target": t["attacker"]}, "ILLEGAL_TARGET"))
        elif t["type"] == "hero_power":
            if t["targets"]:
                out.append(({"type": "hero_power"}, "TARGET_REQUIRED"))
                out.append(({"type": "hero_power", "target": bad}, "ILLEGAL_TARGET"))
            elif not t.get("choose"):
                out.append(({"type": "hero_power", "target": pl.hero.entity_id}, "ILLEGAL_TARGET"))
    return out


def property_worker(seed: int, max_points: int) -> dict[str, Any]:
    """Play one random game; at each decision point try every template instantiation on a copy of the engine."""
    cards = init_engine()
    memo_base = {id(c): c for c in cards.db.values()}
    rng = random.Random(seed)
    engine = Engine(random_deck(rng), random_deck(rng), seed)
    stats = {"points": 0, "valid": 0, "invalid": 0, "failures": []}
    while not engine.over and stats["points"] < max_points:
        i, _ = engine.pending()
        legal = engine.legal_actions(i)
        stats["points"] += 1
        for t in legal:
            for a in all_instantiations(t):
                clone = copy.deepcopy(engine, dict(memo_base))
                try:
                    r = clone.step(i, a)
                except EngineCrash as e:
                    stats["failures"].append({"seed": seed, "action": a, "crash": str(e), "cards": e.card_ids})
                    continue
                stats["valid"] += 1
                if not r.accepted:
                    stats["failures"].append({"seed": seed, "action": a, "rejected": [r.error, r.message]})
        for a, code in invalid_actions(engine, i, legal):
            r = engine.validate(i, a)
            stats["invalid"] += 1
            if r.accepted or r.error != code:
                stats["failures"].append({"seed": seed, "action": a, "expected": code, "got": [r.error, r.message]})
        templates = [t for t in legal if t["type"] != "concede"]
        engine.step(i, instantiate(rng.choice(templates), rng))
    return stats


def stability_worker(args: tuple[str, int, int]) -> dict[str, Any]:
    """Play bot games in-process via the runner; returns per-game summaries (engine errors included)."""
    kind, start, count = args
    from hs_arena.agents import GreedyBot, RandomBot
    from hs_arena.protocol import Config
    from hs_arena.runner import play_game

    init_engine()
    out = []
    with tempfile.TemporaryDirectory(prefix="hs-stab-") as tmp:
        for seed in range(start, start + count):
            rng = random.Random(seed)
            d1, d2 = random_deck(rng), random_deck(rng)
            if kind == "random":
                players = {1: RandomBot("random", d1), 2: RandomBot("random", d2)}
            elif kind == "greedy":
                players = {1: GreedyBot("greedy", d1), 2: GreedyBot("greedy", d2)}
            else:
                raise ValueError(kind)
            cfg = Config(keep_decisions=False)
            r = play_game(players, game_dir=Path(tmp) / f"g{seed}", game_id=f"g{seed}", seed=seed, config=cfg)
            out.append(
                {
                    "seed": seed,
                    "reason": r["reason"],
                    "winner": r["winner"],
                    "illegal": r["illegal_counts"],
                    "duration_s": r["duration_s"],
                    "engine_error": r.get("engine_error"),
                    "classes": (d1.hero_class, d2.hero_class),
                }
            )
    return {"kind": kind, "games": out}
