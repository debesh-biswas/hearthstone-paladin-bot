# Tempo Mage: Deck Guide (hs-arena, Basic + Classic "Legacy" pool)

Pool: `basic-classic-1`, modern Legacy card versions (nerfs applied, Hall of Fame removed). Every cost, stat line and
card text below was checked against `meta.md` §2. Where the online advice used older card versions, the change is noted.

---

## 1. Overview and win condition

Tempo Mage takes the board early with cheap minions that are hard to remove efficiently and keeps it with cheap spells.
It then finishes the game with burn from hand. The plan has three phases:

1. **Turns 2–4: take the board.** Mana Wyrm, Knife Juggler, Faerie Dragon and Sorcerer's Apprentice, backed up by Frostbolt,
   Arcane Missiles and Fireblast to clear the opponent's early minions.
2. **Turns 4–7: keep the board with sturdy bodies.** Water Elemental, Chillwind Yeti and Stranglethorn Tiger survive 3–4 damage
   removal and Flamestrike. Fireball and Polymorph handle the opponent's big minions. Arcane Intellect refills the hand.
3. **Turns 6+: close the game.** Minion damage takes the opponent to about 10–15 health. Then Fireball (6), Frostbolt (3),
   Arcane Missiles (3), Pyroblast (10) and Fireblast (1) finish it, with +1 per spell while Bloodmage Thalnos is alive.

This pool is a little slower and more midrange than the 2014 "Tempo/Aggro Mage". Mana Wyrm now costs 2 and there is no
Ice Lance or Azure Drake. The deck plays as a **tempo-midrange Mage**: win the board first, go face once it is won, and
burn at the end.

**Win condition:** more stats on board from turn 2 onward than the opponent can answer, plus 13–20 burn damage from hand
for the last points.

---

## 2. Decklist (30)

| # | Cost | Id | Name | Stats | Current text | Role |
|---:|---:|---|---|---|---|---|
| 2 | 1 | `EX1_277` | Arcane Missiles | spell | Deal 3 damage randomly split among all enemies. | Clears 1-health minions, finishes lethal on an empty board, Wyrm trigger. Free with Apprentice. |
| 2 | 2 | `NEW1_012` | Mana Wyrm | 1/3 | Whenever you cast a spell, gain +1 Attack. | 2-drop that grows. Its 3 health survives Fireblast and 2-damage effects. |
| 2 | 2 | `EX1_608` | Sorcerer's Apprentice | 3/2 | Your spells cost (1) less. | Discount engine for burst turns: Missiles 0, Frostbolt 1, Fireball 3, Pyroblast 9. |
| 2 | 2 | `NEW1_019` | Knife Juggler | 2/2 | After you summon a minion, deal 1 damage to a random enemy. | Each minion played after it pings once, including Harvest Golem's deathrattle Golem. |
| 2 | 2 | `NEW1_023` | Faerie Dragon | 3/2 | Can't be targeted by spells or Hero Powers. | Spell removal and Fireblast can't target it. Very strong against Mage, Priest, Druid and Shaman. |
| 2 | 2 | `CS2_024` | Frostbolt | spell | Deal 3 damage to a character and Freeze it. | Cheap removal, 3 burn to face, freezes a weapon hero or a big attacker. |
| 1 | 2 | `EX1_012` | Bloodmage Thalnos | 1/1 | Spell Damage +1. Deathrattle: Draw a card. | +1 to every damage spell (Missiles fires 4). Replaces itself when it dies. |
| 1 | 2 | `CS2_025` | Arcane Explosion | spell | Deal 1 damage to all enemy minions. | Answer to 1/1 tokens (Hunter, Paladin, Warlock). Wyrm trigger. 2 damage with Thalnos. |
| 2 | 3 | `CS2_023` | Arcane Intellect | spell | Draw 2 cards. | Refills the hand on a turn the board is safe. 2 mana with Apprentice. |
| 2 | 3 | `EX1_556` | Harvest Golem | 2/3 | Deathrattle: Summon a 2/1 Damaged Golem. | Takes two removal effects. Its 2/1 Golem triggers Juggler. |
| 2 | 4 | `CS2_029` | Fireball | spell | Deal 6 damage. | Kills a big minion or deals 6 to face. Main finisher. |
| 2 | 4 | `CS2_033` | Water Elemental | 3/6 | Freeze any character damaged by this minion. | Strongest 4-drop. Survives Flamestrike, Fireball and 4-damage removal. |
| 2 | 4 | `CS2_022` | Polymorph | spell | Transform a minion into a 1/1 Sheep. | Hard answer to anything with 7+ health or a deathrattle (Ogre, Tirion, Highmane, Cairne, Al'Akir, Grommash). |
| 2 | 4 | `CS2_182` | Chillwind Yeti | 4/5 | (vanilla) | Sturdy 4-drop that beats 3-damage removal and Flamestrike-adjacent damage. |
| 2 | 5 | `EX1_028` | Stranglethorn Tiger | 5/5 | Stealth | Can't be targeted until it attacks. Survives Flamestrike. Mid-game pressure. |
| 1 | 7 | `CS2_032` | Flamestrike | spell | Deal 4 damage to all enemy minions. | Comeback card when we are behind on board. Rarely needed when ahead. |
| 1 | 10 | `EX1_279` | Pyroblast | spell | Deal 10 damage. | Late-game finisher (9 mana with Apprentice), or emergency removal on a huge minion. |

**Totals:** 17 minions, 13 spells. Curve: 1-cost 2 · 2-cost 13 · 3-cost 4 · 4-cost 8 · 5-cost 2 · 7-cost 1 · 10-cost 1.

`deck.json` ids (in order): EX1_277×2, NEW1_012×2, EX1_608×2, NEW1_019×2, NEW1_023×2, CS2_024×2, EX1_012, CS2_025,
CS2_023×2, EX1_556×2, CS2_029×2, CS2_033×2, CS2_022×2, CS2_182×2, EX1_028×2, CS2_032, EX1_279.

### Why these choices (and the cards left out)
- **Faerie Dragon ×2 over Leper Gnome / Argent Squire.** Leper Gnome is now a 1/1, which dies to Fireblast and its
  deathrattle does almost nothing. Faerie Dragon is a 3/2 that the course's Greedy Mage cannot hit with Frostbolt, Fireball,
  Polymorph or Fireblast. It also uses no positioning, so a simple pilot can play it well.
- **Chillwind Yeti ×2 and Stranglethorn Tiger ×2 in place of Azure Drake ×2 and Kirin Tor Mage / secrets.** Azure Drake is
  Hall of Fame. A secret package (Kirin Tor, Mirror Entity, Counterspell) is a sequencing puzzle and is easy to misplay.
  Plain 4/5 and 5/5 Stealth bodies give the same tempo with no decisions to get wrong.
- **Polymorph ×2.** The classic advice is to run 0–1 because Polymorph is dead against aggro. Our known opponents (Greedy
  Mage with Boulderfist Ogre 6/7, Water Elemental, Yeti and Argent Commander, plus unknown bots) play big midrange bodies
  that our 3-health minions can't trade into, so the second copy is worth it.
- **Harvest Golem ×2.** It is sticky against single-target removal and triggers Juggler. It replaces the classic Arcane
  Golem, which is now a 4/4 without Charge that gives the opponent a mana crystal. That is a poor trade in a tempo deck.
- **No Ice Lance, Acolyte of Pain or Azure Drake:** all removed from the pool. **No Mirror Image:** the deck has no
  1-mana minions to protect early, and Water Elemental and Yeti protect the board better.
- **Pyroblast ×1 and Flamestrike ×1:** one finisher and one board reset, the usual counts for a tempo deck.
- **Close calls settled in favour of simplicity:** Yeti over Violet Teacher (no spell-chaining needed), Faerie Dragon over Dire
  Wolf Alpha (no adjacency), and no secrets.

---

## 3. How the nerfs changed the deck (vs online classic lists)

| Card | Online / 2014 version | Ours | Effect on advice |
|---|---|---|---|
| Mana Wyrm `NEW1_012` | **1 mana** 1/3 | **2 mana** 1/3 | Guides say "Turn-1 Mana Wyrm, always keep." Ours is a 2-drop, so **going first the deck has no turn-1 minion**. Still keep it, but it competes with the other 2-drops. Coin + Wyrm on turn 1 is the closest copy of the old opener. |
| Knife Juggler `NEW1_019` | 3/2 | **2/2** | Now dies to any 2-damage effect and trades only with 2-health minions. Play it in turns that also summon other minions. |
| Leper Gnome `EX1_029` | 2/1 | **1/1** | Cut. Online lists (e.g. egraz Classic) run 2. |
| Arcane Golem `EX1_089` | 4/2 Charge | **4/4, no Charge** | Cut. Classic lists used it as 4 charge damage for reach. That reach no longer exists. |
| Ice Lance `CS2_031` | 1-mana burst (4 to a frozen target) | **Removed (HoF)** | The classic "Frostbolt + Ice Lance + Fireball" burst is gone. Real burst is now Fireball, Frostbolt, Missiles, Pyroblast and Fireblast. |
| Azure Drake `EX1_284` | 4/4, +1 spell damage, draw | **Removed (HoF)** | One guide calls it essential ("deck doesn't work without two"). Replaced by Yeti and Tiger as bodies, Thalnos for spell damage and Arcane Intellect for cards. |
| Acolyte of Pain `EX1_007` | draw engine | **Removed (HoF)** | Arcane Intellect ×2 and Harvest Golem stickiness take its place. |
| Ice Block `EX1_295` | secret | **Removed (HoF)** | Not relevant to Tempo Mage. |
| Arcane Intellect, Frostbolt, Fireball, Polymorph, Water Elemental, Flamestrike, Pyroblast, Sorcerer's Apprentice, Arcane Missiles | — | unchanged | Advice applies as written. |

Opponent nerfs that matter to us: Unleash the Hounds now costs 3, Starving Buzzard 5, Hex 4, Lightning Storm 3,
Feral Spirit 3, Equality 4, Avenging Wrath 6, Fiery War Axe 3, Big Game Hunter 5 (and it can't hit our minions: none has
7+ Attack), Ironbeak Owl 3 and Force of Nature 5 without Charge.

---

## 4. Mulligan

General principle (all sources): keep the early curve and throw back expensive and situational spells. We want a
2-drop on turn 2 every game.

### Always keep
- Mana Wyrm `NEW1_012`, Knife Juggler `NEW1_019`, Faerie Dragon `NEW1_023`, Sorcerer's Apprentice `EX1_608`.
- Frostbolt `CS2_024`: keep **one** copy. It is the cheapest answer to an opposing 2- or 3-drop.

### Conditional keeps
- **Harvest Golem `EX1_556`:** keep if the hand already has a 2-drop. Otherwise it is a fine keep only going second.
- **Arcane Missiles `EX1_277`:** keep one if the hand has Mana Wyrm or Sorcerer's Apprentice. Otherwise toss it.
- **Bloodmage Thalnos `EX1_012`:** keep only when no other 2-drop is in hand (it is a weak body).
- **Water Elemental `CS2_033` / Chillwind Yeti `CS2_182`:** going **second** (Coin), keep **one** 4-drop if the hand also has a
  2-drop. Going first, keep a Water Elemental only if the hand already has two cards costing 2–3.
- **Second Frostbolt:** keep it against a known aggro class only. The class is unknown at mulligan, so in practice toss it.

### Always toss
- Fireball `CS2_029`, Polymorph `CS2_022`, Arcane Intellect `CS2_023`, Arcane Explosion `CS2_025`, Stranglethorn Tiger
  `EX1_028`, Flamestrike `CS2_032`, Pyroblast `EX1_279`.

### Going first vs second
- **First (3 cards):** hunt hard for a 2-drop. Toss everything costing 4+, unless the hand already has two 2-drops and the
  4+ card is Water Elemental.
- **Second (4 cards + The Coin):** the Coin smooths the curve, so one 4-drop is fine. A good Coin line is turn 1 Coin +
  2-drop, then 2-drop, then Harvest Golem or two cheap plays. It works best when the hand has two 2-drops.

---

## 5. Turn-by-turn game plan (ideal curve)

| Turn | Mana | Ideal play | Notes |
|---|---:|---|---|
| 1 | 1 | Usually **nothing** going first. With Coin: Coin + Mana Wyrm / Faerie Dragon / Knife Juggler if you hold another 2-drop for turn 2. | Don't fire Arcane Missiles into an empty board on turn 1. Save it to trigger Wyrm or clear tokens. |
| 2 | 2 | **2-drop.** Priority: Mana Wyrm (if spells in hand) > Faerie Dragon > Knife Juggler > Sorcerer's Apprentice > Thalnos. Against an opposing 2-drop you can't otherwise beat, Frostbolt it instead. | No 2-drop in hand? Fireblast a 1-health enemy minion or the enemy hero. |
| 3 | 3 | Harvest Golem; or 2-drop + Arcane Missiles; or Knife Juggler then any 1-cost play; or Apprentice + Frostbolt (1). | Juggler first, then other minions, so it pings. |
| 4 | 4 | **Water Elemental** > Yeti. Or Fireball/Polymorph a threat. Or two 2-drops (Juggler first). | Coin can bring the 4-drop to turn 3. |
| 5 | 5 | **Stranglethorn Tiger**; or 4-drop + Missiles; or 2-drop + Golem; or Frostbolt + 3-drop. | Use all mana. Fireblast with spare 2. |
| 6 | 6 | Two-card turns: 4-drop + 2-drop, Apprentice + Fireball (3) + Frostbolt (1), Arcane Intellect + 3-drop. | Begin counting burn for lethal (Section 9). |
| 7 | 7 | Flamestrike if behind on board (it kills 2+ enemy minions or a key 4-health minion). Otherwise Tiger + 2-drop, or 4-drop + Arcane Intellect. | Don't Flamestrike just one small minion. |
| 8–9 | 8–9 | Develop + burn. Fireball and Frostbolt to face once the board is safe. | Apprentice + Pyroblast = 9 mana. |
| 10 | 10 | Pyroblast face (10) or Pyroblast a huge minion if you are losing on board. | Fireball + Fireball + Fireblast = 10 mana, 13 damage. |

General rules: spend all mana every turn. Draw (Arcane Intellect) early in a turn when you have spare mana, before
deciding what else to cast. Use Fireblast with exactly 2 spare mana.

---

## 6. Card-by-card usage

- **Arcane Missiles `EX1_277`:** best when the enemy board is empty (all 3, or 4 with Thalnos, go face) or when the enemy has
  only 1-health minions. Free with Apprentice. Always cast it before Mana Wyrm attacks (+1 Attack). Don't cast it into a board
  of high-health minions just to deal random chip damage.
- **Mana Wyrm `NEW1_012`:** play it on turn 2. Holding it to cast spells first is a known trap (BlizzardWatch). Every spell you
  cast this turn **before** it attacks adds +1 Attack. The buff is permanent.
- **Sorcerer's Apprentice `EX1_608`:** a 3/2 that is a fine turn-2 play on its own. Its best use is a burst turn: Apprentice +
  Frostbolt (1) + Missiles (0) on turn 3, or Apprentice + Fireball (3) + Frostbolt (1) + Missiles (0) on turn 6. It dies to
  everything, so cast the discounted spells in the same turn whenever possible.
- **Knife Juggler `NEW1_019`:** play it **before** other minions in the same turn. Each later summon (including Harvest Golem's
  deathrattle Golem) pings a random enemy. It is a 2/2 now, so it trades only with 2-health minions.
- **Faerie Dragon `NEW1_023`:** spells and hero powers can't target it, so it is the safest minion against Mage and Priest. It is
  not protected from attacks, AoE (Flamestrike, Consecration, Arcane Explosion) or random effects (Arcane Missiles,
  Multi-Shot, Avenging Wrath).
- **Frostbolt `CS2_024`:** kill a 2–3 health minion (Mana Wyrm, Apprentice, Juggler, Raptor, Ooze); freeze a weapon-wielding hero
  (Warrior, Rogue, Paladin, Hunter with a bow) or a big attacker to buy a turn; or 3 to face as burn. Early on, removal value
  beats face damage.
- **Bloodmage Thalnos `EX1_012`:** play it the turn before or the turn of a big spell turn. With Thalnos alive, Missiles = 4,
  Frostbolt = 4, Fireball = 7, Pyroblast = 11, Flamestrike = 5, Arcane Explosion = 2. When it dies you draw a card.
- **Arcane Explosion `CS2_025`:** cast it when it kills 2+ enemy minions (tokens, Imps, Hounds, Snakes, Silver Hand Recruits,
  Murloc Scouts) or 1 minion plus a Wyrm trigger that wins a trade.
- **Arcane Intellect `CS2_023`:** cast when the hand has 3 or fewer cards and the board is not under pressure, or on a turn with
  exactly 3 (or 2 with Apprentice) spare mana. Don't cast it if your hand already has 8+ cards (overdraw burns cards at 10).
- **Harvest Golem `EX1_556`:** turn-3 play. It trades well because it leaves a 2/1 behind. With Juggler on board, the 2/1
  Golem summoned on death also pings.
- **Fireball `CS2_029`:** use on minions with 4–6 health that you can't trade into (Yeti, Sen'jin, Water Elemental, Tiger once
  visible, Highmane, Fire Elemental). Otherwise save it for face. Hold at least one for the finish once the opponent is ≤12
  health.
- **Water Elemental `CS2_033`:** best on turn 4. Attacking freezes the target, so it trades into big minions without being hit
  back next turn (the frozen minion can't attack). Its 6 health survives Flamestrike, Fireball, Shadow Bolt and Swipe.
- **Polymorph `CS2_022`:** save it for minions with 6+ health or a strong deathrattle or effect: Boulderfist Ogre, Water
  Elemental, Savannah Highmane, Cairne, Tirion, Al'Akir, Earth Elemental, buffed minions, Lord of
  the Arena, Sunwalker, Grommash, Gruul, Alexstrasza, Ysera. Don't polymorph a 2- or 3-drop unless it's about to kill you.
- **Chillwind Yeti `CS2_182`:** a solid 4-drop. Play it when you don't have Water Elemental, or when you want two bodies.
- **Stranglethorn Tiger `EX1_028`:** turn 5. It can't be targeted until it attacks. Attack face with it (if it trades, it loses
  Stealth anyway). It survives Flamestrike.
- **Flamestrike `CS2_032`:** the comeback card. Cast it when it kills 2+ enemy minions, or kills one key minion that you can't
  answer otherwise and you are behind. When we are ahead on board, hold it.
- **Pyroblast `EX1_279`:** 10 to face to finish, or removal on an 8+ health minion when you're losing (Ironbark 8/8, King Krush,
  Deathwing, Alexstrasza). With Apprentice it costs 9.
- **Fireblast (hero power, 2 mana, 1 damage):** see Section 8.

---

## 7. Combos, synergies and positioning

- **Spells before Wyrm attacks.** Cast every spell you plan to cast this turn, then attack with Mana Wyrm.
- **Apprentice first, then spells.** It makes Missiles free, Frostbolt 1, Arcane Intellect 2, Fireball 3, Polymorph 3,
  Flamestrike 6, Pyroblast 9.
- **Thalnos first, then damage spells.** +1 to every damage spell.
- **Juggler first, then minions.** Each minion summoned after Juggler pings once. Juggler + Harvest Golem is two pings over the
  game.
- **Freeze then ignore.** A minion frozen by Frostbolt or Water Elemental can't attack next turn. Go face with your other
  minions instead of trading into it.
- **Biggest burst lines:**
  - Turn 6: Apprentice (2) + Fireball (3) + Frostbolt (1) + Missiles (0) = 6 mana → 12 burn (Missiles only if the enemy
    board is empty).
  - Turn 8: Fireball + Fireball = 8 mana → 12. With Thalnos alive → 14.
  - Turn 10: Fireball + Fireball + Fireblast = 13; Pyroblast = 10; Fireball + Frostbolt + Missiles + Fireblast (9 mana) = 13.
- **Positioning:** no card in this deck cares about adjacency. Always place minions on the right (omit `position`). Only
  enemy adjacency effects matter (enemy Cone of Cold, Explosive Shot, Betrayal, Flametongue Totem). If you face them, spread
  important minions apart, but the effect is small.

---

## 8. Trading rules and hero power

### Trade vs face
1. **Lethal first.** If total available face damage ≥ enemy health + armor, go face with everything (Section 9).
2. **Clear Taunts** that block your attackers. Use the cheapest way (a minion that kills it and survives, then Frostbolt,
   then Fireball, then Polymorph for big taunts).
3. **Free trades:** attack a minion if your attacker kills it and survives. Do it almost always.
4. **Even trades** (both die): take them when the enemy minion costs more than yours, or has an effect that wins games
   (Knife Juggler, Mana Wyrm, Sorcerer's Apprentice, Flametongue Totem, Wild Pyromancer, Questing Adventurer,
   Gadgetzan Auctioneer, Cult Master, Imp Master, Raid Leader, Dire Wolf Alpha, Murloc Warleader, Violet Teacher, Northshire-type
   engines, Lightwell, Mana Tide Totem, Summoning Portal, Starving Buzzard, Scavenging Hyena, Timber Wolf).
5. **Otherwise go face**, except when the enemy board threatens to kill us. If enemy board attack ≥ our health − 8, play
   control: trade everything favourable and keep removal for their minions.
6. **Who is the beatdown:** against slower decks (Warrior, Druid, Priest, Greedy-style midrange Mage), push face once the board
   is won. Against faster decks (Hunter, Zoo Warlock, aggro Paladin/Rogue), trade first and only race when ahead.

### Enemy minion priority (remove first)
1. Taunts blocking lethal.
2. Snowballing engines and auras (list in rule 4 above).
3. Minions with 5+ Attack or Windfury.
4. Anything we can kill for free with a trade.
5. Vanilla small minions last; ignore them if racing.

### Hero power (Fireblast, 2 mana, 1 damage to any target)
- Kill a 1-health enemy minion (tokens, Leper Gnome, a Juggler-pinged minion, a damaged minion).
- Pop a Divine Shield (Argent Squire, Argent Commander, Scarlet Crusader, Tirion) before a trade.
- Finish a minion that one of our attacks left at 1 health.
- Otherwise use it **on the enemy hero** whenever exactly 2 mana is left over.
- Never target Faerie Dragon (illegal) or our own minions.
- Never Fireblast instead of playing a card that uses the same 2 mana better (a 2-drop on turn 2 > Fireblast).

---

## 9. Lethal checklist

Count every turn, from turn 4 onward:
1. Enemy health + armor = **H**. Remove Taunts first (count the mana and cards that costs).
2. **Board:** attack of every friendly minion that can attack this turn (not just played, not frozen, not exhausted).
   Mana Wyrm gets +1 per spell cast before it attacks.
3. **Burn in hand** (with current mana, with Apprentice discounts, +1 per spell if Thalnos is alive):
   Fireball 6 (4 mana), Frostbolt 3 (2), Pyroblast 10 (10), Arcane Missiles 3 (1) (face only if the enemy board is empty,
   otherwise count about 1), Fireblast 1 (2).
4. If board + burn ≥ H, go: spells to face first (Wyrm grows), then all attacks to face.
5. **Next-turn lethal:** if you are 1 turn away and the enemy can't kill you, prefer face damage now over medium trades.

Reference reach (no board): 4 mana = 6, 6 mana = 9 (Fireball + Frostbolt), 7 mana = 10 (Fireball + Frostbolt + Missiles),
8 mana = 12, 10 mana = 15 (Fireball + Fireball + Frostbolt) or 16 (+ Missiles with 11 mana / Apprentice).

---

## 10. Matchups

### Greedy Mage (course Bot 1, known list)
List: Mana Wyrm ×2, Sorcerer's Apprentice ×2, Frostbolt ×2, Arcane Missiles ×2, Arcane Intellect ×2, Bloodmage Thalnos, Harvest
Golem ×2, Chillwind Yeti ×2, Water Elemental ×2, Fireball ×2, Polymorph ×2, Sen'jin Shieldmasta ×2, Stranglethorn Tiger ×2,
Boulderfist Ogre ×2, Argent Commander ×2, Flamestrike ×1.

How it plays (from its public scoring rules): every turn it plays the single highest-scoring action until nothing scores above 0.
- **Frostbolt and Fireball** go to the most valuable of our minions they can kill outright. It fires them as soon as it can,
  not for lethal. If nothing is killable, it burns our face.
- **Polymorph** only hits a minion whose Attack + Health (+ keyword bonus) is at least 6. Juggler (2/2), Apprentice (3/2),
  Golem (2/3), Thalnos and an unbuffed Mana Wyrm (1/3) are **never polymorphed** (a Wyrm that has grown to 3/3 is).
  Water Elemental, Yeti and Tiger are.
- **Fireblast** kills a 1-health minion if it can, otherwise it hits our face.
- **Flamestrike** (one copy) is cast as soon as it kills anything worth more than about 1.4 points, so usually on turn 7–8 the
  first time we have small minions out.
- **Attacks:** it trades when its minion kills ours and survives. Otherwise it mostly goes face. It does check for lethal.

What beats it:
- **Faerie Dragon** can't be touched by any of its targeted removal or Fireblast. Only Flamestrike, Arcane Missiles or a trade
  kills it. Play it early and attack face with it.
- **Stranglethorn Tiger** dodges all its targeting until it attacks. Use it to trade into Water Elemental/Yeti only when
  necessary, otherwise attack face.
- Its only early drops are Mana Wyrm, Apprentice, Thalnos and Harvest Golem. **Kill Mana Wyrm and Apprentice on sight**
  (Frostbolt, Fireblast on a 1-health, trades). Then our 2-drops push face.
- Its big midrange bodies (Sen'jin 3/5 Taunt, Yeti 4/5, Water Elemental 3/6, Tiger 5/5, Ogre 6/7) arrive on turns 4–6.
  **Polymorph Ogre and Water Elemental; Fireball Yeti/Sen'jin/Tiger** when they block our attack. Use Water Elemental to freeze
  their biggest attacker.
- It spends removal eagerly, so it often runs out of answers. Its Fireballs are used on our minions, which lowers its reach.
  Still, respect up to 6 + 3 + 1 = 10 burn + its board from turn 6 when you are low.
- **Play around its single Flamestrike** from turn 7: rely on 5+ health bodies (Water Elemental, Yeti, Tiger) rather than
  flooding with 2-drops. Our own Flamestrike is excellent against its Wyrm/Apprentice/Golem/Argent Commander boards.
- **Argent Commander (4/2 Charge, Divine Shield):** pop the shield with Fireblast, Arcane Missiles or Juggler, then kill it with
  any 2-attack minion.

### Hunter (Face/Midrange)
Their damage: Steady Shot 2 per turn, Kill Command 3/5, Arcane Shot 2, Unleash the Hounds (3 mana now), Savannah Highmane,
Explosive Trap (2 to all of ours when we attack face), Snipe (4 to our next minion), Freezing Trap.
- Trade aggressively early. Their small beasts (Timber Wolf, Hyena, Animal Companions) are worth killing.
- Arcane Explosion and Arcane Missiles clear Hounds and Snakes. Polymorph Highmane (no Hyenas).
- Play the cheaper minion first into a possible Snipe. Don't play Water Elemental into an obvious Snipe on turn 4 if you have
  a 2-drop instead.
- Our life total is a resource they attack. Keep Frostbolt to stop a weapon or big charger. Race only when clearly ahead.

### Paladin (Aggro/Midrange/Control)
Their tools: Consecration 4 (2 to all), Equality 4, Avenging Wrath 6, Truesilver Champion, Blessing of Kings, Tirion.
Divine Shields everywhere.
- Pop shields with Fireblast/Missiles/Juggler before trading.
- Don't flood 2-health minions into Consecration on turn 4+. Mix in Yeti/Water Elemental.
- Arcane Explosion kills Silver Hand Recruits. Polymorph Tirion (no Ashbringer) or a Blessing of Kings target.
- Against control Paladin, push face early and keep burn for the end. They heal (Guardian of Kings, Lay on Hands), so count
  lethal carefully.

### Warrior (Control/Aggro)
Their tools: weapons (Fiery War Axe 3 mana, Arcanite Reaper, Gorehowl), Execute, Shield Slam, Brawl, Whirlwind, armor,
Grommash.
- Considered the hardest classic matchup for this archetype (the guide author won ~2 in 20). Our best wins come from an early
  board plus a turn-4 Water Elemental that survives.
- Freeze their hero with Frostbolt when they have a big weapon. Water Elemental freezes on hit.
- Don't overextend into Brawl. Keep 2–3 minions, not 5.
- Polymorph Grommash or a big taunt. Save Fireball + Pyroblast for face. Armor counts as health.
- Against aggro Warrior (charge minions, weapons), trade and keep life high.

### Shaman (Midrange)
Their tools: Lightning Storm 3 (2–3 to all), Feral Spirit 3, Flametongue Totem, Hex 4, Fire Elemental, Earth Elemental, Al'Akir,
Doomhammer, Bloodlust.
- Kill Flametongue Totem and Mana Tide Totem on sight (Fireblast + attack, Frostbolt).
- Polymorph Earth Elemental / Al'Akir. Fireball Fire Elemental.
- Watch for Bloodlust: if they have 3+ minions and we're low, clear the board rather than race.
- The classic guide calls it "very difficult": pressure early before Lightning Storm and big minions.

### Rogue (Aggro/Miracle-ish)
Their tools: weapon (Dagger hero power, Assassin's Blade, Perdition's Blade), Backstab, Eviscerate, SI:7, Fan of Knives, Blade
Flurry (4, minions only), Sap, Assassinate, Edwin VanCleef, Gadgetzan Auctioneer (6).
- Push face hard: Rogue has little healing and damages itself with the dagger.
- Kill Edwin and Auctioneer immediately (Fireball/Polymorph).
- Frostbolt the Rogue hero when they have a buffed weapon.

### Druid (Ramp/Token)
Their tools: Swipe, Wrath, Keeper of the Grove (4), Starfall, Force of Nature (5, no Charge), Savage Roar, Druid of the Claw,
Ancient of Lore/War, Ironbark Protector, Cenarius.
- A good matchup for tempo: punish ramp turns with board pressure.
- Polymorph Ancient of War / Ironbark / Cenarius. Pyroblast as a last answer to an 8/8.
- Force of Nature no longer has Charge, so the Force + Savage Roar burst combo is gone. Arcane Explosion or Flamestrike clears
  the Treants.

### Warlock (Zoo/Handlock)
Zoo: Flame Imp 3/2, Voidwalker, Knife Juggler, Dire Wolf Alpha, Defender of Argus, Imp Master (Doomguard is Hall of Fame).
Handlock is dead in this pool (no Giants).
- Against Zoo, play control: Arcane Explosion, Missiles, Flamestrike are very strong. Trade, kill buffers and Juggler first.
- Soulfire and Hellfire are their burn and sweeper. Watch our life total from Hellfire (3 to all characters).

### Priest
Their tools: Shadow Word: Pain / Death, Holy Nova, Cabal Shadow Priest (steals 2-Attack minions: Juggler, Golem), Mind Control,
Lightwell, Lightspawn.
- Faerie Dragon is excellent: their removal is all targeted spells.
- Kill Lightwell and Lightspawn quickly. Push face, since Priest is the weakest classic class.

---

## 11. Common mistakes

1. Attacking with Mana Wyrm **before** casting the turn's spells.
2. Playing Knife Juggler **after** the other minions in the same turn.
3. Casting Apprentice-discounted spells on a later turn instead of the same turn (Apprentice usually dies first).
4. Using Fireball on a 2–3 health minion that Frostbolt, Fireblast or a trade could kill.
5. Polymorphing a small minion and then having no answer to Ogre / Highmane / Tirion.
6. Firing Arcane Missiles into a board of high-health minions (it splits randomly).
7. Casting Arcane Intellect with a full hand (10 cards = burned draws).
8. Flooding the board with 2-health minions on turn 7+ into Flamestrike / Consecration / Lightning Storm.
9. Trading when lethal was available, or going face when the enemy board kills us next turn.
10. Floating mana: if 2 mana is left at the end of the turn, Fireblast.
11. Forgetting that the enemy's Faerie Dragon can't be targeted by our spells or Fireblast: kill it with attacks, Arcane
    Explosion, Flamestrike or Arcane Missiles.

---

## 12. Script hints (machine-encodable rules)

Card ids: Missiles `EX1_277`, Wyrm `NEW1_012`, Apprentice `EX1_608`, Juggler `NEW1_019`, Faerie `NEW1_023`, Frostbolt
`CS2_024`, Thalnos `EX1_012`, Explosion `CS2_025`, Intellect `CS2_023`, Golem `EX1_556`, Fireball `CS2_029`, WaterEle
`CS2_033`, Polymorph `CS2_022`, Yeti `CS2_182`, Tiger `EX1_028`, Flamestrike `CS2_032`, Pyroblast `EX1_279`, Coin `GAME_005`.

### Mulligan
- KEEP always: `NEW1_012`, `NEW1_019`, `NEW1_023`, `EX1_608`.
- KEEP first copy of `CS2_024`; REPLACE the second.
- KEEP `EX1_556` if hand has any of {`NEW1_012`,`NEW1_019`,`NEW1_023`,`EX1_608`,`EX1_012`} OR going second.
- KEEP one `EX1_277` if hand has `NEW1_012` or `EX1_608`.
- KEEP `EX1_012` only if no other 2-cost minion is kept.
- Going second: KEEP one of {`CS2_033` > `CS2_182`} if a 2-drop is kept.
- Going first: KEEP `CS2_033` only if two cards costing 2–3 are kept.
- REPLACE always: `CS2_029`, `CS2_022`, `CS2_023`, `CS2_025`, `EX1_028`, `CS2_032`, `EX1_279`.

### Turn procedure (in this order)
1. `lethal = sum(attack of ready friendly attackers not blocked by taunt) + burn_reachable(mana)` where burn uses
   `CS2_029`=6, `CS2_024`=3, `EX1_279`=10, `EX1_277`=3 only if enemy board empty, Fireblast=1; +1 per damage spell if friendly
   `EX1_012` on board; cost −1 per spell if friendly `EX1_608` on board; Wyrm +1 attack per spell cast first. If
   `lethal >= enemy.health + enemy.armor`: cast burn at enemy hero (most damage per mana first), then all attacks at enemy hero.
2. If an enemy Taunt exists: kill it with the cheapest sufficient option: friendly attacker that kills and survives >
   `CS2_024` (health ≤ 3+sd) > Fireblast (health 1) > `CS2_029` (health ≤ 6+sd) > `CS2_022` (health ≥ 7 or deathrattle).
3. Play `EX1_608` (Apprentice) and `EX1_012` (Thalnos) before other spells if spells will be cast this turn.
4. Play `NEW1_019` (Juggler) before any other minion this turn.
5. Removal: for each enemy minion in priority order (engines/auras > attack ≥ 5 > others), use the cheapest killing spell:
   Fireblast (hp 1, or Divine Shield pop), `CS2_024` (hp ≤ 3), `CS2_029` (4 ≤ hp ≤ 6), `CS2_022` (hp ≥ 7, or attack ≥ 6, or
   known deathrattle threat: Highmane `EX1_534`, Cairne `EX1_110`, Tirion `EX1_383`).
6. AoE: cast `CS2_032` if it kills ≥ 2 enemy minions or (kills ≥ 1 and enemy board attack ≥ our health/2). Cast `CS2_025` if it
   kills ≥ 2 enemy minions (hp ≤ 1 + spell damage).
7. Attacks: for each friendly attacker (Wyrm last, after spells): attack enemy minion if it kills it and survives; else even
   trade if enemy minion cost > attacker cost or is in the engine list; else attack enemy hero, unless
   `enemy_board_attack >= my_health - 8` (then prefer any trade that kills).
8. Develop: play minions by priority `CS2_033` > `EX1_028` > `CS2_182` > `EX1_556` > `NEW1_023` > `NEW1_012` > `NEW1_019` >
   `EX1_608` > `EX1_012`, choosing the set that spends the most mana (knapsack). Omit `position`.
9. `CS2_023` (Intellect): cast if hand ≤ 7 cards and mana left ≥ its cost after developing, or if nothing else is playable.
10. `EX1_277` (Missiles): cast if enemy board empty (face) or every enemy minion has hp 1, or as a free Wyrm trigger with
    Apprentice.
11. Hero power: if mana ≥ 2 left, Fireblast a 1-hp enemy minion (highest attack first) or a Divine Shield, else the enemy hero.
12. `end_turn`.

### Never
- Never send `target` when the legal action lists no targets. Never send `position` for spells.
- Never cast `CS2_022` on a minion with attack + health < 6 unless it has a dangerous effect (engine list).
- Never cast `CS2_029` on a minion with hp ≤ 3 when `CS2_024`, Fireblast or a trade kills it.
- Never cast `CS2_024`/`CS2_029`/`EX1_279`/Fireblast at our own hero or minions.
- Never cast `EX1_279` at a minion unless it has hp ≥ 7 and we have no `CS2_022`.
- Never cast `CS2_023` with 8+ cards in hand.
- Never cast `CS2_032` to kill a single minion with attack + health < 6.
- Never attack with `NEW1_012` before the turn's spells are cast.
- Never end the turn with ≥ 2 unspent mana if Fireblast is legal.

### Face-vs-trade thresholds
- Go face if: enemy health ≤ our burn in hand + our board attack (next-turn lethal), OR enemy board attack ≤ 3.
- Trade if: enemy board attack ≥ our health − 8, OR the trade kills an engine, OR the attacker survives and kills.
- Against classes Hunter / Warlock (Zoo) / aggro Paladin: trade-first. Against Warrior / Druid / Priest / Mage: face-first once
  we have more board attack than them.

---

## 13. Sources

| URL | What it provided |
|---|---|
| https://www.hearthstonetopdecks.com/decks/tempo-mage-257-legend-egraz-classic/ | Classic-format legend Tempo Mage list (Mana Wyrm, Argent Squire, Leper Gnome, Faerie Dragon, Knife Juggler, Thalnos, Arcane Golem, Harvest Golem, Water Elemental, Arcane Explosion). Basis for the Faerie Dragon / Harvest Golem / Arcane Explosion package. |
| https://www.hearthstonetopdecks.com/decks/tempo-mage-144-legend-ramza-classic-s87/ | Classic legend list with Antonidas, Flamestrike, Pyroblast, Polymorph, Kirin Tor + Mirror Entity. Showed the burn-finisher top end (Flamestrike ×1, Pyroblast ×1). |
| https://www.hearthstonetopdecks.com/decks/classic-tempo-mage/ | Classic list and mulligan priority (Mana Wyrm, Secretkeeper, Mirror Image, Knife Juggler, Sorcerer's Apprentice, Kirin Tor, Dire Wolf Alpha). Confirmed "keep 1–2 drops" mulligan. |
| https://hearthstone.wiki.gg/wiki/Tempo_Mage | Archetype definition: cheap spells + minions for early board, finish with burn from hand. |
| https://blizzardwatch.com/2015/09/06/deck-tech-rhonin-tempo-mage/ | Mulligan (keep Wyrms, Frostbolts; toss secrets), "play Wyrm immediately, holding it is a trap", Apprentice + cheap spells, Frostbolt uses, Fireball targets, Flamestrike as one-copy reset, per-class matchup advice (pressure Rogue/Warrior, Mirror Images vs weapons). |
| https://www.gosugamers.net/hearthstone/news/37923-mage-guide-aggro-mages-in-modern-meta | Burn-counting method, "10–15 damage with minions then spell burst", Juggler + Fireblast, Water Elemental freeze value, Pyroblast criticism, matchup notes (Druid favoured, Hunter race, Zoo face, Shaman very hard, Control Warrior near unwinnable), common mistakes (two Polymorphs vs aggro, idle Mirror Image, missing lethal breakpoints). |
| https://www.gosugamers.net/hearthstone/news/42205-the-core-quick-guide-to-tempo-mage | Water Elemental as a hard-to-remove 3/6 good vs weapon classes; Flamestrike vs Zoo/Shaman boards; Arcane Explosion as an anti-token tech. |
| https://www.hearthstonetopdecks.com/deck-guide/tempo-mage-deck-list-guide/ | General tempo plan ("get on the board, push damage, draw big spells, finish them"), Apprentice used deliberately, control role vs aggro / aggro role vs control, prioritise board early. |
| https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/ | Classic-format data: Mage is weak in Classic (Burn Mage exploited by top decks), Miracle Rogue / Zoo / Midrange Shaman top tier, Priest worst. Used for matchup expectations. |
| `meta.md` §2–3 (project) | Current card text/stats, nerf list, Hall of Fame removals, Greedy Mage decklist. |
| `pkg/hs-arena-0.2.2/src/hs_arena/agents/greedy_bot.py` + `greedy_config.json` | Greedy Mage behaviour: removal targeting rules, Polymorph threshold (value ≥ 6), Fireblast rules, Flamestrike trigger, trade scoring. |
