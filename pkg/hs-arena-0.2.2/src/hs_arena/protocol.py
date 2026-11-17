"""Protocol constants (see docs/protocol.md) and schema access."""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from . import POOL_VERSION, PROTOCOL_VERSION, RUNTIME_VERSION
from ._resources import SCHEMA_DIR

__all__ = [
    "PROTOCOL_VERSION",
    "POOL_VERSION",
    "RUNTIME_VERSION",
    "PHASES",
    "ACTION_TYPES",
    "PHASE_ACTIONS",
    "ERROR_CODES",
    "RESULT_REASONS",
    "Config",
    "load_schema",
    "SCHEMA_NAMES",
]

PHASES = ("deck_submission", "mulligan", "main", "choice", "game_over")

ACTION_TYPES = ("play_card", "attack", "hero_power", "end_turn", "concede", "mulligan", "choose", "submit_deck")

PHASE_ACTIONS = {
    "deck_submission": ("submit_deck", "concede"),
    "mulligan": ("mulligan", "concede"),
    "choice": ("choose", "concede"),
    "main": ("play_card", "attack", "hero_power", "end_turn", "concede"),
    "game_over": (),
}

# Action fields that are kept (and logged); anything else in an action is dropped.
ACTION_FIELDS = {
    "submit_deck": ("type", "hero_class", "cards"),
    "play_card": ("type", "card", "target", "position", "choose"),
    "attack": ("type", "attacker", "target"),
    "hero_power": ("type", "target", "choose"),
    "end_turn": ("type",),
    "concede": ("type",),
    "mulligan": ("type", "replace"),
    "choose": ("type", "options"),
}

ERROR_CODES = (
    "INVALID_DECK",
    "BAD_JSON",
    "SEQ_MISMATCH",
    "WRONG_PHASE",
    "UNKNOWN_ACTION_TYPE",
    "NOT_YOUR_ENTITY",
    "CARD_NOT_PLAYABLE",
    "TARGET_REQUIRED",
    "ILLEGAL_TARGET",
    "ILLEGAL_POSITION",
    "CHOOSE_REQUIRED",
    "ILLEGAL_CHOICE",
    "CANNOT_ATTACK",
    "HERO_POWER_UNUSABLE",
    "AGENT_EXITED",
    "TIMEOUT",
)

RESULT_REASONS = (
    "hero_death", "draw", "forfeit_illegal", "forfeit_timeout", "forfeit_exit", "forfeit_restart", "concede", "void_engine_error", "max_turns", "aborted",
)

SCHEMA_NAMES = ("state", "action", "manifest", "game", "result")


@dataclass
class Config:
    """Runtime knobs (PLANNING.md §9)."""

    decision_timeout_s: float = 180.0
    max_turns: int | None = None
    exit_grace_s: float = 10.0
    poll_interval_ms: int = 50
    illegal_limit: int = 3  # forfeits on reaching this count, not on exceeding it
    parallel: int = 4
    stderr_cap_kb: int = 512
    keep_decisions: bool = True


def sanitize_action(action: Any) -> Any:
    """Drop unknown fields from an action so that nothing else (reasoning, prompts) is ever logged."""
    if not isinstance(action, dict):
        return None
    fields = ACTION_FIELDS.get(action.get("type"))
    if fields is None:
        t = action.get("type")
        return {"type": t} if isinstance(t, (str, int, float, bool)) or t is None else {"type": None}
    return {k: action[k] for k in fields if k in action}


@lru_cache(maxsize=None)
def load_schema(name: str) -> dict[str, Any]:
    with open(SCHEMA_DIR / f"{name}.schema.json", "r", encoding="utf-8") as f:
        return json.load(f)
