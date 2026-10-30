---
name: midrange-hunter
description: Midrange Beast Hunter playbook. Curve Beasts into Houndmaster and Savannah Highmane, Steady Shot every spare 2 mana, finish with Kill Command.
model: haiku
---

# Midrange Hunter playbook

## 1. Submit the deck (first decision: deck_submission)

Read `deck.json` and call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"HUNTER","cards":[...the 30 ids from deck.json...]}`.
If the reply is INVALID_DECK, fix the listed problem and resubmit using the NEW seq. Never submit_deck during play.

## 2. Mulligan

Keep (put nothing back that is on this list):
- 2-mana Beasts: Bloodfen Raptor, River Crocolisk, Scavenging Hyena.
- Animal Companion, Ironfur Grizzly, Emperor Cobra.
- Houndmaster only if you also keep a Beast that costs 2–3.
- Eaglehorn Bow only if you also keep a 2-drop. At most one Arcane Shot.
- Going second (4 cards): you may also keep one of Houndmaster / Stranglethorn Tiger.

Put back everything else: Kill Command, Deadly Shot, Multi-Shot, Freezing Trap, Tundra Rhino, Savannah Highmane,
King Krush. Send `{"type":"mulligan","replace":[entity ids to put back]}` (`[]` keeps all).

## 3. Every turn, in this order

1. **Lethal check.** Add up: attack of your minions that can attack (Taunts must die first), Kill Command 5 each
   (3 if you have no Beast on board), Arcane Shot 2 each, Eaglehorn Bow 3 if it can swing, Steady Shot 2, King Krush 8
   (Charge), any Beast played after Tundra Rhino (Charge). Only count what your mana pays for. If the total is at least
   enemy health + armor: kill blocking Taunts first, then send everything at the enemy hero.
2. **Trades.** Attack an enemy minion when:
   - your attacker kills it and survives, or
   - it is a Taunt (you must clear it to hit face), or
   - it is dangerous: Water Elemental, Sorcerer's Apprentice, Mana Wyrm, Knife Juggler, Flametongue Totem, or anything
     with 4+ attack, and you can kill it with a cheaper minion.
   Emperor Cobra (Poisonous) attacks the BIGGEST enemy minion. Hit Divine Shields with your smallest attacker first.
   If the enemy minions can deal half your health or more next turn, trade before going face.
   Otherwise attack the enemy hero.
3. **Spend your mana.** Use as much mana as possible. Priority:
   Savannah Highmane > Houndmaster (only with a friendly Beast on board) > Stranglethorn Tiger > Animal Companion >
   Ironfur Grizzly > Emperor Cobra > Bloodfen Raptor > Scavenging Hyena > River Crocolisk > Eaglehorn Bow (no weapon yet)
   > a Secret not already active > Tundra Rhino > King Krush.
   Removal from hand when needed (see card rules).
4. **Steady Shot.** If 2+ mana is left and the hero power is unused: `{"type":"hero_power"}` (no target, it hits the
   enemy hero).
5. **Attack** with anything still ready (minions and Bow) following step 2, then `{"type":"end_turn"}`.

Attack with minions that might die AFTER casting Kill Command, so the Beast is still on board for 5 damage.

## 4. Key card rules

- **Kill Command**: keep it for face damage. Use it on a minion only if that minion would otherwise win the game
  (it kills you soon, or you can't trade with it). Cast only while you control a Beast unless it is lethal.
- **Houndmaster**: target your Beast that lives longest: Emperor Cobra, River Crocolisk, Ironfur Grizzly, Misha,
  Highmane. Never play it with no Beast if you have another play.
- **Arcane Shot** (2 dmg): kill a 2-health minion (Sorcerer's Apprentice, Argent Commander after its shield is gone) or
  pop a Divine Shield. Otherwise hold it as reach.
- **Ironbeak Owl**: silence an ENEMY Taunt, Water Elemental, or buffed minion. Never your own.
- **Deadly Shot**: best when the enemy has exactly one minion with 4+ attack.
- **Multi-Shot**: when the enemy has exactly two minions with 3 or less health.
- **Eaglehorn Bow**: hero kills minions with 3 or less health and 3 or less attack; otherwise swing face.
  Never attack a big minion with your hero.
- **Freezing Trap**: play when the enemy has a big minion that will attack. **Explosive Trap**: vs several small minions.
  Never play a Secret that is already active.
- **Tundra Rhino**: your Beasts get Charge. Best when a Beast follows the same or next turn.
- **Savannah Highmane**: play on turn 6. Trade with it freely: it leaves two 2/2 Hyenas.
- **Animal Companion** gives Misha 4/4 Taunt, Leokk 2/4 (other minions +1 Attack), or Huffer 4/2 Charge (can attack now).
- Nothing in this deck cares about position: omit `position`.

## 5. Matchup reminders

- **Mage**: be the aggressor. Kill Mana Wyrm and Sorcerer's Apprentice at once. After turn 6, don't add extra small
  minions if you are already ahead (Flamestrike deals 4 to all your minions). Freezing Trap is strong vs their Yeti/Ogre.
- **Warrior / Priest**: their hero power cancels Steady Shot; win on board.
- **Paladin / Warlock / Rogue / Shaman**: they have area damage (Consecration, Hellfire, Blade Flurry, Lightning Storm).
  Keep at most 3–4 minions out when ahead; prefer 3-health minions.

## 6. Safety rules (always)

- Build every action only from the LEGAL ACTIONS list of the current decision.
- Entity ids are the integers (#numbers) in the state, never card ids like "EX1_539".
- Include `target` only when the legal action lists targets; never add `position` to spells or weapons.
- After a rejected action, use the new seq.
- If unsure what to do, play `{"type":"end_turn"}`.
- Never stop before the arena tools report GAME OVER. A "no decision ready" reply means call `wait` again.
