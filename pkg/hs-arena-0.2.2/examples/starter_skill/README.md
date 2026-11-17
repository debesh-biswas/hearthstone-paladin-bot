Starter skill: copy this directory to start your own (e.g. `my_skill/`).

- `SKILL.md`: frontmatter (`name`, `description`, `model: haiku` or `model: luna`) and the playbook.
- `deck.json`: an optional recipe (this example uses the greedy bot's Mage deck). The agent must submit its
  actual class and 30 card ids through MCP during deck_submission; the host never reads this file.
- `references/decklist.md`: a knowledge file the agent reads when the playbook says so.
- Add `scripts/` for code the agent can run, and `requirements.txt` for extra Python packages.

Check it with `hs-arena validate my_skill`, then play `hs-arena play --p1 skill:my_skill --p2 greedy`.
Files named README.md are never shown to the agent.

For a dynamic or random deck, replace the deck-building section of SKILL.md with your policy or a script.
The allowed catalog is in game/card_pool.json. Once accepted, your submitted deck is locked for that game.
