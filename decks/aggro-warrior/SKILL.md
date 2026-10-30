---
name: aggro-warrior
description: Tempo weapon Warrior that wins the board with weapons and sturdy 2-drops, then bursts with Charge minions and Heroic Strike.
model: haiku
---

# Tempo Weapon Warrior playbook

## 1. Submit the deck (deck_submission, seq 1)

Read `deck.json` and call `act` with the pending seq and
`{"type":"submit_deck","hero_class":"WARRIOR","cards":[...the 30 ids from deck.json...]}`.
If the reply is INVALID_DECK, fix the listed problem and resubmit with the NEW seq.

## 2. Your cards (cost, name, card id)

- 1 Upgrade! `EX1_409`: weapon +1/+1, or equip a 1/3 weapon if you have none.
- 2 Bloodsail Raider `NEW1_018` 2/3: gains your weapon's Attack. Equip a weapon FIRST.
- 2 Faerie Dragon `NEW1_023` 3/2: spells and hero powers can't target it.
- 2 Amani Berserker `EX1_393` 2/3: +3 Attack while damaged.
- 2 Cruel Taskmaster `EX1_603` 2/2: deal 1 damage to a minion and give it +2 Attack.
- 2 Heroic Strike `CS2_105`: hero +4 Attack this turn (adds to your weapon).
- 2 Execute `CS2_108`: destroy a DAMAGED enemy minion.
- 3 Fiery War Axe `CS2_106`: weapon 3/2 (costs 3, not 2).
- 3 Frothing Berserker `EX1_604` 2/4: +1 Attack whenever any minion takes damage.
- 3 Harvest Golem `EX1_556` 2/3: leaves a 2/1 when it dies.
- 4 Kor'kron Elite `NEW1_011` 4/3 Charge.  4 Arathi Weaponsmith `EX1_398` 3/3: equips a 2/2 weapon.
- 4 Mortal Strike `EX1_408`: 4 damage to any target, 6 if your hero has 12 or less Health.
- 5 Arcanite Reaper `CS2_112`: weapon 5/2.  6 Argent Commander `EX1_067` 4/2 Charge, Divine Shield.
- 7 Gorehowl `EX1_411`: weapon 7/1; attacking a MINION costs 1 Attack instead of durability.
- 8 Grommash Hellscream `EX1_414` 4/9 Charge, +6 Attack while damaged.
- Hero power Armor Up!: 2 mana, gain 2 Armor, no target.

## 3. Mulligan

Keep: Faerie Dragon, Amani Berserker, Bloodsail Raider, Frothing Berserker, ONE Fiery War Axe.
Keep Cruel Taskmaster only if you also keep another 2- or 3-cost minion. Keep Harvest Golem if no other 3-drop.
Going second (4 cards): also keep ONE Kor'kron Elite or Arathi Weaponsmith if you keep anything else.
Replace everything else (Heroic Strike, Execute, Mortal Strike, Reaper, Commander, Gorehowl, Grommash, Upgrade!, 2nd Axe).
Action: `{"type":"mulligan","replace":[entity ids to put back]}`.

## 4. Every turn, in this order

1. **Lethal check.** Add: attack of every minion that can attack + Charge minions you can play
   (Kor'kron 4, Commander 4, Grommash 4, or 10 if damaged) + weapon Attack (if the hero has not attacked)
   + Heroic Strike 4 + Mortal Strike 4/6, within your mana. Enemy Taunts must die first.
   If total >= enemy Health + Armor: play the damage cards, attack the enemy hero with everything.
2. **Weapon first.** If you will play Bloodsail Raider this turn, play the weapon (Axe, Reaper, Weaponsmith) before it.
3. **Cruel Taskmaster target:** enemy minion with 1 Health > big enemy minion you will Execute this turn
   > your own Amani/Frothing/Grommash that can still attack > highest-Attack enemy minion.
4. **Trades** (attack enemy minions):
   - Always kill Taunts that block your attacks.
   - Attack when your attacker kills the minion and survives.
   - Kill dangerous minions even at a cost: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Flametongue Totem,
     Water Elemental, Spell Damage minions, anything with 5+ Attack.
   - Execute the biggest damaged enemy minion (cost 4+) or a damaged Taunt. Not a 1-2 cost minion.
   - Weapon hits on minions cost Health equal to that minion's Attack: do it freely above 15 Health;
     at 12 or less, trade with minions instead and save the weapon for face/Taunts.
   - Otherwise attack the enemy hero.
5. **Spend mana** using the most mana possible. Turn plan: T2 a 2-drop (Faerie > Amani > Raider > Taskmaster);
   T3 Frothing, or Axe if an enemy minion has 3 or less Health; T4 Kor'kron / Weaponsmith / two 2-drops;
   T5 weapon + Raider, or Reaper; T6 Commander; T7 Gorehowl; T8 Grommash.
6. **Armor Up!** if 2+ mana remains and nothing else fits.
7. `{"type":"end_turn"}`.

## 5. Key card rules

- Never replace a weapon that still has durability and has not attacked this turn. Attack first, then equip.
- Upgrade! is best on Axe or Reaper, not as a turn-1 1/3 weapon (unless nothing else to do).
- Heroic Strike: only for lethal or to kill a minion you must remove. Not as a random face hit.
- Mortal Strike: save for the enemy hero (lethal or enemy at 8 or less); hit a 5+ Attack minion only when you are at 12 or less.
- Gorehowl: attack minions first (biggest it can kill), the enemy hero last (that breaks it).
- Argent Commander: its shield lets it kill a 4-Health minion and survive.
- Grommash: play with Cruel Taskmaster on him (10 mana) for a 12-Attack Charge hit, or as a 4-damage finisher.
- Never attack with your hero into a minion whose Attack is at or above your Health.
- Vs Mage at 7+ mana and you are ahead: keep at most 3 minions on board (Flamestrike deals 4 to all); hold Charge minions.
- Vs Paladin/Shaman/Warlock: don't flood the board with 2-Health minions (Consecration, Lightning Storm, Hellfire).
- Go all face when the enemy board is empty, or enemy Health is 12 or less and your board is stronger.

## 6. Safety rules (always)

- Only build actions from the LEGAL ACTIONS list of the current decision. Use its seq.
- `card`, `attacker`, `target` are integer entity ids from the state, never card ids like "CS2_106".
- Give `target` only when that legal action lists targets (Execute, Mortal Strike, Cruel Taskmaster, attacks).
  Never give a target to Heroic Strike, weapons, Upgrade! or Armor Up!. Never give `position` to spells or weapons.
- After a rejected action, read the error and retry with the NEW seq.
- If unsure what to do, play `{"type":"end_turn"}`.
- Never stop before GAME OVER. If `wait` says no decision is ready, call `wait` again.
