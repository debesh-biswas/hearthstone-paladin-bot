"""Our top 5 script decks vs a strength-tuned script on Astra's rebuilt Zoo list, and vs Bots 1 and 2.

    python tools/astra.py                         # measure (fresh seeds 90000+, half each seat)
    python tools/astra.py --tune control-paladin  # first tune that deck against Astra (one pass), then measure
Astra's weights: games/astra_strong.json (tuned vs our top 5 for strength). Ours: games/selfplay/state.json, overridden
by games/astra/weights.json for decks tuned here. Prints markdown.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402
import selfplay  # noqa: E402

TOP5 = ["control-paladin", "infernal-warlock", "counter-paladin", "steady-paladin", "pressure-hunter"]
ASTRA = "script:research/opponents/astra-zoo-warlock.json"
BOTS = ["research/opponents/bot1-greedy-mage.json", "research/opponents/bot2-face-hunter.json"]
TUNED = fastsim.ROOT / "games" / "astra" / "weights.json"


def pct(out, opp=None):
    v = [out[opp]] if opp else out.values()
    return 100 * sum(x[0] for x in v) / sum(x[1] for x in v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tune", nargs="*", default=[])
    ap.add_argument("--games", type=int, default=1000)
    a = ap.parse_args()
    st = json.loads((fastsim.ROOT / "games" / "selfplay" / "state.json").read_text())
    astra_w = json.loads((fastsim.ROOT / "games" / "astra_strong.json").read_text())
    tuned = json.loads(TUNED.read_text()) if TUNED.exists() else {}
    for n in a.tune:
        tuned[n] = selfplay.tune(n, st["decks"][n], tuned.get(n, st["weights"][n]), [ASTRA], {ASTRA: astra_w},
                                 seed=81000, games=600)
        TUNED.parent.mkdir(exist_ok=True)
        TUNED.write_text(json.dumps(tuned, indent=1))
    print(f"Fresh seeds 90000+, {a.games} games per cell, half each seat\n")
    print("| Our deck | weights | vs Astra script | vs Bot 1 | vs Bot 2 | forfeits/voids |")
    print("|---|---|---:|---:|---:|---:|")
    for n in TOP5:
        for label, w in [("self-play", st["weights"][n])] + ([("tuned vs Astra", tuned[n])] if n in tuned else []):
            o1, b1 = fastsim.run(a.games, w, st["decks"][n], field=[ASTRA], seed=90000, opp_w=astra_w)
            o2, b2 = fastsim.run(a.games, w, st["decks"][n], field=BOTS, seed=90000)
            print(f"| {n} | {label} | {pct(o1):.1f} | {pct(o2, BOTS[0]):.1f} | {pct(o2, BOTS[1]):.1f} | {b1 + b2} |", flush=True)


if __name__ == "__main__":
    main()
