"""Print the greedy bot's action for the pending decision.

Reads game/state.json (written by the skill seat before every decision) and prints one line of JSON:
    {"seq": 12, "action": {"type": "attack", "attacker": 22, "target": 37}}
It also appends the move to scratch/moves.log, to show how a skill keeps notes during a game.

To try it by hand, pass any recorded state:  python scripts/greedy_move.py games/<id>/p1/decisions/00012.state.json
"""

import json
import sys
from pathlib import Path

from hs_arena.agents.greedy_bot import GreedyBot
from hs_arena.deck import load_deck

state_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("game/state.json")
state = json.loads(state_path.read_text(encoding="utf-8"))
if state["phase"] == "game_over":
    print(json.dumps({"seq": state["seq"], "game_over": True, "result": state["result"]}))
else:
    deck = load_deck("deck.json")
    if state["phase"] == "deck_submission":
        action = {"type": "submit_deck", "hero_class": deck.hero_class, "cards": list(deck.cards)}
    else:
        action = GreedyBot("greedy", deck).decide(state).action
    if Path("scratch").is_dir():
        with open(Path("scratch") / "moves.log", "a", encoding="utf-8") as f:
            f.write(f"turn {state['turn']} seq {state['seq']}: {json.dumps(action)}\n")
    print(json.dumps({"seq": state["seq"], "action": action}))
