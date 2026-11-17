"""Card pool rules: Basic + Classic collectible cards of the nine classic classes, minus the blacklist."""

from __future__ import annotations

from functools import lru_cache

from . import POOL_VERSION
from ._resources import BLACKLIST_TXT

# hearthstone.enums names; "Basic" is CardSet.BASIC (CardSet.CORE is the 2021 Core set), Classic is EXPERT1.
POOL_SETS = ("BASIC", "EXPERT1")
HALL_OF_FAME_SET = "HOF"

# The nine classic classes and their default heroes.
HERO_FOR_CLASS = {
    "DRUID": "HERO_06",
    "HUNTER": "HERO_05",
    "MAGE": "HERO_08",
    "PALADIN": "HERO_04",
    "PRIEST": "HERO_09",
    "ROGUE": "HERO_03",
    "SHAMAN": "HERO_02",
    "WARLOCK": "HERO_07",
    "WARRIOR": "HERO_01",
}
HERO_CLASSES = tuple(sorted(HERO_FOR_CLASS))
CLASS_FOR_HERO = {v: k for k, v in HERO_FOR_CLASS.items()}
CARD_CLASSES = HERO_CLASSES + ("NEUTRAL",)

DECK_SIZE = 30
MAX_COPIES = 2
MAX_LEGENDARY_COPIES = 1

__all__ = [
    "POOL_VERSION",
    "POOL_SETS",
    "HERO_FOR_CLASS",
    "HERO_CLASSES",
    "CARD_CLASSES",
    "DECK_SIZE",
    "MAX_COPIES",
    "MAX_LEGENDARY_COPIES",
    "load_blacklist",
    "exclusion_reason",
]


@lru_cache(maxsize=1)
def load_blacklist() -> dict[str, str]:
    """Return {card_id: reason} from pool/blacklist.txt.

    Format: one card per line, ``CARD_ID  # reason``; blank lines and lines starting with ``#`` are ignored.
    """
    result: dict[str, str] = {}
    if not BLACKLIST_TXT.exists():
        return result
    for raw in BLACKLIST_TXT.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        card_id, _, reason = line.partition("#")
        card_id = card_id.strip()
        if card_id:
            result[card_id] = reason.strip() or "blacklisted"
    return result


def exclusion_reason(*, collectible: bool, card_set: str, card_type: str, card_class: str, card_id: str) -> str | None:
    """Why a card is not in the pool (None if it is in the pool). Used by cards.json generation."""
    if not collectible:
        return "not_collectible"
    if card_type == "HERO":
        return "hero_card"
    if card_set == HALL_OF_FAME_SET:
        return "hall_of_fame"
    if card_set not in POOL_SETS:
        return "not_basic_or_classic"
    if card_class not in CARD_CLASSES:
        return "class_not_supported"
    if card_id in load_blacklist():
        return "blacklisted"
    return None
