"""Our tuned script decks vs the opponent decks rebuilt from online results (research/opponents/*.json).

    python tools/opponents.py --games 1000
Each opponent list is played by the greedy bot, and Astra's list also by our planner (default weights) as a
stronger stand-in. Weights: games/selfplay/state.json. Prints markdown.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402

OPPS = {"Bot 1 (greedy)": "research/opponents/bot1-greedy-mage.json",
        "Bot 2 (greedy)": "research/opponents/bot2-face-hunter.json",
        "Astra list (greedy)": "research/opponents/astra-zoo-warlock.json",
        "Astra list (our planner)": "script:research/opponents/astra-zoo-warlock.json"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=1000)
    ap.add_argument("--seed", type=int, default=70000)
    a = ap.parse_args()
    st = json.loads((fastsim.ROOT / "research" / "weights" / "selfplay-state.json").read_text())
    rows = {}
    for n, deck in st["decks"].items():
        out, bad = fastsim.run(a.games, st["weights"][n], deck, field=list(OPPS.values()), seed=a.seed)
        rows[n] = (out, bad)
        print(f"{n}: " + ", ".join(f"{k} {out[v][0]}/{out[v][1]}" for k, v in OPPS.items()) + f", forfeits/voids {bad}",
              file=sys.stderr, flush=True)
    print(f"Win % ({a.games} games per cell, half each seat, seeds {a.seed}+)\n")
    print("| Our deck | " + " | ".join(OPPS) + " | forfeits/voids |")
    print("|---|" + "---:|" * (len(OPPS) + 1))
    for n, (out, bad) in sorted(rows.items(), key=lambda r: -r[1][0][OPPS["Astra list (our planner)"]][0]):
        print(f"| {n} | " + " | ".join(f"{100 * out[v][0] / out[v][1]:.1f}" for v in OPPS.values()) + f" | {bad} |")


if __name__ == "__main__":
    main()
