"""Early-game fixes vs aggro for Control Paladin, tested against the tuned stand-ins (tools/standins.py).

    python tools/early.py
Each variant: 1,000 games vs the tuned Astra and Bot 2 scripts (split by who went first), seeds 75000+.
Variant decks go to games/early/. Prints markdown.
"""

import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402
import standins  # noqa: E402  (registers Bot 2's mulligan in every worker)

move = fastsim.move
BASE = json.loads((fastsim.ROOT / "player" / "deck.json").read_text())
W = {**fastsim.BASE_W, **BASE["weights"]}
RULE = move.MULLIGAN["control-paladin"]
AGGRO_KEEP = dict(RULE, always=RULE["always"] | {"CS2_093"}, one_four=["CS2_097", "CS2_179"])
# name: (deck changes, mulligan rule, weight changes)
VARIANTS = {
    "current (sub 2)": ({}, RULE, {}),
    "A keep Consecration + a 4-drop": ({}, AGGRO_KEEP, {}),
    "B spend cards (hand_per_cost x0.5)": ({}, RULE, {"hand_per_cost": W["hand_per_cost"] * 0.5}),
    "C spend cards (hand_per_cost 0)": ({}, RULE, {"hand_per_cost": 0.0}),
    "D -Equality +Doomsayer": ({"EX1_619": -1, "NEW1_021": 1}, RULE, {}),
    "E -Equality +Ooze": ({"EX1_619": -1, "EX1_066": 1}, RULE, {}),
    "F -2 Equality +Doomsayer +Ooze": ({"EX1_619": -2, "NEW1_021": 1, "EX1_066": 1}, RULE, {}),
}
OUT = fastsim.ROOT / "games" / "early"
for i, (_, rule, _) in enumerate(VARIANTS.values()):  # runs in workers too (spawn re-imports this module)
    move.MULLIGAN[f"cp-e{i}"] = rule


def main():
    from hs_arena.deck import validate_deck_data
    OUT.mkdir(parents=True, exist_ok=True)
    opps = {"Astra": ("script:" + standins.ASTRA, json.loads((standins.WEIGHTS / "standin-astra.json").read_text())),
            "Bot 2": ("script:" + standins.BOT2, json.loads((standins.WEIGHTS / "standin-bot2.json").read_text()))}
    print("| Variant | Astra 2nd | Astra 1st | Bot 2 2nd | Bot 2 1st | all |")
    print("|---|---:|---:|---:|---:|---:|")
    for i, (name, (changes, _, dw)) in enumerate(VARIANTS.items()):
        cards = collections.Counter(BASE["cards"])
        cards.update(changes)
        d = {"name": f"cp-e{i}", "hero_class": "PALADIN", "cards": sorted(cards.elements())}
        assert len(d["cards"]) == 30 and not validate_deck_data(d), validate_deck_data(d)
        path = OUT / f"cp-e{i}.json"
        path.write_text(json.dumps(d, indent=1))
        cells, tw, tg = [], 0, 0
        for spec, ow in opps.values():
            o, bad = fastsim.run(1000, {**W, **dw}, path, field=[spec], seed=75000, opp_w=ow, split=True)
            assert not bad, bad
            for k in ("second", "first"):
                w, g = o[f"{spec}|{k}"]
                cells.append(f"{100 * w / g:.1f}")
                tw, tg = tw + w, tg + g
        print(f"| {name} | " + " | ".join(cells) + f" | **{100 * tw / tg:.1f}** |", flush=True)


if __name__ == "__main__":
    main()
