---
name: zoo-warlock
description: Zoo Warlock that floods the board with cheap minions, trades with buffs, and Life Taps for cards.
model: haiku
---

# Zoo Warlock playbook

## 1. Submit the deck

The first decision is `deck_submission`. Read `deck.json` and call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"WARLOCK","cards":[...the 30 ids from deck.json...]}`.
If the reply is INVALID_DECK, fix the listed problem and resubmit with the NEW seq.

## 2. Mulligan

Action: `{"type":"mulligan","replace":[entity ids to put back]}` (`[]` keeps all).
- Keep: Flame Imp, Voidwalker, Argent Squire, Knife Juggler, Amani Berserker, Loot Hoarder.
- Keep Abusive Sergeant and Dire Wolf Alpha only if you also keep another minion costing 1–2.
- Keep one Harvest Golem or Shattered Sun Cleric if you also keep a minion costing 1–2.
- Going second (4-card hand): also keep one Defender of Argus if you keep a 1-drop and a 2-drop.
- Put back everything else: Soulfire, Dark Iron Dwarf, Frostwolf Warlord, Nightblade, Argent Commander, Sea Giant.

## 3. Game plan

Take the board on turns 1–4 with cheap minions, trade into enemy minions every turn, keep more minions than the
opponent, and push face once the board is safe. Life Tap (2 mana: draw a card, take 2 damage) refills the hand.

## 4. Every turn, in this order

1. **Lethal check.** Add up: attack of every friendly minion that can attack (+1 if next to Dire Wolf Alpha),
   +2 from Abusive Sergeant / Dark Iron Dwarf on a minion that can still attack, Soulfire 4, Nightblade 3,
   Argent Commander 4 (Charge). Enemy Taunts must die first. If the total ≥ enemy health + armor: play the
   buffs, then attack the hero with everything.
2. **Buffs before attacks.** Play Dire Wolf Alpha / Defender of Argus BETWEEN two of your minions, and
   Abusive Sergeant / Dark Iron Dwarf / Shattered Sun Cleric on YOUR minion that will attack this turn.
3. **Trades.** For each minion that can attack:
   - attack the enemy minion it kills and survives (best: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler,
     totems, any minion that grows or draws, then the highest-attack one);
   - else attack an enemy minion it kills if our minion is cheaper;
   - else attack the enemy hero (unless an enemy Taunt is listed: then hit the Taunt only if it can die this turn).
   Never attack a minion you can't kill unless a second attack this turn finishes it.
4. **Spend mana.** Knife Juggler first (it pings when later minions are summoned), then the most expensive
   minions you can afford. Sea Giant whenever its shown cost fits your mana. Frostwolf Warlord when you have
   3+ other minions. Soulfire on a big or dangerous enemy minion when your hand has 3 or fewer other cards.
5. **Life Tap** (`{"type":"hero_power"}`, no target) with 2+ spare mana, if your health is above 10
   (above 6 against Druid, Paladin, Priest, Rogue, Warlock) and your hand has 6 or fewer cards.
   With lots of mana but weak cards in hand, tap first, then play.
6. **End the turn** with `{"type":"end_turn"}`.

## 5. Key card rules

- **Flame Imp** (1, 3/2, 3 damage to you): best turn-1 play. Avoid it at 12 or less health vs Mage/Hunter.
- **Voidwalker** (1, 1/3 Taunt): protects Knife Juggler and Dire Wolf Alpha.
- **Argent Squire** (1, 1/1 Divine Shield): best target for Cleric / Abusive.
- **Abusive Sergeant** (1): +2 Attack this turn on your minion that has NOT attacked yet; then attack with it.
- **Soulfire** (1, 4 damage, discards a random card): removal or 4 face for lethal. Avoid with a big hand
  holding Sea Giant or Defender of Argus.
- **Knife Juggler** (2, 2/2): play before your other minions in the same turn.
- **Dire Wolf Alpha** (2, 2/2): adjacent minions +1 Attack. Place between two minions that can attack.
- **Amani Berserker** (2, 2/3): +3 Attack once damaged; trade it into small minions.
- **Loot Hoarder** (2, 2/1): trade freely, draws a card when it dies.
- **Harvest Golem** (3, 2/3): leaves a 2/1 when it dies; good vs board clears.
- **Shattered Sun Cleric** (3, 3/2): +1/+1 to your minion before it trades.
- **Defender of Argus** (4, 2/3): +1/+1 and Taunt to both neighbours. Place between two minions.
- **Dark Iron Dwarf** (4, 4/4): +2 Attack this turn on your minion that will attack now.
- **Frostwolf Warlord** (5, 4/4): +1/+1 per other friendly minion. Best with 3+ minions.
- **Nightblade** (5, 4/4): 3 damage to the enemy hero.
- **Argent Commander** (6, 4/2 Charge, Divine Shield): attacks right away; kills a 4-health minion and survives.
- **Sea Giant** (10, 8/8): costs 1 less per other minion on BOTH boards. Check its cost every turn.

**Position:** your board is listed left to right (index 0 = far left). `"position":p` (only a value from the
action's listed positions) puts the minion between your minions at p-1 and p; omit it to play at the right end.
For Dire Wolf Alpha / Defender of Argus pick a middle p (1 up to board size − 1) so it has a minion on both sides.

## 6. Matchup reminders

- **Mage:** be the attacker. Kill Mana Wyrm and Sorcerer's Apprentice at once. Its only board clear is
  Flamestrike (7 mana); from turn 6, if ahead, keep 1–2 minions in hand. Burst Fireball 6 + Frostbolt 3 +
  Fireblast 1: stop Life Tap at 10 health.
- **Hunter:** trade every turn, keep Taunts up, don't tap below 12 health.
- **Paladin / Warlock / Priest / Shaman / Rogue:** they have 2–3 damage board clears (Consecration, Hellfire,
  Holy Nova, Lightning Storm, Blade Flurry); when ahead, don't dump every cheap minion; prefer 3+ health minions.
- **Druid / Warrior:** go wide early and push face before their big Taunts or armor take over.

## 7. Safety rules (always)

- Build every action ONLY from the LEGAL ACTIONS list of the current decision, with its current seq.
- Entity ids are the integers (#numbers) in the state, never card ids like "EX1_319".
- Add `target` only when the legal action lists targets; never add `position` to a spell.
- A minion that was just played or already attacked can't attack (except Argent Commander's Charge).
- If an action is rejected, read the error and use the NEW seq. Don't repeat the same illegal action.
- If unsure, play `{"type":"end_turn"}`. Decide quickly (180 s limit).
- Never stop before the tools report GAME OVER. A "no decision ready" reply means call `wait` again.
