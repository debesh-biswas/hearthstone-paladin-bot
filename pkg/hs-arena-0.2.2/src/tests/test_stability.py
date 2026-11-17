"""A5 engine stability, D1 random bot legality, D2 greedy strength/speed/determinism."""

import multiprocessing as mp
import random
import time
from concurrent.futures import ProcessPoolExecutor

import pytest

from helpers_engine import stability_worker
from hs_arena.agents import GreedyBot, RandomBot
from hs_arena.deck import load_deck, random_deck
from hs_arena._resources import GREEDY_DECK
from hs_arena.protocol import Config
from hs_arena.runner import play_game


def _batches(kind, start, total, chunk=25):
    return [(kind, s, min(chunk, start + total - s)) for s in range(start, start + total, chunk)]


def _run_batches(batches):
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as pool:
        games = []
        for r in pool.map(stability_worker, batches):
            games += r["games"]
    return games


def _check(games, n):
    assert len(games) == n
    errors = [g for g in games if g["engine_error"] or g["reason"] == "void_engine_error"]
    assert not errors, f"engine errors (add the cards to pool/blacklist.txt with a reason): {errors[:10]}"
    illegal = [g for g in games if g["illegal"] != {"1": 0, "2": 0}]
    assert not illegal, illegal[:5]


@pytest.mark.slow
def test_500_random_vs_random():
    games = _run_batches(_batches("random", 10_000, 500))
    _check(games, 500)


@pytest.mark.slow
def test_200_greedy_vs_greedy():
    games = _run_batches(_batches("greedy", 20_000, 200))
    _check(games, 200)


def test_bots_smoke(tmp_path):
    """Fast variant: a few games of each pairing with random pool decks."""
    for kind in ("random", "greedy"):
        r = stability_worker((kind, 1, 3))
        _check(r["games"], 3)


def _greedy_vs_random(tmp_path, seed, greedy_first=True):
    rng = random.Random(seed)
    g = GreedyBot("greedy", load_deck(GREEDY_DECK))
    rb = RandomBot("random", random_deck(rng))
    players = {1: g, 2: rb} if greedy_first else {1: rb, 2: g}
    r = play_game(players, game_dir=tmp_path / f"g{seed}", game_id=f"g{seed}", seed=seed, config=Config(keep_decisions=False))
    gi = 1 if greedy_first else 2
    return r, gi


@pytest.mark.slow
def test_greedy_beats_random_90_percent(tmp_path):
    from hs_arena._fp import init_engine

    init_engine()
    wins = 0
    worst = 0.0
    for k in range(200):
        t = time.perf_counter()
        r, gi = _greedy_vs_random(tmp_path, 30_000 + k, greedy_first=(k % 2 == 0))
        worst = max(worst, time.perf_counter() - t)
        assert r["illegal_counts"][str(gi)] == 0
        wins += r["winner"] == gi
    print(f"greedy won {wins}/200 vs random; slowest game {worst:.2f} s")
    assert wins >= 180
    assert worst < 2.0


def test_greedy_deterministic_and_fast(tmp_path):
    from hs_arena._fp import init_engine

    init_engine()
    reps = []
    for run in range(2):
        players = {1: GreedyBot("greedy", load_deck(GREEDY_DECK)), 2: GreedyBot("greedy", load_deck(GREEDY_DECK))}
        t = time.perf_counter()
        r = play_game(players, game_dir=tmp_path / f"d{run}", game_id="det", seed=4242, config=Config(keep_decisions=False))
        assert time.perf_counter() - t < 2.0
        assert r["illegal_counts"] == {"1": 0, "2": 0}
        reps.append((tmp_path / f"d{run}" / "replay.jsonl").read_text(encoding="utf-8"))
    assert reps[0] == reps[1]
    wins = sum(_greedy_vs_random(tmp_path, 50 + k, k % 2 == 0)[0]["winner"] == (1 if k % 2 == 0 else 2) for k in range(10))
    assert wins >= 8
