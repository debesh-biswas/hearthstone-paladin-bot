"""Script-only tuning loop: tune every deck against all our script decks, round-robin sim, repeat until stopped.

    python tools/selfplay.py        # resumes from games/selfplay/state.json; kill it to stop
Round 0 is a sim of the starting weights (games/tune/*.json). Each later round: every deck does one coordinate-descent
pass (each weight x0.67 and x1.5) against all 7 script decks, mirror included, at their round-start weights. A change is
kept only if it gains more than MARGIN. Then a round robin on fresh seeds, with the other skills' own pilots added.
Output: games/selfplay/round<r>.md and .json, plus state.json, saved after every deck.
"""

import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402

OUT = fastsim.ROOT / "games" / "selfplay"
PILOTS = ["burst-shaman", "infernal-warlock", "pressure-hunter"]  # decks/<name>/scripts/move.py
TUNE_GAMES = 200   # per opponent per trial (half each seat)
SIM_GAMES = 1000   # per pairing
MARGIN = 0.005     # ponytail: fixed noise margin (~0.4 SE at 1,400 games); raise TUNE_GAMES if weights drift


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def tune_deck(name, st, frozen, seed):
    field = [f"script:{d}" for d in st["decks"].values()]
    opp_ws = {f"script:{st['decks'][n]}": frozen[n] for n in frozen}
    return tune(name, st["decks"][name], st["weights"][name], field, opp_ws, seed)


def tune(name, deck, w, field, opp_ws, seed, games=TUNE_GAMES, only=None):
    """One coordinate-descent pass of every weight (x0.67, x1.5) against field; returns the new weights.
    only="first"/"second": score only the games where we went first/second."""
    w = dict(w)

    def score(trial):
        out, bad = fastsim.run(games, trial, deck, field=field, seed=seed, opp_ws=opp_ws, split=bool(only))
        out = {k: v for k, v in out.items() if not only or k.endswith(only)}
        return sum(v[0] for v in out.values()) / sum(v[1] for v in out.values()), bad

    best, _ = score(w)
    log(f"{name}: start {100 * best:.1f}%")
    for key in fastsim.BASE_W:
        v = w[key]
        for nv in ([round(v * 0.67, 3), round(v * 1.5, 3)] if v else [0.5]):
            win, bad = score({**w, key: nv})
            log(f"{name}: {key} {v} -> {nv}: {100 * win:.1f}% (forfeits/voids {bad})")
            if win > best + MARGIN:
                best, w = win, {**w, key: nv}
    log(f"{name}: BEST {100 * best:.1f}% {json.dumps({k: w[k] for k in w if w[k] != fastsim.BASE_W[k]})}")
    return w


def sim(st, r):
    seed = 60000 + 1000 * r
    sides = {n: (d, st["weights"][n], f"script:{d}") for n, d in st["decks"].items()}
    sides |= {f"{p} (own pilot)": (f"pilot:decks/{p}", {}, f"pilot:decks/{p}") for p in PILOTS}
    names = list(sides)
    wins, bad_total = {x: {} for x in names}, 0
    for x, y in itertools.combinations(names, 2):
        out, bad = fastsim.run(SIM_GAMES, sides[x][1], sides[x][0], field=[sides[y][2]], seed=seed, opp_w=sides[y][1])
        w, g = next(iter(out.values()))
        wins[x][y], wins[y][x], bad_total = [w, g], [g - w, g], bad_total + bad
        log(f"round {r} sim: {x} vs {y}: {w}/{g} (forfeits/voids {bad})")
    tot = {x: sum(v[0] for v in wins[x].values()) / sum(v[1] for v in wins[x].values()) for x in names}
    scripts = list(st["decks"])
    tot_s = {x: sum(wins[x][y][0] for y in scripts if y != x) / sum(wins[x][y][1] for y in scripts if y != x) for x in names}
    order = sorted(names, key=lambda x: -tot_s[x])
    md = [f"## Round {r}: round robin (seeds {seed}+, {SIM_GAMES} games per pairing, half each seat; "
          f"forfeits/voids {bad_total})\n", "Win % of row vs column. \"vs scripts\" counts only our 7 script decks.\n",
          "| vs | " + " | ".join(order) + " | vs scripts | vs all |", "|---|" + "---:|" * (len(order) + 2)]
    for x in order:
        cells = [f"{100 * wins[x][y][0] / wins[x][y][1]:.1f}" if y != x else "–" for y in order]
        md.append(f"| {x} | " + " | ".join(cells) + f" | **{100 * tot_s[x]:.1f}** | {100 * tot[x]:.1f} |")
    md.append("\nWeights (changed from defaults): " + "; ".join(
        f"{n} {json.dumps({k: v for k, v in st['weights'][n].items() if v != fastsim.BASE_W[k]})}" for n in scripts))
    (OUT / f"round{r}.md").write_text("\n".join(md) + "\n")
    (OUT / f"round{r}.json").write_text(json.dumps({"wins": wins, "weights": st["weights"], "bad": bad_total}, indent=1))
    log(f"round {r} sim done: " + ", ".join(f"{x} {100 * tot_s[x]:.1f}" for x in order))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sp = OUT / "state.json"
    if sp.exists():
        st = json.loads(sp.read_text())
    else:
        tuned = {p.stem: json.loads(p.read_text()) for p in sorted((fastsim.ROOT / "games" / "tune").glob("*.json"))}
        st = {"round": 0, "phase": "sim", "done": [], "decks": {n: t["deck"] for n, t in tuned.items()},
              "weights": {n: {**fastsim.BASE_W, **t["weights"]} for n, t in tuned.items()}}
    save = lambda: sp.write_text(json.dumps(st, indent=1))  # noqa: E731
    while True:
        r = st["round"]
        if st["phase"] == "tune":
            frozen = st.setdefault("frozen", {n: dict(w) for n, w in st["weights"].items()})
            for n in st["decks"]:
                if n not in st["done"]:
                    st["weights"][n] = tune_deck(n, st, frozen, 20000 + 1000 * r)
                    st["done"].append(n)
                    save()
            st |= {"phase": "sim", "done": []}
            st.pop("frozen")
            save()
        sim(st, r)
        st |= {"round": r + 1, "phase": "tune"}
        save()


if __name__ == "__main__":
    main()
