"""How often our planner picks Astra's real move, from the returned online games (no games played).

    python tools/imitate.py games/sub1_results/games.json                 # match rate vs Astra, default weights
    python tools/imitate.py games/sub1_results/games.json --tune          # coordinate descent on the match rate
For each Astra turn: Astra's board and hero from our last view before its turn, its mana from the next view, and as
its hand the cards it actually played that turn (the rest of its hand is hidden). At every step we compare the
planner's best first action with Astra's real one, then apply Astra's real one (teacher forcing).
"""

import argparse
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "player" / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import move  # noqa: E402
import fastsim  # noqa: E402


def _id(x):
    return x["entity_id"] if isinstance(x, dict) else x


def turns(path, who="astra"):
    """[(start model state, [model actions])] for every opponent turn in every game."""
    out = []
    for g in (g for g in json.load(open(path))["games"] if g["opponent"] == who):
        me, opp = g["student_seat"], 3 - g["student_seat"]
        obs = [o["state"] for o in g["observations"] if o["state"]["phase"] == "main"]
        for before, after in zip(obs, obs[1:]):
            evs = after["events"]
            if not any(e["event"] == "turn_start" and e.get("player") == opp for e in evs):
                continue
            you, them = before["you"], before["opponent"]
            heroes = {them["hero"]["entity_id"]: "me", you["hero"]["entity_id"]: "hero"}
            acts, hand = [], []
            for e in evs:
                if e.get("player") != opp:
                    continue
                if e["event"] == "play_card":
                    c = move.CATALOG.get(e["card_id"], {})
                    hand.append({"entity_id": e["entity_id"], "card_id": e["card_id"], "cost": e["cost"],
                                 "type": c.get("type", "SPELL"), "attack": c.get("attack", 0),
                                 "health": c.get("health", 0), "durability": c.get("durability", 2)})
                    t = e.get("target")
                    acts.append(("play", e["entity_id"], heroes.get(_id(t), _id(t)) if t is not None else None))
                elif e["event"] == "attack":
                    a, t = _id(e["attacker"]), _id(e["target"])
                    acts.append(("attack", heroes.get(a, a), heroes.get(t, t)))
                elif e["event"] == "hero_power":
                    acts.append(("power",))
            acts.append(("end",))
            board = [dict(m, can_attack=not m.get("frozen")) for m in them["board"]]
            power = dict(them["hero_power"], usable=True)
            state = {"you": dict(them, board=board, hand=hand, hero_power=power,
                                 mana=after["opponent"]["max_mana"], deck_remaining_counts={}),
                     "opponent": dict(you, hand_size=len(you["hand"])), "seq": before["seq"]}
            out.append((move.load(state), acts))
    return out


def match(data, w):
    move.W = {**fastsim.BASE_W, **w}
    hit = n = 0
    for root, acts in data:
        rng, s = random.Random(0), root
        for a in acts:
            best = move.search(s, rng)[0][1]
            hit += best == a
            n += 1
            if a == ("end",) or a not in move.gen(s):
                break  # an action our model cannot follow ends this turn's comparison
            s = move.apply(s, a, rng)
    return hit / n, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("games")
    ap.add_argument("--tune", action="store_true")
    ap.add_argument("--set", action="append", default=[])
    a = ap.parse_args()
    data = turns(a.games)
    w = {k: float(v) for k, v in (x.split("=") for x in a.set)}
    best, n = match(data, w)
    print(f"{len(data)} opponent turns, {n} decisions: match {100 * best:.1f}% {json.dumps(w)}", flush=True)
    if not a.tune:
        return
    for _ in range(2):  # two coordinate-descent passes
        for key in fastsim.BASE_W:
            v = w.get(key, fastsim.BASE_W[key])
            for nv in ([round(v * 0.5, 3), round(v * 0.67, 3), round(v * 1.5, 3), round(v * 2, 3)] if v else [0.5, 1.0]):
                r, _ = match(data, {**w, key: nv})
                if r > best:
                    best, w = r, {**w, key: nv}
                    print(f"  {key} -> {nv}: {100 * r:.1f}%", flush=True)
    print(f"BEST match {100 * best:.1f}% {json.dumps(w)}")


if __name__ == "__main__":
    main()
