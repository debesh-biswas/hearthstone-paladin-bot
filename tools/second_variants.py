"""Control Paladin strategy variants for going second (mulligan rules and deck swaps), no weight tuning.

    python tools/second_variants.py
Each variant: 2,000 games vs the Astra script (split by who went first) and 1,000 vs each of Bots 1 and 2, fresh seeds
96000+, current Control weights. Variant decks are written to games/variants/. Prints markdown.
"""

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402

move = fastsim.move
BASE = json.loads((fastsim.ROOT / "player" / "deck.json").read_text())
RULE = move.MULLIGAN["control-paladin"]
EARLY = RULE["always"]
# name: (deck changes {card: +/-n}, mulligan rule)
VARIANTS = {
    "current": ({}, RULE),
    "M1 keep 4-drops going 2nd": ({}, dict(RULE, second={"CS2_093", "CS2_097", "CS2_179", "EX1_619"})),
    "M2 always keep Consecration": ({}, dict(RULE, always=EARLY | {"CS2_093"})),
    "D1 -Alex -Guardian +2 Doomsayer": ({"EX1_561": -1, "CS2_088": -1, "NEW1_021": 2}, dict(RULE, always=EARLY | {"NEW1_021"})),
    "D2 -Alex -Guardian +Ooze +Owl": ({"EX1_561": -1, "CS2_088": -1, "EX1_066": 1, "CS2_203": 1}, RULE),
    "D3 -Alex -Guardian +2 Argent Protector": ({"EX1_561": -1, "CS2_088": -1, "EX1_362": 2}, dict(RULE, always=EARLY | {"EX1_362"})),
    "D4 -Alex -Guardian -Wrath +2 Doomsayer +Ooze": ({"EX1_561": -1, "CS2_088": -1, "EX1_384": -1, "NEW1_021": 2, "EX1_066": 1},
                                                     dict(RULE, always=EARLY | {"NEW1_021"})),
}
OUT = fastsim.ROOT / "games" / "variants"


def deck_for(i, changes):
    cards = collections.Counter(BASE["cards"])
    cards.update(changes)
    return {"name": f"cp-v{i}", "hero_class": "PALADIN", "cards": sorted(cards.elements())}


# Runs in every worker too (spawn re-imports this module): the variant mulligan rules, keyed by variant deck name.
for i, (changes, rule) in enumerate(VARIANTS.values()):
    move.MULLIGAN[f"cp-v{i}"] = rule


def main():
    from hs_arena.deck import validate_deck_data
    OUT.mkdir(parents=True, exist_ok=True)
    st = json.loads((fastsim.ROOT / "games" / "selfplay" / "state.json").read_text())
    w = st["weights"]["control-paladin"]
    aw = json.loads((fastsim.ROOT / "games" / "astra_strong.json").read_text())
    astra = "script:research/opponents/astra-zoo-warlock.json"
    bots = ["research/opponents/bot1-greedy-mage.json", "research/opponents/bot2-face-hunter.json"]
    print("Fresh seeds 96000+. Astra: 2,000 games (about half going second); bots: 1,000 each.\n")
    print("| Variant | vs Astra, we go 2nd | vs Astra, we go 1st | vs Bot 1 | vs Bot 2 | forfeits/voids |")
    print("|---|---:|---:|---:|---:|---:|")
    for i, (name, (changes, _)) in enumerate(VARIANTS.items()):
        d = deck_for(i, changes)
        assert len(d["cards"]) == 30 and not validate_deck_data(d), validate_deck_data(d)
        path = OUT / f"cp-v{i}.json"
        path.write_text(json.dumps(d, indent=1))
        o, b = fastsim.run(2000, w, path, field=[astra], seed=96000, opp_w=aw, split=True)
        o2, b2 = fastsim.run(1000, w, path, field=bots, seed=96000)
        f = {k.split("|")[1]: 100 * v[0] / v[1] for k, v in o.items()}
        g = [100 * o2[x][0] / o2[x][1] for x in bots]
        print(f"| {name} | {f['second']:.1f} | {f['first']:.1f} | {g[0]:.1f} | {g[1]:.1f} | {b + b2} |", flush=True)


if __name__ == "__main__":
    main()
