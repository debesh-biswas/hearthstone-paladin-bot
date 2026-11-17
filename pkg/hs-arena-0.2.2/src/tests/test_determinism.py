"""A6: the same seed with two deterministic bots gives an identical replay.jsonl, also across processes."""

import os
import subprocess
import sys

from hs_arena.protocol import Config
from hs_arena.runner import run_game


def _replay(tmp_path, name, p1, p2, seed):
    run_game(p1, p2, game_dir=tmp_path / name, game_id="g", seed=seed, config=Config(keep_decisions=False))
    return (tmp_path / name / "replay.jsonl").read_text(encoding="utf-8")


def test_same_seed_same_replay_in_process(tmp_path):
    for p1, p2 in (("greedy", "greedy"), ("random", "random"), ("greedy", "random")):
        a = _replay(tmp_path, f"{p1}{p2}a", p1, p2, 123)
        b = _replay(tmp_path, f"{p1}{p2}b", p1, p2, 123)
        assert a == b, (p1, p2)
    assert _replay(tmp_path, "x", "random", "random", 124) != _replay(tmp_path, "y", "random", "random", 123)


def test_same_seed_same_replay_across_processes(tmp_path):
    outs = []
    for k, hashseed in enumerate(("1", "2")):
        out = tmp_path / f"run{k}"
        env = dict(os.environ, PYTHONHASHSEED=hashseed)
        r = subprocess.run(
            [sys.executable, "-m", "hs_arena", "play", "--p1", "greedy", "--p2", "random", "--games", "3",
             "--seed", "77", "--parallel", "1", "--out", str(out)],
            capture_output=True, text=True, env=env, timeout=600,
        )
        assert r.returncode == 0, r.stderr
        outs.append([(d / "replay.jsonl").read_text(encoding="utf-8") for d in sorted(out.iterdir())])
    assert outs[0] == outs[1]


def test_max_turns_knob_ends_in_a_draw(tmp_path):
    r = run_game("greedy", "greedy", game_dir=tmp_path / "m", game_id="m", seed=3,
                 config=Config(keep_decisions=False, max_turns=4))
    assert r["reason"] == "max_turns" and r["winner"] is None and r["turns"] == 5
    assert Config().max_turns is None  # off by default
