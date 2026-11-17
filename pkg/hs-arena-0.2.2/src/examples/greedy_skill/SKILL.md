---
name: greedy-mage
description: Example skill. The course's rule-based greedy bot decides every move in a script; the agent relays it.
model: haiku
---

# Greedy Mage (example skill)

A fixed policy in `scripts/greedy_move.py` decides every move. Your job is to relay its answer exactly.
The first decision is deck_submission: the same script reads this example's deck.json recipe and prints a
submit_deck action. Relay it just like a move. The host does not load that file for you.

For every decision:

1. Call `wait` (after the first decision, the reply of your previous `act` already shows the next decision).
   If it says GAME OVER, stop: the game is finished.
2. If it shows `YOUR DECISION (seq N)`, run this command in your folder:

       python scripts/greedy_move.py

   It reads `game/state.json` and prints one line of JSON: `{"seq": N, "action": {...}}`.
3. Call `act` with exactly that `seq` and `action`. Do not change the action and do not add fields.
4. Go back to step 1.

If the script fails or prints something else, pick a legal action yourself from the LEGAL ACTIONS list
(`end_turn` is always legal during your turn) and keep playing. Never stop before GAME OVER.
