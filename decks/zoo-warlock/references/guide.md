# Zoo Warlock (Zoolock): guide for the hs-arena Basic + Classic Legacy pool

## 1. Overview and win condition

Zoo is a board-control aggro deck. It plays two or three cheap, efficient minions in the first turns and takes
the board. Every turn it trades its small minions into the enemy's minions on favourable terms, helped by
temporary and permanent buffs (Abusive Sergeant, Dark Iron Dwarf, Dire Wolf Alpha, Shattered Sun Cleric,
Defender of Argus). Life Tap (2 mana: draw a card, take 2 damage) refills the hand, so Zoo never runs out of
threats the way a pure face deck does.

**Win condition:** keep more minions on the board than the opponent from turn 1 to turn 6. Chip damage builds
up while the opponent is busy dealing with the board. Finish with a wide attack, buffed attackers, Soulfire,
Nightblade's battlecry and Argent Commander's Charge. Sea Giant (cheap on a crowded board) and Frostwolf
Warlord (big on a wide board) are the late-game reloads that replace Doomguard.

**How it loses:** to board clears (Flamestrike, Consecration, Hellfire, Lightning Storm, Blizzard, Holy Nova,
Swipe-style splash, Whirlwind effects), to big taunts it cannot get through, and to its own self-damage
(Flame Imp, Life Tap) against burn decks.

## 2. Decklist (30)

| # | Cost | Id | Name | Stats | Current text | Role |
|--:|--:|---|---|---|---|---|
| 2 | 1 | `EX1_319` | Flame Imp | 3/2 | Battlecry: Deal 3 damage to your hero. | Best 1-drop; trades with most 2-drops |
| 2 | 1 | `CS2_065` | Voidwalker | 1/3 | Taunt | Defensive 1-drop, protects Juggler/Dire Wolf, Argus target |
| 2 | 1 | `CS2_188` | Abusive Sergeant | 1/1 | Battlecry: Give a minion +2 Attack this turn. | Trade enabler, burst |
| 2 | 1 | `EX1_008` | Argent Squire | 1/1 | Divine Shield | Sticky 1-drop, best buff target |
| 2 | 1 | `EX1_308` | Soulfire | spell | Deal 4 damage. Discard a random card. | Removal or 4 face reach |
| 2 | 2 | `NEW1_019` | Knife Juggler | 2/2 | After you summon a minion, deal 1 damage to a random enemy. | Pings off every later minion |
| 2 | 2 | `EX1_162` | Dire Wolf Alpha | 2/2 | Adjacent minions have +1 Attack. | Positional buff for trades |
| 2 | 2 | `EX1_393` | Amani Berserker | 2/3 | Has +3 Attack while damaged. | Becomes 5/3 after its first trade |
| 1 | 2 | `EX1_096` | Loot Hoarder | 2/1 | Deathrattle: Draw a card. | Trades and replaces itself |
| 2 | 3 | `EX1_556` | Harvest Golem | 2/3 | Deathrattle: Summon a 2/1 Damaged Golem. | Sticky vs AoE and removal |
| 2 | 3 | `EX1_019` | Shattered Sun Cleric | 3/2 | Battlecry: Give a friendly minion +1/+1. | Permanent buff, tempo |
| 2 | 4 | `EX1_093` | Defender of Argus | 2/3 | Battlecry: Give adjacent minions +1/+1 and Taunt. | Two buffs and a wall |
| 2 | 4 | `EX1_046` | Dark Iron Dwarf | 4/4 | Battlecry: Give a minion +2 Attack this turn. | Body plus trade/burst buff |
| 1 | 5 | `CS2_226` | Frostwolf Warlord | 4/4 | Battlecry: Gain +1/+1 for each other friendly minion on the battlefield. | Wide-board payoff, often 7/7+ |
| 1 | 5 | `EX1_593` | Nightblade | 4/4 | Battlecry: Deal 3 damage to the enemy hero. | Reach |
| 1 | 6 | `EX1_067` | Argent Commander | 4/2 | Charge, Divine Shield | Reach, removes a minion and survives |
| 2 | 10 | `EX1_586` | Sea Giant | 8/8 | Costs (1) less for each other minion on the battlefield. | Counts BOTH boards; often 3–5 mana by turn 5 |

Curve: 10 one-cost cards, 7 two-drops, 4 three-drops, 4 four-drops, 2 five-drops, 1 six-drop, 2 Sea Giants.
Neutral minions: 26. Warlock cards: 6 (Flame Imp, Voidwalker, Soulfire).

`deck.json` holds the 30 ids in this order.

### Card choices versus the classic list

The reference 2014 lists (Reynad, Realz, Stonekeep) are: Flame Imp 2, Voidwalker 2, Soulfire 2, Doomguard 2,
Power Overwhelming 0–2, Abusive Sergeant 2, Argent Squire 2, Leper Gnome 2, Young Priestess 2, Elven Archer,
Knife Juggler 2, Dire Wolf Alpha 2, Harvest Golem 2, Shattered Sun Cleric 2, Dark Iron Dwarf 2, Defender of
Argus 2, Mortal Coil, Ironbeak Owl, Shieldbearer, and later Sea Giant.

| Change | Why |
|---|---|
| Doomguard ×2 removed (Hall of Fame) | Not in pool. Its job (late burst, refill) goes to Nightblade, Argent Commander, Frostwolf Warlord and Sea Giant. |
| Power Overwhelming removed (Hall of Fame) | Not in pool. Abusive Sergeant and Dark Iron Dwarf take over the "make a trade work" role. |
| Leper Gnome cut | Now 1/1 (was 2/1). It no longer trades with anything and its 2 face damage is slow. |
| Young Priestess, Elven Archer, Shieldbearer cut | Low impact. Amani Berserker and Loot Hoarder give better bodies. A simple pilot also plays them better (no end-of-turn random effects to track). |
| Mortal Coil cut | Greedy Mage's early minions (Mana Wyrm 1/3, Sorcerer's Apprentice 3/2) don't die to 1 damage. |
| Ironbeak Owl not used | Now 3 mana. Silence is situational and a simple pilot tends to waste it. |
| Amani Berserker ×2 added | 2/3 that hits for 5 after its first trade; very good into 2-drops and Mage pings. |
| Sea Giant ×2 | The zoo late-game standard: a full board makes it 2–5 mana 8/8. |
| Frostwolf Warlord, Nightblade, Argent Commander | Neutral top end that rewards a wide board (Warlord) or provides reach (Nightblade, Commander). |

Simple-pilot preference: when cards were close, the ones with no target choice and no hidden conditions were
picked (Amani over Young Priestess, Loot Hoarder over Mortal Coil). Felstalker (4/3 for 2) was considered and
left out because its random discard can throw away Sea Giant or Argus.

## 3. How the nerfs changed the deck (compared to online guides)

- **Abusive Sergeant 1/1** (was 2/1): the battlecry is the whole card; don't expect the body to trade.
- **Knife Juggler 2/2** (was 3/2): it no longer trades with 3-health minions. Treat it as an engine. Play it
  before your other cheap minions in the same turn, and protect it with Voidwalker/Argus Taunt.
- **Leper Gnome 1/1**: not worth a slot.
- **Soulfire costs 1** (was 0): it can no longer be played for free with other cards on a full turn. Budget the mana.
- **Flame Imp 3/2 for 1, 3 self-damage**: still the best 1-drop. Against burn Mage the 3 self-damage matters.
- **No Doomguard, no Power Overwhelming, no Leeroy**: Zoo has much less burst than the 2014 deck. That means:
  win by board control first and push face only when the board is safe, rather than planning a big burst turn.
- **Big Game Hunter is 5 mana** and **Ironbeak Owl 3 mana** for opponents: Sea Giant is a bit safer from BGH.
- **Hellfire** (Warlock), **Flamestrike** (Mage 7), **Consecration** (Paladin 4), **Lightning Storm** (Shaman 3,
  2–3 damage), **Blizzard** (Mage 6), **Holy Nova** (Priest 4), **Whirlwind** (Warrior 1) remain the
  board clears to play around. **Unleash the Hounds is 3 mana** and **Equality is 4**.

## 4. Mulligan

General rule: mulligan hard for 1- and 2-drops. Throw away everything that costs 4 or more, and Sea Giant always.

| Card | Going first | Going second (Coin) |
|---|---|---|
| Flame Imp `EX1_319` | Keep | Keep |
| Voidwalker `CS2_065` | Keep | Keep |
| Argent Squire `EX1_008` | Keep | Keep |
| Abusive Sergeant `CS2_188` | Keep only with another 1- or 2-drop minion | Same |
| Soulfire `EX1_308` | Toss | Toss (keep 1 vs Hunter/aggro if hand already has 2 minions) |
| Knife Juggler `NEW1_019` | Keep | Keep |
| Dire Wolf Alpha `EX1_162` | Keep if you also have a 1-drop | Keep if you also have a 1-drop |
| Amani Berserker `EX1_393` | Keep | Keep |
| Loot Hoarder `EX1_096` | Keep | Keep |
| Harvest Golem `EX1_556` | Keep if hand has a 1- or 2-drop | Keep |
| Shattered Sun Cleric `EX1_019` | Keep if hand has a 1- or 2-drop | Keep |
| Defender of Argus `EX1_093` | Toss | Keep one only if the hand already has a 1-drop and a 2-drop |
| Dark Iron Dwarf `EX1_046` | Toss | Toss |
| Frostwolf Warlord, Nightblade, Argent Commander, Sea Giant | Toss | Toss |

Keep at most one 3-drop. If you already have two 2-drops and a 1-drop, keep the hand and don't dig for more.

## 5. Turn-by-turn plan

| Turn | Ideal play | Notes |
|---|---|---|
| 1 | A 1-drop: Flame Imp > Argent Squire > Voidwalker. With Coin: two 1-drops, or Coin + Knife Juggler/Amani. | Don't play Abusive Sergeant alone on turn 1 unless nothing else. |
| 2 | Knife Juggler then a 1-drop (Juggler first so it pings), or two 1-drops, or a 2-drop. | Dire Wolf Alpha between two minions that can attack this turn. |
| 3 | Harvest Golem / Shattered Sun Cleric (buff Squire or an undamaged minion), or 2-drop + 1-drop. | Trade first, then play minions, unless the minion's battlecry helps the trade. |
| 4 | Defender of Argus in between two minions, or Dark Iron Dwarf (buff an attacker before trading), or 2 + 2 / 3 + 1. Life Tap if you have 2 mana spare. | |
| 5 | Nightblade or Frostwolf Warlord (with 3+ other minions), or a cheap Sea Giant plus a small minion. | Check Sea Giant cost every turn. |
| 6 | Argent Commander, or Sea Giant + 2-drop, or Life Tap + 4-drop. | |
| 7+ | Spend all mana, Life Tap with every 2 spare mana, rebuild after board clears with 2–3 cheap minions. | Hold 1–2 cheap minions back vs Flamestrike/Consecration if already ahead. |

Life Tap is the normal use of leftover 2 mana from turn 3 on, as long as health allows (see §8).

## 6. Card-by-card notes

- **Flame Imp:** play turn 1. Trades with any 2-health minion. Against Mage/Hunter, avoid playing it when your
  health is 12 or less unless it wins the board.
- **Voidwalker:** play early vs aggro; place it in front of Knife Juggler/Dire Wolf. It's also a good Argus/Cleric
  target only when you need a wall.
- **Argent Squire:** best Shattered Sun Cleric and Abusive Sergeant target: the Divine Shield absorbs the
  counter-attack, so it trades for free.
- **Abusive Sergeant:** the +2 lasts this turn only. Play it, give +2 to a minion that has not attacked yet, then
  attack with that minion into a target it now kills. Late game: +2 on a face attacker for lethal. Never on a
  minion that can't attack this turn. It can target enemy minions, so make sure the target is yours.
- **Soulfire:** 4 damage for 1 mana, random discard. Best when the hand is small (0–2 other cards) or when it
  kills a key minion (Water Elemental, Yeti, Sorcerer's Apprentice + Mana Wyrm don't need it). Also 4 face
  for lethal. Don't cast it with Sea Giant/Argus in a big hand unless it saves the game.
- **Knife Juggler:** play it before other minions in the same turn (each later summon = 1 random ping).
  Harvest Golem's deathrattle also triggers it.
- **Dire Wolf Alpha:** gives +1 Attack to the minions directly left and right. Place it between two minions
  that can attack this turn, then trade. Keep it out of AoE range where possible.
- **Amani Berserker:** trade it into a minion with 1–2 attack first; it survives damaged as a 5/3.
- **Loot Hoarder:** trade it freely; it draws a card on death.
- **Harvest Golem:** the safe 3-drop vs Flamestrike/Consecration and single removal.
- **Shattered Sun Cleric:** +1/+1 on a minion that then wins a trade (Squire, Amani, Juggler). If no friendly
  minion is on the board, it's still a 3/2 body.
- **Defender of Argus:** place it between two minions (position = index between them). Both get +1/+1 and Taunt.
  Use it to protect your board while ahead, or to make two trades work.
- **Dark Iron Dwarf:** +2 Attack this turn on a minion that has not attacked yet, then trade or go face.
  A 4/4 body is fine on its own.
- **Frostwolf Warlord:** play with 3+ other friendly minions (7/7 or more). With an empty board it's a 4/4 for 5.
- **Nightblade:** 3 face damage now. Best when the enemy is at 3–8 health or you need a 5-drop.
- **Argent Commander:** Charge + Divine Shield. It attacks the turn it is played for 4 and its shield
  absorbs the return hit, so it kills a 4-health minion and survives. Or 4 face for lethal.
- **Sea Giant:** costs 10 minus all other minions on BOTH boards. Play it when it costs 5 or less. It's the
  best card after a board-wide trade-off where both sides still have many minions.

## 7. Combos, synergies and positioning

- **Knife Juggler first, then cheap minions**: each summon pings. Juggler + Harvest Golem deathrattle also pings.
- **Buff then attack**: Abusive Sergeant / Dark Iron Dwarf / Shattered Sun Cleric / Dire Wolf Alpha / Defender
  of Argus are all played BEFORE attacks with the buffed minions.
- **Dire Wolf Alpha and Defender of Argus are adjacency cards.** Board positions run left to right from 0.
  Playing at position `p` puts the new minion between the minions at `p-1` and `p`. Choose `p` so both neighbours
  are your best attackers (Dire Wolf) or the minions you want as Taunts (Argus).
- **Wide board → Frostwolf Warlord / Sea Giant**: the more minions, the bigger/cheaper.
- **Argent Squire + any buff**: divine shield means the buffed Squire trades and survives.
- **Amani + any 1-damage trade**: enrage once, then it's a 5/3.
- Keep the Taunt minions (Voidwalker, Argus-buffed ones) on the board; trade with the others.

## 8. Trading rules and face vs trade

Zoo trades a lot early. Old guides agree: "very rarely go face until lethal is in reach", "only make value trades".

Priority of enemy minions to kill:
1. Taunts that block lethal (only when lethal is on).
2. Minions that snowball or deal damage every turn: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler, Flametongue
   Totem, Imp Master, Questing Adventurer, Violet Teacher, Mana Tide Totem, Demolisher, Cult Master, Lightwell,
   Northshire-like engines, Wild Pyromancer.
3. Minions that would trade into ours efficiently (high attack, low health): Bloodfen Raptor, Magma Rager,
   Argent Commander, Flame Imp, Wolfrider.
4. Water Elemental (freezes your minions) and big bodies, with several minions or Soulfire.

Rules:
- **Good trade**: our minion kills the target and survives, OR our minion costs less than the target.
- **Don't trade** a minion into a target it can't kill unless two attacks together kill it this turn.
- **Go face** with minions that have no good trade, when the enemy board is empty, or once lethal is within reach
  this turn or next.
- **Race** only when our board damage clearly outpaces theirs (we deal at least twice as much per turn) and their
  board can't kill us next turn.
- **Spell damage before attacks**: Soulfire a big minion first, then trade the rest.

## 9. Hero power (Life Tap)

- Cost 2: draw a card, take 2 damage.
- Use it when 2 mana is left and there is no better 2-mana play. It is the default way to finish a turn from
  turn 3 onwards.
- With 4+ mana and only 2-mana-or-less of good plays in hand, tap FIRST (the card drawn may be better).
- Don't tap when health ≤ 10 against Mage, Hunter, Shaman, Warrior (burn/charge decks), or ≤ 6 against anyone.
- Don't tap if the hand already has 6+ cards (risk of overdraw at 10, and wasted health).
- After a board clear, tapping is the priority to refill.

## 10. Lethal checklist

Reach this deck can find in one turn:
- Each minion that can attack: its attack (+1 if next to Dire Wolf Alpha).
- Abusive Sergeant +2, Dark Iron Dwarf +2 (on a minion that can still attack).
- Soulfire 4 (1 mana), Nightblade 3 (5 mana), Argent Commander 4 Charge (6 mana).
- Knife Juggler pings are random; don't count them.
Enemy Taunts must be killed first; subtract enemy armor; check Divine Shield. If total ≥ enemy health, go face
with everything. If one short, play buffs before attacks.

## 11. Matchups

### Greedy Mage (course bot)
Deck: Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Bloodmage Thalnos,
Harvest Golem, Yeti, Water Elemental, Fireball, Polymorph, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre,
Argent Commander, 1 Flamestrike. Plays greedily, one action at a time, no lethal planning.
- **Plan: be the beatdown.** Its only board clear is 1× Flamestrike at 7 mana; Arcane Missiles hits 1-health
  minions. Take the board on turns 1–4 and push damage before turn 7.
- Kill Mana Wyrm and Sorcerer's Apprentice on sight.
- Water Elemental 3/6 and Sen'jin 3/5 Taunt are the walls: use two minions or Soulfire + attack, or go wide and
  ignore Water Elemental only if lethal is close.
- Fireblast (1 damage) kills 1-health minions: Squire's shield helps; buff 1-health minions with Cleric.
- From turn 6, if well ahead, keep 1–2 minions in hand to rebuild after Flamestrike. Harvest Golem and Argent
  Commander's Divine Shield also survive partly.
- Watch your own health: Fireball 6 + Frostbolt 3 + Fireblast 1 = 10 burst. Stop Life Tap at ≤ 10 health.
- Big late bodies (Boulderfist 6/7, Yeti 4/5): Sea Giant 8/8 or Frostwolf Warlord is the answer; or trade 2–3
  minions with Dire Wolf/Dark Iron Dwarf help.

### Other Mage (Tempo / spells)
Same plan. Respect Arcane Explosion (1 to all) and Blizzard (2 to all + Freeze): don't over-commit 1–2 health
minions when you are already ahead.

### Hunter (Face / Midrange)
Board control matters; Hunter has Unleash the Hounds (3 mana, one 1/1 Charge per enemy minion), Explosive Trap
(2 to all on face attack) and Multi-Shot. Trade their beasts every turn (Timber Wolf, Scavenging Hyena first).
Voidwalker/Argus Taunts block their face race. Don't Life Tap below 12 health; Kill Command is 3–5 reach.

### Paladin
Consecration (4 mana, 2 to all enemies) and Equality (4) are the clears. From turn 4 on, prefer 3+ health minions
and keep a reload in hand. Kill Argent Protector-shielded minions with a 1-attack ping/Abusive first. Tirion: trade
into the shield with a small minion, then finish.

### Warrior
Whirlwind, Cleave, Fiery War Axe 3/2, Arcanite Reaper, Brawl (5). Go wide but keep Taunts up vs their
weapons; Frothing Berserker and Armorsmith must die immediately. Aggro Warrior: trade; Control Warrior: go face.

### Shaman
Lightning Storm (3 mana, 2–3 to all), Feral Spirit taunts, Flametongue Totem (kill it first), Mana Tide Totem
(kill it). Harvest Golem and Argus help vs Storm. Zoo is historically favoured.

### Rogue
Blade Flurry (4, weapon damage to all minions), Fan of Knives (1 to all), SI:7 Agent, Edwin VanCleef (kill on
sight). Their weapons trade with your 1–2 health minions; make them pay with face pressure. Keep Argus Taunt up.

### Druid
Swipe (4 + 1 to the others), Starfall AoE (2 to all), Wrath, Keeper of the Grove. Zoo was historically favoured.
Push early before their big taunts (Druid of the Claw, Ancient of War, Ironbark Protector) arrive.

### Warlock
Hellfire (3 to ALL characters, 4 mana): avoid 1–3 health minion floods when ahead. Mirror: whoever wins the early
board and lands Sea Giant first usually wins.

### Priest
Holy Nova (2 to all), Shadow Word: Pain kills 3-attack-or-less minions, Lightwell and Cabal. Pressure fast; kill
Lightwell and Kul Tiran-buffed minions.

## 12. Common mistakes

- Playing minions before attacking with a minion that needed a buff from them (or vice versa: attacking first,
  then playing Dire Wolf/Abusive).
- Using Abusive Sergeant or Dark Iron Dwarf on a minion that already attacked or was just played.
- Placing Dire Wolf Alpha / Argus on the edge of the board with only one neighbour when a middle slot was free.
- Going face with all minions early while the enemy board grows. Trade first.
- Tapping into burn range (Life Tap at low health vs Mage/Hunter).
- Flooding a full board into a known board clear when already ahead.
- Casting Soulfire with a big hand and losing Sea Giant or Argus to the discard.
- Forgetting Sea Giant's cost has dropped.
- Ending the turn with unused mana when Life Tap was available.

## 13. Script hints (machine-encodable rules)

### Mulligan
- KEEP always: `EX1_319`, `CS2_065`, `EX1_008`, `NEW1_019`, `EX1_393`, `EX1_096`.
- KEEP if hand has another card with cost ≤ 2 (minion): `CS2_188`, `EX1_162`.
- KEEP if hand has a card with cost ≤ 2, max one of them: `EX1_556`, `EX1_019`.
- KEEP if going second AND hand has a 1-drop AND a 2-drop: one `EX1_093`.
- REPLACE always: `EX1_046`, `CS2_226`, `EX1_593`, `EX1_067`, `EX1_586`, `EX1_308`.

### Turn order
1. Lethal check (§10). If lethal: buffs (`CS2_188`, `EX1_046`) on attack-ready minions, `EX1_593` battlecry,
   `EX1_067` charge, `EX1_308` face, then attack face with all; kill Taunts first only if needed.
2. Pre-attack buffs: play `EX1_162` (between two attack-ready minions), `EX1_093` (between two), `CS2_188` /
   `EX1_046` (on an attack-ready friendly minion that then kills a target), `EX1_019` (on a minion about to trade).
3. Removal: `EX1_308` on an enemy minion with attack ≥ 3 or an engine minion, only if hand size ≤ 3 or it
   prevents a losing board.
4. Trades: for each attack-ready minion, attack the highest-priority enemy minion it kills and survives;
   else attack an enemy it kills if our minion costs less; else go face.
5. Spend mana: `NEW1_019` first among minions; then by cost high→low until mana is used;
   `EX1_586` when its current cost ≤ mana; `CS2_226` only with ≥ 3 other friendly minions (else play it if
   nothing else costs 5).
6. Life Tap (hero_power, no target) if mana ≥ 2 and health > 10 (> 6 vs Druid/Paladin/Priest/Warlock/Rogue)
   and hand size ≤ 6.
7. End turn.

### Target priority (enemy minions)
- Taunt blocking lethal > engine minion (`NEW1_012` Mana Wyrm, `EX1_608` Sorcerer's Apprentice,
  `NEW1_019`, `EX1_565`, `EX1_575`, `EX1_597`, `EX1_044`, `NEW1_026`, `EX1_102`, `EX1_595`, `EX1_341`,
  `NEW1_020`, `EX1_604`, `EX1_402`, `EX1_613`) > highest attack it can kill > lowest-health minion.

### Never
- Never send `target` unless the legal action lists targets; never use card ids during play.
- Never give `CS2_188` / `EX1_046` / `EX1_019` to an enemy minion.
- Never Life Tap at health ≤ 6, or at health ≤ 10 against Mage/Hunter/Shaman/Warrior.
- Never Soulfire with Sea Giant in hand and hand size ≥ 4, unless it is lethal.
- Never play `EX1_162` / `EX1_093` at an edge when a slot between two friendly minions exists.
- Never attack with a minion into a target it doesn't kill unless a second attack this turn finishes it.

### Face vs trade thresholds
- Face if: enemy board empty, OR lethal this turn, OR (our total attack ≥ enemy health − 6 AND enemy board
  attack < our health / 2).
- Trade otherwise, as long as the trade is good (§8).

## 14. Sources

| URL | What was used |
|---|---|
| https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/ | Realz's classic Zoo decklist (core package, Doomguard/Soulfire burst plan, "empty hand fast, buff and trade"). |
| https://www.hearthstonetopdecks.com/decks/reynads-curse-naxxramas-warlock-zoo/ | Reynad's 2014 list: Harvest Golem / Cleric / Argus / Dark Iron Dwarf core. |
| https://www.hearthstonetopdecks.com/decks/classic-zoo-warlock-zoolock/ | 2021 Classic-format list (Mortal Coil, Leper Gnome, Young Priestess). |
| https://www.hearthstonetopdecks.com/decks/budget-cheap-warlock-zoo-deck-list-guide-mean-streets-gadgetzan/ | Per-card mulligan rules (always keep 1-drops; Abusive only with other 1-drops; Juggler/Dire Wolf with a 1-drop), Life Tap rules (tap before playing cards, tap less in fast matchups), "trade on your own terms", positioning for Dire Wolf/Argus, rebuild after clears. |
| https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/ | Matchup data: Zoo favoured vs Druid, weaker vs Miracle Rogue and Control Warrior; Cleric best 3-drop, Harvest Golem over Scarlet Crusader, Dark Iron Dwarf filler for turn 4, Ironbeak Owl overrated, Mortal Coil good vs 1-health metas. |
| https://blizzardwatch.com/2015/06/07/hearthstone-warlock-zoo-deck/ | Life Tap discipline (early tapping = losing; don't tap into burn range), play around AoE per class (Consecration 2 hp, Swipe 1 hp, Flamestrike → sticky minions), don't flood vs Hunter, mulligan for cheap plays. |
| https://hearthstone.wiki.gg/wiki/Zoo_deck | Archetype definition, sticky minions vs AoE, AoE as the main weakness. |
| https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki:Archived/Zoolock | Early/mid/late plan: flood, trade efficiently, rarely go face until lethal; failed rushes lose. |
| https://www.pocketgamer.com/articles/076724/r/ | Life Tap after board clears, keep cheap cards to rebuild vs AoE, careful with self-damage vs Mage. |
| `meta.md` §2–3 (local) | Current card texts/costs, Hall of Fame list, Greedy Mage decklist and behaviour. |
| fireplace source in the package (local) | Life Tap = 2 damage + draw; Sea Giant cost counts all minions on both boards; Frostwolf Warlord counts other friendly minions. |
