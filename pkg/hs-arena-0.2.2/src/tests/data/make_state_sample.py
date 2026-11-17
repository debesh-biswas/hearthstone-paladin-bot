"""Regenerate tests/data/state_sample.json (+ .txt snapshot): a real greedy-mirror state with an injected
secret and a rejected last action. Run from the hs-arena directory: python tests/data/make_state_sample.py"""

import json
from pathlib import Path

from hs_arena._resources import GREEDY_DECK
from hs_arena.agents import GreedyBot
from hs_arena.deck import load_deck
from hs_arena.engine import Engine
from hs_arena.protocol import Config
from hs_arena.runner import build_state
from hs_arena.sdk import State

HERE = Path(__file__).resolve().parent


def main():
    deck = load_deck(GREEDY_DECK)
    engine = Engine(deck, deck, 77)
    bots = {1: GreedyBot("greedy", deck), 2: GreedyBot("greedy", deck)}
    seq = {1: 0, 2: 0}
    while not engine.over:
        i, phase = engine.pending()
        seq[i] += 1
        st = build_state(engine, "g_20261101_000017", i, seq[i], None, Config())
        if (phase == "main" and i == 1 and engine.turn >= 9 and len(st["you"]["board"]) >= 2
                and len(st["opponent"]["board"]) >= 2 and len(st["you"]["hand"]) >= 3):
            break
        engine.step(i, bots[i].decide(st).action)
    st["deadline_epoch_s"] = 1761955200.0
    st["you"]["secrets"] = [{"entity_id": 90, "card_id": "EX1_287", "name": "Counterspell"}]
    st["opponent"]["secrets_count"] = 1
    st["last_action_result"] = {
        "accepted": False, "error": "ILLEGAL_TARGET",
        "message": "target 999 is not a valid target for card 24 (Fireball); one of [4, 7, 9, 22, 37, 64, 65]",
        "illegal_count": 2, "illegal_limit": 3,
    }
    (HERE / "state_sample.json").write_text(json.dumps(st, indent=1) + "\n", encoding="utf-8", newline="\n")
    (HERE / "state_sample.txt").write_text(State(st).to_text() + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
