"""Skill submissions and the skill seat (PLANNING.md Â§6): validation, the game MCP server, client seats end to end,
first-exit forfeits without restarts, harness commands and stop classification. No model is called."""

import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

from conftest import ROOT, assert_valid
from hs_arena.cli import main
from hs_arena.protocol import Config
from hs_arena.runner import run_game
from hs_arena.skill import SkillError, load_skill
from hs_arena.skill.seat import CODEX_DISABLED_FEATURES, classify_stop, claude_command, codex_command, system_prompt

EXAMPLES = ROOT / "examples"
GREEDY_SKILL = EXAMPLES / "greedy_skill"
GREEDY_CLIENT = EXAMPLES / "greedy_mcp_client"


def _copy(src: Path, dst: Path) -> Path:
    shutil.copytree(src, dst)
    return dst


# ------------------------------------------------------------------------------------------- validation

def test_example_skills_load():
    for name in ("greedy_skill", "starter_skill"):
        skill = load_skill(EXAMPLES / name)
        assert skill.model == "haiku" and skill.harness == "claude" and skill.model_id == "claude-haiku-5-5"
        assert skill.body.strip() and not hasattr(skill, "deck")


def _errors(path: Path) -> list[str]:
    with pytest.raises(SkillError) as e:
        load_skill(path)
    return e.value.errors


def test_skill_errors(tmp_path):
    s = _copy(GREEDY_SKILL, tmp_path / "s")
    (s / "SKILL.md").unlink()
    assert any("SKILL.md: file not found" in e for e in _errors(s))

    (s / "SKILL.md").write_text("no frontmatter\n", encoding="utf-8")
    assert any("frontmatter" in e for e in _errors(s))

    (s / "SKILL.md").write_text("---\nname: x\ndescription: y\n---\nbody\n", encoding="utf-8")
    assert any("'model'" in e for e in _errors(s))

    (s / "SKILL.md").write_text("---\nname: x\ndescription: y\nmodel: opus\n---\nbody\n", encoding="utf-8")
    assert any("must be one of: haiku, luna" in e for e in _errors(s))

    (s / "SKILL.md").write_text("---\nname: x\ndescription: y\nmodel: luna\n---\nbody\n", encoding="utf-8")
    assert load_skill(s).harness == "codex"
    (s / "game").mkdir()
    assert any("'game' is reserved" in e for e in _errors(s))
    (s / "game").rmdir()

    deck = json.loads((s / "deck.json").read_text(encoding="utf-8"))
    deck["cards"] = deck["cards"][:29]
    (s / "deck.json").write_text(json.dumps(deck), encoding="utf-8")
    assert load_skill(s).body  # optional recipe is never loaded or validated by the host
    (s / "deck.json").unlink()
    assert load_skill(s).body


def test_validate_and_prompt_commands(tmp_path, capsys):
    assert main(["validate", str(GREEDY_SKILL), "--no-game"]) == 0
    out = capsys.readouterr().out
    assert "SKILL.md: OK" in out and "model haiku" in out and "deck.json is optional" in out
    bad = _copy(GREEDY_SKILL, tmp_path / "bad")
    (bad / "deck.json").unlink()
    (bad / "SKILL.md").unlink()
    assert main(["validate", str(bad), "--no-game"]) == 1
    assert "ERROR" in capsys.readouterr().out
    assert main(["prompt", str(GREEDY_SKILL), "--player", "2"]) == 0
    text = capsys.readouterr().out
    assert "as player 2" in text and "=== SKILL: greedy-mage ===" in text and "scripts/greedy_move.py" in text
    assert '{"type":"hero_power"}' in text and "(no target)" in text


# ------------------------------------------------------------------------------------------- MCP server

class _Mcp:
    def __init__(self, box: Path):
        env = dict(os.environ, HS_MCP_WAIT_S="0.5")
        self.p = subprocess.Popen([sys.executable, "-m", "hs_arena.skill.mcp_server", str(box)], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, encoding="utf-8", env=env)
        self.n = 0

    def req(self, method, params=None):
        self.n += 1
        self.p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params or {}}) + "\n")
        self.p.stdin.flush()
        return json.loads(self.p.stdout.readline())

    def call(self, tool, **args):
        return self.req("tools/call", {"name": tool, "arguments": args})["result"]["content"][0]["text"]

    def close(self):
        self.p.stdin.close()
        self.p.wait(timeout=10)


def test_mcp_server_tools(tmp_path):
    box = tmp_path / "box"
    box.mkdir()
    m = _Mcp(box)
    try:
        assert m.req("initialize", {"protocolVersion": "2024-11-05"})["result"]["serverInfo"]["name"] == "hs-arena-seat"
        assert [t["name"] for t in m.req("tools/list")["result"]["tools"]] == ["wait", "act", "history"]
        assert m.call("wait").startswith("No decision for you yet")
        (box / "state.txt").write_text("STATE TEXT", encoding="utf-8")
        (box / "state.json").write_text(json.dumps({"seq": 1, "phase": "mulligan"}), encoding="utf-8")
        assert m.call("wait") == "YOUR DECISION (seq 1):\nSTATE TEXT"
        reply = m.call("act", seq=1, action={"type": "mulligan", "replace": []})
        assert reply.startswith("Submitted seq 1") and "No decision for you yet" in reply
        assert json.loads((box / "action.json").read_text(encoding="utf-8")) == {
            "seq": 1, "action": {"type": "mulligan", "replace": []}}
        assert "not the pending decision" in m.call("act", seq=1, action={"type": "end_turn"})
        (box / "history.txt").write_text("Game start: P1 (you) goes first.\n", encoding="utf-8")
        assert m.call("history") == "EVENTS SO FAR (your view):\nGame start: P1 (you) goes first."
        (box / "game_over.txt").write_text("FINAL", encoding="utf-8")
        assert m.call("wait").startswith("GAME OVER")
        assert m.req("tools/call", {"name": "peek", "arguments": {}})["error"]
        calls = [json.loads(x)["tool"] for x in (box / "calls.jsonl").read_text(encoding="utf-8").splitlines()]
        assert calls[:3] == ["wait", "wait", "act"]
    finally:
        m.close()


# ------------------------------------------------------------------------------------------- client seats

def test_client_seat_game(tmp_path, validators):
    gdir = tmp_path / "g1"
    r = run_game(f"client:{GREEDY_CLIENT}", "random", game_dir=gdir, game_id="g_test_000001", seed=3,
                 config=Config(decision_timeout_s=60))
    assert r["reason"] == "hero_death" and r["illegal_counts"] == {"1": 0, "2": 0} and "notes" not in r
    assert r["players"][0]["kind"] == "client"
    assert_valid(validators["result"], r, "result.json")
    assert_valid(validators["game"], json.loads((gdir / "game.json").read_text(encoding="utf-8")), "game.json")
    seat = gdir / "p1" / "seat"
    info = json.loads((seat / "seat.json").read_text(encoding="utf-8"))
    assert info["skill_stops"] == 0 and info["course_stops"] == 0 and len(info["sessions"]) == 1
    calls = [json.loads(x)["tool"] for x in (seat / "mcp_calls.jsonl").read_text(encoding="utf-8").splitlines()]
    assert calls.count("act") == r["decisions"]["1"]
    states = sorted((gdir / "p1" / "decisions").glob("*.state.json"))
    actions = sorted((gdir / "p1" / "decisions").glob("*.action.json"))
    assert len(actions) == r["decisions"]["1"] and len(states) == len(actions) + 1  # + the game_over state
    for p in states[:3]:
        assert_valid(validators["state"], json.loads(p.read_text(encoding="utf-8")), p.name)


FLAKY_CLIENT = '''
import json, os, random, subprocess, sys
from pathlib import Path

STOP_ON_LAUNCHES = {stops}
launches = Path("scratch/launches.txt")
n = int(launches.read_text()) + 1 if launches.exists() else 1
launches.write_text(str(n))
p = subprocess.Popen(json.loads(os.environ["HS_ARENA_MCP"]), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                     text=True, encoding="utf-8")
i = 0
def call(tool, **args):
    global i
    i += 1
    p.stdin.write(json.dumps({{"jsonrpc": "2.0", "id": i, "method": "tools/call",
                              "params": {{"name": tool, "arguments": args}}}}) + "\\n")
    p.stdin.flush()
    return json.loads(p.stdout.readline())["result"]["content"][0]["text"]
reply, acted = call("wait"), 0
while not reply.startswith("GAME OVER"):
    if not reply.startswith("YOUR DECISION"):
        reply = call("wait")
        continue
    if n in STOP_ON_LAUNCHES and acted >= 1:
        sys.exit(0)  # stop before the game is over
    s = json.loads(Path("game/state.json").read_text(encoding="utf-8"))
    t = s["legal_actions"][0]
    if t["type"] == "submit_deck":
        deck = json.loads(Path("deck.json").read_text(encoding="utf-8"))
        a = {{"type": "submit_deck", "hero_class": deck["hero_class"], "cards": deck["cards"]}}
    elif t["type"] == "mulligan":
        a = {{"type": "mulligan", "replace": []}}
    elif t["type"] == "choose":
        a = {{"type": "choose", "options": [t["options"][0]["entity_id"]]}}
    else:
        a = {{"type": "end_turn"}}
    reply = call("act", seq=s["seq"], action=a)
    acted += 1
'''


def _flaky(tmp_path: Path, stops: list[int]) -> Path:
    d = tmp_path / f"flaky{len(stops)}"
    d.mkdir()
    shutil.copy2(GREEDY_CLIENT / "deck.json", d / "deck.json")
    (d / "client.py").write_text(textwrap.dedent(FLAKY_CLIENT.format(stops=set(stops))), encoding="utf-8")
    return d


def test_first_skill_session_stop_forfeits_without_warning_or_restart(tmp_path, validators):
    d = _flaky(tmp_path, [1])
    r = run_game(f"client:{d}", "greedy", game_dir=tmp_path / "g1", game_id="g_test_000001", seed=5,
                 config=Config(decision_timeout_s=60))
    assert r["reason"] == "forfeit_exit" and r["winner"] == 2
    assert r["illegal_counts"]["1"] == 0 and r["restarts"]["1"] == 0
    assert len(r["notes"]["1"]) == 1 and "forfeit_exit" in r["notes"]["1"][0]
    assert_valid(validators["result"], r, "result.json")
    info = json.loads((tmp_path / "g1" / "p1" / "seat" / "seat.json").read_text(encoding="utf-8"))
    assert info["skill_stops"] == 1 and len(info["sessions"]) == 1


# ------------------------------------------------------------------------------------------- harness

def test_harness_commands(tmp_path):
    box, sysfile = tmp_path / "box", tmp_path / "sys.md"
    c = claude_command("claude-haiku-5-5", box, sysfile)
    assert c[c.index("--model") + 1] == "claude-haiku-5-5" and c[c.index("--effort") + 1] == "medium"
    tools = c[c.index("--tools") + 1].split(",")
    assert set(tools) == {"Bash", "Read", "Write", "Edit", "Glob", "Grep"}  # no sub-agents, no web tools
    assert "--strict-mcp-config" in c and c[c.index("--append-system-prompt-file") + 1] == str(sysfile)
    x = codex_command("gpt-6-luna", box, tmp_path)
    assert x[x.index("-m") + 1] == "gpt-6-luna" and 'model_reasoning_effort="medium"' in x
    assert x[x.index("-s") + 1] == "workspace-write" and 'web_search="disabled"' in x and "allow_login_shell=false" in x
    disabled = {x[i + 1] for i, a in enumerate(x) if a == "--disable"}
    assert disabled == set(CODEX_DISABLED_FEATURES) and "multi_agent" in disabled and "shell_tool" not in disabled


def test_classify_stop(tmp_path):
    t, err = tmp_path / "t.jsonl", tmp_path / "e.txt"
    err.write_text("", encoding="utf-8")
    t.write_text(json.dumps({"type": "result", "is_error": True, "result": "API Error: 529 overloaded",
                             "api_error_status": 529}) + "\n", encoding="utf-8")
    assert classify_stop("claude", t, err, 1)[0] == "course"
    t.write_text(json.dumps({"type": "result", "is_error": False, "subtype": "success"}) + "\n", encoding="utf-8")
    assert classify_stop("claude", t, err, 0) == ("skill", "the model ended its session before GAME OVER")
    t.write_text(json.dumps({"type": "turn.failed", "error": {"message": "stream disconnected"}}) + "\n", encoding="utf-8")
    assert classify_stop("codex", t, err, 1)[0] == "course"
    t.write_text(json.dumps({"type": "turn.completed", "usage": {}}) + "\n", encoding="utf-8")
    assert classify_stop("codex", t, err, 0)[0] == "skill"
    t.write_text("", encoding="utf-8")
    err.write_text("Please run /login", encoding="utf-8")
    assert classify_stop("claude", t, err, 1)[0] == "course"


def test_system_prompt_has_skill_and_rules():
    text = system_prompt(load_skill(GREEDY_SKILL), 1, 180, 3)
    assert "as player 1" in text and "within 180 seconds" in text and "Reaching 3 illegal" in text
    assert "game/state.json" in text and "scratch/" in text and "do not use the network" in text
    assert "=== SKILL: greedy-mage ===" in text and "python scripts/greedy_move.py" in text
