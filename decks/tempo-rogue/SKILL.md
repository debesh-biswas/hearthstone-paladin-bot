---
name: tempo-rogue
description: Tempo Rogue that wins the board early with cheap removal and Combo cards, then finishes with burst.
model: haiku
---

# Tempo Rogue playbook

## 1. Deck submission (first decision)

Read `deck.json`. Call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"ROGUE","cards":[...the 30 ids from deck.json...]}`.
If the reply is INVALID_DECK, fix the listed problem and resubmit with the NEW seq. Never submit_deck during play.

## 2. Mulligan

Put back (`{"type":"mulligan","replace":[entity ids]}`) every card except:
- Always keep: Backstab, SI:7 Agent, Defias Ringleader, Faerie Dragon, Loot Hoarder, Harvest Golem, Argent Squire.
- Keep Edwin VanCleef if you have 4 cards (going second) or also hold Backstab / a 1-cost card.
- Keep one Eviscerate. Keep Worgen Infiltrator only if you have no other 1- or 2-cost minion.
- Going second with a 2-drop and a 3-drop already kept: also keep one Chillwind Yeti or Perdition's Blade.
- Always put back: Cold Blood, Sap, Deadly Poison, Assassin's Blade, Assassinate, Stranglethorn Tiger,
  Argent Commander, Gnomish Inventor, Dark Iron Dwarf.

## 3. Combo rule (most important)

Combo cards get their bonus only if you already played ANOTHER CARD this turn (The Coin, Backstab and Deadly Poison
count; hero power and attacks do NOT). So play a cheap card first, then the Combo card:
- SI:7 Agent: Combo deals 2 damage (target a 2-health enemy minion, else face).
- Defias Ringleader: Combo summons an extra 2/1.
- Eviscerate: 2 damage, Combo 4.
- Cold Blood: +2 Attack, Combo +4.
- Perdition's Blade: Battlecry 1 damage, Combo 2.
- Edwin VanCleef: +2/+2 per other card played this turn. Coin + Backstab + Edwin = 6/6. Never play him as the first card
  if a 0-1 cost card is playable before him.
Good enablers: Backstab (0), The Coin (0), Deadly Poison (1, needs a weapon), Argent Squire / Worgen Infiltrator (1).

## 4. Every turn, in this order

1. **Lethal check.** Add: ready minions' Attack (not blocked by Taunt) + weapon Attack (+2 per Deadly Poison)
   + Eviscerate 4 + Cold Blood +4 on a ready minion + SI:7 combo 2 + Argent Commander 4 (Charge)
   + Dark Iron Dwarf +2 on a ready minion. If it is at least the enemy hero's health + armor:
   remove blocking Taunts first (Sap, attacks, SI:7/Eviscerate), then everything to the enemy hero.
2. **Removal / trades.** Kill dangerous enemy minions with the cheapest tool:
   Backstab (2 dmg, only an UNDAMAGED minion) → weapon attack → SI:7 combo → Perdition's Blade → Eviscerate →
   a trade with a minion. Must-kill: Sorcerer's Apprentice, Mana Wyrm, Knife Juggler, Flametongue Totem,
   Raid Leader, Dire Wolf Alpha, anything with 5+ Attack, Taunts in the way.
   Attack an enemy minion when your attacker kills it and survives, or kills a more expensive minion.
   Otherwise attack the enemy hero.
3. **Spend all your mana.** Play the cheap enabler first, then the Combo card. Default priority when no combo:
   - Turn 1: Argent Squire > Worgen Infiltrator. With Coin on turn 1-2: Coin then Defias Ringleader or SI:7 Agent.
   - Turn 2: Faerie Dragon > Defias Ringleader (combo) > Loot Hoarder > Ringleader > hero power.
   - Turn 3: SI:7 Agent (combo) > Edwin (with a card before him) > Harvest Golem > Perdition's Blade.
   - Turn 4: 1-cost card + SI:7 > Chillwind Yeti > Dark Iron Dwarf > two 2-drops > Gnomish Inventor.
   - Turn 5: Stranglethorn Tiger > Yeti + 1-drop > Assassin's Blade (if no weapon).
   - Turn 6+: Argent Commander > Tiger > Yeti; use all mana, two cards a turn.
4. **Hero power** (2 mana, equip a 1/2 dagger) only if you have 2 spare mana AND no weapon equipped. Then attack with it.
5. `{"type":"end_turn"}`.

## 5. Key card rules

- Backstab: only an undamaged enemy minion; use it BEFORE attacking that minion.
- Deadly Poison: only with a weapon equipped; play it before the hero attacks.
- Cold Blood / Dark Iron Dwarf: only on YOUR minion that can still attack this turn (not Faerie Dragon).
- Sap: on a Taunt blocking lethal, or an enemy minion costing 5+ when you are ahead. Never on a 1-2 cost minion.
- Assassinate: only on an enemy minion costing 4+ (Boulderfist Ogre, Water Elemental, Tiger, Yeti, Sen'jin, Commander).
- Assassin's Blade / Perdition's Blade: never hero power while one is equipped (it replaces it).
- Hero attacking a minion: only if your hero stays at 12+ health after the hit. Rogue has no healing.
- Gnomish Inventor: when hand has 2 or fewer cards, or nothing better.
- vs Mage: kill Mana Wyrm and Sorcerer's Apprentice at once; don't attack Water Elemental (it freezes) unless killing it;
  from turn 7 do not put a 5th minion on a board that is already winning (Flamestrike).
- When ahead on board (your total Attack ≥ theirs + 4) or the enemy hero is low: go face.
  When behind on board or your hero is at 12 or less: trade first.

## 6. Safety rules

- Only build actions from the LEGAL ACTIONS list of the current decision. Use its seq.
- Entity ids are the integers (#numbers) from the state, never card id strings like "CS2_072".
- Give `target` only when the legal action lists targets; give `position` only for minions.
- After a rejected action, read the error and use the NEW seq.
- If unsure what to do, play `{"type":"end_turn"}`.
- Decide quickly. Never stop before the arena tools report GAME OVER; if `wait` says no decision is ready, call it again.
