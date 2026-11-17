# Midrange Hunter ("Sunshine" / Beast Hunter): Deck Guide

Pool: hs-arena 0.2.2, `basic-classic-1` (modern Legacy Basic + Classic, nerfs applied, Hall of Fame removed).
Every card text below was checked against the card data (`pkg/hs-arena-0.2.2/data/cards.json`) / `data/cards.json`, not taken from memory or old guides.

---

## 1. Overview and win condition

Midrange Hunter is a **board-first beast curve deck with a free 2-damage clock**. It plays a Beast on turns 2 and 3,
buffs it with Houndmaster on turn 4, lands sticky threats on 5–6 (Stranglethorn Tiger, Savannah Highmane), and
closes with Kill Command (5 to face with a Beast out), Steady Shot every turn, Eaglehorn Bow swings, Tundra Rhino
charge and King Krush.

**How it wins:**
1. Win the early board with efficient 2- and 3-drop Beasts. Trade when the trade is clean.
2. Keep the board through turns 4–6 with Houndmaster Taunts and threats that need 2 removal spells each (Highmane).
3. Steady Shot fills every leftover 2 mana. Over a game it adds 10–16 damage that the opponent can't block.
4. Finish with burst from hand: Kill Command ×2 (10 damage), Steady Shot (2), Bow (3), charging Beasts.

The deck is **midrange, not face**. Against faster boards it controls first. Against slow or greedy decks (like the Greedy Mage
bot) it becomes the beatdown from turn 4–5 on.

---

## 2. Decklist (30)

| # | Cost | Id | Name | Current text (this pool) | Role |
|---:|---:|---|---|---|---|
| 2 | 1 | `DS1_185` | Arcane Shot | Deal 2 damage. | Cheap removal (Mana Wyrm, Sorcerer's Apprentice, 2-health minions), or 2 reach |
| 2 | 2 | `EX1_531` | Scavenging Hyena | 2/2 Beast. Whenever a friendly Beast dies, gain +2/+1. | 2-drop that grows from trades and from Highmane |
| 2 | 2 | `CS2_172` | Bloodfen Raptor | 3/2 Beast | Aggressive 2-drop Beast |
| 2 | 2 | `CS2_120` | River Crocolisk | 2/3 Beast | Sturdy 2-drop Beast (survives Fireblast / Arcane Shot) |
| 1 | 2 | `EX1_611` | Freezing Trap | Secret: When an enemy minion attacks, return it to its owner's hand. It costs (2) more. | Tempo vs big minions (Yeti, Ogre, Commander, Tiger) |
| 1 | 2 | `EX1_610` | Explosive Trap | Secret: When your hero is attacked, deal 2 damage to all enemies. | Anti-swarm/aggro, 2 face damage |
| 2 | 3 | `NEW1_031` | Animal Companion | Summon a random Beast Companion: Misha 4/4 Taunt, Leokk 2/4 (other minions +1 Attack), or Huffer 4/2 Charge. | Best 3-drop: always a Beast, 4/4 Taunt or 4/2 Charge |
| 2 | 3 | `EX1_539` | Kill Command | Deal 3 damage. If you control a Beast, deal 5 damage instead. | Finisher (5 face) or hard removal |
| 2 | 3 | `CS2_125` | Ironfur Grizzly | 3/3 Beast, Taunt | Board/Taunt 3-drop, Houndmaster target |
| 2 | 3 | `EX1_536` | Eaglehorn Bow | Weapon 3/2. Whenever a friendly Secret is revealed, gain +1 Durability. | Kills X/3s and X/2s, 3 face damage per swing |
| 1 | 3 | `EX1_617` | Deadly Shot | Destroy a random enemy minion. | Hard removal when the enemy has one (big) minion |
| 1 | 3 | `EX1_170` | Emperor Cobra | 2/3 Beast, Poisonous | Kills any big minion it hits |
| 1 | 3 | `CS2_203` | Ironbeak Owl | 2/1 Beast. Battlecry: Silence a minion. | Silence Taunts (Sen'jin), buffed or Deathrattle minions |
| 2 | 4 | `DS1_070` | Houndmaster | 4/3. Battlecry: Give a friendly Beast +2/+2 and Taunt. | Turn-4 power play: 4/3 body + permanent buff |
| 1 | 4 | `DS1_183` | Multi-Shot | Deal 3 damage to two random enemy minions. | 2-for-1 when the enemy has exactly 2 minions |
| 2 | 5 | `EX1_028` | Stranglethorn Tiger | 5/5 Beast, Stealth | Threat that can't be targeted the turn it lands |
| 1 | 5 | `DS1_178` | Tundra Rhino | 2/5 Beast. Your Beasts have Charge. | Surprise damage: every Beast played after it charges |
| 2 | 6 | `EX1_534` | Savannah Highmane | 6/5 Beast. Deathrattle: Summon two 2/2 Hyenas. | Best card: needs 2 answers, survives Flamestrike |
| 1 | 9 | `EX1_543` | King Krush | 8/8 Beast, Charge (Legendary) | Top-end finisher: 8 immediate face damage |

**Curve:** 1-cost ×2 · 2-cost ×8 · 3-cost ×11 · 4-cost ×3 · 5-cost ×3 · 6-cost ×2 · 9-cost ×1.
**Beast sources (for Kill Command / Houndmaster / Hyena / Rhino):** 18 cards (Hyena, Raptor, Croc, Companion, Grizzly,
Cobra, Owl, Tiger, Rhino, Highmane, Krush), plus the Hyena tokens from Highmane.

**Why these choices (simple pilot):** no Tracking (an extra discover-style choice with little payoff), no Unleash the Hounds
or Starving Buzzard (both nerfed, see §3), no Dire Wolf Alpha or Defender of Argus (positional). Secrets are fire-and-forget,
which suits a small model. Where two cards were close (e.g. Chillwind Yeti vs a Beast), the Beast won because it powers Kill
Command and Houndmaster.

---

## 3. How the nerfs changed the deck vs the 2014 version

Online lists (Reynad, Amaz 2014; "Sunshine Hunter" by Lifecoach) were built on original card versions. In this pool:

| Card | 2014 version | This pool | Consequence |
|---|---|---|---|
| Starving Buzzard | 2 mana 3/2 | **5 mana** 3/2 | A 5-mana 3/2 is unplayable. The Buzzard + Unleash draw engine is gone. **Cut.** |
| Unleash the Hounds | 2 mana | **3 mana** | Without Buzzard it's just 1/1 chargers. Only good with Hyena / vs wide boards. **Cut** for consistency. |
| Hunter's Mark | 0 (later 1) mana | **2 mana** | Too slow to pair with trades. Cobra, Owl, Deadly Shot, Kill Command do the job. **Cut.** |
| Leeroy Jenkins | 4/5 mana | **Removed (HoF)** | Amaz's list loses its 6-damage finisher. Replaced by King Krush and more Beasts. |
| Webspinner, Haunted Creeper, Loatheb | Naxx | **Not in pool** | Replaced by Bloodfen Raptor / River Crocolisk / Emperor Cobra. |
| Flare | 1 mana | 2 mana | Only good vs secret decks. **Cut** (Greedy Mage plays no secrets). |
| Leper Gnome / Knife Juggler | 2/1, 3/2 | 1/1, 2/2 | Not used. The deck relies on 2-mana Beasts instead. |
| Oasis Snapjaw | 2/7 Beast | same | vS calls it "quite unplayable". Not used. |
| Kill Command, Houndmaster, Highmane, Animal Companion, Eaglehorn Bow, Tundra Rhino, Steady Shot | | **unchanged** | The core of the midrange plan survives intact. |

Net effect: the deck lost its **card draw** (Buzzard) and its **cheap reach** (Leeroy, 0-mana Mark). It's now a fair midrange
deck that wins on **board + Highmane value + Steady Shot**. Don't expect to refill the hand: spend cards efficiently and
don't throw them away.

---

## 4. Mulligan

Starting hand: 3 cards going first, 4 going second (The Coin comes after the mulligan).

**Always keep**
- 2-drop Beasts: Bloodfen Raptor `CS2_172`, River Crocolisk `CS2_120`, Scavenging Hyena `EX1_531`.
- Animal Companion `NEW1_031`.
- Ironfur Grizzly `CS2_125`, Emperor Cobra `EX1_170`.

**Conditional keeps**
- Houndmaster `DS1_070`: keep if the hand also has a 2- or 3-mana Beast (or going second with Coin).
- Eaglehorn Bow `EX1_536`: keep if the hand already has a 2-drop. Good vs Mage/Hunter/Rogue early minions.
- Arcane Shot `DS1_185`: keep **one** vs Mage (Mana Wyrm, Sorcerer's Apprentice). The class is hidden until the game starts,
  so in practice keep one only if the hand has no other cards to play early.
- Ironbeak Owl `CS2_203`: keep only going second with another early play.
- Explosive Trap `EX1_610`: keep only if the hand already has 2-drops (it's a weak opener).
- Going second (4 cards + Coin): you may also keep **one** of Stranglethorn Tiger or Houndmaster if the rest of the hand is good.

**Always toss**
- Kill Command (it's a finisher, it'll be there later), Deadly Shot, Multi-Shot, Freezing Trap, Tundra Rhino,
  Savannah Highmane, King Krush, and Tiger going first.

Rule of thumb: you want to play something on turn 2 **and** turn 3. Throw back everything costing 4+ unless the hand
already has both.

---

## 5. Turn-by-turn game plan (ideal curve)

| Turn | Mana | Ideal play | Notes |
|---:|---:|---|---|
| 1 | 1 | Arcane Shot only on a real target, otherwise nothing | Don't Arcane Shot face early. |
| 2 | 2 | 2-drop Beast (Raptor > Hyena > Croc), or Steady Shot | With nothing to play, Steady Shot (2 to face). |
| 3 | 3 | Animal Companion > Grizzly > Cobra > 2-drop + Arcane Shot > Bow | Coin + Houndmaster on 3 is fine if a Beast is on board. |
| 4 | 4 | Houndmaster on a Beast | No Beast? Play a 3-drop Beast + 1 mana, or a 2-drop + Steady Shot. |
| 5 | 5 | Stranglethorn Tiger, or 3-drop + Steady Shot, or Houndmaster + Arcane Shot | Tundra Rhino only with Beasts in hand to follow. |
| 6 | 6 | Savannah Highmane | Or Tiger + Arcane Shot / 4-drop + Steady Shot. |
| 7 | 7 | 5-drop + Steady Shot, or Highmane + Arcane Shot, or two 3-drops + Arcane Shot | Spend all 7. |
| 8 | 8 | Highmane + Steady Shot, or Houndmaster + Kill Command | |
| 9 | 9 | King Krush (8 charge) | If the board is lost, Krush can still trade or go face. |
| 10 | 10 | Krush + Arcane Shot, or Kill Command ×2 + Steady Shot / Bow for burst | Look for lethal every turn. |

**Mana rule:** spend as much mana as possible every turn. Leftover 2 or more → Steady Shot.

---

## 6. Card-by-card notes

- **Arcane Shot** (1): kill a 2-health minion (Sorcerer's Apprentice 3/2, Argent Commander 4/2 after its Divine Shield pops,
  Stormpike/Jungle Panther-type X/2s). Mana Wyrm is 1/3: Arcane Shot only kills it after it has taken 1 damage. Finish a damaged minion. Late game it's 2 reach.
- **Bloodfen Raptor / River Crocolisk / Scavenging Hyena** (2): play on 2. Hyena wants other Beasts to die next to it: trade
  your other Beasts first, then attack with Hyena. Each Beast that dies gives it +2/+1 (Highmane dying = +2/+1, then its two
  Hyena tokens dying give +4/+2 more).
- **Freezing Trap** (2): play when the enemy has (or is about to have) a big minion that will attack: Yeti, Ogre, Water
  Elemental, Argent Commander, Tiger. It bounces the first attacking minion, costing +2. Great tempo when you're ahead.
- **Explosive Trap** (2): play when the enemy has several small minions or a weapon hero that will hit face. Also 2 face damage.
  Don't play it with no enemy board vs Mage (they rarely attack face with minions early).
- **Animal Companion** (3): best 3-drop. Huffer (4/2 Charge) can trade immediately; Leokk buffs other minions' attack,
  so attack with others after it lands; Misha is a 4/4 Taunt.
- **Kill Command** (3): 5 damage with a Beast on board, 3 without. **Default: hold it as reach.** Use it as removal only when the
  target would otherwise take over the game (Water Elemental freezing your board, Boulderfist Ogre / Tiger you can't trade into,
  a minion that kills you next turn). Always check that a Beast is on board before casting for 5.
- **Ironfur Grizzly** (3): 3/3 Taunt Beast. Good vs aggro, and a fine Houndmaster target (5/5 Taunt).
- **Eaglehorn Bow** (3): 3/2 weapon. Use the hero to kill 3-health or smaller minions when the hit-back damage is fine, or swing
  face. Secrets that trigger add +1 Durability. Don't attack a big minion with the hero (you take its attack back).
- **Deadly Shot** (3): best when the enemy has exactly one minion (guaranteed), or when every enemy minion is worth killing.
- **Emperor Cobra** (3): Poisonous. Send it into the enemy's **biggest** minion (kills anything). It's a great Houndmaster target
  (4/5 Poisonous Taunt).
- **Ironbeak Owl** (3): silence a Taunt blocking lethal, a buffed minion, Water Elemental's freeze, Harvest Golem's Deathrattle,
  or Sen'jin's Taunt. If nothing needs silencing, it's a 2/1 Beast: play it on an enemy minion anyway only if the template
  requires a target, picking the most annoying enemy one, never your own.
- **Houndmaster** (4): play only with a friendly Beast on board. Buff priority: a Beast that **survives longer** (Cobra →
  4/5 Poisonous Taunt; Croc → 4/5; Grizzly → 5/5; Misha → 6/6; Highmane → 8/7 Taunt). If the enemy board is empty and you're
  racing, buff the Beast with the highest attack. Without a Beast it's a vanilla 4/3: acceptable only if there's no other play.
- **Multi-Shot** (4): best with exactly 2 enemy minions that have 3 or less health. With 1 enemy minion it only hits that one.
- **Stranglethorn Tiger** (5): 5/5 Stealth. It can't be targeted by Frostbolt/Polymorph/Fireball until it attacks. Play it on
  an empty-ish board and attack next turn. Good vs Mage.
- **Tundra Rhino** (5): your Beasts have Charge. Play it **after** you've decided the attacks this turn, or on turns when you
  can follow next turn with Highmane/Krush/Tiger (all charge). With Rhino, Highmane is 6 instant damage and Krush is 8 anyway.
- **Savannah Highmane** (6): play it on 6 almost always. Trade with it freely: its Deathrattle leaves 2× 2/2 Hyenas.
  vs Mage it survives Flamestrike (4 damage to a 6/5) but is the prime Polymorph target.
- **King Krush** (9): 8/8 Charge. On an open board it's 8 face damage. Use it to remove a big Taunt only if that enables lethal
  next turn or saves the game.

---

## 7. Combos, synergies and positioning

- **Beast → Houndmaster** (turn 3 Beast, turn 4 Houndmaster): the main tempo swing. Have a Beast survive turn 3.
- **Kill Command + any Beast on board**: 5 damage for 3 mana. If your only Beast may die in combat, cast Kill Command **before**
  attacking with it.
- **Highmane + Scavenging Hyena**: Highmane dying gives Hyena +2/+1; the Hyena tokens dying give +2/+1 each.
- **Tundra Rhino + Highmane / Tiger / Companion / Krush**: everything charges the turn it's played.
- **Secret + Eaglehorn Bow**: a revealed secret refunds a Bow charge. Play the secret, then use the Bow normally.
- **Leokk**: other minions +1 Attack. Play it before attacking.
- **Positioning:** almost none required. Leokk buffs all other minions (not adjacency). Play minions to the right (default).
  Nothing in the deck cares about adjacency, so omit `position` unless needed.

---

## 8. Trading rules

Priority each turn (after the lethal check):

1. **Kill enemy minions that would kill you, or win the race against you.** Count their total attack next turn vs your health.
2. **Trade when it's clean**: your attacker kills the target and survives, or a cheaper minion trades with a more expensive one
   (Cobra into Ogre, Raptor into Sorcerer's Apprentice).
3. **Kill high-value enemy engines** even at a slight loss: Sorcerer's Apprentice (cheaper spells), Mana Wyrm (grows), Water
   Elemental (freezes), Knife Juggler, Flametongue Totem, Imp Master, Cult Master, Questing Adventurer, Violet Teacher.
4. **Go face** with everything else when the enemy has no threats you must answer.

**Face-vs-trade thresholds:**
- If the enemy board can deal ≥ half your current health next turn, trade first.
- If the enemy is at ≤ 15 health and you have more board attack than they do, prefer face.
- If you'd have lethal next turn by going face now (and they can't kill you), go face.
- Don't trade into Divine Shield with a high-attack minion. Pop it with the smallest attacker, Arcane Shot or a Bow swing
  (Steady Shot hits heroes only).

**Enemy minion priority (highest first):** Taunt blocking lethal → Water Elemental → Sorcerer's Apprentice → Mana Wyrm →
Argent Commander → Boulderfist Ogre / Stranglethorn Tiger (when it's revealed) → anything with ≥ 4 attack → the rest.

---

## 9. Hero power rules (Steady Shot, 2 mana, 2 damage to the enemy hero)

- No target needed. It always hits the enemy hero (Taunts don't block it).
- Use it whenever 2 mana is left after card plays. Order: play cards first, then hero power.
- Turn 2 with no 2-drop: Steady Shot.
- Prefer a card over the hero power when the card affects the board (e.g. a 2-drop Beast on turn 2).
- On turns where card plays leave 0–1 mana, skip it; don't hold back a minion just to Steady Shot.
- Late game, if the enemy is ≤ 2 + your burst, count it in the lethal check.

---

## 10. Lethal checklist

Add up, then compare to enemy health + armor:
- Every friendly minion that can attack this turn and isn't blocked (Taunts must die first).
- Charge from hand: Huffer 4 (if Companion rolls it, can't plan on it), King Krush 8, any Beast played after Tundra Rhino.
- Kill Command: 5 each with a Beast on board (3 without).
- Arcane Shot: 2 each.
- Eaglehorn Bow: 3 if equipped and the hero hasn't attacked, or 3 mana to equip and swing.
- Steady Shot: 2 (2 mana).
- Explosive Trap: only if they attack (not part of your own turn).

Mana check: e.g. 10 mana = Kill Command ×2 (6) + Steady Shot (2) + Arcane Shot (1) = 12 damage from hand.
If a Taunt blocks lethal: Owl silence it, Kill Command / Arcane Shot / Bow it, or trade the smallest minion that kills it.

---

## 11. Matchups

### Greedy Mage (bot: Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Water Elemental, Fireball, Polymorph, Yeti, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike)
**You are the beatdown.** The bot plays greedily one action at a time and only has one Flamestrike.
- Keep: 2-drop Beasts, Animal Companion, Bow, one Arcane Shot.
- Early: kill Mana Wyrm and Sorcerer's Apprentice immediately (Arcane Shot, Bow, Raptor trade).
  River Crocolisk (2/3) survives Fireblast and trades with Mana Wyrm (1/3) without dying to it. Mana Wyrm needs 3 damage:
  Bow it, trade Raptor/Croc into it, or Arcane Shot it after a hit (Steady Shot only hits the hero).
- Midgame: Houndmaster Taunts stop Argent Commander's charge from going face. Freezing Trap is excellent: their Yeti/Ogre/
  Commander attack into it and come back costing 2 more.
- Water Elemental (3/6, freezes): kill it with Cobra, Kill Command + a trade, or Owl to silence the freeze and keep attacking.
- Sen'jin Taunt: trade small Beasts into it or Owl it. Don't waste Kill Command unless it blocks lethal.
- Flamestrike (7 mana, 4 to all your minions): from turn 7 on, don't dump extra small minions if your board already wins.
  Highmane (5 health) and Tiger (5 health) survive it. Houndmastered Croc/Cobra (5 health) survive it too.
- Polymorph will hit Highmane/Tiger. Two Highmanes + Tiger + Krush give more big threats than they have answers.
- Their Stranglethorn Tiger: you can't target it until it attacks. Deadly Shot can still hit it (random, untargeted).
- Steady Shot every spare turn: Mage has no healing in this list.

### Hunter (mirror / Face Hunter)
- Board control matters most. Trade, don't race, unless clearly ahead.
- Explosive Trap is strong vs their 1/1s and Hounds. Grizzly / Houndmaster Taunts slow their face damage.
- Their Kill Command and Steady Shot mean your life total matters: keep it above ~10 when possible.
- Deadly Shot / Cobra for their Highmane (Cobra still leaves the 2/2 Hyenas).

### Paladin (Aggro / Shockadin / Control)
- vs Aggro: Taunts (Grizzly, Misha, Houndmaster) + trades. Explosive Trap kills Silver Hand Recruits and 1/1s.
- Consecration (4 mana, 2 to all enemies) wipes 2-health minions: prefer Croc/Grizzly/Cobra over Raptor/Hyena into it on turn 4+.
- Equality (4 mana, sets health to 1) + Consecration is their board clear: don't overextend in the midgame.
- Divine Shields (Argent Squire, Scarlet Crusader, Argent Commander): pop with Arcane Shot / smallest attacker.
- Tirion / Truesilver: Owl silences Tirion (removes Divine Shield + Taunt + Deathrattle weapon).

### Warrior (Aggro / Control)
- Armor Up cancels Steady Shot, so don't count on the hero-power clock; win on board.
- Fiery War Axe (3 mana) and Execute/Shield Slam remove your minions one at a time: play threats one per turn, Highmane
  value matters most.
- vs Aggro Warrior: Taunts and trades; keep your health up. Explosive Trap punishes weapon swings to face.
- Brawl (5 mana): don't put 3+ minions on a board you already win.

### Shaman (Midrange)
- Their totems and Flametongue (0/3, adjacent +2 Attack): kill Flametongue Totem first. Lightning Storm (3 mana, 2–3 to all
  enemy minions) kills 2–3 health minions.
- Hex (4 mana) answers Highmane/Tiger. Expect it; keep a second threat in hand.
- Fire Elemental / Feral Spirit Taunts: Owl or trade small Beasts into the Wolves.
- Their overload turns are when to push damage.

### Rogue (Aggro / Tempo)
- Their weapon and Backstab/SI:7 remove small minions. Croc/Grizzly/Cobra are better than Raptor here.
- Blade Flurry (4 mana, minions only) is their AoE: don't overextend.
- Explosive Trap punishes dagger hits to face. Kill Edwin VanCleef immediately (Kill Command / Deadly Shot / Cobra).

### Druid (Ramp / Token / Aggro)
- Be the beatdown vs Ramp: pressure before their Ancients and Taunts land. Owl silences Ironbark Protector Taunts and Ancient
  of War Taunt.
- vs Token Druid: Explosive Trap and Multi-Shot are strong; Savage Roar burst means keep Taunts up.
- Keeper of the Grove can silence Highmane (no Hyenas). Swipe (4 mana) deals 4 to one enemy and 1 to the rest.

### Warlock (Zoo)
- Trade aggressively early: Zoo wins with board. Explosive Trap and Multi-Shot are great.
- Hellfire (4 mana, 3 to ALL characters) kills almost your whole early board: keep 2 minions max out when ahead.
- Life Tap gives them cards; you can't out-value them, so take the board and race with Steady Shot.

### Priest
- Their hero power heals 2, cancelling Steady Shot. Win on board. Their removal is thin in this pool (no Mind Blast, Holy Fire,
  Auchenai): Highmane and Tiger stick.

---

## 12. Common mistakes

1. Casting Kill Command as removal early when a minion trade or Arcane Shot would do. It's your finisher.
2. Casting Kill Command for 3 by mistake: make sure a Beast is on board (and attack with it **after** casting if it'll die).
3. Playing Houndmaster with no Beast on board when a Beast + Steady Shot was possible.
4. Forgetting Steady Shot with 2 spare mana.
5. Attacking a big minion with the hero (Bow) and taking 6+ damage back.
6. Dumping the whole hand into Flamestrike / Consecration / Hellfire range when already ahead on board.
7. Attacking into a Divine Shield with your biggest minion.
8. Sending Emperor Cobra into a small minion instead of the biggest threat.
9. Using Ironbeak Owl on your own minion (only silence enemies).
10. Holding Highmane back. It's the best card: play it on curve.
11. Playing Tundra Rhino at the end of a turn with no Beasts to follow next turn (a 2/5 for 5 mana).

---

## 13. Script hints (machine-encodable rules)

**Mulligan (by card id)**
- KEEP always: `CS2_172`, `CS2_120`, `EX1_531`, `NEW1_031`, `CS2_125`, `EX1_170`.
- KEEP `DS1_070` if hand contains any of {`CS2_172`,`CS2_120`,`EX1_531`,`NEW1_031`,`CS2_125`,`EX1_170`,`CS2_203`} or going second.
- KEEP `EX1_536` if hand contains a 2-cost Beast.
- KEEP at most one `DS1_185`.
- KEEP `EX1_610`, `CS2_203` only going second with another kept card costing ≤ 3.
- Going second: KEEP at most one card with cost ≥ 4 (prefer `DS1_070`, then `EX1_028`).
- REPLACE everything else: `EX1_539`, `EX1_617`, `DS1_183`, `EX1_611`, `DS1_178`, `EX1_534`, `EX1_543`.

**Turn procedure**
1. Lethal: `dmg = sum(attack of ready unblocked friendly minions) + 5*count(EX1_539 affordable, if beast on board else 3) +
   2*count(DS1_185 affordable) + (3 if bow ready) + (2 if hero power unused and mana ≥ 2) + charge-from-hand`. If
   `dmg ≥ enemy health + armor` (after spending mana budget in this order: Kill Command, Arcane Shot, Steady Shot), go face
   with everything; clear Taunts first with the smallest sufficient attacker or spell.
2. If an enemy Taunt exists and lethal is blocked only by it: Owl (`CS2_203`) it, or Arcane Shot / Kill Command it if health ≤ damage.
3. Trades (see below).
4. Spend mana: pick the card set maximizing mana spent, ties broken by priority list below.
5. If mana ≥ 2 and hero power unused: `hero_power` (no target).
6. Attack face with remaining ready minions (and Bow if no worthwhile minion target).
7. `end_turn`.

**Card play priority (higher first, when affordable and legal)**
- `EX1_534` Highmane (6) > `DS1_070` Houndmaster **only if friendly Beast on board** > `EX1_028` Tiger > `NEW1_031` Companion >
  `CS2_125` Grizzly > `EX1_170` Cobra > `CS2_172` Raptor > `EX1_531` Hyena > `CS2_120` Croc > `EX1_536` Bow (if no weapon) >
  `CS2_203` Owl (only with a worthy target) > secrets `EX1_611`/`EX1_610` (only if that secret isn't already active) >
  `DS1_178` Rhino (only if a Beast in hand can be played next turn, or same turn with charge) > `EX1_543` Krush.
- Removal spells are played in the trade step, not for curve.

**Target rules**
- `DS1_070` Houndmaster target: friendly Beast with highest (health) among {Cobra, Croc, Grizzly, Misha, Highmane}; else highest attack.
- `EX1_539` Kill Command: enemy hero if part of lethal or no minion threatens; else enemy minion with health ≤ 5 (≤ 3 if no Beast) and
  highest attack, only if it can't be traded cleanly.
- `DS1_185` Arcane Shot: enemy minion with health ≤ 2 (or a Divine Shield to pop), prefer engines (`EX1_608` Sorcerer's Apprentice,
  damaged `NEW1_012` Mana Wyrm) then highest attack; else hold; face only for lethal.
- `CS2_203` Owl: enemy Taunt blocking lethal > enemy with Deathrattle/freeze/buffs > highest-attack enemy minion. Never friendly.
- `EX1_617` Deadly Shot: cast when enemy minion count == 1 and its attack ≥ 4, or when all enemy minions have attack ≥ 3.
- `DS1_183` Multi-Shot: cast when enemy minion count == 2 and both have health ≤ 3, or count == 1 and it has health ≤ 3 with
  attack ≥ 4; else hold.
- `EX1_170` Cobra attack target: enemy minion with highest attack (or highest cost).

**Attack/trade rules**
- Trade if (attacker kills target and survives) OR (target attack ≥ 4 and attacker cost < target cost) OR (target is an engine:
  Mana Wyrm, Sorcerer's Apprentice, Water Elemental, Knife Juggler, Flametongue Totem, Imp Master, Violet Teacher, Questing Adventurer).
- Taunts must be killed before face; use the smallest minion that kills it.
- Divine Shield target: attack with the lowest-attack minion first.
- Hero (Bow) attacks a minion only if hero health > 10 after taking its attack, and the minion's attack ≤ 3.
- Go face otherwise. If enemy board total attack ≥ my hero health / 2, trade before face.

**Never do**
- Never cast `EX1_539` without a friendly Beast unless it's lethal or the only way to survive.
- Never cast `DS1_070` with no friendly Beast when another play of equal mana exists.
- Never target own minions with `CS2_203`, `DS1_185`, `EX1_539`.
- Never play a second copy of the same active secret (`EX1_611`/`EX1_610`).
- Never hold 2+ unspent mana with the hero power unused.
- Never play 3+ new small minions into a board you already win vs Mage after turn 6, vs Paladin after turn 3, vs Warlock after
  turn 3, vs Warrior after turn 4.
- Never send `target` unless the legal-action template lists targets; never send `position` for spells/weapons.

---

## 14. Sources

| URL | What was taken |
|---|---|
| https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/ | Reynad's 2014 Midrange Hunter list (Flare, Mark, Tracking, Freezing Trap, Hyena, Buzzard, Companion, Bow, Kill Command, Unleash, Houndmaster ×2, Highmane ×2, Boar, Croc, Snapjaw, Tiger); game plan (Beast synergy, curve topping at 6 with Highmane); Buzzard + Unleash as the classic engine (now dead). |
| https://www.hearthstonetopdecks.com/decks/amazs-vgvn-naxxramas-midrange-hunter/ | Amaz's 2014 list: confirms core (Companion ×2, Kill Command ×2, Houndmaster ×2, Highmane ×2, Deadly Shot, Explosive Trap, Stranglethorn Tiger, Ironbeak Owl) and that Leeroy was the finisher (removed here). |
| https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/ | Sunshine Hunter origin (Lifecoach), game plan (mid-game threats vs Druid/Warrior), weakness vs aggro; Stranglethorn Tiger strong next to Highmane; Snapjaw "unplayable"; Hyena pays off tokens; Buzzard/Timber Wolf/Hunter's Mark underperform; Control Warrior counters Hunter. |
| https://www.pocketgamer.com/hearthstone/hearthstone-deck-guide-midrange-hunter | Mulligan (keep 1–2 drops, Explosive Trap vs aggro, Freezing Trap vs control), hold Kill Command as finisher, Deadly Shot is guaranteed with one target, Explosive Trap timing (wait for more targets), Freezing Trap not on Battlecry minions, Priest/Warrior hero power cancels Steady Shot. |
| https://www.shacknews.com/article/85323/hearthstone-boosting-your-hunter | Tundra Rhino charge synergy, Hyena with token deaths, Highmane's Deathrattle as the real threat (Hex/Polymorph are the counters), Deadly Shot for one big minion, Multi-Shot for two mid minions. |
| https://hearthstone.wiki.gg/wiki/Midrange_Hunter | Archetype definition: take early board control and snowball; Houndmaster to trade up; Kill Command/Bow/Deadly Shot as late-game removal. |
| https://outof.cards/hearthstone/decks/15924-hunting-ranks-with-rexxar (search summary) | Mulligan: something to play on turns 1–3, toss 4+ and Kill Command; Houndmaster as a board-solidifying card. |
| https://www.icy-veins.com/hearthstone/midrange-hunter-deck (search summary; page returned 403) | Mulligan for the strongest curve; keep Animal Companion with a 1- and 2-drop. |
