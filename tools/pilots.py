"""Other skills' own move scripts (decks/<name>/scripts/move.py) vs the greedy field and vs our tuned script decks.

    python tools/pilots.py burst-shaman infernal-warlock pressure-hunter
Writes games/pilots.json and prints markdown. Same seeds as tools/compare.py (field 5000+, pairings 9000+).
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skills", nargs="+", help="folders under decks/ that have scripts/move.py")
    ap.add_argument("--field-games", type=int, default=500)
    ap.add_argument("--pair-games", type=int, default=1000)
    a = ap.parse_args()
    tuned = {p.stem: json.loads(p.read_text()) for p in sorted((fastsim.ROOT / "research" / "weights" / "tune").glob("*.json"))}
    res = {}
    for d in a.skills:
        me = f"pilot:{fastsim.ROOT / 'decks' / d}"
        out, bad = fastsim.run(a.field_games, deck=me, seed=5000)
        res[d] = {"field": sum(v[0] for v in out.values()) / sum(v[1] for v in out.values()), "field_bad": bad, "vs": {}}
        print(f"{d} field {100 * res[d]['field']:.1f}%", file=sys.stderr, flush=True)
        for n, t in tuned.items():
            o, b = fastsim.run(a.pair_games, deck=me, field=[f"script:{t['deck']}"], seed=9000, opp_w=t["weights"])
            w, g = next(iter(o.values()))
            res[d]["vs"][n] = [w, g, b]
            print(f"{d} vs script {n}: {w}/{g}", file=sys.stderr, flush=True)
    (fastsim.ROOT / "games" / "pilots.json").write_text(json.dumps(res, indent=1))
    names = list(tuned)
    print("Win % of each skill's own pilot (row) vs our tuned script on the column deck:\n")
    print("| Pilot | vs greedy field | " + " | ".join(names) + " |")
    print("|---|---:|" + "---:|" * len(names))
    for d, r in res.items():
        print(f"| {d} | {100 * r['field']:.1f} | " + " | ".join(f"{100 * r['vs'][n][0] / r['vs'][n][1]:.1f}" for n in names) + " |")


if __name__ == "__main__":
    main()
