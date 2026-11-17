"""Tougher local stand-ins for the course's Bot 2 and Astra: their rebuilt lists, script-piloted, weights tuned for
strength against our two submitted Control lists (real results: Bot 2 6/8, Astra 3/8 vs ~95% / ~80% locally).

    python tools/standins.py tune     # coordinate descent of each stand-in's weights; writes research/weights/standin-<opp>.json
    python tools/standins.py check    # both Control lists vs every stand-in, split by who went first
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fastsim  # noqa: E402
import selfplay  # noqa: E402

ROOT = fastsim.ROOT
OUT = ROOT / "games" / "standins"
WEIGHTS = ROOT / "research" / "weights"
BOT2 = "research/opponents/bot2-face-hunter.json"
ASTRA = "research/opponents/astra-zoo-warlock.json"
# Bot 2's cheap cards (local opponent only; Astra's rule lives in move.py).
fastsim.move.MULLIGAN["bot2-face-hunter"] = {
    "always": {"CS2_188", "EX1_008", "EX1_029", "DS1_175", "EX1_010", "CS2_173", "NEW1_019"},
    "with_early": {"EX1_536", "CS2_124", "EX1_538"}, "second": set()}

SUB2 = ROOT / "player" / "deck.json"
SUB1 = OUT / "control-sub1.json"  # submission 1 list: Guardian of Kings instead of Doomsayer
OURS = {"sub1": SUB1, "sub2": SUB2}


def lists():
    OUT.mkdir(parents=True, exist_ok=True)
    d = json.loads(SUB2.read_text())
    if "NEW1_021" in d["cards"]:
        d["cards"][d["cards"].index("NEW1_021")] = "CS2_088"
    SUB1.write_text(json.dumps(d, indent=1))
    return {**fastsim.BASE_W, **d["weights"]}


def tune():
    our_w = lists()
    field = [f"script:{p.relative_to(ROOT)}" for p in OURS.values()]
    for name, deck, start in [("bot2", BOT2, {}), ("astra", ASTRA, json.loads((ROOT / "research" / "weights" / "astra-strong.json").read_text()))]:
        w = selfplay.tune(name, deck, {**fastsim.BASE_W, **start}, field, {f: our_w for f in field}, seed=71000, games=400)
        (WEIGHTS / f"standin-{name}.json").write_text(json.dumps(w, indent=1))


def check(games=1000):
    our_w = lists()
    opps = {"bot2 greedy": (BOT2, None),
            "bot2 script tuned": (f"script:{BOT2}", json.loads((WEIGHTS / "standin-bot2.json").read_text())),
            "astra strong (old)": (f"script:{ASTRA}", json.loads((ROOT / "research" / "weights" / "astra-strong.json").read_text())),
            "astra tuned": (f"script:{ASTRA}", json.loads((WEIGHTS / "standin-astra.json").read_text()))}
    print(f"Win % of our list, {games} games per cell (half each seat), seeds 73000+\n")
    print("| Opponent | " + " | ".join(f"{k} 1st | {k} 2nd | {k} all" for k in OURS) + " |")
    print("|---|" + "---:|" * 3 * len(OURS))
    for label, (spec, ow) in opps.items():
        cells = []
        for deck in OURS.values():
            o, bad = fastsim.run(games, our_w, deck, field=[spec], seed=73000, opp_w=ow, split=True)
            f, s = o[f"{spec}|first"], o[f"{spec}|second"]
            cells += [f"{100 * f[0] / f[1]:.1f}", f"{100 * s[0] / s[1]:.1f}", f"**{100 * (f[0] + s[0]) / (f[1] + s[1]):.1f}**"]
            assert not bad, bad
        print(f"| {label} | " + " | ".join(cells) + " |", flush=True)


if __name__ == "__main__":
    {"tune": tune, "check": check}[sys.argv[1]]()
