"""B3 illegal/crash handling, B4 game over + no orphans, B6 output capture, B7 timeouts, B8 voiding."""

import io
import os
import re
import sys
import threading
import time

from conftest import fast_config, load_json, make_submission, read_jsonl
from hs_arena.agents.process import _StderrPump
from hs_arena.protocol import Config
from hs_arena.runner import run_game


def _decisions(game_dir, p):
    d = game_dir / p / "decisions"
    states = {int(f.name[:5]): load_json(f) for f in sorted(d.glob("*.state.json"))}
    actions = {int(f.name[:5]): load_json(f) for f in sorted(d.glob("*.action.json"))}
    return states, actions


def _pid_alive(pid: int) -> bool:
    if sys.platform == "win32":
        import ctypes

        k = ctypes.WinDLL("kernel32", use_last_error=True)
        h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        code = ctypes.c_ulong()
        k.GetExitCodeProcess(h, ctypes.byref(code))
        k.CloseHandle(h)
        return code.value == 259  # STILL_ACTIVE
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    try:  # a zombie counts as dead
        with open(f"/proc/{pid}/stat") as f:
            return f.read().split()[2] != "Z"
    except OSError:
        return True


BUGGY = """
class Buggy(Agent):
    def decide(self, state):
        if state.phase == "mulligan":
            return Action.mulligan([])
        return Action.play_card(999999)
run(Buggy)
"""


def test_buggy_agent_forfeits_on_third_illegal(tmp_path):
    sub = make_submission(tmp_path, BUGGY)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=3, config=fast_config())
    assert r["reason"] == "forfeit_illegal" and r["winner"] == 2
    assert r["illegal_counts"]["1"] == 3
    ill = [e for e in read_jsonl(gd / "replay.jsonl") if e["event"] == "illegal_action"]
    assert [e["illegal_count"] for e in ill] == [1, 2, 3]
    assert all(e["error"] == "NOT_YOUR_ENTITY" for e in ill)
    states, _ = _decisions(gd, "p1")
    counts = [s["last_action_result"]["illegal_count"] for s in states.values() if s["last_action_result"]]
    assert counts[:2] == [1, 2]
    final = load_json(gd / "p1" / "state.json")
    assert final["phase"] == "game_over" and final["result"]["reason"] == "forfeit_illegal"
    assert final["result"]["you_won"] is False


CRASH_ONCE = """
class CrashOnce(Agent):
    def __init__(self):
        self.rng = random.Random(1)
        self.n = 0
    def decide(self, state):
        self.n += 1
        marker = os.path.join(os.environ["HS_WORK_DIR"], "crashed")
        if self.n == 3 and not os.path.exists(marker):
            open(marker, "w").close()
            sys.stderr.write("crashing on purpose\\n")
            os._exit(3)
        return random_action(state, self.rng)
run(CrashOnce)
"""


def test_first_crash_forfeits_without_restart(tmp_path):
    sub = make_submission(tmp_path, CRASH_ONCE)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=5, config=fast_config())
    assert r["reason"] == "forfeit_exit" and r["winner"] == 2
    assert r["restarts"]["1"] == 0 and r["illegal_counts"]["1"] == 0
    events = read_jsonl(gd / "replay.jsonl")
    kinds = [(e["event"], e.get("error")) for e in events if e["event"] in ("illegal_action", "agent_restart", "agent_failure")]
    assert kinds == [("agent_failure", "AGENT_EXITED")]
    log = (gd / "p1" / "stderr.log").read_text(encoding="utf-8")
    assert "crashing on purpose" in log and "restart #1" not in log
    assert not (gd / "p1" / "work").exists(), "work dir must be wiped after the game"


STUBBORN = """
import subprocess
class Stubborn(Agent):
    def on_game_start(self, info):
        child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(600)"])
        sys.stderr.write(f"CHILD_PID={child.pid} SELF_PID={os.getpid()}\\n")
        sys.stderr.flush()
    def decide(self, state):
        return Action.concede()
    def on_game_over(self, result):
        time.sleep(600)  # ignore the game over: the runtime must kill us after exit_grace_s
run(Stubborn)
"""


def test_game_over_kills_stubborn_agent_and_its_children(tmp_path):
    sub = make_submission(tmp_path, STUBBORN)
    gd = tmp_path / "g"
    t = time.monotonic()
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=1, config=fast_config(exit_grace_s=1.0))
    elapsed = time.monotonic() - t
    assert r["reason"] == "concede" and r["winner"] == 2
    final = load_json(gd / "p1" / "state.json")
    assert final["phase"] == "game_over" and final["result"] == {"winner": 2, "you_won": False, "reason": "concede"}
    assert final["legal_actions"] == []
    log = (gd / "p1" / "stderr.log").read_text(encoding="utf-8")
    m = re.search(r"CHILD_PID=(\d+) SELF_PID=(\d+)", log)
    assert m, log
    time.sleep(0.5)
    assert not _pid_alive(int(m.group(2))), "agent process survived"
    assert not _pid_alive(int(m.group(1))), "agent's child process survived (orphan)"
    assert elapsed < 30


def test_well_behaved_agent_exits_on_game_over(example_copy, tmp_path):
    gd = tmp_path / "g"
    t = time.monotonic()
    r = run_game(str(example_copy), "greedy", game_dir=gd, game_id="g", seed=2, config=fast_config(exit_grace_s=10.0))
    assert time.monotonic() - t < 9, "runtime waited for the full exit grace although the agent exited"
    final = load_json(gd / "p1" / "state.json")
    assert final["phase"] == "game_over" and final["result"]["winner"] == r["winner"]


NOISY = """
class Noisy(Agent):
    def __init__(self):
        self.rng = random.Random(2)
    def on_game_start(self, info):
        chunk = "x" * 1023 + "\\n"
        for _ in range(10 * 1024):
            sys.stdout.write(chunk)
            sys.stderr.write(chunk)
        sys.stdout.flush(); sys.stderr.flush()
    def decide(self, state):
        print("thinking...", state.seq)
        return random_action(state, self.rng)
run(Noisy)
"""


def test_10mb_of_output_does_not_break_the_protocol(tmp_path):
    sub = make_submission(tmp_path, NOISY)
    gd = tmp_path / "g"
    cfg = fast_config(stderr_cap_kb=512)
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=8, config=cfg)
    assert r["reason"] in ("hero_death", "draw")
    assert r["illegal_counts"]["1"] == 0 and r["restarts"]["1"] == 0
    size = (gd / "p1" / "stderr.log").stat().st_size
    assert 512 * 1024 <= size <= 512 * 1024 + 200, size
    assert b"size cap reached" in (gd / "p1" / "stderr.log").read_bytes()[-200:]


class _Chunks:
    """A pipe stand-in that returns fixed chunks, like read1() on a real pipe."""

    def __init__(self, chunks):
        self.chunks = list(chunks)

    def read1(self, n):
        return self.chunks.pop(0) if self.chunks else b""

    def close(self):
        pass


def _pump(chunks, cap):
    sink = io.BytesIO()
    _StderrPump(_Chunks(chunks), sink, [cap, False, threading.Lock()]).run()
    return sink.getvalue()


def test_stderr_cap_marker_on_chunk_boundaries():
    marker = b"\n[hs-arena] stderr.log size cap reached; further output discarded\n"
    # a chunk that fills the cap exactly, then more output (the Linux case: 64 KiB reads, 512 KiB cap)
    assert _pump([b"a" * 4, b"b" * 4, b"c" * 4, b"d" * 4], 8) == b"aaaabbbb" + marker
    # the cap falls inside a chunk
    assert _pump([b"a" * 6, b"b" * 6], 8) == b"aaaaaabb" + marker
    # output ends exactly at the cap: nothing was discarded, so no marker
    assert _pump([b"a" * 4, b"b" * 4], 8) == b"aaaabbbb"


SLEEP_ONCE = """
class SleepOnce(Agent):
    def __init__(self):
        self.rng = random.Random(4)
        self.slept = False
    def decide(self, state):
        if state.phase == "main" and not self.slept:
            self.slept = True
            sys.stderr.write(f"sleeping on seq {state.seq}\\n")
            time.sleep(3.0)   # > 2 s timeout, < 2 timeouts
        return random_action(state, self.rng)
run(SleepOnce)
"""


def test_first_timeout_finishes_game_without_reissuing_decision(tmp_path):
    sub = make_submission(tmp_path, SLEEP_ONCE)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=9, config=fast_config(decision_timeout_s=2.0))
    assert r["reason"] == "forfeit_timeout" and r["winner"] == 2
    assert r["timeouts"]["1"] == 1 and r["illegal_counts"]["1"] == 0 and r["restarts"]["1"] == 0
    events = [e for e in read_jsonl(gd / "replay.jsonl") if e["event"] == "agent_failure"]
    assert events == [{"event": "agent_failure", "player": 1, "error": "TIMEOUT"}]
    log = (gd / "p1" / "stderr.log").read_text(encoding="utf-8")
    slept_seq = int(re.search(r"sleeping on seq (\d+)", log).group(1))
    states, actions = _decisions(gd, "p1")
    assert slept_seq not in actions
    assert states[slept_seq + 1]["phase"] == "game_over"


SLEEP_FOREVER = """
class SleepForever(Agent):
    def decide(self, state):
        if state.phase == "main":
            time.sleep(600)
        return Action.mulligan([])
run(SleepForever)
"""


def test_first_unanswered_decision_forfeits(tmp_path):
    sub = make_submission(tmp_path, SLEEP_FOREVER)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=10, config=fast_config(decision_timeout_s=1.0, exit_grace_s=0.5))
    assert r["reason"] == "forfeit_timeout" and r["winner"] == 2
    assert r["timeouts"]["1"] == 1 and r["illegal_counts"]["1"] == 0 and r["restarts"]["1"] == 0


def test_shipped_default_timeout_is_180s():
    from hs_arena.cli import build_parser

    assert Config().decision_timeout_s == 180.0
    a = build_parser().parse_args(["play", "--p1", "greedy", "--p2", "random"])
    assert a.timeout == 180.0
    assert Config().illegal_limit == a.illegal_limit == 3


def test_engine_exception_voids_the_game(tmp_path, monkeypatch, capsys):
    from hs_arena._fp import init_engine
    from hs_arena._vendor.fireplace import actions

    init_engine()
    real = actions.Play.do
    calls = {"n": 0}

    def flaky(self, source, card, *args, **kw):
        calls["n"] += 1
        if calls["n"] == 3:
            raise RuntimeError(f"injected failure while playing {card.id}")
        return real(self, source, card, *args, **kw)

    monkeypatch.setattr(actions.Play, "do", flaky)
    from hs_arena.cli import main

    out_dir = tmp_path / "games"
    assert main(["play", "--p1", "greedy", "--p2", "greedy", "--games", "1", "--parallel", "1", "--seed", "4", "--out", str(out_dir)]) == 0
    printed = capsys.readouterr().out
    gd = next(out_dir.iterdir())
    r = load_json(gd / "result.json")
    assert r["reason"] == "void_engine_error" and r["winner"] is None
    card_ids = r["engine_error"]["card_ids"]
    assert card_ids and all(isinstance(c, str) for c in card_ids)
    log = (gd / "engine_errors.log").read_text(encoding="utf-8")
    assert "injected failure" in log and card_ids[0] in log and "Traceback" in log
    assert "voided 1" in printed and card_ids[0] in printed
    events = read_jsonl(gd / "replay.jsonl")
    assert events[-1] == {"event": "game_over", "winner": None, "reason": "void_engine_error"}
