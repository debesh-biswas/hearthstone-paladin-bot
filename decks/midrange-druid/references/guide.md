# Midrange / Ramp Druid: full guide (hs-arena, Basic + Classic Legacy pool)

All card text, costs and stats below are from `meta.md` §2 (the pool the engine actually uses), not from memory
of the 2014 game. Choose One option names and ids were read from the engine's card definitions.

---

## 1. Overview and win condition

A board-centric midrange Druid. It plays a cheap minion or removal spell on turns 2–3, uses light ramp
(Wild Growth, Innervate, Coin) to reach the 5–7 mana Taunt bodies a turn early, and wins by putting a big
body on the board every turn from turn 4 onward: Sen'jin, Yeti, Druid of the Claw, Sunwalker, Cairne, two
Ancients of War and Cenarius. Every one of those survives the Mage's single Flamestrike (4 damage) and most
survive Fireball (6) only barely or not at all, so the opponent runs out of answers before we run out of
threats.

**Win condition:** control the board from turn 4, then grind the opponent out with bigger minions. Close with
attacks plus Savage Roar (+2 to every character), Swipe to the face, Keeper's 2 damage, and Druid of the Claw
in Cat Form (4/4 Charge).

**Who is the beatdown?** Against aggro (Hunter, Zoo, aggro Warrior/Paladin/Rogue) we are the control deck:
trade, Taunt up, heal. Against slow or greedy decks (Greedy Mage, Control Warrior, Ramp Druid mirror) we are
the beatdown from turn 5 onward: keep attacking face whenever the trade is not clearly better.

---

## 2. Decklist

Curve: 0:1 · 2:5 · 3:6 · 4:8 · 5:3 · 6:3 · 7:3 · 9:1 (19 minions, 11 spells).

| # | Cost | Id | Name | Current text / stats | Role |
|--:|--:|---|---|---|---|
| 1 | 0 | `EX1_169` | Innervate | Gain 1 Mana Crystal this turn only. | Tempo: play a card one turn early |
| 2 | 2 | `EX1_154` | Wrath | Choose One: 3 dmg to a minion (**Solar Wrath** `EX1_154a`); or 1 dmg to a minion + draw (**Nature's Wrath** `EX1_154b`) | Early removal / cycle |
| 2 | 2 | `NEW1_023` | Faerie Dragon | 3/2. Can't be targeted by spells or Hero Powers. | 2-drop immune to Frostbolt/Fireblast/Polymorph |
| 1 | 2 | `EX1_066` | Acidic Swamp Ooze | 3/2. Battlecry: destroy opponent's weapon. | 2-drop + weapon tech |
| 2 | 3 | `CS2_013` | Wild Growth | Gain an empty Mana Crystal. (At 10 crystals: gives Excess Mana, 0 cost "draw a card") | Ramp |
| 2 | 3 | `EX1_556` | Harvest Golem | 2/3. Deathrattle: summon a 2/1 Damaged Golem. | Sticky 3-drop |
| 1 | 3 | `CS2_117` | Earthen Ring Farseer | 3/3. Battlecry: restore 3 Health. | 3-drop + heal |
| 1 | 3 | `CS2_011` | Savage Roar | Give your characters +2 Attack this turn. | Finisher |
| 2 | 4 | `CS2_012` | Swipe | 4 dmg to an enemy and 1 dmg to all other enemies. | AoE + reach |
| 2 | 4 | `EX1_166` | Keeper of the Grove | 2/2. Choose One: deal 2 dmg (**Moonfire** `EX1_166a`); or Silence a minion (**Dispel** `EX1_166b`) | Removal / silence |
| 2 | 4 | `CS2_179` | Sen'jin Shieldmasta | 3/5 Taunt | Early Taunt |
| 2 | 4 | `CS2_182` | Chillwind Yeti | 4/5 | Efficient body |
| 2 | 5 | `EX1_165` | Druid of the Claw | 4/4. Choose One: 4/4 Charge (**Cat Form** `EX1_165a`); or 4/6 Taunt (**Bear Form** `EX1_165b`) | Taunt wall / reach |
| 1 | 5 | `NEW1_007` | Starfall | Choose One: 5 dmg to a minion (**Starlord** `NEW1_007b`); or 2 dmg to all enemy minions (**Stellar Drift** `NEW1_007a`) | Hard removal / AoE |
| 1 | 6 | `EX1_164` | Nourish | Choose One: gain 2 (full) Mana Crystals (**Rampant Growth** `EX1_164a`); or draw 3 (**Enrich** `EX1_164b`) | Card refill |
| 1 | 6 | `EX1_032` | Sunwalker | 4/5 Taunt, Divine Shield | Sticky Taunt |
| 1 | 6 | `EX1_110` | Cairne Bloodhoof | 4/5. Deathrattle: summon a 4/5 Baine. | Two bodies in one card |
| 1 | 7 | `NEW1_008` | Ancient of Lore | 5/5. Choose One: draw a card (**Ancient Teachings** `NEW1_008a`); or restore 5 Health (**Ancient Secrets** `NEW1_008b`) | Body + draw or heal |
| 2 | 7 | `EX1_178` | Ancient of War | 5/5. Choose One: +5 Attack (**Uproot** `EX1_178b`, 10/5); or +5 Health and Taunt (**Rooted** `EX1_178a`, 5/10 Taunt) | Big Taunt |
| 1 | 9 | `EX1_573` | Cenarius | 5/8. Choose One: other minions +2/+2 (**Demigod's Favor** `EX1_573a`); or two 2/2 Taunt Treants (**Shan'do's Lesson** `EX1_573b`) | Top end |

Hero power **Shapeshift** (2): +1 Attack this turn and +1 Armor.

### Why these cards (and what was left out)
- **Faerie Dragon ×2:** the best 2-drop in this pool vs Mage (no Frostbolt, Fireblast, Polymorph, Fireball on it)
  and good everywhere else. Simple to play.
- **Acidic Swamp Ooze ×1:** a 3/2 for 2 that also breaks Fiery War Axe, Truesilver, Eaglehorn Bow, Doomhammer,
  Assassin's Blade. Never dead (still a 3/2).
- **Harvest Golem ×2, Earthen Ring Farseer ×1:** the 3-drop slot. Vicious Syndicate's Classic report preferred
  Farseer; Golem is stickier vs Mage pings. Both are zero-decision cards.
- **Sen'jin ×2, Yeti ×2:** Druid has no good class 4-drop minion any more (Keeper is a 2/2), so neutral bodies
  fill turn 4. Vicious Syndicate's "standard Combo Druid" build runs exactly these.
- **Sunwalker, Cairne:** sticky 6s. Sylvanas (Hall of Fame) and Ragnaros (Hall of Fame) are gone.
- **Ancient of War ×2, Ancient of Lore ×1:** Lore only draws 1 now, so War (5/10 Taunt) is the better Ancient.
- **Cenarius:** the only 9 worth playing; both modes are good.
- **Left out:** Force of Nature (5 mana, three 2/2s, no Charge: no burst, dies to Flamestrike/Consecration/Swipe,
  and it needs Savage Roar to be good, which is a combo a simple pilot plays poorly). Big Game Hunter (5 mana 4/2,
  few 7+ Attack targets in this pool; Boulderfist Ogre is 6/7). Black Knight (few Taunts in opposing lists).
  Ironbark Protector (8/8 Taunt for 8 is worse than Ancient of War). Starfire (6 mana 5 dmg; Starfall is cheaper).
  Mark of Nature / Mark of the Wild (buffs into Polymorph/Hex = card disadvantage). Power of the Wild (needs a wide
  board). Moonfire, Claw, Savagery, Bite (low value). Azure Drake, Ragnaros, Naturalize, Sylvanas: removed from pool.
- **Close calls, chosen for simplicity:** Ancient of Lore ×1 over a second Lore (heal-or-draw is one easy
  decision); one Savage Roar only (reach, not a combo plan); Wild Growth ×2 kept despite its 3-mana cost because
  "play it on turn 2 with Coin or turn 3 with nothing better" is an easy rule.

---

## 3. How the nerfs changed this deck vs the classic (2014) version

| Card | Classic version (online guides) | Our pool | Consequence |
|---|---|---|---|
| Innervate | Gain 2 Mana this turn | **Gain 1** | Only a one-turn tempo boost, costs a card. One copy. Never use it just to "ramp". |
| Wild Growth | 2 mana | **3 mana** | Turn-2 Wild Growth only with The Coin. Turn-3 WG costs your whole turn 3. |
| Nourish | 5 mana | **6 mana** | Almost always pick Draw 3 (Enrich). Ramp mode is rarely worth 6 mana. |
| Keeper of the Grove | 2/4 for 4 | **2/2 for 4** | It is a spell with a weak body now; dies to any ping. Use it for its effect only. |
| Force of Nature | 6 mana, three 2/2 Charge Treants that die at end of turn | **5 mana, three 2/2 (no Charge, permanent)** | The FoN + Savage Roar 14-damage combo is gone. Cut from the list. |
| Ancient of Lore | Draw 2 | **Draw 1** | Weaker; one copy. |
| Swipe | 4 mana | 4 mana | Unchanged; still core. |
| Druid of the Claw | 5 mana, 4/4 Charge or 4/6 Taunt | Same in our pool | Unchanged. (The 2021+ 6-mana 7/6 Rush / 4/9 Taunt versions on the wiki are NOT ours.) |
| Big Game Hunter | 3 mana | **5 mana** | Cut. |
| Ragnaros, Azure Drake, Sylvanas, Naturalize | Staples | **Removed (Hall of Fame)** | Replaced by Sunwalker, Cairne, Yeti, Keeper silence. |

Net effect: the deck is less "ramp" and more "midrange curve with a little ramp". It wins by having bigger
4–7 drops than the opponent, not by skipping turns.

---

## 4. Mulligan

General rule: we want a play on turn 2 or 3, plus (going second) one 4-drop. Wild Growth is only a keep in
specific hands. Throw away everything costing 5+.

| Card | Going first | Going second (Coin) |
|---|---|---|
| Faerie Dragon `NEW1_023` | Keep | Keep |
| Acidic Swamp Ooze `EX1_066` | Keep | Keep |
| Wrath `EX1_154` | Keep (1 copy) | Keep (1 copy) |
| Harvest Golem `EX1_556` | Keep | Keep |
| Earthen Ring Farseer `CS2_117` | Keep | Keep |
| Wild Growth `CS2_013` | Keep only if the hand also has a 2-drop AND a 4-drop | Keep (Coin + WG on turn 2 is the best ramp start) |
| Innervate `EX1_169` | Keep only with a 2-drop or a 4-drop in hand | Same |
| Sen'jin `CS2_179`, Yeti `CS2_182` | Keep one only if the hand already has a 2- or 3-drop | Keep one |
| Keeper of the Grove `EX1_166` | Toss (keep vs known Hunter/aggro only if you have an early drop) | Same |
| Swipe `CS2_012` | Toss (keep 1 vs Hunter/Paladin/Warlock/Rogue/Druid tokens if hand has an early drop) | Same |
| Savage Roar, Starfall, Nourish, all 5+ minions | Toss | Toss |

Note: the opponent's class is visible in the mulligan state. Against Mage, Faerie Dragon is the top keep.

---

## 5. Turn-by-turn game plan (ideal curve)

| Turn | Going first | Going second (Coin) |
|---|---|---|
| 1 | Nothing (hero power is a waste of 2 mana you don't have). Innervate + 2-drop only if both in hand and nothing else to do on turn 2. | Same. |
| 2 | Faerie Dragon / Ooze, or Wrath an enemy 2-drop. | Coin + Wild Growth if you have WG; otherwise a 2-drop. |
| 3 | Harvest Golem / Farseer; or Wild Growth if no 3-drop; or 2-drop + hero power. | 4 mana with WG: Sen'jin/Yeti. Otherwise a 3-drop. |
| 4 | Sen'jin / Yeti; Swipe if they have 2+ small minions; Keeper on a 2-health threat. | 5 mana with WG: Druid of the Claw (Bear) or Starfall. |
| 5 | Druid of the Claw (Bear Form by default); Starfall if they have a big minion or 3+ small. | 6: Sunwalker / Cairne / Nourish. |
| 6 | Sunwalker / Cairne; or 4-drop + 2-drop; Nourish (Draw 3) if your hand is 2 cards or fewer. | 7: Ancient of War (Rooted). |
| 7 | Ancient of War (Rooted) / Ancient of Lore. | 8: Ancient + hero power, or 6-drop + 2-drop. |
| 8–10 | Two cards a turn; Cenarius at 9. Savage Roar for lethal. | Same. |

Spend all your mana every turn. If two plays cost the same total, prefer: board minion > removal on a real
threat > card draw > hero power.

---

## 6. Card-by-card usage

- **Innervate** – Play it only in the same action sequence as a card it enables *this turn* (e.g. turn 3:
  Innervate + Sen'jin; turn 4: Innervate + Druid of the Claw). Never cast it alone. With 10 mana it is dead;
  it is fine to hold it.
- **Wrath** – Solar Wrath (3 dmg) to kill a 3-health minion (Mana Wyrm grown, Sorcerer's Apprentice, Knife
  Juggler, Harvest Golem). Nature's Wrath (1 dmg + draw) when a 1-health minion is the target or to finish a
  damaged minion. Never Wrath a minion your board can kill for free.
- **Faerie Dragon** – Play on 2. Vs Mage it is a permanent 3-damage clock their spells cannot touch. It cannot be
  buffed by your own targeted spells either (we run none).
- **Acidic Swamp Ooze** – Hold it 1–2 turns vs Warrior/Rogue/Paladin/Hunter/Shaman if a weapon is likely
  soon and you have another 2-drop; otherwise just play it on 2.
- **Wild Growth** – Turn 2 with Coin, turn 3 if no 3-drop, or turn 4+ only if mana would otherwise be wasted.
  At 10 crystals it gives Excess Mana (0: draw a card) – fine to cast late as a cycle.
- **Harvest Golem / Earthen Ring Farseer** – Turn 3. Farseer's heal: your hero if damaged by 3+, else a damaged
  friendly minion (it must target something; your own hero is always a legal fallback).
- **Savage Roar** – Lethal only (see §9). Exception: vs a slow deck when it adds 6+ face damage and the
  opponent is at ≤15, it can be used to race. Never use it to make trades.
- **Swipe** – Primary target: the biggest enemy minion with ≤4 health, while the 1 splash kills 1-health
  minions. Want to kill 2+ minions or kill 1 + 3 face damage. Target the hero (4 dmg) only for lethal or when
  there is nothing to kill. Splash also hits the enemy hero (and any target).
- **Keeper of the Grove** – Moonfire (2 dmg): kill a 2-health minion (Knife Juggler, Argent Commander after its
  shield is popped, Sorcerer's Apprentice 3/2) or finish a damaged one, or 2 face for lethal. Dispel (Silence):
  a Taunt in the way of lethal, Sunwalker (removes Taunt and Divine Shield), Cairne (no Baine), Water Elemental
  (no Freeze), enemy buffed minions (Mark of the Wild, Blessing of Kings, Power Word: Shield). Never silence your
  own minion.
- **Sen'jin / Yeti** – Turn 4. Sen'jin first vs aggro, Yeti first vs slow decks.
- **Druid of the Claw** – **Bear Form** (4/6 Taunt) by default. **Cat Form** (4/4 Charge) when: it gives lethal
  this turn, or it kills an enemy minion with ≤4 health that we must remove right now and the 4/4 survives
  (enemy attack ≤3), or vs a slow opponent with an empty board when you are ahead.
- **Starfall** – Stellar Drift (2 to all enemy minions) when it kills 2+ minions. Starlord (5 dmg) on a single
  threat with 5 health or less that our board can't trade into well (Yeti, Water Elemental, Stranglethorn
  Tiger after it has attacked). Don't use Starlord on a 2/2.
- **Nourish** – **Enrich (draw 3)** almost always. Rampant Growth only on turn 6 when your hand already holds
  2+ cards costing 7+ and you have at most 3 other cards.
- **Sunwalker** – Turn 6 Taunt; best vs Mage (Fireball pops the shield only) and aggro.
- **Cairne** – Turn 6, interchangeable with Sunwalker. Vs Mage play Sunwalker first if both are in hand
  (Fireball only pops its shield); Cairne next turn as the bait for Polymorph.
- **Ancient of Lore** – Ancient Teachings (draw 1) by default. Ancient Secrets (heal 5) when your hero is at
  ≤15 Health vs aggro or ≤10 vs anyone.
- **Ancient of War** – **Rooted** (5/10 Taunt) by default. **Uproot** (10/5) only when the opponent's board is
  empty, they are a slow deck, and you are not under pressure (it still can't attack this turn).
- **Cenarius** – Demigod's Favor (+2/+2 to your other minions) when you have 2+ minions on board (or it gives
  lethal next turn / with Savage Roar). Shan'do's Lesson (two 2/2 Taunts) when your board is empty or you are
  under pressure.

---

## 7. Combos, synergies, positioning

- **Coin + Wild Growth on turn 2** → 4 mana on turn 3 (Sen'jin/Yeti), 5 on turn 4 (Druid of the Claw).
- **Innervate + 4-drop on turn 3**, **Innervate + Druid of the Claw on turn 4**.
- **Savage Roar + board** for lethal: each attacking minion +2, hero +2 (+1 more with Shapeshift: hero attacks
  for 3). Cat Form Druid of the Claw adds a 6-damage charger with Roar.
- **Swipe + Keeper Moonfire** clears a 6-health minion (4 + 2) or a board of 1–2 health minions.
- **Cenarius Demigod's Favor** turns a 3-minion board into lethal threat the next turn.
- **Positioning:** this deck has no adjacency effects, so minion position never matters; the default position
  (rightmost, omit `position`) is fine for every minion.
- **Play around AoE:** vs Mage turn 7+, do not dump two small minions next to big ones for no reason; Flamestrike
  deals 4. Our 4-health minions (Cat Form Druid, Keeper, Faerie Dragon, Harvest Golem, Farseer, Ooze) die to it; 5+ health minions live.

---

## 8. Trading rules

1. Kill any minion that threatens lethal or has a strong ongoing effect first: Knife Juggler, Mana Wyrm,
   Sorcerer's Apprentice, Flametongue Totem, Wild Pyromancer, Questing Adventurer, Violet Teacher, Imp Master,
   Gadgetzan Auctioneer, Cult Master, Water Elemental (if it can't be ignored),
   Raid Leader / Dire Wolf Alpha / Stormwind Champion (buff auras).
2. **Favourable trade = take it:** our attacker kills the target and survives, or our cheaper minion kills a more
   expensive one.
3. **Even trade:** take it when we are the control deck (vs aggro), skip it and go face when we are the beatdown
   and the enemy minion is not threatening.
4. **Never** attack into a minion where ours dies and theirs survives, unless it clears a Taunt for lethal.
5. Taunts must be cleared before face; clear them with the least valuable attacker that does the job.
6. Hero attacks (Shapeshift) can finish a 1-health minion if your hero has enough Armor/Health to absorb the
   hit back (you take damage equal to the minion's Attack).
7. Face-vs-trade threshold: go face with everything if the opponent's total board Attack ≤ 3 and we are ≥ 10 HP
   ahead, or if the opponent is at ≤ (our board Attack × 2) and has no Taunt.

---

## 9. Hero power rules

- Shapeshift costs 2: +1 Attack this turn, +1 Armor. Use it with leftover 2 mana after playing cards.
- With the +1 Attack, the hero should attack: a 1-health minion (if its Attack is small) or the enemy hero.
- Don't hero-power instead of playing a card that uses the same mana.

---

## 10. Lethal checklist (every turn, before anything else)

Count damage that can reach the enemy hero this turn, after removing Taunts:
- Each friendly minion that can attack: its Attack (+2 each if you cast Savage Roar, cost 3).
- Druid of the Claw Cat Form from hand: 4 (6 with Roar), cost 5.
- Swipe to face: 4, cost 4 (the 1 splash can also finish a 1-health Taunt).
- Keeper Moonfire to face: 2, cost 4 (body can't attack this turn).
- Hero: Shapeshift 1 (cost 2), +2 with Roar.
- Wrath and Starfall can't hit the hero, but can kill a Taunt (Wrath 3, Starlord 5, Stellar Drift 2 to all).
- Silence (Keeper Dispel) removes Taunt.
If total ≥ enemy Health + Armor: clear Taunts first (with spells if possible), then go face with everything.
Mana check: Savage Roar 3 + Shapeshift 2 = 5; Roar + Swipe = 7; Roar + Cat Druid = 8.

---

## 11. Matchups

**Greedy Mage** (Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Water Elemental,
Fireball, Polymorph, Yeti, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike;
plays greedily, one action at a time, no lethal planning). **Favourable.**
- Mulligan for Faerie Dragon hard; it dodges all of their removal and their hero power.
- Kill Mana Wyrm and Sorcerer's Apprentice on sight (Wrath, Swipe splash, trades).
- Their removal is single-target: Frostbolt (3), Fireball (6), Polymorph. They have only 2 Polymorphs and 2
  Fireballs. Make them spend them on Yetis and Druids of the Claw before Ancient of War / Cenarius land.
- Flamestrike (×1, 7 mana) deals 4 to all our minions. From turn 7, prefer minions with 5+ health on the board
  (Sen'jin, Yeti, Bear Druid, Sunwalker, Cairne, Ancients) over 2/2 Keepers and 3/2s. After Flamestrike is used,
  go wide freely.
- Argent Commander (4/2 Charge Divine Shield): ping the shield with the Swipe splash or Keeper Moonfire, or block
  with a Taunt. Stranglethorn Tiger (5/5 Stealth) can't be targeted until it attacks; Swipe splash still hits it.
- Boulderfist Ogre (6/7): Ancient of War Rooted walls it; or trade two 4-attack minions; Keeper silence doesn't help.
- Their Taunts (Sen'jin 3/5) block lethal; keep Keeper Dispel or Starlord for it in the late game.
- Be the beatdown from turn 6: they are greedy and don't plan lethal, so pressure + Taunts is enough.

**Hunter (Face / Midrange).** Control role. Keep Wrath, Ooze (Eaglehorn Bow), Swipe. Taunts (Sen'jin, Bear Druid,
Sunwalker) shut down Beasts and Charge. Use Farseer and Ancient Secrets to heal. Their Hunter's Mark (2 mana) kills
any Taunt, so don't rely on one Taunt. Kill Starving Buzzard (5 mana now) and Houndmaster beasts first. Unleash the
Hounds (3) punishes going wide only lightly.

**Paladin (Aggro / Midrange).** Swipe and Stellar Drift kill Silver Hand Recruit tokens; Keeper Dispel on
Blessing of Kings / Tirion's Divine Shield body. Ooze on Truesilver/Light's Justice. Equality (4) + Consecration
wipes our board: don't play more than needed when already ahead. Avenging Wrath is 6 mana.

**Warrior (Aggro / Control).** Ooze for Fiery War Axe (3 mana now) / Arcanite Reaper / Gorehowl. Vs Control
Warrior be the beatdown, don't overextend into Brawl (keep 2–3 minions on board, hold the rest). Execute (2)
kills damaged big minions: Ancient of War Rooted is still the best body. Vs Aggro Warrior: Taunts + trades.

**Shaman (Midrange).** Kill Flametongue Totem and Mana Tide Totem first. Hex (4) and Lightning Storm (3) are their
removal; spread value. Swipe splash kills totems. Ooze for Doomhammer. Watch Overload: they are slow the turn after.

**Rogue (Aggro / Miracle).** Ooze on Assassin's Blade / their dagger. Kill Edwin VanCleef / Questing Adventurer /
Gadgetzan Auctioneer (6) immediately. Sap returns our big minion: replay it. Blade Flurry is 4 mana and minion-only
now. Be aggressive vs Miracle; they have little board.

**Warlock (Zoo).** Hardest matchup per Vicious Syndicate data. Keep Wrath, Swipe, 2- and 3-drops. Trade every turn;
Swipe/Stellar Drift on wide boards; Taunt up; heal with Farseer/Ancient Secrets. Kill Knife Juggler, Dire Wolf Alpha,
Defender of Argus taunts with removal.

**Druid (mirror, Token / Ramp).** Whoever gets ahead on board wins. Swipe their Treants (Force of Nature) and
Panther. Keeper Dispel their Ancient of War or Cenarius-buffed minion. Hold Savage Roar as lethal; they have it too,
so don't sit at low Health without Taunts.

**Priest.** Weak in this pool (most good cards Hall of Famed). Be the beatdown; Keeper Dispel their buffed minion.
Avoid overcommitting into Holy Nova (kills 2-health minions).

---

## 12. Common mistakes

1. Casting Innervate or Wild Growth on a turn that leaves no follow-up (card disadvantage for nothing).
2. Picking Cat Form by habit. Bear Form is the default; Cat is for lethal or a needed trade.
3. Using Nourish's ramp mode (it's 6 mana now; draw 3 is the better card).
4. Silencing (Keeper) or Wrathing a target the board could trade into for free.
5. Using Savage Roar for value trades instead of lethal.
6. Attacking face while the opponent builds a board that kills us; we are the control deck vs aggro.
7. Dumping the whole hand into a known AoE (Flamestrike at 7, Consecration, Brawl, Equality combo).
8. Forgetting the hero power with exactly 2 mana left.
9. Ending a turn with unspent mana when a cheaper card was playable.
10. Using online advice for Force of Nature / Keeper 2/4 / Nourish 5 / Innervate +2: those are not our versions.

---

## 13. Script hints (machine-encodable)

**Mulligan (keep list by card id):**
- Always keep: `NEW1_023`, `EX1_066`, `EX1_556`, `CS2_117`; one copy of `EX1_154`.
- Keep `CS2_013` if going second, or if going first with (a 2-drop) AND (a 4-drop) in hand.
- Keep `EX1_169` only if hand also contains a cost-2 or cost-4 card (excluding `CS2_013`).
- Keep one of `CS2_179`/`CS2_182` if going second, or if hand contains a cost 2 or 3 minion.
- Keep one `CS2_012` only if opponent class in {HUNTER, PALADIN, WARLOCK, DRUID, ROGUE} and an early drop is kept.
- Replace everything else (all cards cost ≥5, `CS2_011`, second `EX1_154`).

**Choose One defaults (option card_id → condition):**
- `EX1_165b` Bear Form default; `EX1_165a` Cat Form iff (lethal with it) or (opponent board empty and we are ahead).
- `EX1_178a` Rooted default; `EX1_178b` Uproot iff enemy board empty and enemy class in {MAGE, WARRIOR, PRIEST} and our HP ≥ 20.
- `NEW1_008a` draw default; `NEW1_008b` heal iff our HP ≤ 15 (aggro opp) or ≤ 10.
- `EX1_164b` draw 3 default; `EX1_164a` never unless hand contains ≥2 cards cost ≥7 and hand size ≤ 3.
- `NEW1_007a` Stellar Drift iff it kills ≥2 enemy minions; else `NEW1_007b` on the highest-Attack enemy minion with health ≤5.
- `EX1_154a` (3 dmg) iff target health ∈ {2,3}; `EX1_154b` (1 dmg + draw) iff target health = 1.
- `EX1_166a` (2 dmg) on a 2-health threat or enemy hero for lethal; `EX1_166b` (silence) on a Taunt blocking lethal, a buffed minion, Cairne, or a minion whose effect is worse than its body.
- `EX1_573a` iff our other minions ≥2; else `EX1_573b`.

**Play priority by turn (mana permitting, highest first):**
- Turn 2: if Coin and `CS2_013` → Coin + `CS2_013`; else `NEW1_023` > `EX1_066` > `EX1_154` on a 2–3 health minion.
- Turn 3: `EX1_556` / `CS2_117` > `CS2_013` > 2-drop + hero power. With 4 mana: `CS2_179` > `CS2_182`.
- Turn 4: `CS2_012` if it kills ≥2 minions > `CS2_179` (vs aggro) / `CS2_182` (vs slow) > `EX1_166` > 2-drop + 2-drop.
- Turn 5: `EX1_165` (Bear) > `NEW1_007` if it kills a threat > 4-drop + hero power.
- Turn 6: `EX1_032` / `EX1_110` > `EX1_164` (if hand ≤2) > 4-drop + 2-drop.
- Turn 7+: `EX1_178` > `NEW1_008` > 6-drop; at 9: `EX1_573`; then fill leftover mana with cheapest useful card, then hero power.
- `EX1_169` only together with a card it makes affordable this turn.
- `CS2_011` only in a lethal line.

**Targeting:**
- Removal target priority: (lethal-blocking Taunt) > Knife Juggler/Mana Wyrm/Sorcerer's Apprentice/Flametongue/
  Auctioneer/Violet Teacher/Questing Adventurer/Imp Master/aura minions > highest Attack minion that our board can't trade with > anything else.
- Swipe primary target: the enemy minion maximizing (kills) then (Attack); hero only for lethal or empty board.
- Farseer heal: own hero if missing ≥3 HP else most damaged friendly minion else own hero.

**Never:**
- Never cast `CS2_011` unless it produces lethal this turn (or opp ≤15 HP and Roar adds ≥6 face damage vs a slow deck).
- Never use `EX1_166b` / `EX1_154` on our own minions.
- Never attack a minion if ours dies and theirs survives (unless it clears a lethal-blocking Taunt).
- Never cast `EX1_169` alone. Never end turn with ≥2 unspent mana and hero power available.
- Never pick `EX1_164a` before turn 6 or without 7-cost cards in hand.

**Face vs trade thresholds:**
- Lethal available → all face (after Taunts).
- Opponent class aggressive (HUNTER, WARLOCK, PALADIN tokens) → trade whenever favourable or even.
- Otherwise: favourable trades yes; even trades only on threats (list above); rest face.

---

## 14. Sources

| URL | Used for |
|---|---|
| https://www.gosugamers.net/hearthstone/news/38226-the-ultimate-guide-to-ramp-druid-by-col-thejordude | Ramp Druid mulligan (ramp + 4–5 drops vs slow, answers vs aggro), plan-ahead Innervate rule, Druid of the Claw Taunt-by-default / Charge for reach, Ancient of Lore heal vs aggro, per-class matchup notes (play around Consecration/Equality, Brawl, Flamestrike; avoid overextending), common mistakes. |
| https://www.hearthstonetopdecks.com/decks/blindbisons-classic-ramp-druid/ | Classic Ramp Druid list (Harvest Golem, Yeti, Sen'jin, Sunwalker, Keeper, DotC, Ancients, Cenarius), mulligan priorities (Wild Growth, Wrath, Harvest Golem), notes that Farseer/Golem are better vs aggro. |
| https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/ | Sjow Ramp Druid and Token Druid lists; game plan "Wild Growth turn 2 then a Taunt every turn, Ancient of Lore refill". |
| https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/ | Classic Druid builds (standard/defensive/token), matchup data (Zoo beats Druid, Druid beats Face Hunter/Freeze Mage/Control Warrior), Farseer over Golem, "develop a minion every turn", Taunts as defence. |
| https://www.hearthstonetopdecks.com/which-cards-will-change-in-hearthstone-classic-format-list-of-original-unnerfed-cards-and-their-history/ | Druid nerf history (ramp nerfs, Force of Nature losing Charge, Keeper/Lore nerfs, Naturalize removal). |
| https://www.hearthstonetopdecks.com/decks/s26-legend-midrange-druid/ | Midrange Druid mulligan by opponent type (ramp to the 5–7 Taunt window, removal vs aggro), mistakes (overextending into Flamestrike/Brawl, being greedy with Swipe). |
| https://www.hearthstonetopdecks.com/decks/classic-midrange-druid-wild/ | Midrange Druid: "card draw is the weakness, value trade, hero power spare mana", turn-5 power turn. |
| https://hearthstone.wiki.gg/wiki/Druid_of_the_Claw | Patch history, confirming our 5-mana 4/4 Charge / 4/6 Taunt version is the 2017–2021 one (not the 6-mana modern card). |
| https://hearthstone.wiki.gg/wiki/Keeper_of_the_Grove | Patch history (2016 nerf to 2 Health = our version), option names Moonfire/Dispel. |
| https://www.pocketgamer.com/hearthstone/hearthstone-strategy-guide-basic-decks | Basic Druid: keep ramp + 2-drops. |
| (fetch failed, 403) https://www.icy-veins.com/hearthstone/classic-midrange-combo-druid-deck | Search snippet only: keep Innervate/Wild Growth, Wrath vs aggro, Keeper vs Face Hunter/Zoo. |
