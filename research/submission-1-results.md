# Submission 1 results: Control Paladin (script player, Haiku)

Source: the course results file `hw2-submission-1-control-paladin-results.zip` (`results.md`, `games.json`; not tracked).
Analysis scripts used: a per-game summary and turn log over `games.json`; `tools/opponents.py`.

## Score

| Opponent | Games | W–L | Forfeits | Illegal | Timeouts | Points |
|---|---:|---:|---:|---:|---:|---|
| Bot 1 | 6 | 6–0 | 0 | 0 | 0 | 5 completion + 3 |
| Bot 2 | 4 | 4–0 | 0 | 0 | 0 | 2 |
| Astra | 4 | 2–2 | 0 | 0 | 0 | +2 bonus |
| **Total** | 14 | **12–2** | 0 | 0 | 0 | **10/10 base + 2 bonus** (ladder not included) |

Base points are maxed. The remaining upside is the Astra bonus (+1 per win, up to 4) and the ladder.

## Who the opponents are (rebuilt lists: `research/opponents/`)

| Opponent | Deck | Evidence |
|---|---|---|
| Bot 1 | **Mage = the package's bundled `greedy_mage.json`** | 29 of 30 cards seen in 6 games, every count fits; Fireblast hero power. |
| Bot 2 | **Face Hunter** | 21 cards seen in 4 games (Explosive Trap from its reveal); the other 9 are guessed as second copies. |
| Astra | **Zoo Warlock** | 29 cards seen in 4 games; the 30th guessed as a 2nd Leper Gnome. Same opponent class and list in all 4 games. |

A second, independent rebuild (`research/opponents/submission1/`) reached the same lists.
The card lists are identical.

## The two Astra losses

Both losses came **going second**, and both wins came going first.
- **astra_04, died turn 11 (our 6th turn).**
  - Astra curved Flame Imp, Knife Juggler, Dire Wolf + Flame Imp, then Loot Hoarder + Squire + Mortal Coil.
  - After the mulligan our hand was Farseer, Aldor, Avenging Wrath, Lay on Hands, Harvest Golem and Guardian of Kings: no
    Consecration and no early board.
  - We were at 7 health on turn 10 with five enemy minions on board.
  - Questionable play: turn 6, Farseer healing our hero instead of developing Harvest Golem plus a 2-drop.
- **astra_02, died turn 21.**
  - Two Voidwalkers, then Dark Iron Dwarf ×2 and Defender of Argus, kept the board.
  - We cleared it with double Consecration on turn 16, but were at 4 health from turn 18.
  - Soulfire and Knife Juggler reach finished it.
  - Questionable play: turn 20, at 4 health, Darkscale Healer hit face instead of trading.

## Local check against the rebuilt lists (no model, 1,000 games per cell, half each seat)

| Our deck (self-play weights) | Bot 1 (greedy) | Bot 2 (greedy) | Astra list (greedy) |
|---|---:|---:|---:|
| **Control Paladin** | 91.1 | **95.3** | **93.0** |
| Counter Paladin | 92.0 | 88.4 | 90.2 |
| Steady Paladin | **92.5** | 87.8 | 86.9 |
| Infernal Warlock | 78.4 | 82.2 | 92.2 |
| Aggro Paladin | 87.0 | 84.9 | 83.6 |
| Pressure Hunter | 87.5 | 87.7 | 82.4 |
| Burst Shaman | 81.7 | 87.0 | 74.9 |

0 forfeits or voids.

Readings:
- **Real Astra is much stronger than a greedy pilot on its list.** Locally Control beats the greedy-piloted Astra list 93%. If
  that were Astra's true strength, losing 2 of 4 would have about a 4% chance.
- **We have no strong local stand-in for Astra yet.** Our planner plays the Zoo list worse than greedy does: Control wins
  96–97%. That holds even with a Zoo mulligan rule and face-heavy weights. Zoo battlecries (Abusive Sergeant, Dire Wolf
  adjacency, Defender of Argus, Shattered Sun, Dark Iron Dwarf) are only partly modelled for the opponent's side.
- **Control is still the best deck** against all three rebuilt opponents.
- Bot 1 and Bot 2 are no risk.

## Astra stand-in and tuning (2026-10-30, script vs script)

1. **Card model.** The planner now plays the Zoo cards it used to miss: Soulfire (never cast before), Abusive Sergeant and
   Dark Iron Dwarf (no target before), and Flame Imp's self-damage. Our script on Astra's list vs our tuned Control
   went from 4.8% to 24.2% (600 games).
2. **Imitation check** (`tools/imitate.py`, no games):
   - Over 37 Astra turns (188 decisions) from the returned games, our planner picks Astra's real move 71.8% of the time.
   - Weights fitted to copy Astra reach 78.8%: enemy_minion 3.0, face 0.75.
   - Those weights are *weaker* in play: 16.2% vs Control. So copying Astra's style does not make a stronger opponent.
   - The 2–2 is consistent with luck: at a 20–25% loss rate, 2+ losses in 4 games has about a 1-in-5 chance.
3. **Strength-tuned stand-in.** One pass of Astra's script against our top 5 decks raised its win rate from 29.8% to 32.6%:
   face 0.335, hand_per_cost 0.335, taunt 1.5. Weights: `games/astra_strong.json`.
4. **Our top 5 vs that stand-in and the bots.** Fresh seeds, 1,000 games per cell, 0 forfeits (`tools/astra.py`):

| Our deck | vs Astra script | vs Bot 1 | vs Bot 2 | Expected points (base wins + Astra) |
|---|---:|---:|---:|---:|
| **Control Paladin** | 77.4 | 90.6 | **94.4** | **7.97** |
| Counter Paladin | 75.5 | 91.9 | 90.9 | 7.90 |
| Infernal Warlock | **86.3** | 77.9 | 82.7 | 7.89 |
| Steady Paladin | 74.1 | **92.5** | 87.6 | 7.82 |
| Pressure Hunter | 61.6 | 86.7 | 87.3 | n/a |

- Expected points come from the binomial odds of the grading thresholds, plus 4 × the Astra win rate. Completion (5) is not included.
- Warlock is the best deck against Astra but costs base points against the bots. Control is the best overall, though the top four are within 0.15.
- Tuning Control against the Astra stand-in (one pass, 600 games per step) changed only weapon 0.6 → 0.9. Results were 78.6 / 91.4 / 94.8,
  within noise of the current weights (±2.6 at 1,000 games). **The Control weights are already as good as this tuning gets them.**

## Going second: strategy variants, no tuning (`tools/second_variants.py`)

Both real Astra losses came going second. Locally, Control beats the Astra script 84.5% going first but only 72.2%
going second. Tuning the weights on going-second games only gained under 1 point, which is noise.

Fixed strategy variants, current Control weights. Each variant played 2,000 games vs the Astra script (about half going
second) and 1,000 vs each bot; seeds 96000+; 0 forfeits. Planners now account for an *enemy* Doomsayer: it wipes both boards
at the start of the enemy's turn. Before that fix, the Astra script fed minions into our Doomsayer and D1 showed 80.8.

| Variant | Astra, we go 2nd | Astra, we go 1st | Bot 1 | Bot 2 | Expected points from wins |
|---|---:|---:|---:|---:|---:|
| Current list | 72.2 | 84.5 | 91.0 | 95.5 | 8.03 |
| Mulligan: keep 4-drops going 2nd | 71.1 | 84.5 | 91.6 | 95.6 | – |
| Mulligan: always keep Consecration | 72.6 | 85.3 | 90.7 | 95.4 | – |
| D1 −Alexstrasza −Guardian of Kings +2 Doomsayer | 78.0 | 90.1 | 92.6 | 93.3 | 8.27 |
| D2 −Alexstrasza −Guardian +Ooze +Ironbeak Owl | 72.8 | 85.4 | 89.5 | 92.0 | – |
| D3 −Alexstrasza −Guardian +2 Argent Protector | 74.9 | 87.0 | 93.3 | 93.5 | 8.16 |
| **D4 −Alexstrasza −Guardian −Avenging Wrath +2 Doomsayer +Ooze** | **78.9** | **90.9** | 92.2 | 94.1 | **8.30** |

Readings:
- **Mulligan changes do nothing** (±1).
- **Doomsayer is the one strategic change that helps against Zoo:** +6 going second and +6 going first. It punishes
  Zoo's board flooding, and the cut 7–9-cost cards were rarely cast in time against aggro.
- The bots are about even with the current list: Bot 1 slightly up, Bot 2 1–2 points down.
- Caveat: the Astra stand-in is our own planner. A real opponent that kills or plays around Doomsayer would shrink the gain.

### Doomsayer version vs our other decks (script vs script, 1,000 games per pairing, seeds 97000+)

| Opponent | Current Control | Doomsayer Control (D4) |
|---|---:|---:|
| Aggro Paladin | 57.5 | 51.4 |
| Burst Shaman | 62.0 | 59.3 |
| Counter Paladin | 42.6 | 45.5 |
| Infernal Warlock | 70.8 | 53.5 |
| Pressure Hunter | 51.5 | 52.2 |
| Steady Paladin | 45.9 | 46.5 |
| **Total** | **55.0** | **51.4** |

The Doomsayer list gains against Zoo but loses 3.6 points overall against our other decks, most against Infernal Warlock
(−17.3; it loses its late game vs Jaraxxus) and Aggro Paladin (−6.1). The ladder plays classmates' decks, so this trade
matters there.

### One- and two-card swaps (`tools/swaps.py`, current Control weights, no tuning)

Screen: 12 single swaps (cut Alexstrasza or Guardian of Kings; add Doomsayer, Argent Protector, Ooze, Ironbeak Owl, Knife
Juggler or Argent Squire). Each played 2,000 games vs the Astra script; full table in `games/swaps_screen.md`.
Doomsayer and Argent Squire were best going second; Ironbeak Owl was worse than the current list.

Full check. Astra 2,000 games (about half each way), bots 1,000 each, our 6 other script decks 1,000 each; 0 forfeits:

| Swap | Astra 2nd | Astra 1st | Bot 1 | Bot 2 | Aggro | Shaman | Counter | Warlock | Hunter | Steady | Our decks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Current list | 71.4 | 82.9 | 89.3 | 94.4 | 56.7 | 64.0 | 44.7 | 71.7 | 53.5 | 48.5 | 56.5 |
| **−Guardian of Kings +Doomsayer** | 76.4 | 88.1 | 93.3 | 95.3 | **59.8** | **67.7** | 47.9 | 67.1 | 55.3 | **52.3** | **58.4** |
| −Alexstrasza +Argent Squire | 74.1 | 87.5 | 91.7 | **95.9** | 57.3 | 66.5 | 45.1 | 69.0 | **55.6** | 48.5 | 57.0 |
| Both swaps | **76.7** | **88.3** | **94.2** | 95.0 | 59.6 | 64.8 | **49.0** | 63.4 | 51.0 | 49.2 | 56.2 |

**One swap, Guardian of Kings → Doomsayer, is better almost everywhere:**
- vs Astra: +5.0 going second, +5.2 going first;
- vs Bot 1: +4.0; vs our other decks: +1.9 overall;
- the only drop is Infernal Warlock, −4.6.

It keeps Alexstrasza, which the bigger two-card Doomsayer change (D4) lost; D4 was −17 vs Warlock. Adding Argent Squire on top
gains nothing more vs Astra and costs points against our other decks.
