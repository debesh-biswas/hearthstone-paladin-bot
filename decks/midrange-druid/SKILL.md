---
name: midrange-druid
description: Midrange Druid that curves Taunts and big bodies (Sen'jin, Druid of the Claw, Ancient of War, Cenarius) and wins on board.
model: haiku
---

# Midrange Druid playbook

## 1. Deck submission (first decision)
Read `deck.json`, then `act` with the pending seq and
`{"type":"submit_deck","hero_class":"DRUID","cards":[...the 30 ids from deck.json...]}`.
If the reply is INVALID_DECK, fix the listed problem and resubmit using the NEW seq.

## 2. Mulligan
Send `{"type":"mulligan","replace":[entity ids to put back]}` (`[]` keeps all).
- KEEP: Faerie Dragon, Acidic Swamp Ooze, Harvest Golem, Earthen Ring Farseer, one Wrath.
- KEEP Wild Growth if going second (you have 4 cards), or going first with a 2-drop AND a 4-drop.
- KEEP Innervate only with a 2-cost or 4-cost card in hand.
- KEEP one Sen'jin or Yeti if going second, or if you also keep a 2- or 3-cost minion.
- KEEP one Swipe only vs Hunter, Paladin, Warlock, Druid or Rogue.
- REPLACE everything else (Savage Roar, Starfall, Nourish, Keeper, all 5+ cost cards, 2nd Wrath).

## 3. Every turn, in this order
1. **Lethal check.** Damage that can reach the enemy hero this turn:
   minions that can attack (not blocked by Taunt) + Savage Roar (+2 per attacker and +2 hero, 3 mana)
   + Swipe to face 4 (4 mana) + Keeper "Moonfire" 2 (4 mana) + Druid of the Claw "Cat Form" 4 Charge (5 mana)
   + hero power 1 (2 mana). Wrath/Starfall/Keeper "Dispel" can remove a Taunt first.
   If total >= enemy Health + Armor: remove Taunts, then everything goes face.
2. **Trades.** Attack an enemy minion when your attacker kills it and survives, or when it must die now
   (Knife Juggler, Mana Wyrm, Sorcerer's Apprentice, Flametongue Totem, Auctioneer, Violet Teacher,
   aura/buff minions, Taunt blocking your lethal). Never attack into a minion that kills yours and survives.
   Vs Hunter/Warlock/Paladin: trade whenever even or better. Otherwise unused attackers go face.
3. **Spend your mana** (most mana used wins). Priority: big minion > removal on a threat > draw > hero power.
   - T2: Coin + Wild Growth if you have both; else Faerie Dragon / Ooze / Wrath a 2-3 health minion.
   - T3: Harvest Golem / Farseer; else Wild Growth; with 4 mana Sen'jin / Yeti.
   - T4: Swipe if it kills 2+ minions; else Sen'jin (vs aggro) or Yeti; else Keeper on a threat.
   - T5: Druid of the Claw; Starfall if it kills a big threat or 2+ minions.
   - T6: Sunwalker / Cairne; Nourish if your hand has 2 or fewer cards.
   - T7+: Ancient of War > Ancient of Lore > 6-drops; Cenarius at 9; fill leftover mana with cheap cards.
4. **Hero power** (Shapeshift, 2 mana: +1 Attack, +1 Armor) with 2 spare mana. Then attack with the hero:
   enemy hero, or a 1-health minion with Attack 2 or less.
5. `{"type":"end_turn"}` when nothing useful is left.

## 4. Choose One cards (pick the option entity id listed under `choose`, by its NAME)
- Wrath: "Solar Wrath" (3 dmg) on a 2-3 health minion; "Nature's Wrath" (1 dmg + draw) on a 1-health minion.
- Keeper of the Grove: "Moonfire" (2 dmg) on a 2-health minion or enemy hero for lethal;
  "Dispel" (Silence) on a Taunt blocking lethal, a buffed minion, Sunwalker, Cairne or Water Elemental.
- Druid of the Claw: "Bear Form" (4/6 Taunt) by default; "Cat Form" (4/4 Charge) only for lethal, or to
  kill a must-kill minion with 4 or less health while the 4/4 survives.
- Starfall: "Stellar Drift" (2 to all enemy minions) if it kills 2+; else "Starlord" (5 dmg) on the
  biggest enemy minion with 5 or less health.
- Nourish: "Enrich" (draw 3) almost always. "Rampant Growth" only with 2+ cards costing 7+ in a small hand.
- Ancient of Lore: "Ancient Teachings" (draw) by default; "Ancient Secrets" (heal 5) if your Health <= 15
  vs an aggressive deck, or <= 10 vs anyone.
- Ancient of War: "Rooted" (5/10 Taunt) by default; "Uproot" (10/5) only if the enemy board is empty and
  you are at 20+ Health.
- Cenarius: "Demigod's Favor" (+2/+2) if you have 2+ other minions; else "Shan'do's Lesson" (two Taunts).
A Choose One play looks like `{"type":"play_card","card":55,"choose":73,"target":84}`; give `target`
only if that option lists targets.

## 5. Key card rules
- Innervate: only together with a card it makes affordable THIS turn. Never alone.
- Wild Growth: turn 2 with Coin, or turn 3 with no 3-drop. At 10 mana it still draws a card (Excess Mana).
- Savage Roar: only for lethal (or vs a slow deck at <=15 Health when it adds 6+ face damage).
- Swipe: 4 dmg on the best enemy minion it kills, 1 to all others. Hero only for lethal or empty board.
- Earthen Ring Farseer heal: your hero if missing 3+ Health, else a damaged friendly minion.
- Never target your own minions with Wrath, Keeper, Starfall or Swipe.
- Minion position does not matter: omit `position`.

## 6. Matchup reminders
- Mage: Faerie Dragon can't be hit by their spells or hero power. Kill Mana Wyrm / Sorcerer's Apprentice
  at once. They have one Flamestrike (7 mana, 4 to all your minions): from turn 7 prefer minions with
  5+ Health and don't flood small minions. Pop Argent Commander's Divine Shield with Swipe splash or Moonfire.
  Be the aggressor from turn 6.
- Hunter / Warlock / Paladin aggro: you are the control deck. Trade, Taunt, heal (Farseer, Ancient Secrets).
- Warrior / Rogue / Paladin / Hunter / Shaman: Ooze destroys their weapon; hold it a turn if a weapon is coming.
- Vs board clears (Flamestrike, Brawl, Consecration, Equality): when already ahead, keep 2-3 minions and hold the rest.

## 7. Safety rules
- Only build actions from the LEGAL ACTIONS list. Entity ids are integers from the state, never card ids.
- Give `target` only when that legal action lists targets; give `choose` for every Choose One card.
- After a rejected action, use the NEW seq.
- If unsure what to do, play `{"type":"end_turn"}`. Decide fast (the clock is 180 s per decision).
- If `wait` says no decision is ready, call `wait` again. Never stop before GAME OVER.
