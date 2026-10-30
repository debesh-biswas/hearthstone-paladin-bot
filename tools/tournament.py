"""Round-robin deck tournament on hs-arena.

Stage A (model-free): every deck piloted by the built-in greedy bot.
    python tools/tournament.py a --games 100
Stage B (skills played by the model): skill vs greedy and skill vs skill.
    python tools/tournament.py b --decks zoo-warlock,tempo-mage --vs-greedy 6 --pair-games 4
Stage C (no model): our script player (player/) vs every deck piloted by the greedy bot; --hero rulebot is the baseline.
    python tools/tournament.py c --games 500 --workers 12

Each pairing is split in two orientations (A as P1, then B as P1) with the same seeds, so seat and
first-player luck cancel out. Results: games/<stage>/ (raw) and a markdown report on stdout.
"""

import argparse
import itertools
import json
import math
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HS = ROOT / "pkg/hs-arena-0.2.2/.venv/bin/hs-arena"
GREEDY_MAGE = ROOT / "pkg/hs-arena-0.2.2/decks/greedy_mage.json"


def spec(stage, name):
    if name == "player":
        return f"client:{ROOT / 'player'}"
    if name == "rulebot":  # the greedy bot playing our player's deck: the baseline for stage c
        return f"greedy:{ROOT / 'player' / 'deck.json'}"
    if name == "greedy-mage":
        return "greedy" if stage == "b" else f"greedy:{GREEDY_MAGE}"
    return f"skill:{ROOT / 'decks' / name}" if stage == "b" else f"greedy:{ROOT / 'decks' / name / 'deck.json'}"


def run(stage, p1, p2, games, seed, parallel, out_root):
    out = out_root / f"{p1}__vs__{p2}"
    if out.exists() and len(list(out.glob("g_*/result.json"))) >= games:
        return out  # already played (resume)
    cmd = [str(HS), "play", "--p1", spec(stage, p1), "--p2", spec(stage, p2), "--games", str(games),
           "--seed", str(seed), "--parallel", str(parallel), "--out", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"!! {p1} vs {p2} exit {r.returncode}: {r.stderr[-500:]}", file=sys.stderr)
    return out


def collect(out_root):
    """Yield (p1, p2, result) for every finished game."""
    for d in sorted(out_root.glob("*__vs__*")):
        p1, p2 = d.name.split("__vs__")
        for rf in sorted(d.glob("g_*/result.json")):
            yield p1, p2, json.loads(rf.read_text())


def bradley_terry_elo(names, wins, iters=500):
    """Fit Bradley-Terry strengths (draws = half wins) and map to Elo, mean 1500."""
    s = {n: 1.0 for n in names}
    for _ in range(iters):
        new = {}
        for i in names:
            w = sum(wins[i][j] for j in names if j != i)
            denom = sum((wins[i][j] + wins[j][i]) / (s[i] + s[j]) for j in names if j != i)
            new[i] = w / denom if denom and w else 1e-6
        g = math.exp(sum(math.log(v) for v in new.values()) / len(new))
        s = {k: v / g for k, v in new.items()}
    return {n: 1500 + 400 * math.log10(s[n]) for n in names}


def report(out_root, names):
    wins = {a: {b: 0.0 for b in names} for a in names}
    games = {a: {b: 0 for b in names} for a in names}
    first = {"first": 0, "total": 0}
    stats = {a: {"forfeits": 0, "illegal": 0, "timeouts": 0, "voided": 0} for a in names}
    for p1, p2, r in collect(out_root):
        quota = r["reason"] == "forfeit_exit" and "api status 429" in json.dumps(r.get("notes"))
        if r["reason"] in ("void_engine_error", "aborted") or quota:  # quota = our account's rate limit, not the skill
            stats[p1]["voided"] += 1
            stats[p2]["voided"] += 1
            continue
        side = {1: p1, 2: p2}
        for k, n in side.items():
            stats[n]["illegal"] += r["illegal_counts"][str(k)]
            stats[n]["timeouts"] += r["timeouts"][str(k)]
        if r["reason"].startswith("forfeit"):
            stats[side[3 - r["winner"]]]["forfeits"] += 1
        games[p1][p2] += 1
        games[p2][p1] += 1
        if r["winner"] is None:
            wins[p1][p2] += 0.5
            wins[p2][p1] += 0.5
        else:
            wins[side[r["winner"]]][side[3 - r["winner"]]] += 1
            first["total"] += 1
            first["first"] += r["winner"] == r["first_player"]

    elo = bradley_terry_elo(names, wins)
    order = sorted(names, key=lambda n: -elo[n])
    tot = {n: (sum(wins[n].values()), sum(games[n].values())) for n in names}
    lines = ["| Rank | Deck | Elo | Win % | Games | Forfeits | Illegal | Timeouts | Voided |", "|---:|---|---:|---:|---:|---:|---:|---:|---:|"]
    for i, n in enumerate(order, 1):
        w, g = tot[n]
        st = stats[n]
        lines.append(f"| {i} | {n} | {elo[n]:.0f} | {100 * w / g:.1f} | {g} | {st['forfeits']} | {st['illegal']} | {st['timeouts']} | {st['voided']} |" if g else f"| {i} | {n} | - | - | 0 | | | | |")
    lines += ["", "Win % of row deck vs column deck:", "",
              "| vs | " + " | ".join(n[:10] for n in order) + " |", "|---|" + "---:|" * len(order)]
    for a in order:
        cells = [f"{100 * wins[a][b] / games[a][b]:.0f}" if games[a][b] else "–" for b in order]
        lines.append(f"| {a} | " + " | ".join(cells) + " |")
    if first["total"]:
        lines.append(f"\nFirst player won {100 * first['first'] / first['total']:.1f}% of {first['total']} decided games.")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["a", "b", "c"], help="c: --hero (our script player, no model) vs every deck")
    ap.add_argument("--hero", default="player", choices=["player", "rulebot"], help="stage c: who plays player/deck.json")
    ap.add_argument("--decks", help="comma list (default: every folder in decks/)")
    ap.add_argument("--games", type=int, default=100, help="stage a: games per pairing")
    ap.add_argument("--vs-greedy", type=int, default=6, help="stage b: games per deck vs greedy")
    ap.add_argument("--pair-games", type=int, default=4, help="stage b: games per deck pairing")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--report-only", action="store_true")
    a = ap.parse_args()

    decks = a.decks.split(",") if a.decks else sorted(p.name for p in (ROOT / "decks").iterdir() if (p / "deck.json").exists())
    out_root = ROOT / "games" / (f"stagec_{a.hero}" if a.stage == "c" else f"stage{a.stage}")
    names = decks + ["greedy-mage"]
    jobs = []
    if a.stage == "c":
        for x in names:
            jobs += [(a.hero, x, a.games // 2, a.workers), (x, a.hero, a.games // 2, a.workers)]
        names = [a.hero] + names
        a.workers = 1  # each run already plays its games in parallel
    elif a.stage == "a":
        for x, y in itertools.combinations(names, 2):
            jobs += [(x, y, a.games // 2, 1), (y, x, a.games // 2, 1)]
    else:
        for x in decks:
            jobs += [(x, "greedy-mage", a.vs_greedy // 2, 1), ("greedy-mage", x, a.vs_greedy // 2, 1)]
        for x, y in itertools.combinations(decks, 2):
            jobs += [(x, y, a.pair_games // 2, 1), (y, x, a.pair_games // 2, 1)]
    if not a.report_only:
        print(f"stage {a.stage}: {len(jobs)} runs, {sum(j[2] for j in jobs)} games", file=sys.stderr)
        with ThreadPoolExecutor(a.workers) as ex:
            list(ex.map(lambda j: run(a.stage, j[0], j[1], j[2], a.seed, j[3], out_root), jobs))
    print(report(out_root, names))


if __name__ == "__main__":
    main()
