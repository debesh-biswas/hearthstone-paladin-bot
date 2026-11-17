Example skill: the course's Mage greedy bot as a skill ("script decides, model relays").

- `SKILL.md`: the playbook the course agent follows; `model: haiku` (use `luna` to have GPT-6-Luna play it).
- `deck.json`: the greedy bot's Mage deck.
- `scripts/greedy_move.py`: reads `game/state.json`, prints the greedy bot's action, logs it to `scratch/moves.log`.

Try it: `hs-arena play --p1 skill:examples/greedy_skill --p2 greedy --games 1`.
This README is a note for people; files named README.md are never shown to the agent.
