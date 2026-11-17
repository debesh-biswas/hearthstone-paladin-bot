"""B5 parallel process-agent games; B1 every written file validates against the schemas."""

import json
import shutil
import subprocess
import sys

import pytest

from conftest import EXAMPLE, assert_valid, load_json, read_jsonl


def _play(args, cwd):
    out = subprocess.run([sys.executable, "-m", "hs_arena", "play", *args], cwd=cwd, capture_output=True,
                         text=True, encoding="utf-8", timeout=900)
    assert out.returncode == 0, out.stdout + out.stderr
    return out.stdout


def _validate_game_dir(gd, validators):
    n = 0
    game = load_json(gd / "game.json")
    assert_valid(validators["game"], game, gd / "game.json")
    result = load_json(gd / "result.json")
    assert_valid(validators["result"], result, gd / "result.json")
    for k, ev in enumerate(read_jsonl(gd / "replay.jsonl")):
        assert_valid(validators["event"], ev, f"{gd}/replay.jsonl:{k + 1}")
        n += 1
    for p in ("p1", "p2"):
        pd = gd / p
        if (pd / "state.json").exists():
            assert_valid(validators["state"], load_json(pd / "state.json"), pd / "state.json")
            n += 1
        d = pd / "decisions"
        if d.exists():
            for f in sorted(d.iterdir()):
                kind = "state" if f.name.endswith(".state.json") else "action"
                assert_valid(validators[kind], load_json(f), f)
                n += 1
    return n + 2


def test_parallel_process_games_are_isolated(tmp_path, validators):
    a = tmp_path / "agent_a"
    b = tmp_path / "agent_b"
    shutil.copytree(EXAMPLE, a)
    shutil.copytree(EXAMPLE, b)
    for d, name in ((a, "agent-a"), (b, "agent-b")):
        m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
        m["name"] = name
        (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    out = tmp_path / "games"
    stdout = _play(["--p1", str(a), "--p2", str(b), "--games", "8", "--parallel", "4", "--seed", "500",
                    "--out", str(out)], cwd=tmp_path)
    dirs = sorted(p for p in out.iterdir() if p.is_dir())
    assert len(dirs) == 8
    seeds = set()
    for gd in dirs:
        result = load_json(gd / "result.json")
        game = load_json(gd / "game.json")
        assert result["game_id"] == game["game_id"] == gd.name
        assert result["reason"] in ("hero_death", "draw")
        assert result["illegal_counts"] == {"1": 0, "2": 0}
        seeds.add(game["seed"])
        events = read_jsonl(gd / "replay.jsonl")
        assert events[-1] == {"event": "game_over", "winner": result["winner"], "reason": result["reason"]}
        for p, name in (("p1", "agent-a"), ("p2", "agent-b")):
            assert game["players"][int(p[1]) - 1]["name"] == name
            states = sorted((gd / p / "decisions").glob("*.state.json"))
            actions = sorted((gd / p / "decisions").glob("*.action.json"))
            assert len(actions) == result["decisions"][p[1]]
            for f in states:
                s = load_json(f)
                assert s["game_id"] == gd.name and s["player"] == int(p[1])
            assert not (gd / p / "action.json").exists()
            assert not (gd / p / "work").exists()
        _validate_game_dir(gd, validators)
    assert seeds == set(range(500, 508))
    assert "games 8  counted 8" in stdout


@pytest.mark.slow
def test_files_of_20_games_validate(tmp_path, validators):
    out = tmp_path / "games"
    _play(["--p1", str(EXAMPLE), "--p2", "greedy", "--games", "10", "--parallel", "4", "--seed", "900",
           "--out", str(out)], cwd=tmp_path)
    _play(["--p1", "random", "--p2", str(EXAMPLE), "--games", "10", "--parallel", "4", "--seed", "950",
           "--out", str(out)], cwd=tmp_path)
    dirs = sorted(p for p in out.iterdir() if p.is_dir())
    assert len(dirs) == 20
    total = sum(_validate_game_dir(gd, validators) for gd in dirs)
    print(f"validated {total} files/lines from 20 games")
