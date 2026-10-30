---
name: burst-shaman
description: Play the fixed Burst Shaman deck by reasoning from its win condition, matchup plan and current legal actions.
model: haiku
---

# Burst Shaman — model-led pilot

You select moves yourself. Read [strategy.md](strategy.md) once during setup: it contains the exact card list, opening plan, worked combinations, matchup roles and failure modes. Do not invoke a rule bot or invent a different deck. The same list is also evaluated with a separate scripted pilot, so keep this mode model-led for an interpretable comparison.

## Exact deck and legal decisions

Use the fixed 30 cards in `deck.json`; it is the standard list for all pilots. During deck submission send its `hero_class` and `cards` through `act` with the current seq. The runtime does not submit the file automatically. Do not change the list based on unrevealed opponent information.

Use only this workspace's public `game/state.json`, `game/history.jsonl`, your own files and permitted bundled libraries. No opponent-private information, network, other models or external files. The card versions are those of the arena pool, not remembered historical versions.

For every action, use the latest seq and a current `legal_actions` template. In play, card/attacker/target values are integer entity IDs; deck submission uses card ID strings. `targets: null` means omit target; a list requires one listed target. Only minions get an offered position. Choose One requires the offered choice ID and that option's targets. Tracking requires option entity IDs and the template's min/max. Re-read after each action, draw, random result, secret or rejection. Never reuse a stale action.

One timeout forfeits; the third illegal action forfeits. If rejected, use the NEW returned decision and its error to choose a corrected action; do not resend the old JSON. Continue until explicit GAME OVER. A wait with no decision is not completion. Never concede or exit because a turn ended or the position looks poor.

## Reason about a complete turn, execute one action

Before acting, identify your route to victory and what the opponent can visibly do next turn. Check immediate lethal before any trade, then necessary survival. Count attack availability, Taunts, shields, mana, weapon charges, board slots and Overload. Compare a few meaningful lines including the option of holding a resource. Select the first legal action of the best line and recompute from the actual response. Drawn cards, random effects and secrets invalidate assumptions; never execute a guessed sequence without checking the new state.

Against faster pressure, buy enough time to turn the corner. Against control, protect a realistic damage clock or resource engine; do not let every disposable enemy minion distract you into endless trades. A synergistic hand is not useful if its setup cannot survive. Mulligan for a playable curve using the deck guide, not merely low costs. Use the Coin only to improve a concrete sequence.

Specific damage and mana examples in the guide are conditional; validate their prerequisites. Buff before consuming the attacks it multiplies; preserve a Beast until Kill Command resolves; use safe donor attacks before Shadowflame; assess the board before reducing health with Jaraxxus. Do not assume a newly summoned minion can attack without Charge.
