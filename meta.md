# Card Pool, Game Version & Meta Research

Companion to `task.md`. Part 1 is generated from `pkg/hs-arena-0.2.2/data/cards.json`; Parts 2+ are research notes, added over time.

## 1. Game version

| Item | Value |
|---|---|
| Runtime | hs-arena **0.2.2**, protocol v1 |
| Pool id | `basic-classic-1` · **367 cards** (BASIC 133, CLASSIC/`EXPERT1` 234) |
| Engine | vendored **fireplace**, upstream commit `47a2572a`; card text from `CardDefs.xml` via `hearthstone_data` 251952.1 |
| Card versions | **Modern "Legacy" Basic + Classic**: every balance change up to the ~2021 Legacy/Core split is applied |
| Classes | 9 classic classes (no Demon Hunter); hero = default hero, standard 2014 hero powers |

**What this means for using online meta research:**
- It is **not** the 2014 launch pool. It's also **not** the 2021 "Classic" format, which went back to the original 2014 card versions.
  No real format was ever played on exactly this pool, so every online deck needs adapting.
- Nerfed versions are in effect, e.g. Leper Gnome 1/1, Knife Juggler 2/2, Starving Buzzard 5 mana, Unleash the Hounds 3,
  Force of Nature 5 mana (no Charge), Ancient of Lore draws 1, Keeper of the Grove 4, Hunter's Mark 2,
  Blade Flurry 4 (minions only), Arcane Golem 4/4 no Charge, Charge (spell) can't hit heroes, Warsong Commander only buffs
  Charge minions, Gadgetzan Auctioneer 6, Preparation −2, Big Game Hunter 5, Ironbeak Owl 3, Hex 4, Lightning Storm 3,
  Feral Spirit 3, Equality 4, Avenging Wrath 6, Murloc Warleader +2 Attack only, Fiery War Axe 3 mana, Cold Blood 2,
  Flame Imp 3/2 … (check the table below rather than memory).
- **Hall of Fame (removed, 29 classic cards):** Acolyte of Pain (Neutral, `EX1_007`), Auchenai Soulpriest (Priest, `EX1_591`), Azure Drake (Neutral, `EX1_284`), Captain's Parrot (Neutral, `NEW1_016`), Coldlight Oracle (Neutral, `EX1_050`), Conceal (Rogue, `EX1_128`), Divine Favor (Paladin, `EX1_349`), Divine Spirit (Priest, `CS2_236`), Doomguard (Warlock, `EX1_310`), Elite Tauren Chieftain (Neutral, `PRO_001`), Gelbin Mekkatorque (Neutral, `EX1_112`), Holy Fire (Priest, `EX1_624`), Ice Block (Mage, `EX1_295`), Ice Lance (Mage, `CS2_031`), Leeroy Jenkins (Neutral, `EX1_116`), Mind Blast (Priest, `DS1_233`), Mind Control Tech (Neutral, `EX1_085`), Molten Giant (Neutral, `EX1_620`), Mountain Giant (Neutral, `EX1_105`), Naturalize (Druid, `EX1_161`), Northshire Cleric (Priest, `CS2_235`), Old Murk-Eye (Neutral, `EX1_062`), Power Overwhelming (Warlock, `EX1_316`), Prophet Velen (Priest, `EX1_350`), Ragnaros the Firelord (Neutral, `EX1_298`), Shadowform (Priest, `EX1_625`), Spellbreaker (Neutral, `EX1_048`), Sylvanas Windrunner (Neutral, `EX1_016`), Vanish (Rogue, `NEW1_004`).
- **Blacklisted (engine bugs):** Tome of Intellect (`EX1_180`), Call of the Void (`EX1_181`), Pilfer (`EX1_182`), Barrens Stablehand (`EX1_188`), Brightwing (`EX1_189`), Bane of Doom (`EX1_320`).
- Opponents (Greedy Mage, Mystery Bot, Astra, classmates) all play from this same pool.

## 2. Card list

Format: `cost | id | name | rarity | atk/hp (weapons atk/dur) | text`. Legendary = max 1 copy. Neutral list is shared by all classes.

### Druid (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `EX1_169` | Innervate | Spell | Free |  | Gain 1 Mana Crystal this turn only. |
| 0 | `CS2_008` | Moonfire | Spell | Free |  | Deal 1 damage. |
| 1 | `CS2_005` | Claw | Spell | Free |  | Give your hero +2 Attack this turn. Gain 2 Armor. |
| 1 | `EX1_578` | Savagery | Spell | Rare |  | Deal damage equal to your hero's Attack to a minion. |
| 2 | `CS2_009` | Mark of the Wild | Spell | Free |  | Give a minion Taunt and +2/+2. (+2 Attack/+2 Health) |
| 2 | `EX1_160` | Power of the Wild | Spell | Common |  | Choose One - Give your minions +1/+1; or Summon a 3/2 Panther. |
| 2 | `EX1_154` | Wrath | Spell | Common |  | Choose One - Deal 3 damage to a minion; or 1 damage and draw a card. |
| 3 | `CS2_007` | Healing Touch | Spell | Free |  | Restore 8 Health. |
| 3 | `EX1_155` | Mark of Nature | Spell | Common |  | Choose One - Give a minion +4 Attack; or +4 Health and Taunt. |
| 3 | `CS2_011` | Savage Roar | Spell | Free |  | Give your characters +2 Attack this turn. |
| 3 | `CS2_013` | Wild Growth | Spell | Free |  | Gain an empty Mana Crystal. |
| 4 | `EX1_570` | Bite | Spell | Rare |  | Give your hero +4 Attack this turn. Gain 4 Armor. |
| 4 | `EX1_166` | Keeper of the Grove | Minion | Rare | 2/2 | Choose One - Deal 2 damage; or Silence a minion. |
| 4 | `EX1_158` | Soul of the Forest | Spell | Common |  | Give your minions "Deathrattle: Summon a 2/2 Treant." |
| 4 | `CS2_012` | Swipe | Spell | Free |  | Deal 4 damage to an enemy and 1 damage to all other enemies. |
| 5 | `EX1_165` | Druid of the Claw | Minion | Common | 4/4 | Choose One - Transform into a 4/4 with Charge; or a 4/6 with Taunt. |
| 5 | `EX1_571` | Force of Nature | Spell | Epic |  | Summon three 2/2 Treants. |
| 5 | `NEW1_007` | Starfall | Spell | Rare |  | Choose One - Deal 5 damage to a minion; or 2 damage to all enemy minions. |
| 6 | `EX1_164` | Nourish | Spell | Rare |  | Choose One - Gain 2 Mana Crystals; or Draw 3 cards. |
| 6 | `EX1_173` | Starfire | Spell | Free |  | Deal 5 damage. Draw a card. |
| 7 | `NEW1_008` | Ancient of Lore | Minion | Epic | 5/5 | Choose One - Draw a card; or Restore 5 Health. |
| 7 | `EX1_178` | Ancient of War | Minion | Epic | 5/5 | Choose One - +5 Attack; or +5 Health and Taunt. |
| 8 | `EX1_183` | Gift of the Wild | Spell | Common |  | Give your minions +2/+2 and Taunt. |
| 8 | `CS2_232` | Ironbark Protector | Minion | Free | 8/8 | Taunt |
| 9 | `EX1_573` | Cenarius | Minion | Legendary | 5/8 | Choose One - Give your other minions +2/+2; or Summon two 2/2 Treants with Taunt. |

### Hunter (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 1 | `DS1_185` | Arcane Shot | Spell | Free |  | Deal 2 damage. |
| 1 | `EX1_549` | Bestial Wrath | Spell | Epic |  | Give a friendly Beast +2 Attack and Immune this turn. |
| 1 | `DS1_175` | Timber Wolf | Minion | Free | 1/1 | Your other Beasts have +1 Attack. |
| 1 | `DS1_184` | Tracking | Spell | Free |  | Look at the top 3 cards of your deck. Draw one and discard the others. |
| 2 | `EX1_610` | Explosive Trap | Spell | Common |  | Secret: When your hero is attacked, deal 2 damage to all enemies. |
| 2 | `EX1_544` | Flare | Spell | Rare |  | All minions lose Stealth. Destroy all enemy Secrets. Draw a card. |
| 2 | `EX1_611` | Freezing Trap | Spell | Common |  | Secret: When an enemy minion attacks, return it to its owner's hand. It costs (2) more. |
| 2 | `CS2_084` | Hunter's Mark | Spell | Free |  | Change a minion's Health to 1. |
| 2 | `EX1_533` | Misdirection | Spell | Rare |  | Secret: When an enemy attacks your hero, instead it attacks another random character. |
| 2 | `EX1_531` | Scavenging Hyena | Minion | Common | 2/2 | Whenever a friendly Beast dies, gain +2/+1. |
| 2 | `EX1_554` | Snake Trap | Spell | Epic |  | Secret: When one of your minions is attacked, summon three 1/1 Snakes. |
| 2 | `EX1_609` | Snipe | Spell | Common |  | Secret: After your opponent plays a minion, deal 4 damage to it. |
| 3 | `NEW1_031` | Animal Companion | Spell | Free |  | Summon a random Beast Companion. |
| 3 | `EX1_617` | Deadly Shot | Spell | Common |  | Destroy a random enemy minion. |
| 3 | `EX1_536` | Eaglehorn Bow | Weapon | Rare | 3/2 | Whenever a friendly Secret is revealed, gain +1 Durability. |
| 3 | `EX1_539` | Kill Command | Spell | Free |  | Deal 3 damage. If you control a Beast, deal 5 damage instead. |
| 3 | `EX1_538` | Unleash the Hounds | Spell | Common |  | For each enemy minion, summon a 1/1 Hound with Charge. |
| 4 | `DS1_070` | Houndmaster | Minion | Free | 4/3 | Battlecry: Give a friendly Beast +2/+2 and Taunt. |
| 4 | `DS1_183` | Multi-Shot | Spell | Free |  | Deal 3 damage to two random enemy minions. |
| 5 | `EX1_537` | Explosive Shot | Spell | Rare |  | Deal 5 damage to a minion and 2 damage to adjacent ones. |
| 5 | `CS2_237` | Starving Buzzard | Minion | Free | 3/2 | Whenever you summon a Beast, draw a card. |
| 5 | `DS1_178` | Tundra Rhino | Minion | Free | 2/5 | Your Beasts have Charge. |
| 6 | `EX1_534` | Savannah Highmane | Minion | Rare | 6/5 | Deathrattle: Summon two 2/2 Hyenas. |
| 7 | `DS1_188` | Gladiator's Longbow | Weapon | Epic | 5/2 | Your hero is Immune while attacking. |
| 9 | `EX1_543` | King Krush | Minion | Legendary | 8/8 | Charge |

### Mage (24)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 1 | `EX1_277` | Arcane Missiles | Spell | Free |  | Deal 3 damage randomly split among all enemies. |
| 1 | `CS2_027` | Mirror Image | Spell | Free |  | Summon two 0/2 minions with Taunt. |
| 2 | `CS2_025` | Arcane Explosion | Spell | Free |  | Deal 1 damage to all enemy minions. |
| 2 | `CS2_024` | Frostbolt | Spell | Free |  | Deal 3 damage to a character and Freeze it. |
| 2 | `EX1_179` | Icicle | Spell | Epic |  | Deal 2 damage to a minion. If it's Frozen, draw a card. |
| 2 | `NEW1_012` | Mana Wyrm | Minion | Common | 1/3 | Whenever you cast a spell, gain +1 Attack. |
| 2 | `EX1_608` | Sorcerer's Apprentice | Minion | Common | 3/2 | Your spells cost (1) less. |
| 3 | `CS2_023` | Arcane Intellect | Spell | Free |  | Draw 2 cards. |
| 3 | `EX1_287` | Counterspell | Spell | Rare |  | Secret: When your opponent casts a spell, Counter it. |
| 3 | `CS2_026` | Frost Nova | Spell | Free |  | Freeze all enemy minions. |
| 3 | `EX1_289` | Ice Barrier | Spell | Common |  | Secret: When your hero is attacked, gain 8 Armor. |
| 3 | `EX1_612` | Kirin Tor Mage | Minion | Rare | 4/3 | Battlecry: The next Secret you play this turn costs (0). |
| 3 | `EX1_294` | Mirror Entity | Spell | Common |  | Secret: After your opponent plays a minion, summon a copy of it. |
| 3 | `tt_010` | Spellbender | Spell | Epic |  | Secret: When an enemy casts a spell on a minion, summon a 1/3 as the new target. |
| 3 | `EX1_594` | Vaporize | Spell | Rare |  | Secret: When a minion attacks your hero, destroy it. |
| 4 | `EX1_275` | Cone of Cold | Spell | Common |  | Freeze a minion and the minions next to it, and deal 1 damage to them. |
| 4 | `EX1_274` | Ethereal Arcanist | Minion | Rare | 3/3 | If you control a Secret at the end of your turn, gain +2/+2. |
| 4 | `CS2_029` | Fireball | Spell | Free |  | Deal 6 damage. |
| 4 | `CS2_022` | Polymorph | Spell | Free |  | Transform a minion into a 1/1 Sheep. |
| 4 | `CS2_033` | Water Elemental | Minion | Free | 3/6 | Freeze any character damaged by this minion. |
| 6 | `CS2_028` | Blizzard | Spell | Rare |  | Deal 2 damage to all enemy minions and Freeze them. |
| 7 | `EX1_559` | Archmage Antonidas | Minion | Legendary | 5/7 | Whenever you cast a spell, add a 'Fireball' spell to your hand. |
| 7 | `CS2_032` | Flamestrike | Spell | Free |  | Deal 4 damage to all enemy minions. |
| 10 | `EX1_279` | Pyroblast | Spell | Epic |  | Deal 10 damage. |

### Paladin (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 1 | `CS2_087` | Blessing of Might | Spell | Free |  | Give a minion +3 Attack. |
| 1 | `EX1_363` | Blessing of Wisdom | Spell | Common |  | Choose a minion. Whenever it attacks, draw a card. |
| 1 | `EX1_132` | Eye for an Eye | Spell | Common |  | Secret: When your hero takes damage, deal that much damage to the enemy hero. |
| 1 | `EX1_371` | Hand of Protection | Spell | Free |  | Give a minion Divine Shield. |
| 1 | `EX1_360` | Humility | Spell | Free |  | Change a minion's Attack to 1. |
| 1 | `CS2_091` | Light's Justice | Weapon | Free | 1/4 |  |
| 1 | `EX1_130` | Noble Sacrifice | Spell | Common |  | Secret: When an enemy attacks, summon a 2/1 Defender as the new target. |
| 1 | `EX1_136` | Redemption | Spell | Common |  | Secret: When a friendly minion dies, return it to life with 1 Health. |
| 1 | `EX1_379` | Repentance | Spell | Common |  | Secret: After your opponent plays a minion, reduce its Health to 1. |
| 2 | `EX1_362` | Argent Protector | Minion | Common | 2/2 | Battlecry: Give a friendly minion Divine Shield. |
| 2 | `CS2_089` | Holy Light | Spell | Free |  | Restore 6 Health. |
| 3 | `EX1_382` | Aldor Peacekeeper | Minion | Rare | 3/3 | Battlecry: Change an enemy minion's Attack to 1. |
| 3 | `EX1_366` | Sword of Justice | Weapon | Epic | 1/5 | After you summon a minion, give it +1/+1 and this loses 1 Durability. |
| 4 | `CS2_092` | Blessing of Kings | Spell | Free |  | Give a minion +4/+4. (+4 Attack/+4 Health) |
| 4 | `CS2_093` | Consecration | Spell | Free |  | Deal 2 damage to all enemies. |
| 4 | `EX1_619` | Equality | Spell | Rare |  | Change the Health of ALL minions to 1. |
| 4 | `CS2_094` | Hammer of Wrath | Spell | Free |  | Deal 3 damage. Draw a card. |
| 4 | `CS2_097` | Truesilver Champion | Weapon | Free | 4/2 | Whenever your hero attacks, restore 2 Health to it. |
| 5 | `EX1_355` | Blessed Champion | Spell | Rare |  | Double a minion's Attack. |
| 5 | `EX1_365` | Holy Wrath | Spell | Rare |  | Draw a card and deal damage equal to its Cost. |
| 5 | `EX1_184` | Righteousness | Spell | Rare |  | Give your minions Divine Shield. |
| 6 | `EX1_384` | Avenging Wrath | Spell | Epic |  | Deal 8 damage randomly split among all enemies. |
| 7 | `CS2_088` | Guardian of Kings | Minion | Free | 5/6 | Battlecry: Restore 6 Health to your hero. |
| 8 | `EX1_354` | Lay on Hands | Spell | Epic |  | Restore 8 Health. Draw 3 cards. |
| 8 | `EX1_383` | Tirion Fordring | Minion | Legendary | 6/6 | Divine Shield, Taunt Deathrattle: Equip a 5/3 Ashbringer. |

### Priest (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `EX1_621` | Circle of Healing | Spell | Common |  | Restore 4 Health to ALL minions. |
| 0 | `CS2_004` | Power Word: Shield | Spell | Free |  | Give a minion +2 Health. |
| 0 | `EX1_332` | Silence | Spell | Common |  | Silence a minion. |
| 1 | `CS1_130` | Holy Smite | Spell | Free |  | Deal 3 damage to a minion. |
| 1 | `CS1_129` | Inner Fire | Spell | Common |  | Change a minion's Attack to be equal to its Health. |
| 1 | `CS2_003` | Mind Vision | Spell | Free |  | Put a copy of a random card in your opponent's hand into your hand. |
| 1 | `EX1_193` | Psychic Conjurer | Minion | Free | 1/1 | Battlecry: Copy a card in your opponent’s deck and add it to your hand. |
| 1 | `EX1_192` | Radiance | Spell | Free |  | Restore 5 Health to your hero. |
| 1 | `EX1_196` | Scarlet Subjugator | Minion | Rare | 2/1 | Battlecry: Give an enemy minion -2 Attack until your next turn. |
| 2 | `EX1_195` | Kul Tiran Chaplain | Minion | Rare | 2/3 | Battlecry: Give a friendly minion +2 Health. |
| 2 | `EX1_341` | Lightwell | Minion | Rare | 0/5 | At the start of your turn, restore 3 Health to a damaged friendly character. |
| 2 | `EX1_622` | Shadow Word: Death | Spell | Free |  | Destroy a minion with 5 or more Attack. |
| 2 | `CS2_234` | Shadow Word: Pain | Spell | Free |  | Destroy a minion with 3 or less Attack. |
| 2 | `EX1_339` | Thoughtsteal | Spell | Common |  | Copy 2 cards in your opponent's deck and add them to your hand. |
| 3 | `EX1_334` | Shadow Madness | Spell | Rare |  | Gain control of an enemy minion with 3 or less Attack until end of turn. |
| 4 | `CS1_112` | Holy Nova | Spell | Free |  | Deal 2 damage to all enemy minions. Restore 2 Health to all friendly characters. |
| 4 | `EX1_335` | Lightspawn | Minion | Common | 0/5 | This minion's Attack is always equal to its Health. |
| 4 | `EX1_626` | Mass Dispel | Spell | Rare |  | Silence all enemy minions. Draw a card. |
| 4 | `EX1_345` | Mindgames | Spell | Epic |  | Put a copy of a random minion from your opponent's deck into the battlefield. |
| 4 | `EX1_194` | Power Infusion | Spell | Free |  | Give a minion +2/+6. |
| 4 | `EX1_197` | Shadow Word: Ruin | Spell | Epic |  | Destroy all minions with 5 or more Attack. |
| 5 | `EX1_623` | Temple Enforcer | Minion | Common | 5/6 | Battlecry: Give a friendly minion +3 Health. |
| 6 | `EX1_091` | Cabal Shadow Priest | Minion | Epic | 4/5 | Battlecry: Take control of an enemy minion that has 2 or less Attack. |
| 8 | `EX1_198` | Natalie Seline | Minion | Legendary | 8/1 | Battlecry: Destroy a minion and gain its Health. |
| 10 | `CS1_113` | Mind Control | Spell | Free |  | Take control of an enemy minion. |

### Rogue (24)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `CS2_072` | Backstab | Spell | Free |  | Deal 2 damage to an undamaged minion. |
| 0 | `EX1_145` | Preparation | Spell | Epic |  | The next spell you cast this turn costs (2) less. |
| 0 | `EX1_144` | Shadowstep | Spell | Common |  | Return a friendly minion to your hand. It costs (2) less. |
| 1 | `CS2_074` | Deadly Poison | Spell | Free |  | Give your weapon +2 Attack. |
| 1 | `CS2_075` | Sinister Strike | Spell | Free |  | Deal 3 damage to the enemy hero. |
| 2 | `EX1_126` | Betrayal | Spell | Common |  | Force an enemy minion to deal its damage to the minions next to it. |
| 2 | `CS2_073` | Cold Blood | Spell | Common |  | Give a minion +2 Attack. Combo: +4 Attack instead. |
| 2 | `EX1_131` | Defias Ringleader | Minion | Common | 2/2 | Combo: Summon a 2/1 Defias Bandit. |
| 2 | `EX1_124` | Eviscerate | Spell | Common |  | Deal 2 damage. Combo: Deal 4 damage instead. |
| 2 | `EX1_522` | Patient Assassin | Minion | Epic | 1/1 | Stealth Poisonous |
| 2 | `EX1_581` | Sap | Spell | Free |  | Return an enemy minion to your opponent's hand. |
| 2 | `EX1_278` | Shiv | Spell | Free |  | Deal 1 damage. Draw a card. |
| 3 | `EX1_613` | Edwin VanCleef | Minion | Legendary | 2/2 | Combo: Gain +2/+2 for each other card you've played this turn. |
| 3 | `EX1_129` | Fan of Knives | Spell | Free |  | Deal 1 damage to all enemy minions. Draw a card. |
| 3 | `EX1_137` | Headcrack | Spell | Rare |  | Deal 2 damage to the enemy hero. Combo: Return this to your hand next turn. |
| 3 | `EX1_133` | Perdition's Blade | Weapon | Rare | 2/2 | Battlecry: Deal 1 damage. Combo: Deal 2 instead. |
| 3 | `EX1_134` | SI:7 Agent | Minion | Rare | 3/3 | Combo: Deal 2 damage. |
| 4 | `CS2_233` | Blade Flurry | Spell | Rare |  | Destroy your weapon and deal its damage to all enemy minions. |
| 4 | `NEW1_014` | Master of Disguise | Minion | Rare | 4/4 | Battlecry: Give a friendly minion Stealth until your next turn. |
| 4 | `EX1_191` | Plaguebringer | Minion | Free | 3/3 | Battlecry: Give a friendly minion Poisonous. |
| 5 | `CS2_080` | Assassin's Blade | Weapon | Free | 3/4 |  |
| 5 | `CS2_076` | Assassinate | Spell | Free |  | Destroy an enemy minion. |
| 6 | `NEW1_005` | Kidnapper | Minion | Epic | 5/3 | Combo: Return a minion to its owner's hand. |
| 7 | `CS2_077` | Sprint | Spell | Free |  | Draw 4 cards. |

### Shaman (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `CS2_041` | Ancestral Healing | Spell | Free |  | Restore a minion to full Health and give it Taunt. |
| 0 | `EX1_244` | Totemic Might | Spell | Free |  | Give your Totems +2 Health. |
| 1 | `EX1_243` | Dust Devil | Minion | Common | 3/1 | Windfury. Overload: (2) |
| 1 | `EX1_245` | Earth Shock | Spell | Common |  | Silence a minion, then deal 1 damage to it. |
| 1 | `EX1_251` | Forked Lightning | Spell | Common |  | Deal 2 damage to 2 random enemy minions. Overload: (2) |
| 1 | `CS2_037` | Frost Shock | Spell | Free |  | Deal 1 damage to an enemy character and Freeze it. |
| 1 | `EX1_238` | Lightning Bolt | Spell | Common |  | Deal 3 damage. Overload: (1) |
| 2 | `CS2_038` | Ancestral Spirit | Spell | Rare |  | Give a minion "Deathrattle: Resummon this minion." |
| 2 | `CS2_045` | Rockbiter Weapon | Spell | Free |  | Give a friendly character +3 Attack this turn. |
| 2 | `EX1_247` | Stormforged Axe | Weapon | Common | 2/3 | Overload: (1) |
| 2 | `CS2_039` | Windfury | Spell | Free |  | Give a minion Windfury. |
| 3 | `CS2_053` | Far Sight | Spell | Epic |  | Draw a card. That card costs (3) less. |
| 3 | `EX1_248` | Feral Spirit | Spell | Rare |  | Summon two 2/3 Spirit Wolves with Taunt. Overload: (2) |
| 3 | `EX1_565` | Flametongue Totem | Minion | Free | 0/3 | Adjacent minions have +2 Attack. |
| 3 | `EX1_241` | Lava Burst | Spell | Rare |  | Deal 5 damage. Overload: (2) |
| 3 | `EX1_259` | Lightning Storm | Spell | Rare |  | Deal 2-3 damage to all enemy minions. Overload: (2) |
| 3 | `EX1_575` | Mana Tide Totem | Minion | Rare | 0/3 | At the end of your turn, draw a card. |
| 3 | `EX1_258` | Unbound Elemental | Minion | Common | 2/4 | Whenever you play a card with Overload, gain +1/+1. |
| 4 | `EX1_246` | Hex | Spell | Free |  | Transform a minion into a 0/1 Frog with Taunt. |
| 4 | `EX1_587` | Windspeaker | Minion | Free | 3/3 | Battlecry: Give a friendly minion Windfury. |
| 5 | `CS2_046` | Bloodlust | Spell | Free |  | Give your minions +3 Attack this turn. |
| 5 | `EX1_567` | Doomhammer | Weapon | Epic | 2/8 | Windfury, Overload: (2) |
| 5 | `EX1_250` | Earth Elemental | Minion | Epic | 7/8 | Taunt Overload: (3) |
| 6 | `CS2_042` | Fire Elemental | Minion | Free | 6/5 | Battlecry: Deal 3 damage. |
| 8 | `NEW1_010` | Al'Akir the Windlord | Minion | Legendary | 3/5 | Charge, Divine Shield, Taunt, Windfury |

### Warlock (23)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `NEW1_003` | Sacrificial Pact | Spell | Free |  | Destroy a friendly Demon. Restore 5 Health to your hero. |
| 1 | `CS2_059` | Blood Imp | Minion | Common | 0/1 | Stealth. At the end of your turn, give another random friendly minion +1 Health. |
| 1 | `CS2_063` | Corruption | Spell | Free |  | Choose an enemy minion. At the start of your turn, destroy it. |
| 1 | `EX1_319` | Flame Imp | Minion | Common | 3/2 | Battlecry: Deal 3 damage to your hero. |
| 1 | `EX1_302` | Mortal Coil | Spell | Free |  | Deal 1 damage to a minion. If that kills it, draw a card. |
| 1 | `EX1_308` | Soulfire | Spell | Free |  | Deal 4 damage. Discard a random card. |
| 1 | `CS2_065` | Voidwalker | Minion | Free | 1/3 | Taunt |
| 2 | `EX1_596` | Demonfire | Spell | Common |  | Deal 2 damage to a minion. If it’s a friendly Demon, give it +2/+2 instead. |
| 2 | `EX1_306` | Felstalker | Minion | Free | 4/3 | Battlecry: Discard a random card. |
| 3 | `CS2_061` | Drain Life | Spell | Free |  | Deal 2 damage. Restore 2 Health to your hero. |
| 3 | `EX1_301` | Felguard | Minion | Rare | 3/5 | Taunt Battlecry: Destroy one of your Mana Crystals. |
| 3 | `EX1_317` | Sense Demons | Spell | Common |  | Draw 2 Demons from your deck. |
| 3 | `CS2_057` | Shadow Bolt | Spell | Free |  | Deal 4 damage to a minion. |
| 3 | `EX1_304` | Void Terror | Minion | Rare | 3/3 | Battlecry: Destroy both adjacent minions and gain their Attack and Health. |
| 4 | `CS2_062` | Hellfire | Spell | Free |  | Deal 3 damage to ALL characters. |
| 4 | `EX1_313` | Pit Lord | Minion | Epic | 5/6 | Battlecry: Deal 5 damage to your hero. |
| 4 | `EX1_303` | Shadowflame | Spell | Rare |  | Destroy a friendly minion and deal its Attack damage to all enemy minions. |
| 4 | `EX1_315` | Summoning Portal | Minion | Common | 0/4 | Your minions cost (2) less, but not less than (1). |
| 6 | `CS2_064` | Dread Infernal | Minion | Free | 6/6 | Battlecry: Deal 1 damage to ALL other characters. |
| 6 | `EX1_309` | Siphon Soul | Spell | Rare |  | Destroy a minion. Restore 3 Health to your hero. |
| 7 | `EX1_185` | Siegebreaker | Minion | Rare | 5/8 | Taunt Your other Demons have +1 Attack. |
| 8 | `EX1_312` | Twisting Nether | Spell | Epic |  | Destroy all minions. |
| 9 | `EX1_323` | Lord Jaraxxus | Minion | Legendary | 3/15 | Battlecry: Destroy your hero and replace it with Lord Jaraxxus. |

### Warrior (25)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `EX1_607` | Inner Rage | Spell | Common |  | Deal 1 damage to a minion and give it +2 Attack. |
| 1 | `CS2_103` | Charge | Spell | Free |  | Give a friendly minion Charge. It can't attack heroes this turn. |
| 1 | `EX1_410` | Shield Slam | Spell | Epic |  | Deal 1 damage to a minion for each Armor you have. |
| 1 | `EX1_409` | Upgrade! | Spell | Rare |  | If you have a weapon, give it +1/+1. Otherwise equip a 1/3 weapon. |
| 1 | `EX1_400` | Whirlwind | Spell | Free |  | Deal 1 damage to ALL minions. |
| 2 | `EX1_402` | Armorsmith | Minion | Rare | 1/4 | Whenever a friendly minion takes damage, gain 1 Armor. |
| 2 | `EX1_392` | Battle Rage | Spell | Common |  | Draw a card for each damaged friendly character. |
| 2 | `CS2_114` | Cleave | Spell | Free |  | Deal 2 damage to two random enemy minions. |
| 2 | `NEW1_036` | Commanding Shout | Spell | Rare |  | Your minions can't be reduced below 1 Health this turn. Draw a card. |
| 2 | `EX1_603` | Cruel Taskmaster | Minion | Common | 2/2 | Battlecry: Deal 1 damage to a minion and give it +2 Attack. |
| 2 | `CS2_108` | Execute | Spell | Free |  | Destroy a damaged enemy minion. |
| 2 | `CS2_105` | Heroic Strike | Spell | Free |  | Give your hero +4 Attack this turn. |
| 2 | `CS2_104` | Rampage | Spell | Common |  | Give a damaged minion +3/+3. |
| 2 | `EX1_391` | Slam | Spell | Common |  | Deal 2 damage to a minion. If it survives, draw a card. |
| 3 | `CS2_106` | Fiery War Axe | Weapon | Free | 3/2 |  |
| 3 | `EX1_604` | Frothing Berserker | Minion | Rare | 2/4 | Whenever a minion takes damage, gain +1 Attack. |
| 3 | `EX1_606` | Shield Block | Spell | Free |  | Gain 5 Armor. Draw a card. |
| 3 | `EX1_084` | Warsong Commander | Minion | Free | 2/3 | Your Charge minions have +1 Attack. |
| 4 | `EX1_398` | Arathi Weaponsmith | Minion | Common | 3/3 | Battlecry: Equip a 2/2 weapon. |
| 4 | `NEW1_011` | Kor'kron Elite | Minion | Free | 4/3 | Charge |
| 4 | `EX1_408` | Mortal Strike | Spell | Rare |  | Deal 4 damage. If you have 12 or less Health, deal 6 instead. |
| 5 | `CS2_112` | Arcanite Reaper | Weapon | Free | 5/2 |  |
| 5 | `EX1_407` | Brawl | Spell | Epic |  | Destroy all minions except one. (chosen randomly) |
| 7 | `EX1_411` | Gorehowl | Weapon | Epic | 7/1 | Attacking a minion costs 1 Attack instead of 1 Durability. |
| 8 | `EX1_414` | Grommash Hellscream | Minion | Legendary | 4/9 | Charge Has +6 Attack while damaged. |

### Neutral (146)

| Cost | Id | Name | Type | Rarity | Stats | Text |
|---:|---|---|---|---|---|---|
| 0 | `CS2_231` | Wisp | Minion | Common | 1/1 |  |
| 1 | `CS2_188` | Abusive Sergeant | Minion | Common | 1/1 | Battlecry: Give a minion +2 Attack this turn. |
| 1 | `EX1_009` | Angry Chicken | Minion | Rare | 1/1 | Has +5 Attack while damaged. |
| 1 | `EX1_008` | Argent Squire | Minion | Common | 1/1 | Divine Shield |
| 1 | `NEW1_025` | Bloodsail Corsair | Minion | Rare | 1/2 | Battlecry: Remove 1 Durability from your opponent's weapon. |
| 1 | `CS2_189` | Elven Archer | Minion | Free | 1/1 | Battlecry: Deal 1 damage. |
| 1 | `CS1_042` | Goldshire Footman | Minion | Free | 1/2 | Taunt |
| 1 | `EX1_508` | Grimscale Oracle | Minion | Free | 1/1 | Your other Murlocs have +1 Attack. |
| 1 | `NEW1_017` | Hungry Crab | Minion | Epic | 1/2 | Battlecry: Destroy a Murloc and gain +2/+2. |
| 1 | `EX1_029` | Leper Gnome | Minion | Common | 1/1 | Deathrattle: Deal 2 damage to the enemy hero. |
| 1 | `EX1_001` | Lightwarden | Minion | Rare | 1/2 | Whenever a character is healed, gain +2 Attack. |
| 1 | `CS2_168` | Murloc Raider | Minion | Free | 2/1 |  |
| 1 | `EX1_509` | Murloc Tidecaller | Minion | Rare | 1/2 | Whenever you summon a Murloc, gain +1 Attack. |
| 1 | `EX1_080` | Secretkeeper | Minion | Rare | 1/2 | Whenever a Secret is played, gain +1/+1. |
| 1 | `EX1_405` | Shieldbearer | Minion | Common | 0/4 | Taunt |
| 1 | `CS2_146` | Southsea Deckhand | Minion | Common | 2/1 | Has Charge while you have a weapon equipped. |
| 1 | `CS2_171` | Stonetusk Boar | Minion | Free | 1/1 | Charge |
| 1 | `EX1_011` | Voodoo Doctor | Minion | Free | 2/1 | Battlecry: Restore 2 Health. |
| 1 | `EX1_010` | Worgen Infiltrator | Minion | Common | 2/1 | Stealth |
| 1 | `CS2_169` | Young Dragonhawk | Minion | Common | 1/1 | Windfury |
| 1 | `EX1_004` | Young Priestess | Minion | Rare | 2/1 | At the end of your turn, give another random friendly minion +1 Health. |
| 2 | `EX1_066` | Acidic Swamp Ooze | Minion | Free | 3/2 | Battlecry: Destroy your opponent's weapon. |
| 2 | `EX1_393` | Amani Berserker | Minion | Common | 2/3 | Has +3 Attack while damaged. |
| 2 | `EX1_045` | Ancient Watcher | Minion | Rare | 4/5 | Can't attack. |
| 2 | `CS2_172` | Bloodfen Raptor | Minion | Free | 3/2 |  |
| 2 | `EX1_012` | Bloodmage Thalnos | Minion | Legendary | 1/1 | Spell Damage +1 Deathrattle: Draw a card. |
| 2 | `NEW1_018` | Bloodsail Raider | Minion | Common | 2/3 | Battlecry: Gain Attack equal to the Attack of your weapon. |
| 2 | `CS2_173` | Bluegill Warrior | Minion | Free | 2/1 | Charge |
| 2 | `EX1_059` | Crazed Alchemist | Minion | Rare | 2/2 | Battlecry: Swap the Attack and Health of a minion. |
| 2 | `EX1_162` | Dire Wolf Alpha | Minion | Common | 2/2 | Adjacent minions have +1 Attack. |
| 2 | `NEW1_021` | Doomsayer | Minion | Epic | 0/7 | At the start of your turn, destroy ALL minions. |
| 2 | `NEW1_023` | Faerie Dragon | Minion | Common | 3/2 | Can't be targeted by spells or Hero Powers. |
| 2 | `CS2_121` | Frostwolf Grunt | Minion | Free | 2/2 | Taunt |
| 2 | `NEW1_019` | Knife Juggler | Minion | Rare | 2/2 | After you summon a minion, deal 1 damage to a random enemy. |
| 2 | `CS2_142` | Kobold Geomancer | Minion | Free | 2/2 | Spell Damage +1 |
| 2 | `EX1_096` | Loot Hoarder | Minion | Common | 2/1 | Deathrattle: Draw a card. |
| 2 | `EX1_100` | Lorewalker Cho | Minion | Legendary | 0/4 | Whenever a player casts a spell, put a copy into the other player’s hand. |
| 2 | `EX1_082` | Mad Bomber | Minion | Common | 3/2 | Battlecry: Deal 3 damage randomly split between all other characters. |
| 2 | `EX1_055` | Mana Addict | Minion | Rare | 1/3 | Whenever you cast a spell, gain +2 Attack this turn. |
| 2 | `EX1_616` | Mana Wraith | Minion | Rare | 2/2 | ALL minions cost (1) more. |
| 2 | `NEW1_037` | Master Swordsmith | Minion | Rare | 1/3 | At the end of your turn, give another random friendly minion +1 Attack. |
| 2 | `NEW1_029` | Millhouse Manastorm | Minion | Legendary | 4/4 | Battlecry: Enemy spells cost (0) next turn. |
| 2 | `EX1_506` | Murloc Tidehunter | Minion | Free | 2/1 | Battlecry: Summon a 1/1 Murloc Scout. |
| 2 | `EX1_557` | Nat Pagle | Minion | Legendary | 0/4 | At the start of your turn, you have a 50% chance to draw an extra card. |
| 2 | `EX1_015` | Novice Engineer | Minion | Free | 1/1 | Battlecry: Draw a card. |
| 2 | `EX1_076` | Pint-Sized Summoner | Minion | Rare | 2/2 | The first minion you play each turn costs (1) less. |
| 2 | `CS2_120` | River Crocolisk | Minion | Free | 2/3 |  |
| 2 | `EX1_058` | Sunfury Protector | Minion | Rare | 2/3 | Battlecry: Give adjacent minions Taunt. |
| 2 | `NEW1_020` | Wild Pyromancer | Minion | Rare | 3/2 | After you cast a spell, deal 1 damage to ALL minions. |
| 2 | `EX1_049` | Youthful Brewmaster | Minion | Common | 3/2 | Battlecry: Return a friendly minion from the battlefield to your hand. |
| 3 | `EX1_006` | Alarm-o-Bot | Minion | Rare | 0/3 | At the start of your turn, swap this minion with a random one in your hand. |
| 3 | `EX1_089` | Arcane Golem | Minion | Rare | 4/4 | Battlecry: Give your opponent a Mana Crystal. |
| 3 | `EX1_590` | Blood Knight | Minion | Epic | 3/3 | Battlecry: All minions lose Divine Shield. Gain +3/+3 for each Shield lost. |
| 3 | `EX1_103` | Coldlight Seer | Minion | Rare | 2/3 | Battlecry: Give your other Murlocs +2 Health. |
| 3 | `EX1_582` | Dalaran Mage | Minion | Free | 1/4 | Spell Damage +1 |
| 3 | `EX1_102` | Demolisher | Minion | Rare | 1/4 | At the start of your turn, deal 2 damage to a random enemy. |
| 3 | `CS2_117` | Earthen Ring Farseer | Minion | Common | 3/3 | Battlecry: Restore 3 Health. |
| 3 | `EX1_170` | Emperor Cobra | Minion | Rare | 2/3 | Poisonous |
| 3 | `tt_004` | Flesheating Ghoul | Minion | Common | 2/3 | Whenever a minion dies, gain +1 Attack. |
| 3 | `EX1_556` | Harvest Golem | Minion | Common | 2/3 | Deathrattle: Summon a 2/1 Damaged Golem. |
| 3 | `EX1_597` | Imp Master | Minion | Rare | 1/5 | At the end of your turn, deal 1 damage to this minion and summon a 1/1 Imp. |
| 3 | `CS2_181` | Injured Blademaster | Minion | Rare | 4/7 | Battlecry: Deal 4 damage to HIMSELF. |
| 3 | `CS2_203` | Ironbeak Owl | Minion | Common | 2/1 | Battlecry: Silence a minion. |
| 3 | `CS2_141` | Ironforge Rifleman | Minion | Free | 2/2 | Battlecry: Deal 1 damage. |
| 3 | `CS2_125` | Ironfur Grizzly | Minion | Free | 3/3 | Taunt |
| 3 | `EX1_017` | Jungle Panther | Minion | Common | 4/2 | Stealth |
| 3 | `EX1_014` | King Mukla | Minion | Legendary | 5/5 | Battlecry: Give your opponent 2 Bananas. |
| 3 | `CS2_118` | Magma Rager | Minion | Free | 5/1 |  |
| 3 | `EX1_507` | Murloc Warleader | Minion | Epic | 3/3 | Your other Murlocs have +2 Attack. |
| 3 | `EX1_044` | Questing Adventurer | Minion | Rare | 2/2 | Whenever you play a card, gain +1/+1. |
| 3 | `EX1_412` | Raging Worgen | Minion | Common | 3/3 | Has +1 Attack and Windfury while damaged. |
| 3 | `CS2_122` | Raid Leader | Minion | Free | 2/2 | Your other minions have +1 Attack. |
| 3 | `CS2_196` | Razorfen Hunter | Minion | Free | 2/3 | Battlecry: Summon a 1/1 Boar. |
| 3 | `EX1_020` | Scarlet Crusader | Minion | Common | 3/1 | Divine Shield |
| 3 | `EX1_019` | Shattered Sun Cleric | Minion | Free | 3/2 | Battlecry: Give a friendly minion +1/+1. |
| 3 | `CS2_127` | Silverback Patriarch | Minion | Free | 1/4 | Taunt |
| 3 | `NEW1_027` | Southsea Captain | Minion | Epic | 3/3 | Your other Pirates have +1/+1. |
| 3 | `EX1_390` | Tauren Warrior | Minion | Common | 2/3 | Taunt Has +3 Attack while damaged. |
| 3 | `EX1_021` | Thrallmar Farseer | Minion | Common | 2/3 | Windfury |
| 3 | `EX1_083` | Tinkmaster Overspark | Minion | Legendary | 3/3 | Battlecry: Transform another random minion into a 5/5 Devilsaur or a 1/1 Squirrel. |
| 3 | `CS2_124` | Wolfrider | Minion | Free | 3/1 | Charge |
| 4 | `EX1_057` | Ancient Brewmaster | Minion | Common | 5/4 | Battlecry: Return a friendly minion from the battlefield to your hand. |
| 4 | `EX1_584` | Ancient Mage | Minion | Rare | 2/5 | Battlecry: Give adjacent minions Spell Damage +1. |
| 4 | `CS2_182` | Chillwind Yeti | Minion | Free | 4/5 |  |
| 4 | `EX1_595` | Cult Master | Minion | Common | 4/2 | After a friendly minion dies, draw a card. |
| 4 | `EX1_046` | Dark Iron Dwarf | Minion | Common | 4/4 | Battlecry: Give a minion +2 Attack this turn. |
| 4 | `EX1_093` | Defender of Argus | Minion | Rare | 2/3 | Battlecry: Give adjacent minions +1/+1 and Taunt. |
| 4 | `EX1_025` | Dragonling Mechanic | Minion | Free | 2/4 | Battlecry: Summon a 2/1 Mechanical Dragonling. |
| 4 | `NEW1_022` | Dread Corsair | Minion | Common | 3/3 | Taunt Costs (1) less per Attack of your weapon. |
| 4 | `CS2_147` | Gnomish Inventor | Minion | Free | 2/4 | Battlecry: Draw a card. |
| 4 | `EX1_396` | Mogu'shan Warden | Minion | Common | 1/7 | Taunt |
| 4 | `CS2_119` | Oasis Snapjaw | Minion | Free | 2/7 |  |
| 4 | `CS2_197` | Ogre Magi | Minion | Free | 4/4 | Spell Damage +1 |
| 4 | `EX1_186` | SI:7 Infiltrator | Minion | Rare | 5/4 | Battlecry: Destroy a random enemy Secret. |
| 4 | `CS2_179` | Sen'jin Shieldmasta | Minion | Free | 3/5 | Taunt |
| 4 | `EX1_023` | Silvermoon Guardian | Minion | Common | 3/3 | Divine Shield |
| 4 | `CS2_131` | Stormwind Knight | Minion | Free | 2/5 | Charge |
| 4 | `EX1_043` | Twilight Drake | Minion | Rare | 4/1 | Battlecry: Gain +1 Health for each card in your hand. |
| 4 | `NEW1_026` | Violet Teacher | Minion | Rare | 3/5 | Whenever you cast a spell, summon a 1/1 Violet Apprentice. |
| 5 | `EX1_097` | Abomination | Minion | Rare | 4/4 | Taunt. Deathrattle: Deal 2 damage to ALL characters. |
| 5 | `EX1_005` | Big Game Hunter | Minion | Epic | 4/2 | Battlecry: Destroy a minion with 7 or more Attack. |
| 5 | `CS2_187` | Booty Bay Bodyguard | Minion | Free | 5/4 | Taunt |
| 5 | `NEW1_024` | Captain Greenskin | Minion | Legendary | 5/4 | Battlecry: Give your weapon +1/+1. |
| 5 | `DS1_055` | Darkscale Healer | Minion | Free | 4/5 | Battlecry: Restore 2 Health to all friendly characters. |
| 5 | `EX1_564` | Faceless Manipulator | Minion | Epic | 3/3 | Battlecry: Choose a minion and become a copy of it. |
| 5 | `CS1_069` | Fen Creeper | Minion | Common | 3/6 | Taunt |
| 5 | `CS2_226` | Frostwolf Warlord | Minion | Free | 4/4 | Battlecry: Gain +1/+1 for each other friendly minion on the battlefield. |
| 5 | `EX1_399` | Gurubashi Berserker | Minion | Free | 2/7 | Whenever this minion takes damage, gain +3 Attack. |
| 5 | `EX1_558` | Harrison Jones | Minion | Legendary | 5/4 | Battlecry: Destroy your opponent's weapon and draw cards equal to its Durability. |
| 5 | `EX1_593` | Nightblade | Minion | Free | 4/4 | Battlecry: Deal 3 damage to the enemy hero. |
| 5 | `CS2_151` | Silver Hand Knight | Minion | Common | 4/4 | Battlecry: Summon a 2/2 Squire. |
| 5 | `CS2_221` | Spiteful Smith | Minion | Common | 4/6 | Your weapon has +2 Attack while this is damaged. |
| 5 | `NEW1_041` | Stampeding Kodo | Minion | Rare | 3/5 | Battlecry: Destroy a random enemy minion with 2 or less Attack. |
| 5 | `CS2_150` | Stormpike Commando | Minion | Free | 4/2 | Battlecry: Deal 2 damage. |
| 5 | `EX1_028` | Stranglethorn Tiger | Minion | Common | 5/5 | Stealth |
| 5 | `CS2_227` | Venture Co. Mercenary | Minion | Common | 7/6 | Your minions cost (3) more. |
| 6 | `CS2_155` | Archmage | Minion | Free | 4/7 | Spell Damage +1 |
| 6 | `EX1_067` | Argent Commander | Minion | Rare | 4/2 | Charge Divine Shield |
| 6 | `CS2_200` | Boulderfist Ogre | Minion | Free | 6/7 |  |
| 6 | `EX1_110` | Cairne Bloodhoof | Minion | Legendary | 4/5 | Deathrattle: Summon a 4/5 Baine Bloodhoof. |
| 6 | `EX1_283` | Frost Elemental | Minion | Common | 5/5 | Battlecry: Freeze a character. |
| 6 | `EX1_095` | Gadgetzan Auctioneer | Minion | Rare | 4/4 | Whenever you cast a spell, draw a card. |
| 6 | `NEW1_040` | Hogger | Minion | Legendary | 4/4 | At the end of your turn, summon a 2/2 Gnoll with Taunt. |
| 6 | `CS2_162` | Lord of the Arena | Minion | Free | 6/5 | Taunt |
| 6 | `EX1_583` | Priestess of Elune | Minion | Common | 5/4 | Battlecry: Restore 4 Health to your hero. |
| 6 | `CS2_213` | Reckless Rocketeer | Minion | Free | 5/2 | Charge |
| 6 | `EX1_032` | Sunwalker | Minion | Rare | 4/5 | Taunt Divine Shield |
| 6 | `EX1_577` | The Beast | Minion | Legendary | 9/7 | Deathrattle: Summon a 3/3 Finkle Einhorn for your opponent. |
| 6 | `EX1_002` | The Black Knight | Minion | Legendary | 4/5 | Battlecry: Destroy an enemy minion with Taunt. |
| 6 | `EX1_033` | Windfury Harpy | Minion | Common | 4/5 | Windfury |
| 6 | `EX1_614` | Xavius | Minion | Legendary | 7/5 | After you play a card, summon a 2/1 Satyr. |
| 7 | `EX1_249` | Baron Geddon | Minion | Legendary | 7/5 | At the end of your turn, deal 2 damage to ALL other characters. |
| 7 | `CS2_201` | Core Hound | Minion | Free | 9/5 |  |
| 7 | `EX1_190` | High Inquisitor Whitemane | Minion | Legendary | 6/8 | Battlecry: Summon all friendly minions that died this turn. |
| 7 | `CS2_161` | Ravenholdt Assassin | Minion | Rare | 7/5 | Stealth |
| 7 | `CS2_222` | Stormwind Champion | Minion | Free | 6/6 | Your other minions have +1/+1. |
| 7 | `CS2_186` | War Golem | Minion | Free | 7/7 |  |
| 8 | `EX1_187` | Arcane Devourer | Minion | Rare | 5/5 | Whenever you cast a spell, gain +2/+2. |
| 8 | `NEW1_038` | Gruul | Minion | Legendary | 7/7 | At the end of each turn, gain +1/+1 . |
| 9 | `EX1_561` | Alexstrasza | Minion | Legendary | 8/8 | Battlecry: Set a hero's remaining Health to 15. |
| 9 | `EX1_563` | Malygos | Minion | Legendary | 4/12 | Spell Damage +5 |
| 9 | `EX1_560` | Nozdormu | Minion | Legendary | 8/8 | Players only have 15 seconds to take their turns. |
| 9 | `EX1_562` | Onyxia | Minion | Legendary | 8/8 | Battlecry: Summon 1/1 Whelps until your side of the battlefield is full. |
| 9 | `EX1_572` | Ysera | Minion | Legendary | 4/12 | At the end of your turn, add a Dream Card to your hand. |
| 10 | `NEW1_030` | Deathwing | Minion | Legendary | 12/12 | Battlecry: Destroy all other minions and discard your hand. |
| 10 | `EX1_586` | Sea Giant | Minion | Epic | 8/8 | Costs (1) less for each other minion on the battlefield. |


---

## 3. Meta research (brief, keep adding)

### 3.1 Sources and how much to trust them
| Source | Era | Note |
|---|---|---|
| [vS Data Reaper — Classic #1](https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/) (Apr 2021, 90k games) | 2021 Classic format = **original 2014 cards** | Best hard data on archetype strength. |
| [HSTopDecks — best Classic deck per class](https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/) | 2014 pro lists | Full decklists + game plans (used in 3.3). |
| [HSTopDecks — which cards changed](https://www.hearthstonetopdecks.com/which-cards-will-change-in-hearthstone-classic-format-list-of-original-unnerfed-cards-and-their-history/) | 2014 vs Legacy | Nerf list. Its "current" values sometimes differ from our pool (e.g. it says Edwin 4 mana; **our pool has Edwin at 3**). Always trust §2. |
| [Icy Veins Classic tier list](https://www.icy-veins.com/hearthstone/best-classic-decks-tier-list) (403, not fetched), [HSTopDecks 2014 meta](https://www.hearthstonetopdecks.com/hearthstone-meta-decks-shaped-hearthstone-2014/) | 2014 | Miracle Rogue S tier, Face Hunter A tier. |

⚠️ All of this is from **human ladder** play on **unnerfed** cards. Our opponents are bots/LLM agents on the **nerfed Legacy** pool,
and our pilot is a script plus a small model. Use it to pick **archetypes and card packages**, not exact lists.

### 3.2 2014/Classic meta snapshot (human ladder, original cards)
- **Tier 1:** Miracle Rogue (best at high rank, very high skill ceiling), Midrange Shaman (no bad matchups), Zoo Warlock.
- **Tier 2:** Combo/Ramp Druid, Control Warrior (beats Face Hunter, weak vs Druid/Rogue), Shockadin.
- **Tier 3 and below:** Handlock, Face Hunter (popular at low rank, loses to Control Warrior/Druid), Freeze Mage (niche Rogue/Warlock counter), Control Priest (worst).
- Matchups: Zoo > Druid; Miracle > Druid; Freeze/Handlock > Miracle; Control Warrior >> Face Hunter; Zoo > Shaman.

### 3.3 Archetypes checked against OUR pool
"Survive" = cards from the classic pro list that still exist in our pool. That alone is misleading, since many survivors are nerfed.

| Archetype | Survive | What it lost / nerfs that hurt it | Game plan | Script-friendliness | Verdict |
|---|---|---|---|---|---|
| **Zoo Warlock** | 28/30 | Doomguard (HoF); Leper 1/1, Juggler 2/2, Abusive 1/1. Soulfire 1 mana | Flood the board with cheap minions, trade efficiently, buff (Argus, Cleric, Dark Iron Dwarf), Life Tap refills | **High**: decisions are local trades plus curve. Some positioning (Argus, Dire Wolf) | **Shortlist** |
| **Midrange/Beast Hunter** | 30/30 | Buzzard 5, Unleash 3, Hunter's Mark 2, Flare 2 | Beasts curve into Houndmaster/Highmane; Kill Command reach; Steady Shot 2 dmg every turn | **High**: hero power is free damage, few combos | **Shortlist** |
| **Face Hunter** | 29/30 | Leeroy; Buzzard 5 kills the Buzzard+Unleash combo; Arcane Golem no Charge; Leper/Abusive/Juggler nerfed | Race face | **Very high** (simple), but the deck got much weaker | Maybe, as "aggro Hunter" with Midrange cards |
| **Midrange Shaman** | 28/30 | Azure Drake; Flametongue 3, Hex 4, Lightning Storm 3, Feral Spirit 3, Rockbiter 2 | Outlast aggro, board control, burst with Doomhammer/Al'Akir/Rockbiter | Medium: Overload planning + Flametongue adjacency | Candidate |
| **Shockadin (Aggro Paladin)** | 27/30 | Divine Favor, Leeroy; Equality 4 | Cheap minions + weapons + Avenging Wrath | High | Weakened (no refill) |
| **Control Paladin** | 27/30 | Acolyte, Azure Drake; Equality 4 | Removal + Taunts + heal, win with Tirion | Medium (long games = more decisions, timeout risk) | Candidate vs aggro bots |
| **Miracle Rogue** | 26/30 | Conceal, Azure Drake, Leeroy; Auctioneer 6, Prep −2, Cold Blood 2, Blade Flurry 4 | Draw the deck with Auctioneer + cheap spells, burst with Edwin/Cold Blood | **Low**: combo sequencing, the hardest for a script | Avoid |
| **Aggro Rogue** | 29/30 | Leeroy; Cold Blood 2, Blade Flurry 4 | Early pressure + weapon damage, Combo burst | Medium (Combo ordering) | Maybe |
| **Control Warrior** | 25/30 | Acolyte x2, Sylvanas, Ragnaros; Execute 2, Fiery War Axe 3 | Armor + removal, big finishers (Grom, Alexstrasza) | Low/Medium: long games, value decisions | Probably avoid |
| **Aggro Warrior** | 29/30 | Leeroy; Fiery War Axe 3 | Weapons + aggressive minions | High | Candidate |
| **Ramp Druid** | 29/30 | Ragnaros; Innervate/Wild Growth weaker, Nourish 6, Keeper 4, Ancient of Lore draws 1 | Ramp → Taunt wall → big minions | Medium (Choose One everywhere) | Weakened |
| **Token Druid** | 28/30 | Azure Drake; **Force of Nature lost Charge → FoN + Savage Roar combo is gone** | Wide board + Savage Roar | Medium | Weakened |
| **Tempo Mage** | 25/30 | Ice Lance, Acolyte, Azure Drake; Mana Wyrm 2 (1/3) | Early pressure + burn | Medium (spell targeting) | Candidate, mirrors Greedy Mage |
| **Handlock** | 24/30 | Mountain + Molten Giant, Power Overwhelming, Leeroy | Giants + Taunts | — | **Dead** |
| **Freeze Mage** | 23/30 | Ice Block, Ice Lance, Acolyte, Azure Drake | Stall + burn | — | **Dead** |
| **Control Priest** | 20/30 | Northshire, Mind Blast, Auchenai, Holy Fire, Sylvanas, Ragnaros | Removal + heal | — | **Dead** |

**Takeaway:** in this pool, the combo and control decks of 2014 lost key cards. The decks that survive mostly intact are
**board-centric curve decks**: Zoo, Midrange Hunter, Aggro Warrior, Midrange Shaman, Tempo Mage. These are also the easiest to script.

### 3.4 Known opponent: Bot 1 Greedy Mage (`decks/greedy_mage.json`)
Mana Wyrm 2, Sorcerer's Apprentice 2, Frostbolt 2, Arcane Missiles 2, Arcane Intellect 2, Bloodmage Thalnos 1, Harvest Golem 2,
Chillwind Yeti 2, Water Elemental 2, Fireball 2, Polymorph 2, Sen'jin Shieldmasta 2, Stranglethorn Tiger 2, Boulderfist Ogre 2,
Argent Commander 2, Flamestrike 1.
- **Midrange "good stuff" Mage.** Removal: Frostbolt, Fireball, Polymorph, Arcane Missiles, Fireblast. Only AoE: 1× Flamestrike (7 mana). No Arcane Explosion.
- Plays one action at a time, greedily (no turn planning, no lethal setup). It ends the turn when nothing scores above 0.
- **Implications:** fast board pressure on turns 1–6 lands before Flamestrike. Keep 1-health minions off its Fireblast where possible.
  Sticky/Deathrattle and Divine Shield minions blunt its single-target removal. Its Taunts (Sen'jin) and big bodies at 4–6 mana are
  where the game turns. Have answers or go wide before turn 7.

### 3.5 General strategy principles (to encode in the script)
- **Who's the beatdown:** decide each game whether we race (aggro vs slow decks) or control (vs faster boards). Against bots, tempo usually wins.
- **Mana efficiency:** spend all mana every turn. Use the hero power with leftover mana. Pick the combination of plays that uses the most mana (knapsack).
- **Lethal check first, every turn:** sum charge/attack-ready damage + burn + weapon + hero power, minus Taunts we must clear first.
- **Favorable trades:** kill an enemy minion when our attacker survives (or trades up in mana). Otherwise go face. Always clear Taunts that block lethal.
- **Board > face** while the opponent's board threatens us; **face > board** when we're ahead or have lethal next turn.
- **Mulligan for curve:** keep 1–3 drops. Going second also keep a 4-drop (The Coin).
- **Play around AoE:** don't overextend into Flamestrike (Mage, 7 mana) or Consecration/Hellfire/Lightning Storm when already ahead on board.
- **Sequence:** buffs/positional minions before attacks; attack before playing minions that care about deaths; draw spells early in the turn.
