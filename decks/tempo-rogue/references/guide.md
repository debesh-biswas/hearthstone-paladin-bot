# Tempo Rogue — Deck Guide (pool `basic-classic-1`, hs-arena 0.2.2)

All card text, costs and stats below are the **current** versions from the card data (`pkg/hs-arena-0.2.2/data/cards.json`) (modern Legacy Basic+Classic,
nerfs applied, Hall of Fame removed). Online guides describe stronger 2014 versions; where they differ, this guide
follows our pool.

---

## 1. Overview and win condition

**Archetype choice: Tempo (midrange-aggro) Rogue, not Miracle Rogue.**

Miracle Rogue was the best Rogue deck of 2014 and of 2021 Classic mode (hearthstone.wiki.gg), but in this pool it
lost almost every engine piece:

| Miracle piece | 2014 / 2021 Classic | Our pool | Effect |
|---|---|---|---|
| Gadgetzan Auctioneer | 5 mana (2014: 5) | **6 mana** | The "Auctioneer + 3 cheap spells" turn now needs 8–9 mana. |
| Preparation | spell costs (3) less | **(2) less** | Prep → Sprint / Prep → Auctioneer chains lose a mana each. |
| Conceal | protects Edwin / Auctioneer | **Hall of Fame (removed)** | No way to protect the combo minion. |
| Leeroy Jenkins | 6/2 Charge finisher | **removed** | No Leeroy + Cold Blood + Shadowstep burst. |
| Azure Drake | draw + spell dmg | **removed** | No cheap card draw / Eviscerate boost. |
| Cold Blood | 1 mana | **2 mana** | Every burst turn costs one more mana. |
| Blade Flurry | 2 mana, hit heroes too | **4 mana, minions only** | Lost its face damage. |

What remains (6-mana Auctioneer, Sprint 7) is slow, card-sequencing-heavy and the hardest thing for a simple pilot
to execute (Miracle is hard to script). Meanwhile the **tempo tools are all intact**:
Backstab 0, Eviscerate 2, SI:7 Agent 3, Sap 2, Defias Ringleader 2, Edwin VanCleef **3** (the 2021 cost-4 nerf was
reverted), the dagger hero power and Assassin's Blade. Opponents in this arena are bots that play greedily without
planning, which tempo punishes best. **So: Tempo Rogue.**

**Win condition:** control the board on turns 1–5 with cheap, efficient removal (Backstab, dagger, SI:7, Eviscerate)
while developing sticky/efficient minions; then turn the board into face damage and finish with reach
(Eviscerate 4, Cold Blood, weapon swings, Argent Commander Charge). The deck is a **mid-game** deck: its best
turns are 2–6. It is not a pure face-rush deck, because our 1-drops are weak in this pool.

---

## 2. Decklist (30)

| # | Cost | Id | Name | Type | Stats | Current text | Role |
|---:|---:|---|---|---|---|---|---|
| 2 | 0 | `CS2_072` | Backstab | Spell | — | Deal 2 damage to an undamaged minion. | Free removal; free combo enabler; Edwin fuel |
| 1 | 1 | `CS2_074` | Deadly Poison | Spell | — | Give your weapon +2 Attack. | Turns dagger into 3/2, Assassin's Blade into 5/4; combo enabler |
| 2 | 1 | `EX1_008` | Argent Squire | Minion | 1/1 | Divine Shield | Turn-1 play, survives one ping, Cold Blood carrier, combo enabler |
| 1 | 1 | `EX1_010` | Worgen Infiltrator | Minion | 2/1 | Stealth | Turn-1 play that dodges Fireblast for a turn |
| 2 | 2 | `CS2_073` | Cold Blood | Spell | — | Give a minion +2 Attack. Combo: +4 Attack instead. | Burst / makes a small minion trade up |
| 2 | 2 | `EX1_131` | Defias Ringleader | Minion | 2/2 | Combo: Summon a 2/1 Defias Bandit. | 2-drop; 4 stats for 2 + Coin/Backstab |
| 2 | 2 | `EX1_124` | Eviscerate | Spell | — | Deal 2 damage. Combo: Deal 4 damage instead. | Removal or 4 face damage |
| 2 | 2 | `NEW1_023` | Faerie Dragon | Minion | 3/2 | Can't be targeted by spells or Hero Powers. | Best 2-drop vs Mage (immune to Frostbolt/Polymorph/Fireblast) |
| 1 | 2 | `EX1_096` | Loot Hoarder | Minion | 2/1 | Deathrattle: Draw a card. | 2-drop that replaces itself |
| 1 | 2 | `EX1_581` | Sap | Spell | — | Return an enemy minion to your opponent's hand. | Removes a Taunt / big minion for a lethal or tempo turn |
| 2 | 3 | `EX1_134` | SI:7 Agent | Minion | 3/3 | Combo: Deal 2 damage. | Best tempo card: 3/3 + 2 damage |
| 1 | 3 | `EX1_613` | Edwin VanCleef | Minion | 2/2 | Combo: Gain +2/+2 for each other card you've played this turn. | Early huge minion (4/4–8/8 on turns 2–4) |
| 2 | 3 | `EX1_556` | Harvest Golem | Minion | 2/3 | Deathrattle: Summon a 2/1 Damaged Golem. | Sticky body, two-for-one vs single-target removal |
| 1 | 3 | `EX1_133` | Perdition's Blade | Weapon | 2/2 | Battlecry: Deal 1 damage. Combo: Deal 2 instead. | Ping + weapon; kills 2-health minions |
| 2 | 4 | `CS2_182` | Chillwind Yeti | Minion | 4/5 | — | Solid 4-drop, survives Fireball-less trades |
| 1 | 4 | `CS2_147` | Gnomish Inventor | Minion | 2/4 | Battlecry: Draw a card. | Refill |
| 1 | 4 | `EX1_046` | Dark Iron Dwarf | Minion | 4/4 | Battlecry: Give a minion +2 Attack this turn. | Body + burst / trade-up |
| 1 | 5 | `CS2_080` | Assassin's Blade | Weapon | 3/4 | — | 12 damage over 4 turns; 5/4 with Deadly Poison |
| 1 | 5 | `CS2_076` | Assassinate | Spell | — | Destroy an enemy minion. | Hard removal for Boulderfist / Water Elemental / Tiger |
| 1 | 5 | `EX1_028` | Stranglethorn Tiger | Minion | 5/5 | Stealth | Can't be targeted until it attacks; guaranteed 5 damage |
| 1 | 6 | `EX1_067` | Argent Commander | Minion | 4/2 | Charge Divine Shield | Reach (4 Charge), kills a minion and survives |

Curve: 0×2, 1×4, 2×10, 3×6, 4×4, 5×3, 6×1 (19 minions, 2 weapons, 9 spells). 16 cards cost 0–2 and can enable Combo.

**Simplicity choices (deliberate):** Preparation, Shadowstep, Betrayal, Blade Flurry, Headcrack and Gadgetzan Auctioneer
are left out. They are either positional (Betrayal), need multi-card planning (Prep, Shadowstep loops) or are weak
in this pool (Blade Flurry 4, minions-only). Faerie Dragon, Harvest Golem and Yeti are "just play it" cards
that a simple pilot cannot misuse.

**Swap options:** Southsea Deckhand (`CS2_146`, 2/1, Charge with a weapon) for Worgen Infiltrator in a faster
build; Sen'jin Shieldmasta (`CS2_179`) for Gnomish Inventor vs aggro-heavy fields; Kidnapper (`NEW1_005`, 6 mana 5/3,
Combo bounce) for Argent Commander if more control is wanted; a 2nd Sap vs Taunt-heavy fields.

---

## 3. How the nerfs changed the deck (adjust online advice)

- **Cold Blood is 2 mana** (was 1). "Cold Blood + Cold Blood on a Charge minion" burst is gone (no Leeroy, and it costs 4).
  Use it as +4 Attack (combo) on a minion that can attack **this turn**, either for lethal or to kill a big minion.
- **No Leeroy Jenkins, no Conceal, no Azure Drake.** Online aggro lists (hearthstonetopdecks "Classic Aggro Rogue")
  rely on Leeroy for reach. Our reach is Eviscerate (4), Cold Blood, weapon + Deadly Poison, Argent Commander (4 Charge).
- **Edwin VanCleef is 3 mana** in our pool (hearthstone.wiki.gg: 3→4 in Jan 2021, back to 3 in Mar 2021). Keep advice:
  keep him with Coin or a 0-cost enabler.
- **Preparation reduces by 2**, so Prep → SI:7 / Eviscerate is still fine but Prep → Sprint is 5 mana; we cut it.
- **Blade Flurry 4 mana, minions only** → no longer a finisher or cheap board clear; cut.
- **Gadgetzan Auctioneer 6** → Miracle is a 9-mana combo; cut.
- **Leper Gnome 1/1, Knife Juggler 2/2, Abusive Sergeant** — weak 1-drops in this pool; online aggro Rogue
  keeps "all 1-drops", we keep only Argent Squire/Worgen and value 2-drops instead.
- **Southsea Deckhand** is still 2/1 Charge-with-weapon; good but a 1-health body vs a Mage, so it's a sideboard card.
- **Dread Corsair** (Taunt 3/3, cost 4 − weapon Attack): needs a big weapon to be cheap; cut to keep the deck simple.
- **Big Game Hunter 5 mana**: nothing in the Mage bot deck has 7 Attack; cut.

---

## 4. Mulligan

General principle (HSReplay "Art of the Mulligan"; HSTD Tempo Rogue guide): keep cheap cards and **combo cards you can
actually activate**; mulligan for curve; toss slow cards.

**Always keep:** Backstab `CS2_072`, SI:7 Agent `EX1_134`, Defias Ringleader `EX1_131`, Faerie Dragon `NEW1_023`,
Loot Hoarder `EX1_096`, Harvest Golem `EX1_556`, Argent Squire `EX1_008`.

**Conditional keeps:**
- Edwin VanCleef `EX1_613`: keep going second (Coin) or with a Backstab/1-drop in hand. Otherwise toss.
- Eviscerate `EX1_124`: keep one vs aggressive classes (Hunter, Paladin, Warrior, Rogue, Mage) — it kills a 2-drop.
- Worgen Infiltrator `EX1_010`: keep if no other 1- or 2-drop.
- Perdition's Blade `EX1_133`: keep going second or with a 2-drop already kept.
- Chillwind Yeti `CS2_182`: keep **one** when going second and the hand already has a 2-drop and a 3-drop.
- Deadly Poison `CS2_074`: toss (needs weapon; only good later).

**Always toss:** Cold Blood, Sap, Assassin's Blade, Assassinate, Stranglethorn Tiger, Argent Commander, Gnomish Inventor,
Dark Iron Dwarf, 2nd copy of any 4+.

**Vs Mage:** prefer Faerie Dragon, Harvest Golem, Argent Squire (Fireblast only pops its Divine Shield);
deprioritise Worgen/Loot Hoarder 1-health bodies only if you have alternatives (HSTD aggro guide:
"vs Mage, mulligan away one-toughness minions").

---

## 5. Turn-by-turn plan (ideal)

| Turn | Mana | Ideal play | Notes |
|---|---|---|---|
| 1 | 1 | Argent Squire / Worgen Infiltrator | Nothing? pass (don't Coin a 1-drop going second unless it enables Edwin/Ringleader combo). |
| 1 (Coin) | 2 | Coin → Defias Ringleader (2/2 + 2/1) | Coin counts as a card for Combo. |
| 2 | 2 | Faerie Dragon / Ringleader / Loot Hoarder / Golem with Coin; or Backstab + 2-drop | Backstab an enemy 2-drop, then Ringleader with combo. |
| 2 (Coin) | 3 | Coin → SI:7 Agent (kill a 2-health minion) or Coin → Backstab → Edwin (6/6) | Edwin 6/6 on turn 2 is game-winning vs bots. |
| 3 | 3 | SI:7 with combo (1-drop/Backstab/DP first) or Harvest Golem or Edwin with 0–1 cost enabler | If nothing combos, Golem or hero power + 1-drop. |
| 4 | 4 | Yeti / Dark Iron Dwarf / 1-drop + SI:7 combo / 2-drop + 2-drop | Spend all 4. |
| 5 | 5 | Stranglethorn Tiger / Assassin's Blade / 2-drop + SI:7 / Yeti + 1-drop | Assassinate only on a 5+ cost threat. |
| 6 | 6 | Argent Commander / Tiger + 1 / Yeti + Eviscerate | Start counting lethal from here. |
| 7–10 | 7+ | Two cards per turn, combos for reach, weapon swings face | Play around Flamestrike (Mage turn 7+): keep ≤4 minions if already winning. |

---

## 6. Card-by-card usage

- **Backstab** (0): kill an undamaged 2-health minion (Mana Wyrm is 1/3: Backstab + dagger swing kills it). Best targets: Sorcerer's Apprentice 3/2, 2-health 2-drops, Divine Shield removal (pops it). Played first,
  it enables Combo for free. It needs an **undamaged** minion: use it before attacking that minion.
- **Deadly Poison** (1): only when a weapon is equipped. Dagger → 3 Attack; Assassin's Blade → 5. Play it before the
  hero attacks. Good with Perdition's Blade (4/2). Also a 1-mana Combo enabler.
- **Argent Squire** (1): turn 1. Divine Shield makes it a good Cold Blood target (5/1 shielded = trades twice).
- **Worgen Infiltrator** (1): turn 1; Stealth means first attack is guaranteed.
- **Cold Blood** (2): with Combo → +4 Attack. Use for (a) lethal, (b) letting a minion kill a big threat it couldn't
  otherwise (Yeti + combo Cold Blood = 8/5, kills Boulderfist Ogre 6/7).
  Never on Faerie Dragon (can't be targeted) and never on a minion that can't attack this turn unless planning lethal.
- **Defias Ringleader** (2): always try to play it as the 2nd+ card of the turn (Coin, Backstab, a 1-drop first).
  Without combo it is just a 2/2 — acceptable when nothing else to play.
- **Eviscerate** (2): 4 damage with combo. Prefer removal on the opponent's best early minion (Water Elemental after
  it's damaged, Yeti with other damage). In the late game it is 4 face damage — count it in lethal.
- **Faerie Dragon** (2): best turn-2 play vs Mage and Priest; only minion combat removes it.
- **Loot Hoarder** (2): turn 2 filler; trade it eagerly (it draws).
- **Sap** (2): bounce a Taunt blocking lethal, or a big minion (Boulderfist Ogre, Argent Commander loses Divine Shield
  value, Tiger after it attacked) when we are ahead on board and the bounce lets our minions hit face. Never Sap a
  1–2 cost minion.
- **SI:7 Agent** (3): combo → 2 damage to any character. Targets: 2-health minion > Divine Shield pop > face (when lethal).
  Enabler order: Backstab (0) / Coin / 1-drop / Deadly Poison / Eviscerate, then SI:7.
- **Edwin VanCleef** (3): +2/+2 per other card played this turn. Coin + Backstab + Edwin = 6/6 on turn 2;
  turn 4 with 1-drop + Backstab + Edwin = 6/6; turn 5 with two 1-mana cards + Backstab = 8/8. Play him only with
  at least one card before him (4/4 for 3 is fine). With zero cards before him he is a 2/2 — only if nothing else.
- **Harvest Golem** (3): turn-3 filler; trades into 2-drops twice.
- **Perdition's Blade** (3): Battlecry 1 damage, combo 2. Kill a 1–2 health minion, then swing. Don't play it while
  Assassin's Blade (or a poisoned dagger) is still equipped — it replaces that weapon.
- **Chillwind Yeti** (4): plain 4/5. Survives most 3-attack minions.
- **Gnomish Inventor** (4): play when the hand is ≤2 cards or nothing better.
- **Dark Iron Dwarf** (4): 4/4 + give a minion +2 Attack **this turn**. Target a friendly minion that can still attack
  now (never an enemy minion). For lethal or to trade up.
- **Assassin's Blade** (5): 3/4. Use the hero to clear small minions and hit face; keep hero health above ~12 when
  trading into minions. Never replace it with the hero power while it has durability.
- **Assassinate** (5): only on minions costing 4+ or with Taunt that block lethal: Boulderfist Ogre, Water Elemental,
  Stranglethorn Tiger (once visible), Argent Commander, Sen'jin, Yeti.
- **Stranglethorn Tiger** (5): 5/5 Stealth. Opponent can't target or attack it until it attacks. Hit face or kill a key minion.
- **Argent Commander** (6): 4/2 Charge Divine Shield. Kills a 4-health minion and survives (shield), or 4 face for lethal.

---

## 7. Combos, synergies, positioning

- **Combo = any card played earlier this turn.** The Coin, Backstab and Deadly Poison count; the **hero power and
  attacks do not**. Always play the cheap enabler first, then the Combo card.
- Key combos (mana): Backstab + SI:7 (3) — 4 damage total of removal + 3/3; Backstab + Ringleader (2);
  Coin + Backstab + Edwin (turn 2, 6/6); 1-drop + SI:7 (4); Backstab + Eviscerate (2 mana, 6 damage);
  Eviscerate + Cold Blood on a ready minion (4 mana, 4 face + 4 attack); Deadly Poison + Eviscerate (3 mana, combo 4 dmg
  plus a 3-attack dagger swing); hero power (2) + Deadly Poison (1) = 3-damage swing on turn 3+.
- **Positioning matters little** — the deck has no adjacency effects. Default rightmost placement is fine.
  Only rule: Dark Iron Dwarf/Cold Blood the minion that can attack now.

---

## 8. Trading rules (face vs trade)

1. **Lethal first** (see §10). If lethal, everything face (clear only Taunts that block it).
2. **Free trades:** attack an enemy minion if our attacker kills it **and survives**. Always take these.
3. **Value trades:** our minion dies but kills a minion that costs more (e.g. Loot Hoarder into Sorcerer's Apprentice).
4. **Must-kill priority:** Sorcerer's Apprentice, Mana Wyrm (grows), Knife Juggler, Flametongue Totem, Raid Leader,
   Dire Wolf Alpha, Imp Master, any minion with ≥5 Attack, any Taunt blocking lethal, Water Elemental (freezes).
5. **Go face** when: the opponent's board is empty/only 0–1 attack minions; we are ahead on board by ≥4 total Attack;
   or the opponent is ≤12 health and we have reach in hand.
6. **Trade instead of face** when the enemy board has more total Attack than ours, or our hero is ≤12 health.
7. Hero (weapon) attacks: hit a minion only if hero health after the hit stays ≥ 12 (≥ 8 when it wins the game), or the
   minion has ≤2 Attack. Otherwise swing face.

---

## 9. Hero power (Dagger Mastery: equip a 1/2 dagger, 2 mana)

- Use when mana is left over and **no weapon is equipped**. A turn-2 dagger when there is no 2-drop is fine.
- **Never** use it while Assassin's Blade, Perdition's Blade or a poisoned dagger is equipped (it replaces the weapon).
- Equip then immediately use it: kill a 1-health minion or hit face.
- Dagger + Deadly Poison (3 mana) = 3-damage swing, good removal on turn 3.

---

## 10. Lethal checklist

Every turn before anything else, add:
- Each ready minion's Attack (not frozen, not summoned this turn unless Charge).
- Weapon Attack (if hero hasn't attacked) — or 1 if we can hero power (2 mana) into a dagger; +2 per Deadly Poison.
- Eviscerate: 4 if it's not the first card played (else 2).
- Cold Blood: +4 on a ready minion with combo (+2 without).
- Dark Iron Dwarf: +2 on a ready minion (4 mana).
- SI:7 Agent combo: 2 to face.
- Perdition's Blade: 1/2 Battlecry + 2 Attack swing.
- Argent Commander: 4 Charge.
- Minus: Taunts (need Sap, SI:7/Eviscerate, or attacks to remove). Subtract enemy Armor.
Spend mana in the order that gives most damage: enabler (0–1 cost) first, then combo cards.

---

## 11. Matchups

**Greedy Mage** (Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Thalnos, Harvest
Golem, Yeti, Water Elemental, Fireball, Polymorph, Sen'jin, Tiger, Boulderfist, Argent Commander, 1 Flamestrike).
- It plays greedily one action at a time and has a lot of single-target removal; only one Flamestrike (7 mana).
- Plan: be the beatdown on turns 2–6. Faerie Dragon is immune to all its spells and Fireblast. Harvest Golem and
  Argent Squire blunt Frostbolt/Fireblast.
- Kill Mana Wyrm and Sorcerer's Apprentice immediately (Backstab kills Apprentice; dagger+Backstab kills Wyrm).
- Water Elemental 3/6: Assassinate or Sap; otherwise ignore and go face (attacking into it freezes our minion).
- Sen'jin 3/5 Taunt: SI:7 + Eviscerate or Sap when face damage is close; Yeti trades evenly.
- Boulderfist 6/7, Tiger 5/5: Assassinate; otherwise race.
- Turn 7+: don't add a 4th minion to a board that's already winning (Flamestrike deals 4 — Yeti survives).
- Expect up to ~10 burn from hand (Fireball 6, Frostbolt 3) — don't drop below ~10 health with no board.

**Hunter (Midrange/Face):** race is risky; contest early. Trade with everything; Knife Juggler, Houndmaster, Highmane
are must-kills. Save Assassinate for Savannah Highmane (kill the Hyenas with dagger/Eviscerate). Hunter has
Explosive Trap — attack face with the hero when hero health is high.

**Paladin:** Divine Shield minions — pop shields with dagger/SI:7/Backstab before trading. Equality + Consecration
can wipe; don't overextend past 3 minions after turn 4. Tirion: Sap or Assassinate (Sap is excellent — it removes the
Ashbringer Deathrattle too).

**Warrior:** Fiery War Axe 3/2, Execute, Brawl. Their weapons kill our 2-drops; contest with SI:7 and Edwin early
(HSTD Tempo guide: "a big early combo minion is strong vs Warrior"). Keep pressure, they armor up; Eviscerate face late.

**Shaman:** Flametongue Totem, Feral Spirit Taunts, Lightning Storm 3. Kill totems (Flametongue first) with dagger/
SI:7. Sap Feral Spirit Taunts only for lethal. Don't flood into Lightning Storm.

**Rogue (mirror):** removal-heavy. Keep minions at 3+ health (Golem, Yeti). Save Eviscerate for their Edwin or SI:7.
Watch for their Eviscerate/Cold Blood burst — trade aggressively.

**Druid:** Swipe, Wrath, Keeper of the Grove, Taunts (Ancient of War, Ironbark). Push early; use Sap/Assassinate on
Taunts when close to lethal; play around Swipe (keep minions at 2+ health where possible).

**Warlock (Zoo):** trade everything early; Backstab/dagger kill 1–2 health minions. Our 3/3s and Yeti outclass Zoo bodies.

**Priest:** Faerie Dragon dodges spells; Edwin and Tiger are big threats. Shadow Word: Death kills 5+ attack minions —
prefer several medium threats over one huge one.

---

## 12. Common mistakes

1. Playing the Combo card first (SI:7, Ringleader, Eviscerate, Edwin, Cold Blood) — always play the enabler first.
2. Hero powering over Assassin's Blade or a poisoned weapon.
3. Backstab on a damaged minion (illegal/useless) — use it before attacking that minion.
4. Attacking into Water Elemental with a minion we need next turn (it gets frozen).
5. Trading the hero into big minions with a weapon and dying to burn later. Rogue has no healing.
6. Going all-in on board after turn 6 vs Mage (Flamestrike) or Paladin (Consecration).
7. Using Assassinate on a 2–3 mana minion.
8. Wasting Cold Blood on a minion that cannot attack this turn without lethal in sight.
9. Ending a turn with unspent mana when the hero power was available and no weapon is equipped.

---

## 13. Script hints (machine-encodable)

**Mulligan**
- KEEP always: `CS2_072`, `EX1_134`, `EX1_131`, `NEW1_023`, `EX1_096`, `EX1_556`, `EX1_008`.
- KEEP if going second (Coin) OR hand has `CS2_072`/`EX1_008`/`EX1_010`: `EX1_613`.
- KEEP 1 copy: `EX1_124` (if opponent class is unknown keep one anyway); `EX1_010` only if no other ≤2 cost minion kept.
- KEEP if going second and a 2-drop and 3-drop are kept: one `CS2_182`; `EX1_133`.
- REPLACE everything else (`CS2_073`, `EX1_581`, `CS2_080`, `CS2_076`, `EX1_028`, `EX1_067`, `CS2_147`, `EX1_046`, `CS2_074`).

**Turn order (each turn)**
1. Lethal check (sum per §10). If lethal: enablers → burn (`EX1_124`, `EX1_134` target face) → buffs (`CS2_073` /
   `EX1_046` on a ready minion) → attack face with everything; clear Taunts first (`EX1_581` on the biggest Taunt).
2. Removal phase: kill must-kill minions with the cheapest sufficient tool:
   `CS2_072` (2 dmg, undamaged target) < weapon swing (if hero HP stays ≥12) < `EX1_134` combo (2) <
   `EX1_133` (1/2) < `EX1_124` (2/4) < trade minion < `CS2_076` (only target cost ≥4).
3. Attacks: favourable trades (killer survives) → value trades vs higher-cost minion → rest face.
4. Spend mana (greedy knapsack, maximize mana spent): cards with cost 0–1 first if a Combo card follows; Combo cards
   (`EX1_134`, `EX1_131`, `EX1_613`, `EX1_124`, `CS2_073`, `EX1_133`) only after ≥1 card already played this turn when possible.
5. Hero power if ≥2 mana left and no weapon equipped.
6. `end_turn`.

**Card priority by turn (when no combo/lethal applies)**
- T1: `EX1_008` > `EX1_010`. T1 with Coin: Coin + `EX1_131`.
- T2: `NEW1_023` > `EX1_131`(combo) > `EX1_096` > `EX1_131` > hero power.
- T3: `EX1_134`(combo) > `EX1_613`(combo, ≥1 card before) > `EX1_556` > `EX1_133` > 2-drop + 1-drop.
- T4: 1-drop + `EX1_134` > `CS2_182` > `EX1_046` > two 2-drops > `CS2_147`.
- T5: `EX1_028` > `CS2_182` + 1-drop > `CS2_080` (if no weapon) > `CS2_076` on cost≥5 threat.
- T6+: `EX1_067` > `EX1_028` > `CS2_182` > `CS2_147` (if hand ≤2) > others; use all mana.

**Target rules**
- `CS2_072`: undamaged enemy minion with health exactly 2 (or 1, or a Divine Shield) — highest Attack first.
- `EX1_134` / `EX1_133` battlecry: enemy minion with health ≤ damage, highest Attack; else Divine Shield; else face.
- `EX1_124`: enemy minion with health ≤ (4 if combo else 2) and Attack ≥3; else hold for face lethal (combo 4).
- `CS2_073` / `EX1_046`: friendly minion that can attack this turn (not `NEW1_023`), highest health.
- `EX1_581`: biggest-cost enemy Taunt blocking lethal; else enemy minion cost ≥5 when we're ahead on board.
- `CS2_076`: enemy minion with highest (cost, Attack), cost ≥4.

**Never**
- Never hero power while a weapon with Attack ≥2 is equipped.
- Never play `CS2_074` without a weapon equipped (or about to be equipped this turn).
- Never play `EX1_613` as the first card of a turn if any 0–1 cost card is playable first.
- Never target `NEW1_023` with our own spells (not allowed anyway).
- Never `CS2_076` a minion costing ≤3. Never `EX1_581` a minion costing ≤2.
- Never attack a minion with the hero if hero health after the hit < 12 (unless it gives lethal or saves us from lethal).
- Vs Mage on turn ≥7: never have more than 4 minions on board when already ahead.

**Face-vs-trade thresholds**
- Face if: enemy board total Attack ≤ 2, or our board Attack ≥ enemy board Attack + 4, or enemy hero ≤ 12 and our
  reach in hand (Eviscerate 4 + Cold Blood 4 + weapon + Commander 4) ≥ enemy hero health − our board Attack.
- Trade if: enemy board Attack ≥ our hero health / 2, or our hero ≤ 12.

---

## 14. Sources

- hearthstonetopdecks.com, "Aggro Rogue" — https://www.hearthstonetopdecks.com/decks/aggro-rogue-3/ — mulligan rules
  (keep Backstab + 1-drops; on Coin keep Ringleader + SI:7; vs Mage toss 1-toughness minions), game plan (early board →
  face, finish with Eviscerate/Assassin's Blade/Charge), Cold Blood targets (Argent Squire), weapon counts.
- hearthstonetopdecks.com, "Tempo Rogue Deck List Guide" — https://www.hearthstonetopdecks.com/deck-guide/tempo-rogue-deck-list-guide/
  — tempo is a mid-game deck (turns 3–6), keep combo cards only if they can be activated, keep burst in reserve,
  matchup notes (Warrior: big early combo minion; control: 2–3 minions, avoid overextending).
- hearthstonetopdecks.com, "Classic Aggro Rogue" — https://www.hearthstonetopdecks.com/decks/classic-aggro-rogue/ —
  basic+classic decklist template (Backstab, Cold Blood, Deadly Poison, Eviscerate, Sap, Edwin, SI:7, Assassin's Blade)
  and per-matchup mulligan keeps; adapted because it relies on Leeroy, Prep 3 and Cold Blood 1.
- icy-veins.com, "Aggro/Tempo Rogue Deck" (search excerpt; page blocked full fetch) — https://www.icy-veins.com/hearthstone/aggro-rogue-deck
  — Coin + cheap cards → early Edwin line is strong vs decks without hard removal; keep Backstab in most matchups.
- hearthstone.wiki.gg, "Edwin VanCleef" — https://hearthstone.wiki.gg/wiki/Edwin_VanCleef — cost history (3→4→3) confirming 3 mana.
- hearthstone.wiki.gg, "Miracle Rogue" — https://hearthstone.wiki.gg/wiki/Miracle_Rogue — archetype history; nerfs to
  Conceal, Leeroy, Auctioneer, Cold Blood, Preparation; basis of the Miracle-vs-Tempo decision.
- hearthstone.wiki.gg, "Tempo Rogue" (archived) — https://hearthstone.wiki.gg/wiki/Tempo_Rogue — tempo plan (board early,
  burst finish), return-to-hand re-triggers SI:7 (considered, cut for simplicity).
- hearthstone.wiki.gg, "Aggro Rogue" (archived) — https://hearthstone.wiki.gg/wiki/Hearthstone_Wiki:Archived/Aggro_Rogue —
  weapon + stealth aggro plan; Southsea Deckhand / Dread Corsair options.
- HSReplay, "The Art of the Mulligan" — https://articles.hsreplay.net/2019/04/15/the-art-of-mulligan/ — keep cards that
  contest the board early; mulligan depends on Coin and opponent class; how opponents beat Tempo Rogue (stabilize, keep life high).
- the card data (`pkg/hs-arena-0.2.2/data/cards.json`) — current card text, nerf list, Greedy Mage decklist and behaviour.
