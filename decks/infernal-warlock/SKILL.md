---
name: infernal-warlock
description: Play the fixed Infernal Warlock deck using its deterministic legal-action pilot, with a concept-led strategy fallback.
model: haiku
---

# Infernal Warlock — scripted pilot

Win a full game with the strategy in [strategy.md](strategy.md). Read it once at setup to understand the win condition, resources, matchup shifts and dangerous sequences. This is an untested research candidate.

## Decision loop

1. Call `wait`. On each YOUR DECISION, run `python scripts/move.py` from the skill root. Use the environment-provided Python fallback if `hs_arena` is not importable; do not install dependencies.
2. The script prints one JSON object with `seq` and `action`. Relay those exact fields to `act`. Diagnostic messages go to stderr. The script handles deck submission, mulligan, choices and turns.
3. After `act`, the response may already contain the next decision. Run the script again for that current state; do not replay its previous output. If no decision is ready, call `wait`.
4. On explicit GAME OVER, stop. A script output with `game_over: true` also indicates completion; do not send an action for it.

Default mode is script relay. Do not silently switch between scripted and model-selected moves during a comparison. If execution fails, retry once using the provided runtime interpreter. If it still fails, choose a legal action yourself using the strategy below; do not spend the decision budget debugging. A fresh `end_turn` template is a legal main-phase last resort, not a response for mulligan or choice. Do not let a shell failure terminate the game session.

The script searches supported immediate face-damage combinations, then scores legal actions using class-specific rules. It is not a complete simulator. It knows neither hidden secrets nor future draws. Instructions do not convert heuristic decisions into guaranteed optimal play.

## Exact deck and legal decisions

Use the fixed 30 cards in `deck.json`; it is the standard list for all pilots. During deck submission send its `hero_class` and `cards` through `act` with the current seq. The runtime does not submit the file automatically. Do not change the list based on unrevealed opponent information.

Use only this workspace's public `game/state.json`, `game/history.jsonl`, your own files and permitted bundled libraries. No opponent-private information, network, other models or external files. The card versions are those of the arena pool, not remembered historical versions.

For every action, use the latest seq and a current `legal_actions` template. In play, card/attacker/target values are integer entity IDs; deck submission uses card ID strings. `targets: null` means omit target; a list requires one listed target. Only minions get an offered position. Choose One requires the offered choice ID and that option's targets. Tracking requires option entity IDs and the template's min/max. Re-read after each action, draw, random result, secret or rejection. Never reuse a stale action.

One timeout forfeits; the third illegal action forfeits. If rejected, use the NEW returned decision and its error to choose a corrected action; do not resend the old JSON. Continue until explicit GAME OVER. A wait with no decision is not completion. Never concede or exit because a turn ended or the position looks poor.

## Manual fallback thinking

Read [strategy.md](strategy.md) for the full card list and deck-specific plan. First count immediate lethal using mana, actual attack availability, Taunts, shields, weapon durability and known effects. Then assess survival. Compare a pressure line, a stabilization line and a resource-development line as appropriate. Execute one legal action and reassess. Do not keep clearing harmless bodies after a face-damage clock wins; do not race when the visible counterattack kills you first.
