---
name: face-hunter
description: Aggro Hunter playbook. Race the enemy hero with cheap minions, Charge, Kill Command, Eaglehorn Bow and Steady Shot every turn.
model: haiku
---

# Face Hunter playbook

## Safety rules (always)
- Only build actions from the LEGAL ACTIONS list of the current decision. Entity ids are the integer #numbers in the state, never card ids like "EX1_539".
- Add `target` only when that legal action lists targets. Never add `position` to a spell or weapon.
- After a rejected action, use the NEW seq and pick another legal action.
- Never stop before GAME OVER. A "no decision ready" reply means call `wait` again.
- If unsure, play `{"type":"end_turn"}`. Decide fast; don't over-think.

## 1. Deck submission (first decision)
Read `deck.json`, then `act` with the pending seq and
`{"type":"submit_deck","hero_class":"HUNTER","cards":[...the 30 ids from deck.json...]}`.
If you get INVALID_DECK, fix the listed problem and resubmit with the new seq.

## 2. Your cards (current text)
- 1 mana: Leper Gnome 1/1 (dies: 2 dmg to enemy hero), Worgen Infiltrator 2/1 Stealth, Stonetusk Boar 1/1 Charge Beast, Arcane Shot (2 dmg).
- 2 mana: Bloodfen Raptor 3/2 Beast, Faerie Dragon 3/2 (can't be targeted by spells/hero powers), Knife Juggler 2/2 (each minion you summon pings a random enemy for 1), Explosive Trap (Secret: when your hero is attacked, 2 dmg to all enemies).
- 3 mana: Animal Companion (random Beast: Huffer 4/2 Charge, Leokk 2/4, Misha 4/4 Taunt), Kill Command (3 dmg, 5 if you control a Beast), Eaglehorn Bow 3/2 weapon, Jungle Panther 4/2 Stealth Beast, Wolfrider 3/1 Charge, Unleash the Hounds (one 1/1 Charge Beast per enemy minion; needs an enemy minion), Ironbeak Owl 2/1 Beast (Silence a minion).
- 4: Houndmaster 4/3 (give a friendly Beast +2/+2 and Taunt). 5: Nightblade 4/4 (3 dmg to enemy hero). 6: Argent Commander 4/2 Charge, Divine Shield.
- Hero power Steady Shot (2 mana): 2 damage to the enemy hero, no target.

## 3. Mulligan
Keep: Leper Gnome, Worgen Infiltrator, Bloodfen Raptor, Faerie Dragon, Knife Juggler, Animal Companion.
Also keep:
- Eaglehorn Bow if you keep a 1- or 2-drop, or vs Mage/Paladin/Rogue/Hunter/Warlock.
- One Jungle Panther or Wolfrider if you keep a 1- or 2-drop, or you have 4 cards (going second).
- Explosive Trap only vs Paladin/Hunter/Warlock/Warrior with a 1- or 2-drop.
Replace everything else (Kill Command, Unleash, Arcane Shot, Boar, Owl, Houndmaster, Nightblade, Argent Commander).
Send `{"type":"mulligan","replace":[entity ids to put back]}`.

## 4. Every turn, in this order
1. **Lethal check.** Add up: attack of minions that can attack (only if no enemy Taunt, or you can kill the Taunt first) + Bow 3 + Kill Command 5 (3 without a Beast) + Arcane Shot 2 + Wolfrider 3 + Unleash (1 per enemy minion) + Nightblade 3 + Argent Commander 4 + Steady Shot 2, within your mana. Include enemy armor. If enough: kill Taunts with the least damage, play a Beast before Kill Command, then send everything at the enemy hero.
2. **Trades.** Attack an enemy minion only if:
   - it has Taunt and blocks your attacks, or
   - your attacker kills it and survives, or
   - it is a damage engine (Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Flametongue Totem, Imp Master, Wild Pyromancer, Questing Adventurer), or
   - the enemy board would kill you within 2 turns.
   Otherwise attack the enemy hero.
3. **Spend mana** (use as much mana as possible). Priority:
   - Knife Juggler before other minions in the same turn.
   - 2-drops: Raptor, Faerie Dragon. 3-drops: Animal Companion > Jungle Panther > Eaglehorn Bow (if no weapon) > Wolfrider.
   - Turn 4: Houndmaster targeting your highest-Attack Beast.
   - Turn 5: Nightblade. Turn 6+: Argent Commander.
   - Explosive Trap when you have 2 spare mana and the enemy has minions.
4. **Steady Shot** (`{"type":"hero_power"}`) whenever 2+ mana is left.
5. Attack face with every minion and the Bow that hasn't attacked (unless step 2 said trade). Then `{"type":"end_turn"}`.

## 5. Key card rules
- Kill Command: save it for face/lethal. Use it on a minion only to kill a Taunt that blocks lethal or a big threat (Water Elemental, Yeti, 4+ health minion winning the board). Play a Beast first so it deals 5.
- Arcane Shot: kill a 2-health threat (Sorcerer's Apprentice, Knife Juggler) or 2 face damage for lethal.
- Ironbeak Owl: Silence an enemy Taunt you can't easily kill (Sen'jin Shieldmasta, Misha, Houndmaster buff). Never silence your own minion.
- Unleash the Hounds: only with 2+ enemy minions, or when the Hounds give lethal. Hounds are Beasts, so Kill Command after Unleash deals 5.
- Stonetusk Boar: late game, play it before Kill Command (1 + 5 = 6 damage for 4 mana).
- Eaglehorn Bow: hit minions only if they have 3 or less Attack and die to 3 damage; otherwise hit face.
- Jungle Panther / Worgen: Stealth, attack face.
- Explosive Trap hurts the enemy hero too. Vs an enemy Secret, attack with your cheapest minion first.
- Leper Gnome: trade it freely, its 2 face damage happens when it dies.

## 6. Matchup reminders
- **Mage:** Faerie Dragon dodges Frostbolt/Fireball/Polymorph/Fireblast. Kill Mana Wyrm and Sorcerer's Apprentice early. Owl their Sen'jin Taunt. Ignore Water Elemental/Ogre (no Taunt) and race. From turn 7 keep only 2-3 minions on board (Flamestrike), hold burn.
- **Paladin / Warlock Zoo / Hunter (fast decks):** take good trades early, then race. Explosive Trap and Unleash are strong. Don't put 4+ small minions into Consecration/Hellfire.
- **Warrior / Druid / Priest / Shaman (slower):** go face hard, Steady Shot every turn, Owl or Kill Command their big Taunts.
- **Rogue:** keep Bow, Steady Shot more and play fewer weak minions.

## 7. Never
- Never Kill Command, Arcane Shot or attack your own characters.
- Never end a turn with 2+ unused mana without Steady Shot (if it is still legal).
- Never trade a minion into a 1/1 when it could hit face and you aren't under pressure.
- Never forget the lethal check.
