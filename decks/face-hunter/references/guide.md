# Face (Aggro) Hunter: Deck Guide

Pool: hs-arena 0.2.2, `basic-classic-1` (modern "Legacy" Basic + Classic, nerfs applied, Hall of Fame cards removed).
All card text below is the CURRENT text from `meta.md` §2 / `data/cards.json`, not the 2014 text.

## 1. Overview and win condition

Face Hunter wins by dealing 30 damage before the opponent's bigger cards take over, ideally by turn 7-8.
Damage comes from four places:

1. **Cheap minions** that hit face on turns 1-4 (Leper Gnome, Worgen Infiltrator, Bloodfen Raptor, Faerie Dragon, Jungle Panther, Animal Companion).
2. **Charge and direct damage** that ignore the board (Wolfrider, Huffer, Unleash the Hounds, Kill Command, Arcane Shot, Nightblade, Argent Commander, Leper Gnome Deathrattle, Explosive Trap).
3. **Eaglehorn Bow**: 3 face damage per swing, extra durability when Explosive Trap fires.
4. **Steady Shot** (hero power, 2 mana): 2 damage to the enemy hero that nothing can block. Over a 9-turn game that is 10-16 damage, half the opponent's life.

The plan is **early board → chip face → burn them out**. Minions only trade when that keeps more damage flowing (a better minion of ours survives, a Taunt is in the way, or the enemy board would out-race us).

Because the 2014 burst cards are gone (Leeroy Jenkins, Charge Arcane Golem, Starving Buzzard + Unleash draw engine), this build leans a little toward "aggressive Beast Hunter": eight Beast cards to power up Kill Command (5 damage) and Houndmaster, plus two units that Mage removal can't touch (Faerie Dragon, Jungle Panther in Stealth).

## 2. Decklist (30 cards, curve 6/8/11/2/1/1, average cost 2.47)

| # | Cost | Id | Name | Type / stats | Current text | Role |
|---:|---:|---|---|---|---|---|
| 2 | 1 | `EX1_029` | Leper Gnome | Minion 1/1 | Deathrattle: Deal 2 damage to the enemy hero. | Turn-1 drop; guaranteed 2 face when it dies |
| 2 | 1 | `EX1_010` | Worgen Infiltrator | Minion 2/1 | Stealth | Turn-1 drop that is sure to attack once |
| 1 | 1 | `DS1_185` | Arcane Shot | Spell | Deal 2 damage. | Kills 2-health minions / 2 face reach |
| 1 | 1 | `CS2_171` | Stonetusk Boar | Minion 1/1 Beast | Charge | Late-game Beast enabler for Kill Command (Boar + KC = 6 dmg for 4 mana) |
| 2 | 2 | `CS2_172` | Bloodfen Raptor | Minion 3/2 Beast | — | Best 2-drop stats; Beast for KC/Houndmaster |
| 2 | 2 | `NEW1_023` | Faerie Dragon | Minion 3/2 Dragon | Can't be targeted by spells or Hero Powers. | Immune to Frostbolt/Fireball/Polymorph/Fireblast |
| 2 | 2 | `NEW1_019` | Knife Juggler | Minion 2/2 | After you summon a minion, deal 1 damage to a random enemy. | Extra pings with cheap minions and Unleash |
| 2 | 2 | `EX1_610` | Explosive Trap | Secret | When your hero is attacked, deal 2 damage to all enemies. | Anti-aggro sweeper that also hits the enemy hero; +1 Bow durability |
| 2 | 3 | `NEW1_031` | Animal Companion | Spell | Summon a random Beast Companion. | Huffer 4/2 Charge, Leokk 2/4 (+1 Attack to others), Misha 4/4 Taunt |
| 2 | 3 | `EX1_539` | Kill Command | Spell | Deal 3 damage. If you control a Beast, deal 5 damage instead. | Main burn / removal |
| 2 | 3 | `EX1_536` | Eaglehorn Bow | Weapon 3/2 | Whenever a friendly Secret is revealed, gain +1 Durability. | 6+ damage over two turns, kills small minions |
| 2 | 3 | `EX1_017` | Jungle Panther | Minion 4/2 Beast | Stealth | 4 guaranteed face damage; Beast |
| 2 | 3 | `CS2_124` | Wolfrider | Minion 3/1 | Charge | 3 burn on a body |
| 1 | 3 | `EX1_538` | Unleash the Hounds | Spell | For each enemy minion, summon a 1/1 Hound with Charge. | Burst vs wide boards; Hounds are Beasts (power up KC) |
| 1 | 3 | `CS2_203` | Ironbeak Owl | Minion 2/1 Beast | Battlecry: Silence a minion. | Removes a Taunt (Sen'jin, Misha-type) or a buff |
| 2 | 4 | `DS1_070` | Houndmaster | Minion 4/3 | Battlecry: Give a friendly Beast +2/+2 and Taunt. | Turn-4 power play on a Beast |
| 1 | 5 | `EX1_593` | Nightblade | Minion 4/4 | Battlecry: Deal 3 damage to the enemy hero. | Unblockable 3 face + body |
| 1 | 6 | `EX1_067` | Argent Commander | Minion 4/2 | Charge, Divine Shield | 4 charge damage, survives a ping |

Beasts in the deck: Stonetusk Boar, Bloodfen Raptor ×2, Jungle Panther ×2, Ironbeak Owl, all three Animal Companions, Unleash Hounds.

Validator output for `deck.json`: `[]`.

### Cards considered and left out

| Card | Why not |
|---|---|
| Leeroy Jenkins | Hall of Fame (not in pool). |
| Starving Buzzard (`CS2_237`) | Now 5 mana 3/2. The Buzzard + Unleash draw combo is dead. |
| Arcane Golem (`EX1_089`) | Now 4/4 with no Charge and still gives the opponent a Mana Crystal. Not a finisher any more; ramping a Mage into Fireball/Water Elemental is bad. |
| Abusive Sergeant (`CS2_188`) | 1/1 body, +2 Attack this turn. Weak tempo and needs a correct target; replaced by Arcane Shot and Boar. |
| Timber Wolf (`DS1_175`) | 1/1, only matters with several Beasts on board. Too low impact. |
| Scavenging Hyena (`EX1_531`) | Slow without Unleash/Buzzard engine. |
| Dire Wolf Alpha (`EX1_162`) | Positional buff; harder for a simple pilot. Raptor gives the same damage with no positioning. |
| Hunter's Mark (`CS2_084`) | Now 2 mana. Owl handles Taunts more simply (no follow-up attack needed to remove the Taunt). |
| Freezing Trap / Misdirection / Snipe | Defensive or random; Explosive Trap is the only Secret that adds face damage. |
| Savannah Highmane, King Krush, Tundra Rhino, Gladiator's Longbow | Too slow for a race plan (midrange cards). |
| Reckless Rocketeer (`CS2_213`) | Playable 6-mana 5/2 Charge; Argent Commander preferred for Divine Shield. Swap in if you want more reach. |
| Stranglethorn Tiger (`EX1_028`) | Strong 5/5 Stealth Beast, but 5 mana; Nightblade's damage is immediate. Good swap vs slow decks. |

## 3. How the nerfs changed the deck (vs the 2014 / 2021 Classic version)

| Card (current) | Original | Effect on the deck |
|---|---|---|
| Leper Gnome 1/1 | 2/1 | Loses 1 damage per attack and now dies to everything; still worth it for the 2 Deathrattle damage. Keep it, but it is no longer a premium 1-drop. |
| Knife Juggler 2/2 | 3/2 | Weaker body; still useful because the deck summons many minions and Hounds. |
| Abusive Sergeant 1/1 | 2/1 | Cut. |
| Starving Buzzard 5 mana | 2 mana | Buzzard + Unleash card draw gone; the deck has no card draw, so play for fast damage, not long games. |
| Unleash the Hounds 3 mana | 2 mana (pre-nerf) | Now a pure burst card, played only when it makes 2+ Hounds or wins the game. |
| Arcane Golem no Charge | 4/2 Charge (2014) | No longer a finisher; cut. |
| Leeroy Jenkins | in pool | Removed (Hall of Fame). Lost 6 burst; Argent Commander + Nightblade replace some of it. |
| Steady Shot | same 2 dmg, 2 mana | Unchanged and now proportionally more important. |
| Kill Command, Eaglehorn Bow, Animal Companion, Explosive Trap, Wolfrider | unchanged | The core is intact. |

Online advice that had to be changed:
- "Coin + Buzzard + Unleash to draw your hand" and "Leeroy + Abusive/Power-up for 10+ burst": both gone. Count lethal with Kill Command, Charge minions, Bow and Steady Shot only.
- "Arcane Golem as a finisher" (2016 guide): Golem has no Charge here.
- Mulligans that kept Leper Gnome above everything: Leper is still a keep, but Raptor/Faerie Dragon/Animal Companion carry the early game now.
- Mad Scientist, Haunted Creeper, Quick Shot, Glaivezooka, Argent Horserider, Fiery Bat, Kindly Grandmother (later-set cards in online lists): not in the pool.

## 4. Mulligan

Starting hand: 3 cards going first, 4 cards going second (The Coin comes after the mulligan).

**Always keep:** Leper Gnome (`EX1_029`), Worgen Infiltrator (`EX1_010`), Bloodfen Raptor (`CS2_172`), Faerie Dragon (`NEW1_023`), Knife Juggler (`NEW1_019`), Animal Companion (`NEW1_031`).

**Conditional keeps:**
- Eaglehorn Bow (`EX1_536`): keep if you also hold a 1- or 2-drop. Always keep vs Mage, Paladin, Rogue, Hunter, Warlock (kills their 2-3 health early minions).
- Jungle Panther (`EX1_017`) / Wolfrider (`CS2_124`): keep one 3-drop minion if you already hold a 1- or 2-drop, or if going second.
- Explosive Trap (`EX1_610`): keep only vs aggressive classes (Paladin, Hunter, Warlock, Warrior) and only with a 1-2 drop.
- Houndmaster (`DS1_070`): keep only going second, with a Beast 2-drop (Raptor) in hand.

**Always mulligan:** Kill Command, Unleash the Hounds, Arcane Shot, Stonetusk Boar, Ironbeak Owl, Nightblade, Argent Commander. (Burn is for the end of the game; you can't afford it in the opening hand.)

Rule of thumb: you want a 1-drop or 2-drop **and** a 3-drop. Never keep two 3-drops and nothing cheaper.

## 5. Turn-by-turn plan (ideal curves)

| Turn | Going first | Going second (with Coin) |
|---|---|---|
| 1 | Leper Gnome / Worgen Infiltrator | 1-drop, or Coin → Raptor/Faerie Dragon |
| 2 | Raptor / Faerie Dragon / Knife Juggler (or 1-drop + 1-drop, or Explosive Trap if nothing else) | 2-drop, or Coin → 3-drop (Animal Companion / Panther) |
| 3 | Animal Companion / Jungle Panther / Eaglehorn Bow / Wolfrider | same |
| 4 | Houndmaster on a Beast; or 3-drop + 1-drop; or Bow + 1-drop; or 2-drop + Steady Shot | same |
| 5 | Nightblade; or 3-drop + Steady Shot; or 2 + 3 | same |
| 6 | Argent Commander; or Kill Command + 3-drop; or 4-drop + Steady Shot | same |
| 7+ | Burn + Steady Shot every turn: Kill Command (5 with a Beast), Wolfrider, Bow swings, Unleash. Hold burn for a lethal turn unless a minion must die. | same |

Mana priorities each turn: spend all mana. From turn 2 onward, if 2 mana are left over, **always** use Steady Shot.

## 6. Card-by-card usage notes

- **Leper Gnome** (`EX1_029`): turn 1. Attack face; trade it into a 1-health minion freely (the 2 face damage happens anyway). Never use Steady Shot or Kill Command to protect it.
- **Worgen Infiltrator** (`EX1_010`): turn 1. Stealth guarantees one face hit; after it attacks it can be targeted.
- **Arcane Shot** (`DS1_185`): kill a 2-health minion that blocks or threatens (Sorcerer's Apprentice 3/2, Mana Wyrm after it gets damaged, Knife Juggler, Flame Imp). Otherwise hold it for 2 face damage on the lethal turn. Good 1-mana filler next to a 3- or 4-drop.
- **Stonetusk Boar** (`CS2_171`): don't play it turn 1 unless nothing else. Best played late, the same turn as Kill Command: Boar (1 face) + KC to face (5) = 6 damage for 4 mana.
- **Bloodfen Raptor** (`CS2_172`): turn 2. Beast for Houndmaster on 4 and for Kill Command.
- **Faerie Dragon** (`NEW1_023`): turn 2. Vs Mage it can't be targeted by Frostbolt, Fireball, Polymorph or Fireblast, so it often lives several turns (random Arcane Missiles and Flamestrike can still hit it). Best 2-drop vs Mage, Priest, Druid, Shaman.
- **Knife Juggler** (`NEW1_019`): play it before other minions in the same turn so each summon pings. Before Unleash the Hounds it deals extra damage (one ping per Hound).
- **Explosive Trap** (`EX1_610`): play on a turn with 2 spare mana, best when the enemy has several small minions that will attack your face. It also deals 2 to the enemy hero and gives the Bow +1 durability. Vs a Hunter, beware your own Charge attacks into their face trigger theirs.
- **Animal Companion** (`NEW1_031`): turn 3. Huffer (4/2 Charge, attack face right away), Leokk (2/4, gives your other minions +1 Attack), Misha (4/4 Taunt, protects the board). All three are Beasts.
- **Kill Command** (`EX1_539`): 5 damage if you control a Beast at cast time, 3 otherwise. Prefer face for lethal; use on a minion only when it is a must-kill (a big Taunt blocking lethal, a 4-5 health minion that would win the board like Water Elemental or Yeti). Play a Beast first (Boar, Raptor, Panther, Owl, Animal Companion, Unleash) to get 5.
- **Eaglehorn Bow** (`EX1_536`): turn 3 vs early minions, or later for 3 face per turn. Use it on minions with 3 or less Attack (you take that much damage) and 3 or less Health. Against slow decks, swing face. Play Explosive Trap while holding the Bow to keep it alive longer.
- **Jungle Panther** (`EX1_017`): 4/2 Stealth Beast. The opponent can't target it until it attacks; it almost always deals 4 face. Great Houndmaster target only when you need a Taunt (it loses Stealth when it attacks anyway).
- **Wolfrider** (`CS2_124`): 3 face damage immediately. Use as burn: play it when it adds lethal, when you have no better 3-drop, or to kill a 1-3 health minion (it dies to most counter-attacks anyway).
- **Unleash the Hounds** (`EX1_538`): requires at least one enemy minion. Play it when it makes 2+ Hounds or when the Hounds give lethal. Hounds are Beasts with Charge: Unleash + Kill Command (6 mana) = N face + 5. With Knife Juggler on board each Hound also pings.
- **Ironbeak Owl** (`CS2_203`): Silence an enemy Taunt that blocks your attackers (Sen'jin Shieldmasta, Misha, Ironfur Grizzly, Mogu'shan, a Houndmaster buff), or a big buffed minion. Don't waste it on small Taunts you can just attack. Without a target worth silencing, it is a 2/1 Beast. If the game asks for a target, pick an enemy minion (never your own buffed/Taunt minion).
- **Houndmaster** (`DS1_070`): turn 4, target your best Beast (+2/+2 Taunt). Best on Raptor (5/4 Taunt) or Leokk/Misha. Without a Beast it is a plain 4/3: still fine if nothing else uses your mana.
- **Nightblade** (`EX1_593`): 3 unblockable face damage + 4/4 body. Play on 5, or later as part of lethal.
- **Argent Commander** (`EX1_067`): 4 Charge damage, Divine Shield lets it trade into a small minion and survive. Mostly face.
- **Steady Shot** (hero power): 2 face damage for 2 mana. Use every turn you have 2 spare mana. It is not targeted.

## 7. Combos, synergies and positioning

- **Beast + Kill Command** = 5 damage. Keep a Beast alive (or play one first) on the burn turn.
- **Unleash + Kill Command**: Hounds count as Beasts.
- **Knife Juggler first, then summon**: each summon (including Animal Companion, Hounds, Owl) pings a random enemy.
- **Houndmaster on a Beast**: turn-4 power play; Raptor becomes 5/4 Taunt.
- **Explosive Trap + Eaglehorn Bow**: Bow gains +1 durability when Trap is revealed.
- **Stonetusk Boar + Kill Command** late: 6 damage for 4 mana.
- **Leokk** gives +1 Attack to every other friendly minion: attack with your other minions after Leokk is on board.
- **Positioning:** only Leokk's aura is board-wide; nothing in this deck cares about adjacency. Place minions rightmost (default). No positional mistakes are possible.

## 8. Trading rules (face vs trade)

Default is **face**. Trade only when one of these is true:
1. **Taunt** blocks your attackers: kill it with the cheapest combination (attacks first, then Arcane Shot / Owl / Kill Command).
2. **Free kill**: your minion kills the enemy minion and survives (e.g. Raptor 3/2 into a 2/1).
3. **Board threat**: the enemy board would deal more damage to you next turn than you can race, or the enemy minion is a damage engine (Knife Juggler, Mana Wyrm, Flametongue Totem, Wild Pyromancer, Imp Master, Questing Adventurer, Violet Teacher, Cult Master). Kill it.
4. **Even trade up**: your cheap minion kills a more expensive one (e.g. Wolfrider 3/1 kills Sorcerer's Apprentice).

Never trade when:
- You have lethal (count first!).
- The trade only kills a 1/1 token while your minion could deal 3+ face.
- The enemy is at ≤ 10 health and you are not in danger of dying next turn: race.

Target priority when trading: Taunt blocking lethal > damage engines (Mana Wyrm, Knife Juggler, Sorcerer's Apprentice, Flametongue Totem) > minions with 4+ Attack that threaten your face > everything else.

Race math: if (your damage per turn) × (turns until they die) beats theirs, ignore their board and go face.

## 9. Hero power (Steady Shot)

- 2 mana: deal 2 damage to the enemy hero. No target needed.
- Use it whenever you end a turn with 2+ unspent mana (turn 2 with no 2-drop, turn 5 with a 3-drop, etc.).
- When choosing between "a weak minion" and "Steady Shot", Steady Shot is often better vs heavy-removal decks (Mage, Rogue, Priest).
- Order: play cards first, then Steady Shot with leftover mana, then end turn.

## 10. Lethal checklist (run every turn before anything else)

Count damage you can deal this turn to the enemy hero:
- Attack of every friendly minion that can attack and is not blocked (if the enemy has a Taunt you must remove it first, or this damage doesn't count).
- Eaglehorn Bow swing: 3 (if equipped and hero hasn't attacked).
- Kill Command: 5 with a Beast on board (3 otherwise), 3 mana.
- Arcane Shot: 2 (1 mana). Wolfrider: 3 (3 mana). Stonetusk Boar: 1 (1 mana), also enables KC.
- Huffer from Animal Companion: random, don't count it.
- Unleash the Hounds: one per enemy minion (3 mana), each Hound 1 Charge damage.
- Nightblade: 3 (5 mana). Argent Commander: 4 (6 mana).
- Steady Shot: 2 (2 mana).
- Leper Gnome dying: 2.
Pick the combination that fits in your mana. If total ≥ enemy health + armor, go all face. Remove Taunts first with the minimum resources.

Max burst examples:
- 6 mana: Kill Command (5 w/ Beast) + Wolfrider (3) = 8.
- 7 mana: Kill Command (5) + Wolfrider (3) + Arcane Shot (2) = 10, or KC + Unleash vs 3 minions + Arcane Shot.
- 10 mana: KC ×2 (10) + Steady Shot (2) + Arcane Shot (2) = 14 plus board.

## 11. Matchups

### Greedy Mage (the course bot: Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Water Elemental, Fireball, Polymorph, Yeti, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike)
- **Favourable if fast.** Its removal is single-target and its only AoE is one 7-mana Flamestrike. It plays greedily and doesn't plan.
- Keep Faerie Dragon (immune to its spells and Fireblast), Bloodfen Raptor, Animal Companion, Bow.
- Kill Mana Wyrm and Sorcerer's Apprentice early with Bow / Arcane Shot / free trades: they snowball.
- 1-health minions die to Fireblast; prefer Raptor/Faerie Dragon over Leper (but Leper still gives 2 face when Fireblasted).
- **Sen'jin Shieldmasta (3/5 Taunt) is the key blocker.** Silence it with Ironbeak Owl, or ignore the board and use Charge/burn/Steady Shot.
- Water Elemental (3/6, freezes) and Boulderfist Ogre (6/7) are too big to trade with and have no Taunt: ignore them and race with burn, Stealth and Steady Shot. Silence Water Elemental with Owl only if its freeze is stopping your lethal.
- Don't overextend after turn 6: keep 2-3 minions on board, hold the rest plus burn for after Flamestrike.
- Stranglethorn Tiger (5/5 Stealth) can't be targeted; race it.
- Its Argent Commander is a 4/2 Divine Shield Charge: pop the shield with a 1-attack hit (Hound, Boar, Leper), then kill it.

### Hunter (mirror / midrange)
- Board matters more. Keep Bow and 2-drops. Trade for board early, then race with burn.
- Respect their Explosive Trap: if they have a Secret and you have several 2-health minions, attack their minions first or attack face with only one minion to trigger it. Freezing Trap bounces the first attacking minion: attack with the cheapest one first.
- Their Houndmaster/Misha Taunts: Owl or Kill Command.

### Paladin (aggro / midrange)
- Divine Shield minions (Argent Squire, Scarlet Crusader, Argent Commander): pop the shield with a cheap 1-attack hit (Hound, Boar, Leper) or a Knife Juggler ping, then kill it. Steady Shot only hits the hero.
- Consecration (2 to all enemies) wipes your 2-health board: don't dump more than 3 small minions at once from turn 4.
- Truesilver/healing slows the race: push early, kill Paladin's 1/1 Silver Hand Recruits only if they block.

### Warrior
- Armor Up (+2) cancels Steady Shot. Count armor in lethal math.
- Fiery War Axe (3 mana) kills your 2-drops; Whirlwind and Cleave punish many small minions. Spread threats over turns.
- Taunts (Shieldmasta, Fen Creeper, Grommash pre-buff): Owl them. Go maximum face early; they gain armor late.

### Shaman
- Lightning Storm (3 mana) and Flametongue Totem: don't overextend; kill Flametongue Totem immediately.
- Feral Spirit wolves (2/3 Taunt): need two attacks or Kill Command; consider Unleash (they're minions that give Hounds).
- Hex (4 mana) and Earth Shock can answer one threat; Jungle Panther and Faerie Dragon (can't be targeted) dodge them.

### Rogue
- Backstab, Deadly Poison, SI:7 Agent kill early minions. Steady Shot more, minions less.
- Keep Bow: kill their small minions and 1-health weapon-users. Blade Flurry (4 mana, minions only) punishes wide boards.
- Their weapon attacks cost them health: force them to use the weapon on minions or race.

### Druid
- Swipe (4 dmg + 1 to others) and Keeper of the Grove (4 mana) answer one or two minions. Mix Stealth (Panther) and Charge.
- Big Taunts (Ancient of War, Druid of the Claw bear form 4/6 Taunt): Owl or go around with burn.
- Innervate can bring out a Taunt early: save Kill Command or Owl for it.

### Warlock (Zoo)
- Board war: trade aggressively early (Zoo out-races Face Hunter if left alone). Bow, Explosive Trap and Unleash all shine.
- Kill Knife Juggler, Flame Imp, Imp Master, Dire Wolf Alpha first.
- Hellfire (3 to all) wipes everything: don't overextend in the mid game.

### Priest
- Few early answers but heals. Rush hard; kill healers (Injured Blademaster, Earthen Ring Farseer) only if they block. Holy Nova-style AoE punishes 2-health boards.

## 12. Common mistakes

1. Using Kill Command on a minion when it could have dealt the last 5 face damage next turn.
2. Forgetting Steady Shot with 2 unspent mana.
3. Trading a 3-attack minion into a 1/1 token instead of hitting face.
4. Playing Unleash with only one enemy minion when no lethal follows (a 3-mana 1/1).
5. Casting Kill Command for 3 because the Beast died first / wasn't played first.
6. Playing every minion into a known AoE (Flamestrike on 7, Consecration, Lightning Storm, Hellfire).
7. Silencing a small Taunt with Owl instead of attacking it; then having no answer for Sen'jin later.
8. Attacking into a Hunter's Secret with the whole board (Explosive Trap) without testing with one minion.
9. Swinging the Bow into a minion with 4+ Attack (you take too much damage) when face was available.
10. Not checking lethal before trading.

## 13. Script hints (machine-encodable rules)

**Mulligan**
- KEEP always: `EX1_029`, `EX1_010`, `CS2_172`, `NEW1_023`, `NEW1_019`, `NEW1_031`.
- KEEP `EX1_536` if hand also contains any of {`EX1_029`,`EX1_010`,`CS2_172`,`NEW1_023`,`NEW1_019`} or opponent class ∈ {MAGE, PALADIN, ROGUE, HUNTER, WARLOCK}.
- KEEP at most one of {`EX1_017`,`CS2_124`} if hand has a cost-1/2 minion OR going second.
- KEEP `EX1_610` only if opponent class ∈ {PALADIN, HUNTER, WARLOCK, WARRIOR} and hand has a cost-1/2 minion.
- KEEP `DS1_070` only if going second and hand has `CS2_172`.
- REPLACE everything else: `EX1_539`, `EX1_538`, `DS1_185`, `CS2_171`, `CS2_203`, `EX1_593`, `EX1_067`.

**Turn order**
1. Lethal check (§10). If lethal: remove Taunts with minimum resources, then all damage face. Play Beasts before `EX1_539`.
2. Trades: attack only per §8 (Taunt, free kill, damage engine, enemy board out-races us).
3. Play cards maximizing mana spent; tie-break priority by cost:
   - cost 1: `EX1_029` > `EX1_010` > `CS2_171`(only turn ≥ 6 or with KC) ; `DS1_185` only to kill a ≤2-health target or for lethal.
   - cost 2: `NEW1_019` (play first when more summons follow) > `CS2_172` > `NEW1_023` > `EX1_610` (only if no 2-drop minion or vs aggro).
   - cost 3: `NEW1_031` > `EX1_017` > `EX1_536` (if no weapon equipped) > `CS2_203` (only with an enemy Taunt or buffed target) > `CS2_124` > `EX1_538` (only with ≥2 enemy minions or lethal) > `EX1_539` (only for lethal or to kill a Taunt/threat with ≥4 health).
   - cost 4: `DS1_070` targeting highest-Attack friendly Beast.
   - cost 5: `EX1_593`. cost 6: `EX1_067`.
4. Hero power if ≥2 mana left (no target).
5. Attack face with every remaining attacker (Bow included) unless a trade rule fired.
6. `end_turn`.

**Targets**
- `EX1_539` / `DS1_185`: enemy hero if lethal or no threat; else enemy Taunt blocking; else highest-threat minion that dies to it.
- `CS2_203`: enemy Taunt with highest Health; else enemy minion with highest Attack; never a friendly minion unless forced.
- `DS1_070`: friendly Beast with highest Attack (prefer non-Stealth).
- Bow attacks: minions only if target Attack ≤ 3 and target dies; else face.

**Never**
- Never use `EX1_539`, `DS1_185` or Steady Shot on your own characters.
- Never play `EX1_538` when the enemy has no minions (illegal) or exactly one minion without lethal.
- Never attack a minion with a Stealth minion that could hit face for 4, unless rule §8.1/§8.3 applies.
- Never end a turn with ≥2 unused mana without using Steady Shot.
- Never give `target` when the legal action lists no targets; never `position` for spells/weapons.

**Face-vs-trade thresholds**
- Enemy health ≤ (our board attack + burn in hand + 2): pure face.
- Enemy board total attack ≥ our health − 5 and they could kill us within 2 turns: trade with free kills first.
- Otherwise: face, except Taunts and damage engines.

## 14. Sources

| URL | What was taken |
|---|---|
| https://icy-veins.com/hearthstone/classic-face-hunter-deck | Classic-format Face Hunter decklist (Leper, Abusive, Golem, Wolfrider, Leeroy, Buzzard, Unleash, Bow, Explosive Trap, Animal Companion, KC) and mulligan: always keep Leper Gnome + Animal Companion; vs aggro add Eaglehorn Bow + Explosive Trap; vs control nothing else. (Page blocked direct fetch; content read from search-result excerpts.) |
| https://hearthstone.wiki.gg/wiki/Face_Hunter | Archetype definition, core cards, "face damage is free because the opponent must trade back", trade only when a minion threatens your board, use burn to reach over Taunts, Steady Shot is unpreventable; weaknesses (little card draw, Taunts, Armor Up / heals). |
| https://www.hearthstonetopdecks.com/decks/face-hunter-deck-list/ | 2016 Wild list + mulligan (keep 1-2 drops; Bow vs 3-health early drops; Owl vs Taunt decks); hold a Beast for Kill Command; Owl only for big Taunts; Huffer is best companion; common mistakes (playing Arcane Golem too early, Leeroy clogging). |
| https://www.hearthstonetopdecks.com/decks/curseds-face-hunter-deck-list-guide-august-2016-season-29/ | Hero power almost every turn ("Steady Shot is like a card"); plan a kill turn; don't play defensively when behind; per-class matchup notes (Rogue: keep Bow, Steady Shot over weak minions; Druid: play around Swipe, Unleash/Explosive Trap punish wide boards; Paladin: push early; Warlock Zoo: trade early); mistake: walking a board into Explosive Trap. |
| https://www.hearthstonetopdecks.com/decks/face-hunter-deck-list-guide-standard/ | Mulligan split vs fast/slow decks; vs aggro prioritise board and trades, vs control chip + Steady Shot + KC finish; Houndmaster to protect board; avoid overextending into known AoE; note that Leper/Abusive nerfs forced the archetype to change. |
| https://www.hearthstonetopdecks.com/decks/how-to-still-go-face-standard/ | Author's assessment of the nerfs: Knife Juggler nerf "not as bad", Leper Gnome and Arcane Golem nerfs "huge" (Golem no longer a finisher); Owl for early Taunts; Wolfrider as extra pressure. |
| https://www.pocketgamer.com/hearthstone/hearthstone-strategy-guide-basic-decks | Basic Hunter plan: Beast synergy + direct damage; mulligan for 2-drops and Animal Companion; use damage cards as removal for board control when needed. |
| `meta.md` §2-3 (project) and `pkg/hs-arena-0.2.2/src/hs_arena/_vendor/fireplace/cards/classic/hunter.py` | Current card text/stats; Greedy Mage list; engine checks: Unleash needs ≥1 enemy minion, Houndmaster can be played without a Beast, Animal Companion = Misha 4/4 Taunt / Leokk 2/4 / Huffer 4/2 Charge. |
