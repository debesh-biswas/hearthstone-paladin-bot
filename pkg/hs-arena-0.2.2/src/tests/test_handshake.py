"""B2: seq handshake edge cases and atomic file exchange."""

import json
import os
import threading
import time

from conftest import fast_config, make_submission, read_jsonl
from hs_arena._fileio import atomic_write_json, read_text
from hs_arena.runner import run_game

STALE_FIRST = """
from hs_arena._fileio import atomic_write_json
class Stale(Agent):
    def __init__(self):
        self.rng = random.Random(3)
    def decide(self, state):
        # an answer to an older state first: must be dropped without penalty
        atomic_write_json(os.environ["HS_ACTION_FILE"], {"seq": state.seq - 1, "action": {"type": "concede"}})
        time.sleep(0.15)
        return random_action(state, self.rng)
run(Stale)
"""


def test_stale_seq_is_dropped_silently(tmp_path):
    sub = make_submission(tmp_path, STALE_FIRST)
    r = run_game(str(sub), "random", game_dir=tmp_path / "g", game_id="g", seed=11, config=fast_config())
    assert r["reason"] in ("hero_death", "draw")
    assert r["illegal_counts"]["1"] == 0


AHEAD = """
from hs_arena._fileio import atomic_write_json
class Ahead(Agent):
    def __init__(self):
        self.rng = random.Random(3)
        self.done = False
    def decide(self, state):
        if not self.done:
            self.done = True
            atomic_write_json(os.environ["HS_ACTION_FILE"], {"seq": state.seq + 5, "action": {"type": "end_turn"}})
            time.sleep(1.0)  # the runtime re-issues the decision meanwhile; our answer below is then stale
        return random_action(state, self.rng)
run(Ahead)
"""


def test_seq_ahead_is_seq_mismatch(tmp_path):
    sub = make_submission(tmp_path, AHEAD)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=12, config=fast_config())
    ill = [e for e in read_jsonl(gd / "replay.jsonl") if e["event"] == "illegal_action"]
    assert [(e["player"], e["error"]) for e in ill] == [(1, "SEQ_MISMATCH")]
    assert r["illegal_counts"]["1"] == 1


BAD_JSON_ONCE = """
class BadOnce(Agent):
    def __init__(self):
        self.rng = random.Random(5)
        self.done = False
    def decide(self, state):
        if not self.done:
            self.done = True
            with open(os.environ["HS_ACTION_FILE"], "w") as f:
                f.write("{this is not json")
            time.sleep(2.0)  # stays unparseable > 1 s: BAD_JSON; our late answer below is dropped
        return random_action(state, self.rng)
run(BadOnce)
"""


def test_bad_json_counts_once(tmp_path):
    sub = make_submission(tmp_path, BAD_JSON_ONCE)
    gd = tmp_path / "g"
    r = run_game(str(sub), "random", game_dir=gd, game_id="g", seed=13, config=fast_config())
    ill = [e for e in read_jsonl(gd / "replay.jsonl") if e["event"] == "illegal_action"]
    assert [e["error"] for e in ill] == ["BAD_JSON"]
    assert r["illegal_counts"]["1"] == 1


SLOW_WRITER = """
class SlowWriter(Agent):
    '''Writes action.json non-atomically, in two parts with a pause in between.'''
    def __init__(self):
        self.rng = random.Random(6)
    def decide(self, state):
        a = random_action(state, self.rng)
        text = json.dumps({"seq": state.seq, "action": dict(a)})
        with open(os.environ["HS_ACTION_FILE"], "w") as f:
            f.write(text[: len(text) // 2]); f.flush()
            time.sleep(0.3)
            f.write(text[len(text) // 2 :])
        # tell the SDK loop not to write again: wait for the next state ourselves
        raise _Handled()
class _Handled(Exception):
    pass

def main():
    agent = SlowWriter()
    from hs_arena.sdk import State
    path = os.environ["HS_STATE_FILE"]; last = 0
    while True:
        try:
            data = json.load(open(path, encoding="utf-8"))
        except (OSError, ValueError):
            time.sleep(0.02); continue
        if data["seq"] <= last:
            time.sleep(0.02); continue
        last = data["seq"]
        if data["phase"] == "game_over":
            return
        try:
            agent.decide(State(data))
        except _Handled:
            pass
main()
"""


def test_slow_non_atomic_writer_is_accepted(tmp_path):
    sub = make_submission(tmp_path, SLOW_WRITER)
    r = run_game(str(sub), "random", game_dir=tmp_path / "g", game_id="g", seed=14, config=fast_config())
    assert r["reason"] in ("hero_death", "draw")
    assert r["illegal_counts"]["1"] == 0


def test_sdk_waits_for_missing_state_file(tmp_path, monkeypatch):
    from hs_arena.sdk import Action, Agent, run

    state_file = tmp_path / "state.json"
    action_file = tmp_path / "action.json"
    monkeypatch.setenv("HS_STATE_FILE", str(state_file))
    monkeypatch.setenv("HS_ACTION_FILE", str(action_file))
    monkeypatch.setenv("HS_WORK_DIR", str(tmp_path))
    seen = []

    class A(Agent):
        def on_game_start(self, info):
            seen.append(("start", info.player))

        def decide(self, state):
            seen.append(("decide", state.seq))
            return Action.end_turn()

        def on_game_over(self, result):
            seen.append(("over", result.reason))

    base = json.loads((__import__("pathlib").Path(__file__).parent / "data" / "state_sample.json").read_text(encoding="utf-8"))

    def feeder():
        time.sleep(0.3)  # the SDK starts before state.json exists
        atomic_write_json(state_file, dict(base, seq=1))
        deadline = time.time() + 10
        while time.time() < deadline and not action_file.exists():
            time.sleep(0.01)
        ans = json.loads(read_text(action_file))
        assert ans == {"seq": 1, "action": {"type": "end_turn"}}
        atomic_write_json(state_file, dict(base, seq=1))  # same seq again: ignored
        time.sleep(0.2)
        over = dict(base, seq=2, phase="game_over", legal_actions=[],
                    result={"winner": 1, "you_won": True, "reason": "hero_death"})
        atomic_write_json(state_file, over)

    t = threading.Thread(target=feeder)
    t.start()
    assert run(A, poll_interval=0.01) == 0
    t.join()
    assert seen == [("start", base["player"]), ("decide", 1), ("over", "hero_death")]


def test_readers_never_observe_partial_files(tmp_path):
    path = tmp_path / "state.json"
    big = {"payload": "x" * 200_000}
    atomic_write_json(path, dict(big, n=0))
    errors = []
    stop = threading.Event()

    def writer():
        for n in range(1, 400):
            atomic_write_json(path, dict(big, n=n))
        stop.set()

    def reader():
        while not stop.is_set():
            text = read_text(path)
            try:
                obj = json.loads(text)
                assert len(obj["payload"]) == 200_000
            except Exception as e:  # pragma: no cover - failure path
                errors.append(repr(e))

    threads = [threading.Thread(target=writer)] + [threading.Thread(target=reader) for _ in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert not errors, errors[:3]
    assert not os.path.exists(str(path) + ".tmp")
