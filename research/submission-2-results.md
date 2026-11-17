# Submission 2 results and the early-game study

Submission 2 = Control Paladin with −1 Guardian of Kings +1 Doomsayer (commit e414c9e), script player, Haiku.
Source: the course results file (`results.md`, `games.json`; not tracked).

## Score

| Opponent | Games | W–L | Forfeits | Points |
|---|---:|---:|---:|---|
| Bot 1 | 6 | 6–0 | 0 | 5 completion + 3 |
| Bot 2 | 4 | 2–2 | 0 | 1 |
| Astra | 4 | 1–3 | 0 | +1 bonus |
| **Total** | 14 | **9–5** | 0 | **9 base + 1 bonus** (ladder not included) |

Submission 1 scored 12–2. Over both submissions, Bot 2 + Astra went 6/8 vs 3/8 (p ≈ 0.3), so the drop is
mostly variance, not the deck change. The opponent lists did not change; Astra showed a 2nd Mortal Coil, which
replaces the earlier guess (2nd Leper Gnome) in `opponents/astra-zoo-warlock.json`. All 30 Astra cards are now seen.

## Tougher local stand-ins (`tools/standins.py`)

Locally we beat Bot 2 ~95% and Astra ~80%, but real results were 6/8 and 3/8. Both opponent lists are now
script-piloted with weights tuned (one coordinate-descent pass, 400 games, seeds 71000) to beat our two lists.
Win % of our list, 1,000 games per cell, seeds 73000:

| Opponent | sub 1 1st | sub 1 2nd | sub 1 all | sub 2 1st | sub 2 2nd | sub 2 all |
|---|---:|---:|---:|---:|---:|---:|
| Bot 2 greedy | 96.8 | 93.2 | **95.0** | 97.6 | 92.6 | **95.1** |
| Bot 2 script, tuned | 84.0 | 79.0 | **81.5** | 81.0 | 75.6 | **78.3** |
| Astra script (old weights) | 82.0 | 67.6 | **74.8** | 84.6 | 74.8 | **79.7** |
| Astra script, tuned | 81.4 | 63.6 | **72.5** | 83.8 | 69.4 | **76.6** |

The tuned Bot 2 is close to the real one. The real Astra is still stronger than any local stand-in.

## The loss pattern

In the real losses we lose the board on our turns 2–4 against aggro and never get it back: Astra has 3–5 minions
with 8–12 attack while we have none. "Nothing to play but the hero power on turns 2–3" happened in only 1 of 7
losses. Equality was never played in a loss: without Wild Pyromancer or Consecration it is a dead card early.

## Fixes tested (`tools/early.py`)

Screen, 500 games per cell vs the tuned stand-ins (seeds 75000), total win %:

| Variant | Total |
|---|---:|
| current (sub 2) | 77.4 |
| A: aggro mulligan (keep Consecration + a 4-drop) | 78.6 |
| B: spend cards sooner (hand_per_cost ×0.5) | 77.5 |
| C: hand_per_cost 0 | 78.0 |
| **D: −1 Equality +1 Doomsayer** | **80.2** |
| E: −1 Equality +1 Acidic Swamp Ooze | 79.5 |
| F: −2 Equality +Doomsayer +Ooze | 80.0 |

Fresh-seed confirm (seeds 77000, 2,000 games per stand-in):

| List | Astra 2nd | Astra 1st | Bot 2 2nd | Bot 2 1st | aggro all | Bot 1 |
|---|---:|---:|---:|---:|---:|---:|
| current (sub 2) | 71.2 | 83.9 | 78.2 | 82.6 | **79.0** | 93.0 |
| D −Equality +Doomsayer | 75.3 | 88.9 | 78.1 | 83.6 | **81.5** | 93.3 |
| D + aggro mulligan | 75.3 | 88.9 | 78.3 | 85.2 | **81.9** | 93.6 |
| sub 1 list | 65.3 | 83.2 | 76.9 | 83.2 | **77.2** | 92.1 |

Ladder proxy (our six other script decks, seeds 78000, 1,000 games each):

| List | aggro-paladin | burst-shaman | counter-paladin | infernal-warlock | pressure-hunter | steady-paladin | all |
|---|---:|---:|---:|---:|---:|---:|---:|
| current (sub 2) | 57.8 | 65.1 | 49.2 | 68.6 | 56.2 | 52.5 | **58.2** |
| D −Equality +Doomsayer | 59.0 | 66.7 | 51.1 | 62.3 | 58.1 | 52.6 | **58.3** |

**Reading:** D is the best change found (+2.5 points vs aggro, +4 going second vs Astra, flat elsewhere, −6 vs
Infernal Warlock). Not applied to `player/`; it is left here as the next step if the work is picked up again.
