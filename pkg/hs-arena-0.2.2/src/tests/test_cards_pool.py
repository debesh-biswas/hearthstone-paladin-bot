"""A1/A2: versions, imports without setuptools, generated card catalog."""

import subprocess
import sys
import xml.etree.ElementTree as ET

from hs_arena import FIREPLACE_COMMIT, POOL_VERSION, PROTOCOL_VERSION, RUNTIME_VERSION, cards
from hs_arena._resources import CARD_DEFS_XML, CARDS_JSON
from hs_arena.pool import HERO_CLASSES

# GameTag ids in CardDefs.xml
TAG_CARD_SET, TAG_CLASS, TAG_CARDTYPE, TAG_COLLECTIBLE = "183", "199", "202", "321"
SET_BASIC, SET_EXPERT1 = 2, 3
TYPE_HERO = 3
NINE_CLASSES = {2, 3, 4, 5, 6, 7, 8, 9, 10, 12}  # DRUID..WARRIOR (2-10) and NEUTRAL (12)


def _direct_xml_ids() -> set:
    """Pool card ids straight from the XML (before the blacklist), independently of the hearthstone library."""
    ids = set()
    for _, el in ET.iterparse(str(CARD_DEFS_XML), events=("end",)):
        if el.tag != "Entity":
            continue
        tags = {t.get("enumID"): t.get("value") for t in el.findall("Tag")}
        if (
            tags.get(TAG_COLLECTIBLE) == "1"
            and int(tags.get(TAG_CARD_SET, 0)) in (SET_BASIC, SET_EXPERT1)
            and int(tags.get(TAG_CARDTYPE, 0)) != TYPE_HERO
            and int(tags.get(TAG_CLASS, 0)) in NINE_CLASSES
        ):
            ids.add(el.get("CardID"))
        el.clear()
    return ids


def test_versions_and_import_without_setuptools():
    code = (
        "import sys, builtins\n"
        "real = builtins.__import__\n"
        "def guard(name, *a, **k):\n"
        "    if name.split('.')[0] in ('pkg_resources', 'setuptools'):\n"
        "        raise ImportError('blocked ' + name)\n"
        "    return real(name, *a, **k)\n"
        "builtins.__import__ = guard\n"
        "import hs_arena.engine, hs_arena._fp\n"
        "hs_arena._fp.init_engine()\n"
        "print('ok')\n"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr
    assert "ok" in out.stdout
    from hs_arena.cli import main

    assert main(["version"]) == 0
    assert RUNTIME_VERSION and PROTOCOL_VERSION == "1" and POOL_VERSION == "basic-classic-1"
    assert len(FIREPLACE_COMMIT) == 40


def test_cards_json_entries():
    catalog = cards.load()
    assert catalog, "cards.json is empty"
    for cid, c in catalog.items():
        assert c["id"] == cid
        assert c["set"] in ("BASIC", "EXPERT1"), c
        assert c["type"] in ("MINION", "SPELL", "WEAPON"), c
        assert c["card_class"] in HERO_CLASSES + ("NEUTRAL",), c
        assert c["name"] and isinstance(c["cost"], int)
        assert isinstance(c["text"], str) and "<b>" not in c["text"] and "$" not in c["text"] and "[x]" not in c["text"]
        if c["type"] == "MINION":
            assert "attack" in c and "health" in c
        if c["type"] == "WEAPON":
            assert "attack" in c and "durability" in c
    # Hall of Fame cards are not in the pool
    for hof in ("EX1_284", "EX1_007", "EX1_116", "EX1_016"):  # Azure Drake, Acolyte, Leeroy, Sylvanas
        assert hof not in catalog
        assert cards.load_excluded()[hof]["reason"] == "hall_of_fame"


def test_cards_count_matches_xml_and_generation_is_reproducible():
    doc, _ = cards.generate()
    catalog = cards.load()
    from hs_arena.pool import load_blacklist

    direct = _direct_xml_ids()
    blacklist = set(load_blacklist())
    assert blacklist <= direct, "blacklisted ids must be pool cards"
    assert set(catalog) == direct - blacklist
    assert doc["count"] == len(catalog) == len(direct) - len(blacklist)
    import json

    on_disk = json.loads(CARDS_JSON.read_text(encoding="utf-8"))
    assert on_disk == doc, "data/cards.json is stale: run tools/gen_cards.py"
    print(f"pool size: {doc['count']} cards")


def test_card_pool_md_is_generated():
    from pathlib import Path

    md = (Path(__file__).resolve().parents[1] / "docs" / "card_pool.md").read_text(encoding="utf-8")
    doc, _ = cards.generate()
    assert md.strip() == cards.card_pool_markdown(doc).strip(), "docs/card_pool.md is stale: run tools/gen_cards.py"
