"""Card catalog: generation of ``data/cards.json`` from the vendored card XML, and loading it at run time.

Loading the catalog does not touch the fireplace engine, so it is cheap and safe to use from agents::

    from hs_arena import cards
    catalog = cards.load()          # {card_id: {...}} for every pool card
    catalog["CS2_029"]["text"]      # 'Deal 6 damage.'
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import Any

from . import FIREPLACE_COMMIT, POOL_VERSION
from ._fileio import load_json, write_json
from ._resources import CARD_DEFS_XML, CARDS_JSON, EXCLUDED_JSON
from .pool import exclusion_reason

# GameTag name -> mechanic keyword exported in cards.json
MECHANIC_TAGS = {
    "TAUNT": "TAUNT",
    "CHARGE": "CHARGE",
    "DIVINE_SHIELD": "DIVINE_SHIELD",
    "BATTLECRY": "BATTLECRY",
    "DEATHRATTLE": "DEATHRATTLE",
    "WINDFURY": "WINDFURY",
    "STEALTH": "STEALTH",
    "SECRET": "SECRET",
    "FREEZE": "FREEZE",
    "SPELLPOWER": "SPELL_DAMAGE",
    "ENRAGED": "ENRAGE",
    "COMBO": "COMBO",
    "OVERLOAD": "OVERLOAD",
    "POISONOUS": "POISONOUS",
    "SILENCE": "SILENCE",
    "AURA": "AURA",
    "CHOOSE_ONE": "CHOOSE_ONE",
    "LIFESTEAL": "LIFESTEAL",
    "ADJACENT_BUFF": "ADJACENT_BUFF",
    "CANT_ATTACK": "CANT_ATTACK",
    "TRIGGER_VISUAL": "TRIGGER",
    "DISCARD_CARDS": "DISCARD",
    "AFFECTED_BY_SPELL_POWER": "AFFECTED_BY_SPELL_DAMAGE",
    "ImmuneToSpellpower": "IMMUNE_TO_SPELL_DAMAGE",
    "CANT_BE_TARGETED_BY_SPELLS": "ELUSIVE",
    "CANT_BE_TARGETED_BY_HERO_POWERS": "CANT_BE_TARGETED_BY_HERO_POWERS",
    "DISCOVER": "DISCOVER",
}

_TAG_RE = re.compile(r"</?[a-zA-Z]+>")
_WS_RE = re.compile(r"\s+")
_NUM_MARK_RE = re.compile(r"[$#](\d+)")


def plain_text(text: str | None) -> str:
    """Strip card-text markup: <b>/<i> tags, [x], $N/#N damage/heal markers, '_' non-breaking spaces, and the
    alternate text after '@' (e.g. Steady Shot: "Deal $2 damage to the enemy hero.@<b>Hero Power</b>...")."""
    if not text:
        return ""
    s = text.split("@", 1)[0].replace("[x]", "")
    s = _TAG_RE.sub("", s)
    s = _NUM_MARK_RE.sub(r"\1", s)
    s = s.replace("_", " ").replace("\n", " ")
    return _WS_RE.sub(" ", s).strip()


def _enum_name(value: Any) -> str:
    return getattr(value, "name", str(value))


def _card_entry(c) -> dict[str, Any]:
    card_type = _enum_name(c.type)
    entry: dict[str, Any] = {
        "id": c.id,
        "name": c.name,
        "card_class": _enum_name(c.card_class),
        "type": card_type,
        "rarity": _enum_name(c.rarity),
        "cost": int(c.cost),
    }
    if card_type == "MINION":
        entry["attack"] = int(c.atk)
        entry["health"] = int(c.health)
        race = _enum_name(c.race)
        if race not in ("INVALID", "BLANK"):
            entry["race"] = race
    elif card_type == "WEAPON":
        entry["attack"] = int(c.atk)
        entry["durability"] = int(c.durability)
    entry["text"] = plain_text(c.description)
    mechanics = []
    for tag, value in c.tags.items():
        name = getattr(tag, "name", None)
        if value and name in MECHANIC_TAGS:
            mechanics.append(MECHANIC_TAGS[name])
    entry["mechanics"] = sorted(set(mechanics))
    entry["set"] = _enum_name(c.card_set)
    return entry


def _sort_key(entry: dict[str, Any]):
    return (entry["card_class"] == "NEUTRAL", entry["card_class"], entry["cost"], entry["name"], entry["id"])


def generate(xml_path=CARD_DEFS_XML) -> tuple[dict[str, Any], dict[str, Any]]:
    """Build (cards_doc, excluded_doc) from the card XML. Does not initialise the fireplace engine."""
    from hearthstone import cardxml

    db, _ = cardxml.load(path=str(xml_path), locale="enUS")
    pool: list[dict[str, Any]] = []
    excluded: dict[str, dict[str, Any]] = {}
    for card_id, c in db.items():
        if not c.collectible:
            continue
        reason = exclusion_reason(
            collectible=bool(c.collectible),
            card_set=_enum_name(c.card_set),
            card_type=_enum_name(c.type),
            card_class=_enum_name(c.card_class),
            card_id=card_id,
        )
        if reason is None:
            pool.append(_card_entry(c))
        else:
            excluded[card_id] = {
                "name": c.name,
                "set": _enum_name(c.card_set),
                "card_class": _enum_name(c.card_class),
                "reason": reason,
            }
    pool.sort(key=_sort_key)
    cards_doc = {
        "pool_version": POOL_VERSION,
        "source": f"fireplace {FIREPLACE_COMMIT} CardDefs.xml",
        "count": len(pool),
        "cards": pool,
    }
    excluded_doc = {
        "pool_version": POOL_VERSION,
        "cards": dict(sorted(excluded.items())),
    }
    return cards_doc, excluded_doc


def write_generated(cards_path=CARDS_JSON, excluded_path=EXCLUDED_JSON) -> dict[str, Any]:
    cards_doc, excluded_doc = generate()
    cards_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(cards_path, cards_doc, indent=1)
    write_json(excluded_path, excluded_doc, indent=1)
    load.cache_clear()
    load_excluded.cache_clear()
    return cards_doc


@lru_cache(maxsize=1)
def load() -> dict[str, dict[str, Any]]:
    """Return the pool catalog {card_id: card} (same content as data/cards.json)."""
    doc = load_json(CARDS_JSON)
    return {c["id"]: c for c in doc["cards"]}


@lru_cache(maxsize=1)
def load_excluded() -> dict[str, dict[str, Any]]:
    """Collectible cards that are not in the pool, with the reason (used for precise deck errors)."""
    if not EXCLUDED_JSON.exists():
        return {}
    return load_json(EXCLUDED_JSON)["cards"]


def card_pool_markdown(cards_doc: dict[str, Any]) -> str:
    """Render docs/card_pool.md."""
    lines = [
        "# Card pool",
        "",
        f"Pool version `{cards_doc['pool_version']}`: **{cards_doc['count']} cards** — every collectible Basic and "
        "Classic card of the nine classic classes in the pinned fireplace card data, minus Hall of Fame cards and "
        "`pool/blacklist.txt`. Generated from `data/cards.json` (do not edit by hand).",
        "",
        "Deck rules: exactly 30 cards; class cards only from your `hero_class` or NEUTRAL; at most 2 copies of a "
        "card; at most 1 copy of a LEGENDARY.",
        "",
    ]
    by_class: dict[str, list[dict[str, Any]]] = {}
    for c in cards_doc["cards"]:
        by_class.setdefault(c["card_class"], []).append(c)
    for cls, items in by_class.items():
        lines.append(f"## {cls.title()} ({len(items)})")
        lines.append("")
        lines.append("| Cost | Id | Name | Type | Rarity | Stats | Text |")
        lines.append("|-----:|----|------|------|--------|-------|------|")
        for c in items:
            if c["type"] == "MINION":
                stats = f"{c['attack']}/{c['health']}"
            elif c["type"] == "WEAPON":
                stats = f"{c['attack']}/{c['durability']}"
            else:
                stats = ""
            text = c["text"].replace("|", "\\|")
            lines.append(
                f"| {c['cost']} | `{c['id']}` | {c['name']} | {c['type'].title()} | {c['rarity'].title()} | {stats} | {text} |"
            )
        lines.append("")
    return "\n".join(lines)
