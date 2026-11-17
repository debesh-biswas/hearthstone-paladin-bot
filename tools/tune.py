"""Same tuning budget for every deck: one coordinate-descent pass over GRID vs the greedy field, then results JSON.

    python tools/tune.py decks/steady-paladin/deck.json research/decks/counter-paladin.json --games 300
Writes games/tune/<deck name>.json with every run and the chosen weights.
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402
from hs_arena.deck import load_deck  # noqa: E402

GRID = {
    "face": [0.3, 0.5, 0.7, 1.0],
    "enemy_minion": [1.2, 1.5, 1.8],
    "hand_per_cost": [0.25, 0.5, 0.75],
    "danger": [2, 5, 10],
    "our_hp": [3, 5, 8],
    "taunt": [1, 2.5],
    "draw": [1.5, 3, 4.5],
}


def score(deck, w, games, seed):
    out, bad = fastsim.run(games, w, deck, seed=seed)
    return sum(v[0] for v in out.values()) / sum(v[1] for v in out.values()), out, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decks", nargs="+")
    ap.add_argument("--games", type=int, default=300, help="per opponent per run")
    ap.add_argument("--seed", type=int, default=1000)
    a = ap.parse_args()
    out_dir = fastsim.ROOT / "research" / "weights" / "tune"
    out_dir.mkdir(parents=True, exist_ok=True)
    for deck in a.decks:
        name = load_deck(deck).name
        w = {}
        best, _, _ = score(deck, w, a.games, a.seed)
        runs = [{"w": dict(w), "win": best}]
        print(f"{name}: start {100 * best:.1f}%", flush=True)
        for key, values in GRID.items():
            for v in values:
                if w.get(key, fastsim.BASE_W[key]) == v:
                    continue  # the current weights: already measured
                trial = {**w, key: v}
                win, _, bad = score(deck, trial, a.games, a.seed)
                runs.append({"w": trial, "win": win, "bad": bad})
                print(f"{name}: {json.dumps(trial)} {100 * win:.1f}%", flush=True)
                if win > best:
                    best, w = win, trial
        (out_dir / f"{name}.json").write_text(json.dumps({"deck": deck, "best": best, "weights": w, "runs": runs}, indent=1))
        print(f"{name}: BEST {100 * best:.1f}% {json.dumps(w)}", flush=True)


if __name__ == "__main__":
    main()
