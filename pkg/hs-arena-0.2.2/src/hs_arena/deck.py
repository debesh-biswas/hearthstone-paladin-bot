"""deck.json and manifest.json loading and validation, with precise error messages."""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import POOL_VERSION, PROTOCOL_VERSION
from . import cards as cards_mod
from .pool import (
    CLASS_FOR_HERO,
    DECK_SIZE,
    HERO_CLASSES,
    HERO_FOR_CLASS,
    MAX_COPIES,
    MAX_LEGENDARY_COPIES,
    load_blacklist,
)

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.\-]{0,63}$")


class DeckError(ValueError):
    """Raised by load_deck() when a deck is invalid; .errors lists every problem."""

    def __init__(self, errors: list[str]):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class Deck:
    hero_class: str
    cards: tuple[str, ...]
    name: str | None = None

    @property
    def hero_id(self) -> str:
        return HERO_FOR_CLASS[self.hero_class]

    def to_json(self) -> dict[str, Any]:
        return {"hero_class": self.hero_class, "cards": list(self.cards)}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _card_label(card_id: str) -> str:
    c = cards_mod.load().get(card_id) or cards_mod.load_excluded().get(card_id)
    return f"'{card_id}' ({c['name']})" if c else f"'{card_id}'"


def validate_deck_data(data: Any) -> list[str]:
    """Return the list of problems with a deck.json document (empty if valid)."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["deck.json must be a JSON object with 'hero_class' and 'cards'"]
    hero_class = data.get("hero_class")
    if hero_class is None:
        errors.append("deck.json: missing field 'hero_class'")
    elif not isinstance(hero_class, str) or hero_class.upper() not in HERO_CLASSES:
        errors.append(f"deck.json: hero_class {hero_class!r} is not one of {', '.join(HERO_CLASSES)}")
        hero_class = None
    else:
        hero_class = hero_class.upper()
    if "pool_version" in data and data["pool_version"] != POOL_VERSION:
        errors.append(f"deck.json: pool_version {data['pool_version']!r} does not match the runtime pool {POOL_VERSION!r}")
    card_list = data.get("cards")
    if card_list is None:
        errors.append("deck.json: missing field 'cards'")
        return errors
    if not isinstance(card_list, list):
        errors.append("deck.json: 'cards' must be a list of card ids")
        return errors
    bad_entries = [i for i, c in enumerate(card_list) if not isinstance(c, str)]
    for i in bad_entries:
        errors.append(f"deck.json: cards[{i}] = {card_list[i]!r} is not a card id string")
    ids = [c for c in card_list if isinstance(c, str)]
    if len(card_list) != DECK_SIZE:
        errors.append(f"deck has {len(card_list)} cards; exactly {DECK_SIZE} are required")

    pool = cards_mod.load()
    excluded = cards_mod.load_excluded()
    blacklist = load_blacklist()
    counts = Counter(ids)
    for card_id in counts:  # first-appearance order
        if card_id in pool:
            card = pool[card_id]
            if card_id in blacklist:
                errors.append(f"card {_card_label(card_id)} is blacklisted: {blacklist[card_id]}")
            if hero_class and card["card_class"] not in (hero_class, "NEUTRAL"):
                errors.append(
                    f"card {_card_label(card_id)} is a {card['card_class']} card; a {hero_class} deck may only "
                    f"contain {hero_class} and NEUTRAL cards"
                )
            n = counts[card_id]
            if card["rarity"] == "LEGENDARY" and n > MAX_LEGENDARY_COPIES:
                errors.append(
                    f"card {_card_label(card_id)} is LEGENDARY and appears {n} times; at most "
                    f"{MAX_LEGENDARY_COPIES} copy is allowed"
                )
            elif n > MAX_COPIES:
                errors.append(f"card {_card_label(card_id)} appears {n} times; at most {MAX_COPIES} copies are allowed")
        elif card_id in excluded:
            info = excluded[card_id]
            reason = info["reason"]
            label = f"'{card_id}' ({info['name']})"
            if reason == "hall_of_fame":
                errors.append(f"card {label} is in the Hall of Fame and not in the pool")
            elif reason == "not_basic_or_classic":
                errors.append(f"card {label} is from set {info['set']}, not Basic or Classic")
            elif reason == "hero_card":
                errors.append(f"card {label} is a hero card and cannot be put in a deck")
            elif reason == "class_not_supported":
                errors.append(f"card {label} belongs to class {info['card_class']}, which is not playable")
            elif reason == "blacklisted":
                errors.append(f"card {label} is blacklisted: {blacklist.get(card_id, 'engine bug')}")
            else:
                errors.append(f"card {label} is not in the pool ({reason})")
        else:
            errors.append(f"card '{card_id}' is not a known collectible card id")
    return errors


def load_deck(path: str | Path) -> Deck:
    """Load and validate deck.json; raises DeckError listing every problem."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise DeckError([f"{path}: file not found"]) from None
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        raise DeckError([f"{path}: invalid JSON ({e})"]) from None
    errors = validate_deck_data(data)
    if errors:
        raise DeckError(errors)
    return Deck(hero_class=data["hero_class"].upper(), cards=tuple(data["cards"]), name=data.get("name"))


def deck_from_ids(hero_class: str, ids: list[str]) -> Deck:
    data = {"hero_class": hero_class, "cards": list(ids)}
    errors = validate_deck_data(data)
    if errors:
        raise DeckError(errors)
    return Deck(hero_class=hero_class.upper(), cards=tuple(ids))


def class_of_hero(hero_card_id: str) -> str | None:
    return CLASS_FOR_HERO.get(hero_card_id)


def random_deck(rng, hero_class: str | None = None) -> Deck:
    """A random valid deck from the pool (used by the random bot when no deck is given)."""
    blacklist = load_blacklist()
    if hero_class is None:
        hero_class = rng.choice(HERO_CLASSES)
    candidates = [
        c
        for c in cards_mod.load().values()
        if c["card_class"] in (hero_class, "NEUTRAL") and c["id"] not in blacklist
    ]
    ids: list[str] = []
    counts: Counter = Counter()
    while len(ids) < DECK_SIZE:
        c = rng.choice(candidates)
        limit = MAX_LEGENDARY_COPIES if c["rarity"] == "LEGENDARY" else MAX_COPIES
        if counts[c["id"]] < limit:
            counts[c["id"]] += 1
            ids.append(c["id"])
    return Deck(hero_class=hero_class, cards=tuple(ids), name=f"random_{hero_class.lower()}")


# --------------------------------------------------------------------------------------------------- manifest

MANIFEST_FIELDS = ("protocol_version", "pool_version", "name", "author", "command")


def validate_manifest_data(data: Any) -> Report:
    report = Report()
    if not isinstance(data, dict):
        report.errors.append("manifest.json must be a JSON object")
        return report
    for key in MANIFEST_FIELDS:
        if key not in data:
            report.errors.append(f"manifest.json: missing field '{key}'")
    pv = data.get("protocol_version")
    if "protocol_version" in data and pv != PROTOCOL_VERSION:
        report.errors.append(
            f"manifest.json: protocol_version {pv!r} is not supported (this runtime speaks {PROTOCOL_VERSION!r})"
        )
    pool = data.get("pool_version")
    if "pool_version" in data and pool != POOL_VERSION:
        report.errors.append(f"manifest.json: pool_version {pool!r} does not match the runtime pool {POOL_VERSION!r}")
    name = data.get("name")
    if "name" in data and (not isinstance(name, str) or not NAME_RE.match(name)):
        report.errors.append(
            f"manifest.json: name {name!r} must be 1-64 characters of letters, digits, '_', '.', '-'"
        )
    author = data.get("author")
    if "author" in data and (not isinstance(author, str) or not author.strip()):
        report.errors.append(f"manifest.json: author {author!r} must be a non-empty string")
    command = data.get("command")
    if "command" in data:
        if (
            not isinstance(command, list)
            or not command
            or not all(isinstance(x, str) and x for x in command)
        ):
            report.errors.append(
                f"manifest.json: command {command!r} must be a non-empty list of strings, e.g. [\"python\", \"agent.py\"]"
            )
    for key in data:
        if key not in MANIFEST_FIELDS:
            report.warnings.append(f"manifest.json: unknown field '{key}' ignored")
    return report


@dataclass(frozen=True)
class Submission:
    path: Path
    manifest: dict[str, Any]
    deck: Deck

    @property
    def name(self) -> str:
        return self.manifest["name"]

    @property
    def command(self) -> list[str]:
        return list(self.manifest["command"])


class SubmissionError(ValueError):
    def __init__(self, errors: list[str], warnings: list[str] | None = None):
        self.errors = list(errors)
        self.warnings = list(warnings or [])
        super().__init__("; ".join(self.errors))


def load_submission(path: str | Path) -> Submission:
    """Load manifest.json + deck.json from a submission directory; raises SubmissionError on any problem."""
    path = Path(path).resolve()
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_dir():
        raise SubmissionError([f"{path}: not a directory"])
    manifest: Any = None
    mpath = path / "manifest.json"
    try:
        manifest = json.loads(mpath.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append("manifest.json: file not found")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        errors.append(f"manifest.json: invalid JSON ({e})")
    if manifest is not None:
        rep = validate_manifest_data(manifest)
        errors += rep.errors
        warnings += rep.warnings
    deck = None
    try:
        deck = load_deck(path / "deck.json")
    except DeckError as e:
        errors += e.errors
    if errors:
        raise SubmissionError(errors, warnings)
    return Submission(path=path, manifest=manifest, deck=deck)
