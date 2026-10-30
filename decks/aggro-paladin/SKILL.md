---
name: aggro-paladin
description: Aggressive midrange Paladin that curves out with shielded and sticky minions, wins the board with Truesilver and Blessings, and closes with Charge and burn.
model: haiku
---

# Aggro Paladin playbook

## 1. Submit the deck (first decision)

Read `deck.json` and call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"PALADIN","cards":[...the 30 ids from deck.json...]}`.
If you get INVALID_DECK, fix the listed problem and resubmit with the NEW seq. Never submit_deck during play.

## 2. Mulligan

Keep: Argent Squire, Argent Protector, Knife Juggler, Loot Hoarder, Acidic Swamp Ooze, Harvest Golem,
Aldor Peacekeeper, Shattered Sun Cleric.
- Truesilver Champion: keep if you have 4 cards (going second) or you also keep a 2-drop and a 3-drop.
- Chillwind Yeti: keep only with 4 cards and a cheaper minion kept.
- Blessing of Might: keep only next to a kept 1- or 2-cost minion.
- Going first with two 3-drops and nothing cheaper: put one 3-drop back.
Replace everything else (Blessing of Kings, Hammer of Wrath, Consecration, Avenging Wrath, Argent Commander, Tirion).
Send `{"type":"mulligan","replace":[entity ids to put back]}` (`[]` keeps all).

## 3. Every turn, in this order

1. **Lethal check.** Add: attack of your minions that can attack + Truesilver 4 (equipped or affordable)
   + Hammer of Wrath 3 + Consecration 2 + Blessing of Might +3 / Blessing of Kings +4 on a ready attacker
   + Argent Commander 4 (Charge) + Avenging Wrath 8 only if the enemy has no minions. Count only what your mana pays for.
   Kill Taunts in the way first. If total ≥ enemy health + armor: spells to the enemy hero, every attack to the face.
2. **Pre-plays:** Acidic Swamp Ooze if the enemy has a weapon. Hammer of Wrath early if it kills a good target.
3. **Trades.** Attack an enemy minion when your attacker kills it and survives (Divine Shield counts as surviving),
   when it is a Taunt in the way, or when it is dangerous (attack 4+, Mana Wyrm, Sorcerer's Apprentice, Knife Juggler,
   Raid Leader, Dire Wolf Alpha, Imp Master, Violet Teacher, Questing Adventurer). Use the smallest attacker that does it.
   If the enemy board can deal half your health next turn, trade first. Otherwise attack the enemy hero.
4. **Spend all your mana** (see card rules). Play Knife Juggler before other minions on the same turn.
5. **Hero power** (Reinforce, 2 mana, a 1/1) whenever 2 mana is left and you have fewer than 7 minions.
6. `{"type":"end_turn"}`.

Minions can attack the turn after they are played (Argent Commander has Charge: it can attack at once).
Play buffs and minions with battlecries BEFORE attacking with the minion they help.

## 4. Card rules

- **Argent Squire** (1, 1/1 shield): turn-1 play.
- **Blessing of Might** (1, +3 attack): on a minion that attacks THIS turn, to win a trade or for lethal.
- **Argent Protector** (2): shield your best attacker that has no shield. Play after another minion.
- **Knife Juggler** (2): play first; every minion or Reinforce after it pings a random enemy.
- **Loot Hoarder** (2, 2/1, draws on death): trade it freely.
- **Acidic Swamp Ooze** (2, 3/2): kills the enemy weapon; else a normal 2-drop.
- **Aldor Peacekeeper** (3): target the enemy minion with the highest attack (3+). It becomes 1 attack.
- **Harvest Golem** (3, 2/3, leaves a 2/1): trade it first.
- **Shattered Sun Cleric** (3): +1/+1 on a minion about to trade. Needs a friendly minion.
- **Truesilver Champion** (4, weapon 4/2, hero heals 2 per attack): attack minions with 4 or less health and low attack
  (Mana Wyrm, Apprentice, 2-3 drops); else face. Do not replace a weapon that still has durability.
- **Blessing of Kings** (4, +4/+4): on a minion that can attack this turn, best on a Divine Shield minion.
- **Hammer of Wrath** (4, 3 damage + draw): kill a 3-health threat, or 3 to the face for lethal.
- **Consecration** (4, 2 damage to all enemies incl. hero): when it kills 2+ minions, or for lethal.
- **Chillwind Yeti** (4, 4/5): turn-4 body.
- **Argent Commander** (6, 4/2 Charge + shield): play and attack at once (good trade or face).
- **Avenging Wrath** (6, 8 damage split randomly among enemies): vs an empty or tiny board, or as a finisher.
- **Tirion Fordring** (8, 6/6 shield Taunt, leaves a 5/3 weapon): play when you have 8 mana.

Curve: turn 1 Squire, 2 a 2-drop (or Reinforce), 3 Aldor/Golem/Cleric, 4 Truesilver/Kings/Yeti,
5 4-drop + 1-drop, 6 Commander, 8 Tirion.

## 5. Matchup reminders

- **Mage:** kill Mana Wyrm and Sorcerer's Apprentice at once. Aldor the Boulderfist Ogre / Yeti / Tiger.
  Kings a minion that attacks right away (Polymorph). From turn 7 (Flamestrike) don't dump extra minions if already ahead.
- **Hunter / Warlock Zoo / token decks:** trade early, Consecration on 2+ small minions, then turn to face.
- **Warrior / Rogue / Shaman / Hunter / Paladin weapons:** Ooze the weapon.
- **Slow decks (Priest, Control Warrior, Ramp Druid):** you are the beatdown: go face whenever the board is safe.

## 6. Never

- Never cast Blessing of Might/Kings, Shattered Sun Cleric or Argent Protector without a friendly minion target.
- Never cast Consecration when it kills nothing, unless it is lethal.
- Never use Avenging Wrath into 4+ enemy minions unless it is lethal.
- Never hit face when the enemy board threatens lethal on you and a trade exists.

## 7. Safety rules

- Only build actions from the LEGAL ACTIONS list. Entity ids are integers from the state, never card ids like "CS2_097".
- Give `target` only when the legal action lists targets; never add `position` to spells or weapons.
- After a rejected action, read the new state and use the NEW seq.
- If "no decision ready", call `wait` again. Never stop before GAME OVER.
- Decide quickly. If unsure, play `{"type":"end_turn"}`.
