"""A3: deck and manifest validation fixtures."""

import json

import pytest

from conftest import MANIFEST, make_submission
from hs_arena._resources import GREEDY_DECK
from hs_arena.deck import DeckError, SubmissionError, load_deck, load_submission, validate_deck_data, validate_manifest_data


def greedy_cards():
    return json.loads(GREEDY_DECK.read_text(encoding="utf-8"))["cards"]


def deck(cards, hero_class="MAGE", **extra):
    d = {"hero_class": hero_class, "cards": cards}
    d.update(extra)
    return d


def errors_for(d):
    errs = validate_deck_data(d)
    assert errs, "expected the deck to be rejected"
    return " | ".join(errs)


def test_valid_decks():
    assert validate_deck_data(deck(greedy_cards())) == []
    d = load_deck(GREEDY_DECK)
    assert d.hero_class == "MAGE" and len(d.cards) == 30


def test_29_and_31_cards():
    assert "29 cards" in errors_for(deck(greedy_cards()[:29]))
    assert "31 cards" in errors_for(deck(greedy_cards() + ["CS2_182"]))


def test_off_class_card():
    cards = greedy_cards()
    cards[0] = "CS2_106"  # Fiery War Axe (Warrior)
    msg = errors_for(deck(cards))
    assert "CS2_106" in msg and "WARRIOR" in msg


def test_three_copies():
    cards = greedy_cards()
    cards[cards.index("CS2_182")] = "CS2_179"  # third Sen'jin
    msg = errors_for(deck(cards))
    assert "CS2_179" in msg and "3 times" in msg


def test_two_legendaries():
    cards = greedy_cards()
    cards[cards.index("CS2_032")] = "EX1_012"  # second Bloodmage Thalnos
    msg = errors_for(deck(cards))
    assert "EX1_012" in msg and "LEGENDARY" in msg


def test_unknown_id():
    cards = greedy_cards()
    cards[0] = "NOT_A_CARD"
    assert "NOT_A_CARD" in errors_for(deck(cards))


def test_hall_of_fame_card():
    cards = greedy_cards()
    cards[0] = "EX1_284"  # Azure Drake
    msg = errors_for(deck(cards))
    assert "EX1_284" in msg and "Hall of Fame" in msg


def test_non_classic_set_card():
    cards = greedy_cards()
    cards[0] = "GVG_110"  # Dr. Boom (GvG)
    msg = errors_for(deck(cards))
    assert "GVG_110" in msg and "not Basic or Classic" in msg


def test_bad_hero_class_and_shape():
    assert "hero_class" in errors_for(deck(greedy_cards(), hero_class="DEMONHUNTER"))
    assert "hero_class" in errors_for({"cards": greedy_cards()})
    assert "cards" in errors_for({"hero_class": "MAGE"})
    assert "cards[3]" in errors_for(deck(greedy_cards()[:3] + [42] + greedy_cards()[4:]))
    assert "pool_version" in errors_for(deck(greedy_cards(), pool_version="other-pool"))


def test_load_deck_errors(tmp_path):
    p = tmp_path / "deck.json"
    p.write_text("{not json", encoding="utf-8")
    with pytest.raises(DeckError, match="invalid JSON"):
        load_deck(p)
    with pytest.raises(DeckError, match="not found"):
        load_deck(tmp_path / "missing.json")


@pytest.mark.parametrize(
    "change, needle",
    [
        ({"protocol_version": "2"}, "protocol_version"),
        ({"pool_version": "classic-2"}, "pool_version"),
        ({"name": ""}, "name"),
        ({"name": "has spaces"}, "name"),
        ({"author": ""}, "author"),
        ({"command": []}, "command"),
        ({"command": "python agent.py"}, "command"),
        ({"command": ["python", 3]}, "command"),
    ],
)
def test_manifest_field_errors(change, needle):
    m = dict(MANIFEST)
    m.update(change)
    rep = validate_manifest_data(m)
    assert not rep.ok and any(needle in e for e in rep.errors), rep.errors


@pytest.mark.parametrize("missing", ["protocol_version", "pool_version", "name", "author", "command"])
def test_manifest_missing_fields(missing):
    m = dict(MANIFEST)
    del m[missing]
    rep = validate_manifest_data(m)
    assert any(f"missing field '{missing}'" in e for e in rep.errors)


def test_manifest_unknown_field_is_a_warning():
    rep = validate_manifest_data(dict(MANIFEST, extra=1))
    assert rep.ok and rep.warnings


def test_load_submission(tmp_path):
    sub = make_submission(tmp_path, "pass\n")
    s = load_submission(sub)
    assert s.name == "test-agent" and s.deck.hero_class == "MAGE"
    (sub / "manifest.json").write_text("[]", encoding="utf-8")
    with pytest.raises(SubmissionError, match="JSON object"):
        load_submission(sub)
    (sub / "manifest.json").unlink()
    with pytest.raises(SubmissionError, match="manifest.json: file not found"):
        load_submission(sub)
