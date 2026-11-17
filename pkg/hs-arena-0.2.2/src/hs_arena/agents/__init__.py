"""Players: skill seats (student submissions), client seats, process agents and the built-in bots.

Player specs used by the CLI and the runner:

- ``skill:<dir>`` (or ``<dir>`` containing SKILL.md)   a skill, played by the course agent (hs_arena.skill)
- ``client:<dir>``                     a seat driven by an MCP client program (<dir>/client.py)
- ``mcp:<workspace>``                  an external agent (no skill/model/deck loading by the host)
- ``random`` / ``random:<deck.json>``  built-in random bot (default deck: a seeded random pool deck)
- ``greedy`` / ``greedy:<deck.json>``  built-in greedy bot (default deck: decks/greedy_mage.json)
- ``<dir>`` with manifest.json         a process agent speaking the file protocol (course-internal)
"""

from __future__ import annotations

import random
from pathlib import Path

from .._resources import GREEDY_DECK
from ..deck import load_deck, load_submission, random_deck
from .base import Decision, Player, SeatInfo
from .greedy_bot import GreedyBot
from .process import ProcessAgent
from .random_bot import RandomBot

__all__ = ["Decision", "Player", "SeatInfo", "GreedyBot", "RandomBot", "ProcessAgent", "make_player", "BUILTIN_KINDS",
           "spec_kind"]

BUILTIN_KINDS = ("random", "greedy")
SEAT_PREFIXES = ("skill", "client", "mcp")


def _split(spec: str) -> tuple[str, str | None]:
    for kind in BUILTIN_KINDS + SEAT_PREFIXES:
        if spec == kind and kind in BUILTIN_KINDS:
            return kind, None
        if spec.startswith(kind + ":"):
            return kind, spec[len(kind) + 1 :]
    if (Path(spec) / "SKILL.md").exists():
        return "skill", spec
    return "process", spec


def spec_kind(spec: str) -> str:
    """'random' | 'greedy' | 'skill' | 'client' | 'process'."""
    return _split(spec)[0]


def is_builtin(spec: str) -> bool:
    return _split(spec)[0] in BUILTIN_KINDS


def spec_path(spec: str) -> str | None:
    kind, arg = _split(spec)
    return None if kind in BUILTIN_KINDS else arg


def make_player(spec: str, player: int, seed: int) -> Player:
    """Build a Player from a spec; raises DeckError / SubmissionError / SkillError for invalid inputs."""
    kind, arg = _split(spec)
    if kind == "random":
        deck = load_deck(arg) if arg else random_deck(random.Random(seed * 1000003 + player))
        return RandomBot("random", deck)
    if kind == "greedy":
        deck = load_deck(arg) if arg else load_deck(GREEDY_DECK)
        return GreedyBot("greedy", deck)
    if kind == "skill":
        from ..skill import load_skill
        from ..skill.seat import SkillSeat

        return SkillSeat(load_skill(arg))
    if kind == "client":
        from ..skill.seat import ClientSeat

        return ClientSeat(arg)
    if kind == "mcp":
        from ..skill.seat import McpSeat

        return McpSeat(arg)
    sub = load_submission(Path(arg))
    return ProcessAgent(sub)
