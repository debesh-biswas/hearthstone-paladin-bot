"""One- and two-card swaps for Control Paladin aimed at going second vs Astra, no weight tuning.

    python tools/swaps.py screen                 # every single swap: 2,000 games vs the Astra script, split first/second
    python tools/swaps.py check "-EX1_561+NEW1_021" "-EX1_561-CS2_088+NEW1_021+EX1_066"
        # full check of named swaps: Astra (2,000, split), Bots 1 and 2 (1,000 each), our 6 other script decks (1,000 each)
Swap syntax: -<card id> removes one copy, +<card id> adds one. Current Control weights; cheap added cards (cost <= 2)
join the mulligan keep list. Prints markdown.
"""

import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402

move = fastsim.move
ROOT = fastsim.ROOT
BASE = json.loads((ROOT / "player" / "deck.json").read_text())
RULE = move.MULLIGAN["control-paladin"]
CUTS = ["EX1_561", "CS2_088"]  # Alexstrasza, Guardian of Kings
ADDS = ["NEW1_021", "EX1_362", "EX1_066", "CS2_203", "NEW1_019", "EX1_008"]
OUT = ROOT / "games" / "swaps"
ASTRA = "script:research/opponents/astra-zoo-warlock.json"
BOTS = ["research/opponents/bot1-greedy-mage.json", "research/opponents/bot2-face-hunter.json"]


def parse(swap):
    return [(sign, cid) for sign, cid in re.findall(r"([+-])([A-Za-z0-9_]+)", swap)]


def name(swap):
    return " ".join(f"{s}{move.CATALOG[c]['name']}" for s, c in parse(swap)) or "current list"


def deck_path(swap):
    """Write the variant deck and return its path; its mulligan rule is registered under the deck name."""
    cards = collections.Counter(BASE["cards"])
    for sign, cid in parse(swap):
        cards[cid] += 1 if sign == "+" else -1
    key = "cp-" + (re.sub(r"[^A-Za-z0-9]", "", swap) or "base")
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"{key}.json"
    p.write_text(json.dumps({"name": key, "hero_class": "PALADIN", "cards": sorted(cards.elements())}, indent=1))
    return p


def register(swaps):
    for swap in swaps:
        key = "cp-" + (re.sub(r"[^A-Za-z0-9]", "", swap) or "base")
        cheap = {c for s, c in parse(swap) if s == "+" and move.CATALOG[c]["cost"] <= 2}
        move.MULLIGAN[key] = dict(RULE, always=RULE["always"] | cheap)


SCREEN = [""] + [f"-{c}+{a}" for c in CUTS for a in ADDS]
CHECK = sys.argv[2:] if len(sys.argv) > 2 and sys.argv[1] == "check" else []
register(SCREEN + CHECK)  # module level: spawned workers re-import this file and need the rules too


def pct(o, k):
    return 100 * o[k][0] / o[k][1]


def main():
    from hs_arena.deck import validate_deck_data
    st = json.loads((ROOT / "research" / "weights" / "selfplay-state.json").read_text())
    w = st["weights"]["control-paladin"]
    aw = json.loads((ROOT / "research" / "weights" / "astra-strong.json").read_text())
    swaps = SCREEN if sys.argv[1] == "screen" else [""] + CHECK
    others = [n for n in st["decks"] if n != "control-paladin"]
    if sys.argv[1] == "screen":
        print("| Swap | vs Astra, we go 2nd | vs Astra, we go 1st |\n|---|---:|---:|")
    else:
        print("| Swap | Astra 2nd | Astra 1st | Bot 1 | Bot 2 | " + " | ".join(others) + " | our decks total |")
        print("|---|" + "---:|" * (5 + len(others)))
    for swap in swaps:
        p = deck_path(swap)
        d = json.loads(p.read_text())
        assert len(d["cards"]) == 30 and not validate_deck_data(d), validate_deck_data(d)
        o, bad = fastsim.run(2000, w, p, field=[ASTRA], seed=98000, opp_w=aw, split=True)
        row = [f"{pct(o, ASTRA + '|second'):.1f}", f"{pct(o, ASTRA + '|first'):.1f}"]
        if CHECK:
            o2, b2 = fastsim.run(1000, w, p, field=BOTS, seed=98000)
            row += [f"{pct(o2, b):.1f}" for b in BOTS]
            tw = tg = 0
            for n in others:
                o3, b3 = fastsim.run(1000, w, p, field=[f"script:{st['decks'][n]}"], seed=97000, opp_w=st["weights"][n])
                x, g = next(iter(o3.values()))
                tw, tg, bad = tw + x, tg + g, bad + b2 + b3
                row.append(f"{100 * x / g:.1f}")
            row.append(f"**{100 * tw / tg:.1f}**")
        print(f"| {name(swap)} | " + " | ".join(row) + (f" | forfeits {bad}" if bad else "") + " |", flush=True)


if __name__ == "__main__":
    main()
