"""Deck building belongs to agents; the engine starts only after two locked valid decks."""
import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor

import pytest

from conftest import assert_valid
from hs_arena.agents.base import Decision, Player
from hs_arena.deck import random_deck
from hs_arena.protocol import Config
from hs_arena.runner import play_game, run_game
from hs_arena.sdk import Action, State
from test_skill import _Mcp


class BuildingSeat(Player):
    kind = "mcp"
    requires_deck_submission = True

    def __init__(self, seed, barrier=None):
        super().__init__(f"builder-{seed}")
        self.recipe = random_deck(random.Random(seed))
        self.barrier = barrier
        self.states = []
        self.final = None

    def decide(self, state):
        self.states.append(state)
        if state["phase"] == "deck_submission":
            if self.barrier:
                self.barrier.wait(timeout=5)  # catches sequential setup requests
            return Decision("action", Action.submit_deck(self.recipe.hero_class, self.recipe.cards))
        if state["phase"] == "mulligan":
            return Decision("action", Action.mulligan())
        return Decision("action", Action.end_turn())

    def game_over(self, state):
        self.final = state


def test_simultaneous_builders_lock_decks_before_engine(tmp_path, monkeypatch, validators):
    import hs_arena.runner as runner
    actual = runner.Engine
    barrier = threading.Barrier(2)
    players = {1: BuildingSeat(7, barrier), 2: BuildingSeat(8, barrier)}
    calls = []

    def engine(*args, **kw):
        assert all(p.deck.to_json() == p.recipe.to_json() for p in players.values())
        calls.append(args)
        return actual(*args, **kw)

    monkeypatch.setattr(runner, "Engine", engine)
    result = play_game(players, game_dir=tmp_path / "g", game_id="g", seed=0, config=Config(max_turns=2))
    assert len(calls) == 1 and result["reason"] == "max_turns"
    for p in players.values():
        assert [s["phase"] for s in p.states[:2]] == ["deck_submission", "mulligan"]
        assert [s["seq"] for s in p.states[:2]] == [1, 2]
        setup = p.states[0]
        assert setup["you"] is None and setup["opponent"] is None and setup["events"] == []
        assert "first_player" not in setup and "seed" not in setup
        assert State(setup).entity(1) is None
        assert "DECK SUBMISSION" in State(setup).to_text()
        for s in p.states + [p.final]:
            assert_valid(validators["state"], s)
    game = json.loads((tmp_path / "g/game.json").read_text())
    assert [p["deck"] for p in game["players"]] == [list(players[i].recipe.cards) for i in (1, 2)]
    assert_valid(validators["game"], game)
    assert_valid(validators["result"], result)


def test_invalid_deck_retried_and_resubmission_during_play_rejected(tmp_path, validators):
    class RetrySeat(BuildingSeat):
        def decide(self, state):
            if state["phase"] == "deck_submission" and not self.states:
                self.states.append(state)
                return Decision("action", Action.submit_deck(self.recipe.hero_class, self.recipe.cards[:-1]))
            if state["phase"] == "main" and not any(s["phase"] == "main" for s in self.states):
                self.states.append(state)
                other = random_deck(random.Random(99))
                return Decision("action", Action.submit_deck(other.hero_class, other.cards))
            return super().decide(state)

    p = RetrySeat(7)
    players = {1: p, 2: BuildingSeat(8)}
    result = play_game(players, game_dir=tmp_path / "g", game_id="g", seed=0, config=Config(max_turns=3))
    assert result["illegal_counts"]["1"] == 2
    errors = [s["last_action_result"]["error"] for s in p.states if s["last_action_result"]]
    assert errors == ["INVALID_DECK", "WRONG_PHASE"]
    assert p.deck.to_json() == p.recipe.to_json()
    assert [s["seq"] for s in p.states] == list(range(1, len(p.states) + 1))
    for s in p.states:
        assert_valid(validators["state"], s)


@pytest.mark.parametrize("failure", ["invalid", "timeout", "forfeit", "concede"])
def test_setup_failure_finishes_both_seats_without_engine(tmp_path, monkeypatch, validators, failure):
    import hs_arena.runner as runner
    both_requested = threading.Barrier(2)

    class FailingSeat(BuildingSeat):
        def decide(self, state):
            self.states.append(state)
            both_requested.wait(timeout=5)
            if failure == "invalid":
                return Decision("action", Action.submit_deck("MAGE", []))
            if failure == "concede":
                return Decision("action", Action.concede())
            return Decision(failure)

    class WaitingSeat(BuildingSeat):
        def decide(self, state):
            self.states.append(state)
            both_requested.wait(timeout=5)
            assert self._decision_cancelled.wait(timeout=5)
            return Decision("cancelled")

    def no_engine(*args, **kwargs):
        pytest.fail("engine must not exist before both decks are valid")

    monkeypatch.setattr(runner, "Engine", no_engine)
    players = {1: FailingSeat(7), 2: WaitingSeat(8)}
    result = play_game(players, game_dir=tmp_path / "g", game_id="g", seed=0, config=Config(illegal_limit=0))
    assert result["winner"] == 2 and result["first_player"] is None and result["turns"] == 0
    assert result["reason"] == {"forfeit": "forfeit_exit", "timeout": "forfeit_timeout", "concede": "concede"}.get(failure, "forfeit_illegal")
    assert result["timeouts"]["1"] == (1 if failure == "timeout" else 0)
    for p in players.values():
        assert p.final["phase"] == "game_over" and p.final["you"] is None
        assert "ended before" in State(p.final).to_text()
        assert_valid(validators["state"], p.final)
    assert_valid(validators["result"], result)
    assert_valid(validators["game"], json.loads((tmp_path / "g/game.json").read_text()))


def test_same_engine_seed_allows_different_agent_built_decks(tmp_path):
    decks = []
    for n in (1, 2):
        players = {1: BuildingSeat(n), 2: BuildingSeat(n + 10)}
        play_game(players, game_dir=tmp_path / str(n), game_id=str(n), seed=0, config=Config(max_turns=1))
        decks.append(players[1].deck)
    assert decks[0] != decks[1]


def test_external_agents_use_only_mcp_and_need_no_skill_or_deck_files(tmp_path, validators):
    """Two real stdio MCP clients connect to a host that launches/parses no student agent."""
    work = {i: tmp_path / f"agent{i}" for i in (1, 2)}
    clients = {}
    for i in (1, 2):
        box = work[i] / "arena-mailbox"
        box.mkdir(parents=True)
        clients[i] = _Mcp(box)
        clients[i].req("initialize")
        clients[i].req("tools/list")  # server/tool traffic may arrive before the host
        assert clients[i].call("wait").startswith("No decision")

    def agent(i):
        from hs_arena.agents.greedy_bot import GreedyBot
        deck = random_deck(random.Random(20 + i))
        bot = GreedyBot("external", deck)
        reply = clients[i].call("wait")
        while not reply.startswith("GAME OVER"):
            if not reply.startswith("YOUR DECISION") and "YOUR DECISION" not in reply:
                reply = clients[i].call("wait")
                continue
            state = json.loads((work[i] / "game/state.json").read_text(encoding="utf-8"))
            if state["phase"] == "deck_submission":
                catalog = json.loads((work[i] / "game/card_pool.json").read_text(encoding="utf-8"))
                assert set(deck.cards) <= set(catalog)
                action = Action.submit_deck(deck.hero_class, deck.cards)
            else:
                action = bot.decide(state).action
            reply = clients[i].call("act", seq=state["seq"], action=action)
        return deck

    try:
        with ThreadPoolExecutor(max_workers=3) as pool:
            host = pool.submit(run_game, f"mcp:{work[1]}", f"mcp:{work[2]}", game_dir=tmp_path / "g",
                               game_id="g", seed=0, config=Config(max_turns=3, decision_timeout_s=10))
            agents = {i: pool.submit(agent, i) for i in (1, 2)}
            result = host.result(timeout=30)
            decks = {i: f.result(timeout=10) for i, f in agents.items()}
        assert result["reason"] == "max_turns" and result["illegal_counts"] == {"1": 0, "2": 0}
        game = json.loads((tmp_path / "g/game.json").read_text())
        for i in (1, 2):
            assert not (work[i] / "SKILL.md").exists() and not (work[i] / "deck.json").exists()
            assert game["players"][i - 1]["deck"] == list(decks[i].cards)
            for path in (tmp_path / f"g/p{i}/decisions").glob("*.state.json"):
                assert_valid(validators["state"], json.loads(path.read_text(encoding="utf-8")))
        for line in (tmp_path / "g/replay.jsonl").read_text().splitlines():
            assert_valid(validators["event"], json.loads(line))
        assert_valid(validators["result"], result)
    finally:
        for client in clients.values():
            client.close()
