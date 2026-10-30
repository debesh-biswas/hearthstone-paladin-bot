# Tempo Weapon Warrior — Deck Guide (hs-arena, Basic + Classic Legacy pool)

## 1. Overview and win condition

This is a **tempo / weapon Warrior**: an aggressive deck that keeps the board with weapons and sturdy 2- and 3-drops,
then kills with Charge minions, weapon swings and direct damage. It is the aggro Warrior shell of 2014
(Fiery War Axe, Heroic Strike, Frothing Berserker, Kor'kron Elite, Arathi Weaponsmith, Arcanite Reaper, Argent Commander)
rebuilt for **our** pool, where Leeroy Jenkins is gone, Fiery War Axe costs 3 and the classic 1-drops are weaker.

**Why tempo rather than pure face.** The 2014 list won by racing: 1-drops, face damage, then Leeroy + Heroic Strike + Mortal
Strike burst. In this pool the race tools are worse (Leper Gnome 1/1, no Leeroy, Axe at 3 collides with the 3-drop slot),
while the opponents we expect (Greedy Mage and other bots and classmates) play big midrange bodies (Yeti, Water Elemental,
Sen'jin, Stranglethorn Tiger, Boulderfist Ogre) and single-target removal. A deck that wins the board first and only
goes face once it is ahead beats them more reliably than a deck that throws 1/1s into Frostbolts. So this list:
- drops the weak 1-drops (Leper Gnome, Argent Squire) for 2-drops with 3 health or elusive (Bloodsail Raider, Amani Berserker,
  Faerie Dragon) and Cruel Taskmaster,
- adds **Execute x2** to kill the big Taunts/minions that stop an aggro deck,
- keeps the burst package (Kor'kron x2, Argent Commander x2, Heroic Strike x2, Mortal Strike x2, Arcanite Reaper x2),
- tops out with **Gorehowl** (board control against 4/5 and 6/7 bodies) and **Grommash** (8 mana Charge finisher).

**Win condition:** by turn 6–8 the opponent is at 10–15 health with our minions on board; then Charge minions + weapon +
Heroic Strike / Mortal Strike finish it. Weapons are our main damage source, and they **cannot be hit by minion removal**
(Frostbolt, Fireball, Polymorph do nothing to a weapon), which is why the deck is strong against removal-heavy Mage.

Simplicity: nothing in the list depends on minion position (no Dire Wolf Alpha, Flametongue, Defender of Argus),
and the only real combos are "damage a minion, then Execute it" and "weapon equipped, then Bloodsail Raider". Where two
cards were close (Jungle Panther vs Harvest Golem, Nightblade vs a 2nd Gorehowl, Warsong Commander vs anything) we took
the one a simple pilot cannot misuse.

## 2. Decklist (30)

Curve: 1 mana ×1 · 2 mana ×12 · 3 mana ×5 · 4 mana ×6 · 5 mana ×2 · 6 mana ×2 · 7 mana ×1 · 8 mana ×1.
18 minions, 5 weapons (+Upgrade!, +2 weapons from Weaponsmith), 7 spells.

| # | Cost | Id | Name | Current text / stats (our pool) | Role |
|---:|---:|---|---|---|---|
| 1 | 1 | `EX1_409` | Upgrade! | If you have a weapon, give it +1/+1. Otherwise equip a 1/3 weapon. | Turn-1 weapon or +1/+1 on Axe/Reaper |
| 2 | 2 | `NEW1_018` | Bloodsail Raider | 2/3. Battlecry: gain Attack equal to your weapon's Attack. | 5/3 after Axe, 4/3 after Weaponsmith, 7/3 after Reaper |
| 2 | 2 | `NEW1_023` | Faerie Dragon | 3/2. Can't be targeted by spells or Hero Powers. | Removal-proof pressure vs Mage/Shaman/Priest |
| 2 | 2 | `EX1_393` | Amani Berserker | 2/3. +3 Attack while damaged. | Sturdy 2-drop, 5/2 trader once hit |
| 2 | 2 | `EX1_603` | Cruel Taskmaster | 2/2. Battlecry: deal 1 damage to a minion and give it +2 Attack. | Execute enabler, kills 1-health minions, buffs Amani/Frothing/Grom |
| 2 | 2 | `CS2_105` | Heroic Strike | Give your hero +4 Attack this turn. | Burst (+4 to weapon swing) or kills a 4-health minion |
| 2 | 2 | `CS2_108` | Execute | Destroy a damaged enemy minion. | Removal for big Taunts/threats |
| 2 | 3 | `CS2_106` | Fiery War Axe | Weapon 3/2 (**3 mana now**, was 2). | Early removal, Raider enabler |
| 2 | 3 | `EX1_604` | Frothing Berserker | 2/4. Whenever a minion takes damage, gain +1 Attack. | Snowballing threat, enemy must answer it |
| 1 | 3 | `EX1_556` | Harvest Golem | 2/3. Deathrattle: summon a 2/1 Damaged Golem. | Sticky 3-drop vs single-target removal |
| 2 | 4 | `NEW1_011` | Kor'kron Elite | 4/3 Charge. | Tempo trade or 4 face damage |
| 2 | 4 | `EX1_398` | Arathi Weaponsmith | 3/3. Battlecry: equip a 2/2 weapon. | Two bodies of damage, weapon for Raider |
| 2 | 4 | `EX1_408` | Mortal Strike | Deal 4 damage; 6 if you have 12 or less Health. | Reach to face, or removal |
| 2 | 5 | `CS2_112` | Arcanite Reaper | Weapon 5/2. | 10 damage over two turns, kills Yetis/Water Elementals |
| 2 | 6 | `EX1_067` | Argent Commander | 4/2 Charge, Divine Shield. | Trades twice or 4 face damage; kills a 4-attack minion and lives |
| 1 | 7 | `EX1_411` | Gorehowl | Weapon 7/1. Attacking a minion costs 1 Attack instead of 1 Durability. | Kills several big minions in a row, then hits face |
| 1 | 8 | `EX1_414` | Grommash Hellscream | 4/9 Charge. +6 Attack while damaged. | Finisher: 4 face, 10 once damaged |

Hero power: **Armor Up!** (2 mana, gain 2 Armor, no target).

Considered and left out (all checked against the current pool): Leper Gnome (1/1 now), Argent Squire (1/1 Divine Shield;
low impact, dies to Fireblast after one hit), Southsea Deckhand (2/1, needs a weapon), Wolfrider (3/1, dies to everything), Jungle Panther (4/2 stealth;
fine but trades badly), Nightblade (5 mana 4/4 + 3 face; good reach, close cut with Harvest Golem/Gorehowl), Warsong Commander
(only buffs Charge minions now, +1 Attack), Dread Corsair (3/3 Taunt, defensive), Captain Greenskin (5/4, +1/+1 weapon; a fine
substitute for Gorehowl), Leeroy Jenkins (Hall of Fame, removed), Inner Rage (card disadvantage for a simple pilot), Whirlwind
(hurts our own 2-health minions).

## 3. How the nerfs changed the deck vs the classic version

| Card (online advice) | Our pool | Adjustment |
|---|---|---|
| Fiery War Axe "2 mana, keep always, play turn 2" | **3 mana** 3/2 | Still a keep, but it is a turn-3 play competing with Frothing. On turn 2 play a 2-drop instead. Axe + Raider is now a turn-5 play (3+2). |
| Leeroy Jenkins (6 burst, often with Heroic Strike / Mortal Strike) | **Removed** (Hall of Fame) | Burst now comes from Kor'kron, Argent Commander, Grommash and weapons. Lethal arrives a turn or two later; play for board first. |
| Leper Gnome "best 1-drop, 2 face on death" | **1/1** | Cut. Our 1-mana slot is Upgrade! (a 1/3 weapon = 3 hits of 1). |
| Knife Juggler / Abusive Sergeant style aggro 1-2 drops | Juggler 2/2 | Not used. |
| Charge (spell) + Warsong to OTK | Charge can't hit heroes; Warsong only buffs Charge minions | Not used; no Warsong/Charge combo exists any more. |
| Execute (classic 1 mana) | **2 mana** | Still worth it: 2 mana kills Ogre/Yeti/Tiger after one weapon hit or Taskmaster ping. |
| Mortal Strike | unchanged (4 / 6 at ≤12 Health) | Still burn; counts toward lethal. |
| Arcanite Reaper, Heroic Strike, Kor'kron, Arathi Weaponsmith, Frothing, Argent Commander, Gorehowl, Grommash | unchanged | Advice from 2014 guides still applies. |
| Big Game Hunter (opponent) | 5 mana | Only matters vs Grommash once damaged (10 attack): expect it rarely. |
| Opponent Mage removal: Ice Lance removed, Frostbolt/Fireball/Polymorph unchanged | — | Faerie Dragon and weapons are even better: Mage has fewer cheap answers. |

## 4. Mulligan

Starting hand: 3 cards going first, 4 going second (+ The Coin after the mulligan).

**Always keep:** Fiery War Axe `CS2_106` (one copy), Bloodsail Raider `NEW1_018`, Faerie Dragon `NEW1_023`,
Amani Berserker `EX1_393`, Frothing Berserker `EX1_604`.

**Conditional keeps:**
- Cruel Taskmaster `EX1_603`: keep if you also have another 2-drop or 3-drop; keep vs Hunter/Paladin/Warlock/Druid (1-health tokens).
- Harvest Golem `EX1_556`: keep if you have no other 3-drop.
- Upgrade! `EX1_409`: toss. A turn-1 1/3 weapon is weak; the card is much better later on Fiery War Axe or Arcanite Reaper.
- Kor'kron Elite `NEW1_011` / Arathi Weaponsmith `EX1_398`: keep **one** 4-drop going second (The Coin) if the rest of the hand
  already has a 2-drop or 3-drop.
- Execute `CS2_108`: keep one vs Warrior/Druid/Paladin only when the hand already has two early drops. Otherwise toss.
- Second Fiery War Axe: toss (one weapon is enough early).

**Always toss:** Heroic Strike, Mortal Strike, Arcanite Reaper, Argent Commander, Gorehowl, Grommash, Upgrade!.

Rule of thumb: after the mulligan we want a play on turn 2 and turn 3. A hand with only spells/weapons is a mulligan.

## 5. Turn-by-turn game plan (ideal curve)

| Turn | Ideal play | Notes |
|---|---|---|
| 1 | Upgrade! (1/3 weapon) if drawn; otherwise nothing | Hit a 1-health minion or face with the 1/3 weapon. |
| 2 | 2-drop: Faerie Dragon > Amani Berserker > Bloodsail Raider (2/3) > Cruel Taskmaster | Coin turn 1 + a 2-drop is fine going second. |
| 3 | Frothing Berserker, or Fiery War Axe if the enemy has a minion to kill; Harvest Golem | With coin: Axe + attack, or 2-drop + 2-drop. |
| 4 | Kor'kron Elite (trade or face) / Arathi Weaponsmith / Axe + 1-mana Upgrade / 2-drop + 2-drop | Weaponsmith then Raider next turn. |
| 5 | Arcanite Reaper (+ swing), or Axe/Weaponsmith-weapon + Bloodsail Raider, or 4-drop + Upgrade | Raider after a weapon is a 4/3–7/3 for 2. |
| 6 | Argent Commander, or 4-drop + 2-drop, or Reaper | Commander trades with a 4-attack minion and survives (shield). |
| 7 | Gorehowl (kill one or two big minions), or Commander + Upgrade | |
| 8+ | Grommash; Kor'kron + Heroic Strike; double burn | Count lethal every turn. |

Every turn, if 2 mana are left and nothing better uses them, press **Armor Up!**

## 6. Card-by-card notes

- **Upgrade!** Turn 1: equip the 1/3 weapon and attack (1 damage per swing, three swings: kills 1-health minions or chips face). Later:
  play it on Arcanite Reaper (6/3 = one more swing) or Fiery War Axe (4/3). Never play it with a 1-durability weapon when a
  fresh weapon is coming next turn — better to save it.
- **Bloodsail Raider** Play **after** equipping a weapon the same or a previous turn (Axe 3 → 5/3; Weaponsmith 2/2 → 4/3; Reaper → 7/3;
  Gorehowl 7 → 9/3). Without a weapon it is still an acceptable 2/3 on turn 2.
- **Faerie Dragon** Best turn-2 play vs Mage, Shaman, Priest, Druid (their hero power and spells cannot touch it). It only dies to
  combat, AoE (Flamestrike, Consecration, Hellfire, Lightning Storm) or random effects.
- **Amani Berserker** 2/3 that becomes 5/3 after taking damage. Trading into a 1- or 2-attack minion leaves a 5-attack threat.
  Good Cruel Taskmaster target (→ 7/2).
- **Cruel Taskmaster** Battlecry priority: (1) kill an enemy 1-health minion; (2) damage a big enemy minion you will Execute this
  turn; (3) buff your own Amani Berserker (+5 total) or Frothing Berserker (+3) that can attack this turn; (4) any enemy minion.
  Never use it on your own minion with 1 Health.
- **Heroic Strike** +4 Attack to the hero this turn, stacks with the weapon (Axe 3 → 7, Reaper 5 → 9). Use it for lethal, or to kill
  a 4–5 health minion when you have no weapon and your health is high. Do not use it as a turn-2 play to hit face for 4 unless lethal.
- **Execute** Only legal on a **damaged enemy** minion. Use it on the biggest threat or a Taunt that blocks lethal: Boulderfist Ogre,
  Water Elemental, Stranglethorn Tiger (after it attacks), Yeti, Sen'jin, Argent Commander (after its shield is gone), Fire Elemental, Savannah Highmane, Ironbark Protector. Enable with a
  weapon hit, Taskmaster, a minion trade or Gorehowl. Don't Execute a 2-mana minion unless it is a Taunt blocking lethal.
- **Fiery War Axe** 3 mana 3/2. Kills 2- and 3-health minions (Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Harvest Golem).
  Swing face when there is nothing worth killing.
- **Frothing Berserker** Gets +1 Attack for **every** minion that takes damage (both sides). Play it before trades on the same turn
  only if it can't attack anyway: trades made afterwards grow it. A turn-3 Frothing that survives usually wins the game.
- **Harvest Golem** Two bodies for one card, so Frostbolt/Fireball/Arcane Missiles only half-answer it (Polymorph removes the Deathrattle). Fine filler.
- **Kor'kron Elite** 4/3 Charge. If an enemy minion with ≤4 Health and ≤2 Attack exists, trade (Kor'kron survives). Else face,
  especially when the opponent is at ≤15.
- **Arathi Weaponsmith** 3/3 + 2/2 weapon. Same turn: attack with the weapon. Next turn: Bloodsail Raider (4/3).
- **Mortal Strike** 4 damage anywhere (6 if your hero has ≤12 Health). Prefer to save it for face/lethal; use it on a minion only to
  survive or to remove a must-kill (e.g. Frothing-like snowballer, Water Elemental when we have no weapon).
- **Arcanite Reaper** 5/2. Kills Yeti, Water Elemental, Sen'jin, Tiger in one swing. Two swings = 10 face. Do not replace a weapon
  that still has durability unless the new one is clearly better and the old one already swung this turn.
- **Argent Commander** 4/2 Charge + Divine Shield. Trades into a 4-health minion and survives (shield absorbs the hit), then hits
  face next turn. Pops Divine Shields/Taunts too.
- **Gorehowl** 7/1. Attacking a minion lowers its Attack by 1 instead of using durability: 7 damage kills a 6/7 Ogre, then 6, then 5...
  Attacking a hero uses the durability and the weapon breaks. Swing at big minions first, the hero last. Watch your own health:
  each minion attack deals that minion's Attack to your hero.
- **Grommash Hellscream** 4/9 Charge, 10 Attack once damaged. Damage him with Cruel Taskmaster (→ 12 attack), or attack a minion first
  (he survives with 9 health) — but he can only attack once per turn, so the usual line is Taskmaster on Grom then face for 12 (10 mana).
  At 8 mana: Grom face for 4 is fine when that is lethal; otherwise trade him into a minion; next turn he hits for 10.

## 7. Combos, synergies and positioning

- **Weapon → Bloodsail Raider** (Axe+Raider 5 mana: 3 dmg now + 5/3; Weaponsmith+Raider 6 mana; Reaper+Raider 7 mana).
- **Damage → Execute**: weapon hit / Cruel Taskmaster / trade, then Execute. Taskmaster + Execute = 4 mana removal of anything.
- **Heroic Strike + weapon**: Axe 7, Reaper 9, Upgraded Reaper 10, Gorehowl 11 to face.
- **Cruel Taskmaster on Amani** (7/2) or **Grommash** (12/8).
- **Frothing + trades**: every damaged minion is +1. A 2-for-2 trade (both damaged) = +2.
- **Upgrade! on Reaper**: 6/3 = 18 total damage over three turns.
- **Positioning:** no position effects in the deck. Default rightmost placement is always fine.

## 8. Trading rules (trade vs face)

1. **Lethal first:** if total face damage this turn ≥ enemy Health + Armor (after clearing required Taunts), go face with everything.
2. **Kill Taunts** that block attacks, with the cheapest attacker that kills them (weapon > minion if hero health is safe; Execute
   if the Taunt is damaged and big).
3. **Free trades:** attack an enemy minion when our attacker kills it and survives. Do it.
4. **Even/up trades:** trade when we kill a minion that costs at least as much as ours, or when the enemy minion is a must-kill
   (Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Flametongue Totem, Frothing Berserker, Cult Master, Water Elemental, any
   minion with ≥5 Attack, Spell Damage minions, Wild Pyromancer, Imp Master, Questing Adventurer).
5. **Otherwise face.** When we are ahead on board, or the enemy is at ≤ 15 Health and has no board, go face.
6. **Weapon on minions** costs hero Health equal to the minion's Attack. Use the weapon on minions freely while our Health > 15;
   at ≤ 12 prefer minion trades and keep the weapon for face/Taunts. (At ≤ 12 Health Mortal Strike deals 6.)
7. Priority among enemy minions: (a) Taunt blocking lethal, (b) anything that grows or snowballs, (c) highest Attack we can kill
   cheaply, (d) Spell Damage / engines, (e) the rest.
8. Against Mage at 7+ mana, don't put a 4th/5th minion on the board if we are already ahead: Flamestrike deals 4 to all our minions. Hold a
   Charge minion/weapon in hand instead.

## 9. Hero power (Armor Up!, 2 mana, +2 Armor)

- Use it whenever exactly 2+ mana are left after the best plays and nothing else costs ≤ the remainder.
- Do **not** use it instead of a 2-mana minion on turns 2–5 (tempo first).
- Against Mage/Hunter/aggro it buys time; against slow decks it is the last thing to spend mana on.
- Armor does **not** count for Mortal Strike's "12 or less Health" check (Health only).

## 10. Lethal checklist

Count face damage available this turn (enemy Health + Armor to beat):
- Each friendly minion that can attack: its Attack (Charge minions played this turn count: Kor'kron 4, Commander 4, Grom 4 / 10 damaged).
- Weapon Attack (if hero hasn't attacked) + Heroic Strike 4 per copy (2 mana each).
- Mortal Strike 4 (6 if our Health ≤ 12), 4 mana each.
- Weapon not yet equipped: Axe 3 (3 mana), Reaper 5 (5 mana), Gorehowl 7 (7 mana), Weaponsmith 2 + 3/3 body (4 mana), Upgrade! +1 (1 mana).
- Subtract Taunts: each Taunt must die first; Execute (2 mana, if damaged) or a weapon/minion attack removes it.
- Mana check: the plays must fit in this turn's mana.
Example (8 mana): Reaper equipped (5) + Kor'kron (4 mana, 4) + Heroic Strike (2 mana, 4) = 13 damage for 6 mana, + Armor Up.

## 11. Matchups

**Greedy Mage (bot: Mana Wyrm, Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Thalnos, Harvest Golem, Yeti, Water Elemental,
Fireball, Polymorph, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike).** Favoured.
- It plays greedily one action at a time, no lethal planning. Its removal is single target and can't touch weapons or Faerie Dragon.
- Mulligan: Faerie Dragon, Amani, Raider, Frothing, Fiery War Axe (Mana Wyrm/Apprentice killer).
- Kill Mana Wyrm and Sorcerer's Apprentice immediately (Axe, Taskmaster on 1-health, trades).
- Turns 4–6 it drops Yeti/Water Elemental/Sen'jin/Tiger: answer with Reaper, Execute after a hit, or trade 2-drops + Taskmaster.
  Water Elemental freezes the attacker: attack it with a minion, not the hero, unless you will Execute it anyway.
- Its Argent Commander (Charge + shield) can hit our minions: pop the shield with a small attacker before using a weapon.
- Turn 7+: Flamestrike (4 damage to all our minions). Keep 2–3 minions max on board when ahead; keep Kor'kron/Commander/weapons in hand.
- Mage burst on us: Fireball 6, Frostbolt 3, Missiles 3, Fireblast 1. At ≤ 10 Health, use Armor Up and trade.
- Boulderfist Ogre 6/7: Execute (after any damage), Gorehowl, or ignore it and race if we are far ahead.

**Hunter (midrange/face).** Even to favoured. Fight for the board early (Taskmaster kills 1-health tokens, Axe kills 2/x beasts),
Armor Up when spare mana. Don't let Houndmaster/Highmane trade freely; Execute Savannah Highmane. Race only when ahead.

**Paladin (aggro/control).** Control the 1/1 Silver Hand Recruits with Taskmaster/weapons; Consecration (2 to all) kills our 2/2s —
prefer 3-health minions. Kill Truesilver-armed hero's minions; Tirion Fordring (8 mana 6/6 Divine Shield Taunt): pop the shield with a small minion, damage him with a weapon or Taskmaster,
then Execute; expect a 5/3 Ashbringer after he dies. Equality 4 + Consecration wipes us: don't overextend.

**Warrior (control or aggro).** Mirror. Control Warrior has Execute/Shield Slam/Brawl and Armor; we need card-efficient pressure,
not a big board (Brawl). Weapons do the work. Their Acidic Swamp Ooze/Harrison Jones kill our weapon: equip and swing in the same turn.
Aggro Warrior mirror: whoever controls turns 2–4 wins; trade.

**Shaman (midrange).** Hard. Taunt totems, Flametongue, Hex, Lightning Storm (2–3 to all), Feral Spirit taunts. Faerie Dragon dodges
Hex/Earth Shock. Clear totems with weapons (Flametongue first). Execute Fire Elemental / Al'Akir. Don't overextend into Lightning Storm.

**Rogue.** Fast. Their hero power dagger (1/2) and Assassin's Blade (5 mana 3/4) kill our 2-health minions; Blade Flurry 4 clears minions only.
Prefer 3-health 2-drops. Push face — Rogue has little healing — but kill Edwin VanCleef (3 mana) and Questing Adventurer at once.

**Druid (ramp/token).** Pressure early before Druid of the Claw/Ancients; Execute big Taunts (Ancient of War, Ironbark).
Savage Roar can burst us: keep Armor up from turn 8. Swipe (4 mana: 4 to one enemy, 1 to all others) kills 1-health minions.

**Warlock (Zoo).** Board fight: trade early, Taskmaster/Axe kill 1/1s and Flame Imp (1 mana 3/2). Hellfire (4 mana, 3 to ALL characters) is their reset button;
Doomguard and Power Overwhelming are removed. Frothing grows a lot in Zoo games.

**Priest.** Slow and weak in this pool (many cards removed). Go face; Faerie Dragon and weapons dodge their removal.
Execute Lightspawn (0/5, Attack = Health) or Cabal Shadow Priest (6 mana 4/5; it steals a minion with ≤ 2 Attack, so
prefer buffing/keeping our minions above 2 Attack).

## 12. Common mistakes

- Playing Fiery War Axe on turn 2 thinking it's 2 mana — it's 3 now.
- Bloodsail Raider before the weapon (loses 2–7 Attack).
- Swinging the weapon into big minions at low Health and dying to burn.
- Executing a 2-mana minion while a Taunt Ogre stands.
- Heroic Strike to face early "for value" — save it for lethal or a key kill.
- Overextending into Flamestrike / Consecration / Lightning Storm / Hellfire when already ahead.
- Using Gorehowl on the hero first (it breaks) instead of on minions first.
- Forgetting Armor Up with 2 spare mana.
- Equipping a new weapon over one that still has charges and hasn't attacked this turn.
- Sending `target` for Heroic Strike / Fiery War Axe / Arcanite Reaper / Upgrade! / Armor Up (no targets).

## 13. Script hints (rule-based bot)

Card ids: UPG=`EX1_409`, RAIDER=`NEW1_018`, FAERIE=`NEW1_023`, AMANI=`EX1_393`, TASK=`EX1_603`, HS=`CS2_105`, EXEC=`CS2_108`,
AXE=`CS2_106`, FROTH=`EX1_604`, GOLEM=`EX1_556`, KORK=`NEW1_011`, ARATHI=`EX1_398`, MS=`EX1_408`, REAPER=`CS2_112`,
CMDR=`EX1_067`, GORE=`EX1_411`, GROM=`EX1_414`.

**Mulligan**
- KEEP: `NEW1_023`, `EX1_393`, `NEW1_018`, `EX1_604`, first copy of `CS2_106`.
- KEEP `EX1_603` if hand has another card with cost 2–3 that is a minion or `CS2_106`.
- KEEP `EX1_556` if no other 3-cost card kept.
- If going second (4-card hand): KEEP one of `NEW1_011` / `EX1_398` if any other keep exists.
- REPLACE everything else (`CS2_105`, `CS2_108`, `EX1_408`, `CS2_112`, `EX1_067`, `EX1_411`, `EX1_414`, `EX1_409`, 2nd `CS2_106`).

**Turn order**
1. Lethal check (§10). If lethal: play Charge minions / weapon / HS / MS, attack hero with everything, MS to face.
2. If an enemy Taunt exists and lethal is otherwise possible: remove Taunt (EXEC if damaged, else cheapest killer), re-check.
3. Equip a weapon before playing `NEW1_018` (same turn when mana allows).
4. Play `EX1_603` before attacks; target per priority below.
5. Attacks: trades per §8, then face.
6. Spend remaining mana: maximise mana used; tie-break by priority list below.
7. Hero power if ≥ 2 mana left. 8. `end_turn`.

**Play priority by turn (mana available)**
- T1: `EX1_409` (no weapon) → attack.
- T2: `NEW1_023` > `EX1_393` > `NEW1_018` > `EX1_603` (only with a valid target).
- T3: `CS2_106` if an enemy minion with Health ≤ 3 exists, else `EX1_604` > `EX1_556` > `CS2_106` > two 1–2 drops.
- T4: `NEW1_011` if it can kill a minion and survive or opp ≤ 15; else `EX1_398` > 2-drop+2-drop > `CS2_106`+`EX1_409`.
- T5: weapon-then-`NEW1_018`; else `CS2_112`; else 4-drop + 1.
- T6: `EX1_067`; else 4-drop + 2-drop.
- T7: `EX1_411` if ≥ 2 enemy minions with Health ≤ 7, else best mana-fill.
- T8+: `EX1_414` (+ `EX1_603` on Grom when 10 mana) else best mana-fill.

**Targeting**
- `EX1_603`: enemy minion with Health 1 > enemy minion we Execute this turn > own `EX1_393` / `EX1_604` / `EX1_414` that can attack
  this turn and has Health ≥ 2 > highest-Attack enemy minion.
- `CS2_108`: damaged enemy Taunt blocking us > highest-cost damaged enemy minion (cost ≥ 4) > never on cost ≤ 2 unless it is a Taunt.
- `EX1_408`: enemy hero if it brings lethal or enemy Health ≤ 8; else enemy minion with Attack ≥ 5 only if our Health ≤ 12; else hold.
- Weapon attacks: Taunt > minion it kills where (minion Attack < our Health − 8) > hero.
- `EX1_411`: attack minions with Health ≤ current weapon Attack, highest Attack first; attack hero last.

**Never**
- Never give `target` to `CS2_105`, `CS2_106`, `CS2_112`, `EX1_411`, `EX1_409`, Armor Up — they list no targets.
- Never play `NEW1_018` with no weapon if a weapon is playable first this turn.
- Never play a weapon while the current one has durability left and has not attacked this turn (exception: `EX1_409` buffs, not replaces).
- Never `CS2_105` unless it kills a minion we need dead or is part of lethal.
- Never attack with the hero into a minion with Attack ≥ our Health.
- Never put more than 3 minions on board vs Mage at 7+ mana when already ahead on board.

**Face vs trade thresholds**
- Go all face if: lethal, or enemy has no minions, or (enemy Health ≤ 12 and our board Attack ≥ enemy board Attack).
- Trade if: our attacker survives and kills, or the target is in the must-kill list (§8.4), or enemy board Attack ≥ our Health / 2.

## 14. Sources

- HearthstoneTopDecks, "Aggro Weapon Warrior" (Season 2, 2014): https://www.hearthstonetopdecks.com/decks/aggro-weapon-warrior/ —
  base weapon list (Upgrade!, Axe, Heroic Strike, Frothing, Weaponsmith, Kor'kron, Mortal Strike, Reaper, Gorehowl, Raider, Faerie Dragon, Commander).
- HearthstoneTopDecks, "Reynad's Deck Wars Aggro Warrior" (Aug 2014): https://www.hearthstonetopdecks.com/decks/reynads-deck-wars-aggro-warrior/ —
  tournament version; confirmed the core and Faerie Dragon/Raider/Commander package.
- HearthstoneTopDecks, "Best Hearthstone Classic decks for every class": https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/ —
  Reynad aggro list (Harvest Golem, Nightblade), Control Warrior list, aggro needs reach vs decks that clear early boards.
- GosuGamers, "Going legend on a budget: the aggro Warrior guide": https://gosugamers.net/hearthstone/features/37700-going-legend-on-a-budget-the-aggro-warrior-guide —
  mulligan (keep Axe, don't keep Heroic Strike), card roles, mix face with board control, keep board vs taunts, per-class matchups.
- GosuGamers, Freohr's Tempo Warrior guide: https://www.gosugamers.net/hearthstone/news/39055-hearthstone-deck-guide-in-depth-guide-to-tempo-warrior-by-freohr —
  tempo-vs-aggro framing, Kor'kron as the best 4-drop, Frothing as fastest win condition, don't overextend into AoE, use Execute for tempo.
- HearthPwn, "Arms Warrior (Aggro)": https://www.hearthpwn.com/decks/184232-arms-warrior-aggro — use weapons on Taunts, Mortal Strike at ≤ 12 Health, deck fades after turn 8–9.
- HearthPwn, "Aggro Warrior" (Naxx era): https://www.hearthpwn.com/decks/121659-aggro-warrior — mulligan for Axe + cheap minions, Reaper's multiple charges, save Mortal Strike for lethal through Taunts.
- hearthstone.wiki.gg, Fiery War Axe: https://hearthstone.wiki.gg/wiki/Fiery_War_Axe — cost history (2 → 3 in Sep 2017; our pool uses 3).
- Project `meta.md` §2 (current card text) and §3.4 (Greedy Mage list and behaviour).
