"""Compare tuned decks on fresh seeds: each vs the greedy field, then a script-vs-script round robin.

    python tools/compare.py --field-games 500 --pair-games 1000     # uses games/tune/*.json weights
Prints markdown.
"""

import argparse
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402

TUNE = fastsim.ROOT / "games" / "tune"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--field-games", type=int, default=500)
    ap.add_argument("--pair-games", type=int, default=1000)
    ap.add_argument("--field-seed", type=int, default=5000)
    ap.add_argument("--pair-seed", type=int, default=9000)
    a = ap.parse_args()
    tuned = {p.stem: json.loads(p.read_text()) for p in sorted(TUNE.glob("*.json"))}
    names = list(tuned)

    print(f"## Each tuned deck vs the greedy field (seeds {a.field_seed}+, {a.field_games} games per opponent)\n")
    field_rows = {}
    for n in names:
        out, bad = fastsim.run(a.field_games, tuned[n]["weights"], tuned[n]["deck"], seed=a.field_seed)
        field_rows[n] = (out, bad)
        print(f"{n} done", file=sys.stderr, flush=True)
    opps = fastsim.FIELD
    print("| Opponent | " + " | ".join(names) + " |")
    print("|---|" + "---:|" * len(names))
    for o in opps:
        print(f"| {o} | " + " | ".join(f"{100 * field_rows[n][0][o][0] / field_rows[n][0][o][1]:.1f}" for n in names) + " |")
    tot = {n: sum(v[0] for v in field_rows[n][0].values()) / sum(v[1] for v in field_rows[n][0].values()) for n in names}
    print("| **Total** | " + " | ".join(f"**{100 * tot[n]:.1f}**" for n in names) + " |")
    print("| forfeits/voids | " + " | ".join(str(field_rows[n][1]) for n in names) + " |")

    print(f"\n## Script vs script (seeds {a.pair_seed}+, {a.pair_games} games per pairing, half each seat)\n")
    wins = {x: {y: None for y in names} for x in names}
    for x, y in itertools.combinations(names, 2):
        out, bad = fastsim.run(a.pair_games, tuned[x]["weights"], tuned[x]["deck"], field=[f"script:{tuned[y]['deck']}"],
                               seed=a.pair_seed, opp_w=tuned[y]["weights"])
        w, g = next(iter(out.values()))
        wins[x][y], wins[y][x] = (w, g), (g - w, g)
        print(f"{x} vs {y}: {w}/{g} (forfeits/voids {bad})", file=sys.stderr, flush=True)
    print("Win % of row deck vs column deck:\n")
    print("| vs | " + " | ".join(names) + " | Total |")
    print("|---|" + "---:|" * (len(names) + 1))
    for x in names:
        cells = [f"{100 * wins[x][y][0] / wins[x][y][1]:.1f}" if wins[x][y] else "–" for y in names]
        tw = sum(wins[x][y][0] for y in names if wins[x][y])
        tg = sum(wins[x][y][1] for y in names if wins[x][y])
        print(f"| {x} | " + " | ".join(cells) + f" | **{100 * tw / tg:.1f}** |")
    print("\nWeights: " + "; ".join(f"{n} {json.dumps(tuned[n]['weights'])}" for n in names))


if __name__ == "__main__":
    main()
