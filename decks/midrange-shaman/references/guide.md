# Midrange Shaman — Deck Guide (hs-arena, Basic + Classic "Legacy" pool)

## 1. Overview and win condition

Midrange Shaman is a board-control deck. It answers early minions efficiently (Lightning Bolt, Earth Shock,
Rockbiter Weapon, Lightning Storm, Feral Spirit Taunts), develops sturdy 3–4 drops (Unbound Elemental, Harvest
Golem, Chillwind Yeti), removes the opponent's one big threat with Hex, and swings the board with Fire Elemental
(6/5 + 3 damage). Once the board is ours, it closes with burst: Doomhammer + Rockbiter (10 damage from hand), Al'Akir
(6 Charge damage through a Divine Shield), Argent Commander (4 Charge) and Lightning Bolt (3).

- **Against aggressive/tempo decks** (Hunter, Zoo, aggro Paladin/Warrior, tempo Mage): we are the control deck. Trade,
  keep our hero healthy, win with bigger cards later.
- **Against slower decks** (Greedy Mage, Druid ramp, Control Warrior): we are the beatdown from turn 5 on. Keep a
  board, push face once their minions are handled, finish with Doomhammer/Al'Akir.
- **Hero power, Totemic Call (2 mana):** summon a random basic Totem that you don't already control: Searing Totem 1/1,
  Stoneclaw Totem 0/2 Taunt, Healing Totem 0/2 (heals your minions 1 at end of turn), Wrath of Air Totem 0/2
  (Spell Damage +1). In this engine it cannot be used if all four are already on the board or the board is full.
  Totems are always placed on the **right end** of the board.

## 2. Decklist (30)

| # | Cost | Id | Name | Current text / stats | Role |
|--:|--:|---|---|---|---|
| 2 | 1 | `EX1_245` | Earth Shock | Silence a minion, then deal 1 damage to it. | Kills Divine Shield 1-health minions (Argent Commander!), removes Taunt/buffs/Deathrattles |
| 2 | 1 | `EX1_238` | Lightning Bolt | Deal 3 damage. Overload: (1) | Cheap removal or 3 face damage |
| 2 | 2 | `CS2_045` | Rockbiter Weapon | Give a friendly character +3 Attack this turn. | Early removal via hero attack; burst with Doomhammer/Al'Akir |
| 1 | 2 | `EX1_066` | Acidic Swamp Ooze | 3/2. Battlecry: Destroy your opponent's weapon. | 2-drop; weapon answer vs Warrior/Rogue/Paladin/Hunter |
| 1 | 2 | `EX1_012` | Bloodmage Thalnos | 1/1. Spell Damage +1. Deathrattle: Draw a card. | Makes Lightning Storm 3–4, Bolt 4; replaces itself |
| 2 | 3 | `EX1_248` | Feral Spirit | Summon two 2/3 Spirit Wolves with Taunt. Overload: (2) | Board + protection vs aggro |
| 2 | 3 | `EX1_565` | Flametongue Totem | 0/3. Adjacent minions have +2 Attack. | Turns small minions into trading machines |
| 2 | 3 | `EX1_259` | Lightning Storm | Deal 2-3 damage to all enemy minions. Overload: (2) | Board clear vs wide boards |
| 2 | 3 | `EX1_258` | Unbound Elemental | 2/4. Whenever you play a card with Overload, gain +1/+1. | Sturdy 3-drop that grows |
| 2 | 3 | `EX1_556` | Harvest Golem | 2/3. Deathrattle: Summon a 2/1 Damaged Golem. | Sticky 3-drop, good next to Flametongue |
| 1 | 3 | `EX1_575` | Mana Tide Totem | 0/3. At the end of your turn, draw a card. | Card draw (Azure Drake replacement) |
| 2 | 4 | `EX1_246` | Hex | Transform a minion into a 0/1 Frog with Taunt. | Hard removal for the biggest threat |
| 1 | 4 | `EX1_093` | Defender of Argus | 2/3. Battlecry: Give adjacent minions +1/+1 and Taunt. | Protect a lead / stabilise |
| 2 | 4 | `CS2_182` | Chillwind Yeti | 4/5 | Efficient 4-drop body (survives Flamestrike) |
| 1 | 4 | `CS2_147` | Gnomish Inventor | 2/4. Battlecry: Draw a card. | Card draw on a body |
| 1 | 5 | `EX1_567` | Doomhammer | 2/8 weapon, Windfury, Overload: (2) | 4 damage per turn for 4+ turns; burst with Rockbiter |
| 2 | 6 | `CS2_042` | Fire Elemental | 6/5. Battlecry: Deal 3 damage. | Big tempo swing; 3 damage removal or reach |
| 1 | 6 | `EX1_067` | Argent Commander | 4/2. Charge, Divine Shield | Reach (4) / kills a 4-health minion and survives |
| 1 | 8 | `NEW1_010` | Al'Akir the Windlord | 3/5. Charge, Divine Shield, Taunt, Windfury | 6 Charge damage + Taunt wall |

Curve: 1-cost 4 · 2-cost 4 · 3-cost 11 · 4-cost 6 · 5-cost 1 · 6-cost 3 · 8-cost 1. Overload cards: Bolt ×2, Feral ×2,
Storm ×2, Doomhammer (7 triggers for Unbound Elemental).

**Why these neutrals.** Azure Drake (Hall of Fame), Haunted Creeper, Loatheb, Sludge Belcher, Dr. Boom (not in the
pool) are gone. Replacements: Harvest Golem (closest to Haunted Creeper), Gnomish Inventor + Mana Tide (card draw),
Chillwind Yeti (solid 4-drop), Argent Commander (reach), Acidic Swamp Ooze (2-drop + weapon tech).
**Left out on purpose:** Big Game Hunter (5 mana, few 7-attack targets in this pool), The Black Knight (too narrow),
Windspeaker / Bloodlust (combo-dependent, hard for a simple pilot), Lava Burst (another Overload 2 three-cost card,
clogs the turn-3/4 mana), Earth Elemental (Overload 3 cripples the next turn), Stormforged Axe (weak with Overload),
Forked Lightning (random targets). When choices were close, the simpler card won (Yeti over Windspeaker, Golem
over Knife Juggler).

## 3. How the nerfs changed the deck (vs 2014)

| Card | 2014 | Our pool | Consequence |
|---|---|---|---|
| Flametongue Totem | 2 mana | **3 mana** | The famous "T3 Feral Spirit → T4 Flametongue between the wolves" no longer fits: after Feral's Overload you only have 2 mana on turn 4. Flametongue is now a turn 3 (with existing minions), 5 (with Bolt/Earth Shock/Rockbiter) or 6 (with Feral) play. |
| Rockbiter Weapon | 1 mana | **2 mana** | Doomhammer + Rockbiter now costs 7 (still 10 damage). Rockbiter + Bolt early removal costs 3. |
| Hex | 3 mana | **4 mana** | Hex now competes with our 4-drops; save it for real threats (6+ drops, Water Elemental, Cairne, Edwin, Ysera…), not 3-drops. |
| Lightning Storm | 2 mana (in some eras) | **3 mana, Overload 2** | Effectively 5 mana across two turns; use only when it kills 2+ minions or saves you. |
| Feral Spirit | 2 mana | **3 mana, Overload 2** | Still good vs aggro, but turn 4 after it is weak; prefer it on turn 4 with 1 spare mana or turn 6 with Flametongue. |
| Azure Drake | — | **removed** | Less card draw → Gnomish Inventor, Mana Tide, Thalnos. |
| Leper Gnome / Knife Juggler (opponents) | 2/1 / 3/2 | 1/1 / 2/2 | Opposing aggro is weaker; Lightning Storm 2 damage kills almost every aggro 1–2 drop. |
| Big Game Hunter | 3 mana | 5 mana | No longer a cheap tech; not included. |

## 4. Mulligan

General rule: we want a 2–3 mana play and cheap removal. Keep at most one "reactive" spell if it's not Bolt.

**Always keep:** Lightning Bolt (`EX1_238`), Unbound Elemental (`EX1_258`), Harvest Golem (`EX1_556`),
Feral Spirit (`EX1_248`), Acidic Swamp Ooze (`EX1_066`).
**Keep conditionally:**
- Flametongue Totem (`EX1_565`): keep if you also keep a 2–3 mana minion (it needs neighbours).
- Rockbiter Weapon (`CS2_045`): keep one copy vs aggressive classes (Hunter, Warlock, Paladin, Warrior, Rogue, Druid
  tokens) and vs Mage (kills Mana Wyrm / Sorcerer's Apprentice by attacking with the hero).
- Earth Shock (`EX1_245`): keep one vs Paladin/Warlock (Divine Shield, Taunt) or if hand already has a minion.
- Chillwind Yeti (`CS2_182`), Gnomish Inventor (`CS2_147`): keep one when **going second** (The Coin) and you
  already have a 2–3 drop.
- Lightning Storm (`EX1_259`): keep one vs Hunter / Warlock / Paladin / Druid (wide boards) when going second.
- Bloodmage Thalnos (`EX1_012`): keep only alongside Lightning Storm.
**Always toss:** Hex, Fire Elemental, Doomhammer, Al'Akir, Argent Commander, Defender of Argus, Mana Tide Totem,
second copy of any spell.

Going first: hand of 3. Toss aggressively for a 3-drop. Going second: hand of 4 + Coin; one 4-drop is fine.

## 5. Turn-by-turn game plan (ideal curve)

- **Turn 1:** Usually nothing. Lightning Bolt / Earth Shock only to kill a valuable 1-drop (Mana Wyrm, Knife Juggler,
  Flame Imp …). Otherwise pass.
- **Turn 2:** Acidic Swamp Ooze (destroy their weapon if any), or Totemic Call. Rockbiter on hero to kill a 2/x or
  3/x minion if the opponent's board is ahead. Coin + 3-drop is fine (not Coin + Feral unless facing heavy aggro).
- **Turn 3:** Unbound Elemental > Harvest Golem > Feral Spirit (vs aggro) > Flametongue (only next to 1+ friendly
  minion that can attack next turn). Lightning Storm if it kills 2+ minions.
- **Turn 4:** Chillwind Yeti / Gnomish Inventor / Hex on a real threat / Feral Spirit + Earth Shock or Bolt / 3-drop +
  Bolt. If overloaded 2 from Feral: Ooze, Rockbiter or Totemic Call.
- **Turn 5:** Doomhammer (when the board is stable — vs slow decks it's a clock), or Flametongue + Bolt/Earth Shock/
  Rockbiter, or 3-drop + Totemic Call, or Hex + Bolt.
- **Turn 6:** Fire Elemental (3 damage to the best target). Or Feral Spirit + Flametongue between the wolves.
  Or Argent Commander.
- **Turn 7:** Fire Elemental + Bolt, Hex + Lightning Storm, Doomhammer + Rockbiter (10 face when lethal-ish), 4-drop +
  3-drop.
- **Turn 8+:** Al'Akir (6 damage, Taunt, Divine Shield). Doomhammer swings each turn. Keep 2 mana for Rockbiter when
  the opponent is ≤ 10 (Doomhammer) or ≤ 12 (Al'Akir).

**Overload rules:** Before playing an Overload card, check what next turn needs. Do not go into turn 5 with 2 crystals
locked if you plan to play Doomhammer, or into turn 6 if you have Fire Elemental. Overload 1 (Bolt) almost never
matters. Play Unbound Elemental **before** any Overload card in the same turn.

## 6. Card-by-card notes

- **Earth Shock:** Best uses: kill Argent Commander / Scarlet Crusader / Argent Squire (silence removes Divine
  Shield, then 1 damage); remove Taunt (Sen'jin Shieldmasta, Sunwalker) to open lethal; silence a buffed minion,
  Water Elemental (removes Freeze effect), Cairne/Harvest Golem/Abomination deathrattles, Gurubashi Berserker.
  Never silence your own minions.
- **Lightning Bolt:** 3 damage to a 3-health minion (Sorcerer's Apprentice, Knife Juggler, Wolfrider) or to finish a
  damaged one. Hold 1 copy late as reach. With Thalnos/Wrath of Air: 4.
- **Rockbiter Weapon:** Target your hero to attack a minion (hero takes damage back — only do it at healthy life),
  or your own minion to trade up, or Doomhammer/Al'Akir for burst (Windfury doubles it: +6).
- **Acidic Swamp Ooze:** If the opponent has a weapon, play now. Otherwise a fine 3/2 on turn 2.
- **Bloodmage Thalnos:** Play it the same turn as Lightning Storm (3–4 damage to all) or before Bolt. Cheap filler
  late game.
- **Feral Spirit:** Vs aggro on curve. Vs slow decks better on turn 6 with Flametongue (4/3 Taunts) or with Unbound
  on board. Remember the Overload 2.
- **Flametongue Totem:** Place it **between** two friendly minions (use `position` = index of the right neighbour).
  Never play it on an empty board unless nothing else to do. Totems from the hero power always appear on the right
  end, so later totems will be next to Flametongue if it is on the right end.
- **Lightning Storm:** Play when it kills 2+ enemy minions (count only 2 damage as guaranteed) or the opponent's
  board threatens lethal. Vs Mage, Mana Wyrm 1/3 and Harvest Golem may survive the 2 roll.
- **Unbound Elemental:** Best 3-drop. Then add Overload cards (Bolt is cheapest) to grow it.
- **Harvest Golem:** Trade it freely; the 2/1 stays behind.
- **Mana Tide Totem:** Not on curve; play when you have spare mana (turn 5+ with 2 mana left or turn 4 with Bolt), ideally
  behind Taunt. Each turn it survives draws a card.
- **Hex:** For minions costing 5+ or a snowballing threat (Water Elemental, Boulderfist Ogre, Cairne, Ysera, Gruul,
  Core Hound / War Golem-sized bodies, Edwin VanCleef, Lightwarden huge). Cannot target Stealth minions (Stranglethorn Tiger).
  Hex removes deathrattles (Cairne, Sylvanas) cleanly.
- **Defender of Argus:** Put it between two minions (best between two healthy ones). Turns a lead into a wall.
- **Chillwind Yeti / Gnomish Inventor:** Turn-4 plays. Inventor when the hand is low.
- **Doomhammer:** Equip on 5+ when you are not under heavy pressure. Attack face twice per turn unless a minion
  must die. Hero takes damage when attacking minions — avoid hitting big minions with it. With Rockbiter: 10.
- **Fire Elemental:** 3 damage to the best target (kill a 3-health minion, finish a damaged big one) or face for lethal.
- **Argent Commander:** Kill a 4-health minion and keep a 4/2 (shield absorbs the hit), or 4 face for lethal.
- **Al'Akir:** Charge + Windfury: 6 face immediately, or kill two small minions. Keep it as a Taunt wall when behind.

## 7. Combos, synergies and positioning

- **Feral Spirit + Flametongue (6 mana):** wolves become 4/3 Taunts; place Flametongue between them.
- **Doomhammer + Rockbiter (7 mana):** 10 damage. **Al'Akir + Rockbiter (10 mana):** 12. **Al'Akir next to
  Flametongue:** 5 attack ×2 = 10.
- **Thalnos/Wrath of Air + Lightning Storm:** 3–4 damage AoE. **Thalnos + Bolt:** 4.
- **Unbound + any Overload card:** grows +1/+1 each time.
- **Defender of Argus:** +1/+1 and Taunt to both neighbours; place between your two best bodies.
- **Positioning:** keep the board as `[big minion] [Flametongue] [big minion]`. Attack with minions next to Flametongue
  **before** killing/trading Flametongue itself. Totemic Call lands rightmost.
- **Lightning Storm is one-sided** — no risk to our own board, so it can be played after developing.

## 8. Trading rules

1. Clear Taunts that block lethal first.
2. Kill minions that snowball or generate value every turn: Mana Wyrm, Sorcerer's Apprentice, Knife Juggler,
   Questing Adventurer, Mana Tide Totem, Imp Master, Cult Master, Gadgetzan Auctioneer, Water Elemental, Northshire-like
   engines, Wild Pyromancer, Flesheating Ghoul, Lightwarden, Violet Teacher, Hogger.
3. Trade when our attacker kills the target and survives, or when a cheaper/smaller minion of ours kills a bigger one.
4. Don't trade a big minion (Fire Elemental, Yeti) into a 1/1; use Rockbiter-hero, Earth Shock or a token.
5. Go face when the enemy board has no minion that can kill ours or threaten us, or when lethal is within 2 turns and
   we're ahead on board.
6. Enemy Freeze/Stealth: Stranglethorn Tiger can't be targeted until it attacks — answer it when it appears.
7. When behind on board, prefer AoE (Storm) + Taunt (Feral, Argus, Al'Akir) over racing.

## 9. Hero power rules

- Use Totemic Call whenever 2 mana is otherwise unused and there is a free board slot (and not all 4 totems in play).
- Turn 2 with no 2-drop: Totemic Call.
- Prefer playing cards over the hero power when both fit, unless the card is a situational spell (Hex, Earth Shock,
  Rockbiter) better kept for later.
- Vs Mage, a Searing Totem 1/1 dies to Fireblast — still worth it as a 1-for-1 of their mana.

## 10. Lethal checklist (every turn, before anything else)

Count: (a) attack of every friendly minion that can attack, ×2 for Windfury (Al'Akir), (b) hero weapon attack ×2 for
Doomhammer, (c) Lightning Bolt 3 each (+1 with spell damage), (d) Rockbiter +3 on a Windfury attacker = +6 (+3 otherwise),
(e) Fire Elemental battlecry 3, (f) Argent Commander 4 (Charge), (g) Al'Akir 6 (Charge + Windfury), (h) Flametongue +2
to each adjacent attacker. Subtract what is lost to clearing Taunts (Earth Shock removes a Taunt for 1 mana).
Divine Shield on an enemy Taunt absorbs one hit. If total ≥ enemy health + armor → go face with everything.

## 11. Matchups

- **Greedy Mage (Mana Wyrm, Sorcerer's Apprentice, Frostbolt, Arcane Missiles, Arcane Intellect, Water Elemental,
  Fireball, Polymorph, Yeti, Sen'jin, Stranglethorn Tiger, Boulderfist Ogre, Argent Commander, 1 Flamestrike):**
  - Their early drops (Wyrm 1/3, Apprentice 3/2) die to Bolt, Rockbiter-hero, Ooze trades. Kill Mana Wyrm early.
  - Their removal is single-target (Frostbolt/Fireball/Polymorph). Go wide-ish with sturdy bodies: Harvest Golem,
    Feral Spirit, Yeti (4/5 survives Flamestrike's 4), Unbound 3/5+.
  - Hex targets: Water Elemental, Boulderfist Ogre. Earth Shock: Argent Commander (kills it outright), Sen'jin (removes Taunt).
  - Stranglethorn Tiger (5/5 Stealth) can't be targeted until it attacks; then Hex it or trade Yeti + something.
  - Flamestrike only from turn 7 and only one copy: don't dump more than 3 small minions into it after turn 7;
    once it's been played, overextend freely.
  - They have no weapons; Ooze is just a 3/2. Doomhammer is excellent here (no weapon removal) and Al'Akir is a great
    finisher. Expect Polymorph on Fire Elemental / Al'Akir.
  - The bot plays greedily with no lethal planning: pressure face from turn 5–6 once its board is clean.
- **Hunter (face/midrange):** Be the control deck. Keep Feral Spirit, Bolt, Rockbiter, Golem. Lightning Storm kills
  Unleash hounds and small beasts. Ooze their Eaglehorn Bow/Gladiator's Longbow. Keep life high; Kill Command (3/5)
  and Steady Shot add reach. Don't race.
- **Paladin:** Earth Shock for Divine Shield (Argent Squire, Scarlet Crusader, Argent Commander) and Tirion (silence
  removes shield/taunt and deathrattle; Hex is cleaner). Ooze Truesilver/Ashbringer. Lightning Storm kills Silver Hand
  Recruits and Muster-style tokens. Save Hex for Tirion.
- **Warrior:** Ooze Fiery War Axe / Arcanite Reaper / Gorehowl. Aggro Warrior: be control, Taunts. Control Warrior:
  pressure with sturdy minions, don't overextend into Brawl (keep 2–3 minions), Hex Grommash/big minions, Doomhammer
  as a persistent clock. Execute targets damaged minions.
- **Shaman mirror:** Kill Unbound Elementals and Flametongue Totems immediately. Hex Fire Elemental / Al'Akir.
  Don't overextend into Lightning Storm.
- **Rogue:** Ooze their dagger or Assassin's Blade. Kill Edwin VanCleef / Questing Adventurer at once (Hex or Bolt +
  attacks). Equip Doomhammer early vs Miracle-style. Sap can bounce our Overload cards — no big deal.
- **Druid:** Kill ramp/early minions to stop snowballs. Hex Ancient of War/Lore, Druid of the Claw, Cenarius, Ironbark.
  Lightning Storm vs Force of Nature treants (no Charge in our pool) and tokens.
- **Warlock (Zoo):** Lightning Storm is the key card; keep it. Feral Spirit Taunts. Kill Knife Juggler, Flame Imp,
  Imp Master, Dire Wolf Alpha first. Earth Shock Voidwalker/Taunts when racing.
- **Priest:** Weak class in this pool (lost Northshire, Mind Blast, Auchenai, Holy Fire). Pressure early; Hex
  Cabal Shadow Priest / Lightspawn / big stolen minions; kill Lightwarden. Avoid giving Shadow Word: Death a 5+ attack target
  when a smaller threat does the job.

## 12. Common mistakes

1. Playing Feral Spirit on turn 3 and then having only 2 mana on turn 4 with nothing to do (plan Overload).
2. Playing Flametongue Totem on an empty board.
3. Using Hex on a 2–3 mana minion when Bolt/trades would do.
4. Attacking a large minion with the hero/Doomhammer and taking too much damage.
5. Forgetting the lethal check (Doomhammer + Rockbiter = 10, Al'Akir + Rockbiter = 12).
6. Trading Fire Elemental into a token instead of using cheap removal.
7. Playing Lightning Storm into one minion.
8. Overextending into Flamestrike (Mage turn 7+), Brawl (Warrior), Lightning Storm (Shaman).
9. Not using the 2 spare mana for Totemic Call.
10. Earth Shocking a Stealth minion (not targetable) or our own minion.

## 13. Script hints (machine-encodable)

**Mulligan**
- KEEP always: `EX1_238`, `EX1_258`, `EX1_556`, `EX1_248`, `EX1_066`.
- KEEP `EX1_565` iff hand also contains one of `EX1_258`, `EX1_556`, `EX1_066`, `EX1_248`.
- KEEP at most 1 `CS2_045`; at most 1 `EX1_245`.
- If going second (4 cards): KEEP at most 1 of `CS2_182`, `CS2_147`; KEEP at most 1 `EX1_259`.
- KEEP `EX1_012` iff `EX1_259` kept.
- REPLACE always: `EX1_246`, `CS2_042`, `EX1_567`, `NEW1_010`, `EX1_067`, `EX1_093`, `EX1_575`; second copies of spells.

**Turn order**
1. Lethal check (§10). If lethal: Earth Shock (`EX1_245`) enemy Taunts → Rockbiter (`CS2_045`) on Windfury attacker
   (Doomhammer hero or `NEW1_010`) → Charge minions (`NEW1_010`, `EX1_067`) → all attacks face → Bolt (`EX1_238`) face
   → Fire Elemental (`CS2_042`) target hero.
2. Removal on priority targets (see below).
3. Attacks: trades where attacker survives and kills; else face.
4. Spend mana: highest-value play that uses the most mana; play `EX1_258` before overload cards.
5. Hero power if ≥2 mana left and a board slot is free.
6. `end_turn`.

**Play priority by turn (when nothing urgent):**
- T2: `EX1_066` > hero power > `CS2_045` (hero, to kill a minion with health ≤3 when hero health ≥ 20).
- T3: `EX1_258` > `EX1_556` > `EX1_248` (if enemy has ≥2 minions) > `EX1_565` (if ≥1 friendly minion) > `EX1_259`
  (if it kills ≥2) > hero power.
- T4: `CS2_182` > `CS2_147` (if hand ≤3) > `EX1_246` on a priority threat > 3-drop + `EX1_238`/`EX1_245`.
- T5: `EX1_567` (if no Doomhammer equipped and enemy board attack ≤ 6) > `EX1_565` + 2-cost > 4-drop + 1-cost.
- T6: `CS2_042` > `EX1_248` + `EX1_565` > `EX1_067`.
- T8+: `NEW1_010` > `CS2_042` + 2-cost > two mid plays.

**Targets**
- `EX1_246` Hex: highest-cost enemy minion with cost ≥5, or Water Elemental / any minion with attack ≥5. Never on a
  Stealth minion, never on our own.
- `EX1_245` Earth Shock: (1) Divine Shield minion with health 1 after shield (Argent Commander, Scarlet Crusader, Argent
  Squire); (2) Taunt blocking lethal; (3) buffed/engine minion. Never our own.
- `EX1_238` Bolt: minion with health ≤3 (prefer highest attack), else enemy hero when lethal or late with no targets.
- `CS2_042` Fire Elemental: enemy minion with health ≤3 and highest attack; else damaged minion it finishes; else hero.
- `CS2_045` Rockbiter: our hero (with weapon or to kill health ≤3 minion when hero HP ≥ 20) / Doomhammer hero / Al'Akir for burst.
- `EX1_565` / `EX1_093` position: index between two friendly minions (position = index of right neighbour);
  if only one friendly minion, place next to it.

**Never**
- Never play `EX1_259` if it kills <2 minions unless enemy board attack ≥ our hero HP / 2.
- Never play an Overload-2 card when overload would stop next turn's planned 5–6 drop, unless survival needs it.
- Never attack with the hero into a minion whose attack ≥ our hero HP − 5.
- Never target our own minions with Hex/Earth Shock/Bolt.
- Never add `target` when the legal action lists no targets.

**Face vs trade thresholds**
- Go face if enemy has no minions, or enemy board attack total ≤ 3 and our hero HP ≥ 15.
- Trade if enemy board attack total ≥ 6 or any enemy minion is on the priority list.
- Always face when lethal is available this turn.

## 14. Sources

- HearthstoneTopDecks — Best Classic decks for every class (Kolento's Midrange Shaman): https://www.hearthstonetopdecks.com/best-hearthstone-classic-decks-for-every-class/
  — core list (Earth Shock, Bolt, Flametongue, Rockbiter, Feral, Hex, Storm, Mana Tide, Unbound, Fire Elemental, Al'Akir,
  Argus, Argent Commander), game plan (outlast aggro, pressure control, Al'Akir + Rockbiter burst), Feral→Flametongue line,
  "kill Unbound quickly".
- HearthstoneTopDecks — Greensheep's BlizzCon 2014 Midrange Shaman: https://www.hearthstonetopdecks.com/decks/greensheeps-blizzcon-2014-midrange-shaman/
  — Doomhammer ×2 + Al'Akir version, Harvest Golem / Gnomish Inventor / Harrison neutrals.
- HearthstoneTopDecks — Xiao Zhong's WCA 2014 Midrange Shaman: https://www.hearthstonetopdecks.com/decks/xiao-zhongs-wca-2014-midrange-shaman/
  — list with Lightning Bolt ×2, Unbound ×2, Mana Tide, Doomhammer + Al'Akir, Gnomish Inventor.
- HearthstoneTopDecks — Which cards changed in Classic: https://www.hearthstonetopdecks.com/which-cards-will-change-in-hearthstone-classic-format-list-of-original-unnerfed-cards-and-their-history/
  — Flametongue 2→3, Rockbiter 1→2, Hex 3→4.
- BlizzardWatch — Deck Tech: Revisiting Hearthstone's Shaman decks: https://blizzardwatch.com/2015/10/26/deck-tech-revisiting-hearthstones-shaman-decks/
  — don't Coin out Feral Spirit on turn 2, never play Flametongue alone, totems spawn on the right, Rockbiter vs early
  aggro minions, per-class matchup notes (Mage: Rockbiter kills Mana Wyrm; Paladin: Earth Shock Divine Shields,
  Storm vs tokens; Warrior: don't overextend into Brawl; Hunter: don't overextend into AoE).
- GosuGamers — Midrange Shaman guide by Devt: https://www.gosugamers.net/hearthstone/news/39067-hearthstone-deck-guide-midrange-shaman-by-devt
  — Overload management (don't enter key turns overloaded), Mana Tide not on curve, strong minions left with buffers in
  the middle, Doomhammer + Rockbiter 10 damage from empty board, keep Doomhammer vs slow classes only with early plays.
- Hearthstone Wiki — Totemic Call: https://hearthstone.wiki.gg/wiki/Totemic_Call — 2 mana, random basic totem, placed
  right; behaviour in our engine verified in the vendored fireplace code (no duplicates, unusable with all 4 out).
- the card data (`pkg/hs-arena-0.2.2/data/cards.json`) — current text/cost/stats of every card listed above; §3.4 Greedy Mage list.
