"""Lecture 5 thresholds across phases, with no model account required."""
import json

import pytest

from hs_arena.agents.base import Decision
from hs_arena.protocol import Config
from hs_arena.runner import play_game
from test_deck_submission import BuildingSeat
from conftest import assert_valid


@pytest.mark.parametrize("phase", ["deck_submission", "mulligan", "main"])
@pytest.mark.parametrize("failure,reason,count", [
    ("invalid", "forfeit_illegal", 3),
    ("timeout", "forfeit_timeout", 1),
    ("exited", "forfeit_exit", 1),
])
def test_first_terminal_failure_or_third_illegal_in_every_phase(tmp_path, validators, phase, failure, reason, count):
    class FailingSeat(BuildingSeat):
        faults = 0

        def decide(self, state):
            if state["phase"] == phase:
                self.states.append(state)
                self.faults += 1
                return Decision("action", {"type": "not_an_action"}) if failure == "invalid" else Decision(failure)
            return super().decide(state)

    bad = FailingSeat(7)
    result = play_game({1: bad, 2: BuildingSeat(8)}, game_dir=tmp_path / "game", game_id="game", seed=0, config=Config())
    assert result["winner"] == 2 and result["reason"] == reason
    assert bad.faults == count
    assert result["illegal_counts"]["1"] == (3 if failure == "invalid" else 0)
    assert result["timeouts"]["1"] == (1 if failure == "timeout" else 0)
    assert result["restarts"] == {"1": 0, "2": 0}
    assert_valid(validators["result"], result)
    for seat in (bad,):
        assert_valid(validators["state"], seat.final)
    for line in (tmp_path / "game/replay.jsonl").read_text().splitlines():
        assert_valid(validators["event"], json.loads(line))


def test_illegal_count_carries_across_deck_mulligan_and_main(tmp_path):
    class AcrossPhases(BuildingSeat):
        failed = set()

        def decide(self, state):
            if state["phase"] not in self.failed:
                self.failed.add(state["phase"])
                return Decision("action", {"type": "not_an_action"})
            return super().decide(state)

    bad = AcrossPhases(7)
    result = play_game({1: bad, 2: BuildingSeat(8)}, game_dir=tmp_path / "game", game_id="game", seed=0, config=Config())
    assert bad.failed == {"deck_submission", "mulligan", "main"}
    assert result["illegal_counts"]["1"] == 3 and result["reason"] == "forfeit_illegal"


def test_exit_is_detected_while_opponent_is_deciding(tmp_path):
    class ExitSeat(BuildingSeat):
        stopped = False

        def poll_exit(self):
            return Decision("exited") if self.stopped else None

    bad = ExitSeat(7)

    class Opponent(BuildingSeat):
        def decide(self, state):
            if state["phase"] == "main":
                bad.stopped = True
            return super().decide(state)

    result = play_game({1: bad, 2: Opponent(8)}, game_dir=tmp_path / "game", game_id="game", seed=0, config=Config())
    assert result["reason"] == "forfeit_exit" and result["winner"] == 2
