# random_agent — example submission

A complete, valid submission that demonstrates the protocol: `manifest.json`, `deck.json` (the greedy bot's
Mage deck) and `agent.py`, which picks uniformly among the legal actions using the `hs_arena.sdk` polling loop.
It keeps a per-game decision counter in instance state and reports it on stderr when the game ends.

It contains **no LLM code**; your own agent must have an LLM core.

- Tested with Python 3.10+ (the runtime starts it with the same interpreter that runs `hs-arena`).
- Run: `hs-arena play --p1 examples/random_agent --p2 greedy --games 5 --out ./games`
