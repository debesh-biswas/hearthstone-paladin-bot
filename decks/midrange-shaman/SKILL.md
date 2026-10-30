---
name: midrange-shaman
description: Midrange Shaman that controls the board with cheap removal and sturdy minions, then bursts with Doomhammer, Rockbiter and Al'Akir.
model: haiku
---

# Midrange Shaman playbook

## 1. Submit the deck (first decision)

Read `deck.json`, then call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"SHAMAN","cards":[...the 30 ids from deck.json...]}`.
If you get INVALID_DECK, fix the listed problem and resubmit with the NEW seq.

## 2. Mulligan

Keep: Lightning Bolt, Unbound Elemental, Harvest Golem, Feral Spirit, Acidic Swamp Ooze.
Keep Flametongue Totem only if you also keep a minion. Keep at most one Rockbiter Weapon and one Earth Shock.
Going second (4 cards): you may also keep one Chillwind Yeti or Gnomish Inventor, and one Lightning Storm.
Replace: Hex, Fire Elemental, Doomhammer, Al'Akir, Argent Commander, Defender of Argus, Mana Tide Totem,
Bloodmage Thalnos, and second copies of any spell.
Action: `{"type":"mulligan","replace":[entity ids to put back]}` (`[]` keeps all).

## 3. Every turn, in this order

1. **Lethal check.** Add: attack of each friendly minion that can attack (Al'Akir and Doomhammer hit twice:
   Windfury), Lightning Bolt 3, Rockbiter +3 (+6 on Doomhammer or Al'Akir), Fire Elemental 3, Argent Commander 4
   and Al'Akir 6 (Charge). Subtract enemy Taunt health you must clear (Earth Shock removes a Taunt for 1).
   If total ≥ enemy health + armor: clear Taunts, then everything goes to the enemy hero.
2. **Remove threats.** Kill first: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Water Elemental, any minion
   with 5+ attack, any minion that grows or draws cards.
3. **Attacks.** Attack an enemy minion when your attacker kills it and survives, or when a smaller minion kills a
   bigger one. Otherwise attack the enemy hero. Do not trade Fire Elemental or Yeti into 1/1s.
4. **Spend your mana** (see card rules). Use as much mana as possible. Play minions before attacking only if they
   buff attackers (Flametongue, Defender of Argus).
5. **Hero power** (Totemic Call, 2 mana, no target) when 2 mana is left and you have a free board slot.
6. `{"type":"end_turn"}`.

## 4. Curve guide

- T1: usually nothing (Bolt only a strong 1-drop such as Mana Wyrm).
- T2: Acidic Swamp Ooze, else hero power. Rockbiter on your hero to kill a 3-health minion if you have 20+ health.
- T3: Unbound Elemental > Harvest Golem > Feral Spirit (if enemy has 2+ minions) > Flametongue (only next to a minion).
- T4: Chillwind Yeti / Gnomish Inventor / Hex on a big threat / 3-drop + 1-cost spell.
- T5: Doomhammer if the board is not dangerous, else Flametongue + spell or 4-drop + 1-drop.
- T6: Fire Elemental; or Feral Spirit + Flametongue placed between the wolves; or Argent Commander.
- T8+: Al'Akir. Keep 2 mana for Rockbiter when it gives lethal.

## 5. Overload

Overload locks that many mana crystals NEXT turn (state shows `overload_next_turn`).
- Lightning Bolt (1), Feral Spirit (2), Lightning Storm (2), Doomhammer (2).
- Do not play an Overload 2 card the turn before you want to play Doomhammer (5) or Fire Elemental (6),
  unless you need it to survive.
- Play Unbound Elemental BEFORE Overload cards in the same turn (it gains +1/+1 for each).

## 6. Key card rules

- **Hex** (4): only on the biggest threat: cost 5+, attack 5+, or Water Elemental. Not on 2-3 drops.
- **Earth Shock** (1): kills Argent Commander, Scarlet Crusader, Argent Squire (removes Divine Shield first);
  removes a Taunt that blocks lethal. Never on your own minions.
- **Lightning Bolt** (1): kill a minion with 3 or less health, or 3 face for lethal.
- **Lightning Storm** (3): only if it kills 2+ enemy minions (count 2 damage) or you are about to lose the board.
  Play Bloodmage Thalnos first if you can (+1 damage).
- **Rockbiter Weapon** (2): target your hero to kill a small minion, or Doomhammer/Al'Akir for burst.
  Doomhammer + Rockbiter = 10 damage.
- **Flametongue Totem**: give it a `position` between two of your minions (position = index of the right
  neighbour; board is listed left to right). Never on an empty board unless nothing else to do.
- **Defender of Argus**: same placement, between your two best minions.
- **Fire Elemental**: 3 damage to the best enemy minion with 3 or less health, else the enemy hero.
- **Doomhammer**: attack face twice per turn. Do not hit big minions with your hero.
- **Mana Tide Totem**: play when you have spare mana (not on turn 3); it draws every turn it lives.
- **Al'Akir**: 6 Charge damage or clears two small minions; also a Taunt wall when behind.

## 7. Against Mage

Kill Mana Wyrm and Sorcerer's Apprentice early. Hex Water Elemental or Boulderfist Ogre. Earth Shock their Argent
Commander. Stranglethorn Tiger is Stealth: you cannot target it until it attacks. From turn 7, do not put more than
3 small minions on the board (Flamestrike deals 4). Doomhammer is very strong here. Push face once their board is
clear.

## 8. Never

- Never play Lightning Storm into a single small minion.
- Never attack with your hero into a minion whose attack would leave you below 10 health.
- Never target your own minions with Hex, Earth Shock or Bolt.

## 9. Safety rules

- Only build actions from the LEGAL ACTIONS list of the current decision.
- Entity ids are integers taken from the state (never card ids like "EX1_246") during play.
- Give `target` only when the legal action lists targets; give `position` only for minions.
- After a rejected action, use the NEW seq.
- Never stop before GAME OVER. If "no decision ready", call `wait` again.
- If unsure what to do, play `{"type":"end_turn"}`.
