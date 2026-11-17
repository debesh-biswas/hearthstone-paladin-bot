Example MCP client: the course's Mage greedy bot playing through the seat's game MCP server.

`client.py` does what Claude Code or Codex do when they play a skill, without a model: it starts the seat's MCP
server (the command is in the environment variable `HS_ARENA_MCP`), calls `wait`, reads `game/state.json`,
decides with the greedy bot, calls `act`, and repeats until GAME OVER.

Its first action is submit_deck: the client itself reads the optional deck.json recipe and sends its class
and card list through MCP. The host does not load the recipe. Replace this step to build dynamically or
randomly; no deck.json file is required by the client seat runtime.

Try it (no model, no login needed): `hs-arena play --p1 client:examples/greedy_mcp_client --p2 random --games 3`.
It plays exactly like `--p2 greedy`; that built-in version just skips the MCP round trip.
