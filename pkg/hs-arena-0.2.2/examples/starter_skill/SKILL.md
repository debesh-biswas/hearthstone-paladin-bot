---
name: starter-mage
description: Starter template. A short playbook for the Mage deck; the model makes every decision itself.
model: haiku
---

# Starter Mage playbook

## Build your deck first

Your first decision is `deck_submission`. Read `deck.json` as this example's suggested tempo Mage recipe,
then call `act` with the pending seq and `{"type":"submit_deck","hero_class":"MAGE","cards":[...the 30 ids...]}`.
The host does not read deck.json: you must submit the actual class and card ids through MCP.
Read `references/decklist.md` once to know your cards. After acceptance the deck is fixed for this game.

You may replace this recipe with your own deck-building instructions or a script, including random decks
using `game/card_pool.json`. Submit exactly 30 legal card ids from one class plus Neutral cards, at most
2 copies per card and 1 per Legendary. Fix any INVALID_DECK error and resubmit with the new seq.

## Mulligan

Keep cards that cost 3 or less. Going second (check the game_start event or your four-card starting hand;
The Coin arrives after both mulligans), also keep one 4-cost minion.
Put the rest back.

## Every turn

1. Lethal check: add up the damage you can deal to the enemy hero this turn (minions that can attack and are
   not blocked by a Taunt, Fireball 6, Frostbolt 3, Arcane Missiles up to 3, Fireblast 1). If it is enough,
   go face with everything.
2. Trades: attack an enemy minion when your attacker kills it and survives, or when it removes a Taunt that
   blocks lethal. Otherwise attack the enemy hero.
3. Spend your mana: play the best minions you can afford; use removal (Frostbolt, Fireball, Polymorph) on
   the biggest threats; Flamestrike when it kills two or more enemy minions.
4. Use Fireblast with spare mana (on a 1-health minion, otherwise the enemy hero).
5. End the turn with `{"type":"end_turn"}` when nothing useful is left.

Keep short notes in `scratch/notes.md` if they help you (for example, cards the opponent has played).
Never stop before the arena tools report GAME OVER.
