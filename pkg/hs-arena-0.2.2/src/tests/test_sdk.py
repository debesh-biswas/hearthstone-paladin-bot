"""C2 to_text snapshot, C3 Action constructors, C4 no network code in the SDK, C5 example agent memory."""

import json
import os
import re
from pathlib import Path

from conftest import ROOT, assert_valid, fast_config, load_json
from hs_arena.runner import run_game
from hs_arena.sdk import Action, State, View

DATA = Path(__file__).parent / "data"


def test_to_text_snapshot_and_determinism():
    state = json.loads((DATA / "state_sample.json").read_text(encoding="utf-8"))
    text = State(state).to_text()
    if os.environ.get("UPDATE_SNAPSHOTS"):
        (DATA / "state_sample.txt").write_text(text + "\n", encoding="utf-8", newline="\n")
    expected = (DATA / "state_sample.txt").read_text(encoding="utf-8").rstrip("\n")
    assert text == expected
    assert State(json.loads(json.dumps(state))).to_text() == text  # deterministic
    # coverage of the rendering
    for needle in (
        "OPPONENT:", "YOU:", "health", "mana 7/7", "hand:", "board:", "secrets: #90 Counterspell", "LEGAL ACTIONS:",
        "EVENTS since your previous state:", "deadline_epoch_s 1761955200.0", "REJECTED: ILLEGAL_TARGET", "end_turn",
        "hero power: Fireblast", "mana crystals 7 | hand 4",
    ):
        assert needle in text, needle


def test_to_text_silenced_minion_keeps_original_text_for_reference():
    state = json.loads((DATA / "state_sample.json").read_text(encoding="utf-8"))
    m = state["you"]["board"][0]
    assert m["text"] and not m["silenced"]
    m["silenced"] = True
    line = next(x for x in State(state).to_text().splitlines() if f"#{m['entity_id']} {m['name']}" in x)
    assert "[silenced" in line or ", silenced" in line, line
    assert line.endswith(f" - silenced; original text (no longer active): {m['text']}"), line


def test_to_text_game_over_has_no_decision_deadline():
    state = json.loads((DATA / "state_sample.json").read_text(encoding="utf-8"))
    state.update(phase="game_over", legal_actions=[], last_action_result=None, timeout_s=10)
    for you_won, outcome in ((True, "you won"), (False, "you lost"), (None, "no winner")):
        winner = {True: 1, False: 2, None: None}[you_won]
        state["result"] = {"winner": winner, "you_won": you_won, "reason": "hero_death" if winner else "draw"}
        text = State(state).to_text()
        assert "The game is over; no action is expected." in text
        assert "Answer within" not in text and "deadline_epoch_s" not in text  # the exit grace is not a decision deadline
        assert f"RESULT: winner {winner} ({outcome})" in text


def test_state_typed_access():
    state = State(json.loads((DATA / "state_sample.json").read_text(encoding="utf-8")))
    assert state.you.hero.health == state["you"]["hero"]["health"]
    assert isinstance(state.you.hand[0], View) and state.you.hand[0].name
    assert state.legal("end_turn") == [{"type": "end_turn"}]
    eid = state.you.board[0].entity_id
    assert state.entity(eid).name == state.you.board[0].name
    assert state.seconds_left() < 0  # the sample's deadline is in the past
    assert json.loads(json.dumps(state)) == json.loads((DATA / "state_sample.json").read_text(encoding="utf-8"))


def test_action_constructors_are_schema_valid(validators):
    hand_card = {"entity_id": 88, "name": "Fireball"}
    actions = [
        Action.play_card(88, target=130),
        Action.play_card(hand_card, target={"entity_id": 64}),
        Action.play_card(92, position=1),
        Action.play_card(95, choose=201, target=130),
        Action.attack(71, 130),
        Action.hero_power(target=64),
        Action.hero_power(),
        Action.end_turn(),
        Action.concede(),
        Action.mulligan([88, 95]),
        Action.mulligan(),
        Action.choose([301]),
        Action.choose(301),
    ]
    assert actions[1] == {"type": "play_card", "card": 88, "target": 64}
    assert actions[12] == {"type": "choose", "options": [301]}
    seen_types = set()
    for a in actions:
        assert_valid(validators["action"], {"seq": 1, "action": a.to_dict()}, a)
        json.dumps(a)
        seen_types.add(a["type"])
    assert seen_types == {"play_card", "attack", "hero_power", "end_turn", "concede", "mulligan", "choose"}


NETWORK_IMPORT = re.compile(
    r"^\s*(import|from)\s+(http|urllib|urllib3|requests|socket|openai|httpx|aiohttp|asyncio|ssl|ftplib|smtplib)\b",
    re.M,
)


def test_sdk_has_no_network_code():
    sdk = ROOT / "hs_arena" / "sdk"
    files = list(sdk.rglob("*.py"))
    assert files
    for f in files:
        src = f.read_text(encoding="utf-8")
        assert not NETWORK_IMPORT.search(src), f"network import in {f}"
        assert "__import__(" not in src and "import_module(" not in src, f"dynamic import in {f}"


def test_example_agent_reports_decision_counter(example_copy, tmp_path):
    gd = tmp_path / "g"
    r = run_game(str(example_copy), "greedy", game_dir=gd, game_id="g", seed=21, config=fast_config())
    log = (gd / "p1" / "stderr.log").read_text(encoding="utf-8")
    m = re.search(r"after (\d+) decisions", log)
    assert m, log
    assert int(m.group(1)) == r["decisions"]["1"] > 0
    assert "I am player 1 playing MAGE" in log
    final = load_json(gd / "p1" / "state.json")
    assert final["phase"] == "game_over"


def test_to_text_marks_lost_divine_shield_and_stealth():
    state = json.loads((DATA / "state_sample.json").read_text(encoding="utf-8"))
    board = state["you"]["board"]
    squire = dict(board[0], entity_id=901, card_id="EX1_008", name="Argent Squire", text="Divine Shield",
                  divine_shield=False, silenced=False)
    worgen = dict(board[0], entity_id=902, card_id="EX1_010", name="Worgen Infiltrator", text="Stealth",
                  stealth=True, silenced=False)
    knight = dict(board[0], entity_id=903, card_id="EX1_590", name="Blood Knight",
                  text="Battlecry: All minions lose Divine Shield. Gain +3/+3 for each Shield lost.", silenced=False)
    board += [squire, worgen, knight]
    lines = {m["entity_id"]: next(x for x in State(state).to_text().splitlines() if f"#{m['entity_id']} " in x)
             for m in (squire, worgen, knight)}
    assert lines[901].endswith(" - Divine Shield (Divine Shield already lost)"), lines[901]
    assert lines[902].endswith(" - Stealth"), lines[902]  # still stealthed
    assert "already lost" not in lines[903]  # mentions Divine Shield but never had one


def test_card_text_drops_alternate_text_after_at_sign():
    from hs_arena.cards import plain_text

    raw = "<b>Hero Power</b>\nDeal $2 damage to the enemy hero.@<b>Hero Power</b>\nDeal $2 damage."
    assert plain_text(raw) == "Hero Power Deal 2 damage to the enemy hero."
