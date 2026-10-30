"""Fast local tuning: play player/scripts/move.py in-process (no MCP, no model).

Opponents are greedy-piloted decks (names from decks/ or greedy-mage) or `script:<deck.json>` (our planner on that
deck). Same seeds and seat split as `tournament.py c`: half the games with us as P1, half as P2.
    python tools/fastsim.py --games 500                                   # aggro list vs every deck
    python tools/fastsim.py --deck decks/steady-paladin/deck.json --set face=0.7
    python tools/fastsim.py --deck decks/steady-paladin/deck.json --opponents script:decks/aggro-paladin/deck.json
    python tools/fastsim.py --deck pilot:decks/burst-shaman          # another skill's own scripts/move.py as our side
"""

import argparse
import importlib.util
import json
import shutil
import sys
import tempfile
from multiprocessing import Pool
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "player" / "scripts"))

import move  # noqa: E402
from hs_arena.agents import make_player  # noqa: E402
from hs_arena.agents.base import Decision, Player  # noqa: E402
from hs_arena.deck import load_deck  # noqa: E402
from hs_arena.protocol import Config  # noqa: E402
from hs_arena.runner import play_game  # noqa: E402

FIELD = sorted(p.name for p in (ROOT / "decks").iterdir() if (p / "deck.json").exists()) + ["greedy-mage"]
BASE_W = dict(move.W)


class ScriptPlayer(Player):
    """Our planner with its own deck and weights (move.py keeps them in module globals, so swap per call)."""
    kind = "script"

    def __init__(self, name, deck_path, weights):
        super().__init__(name, load_deck(str(deck_path)))
        self.deck_path, self.w = Path(deck_path), {**BASE_W, **weights}

    def decide(self, state):
        move.W, move.DECK_PATH = self.w, self.deck_path
        return Decision("action", move.decide(state))


class PilotPlayer(Player):
    """Another skill's own move script (a decide(state) function), e.g. decks/burst-shaman/scripts/move.py."""
    kind = "pilot"

    def __init__(self, name, skill_dir):
        super().__init__(name, load_deck(str(Path(skill_dir) / "deck.json")))
        path = Path(skill_dir) / "scripts" / "move.py"
        spec = importlib.util.spec_from_file_location(f"pilot_{Path(skill_dir).name.replace('-', '_')}", path)
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)

    def decide(self, state):
        return Decision("action", self.mod.decide(state))


def _opponent(spec, seat, seed, opp_w):
    if spec.startswith("script:"):
        return ScriptPlayer("opp", ROOT / spec[7:], opp_w)
    if spec.startswith("pilot:"):
        return PilotPlayer("opp", ROOT / spec[6:])
    if spec.endswith(".json"):  # any deck file, greedy-piloted
        return make_player(f"greedy:{ROOT / spec}", seat, seed)
    deck = "greedy" if spec == "greedy-mage" else f"greedy:{ROOT / 'decks' / spec / 'deck.json'}"
    return make_player(deck, seat, seed)


def _game(job):
    opp, seed, seat, deck_path, w, opp_w = job
    me = PilotPlayer("player", Path(deck_path[6:])) if deck_path.startswith("pilot:") else ScriptPlayer("player", deck_path, w)
    players = {seat: me, 3 - seat: _opponent(opp, 3 - seat, seed, opp_w)}
    tmp = Path(tempfile.mkdtemp(prefix="fastsim_"))
    try:
        r = play_game(players, game_dir=tmp / "g", game_id=f"g{seed}", seed=seed, config=Config(keep_decisions=False))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return opp, seat, r["winner"], r["reason"], r.get("first_player") == seat


def run(games, w=None, deck=None, field=FIELD, seed=1000, workers=14, opp_w=None, opp_ws=None, split=False):
    """opp_ws: {opponent spec: weights} for script: opponents that each need their own weights (default opp_w).
    split: key results by "<opponent>|first" / "<opponent>|second" (whether we went first)."""
    deck_path = str(deck or ROOT / "player" / "deck.json")
    jobs = [(o, seed + k, s, deck_path, w or {}, (opp_ws or {}).get(o, opp_w or {}))
            for o in field for s in (1, 2) for k in range(1, games // 2 + 1)]
    with Pool(workers) as pool:
        rows = pool.map(_game, jobs, chunksize=4)
    out = {f"{o}|{f}": [0, 0] for o in field for f in ("first", "second")} if split else {o: [0, 0] for o in field}
    bad = 0
    for opp, seat, winner, reason, first in rows:
        if split:
            opp = f"{opp}|{'first' if first else 'second'}"
        out[opp][0] += winner == seat
        out[opp][1] += 1
        bad += reason.startswith("forfeit") or reason.startswith("void")
    return out, bad


def _parse(sets):
    return {k: float(v) for k, v in (s.split("=") for s in sets)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=500, help="per opponent")
    ap.add_argument("--set", action="append", default=[], help="our weight override, e.g. reach=4")
    ap.add_argument("--deck", help="deck.json for our script (default player/deck.json), or pilot:<skill dir>")
    ap.add_argument("--opponents", help="comma list: deck names / greedy-mage / script:<deck.json> / pilot:<skill dir>")
    ap.add_argument("--opp-set", action="append", default=[], help="weight override for script: opponents")
    ap.add_argument("--seed", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=14)
    a = ap.parse_args()
    w = _parse(a.set)
    field = a.opponents.split(",") if a.opponents else FIELD
    out, bad = run(a.games, w, a.deck, field, a.seed, a.workers, _parse(a.opp_set))
    tw = tg = 0
    for o in sorted(out, key=lambda o: out[o][0] / out[o][1]):
        wins, g = out[o]
        tw, tg = tw + wins, tg + g
        print(f"{o:18} {100 * wins / g:5.1f}%  ({wins}/{g})")
    print(f"{'TOTAL':18} {100 * tw / tg:5.1f}%  ({tw}/{tg})  forfeits/voids {bad}  {a.deck or 'player/deck.json'} {json.dumps(w)}")


if __name__ == "__main__":
    main()
