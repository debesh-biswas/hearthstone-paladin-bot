# Aggro Paladin ("Shockadin" adapted to Midrange-Aggro): Deck Guide

Pool: hs-arena `basic-classic-1` (modern Legacy Basic + Classic, nerfs applied, Hall of Fame removed).
Every card text below was checked against `meta.md` §2 / `hs_arena.cards`. Do not trust remembered 2014 text.

---

## 1. Overview and win condition

The 2014 Shockadin was a hyper-aggressive list: a pile of 1-drops (Leper Gnome, Argent Squire, Worgen Infiltrator,
Abusive Sergeant, Elven Archer), Blessing of Might, Knife Juggler, Arcane Golem, Wolfrider, Leeroy Jenkins, refuelled by
**Divine Favor**, with Equality + Consecration as a cheap board clear and Avenging Wrath / Hammer of Wrath as reach.

In this pool the engine is broken:

- **Divine Favor and Leeroy Jenkins are removed** (Hall of Fame). There is no cheap refill and no 6-damage Charge finisher.
- **Leper Gnome is 1/1, Knife Juggler 2/2, Arcane Golem is 4/4 with no Charge** (and still ramps the opponent).
- **Equality costs 4, Avenging Wrath costs 6**, so the classic "Equality + Consecration for 6 mana" clear is now 8 mana.

A pure 1-drop rush hand runs out of cards by turn 4–5 and then loses to any 4/5 or Taunt; versus the known
Greedy Mage bot, 1/1s die to Fireblast and Arcane Missiles for free. So this deck is an **aggressive midrange Paladin**:

- Curve out turns 1–4 with sticky or shielded minions (Argent Squire, Argent Protector, Harvest Golem, Aldor Peacekeeper,
  Shattered Sun Cleric), trading efficiently while hitting face whenever the board is safe.
- Win the board with **Truesilver Champion** (4 damage per swing, heals 2), **Consecration**, **Aldor Peacekeeper**.
- Convert the board into damage with **Blessing of Kings / Blessing of Might**, then close with **Argent Commander** (Charge),
  **Hammer of Wrath**, **Consecration** (hits face for 2) and **Avenging Wrath** (8 random damage to enemies).
- Refill replaces Divine Favor: **Hammer of Wrath ×2** (cantrip), **Loot Hoarder ×2**, **Harvest Golem** stickiness, and the
  hero power **Reinforce** (2 mana: summon a 1/1 Silver Hand Recruit) as a mana sink every spare turn.
- **Tirion Fordring** is the single top-end card that wins any game that drags past turn 8.

Win condition: be ahead on board by turn 4–5, then push face; the opponent dies around turns 7–9 from minions + weapon + burn.
Against faster decks we play the control role until they run out of cards, then turn the corner.

### Why not the pure Shockadin build?
| | Pure Shockadin (adapted) | Aggressive Midrange (chosen) |
|---|---|---|
| Refill | none (Divine Favor gone) | Hammer ×2, Loot Hoarder ×2, Tirion, hero power |
| Reach | Blessing of Might, Avenging Wrath 6, Hammer, 1/1 Leper | Commander ×2, Truesilver, Hammer, Consecration, Avenging Wrath |
| vs Greedy Mage | 1/1s die to Fireblast/Missiles; dead hand by turn 5 vs Yeti/Sen'jin | Bodies survive pings; Aldor neutralises Ogre/Yeti/Tiger |
| Pilot complexity | Low, but punishes every misplay with no recovery | Low: few combos, no adjacency, almost no secrets |
Result: midrange-aggro is clearly stronger in this pool and still simple to pilot.

---

## 2. Decklist (30)

| # | Cost | Id | Name | Current text / stats | Role |
|--:|--:|---|---|---|---|
| 2 | 1 | `EX1_008` | Argent Squire | 1/1 Divine Shield | Turn-1 play that survives one ping; Kings/Might target |
| 2 | 1 | `CS2_087` | Blessing of Might | Give a minion +3 Attack | Cheap reach / makes a trade work |
| 2 | 2 | `EX1_362` | Argent Protector | 2/2. Battlecry: give a friendly minion Divine Shield | Free trade enabler |
| 2 | 2 | `NEW1_019` | Knife Juggler | 2/2. After you summon a minion, deal 1 dmg to a random enemy | Pings 1-health minions / face |
| 2 | 2 | `EX1_096` | Loot Hoarder | 2/1. Deathrattle: draw a card | Refill, trades into 1-2 health |
| 1 | 2 | `EX1_066` | Acidic Swamp Ooze | 3/2. Battlecry: destroy opponent's weapon | 3/2 body; tech vs weapon classes |
| 2 | 3 | `EX1_382` | Aldor Peacekeeper | 3/3. Battlecry: change an enemy minion's Attack to 1 | Neutralises their biggest attacker |
| 2 | 3 | `EX1_556` | Harvest Golem | 2/3. Deathrattle: summon a 2/1 Damaged Golem | Sticky vs removal/AoE |
| 2 | 3 | `EX1_019` | Shattered Sun Cleric | 3/2. Battlecry: give a friendly minion +1/+1 | Tempo; wins early trades |
| 2 | 4 | `CS2_097` | Truesilver Champion | Weapon 4/2. When your hero attacks, restore 2 Health to it | Removal + face damage + heal |
| 2 | 4 | `CS2_092` | Blessing of Kings | Give a minion +4/+4 | Biggest tempo swing; snowball |
| 2 | 4 | `CS2_094` | Hammer of Wrath | Deal 3 damage. Draw a card | Removal or 3 face, replaces itself |
| 2 | 4 | `CS2_093` | Consecration | Deal 2 damage to all enemies (incl. hero) | AoE vs tokens; 2 face reach |
| 1 | 4 | `CS2_182` | Chillwind Yeti | 4/5 | Solid turn-4 body |
| 2 | 6 | `EX1_067` | Argent Commander | 4/2 Charge, Divine Shield | Finisher; kills a minion and survives |
| 1 | 6 | `EX1_384` | Avenging Wrath | Deal 8 damage randomly split among all enemies | Reach / clears small boards |
| 1 | 8 | `EX1_383` | Tirion Fordring | 6/6 Divine Shield, Taunt. Deathrattle: equip a 5/3 Ashbringer | Late-game bomb |

Curve: 1-mana ×4, 2-mana ×7, 3-mana ×6, 4-mana ×9, 6-mana ×3, 8-mana ×1.
Hero power: **Reinforce** (2 mana, summon a 1/1 Silver Hand Recruit).

Close cuts (legal alternatives): Blessing of Wisdom `EX1_363` (refill, but needs a minion that survives to attack),
second Yeti, Gnomish Inventor `CS2_147` (4-slot already crowded), Silvermoon Guardian `EX1_023`, Bloodfen Raptor `CS2_172`,
Amani Berserker `EX1_393`, Abusive Sergeant `CS2_188` (1/1 now; weak body), Equality `EX1_619` (4 mana, combo with
Consecration costs 8, too slow for this plan), Defender of Argus `EX1_093` (positional; avoided for a simple pilot),
Sunwalker `EX1_032`, Stormwind Champion `CS2_222`. Where two cards were close, the one with no positioning/combo decision won.

---

## 3. How the nerfs changed the deck vs the classic version

| Classic card / advice | Status here | Adjustment |
|---|---|---|
| Divine Favor ("most important card", draws 5+ vs Mage) | **Removed** | Replace with Hammer ×2, Loot Hoarder ×2, Tirion; do not dump the hand blindly |
| Leeroy Jenkins (+Blessing of Might = 9 burst) | **Removed** | Burst now comes from Argent Commander (4 Charge) + Blessings on existing minions |
| Leper Gnome ("usually 4+ damage") | 1/1 (was 2/1) | Cut: dies to every ping, at most 1 attack + 2 damage |
| Knife Juggler | 2/2 (was 3/2) | Still played: Reinforce and every minion trigger it, but it is a weaker body |
| Arcane Golem (Charge reach in Rush Paladin) | 4/4 no Charge, still gives opponent a crystal | Cut: pure downside |
| Equality + Consecration "6 mana clear" | Equality 4 → combo is 8 mana | Cut Equality; Consecration alone vs tokens; Aldor/Truesilver for big minions |
| Avenging Wrath at 5 mana | **6 mana** | Only one copy; used as finisher or vs 2-3 small minions |
| Wolfrider / Bluegill as reach | Still legal but 3/1 & 2/1 bodies trade badly | Cut in favour of Argent Commander |
| Big Game Hunter (classic tech) | 5 mana | Not needed: Aldor Peacekeeper answers big minions for 3 |
| Mage's Ice Lance / Ice Block (freeze tricks vs Paladin) | Removed | Mage reach is lower; racing Mage is safer than in 2014 |
| Mage's Flamestrike | 7 mana | Still the main threat to a wide board from turn 7 |

---

## 4. Mulligan

General rule: keep cards that let us make a play on turns 1–3. Throw away 4+ cost cards unless noted.

**Always keep:** Argent Squire `EX1_008`, Argent Protector `EX1_362`, Knife Juggler `NEW1_019`, Loot Hoarder `EX1_096`,
Acidic Swamp Ooze `EX1_066`, Harvest Golem `EX1_556`, Aldor Peacekeeper `EX1_382`, Shattered Sun Cleric `EX1_019`.

**Conditional keeps:**
- Truesilver Champion `CS2_097`: keep if going second (Coin), or if the hand already has at least one 2-drop and one 3-drop.
- Chillwind Yeti `CS2_182`: keep only going second with a 2- or 3-drop already in hand.
- Blessing of Might `CS2_087`: keep only with a 1- or 2-drop minion also kept (otherwise it is dead).
- Consecration `CS2_093`: keep only vs a known token/aggro deck (rare: opponent class is hidden at mulligan time, so normally toss).
- Do not keep two 3-drops and nothing cheaper going first; toss one 3-drop to dig for a 1/2-drop.

**Always toss:** Blessing of Kings `CS2_092`, Hammer of Wrath `CS2_094`, Avenging Wrath `EX1_384`, Argent Commander `EX1_067`,
Tirion Fordring `EX1_383`, Consecration (default).

Going first (3 cards): aim for a 1- or 2-drop plus a 3-drop. Going second (4 cards + Coin): the Coin allows a turn-1 2-drop
or a turn-3 Truesilver/Yeti, so the 4-drop conditional keeps above apply.

---

## 5. Turn-by-turn plan (ideal curve)

| Turn | Ideal play | Fallback |
|---|---|---|
| 1 | Argent Squire | Nothing (do not Blessing an empty board). With Coin: a 2-drop |
| 2 | Knife Juggler / Argent Protector (shield the Squire or best minion) / Loot Hoarder / Ooze | Reinforce (hero power) |
| 3 | Aldor Peacekeeper (if enemy minion with Attack ≥3), else Harvest Golem / Shattered Sun Cleric on the best minion | 2-drop + 1-drop; or 2-drop + nothing |
| 4 | Truesilver Champion + attack; or Blessing of Kings on a minion that can attack now; or Yeti | Hammer of Wrath on a key minion; Consecration vs 2+ small minions |
| 5 | 4-drop + 1-drop; or 3-drop + Reinforce; Hammer + Blessing of Might | Two 2/3-drops |
| 6 | Argent Commander (attack immediately); or Avenging Wrath when it kills 2+ things or gives lethal | Truesilver + Reinforce |
| 7 | 6-drop + 1-drop; Kings + 3-drop | Hammer + 3-drop |
| 8+ | Tirion; or combine burn for lethal | Spend all mana; Reinforce with leftovers |

Mana rule: every turn spend as much mana as possible; Reinforce (2) is the default use of 2 spare mana.

---

## 6. Card-by-card notes

- **Argent Squire**: best turn-1 play. Its shield eats a Fireblast, Arcane Missile or Frostbolt. Good Kings target
  because the shield survives the next trade.
- **Blessing of Might**: +3 Attack permanently. Use (a) to let a minion kill something bigger this turn, (b) for lethal,
  (c) on a Divine Shield minion so it trades without dying. Do not cast it on a minion that cannot attack this turn unless mana would be wasted and the board is safe.
- **Argent Protector**: give the shield to the minion that will trade next (or the one most likely to be targeted, e.g. a
  Blessed minion). If it is the only minion, the battlecry has no target and it is just a 2/2.
- **Knife Juggler**: play it BEFORE other minions or Reinforce on the same turn so they trigger it. Each trigger hits a random
  enemy (minion or hero). Great vs 1-health tokens (Mirror Image 0/2 not killed, Imps/Whelps/Recruits killed).
- **Loot Hoarder**: trade it freely into 1–2 health minions; its death draws a card. Never hold it back "for value".
- **Acidic Swamp Ooze**: if the opponent has a weapon, play it now (huge vs Warrior/Rogue/Paladin/Hunter/Shaman). Otherwise just a 3/2 on turn 2.
- **Aldor Peacekeeper**: target the enemy minion with the HIGHEST Attack (ideally ≥4: Yeti, Water Elemental 3/6 is borderline,
  Boulderfist Ogre 6/7, Stranglethorn Tiger once revealed, Argent Commander, Core Hound). A 1-attack minion can be ignored or
  traded into by our 2/x minions. If no enemy minion exists, the battlecry fizzles; then play it as a 3/3 only if nothing better.
- **Harvest Golem**: sticky turn-3; trade it first because it leaves a 2/1.
- **Shattered Sun Cleric**: buff a minion that is about to trade (turns 2/2 into 3/3 to beat a 2/x) or a Divine Shield minion.
  Needs another friendly minion to target; otherwise a 3/2.
- **Truesilver Champion**: 2 swings of 4 damage, each heals our hero 2. Use it on minions with ≤4 Health whose Attack is low
  enough that we don't lose much health (Truesilver heal offsets 2). Excellent vs Sorcerer's Apprentice, Mana Wyrm, Yeti (with a
  minion hit first), Sen'jin (3 dmg to us). If no good target, hit face. Do not replace a weapon that still has charges.
- **Blessing of Kings**: on a minion that can attack THIS turn (tempo) or on a Divine Shield minion. Avoid playing it into an
  open Polymorph/Hex/Fireball turn when another option exists, but do not hold it forever: tempo > fear.
- **Hammer of Wrath**: 3 damage + draw. Kill a 3-health threat (Apprentice, Mana Wyrm, Water Elemental after a hit, Knife Juggler,
  Raid Leader, Dire Wolf) or go face for lethal. Cast early in the turn when it is only for value (the draw may change the plan).
- **Consecration**: deals 2 to all enemies including the hero. Cast when it kills 2+ enemy minions, or kills a minion and enables
  our trades, or completes lethal. Divine Shields on enemy minions absorb it.
- **Chillwind Yeti**: plain 4/5; on curve when nothing better.
- **Argent Commander**: Charge + Divine Shield: it can attack a minion the turn it lands and survive (shield), then threaten 4 more.
  Or 4 face for lethal.
- **Avenging Wrath**: 8 random damage split among enemy hero + minions. Best when the enemy board is empty/small (all 8 face) or
  has 1-2 small minions. Finisher when the enemy hero has ≤8 health and no minions.
- **Tirion Fordring**: drop when mana allows; Taunt + shield protects our board and his death gives a 5/3 weapon.
- **Reinforce (hero power)**: 2 mana, 1/1 Recruit. Use whenever 2 mana is left after cards. Triggers Knife Juggler. Recruits are
  Blessing targets late.

---

## 7. Combos, synergies and positioning

- **Divine Shield + buff**: Squire/Protector-shielded minion + Blessing of Kings or Might = a minion that trades twice.
- **Knife Juggler + Reinforce / any minion**: each summon is a free ping; play Juggler first.
- **Shattered Sun Cleric / Argent Protector** need a friendly minion already on board; play them after another minion.
- **Truesilver + minion trades**: attack the enemy minion with our minions first to weaken it, then finish with the weapon
  (or vice-versa) to keep our minions alive.
- **Burn turn**: Hammer (3) + Consecration (2) + Truesilver (4) + Commander (4) + Avenging Wrath (up to 8) is our reach.
- Positioning does not matter for this list (no adjacency cards). Default rightmost placement is fine.

---

## 8. Trading rules (trade vs face)

1. Always kill an enemy Taunt that blocks lethal.
2. Kill enemy minions that would deal big damage or snowball: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Flametongue,
   Raid Leader, Dire Wolf Alpha, Imp Master, Questing Adventurer, Violet Teacher, Cult Master, Gadgetzan Auctioneer,
   anything with Attack ≥ 4 that we can kill efficiently.
3. Make a trade if our attacker kills the enemy minion and survives (or has Divine Shield), or if we trade a cheaper/equal
   card for a more expensive one (e.g. Loot Hoarder into a 3-drop).
4. If the enemy board can deal ≥ half our remaining health next turn, prioritise trades over face (we are the control deck now).
5. Otherwise hit face. Against slow decks (Greedy Mage, Control Warrior, Ramp Druid, Priest) default to face once the board is ours.
6. Do not attack into a minion that kills our attacker without dying unless it removes a lethal threat.
7. Weapon: use Truesilver on minions mainly when it doesn't cost more than ~4 of our health; otherwise face.

---

## 9. Hero power rules

- Use Reinforce whenever ≥2 mana remains after the best card plays (it is better than wasting mana).
- On turn 2 with no 2-drop: Reinforce.
- Prefer spending mana on cards first; Reinforce last, except with Knife Juggler on board play Juggler first then Reinforce.
- With 7 board slots full, Reinforce is impossible.

---

## 10. Lethal checklist

Compute each turn before anything else:
- Sum of Attack of our minions that can attack (not frozen, not summoning sick, Argent Commander has Charge)
- + weapon Attack (Truesilver 4) if hero can attack, or + 4 if we can equip Truesilver this turn
- + Hammer of Wrath 3 (4 mana) + Consecration 2 (4 mana) + Blessing of Might +3 on an attacker (1 mana)
- + Blessing of Kings +4 on an attacker (4 mana) + Argent Commander 4 (6 mana)
- + Avenging Wrath: 8 only if the enemy has no minions (otherwise unreliable)
- − enemy armor; Taunts must be removed first (Hammer/Consecration/weapon/minions on the Taunt)
If total ≥ enemy health + armor within available mana: go face with everything (spells to face, attack face).

---

## 11. Matchups

**Greedy Mage (known bot: Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Thalnos, Harvest Golem,
Yeti, Water Elemental, Fireball, Polymorph, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike).**
- It plays one greedy action at a time with no lethal planning; it is a midrange value deck. We are the beatdown.
- Early: kill Mana Wyrm and Sorcerer's Apprentice immediately (Truesilver, Hammer, trades). Divine Shield minions blunt Fireblast and Missiles.
- Mid: Aldor Peacekeeper on Boulderfist Ogre / Yeti / Stranglethorn Tiger / Water Elemental (Water Elemental freezes what it
  damages: Aldor it or kill it rather than trade into it with important minions). Sen'jin 3/5 Taunt must be cleared to go face: Aldor it (becomes 1/5) and then trade into it freely, or Truesilver + a minion.
- Polymorph will hit our Blessing of Kings target: prefer Kings on a minion that attacks immediately, gaining value at once.
- Flamestrike (7 mana, 4 to all our minions): from turn 7, do not add extra minions if we already have lethal pressure; keep 1-2 in hand.
  Harvest Golem and Divine Shield minions survive better.
- Argent Commander of theirs (4/2 shield, charge): pop the shield with a Recruit or Juggler ping then kill it.
- Try to finish by turn 8-9 before Boulderfist Ogres stack. Consecration often hits face for the last 2.

**Hunter (Midrange/Face)**: contest the board early; Steady Shot deals 2 every turn so race carefully. Kill Knife Juggler, Houndmaster
targets, Scavenging Hyena. Consecration vs Unleash the Hounds (3 mana now) tokens. Ooze on Eaglehorn Bow/Gladiator's Longbow. Keep health
above Kill Command range when ahead. Tirion is a wall.

**Paladin mirror**: board control and Aldor on Blessed/Tirion. Ooze their Truesilver. Consecration hurts both; shields matter.

**Warrior (Aggro/Control)**: Ooze on Fiery War Axe (3 mana) / Arcanite Reaper / Gorehowl. Vs Control: go face, avoid overextending
into Brawl (keep 2 minions in hand). Execute targets damaged minions: Kings on full-health minions.

**Shaman**: Ooze on Doomhammer. Aldor on Fire Elemental/Al'Akir. Lightning Storm (3 mana now) kills 2-3-health boards: Harvest Golem and
shields help. Kill Flametongue Totem and Mana Tide.

**Rogue**: Ooze on Assassin's Blade/daggers (huge value: Rogue hero power daggers). Blade Flurry (4, minions only) punishes wide boards.
Kill Edwin VanCleef / Questing Adventurer immediately. Truesilver heal helps vs their weapon damage.

**Druid (Ramp/Token)**: be the beatdown before big Ancients. Aldor on Druid of the Claw/Ancient of War/Ironbark. Consecration vs Force of
Nature treants (no Charge anymore). Savage Roar is the burst; keep board advantage.

**Warlock (Zoo)**: Consecration is key (most Zoo minions have ≤2 health). Trade, don't race early; Kill Knife Juggler, Dire Wolf, Imp Master.
Then turn the corner with Commander/Kings. Vs Handlock-like (giants gone): race.

**Priest**: slow; go face; Kings minions are Shadow Word: Death/Pain targets but keep pressing. Avoid stacking all buffs on one minion vs Mind Control (10 mana).

---

## 12. Common mistakes

- Casting Blessing of Might/Kings on a minion that cannot attack this turn when an attacking minion was available.
- Playing Shattered Sun Cleric or Argent Protector first on an empty board (battlecry wasted).
- Playing minions before Knife Juggler on the same turn.
- Hitting face while the enemy board threatens lethal or snowballs (Mana Wyrm, Apprentice).
- Using Avenging Wrath into a big board (8 damage gets split badly) instead of Consecration/trades.
- Not using Reinforce with 2+ spare mana.
- Dumping every minion into a 7-mana Mage turn (Flamestrike) when already winning.
- Forgetting Consecration and Avenging Wrath also hit the enemy hero (lethal math).
- Holding Hammer of Wrath "for value" instead of cycling it on a decent target.
- Attacking with the hero into a high-Attack minion with Truesilver when the damage taken is greater than the value.

---

## 13. Script hints (rule-based bot)

Card ids: SQUIRE=`EX1_008` MIGHT=`CS2_087` PROTECTOR=`EX1_362` JUGGLER=`NEW1_019` LOOT=`EX1_096` OOZE=`EX1_066` ALDOR=`EX1_382`
GOLEM=`EX1_556` CLERIC=`EX1_019` TRUESILVER=`CS2_097` KINGS=`CS2_092` HAMMER=`CS2_094` CONSEC=`CS2_093` YETI=`CS2_182`
COMMANDER=`EX1_067` WRATH=`EX1_384` TIRION=`EX1_383`.

**Mulligan**
- KEEP = {EX1_008, EX1_362, NEW1_019, EX1_096, EX1_066, EX1_556, EX1_382, EX1_019}.
- KEEP CS2_097 if hand_size==4 (going second) OR (hand has a 2-cost minion AND a 3-cost minion).
- KEEP CS2_182 if going second AND hand has a ≤3-cost minion.
- KEEP CS2_087 only if another kept card is a minion costing ≤2.
- If going first and kept 3-drops ≥2 with no ≤2-cost minion: replace one 3-drop.
- REPLACE everything else.

**Turn order (each step loops until nothing applies)**
1. LETHAL: if (ready_attack_sum + weapon + burn_available_within_mana) ≥ enemy_hp + armor and Taunts can be removed → spells to face,
   all attacks face (clear Taunts first with the cheapest sufficient source).
2. OOZE first if enemy has a weapon (EX1_066).
3. HAMMER (CS2_094) for value early in the turn if a target with Health ≤3 and Attack ≥3 or a priority engine exists.
4. Minions in order: JUGGLER first, then other minions; CLERIC/PROTECTOR only if a friendly minion exists (target: best attacker; for
   PROTECTOR prefer a minion without Divine Shield with highest Attack).
5. ALDOR target = enemy minion with max Attack (only if that Attack ≥3; else prefer another card).
6. Buffs: KINGS/MIGHT only on a friendly minion that can attack this turn (prefer Divine Shield, then highest Health); else if no other
   use of mana, on highest-Health minion.
7. Attacks: for each enemy minion in priority (Taunt blocking, Attack≥4 or engine id list, then highest Attack), find the cheapest
   attacker that kills it and survives (Divine Shield counts as surviving). Else face.
8. TRUESILVER (CS2_097): equip if no weapon or current weapon has 0 durability left; hero attacks target per rule 7 if
   (enemy_attack ≤ 4 and enemy_health ≤ 4), else face.
9. CONSEC (CS2_093) if kills ≥2 enemy minions, or kills 1 and enemy hero ≤2 + other lethal, or lethal.
10. WRATH (EX1_384) if enemy has 0 minions and hp ≤ 8 + other damage, or if enemy minions all have Health ≤2 and count ≤3.
11. COMMANDER (EX1_067): play and attack immediately (minion target per rule 7 if a good trade, else face).
12. TIRION when mana ≥8.
13. HERO POWER if mana ≥2 and board < 7.
14. end_turn.

**Never**
- Never cast MIGHT/KINGS/CLERIC/PROTECTOR without a friendly minion target.
- Never target our own minions with HAMMER or ALDOR (Aldor only targets enemies anyway).
- Never re-equip TRUESILVER over a weapon with durability left.
- Never cast CONSEC when it kills nothing unless it is lethal.
- Never use WRATH into ≥4 enemy minions unless lethal is possible only that way.
- Never attack face when enemy board Attack sum ≥ our hero hp − 4 and a trade exists.

**Face-vs-trade thresholds**
- Face if (our board Attack ≥ enemy board Attack + 3) and no enemy engine minion alive.
- Trade if enemy board Attack ≥ our hp / 2.
- Opponent hero hp ≤ 10: favour face/burn; hp ≤ our total reach: lethal mode.

---

## 14. Sources

- https://www.tentonhammer.com/guides/deck-of-the-week-3-paladin-shockadin-deck: classic 2014 Shockadin core cards, game plan
  (race, avoid trades, finish before turn 7), mulligan (no 4+ costs, toss buffs without minions), Equality+Consecration combo,
  Leeroy+Blessing combo, Divine Favor as engine, common mistakes and the "wins by turn 7 / loses after turn 10" profile. Adjusted
  for the nerfs (Divine Favor/Leeroy gone, Leper 1/1, Equality 4, Avenging Wrath 6).
- https://www.hearthstonetopdecks.com/decks/shockadin-classic-legacy/: Classic+ Shockadin list (Light's Justice, Southsea, Worgen,
  Knife Juggler, Arcane Golem, King Mukla, Black Knight) and mulligan priorities vs aggro/control.
- https://www.hearthstonetopdecks.com/decks/classic-aggro-paladin-shockadin/: 2021 Classic-format Shockadin list (Abusive,
  Elven Archer, Leper Gnome, Equality ×2, Divine Favor ×2, Avenging Wrath ×2, Leeroy) used to identify cards that do not survive here.
- https://www.hearthstonetopdecks.com/decks/midrange-paladin-deck-list/: Midrange Paladin plan (board control, Equality +
  Consecration, Aldor for tempo vs big minions, Truesilver keep on the Coin, Tirion as finisher), mulligan logic.
- https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki:Archived/Aggro_Paladin: archetype definition (swarm + buffs), Divine Favor's
  loss weakening the deck, list of core/optional classic cards (Blessing of Might/Kings, Truesilver, Avenging Wrath, Tirion, Knife Juggler).
- https://hearthstone.wiki.gg/wiki/Midrange_Paladin: midrange approach (early board, snowball with Aldor/Equality, Truesilver and
  Consecration as mid-game tools, Tirion top end).
- https://icy-veins.com/hearthstone/classic-aggro-paladin-deck (search-result summary; page blocks fetching): Shockadin definition
  as Charge minions + weapons + attack buffs with Divine Favor refill.
- https://articles.hsreplay.net/2019/04/15/the-art-of-mulligan/: mulligan principles (keeps depend on Coin/turn order and opponent;
  keep early board contesters vs aggro).
- `meta.md` §2–3 (project): current card text/costs, Hall of Fame list, Greedy Mage decklist and behaviour.
