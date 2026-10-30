# Script player: four Paladin decks compared (no model)

Date: 2026-10-28. All games are local and model-free: our turn planner (`player/scripts/move.py`) plays each deck;
opponents are the course greedy bot on our deck lists, or our planner on another list. 0 forfeits, 0 voids,
0 illegal actions in every run below.

## Method (same for every deck)

1. **Card model.** The planner models every card in the four lists (keywords from the official card data;
   explicit effects for battlecries, spells, deathrattles, Cult Master, Wild Pyromancer, Sea Giant / Dread Corsair
   cost changes). Self-check: `tools/test_move.py`. Offline: 168,101 recorded Paladin decisions, 0 illegal, max 0.02 s.
2. **Mulligan per deck**, from each deck's guide (Steady's from its playbook §3).
3. **Tuning:** identical coordinate-descent pass for each deck (`tools/tune.py`, seeds 1000, 300 games per
   opponent per run, same field and same grid of 7 weights). Results and every run: `games/tune/<deck>.json`.
4. **Fresh seeds** (5000, 500 games per opponent, 15 greedy opponents) and a **script-vs-script round robin**
   (seeds 9000, 1,000 games per pairing, half in each seat): `tools/compare.py`, output `games/compare.md`.

## Results

| Deck | Tuned weights | vs greedy field (7,500 games) | Script vs script (3,000 games) |
|---|---|---:|---:|
| **Counter Paladin** | enemy_minion 1.2, danger 10, our_hp 8 | 93.9% | **57.5%** |
| Steady Paladin | enemy_minion 1.2, danger 10, draw 1.5 | 94.9% | 52.7% |
| Control Paladin | face 0.3, enemy_minion 1.2, danger 10, draw 4.5 | **95.1%** | 49.8% |
| Aggro Paladin | hand_per_cost 0.25, taunt 2.5 | 91.7% | 40.0% |

Script vs script, win % of row deck (1,000 games each, ±3 points at 95%):

| vs | Aggro | Control | Counter | Steady |
|---|---:|---:|---:|---:|
| Aggro | – | 45.9 | 37.4 | 36.7 |
| Control | 54.1 | – | 44.5 | 50.9 |
| Counter | 62.6 | 55.5 | – | 54.4 |
| Steady | 63.3 | 49.1 | 45.6 | – |

Readings:
- **Aggro is the weakest of the four** in both tests; it lost every pairing (36.7–45.9%).
- **Counter wins every head-to-head**, including Steady 54.4% and Control 55.5% (both beyond the ±3 noise).
- **Against the greedy field the three newer lists are tied** (93.9–95.1%); the field is too weak to separate them.
- Steady vs Control is even (49.1/50.9).
- Caveat: the head-to-head uses our own planner on both sides. Counter's extra draw (Cult Master, Blessing of
  Wisdom) is valued by our evaluation; a stronger or different opponent pilot may change the order. No model-played
  or Mystery Bot games yet.

## Added 2026-10-28: Astra's Burst Shaman, Infernal Warlock, Pressure Hunter

The planner was extended to Shaman, Warlock and Hunter: their hero powers, plus Overload, Spell Damage, Silence, Hex,
Beasts, Jaraxxus and Doomsayer. Offline: 169,108 recorded states across 4 classes, 0 illegal, max 0.03 s. Each new deck was
tuned with the same `tools/tune.py` pass. Caveat: the Paladin decks were tuned earlier against 12 greedy opponents, the new
three against 15; the grid and the budget are the same. The full output is in `games/compare7.md` and `games/pilots.md`.
There were 0 forfeits or voids in any run.

| Deck (our planner) | Tuned weights | vs greedy field (7,500) | Script vs script, 7 decks (6,000) |
|---|---|---:|---:|
| Control Paladin | face 0.3, enemy_minion 1.2, danger 10, draw 4.5 | **95.1%** | **59.0%** |
| Infernal Warlock | face 0.3, our_hp 8 | 86.8% | 58.4% |
| Counter Paladin | enemy_minion 1.2, danger 10, our_hp 8 | 93.9% | 56.7% |
| Steady Paladin | enemy_minion 1.2, danger 10, draw 1.5 | 94.9% | 54.1% |
| Aggro Paladin | hand_per_cost 0.25, taunt 2.5 | 91.7% | 45.9% |
| Pressure Hunter | face 1.0, enemy_minion 1.2, our_hp 3, draw 1.5 | 87.6% | 43.7% |
| Burst Shaman | face 0.3, enemy_minion 1.2, danger 2, our_hp 8 | 84.1% | 32.0% |

Astra's own pilots (`decks/<name>/scripts/move.py`), same seeds:

| Astra's pilot | vs greedy field | vs our planner on the same deck | best vs any of our 7 script decks |
|---|---:|---:|---:|
| Infernal Warlock | 78.1% | 47.5% | 70.6% (vs Burst Shaman) |
| Pressure Hunter | 77.6% | 37.8% | 45.0% |
| Burst Shaman | 66.5% | 32.9% | 32.9% |

Readings:
- **Infernal Warlock is a real contender.** It is second in the round robin and beats Counter (58.5), Steady (62.2) and
  Aggro (54.7), but it loses clearly to Control (32.4). Its lower score against the greedy field comes from Midrange Hunter (75.6) and
  Face Hunter (79.0): Life Tap and Hellfire cost it health against fast damage.
- **Burst Shaman is the weakest of the 7** under our planner. It loses every pairing, and Warlock beats it 84–16. Pressure Hunter is
  close to Aggro Paladin.
- **Our planner beats Astra's pilot on every deck**, by 2.5 (Warlock) to 17 (Shaman) points in the mirror with the same list.
  Burst decks rely on multi-card lethal turns, which a whole-turn search finds and a one-action scorer misses.
- With 7 decks, **Control overtakes Counter** in the round robin, because Control farms Burst Shaman (77.5) and Warlock (67.6).
  Counter still beats Control head to head (55.5).

## Added 2026-10-29: script-only self-play tuning, 6 rounds (`tools/selfplay.py`)

Method:
- No greedy bots. Each round, every deck retuned against all 7 script decks, a copy of itself included. The opponents
  were frozen at their start-of-round weights.
- Each of the 14 weights was tried at x0.67 and x1.5. A change was kept only if it gained more than 0.5 points.
- 200 games per opponent per trial, then a fresh-seed round robin with 1,000 games per pairing. Astra's three pilots
  joined the round robin, untuned.
- 0 forfeits or voids. Tables: `games/selfplay/round0.md` to `round6.md`. Weights: `games/selfplay/state.json`.

Win % against the 6 other script decks, each round on fresh seeds:

| Deck | R0 | R1 | R2 | R3 | R4 | R5 | R6 | Tuned vs own start weights, same deck (1,000) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Infernal Warlock | 58.7 | 57.6 | 54.0 | 54.7 | 56.6 | 55.0 | 56.7 | 47.9 |
| Control Paladin | 57.8 | 55.8 | 53.0 | 54.0 | 53.7 | 54.5 | 55.9 | **55.4** |
| Counter Paladin | 55.5 | 55.7 | 56.9 | 54.5 | 54.6 | 53.6 | 52.9 | 51.4 |
| Steady Paladin | 56.9 | 55.5 | 54.4 | 53.3 | 52.0 | 52.5 | 51.7 | 47.5 |
| Pressure Hunter | 44.5 | 44.9 | 47.9 | 49.6 | 46.9 | 48.2 | 48.9 | 49.4 |
| Aggro Paladin | 44.0 | 47.0 | 44.5 | 44.4 | 45.6 | 44.8 | 43.0 | 49.7 |
| Burst Shaman | 32.6 | 33.6 | 39.2 | 39.4 | 40.5 | 41.4 | 40.8 | **65.6** |

Readings:
- **Tuning has plateaued.** After round 2 the weights wander inside the noise, and the order hardly changes:
  Warlock and Control on top, then Counter and Steady, then Hunter, Aggro and Shaman.
- **Tuned vs untuned on the same deck:** only Burst Shaman (65.6%) and Control (55.4%) clearly gained. The other five are within
  ±3 points of 50%, so their earlier tuning was already good enough. The ~3-point drop in round-robin share for Steady and Counter
  reflects the others getting stronger, not Steady or Counter getting worse.
- **Our planner beats Astra's own pilot** on all three decks in every round.

## The Steady script player in detail

Deck: `decks/steady-paladin/deck.json` (unchanged 30 cards). What the planner knows, mapped to the playbook:

| Playbook lesson | How the script handles it |
|---|---|
| Mulligan for a curve (Squire/Worgen/Juggler/Hoarder/Ooze/Golem; Protector, Aldor, Cleric, Knight only with an early drop; Truesilver/Yeti going second) | `MULLIGAN["steady-paladin"]` |
| Blood Knight takes every shield (+3/+3 each), order vs shield-breaking attacks | modelled exactly; the turn search tries Knight before and after attacks and keeps the better board |
| Sea Giant costs 1 less per minion; play it before trades shrink the discount | cost recomputed after every simulated action |
| Cairne leaves Baine; Harvest Golem leaves a 2/1; Loot Hoarder draws | deathrattles in the board model |
| Tirion leaves Ashbringer, which replaces our weapon | modelled; the search spends Truesilver swings first when that scores better |
| Worgen Stealth protects until it attacks | keyword from card data; enemy Stealth minions are never targeted |
| Juggler before summons | each simulated summon pings; the search orders plays by outcome |
| Truesilver heals 2 before combat | modelled |
| Consecration value = the whole board after, not the kill count | scored by the end-of-turn evaluation |
| Survive first when their next turn is dangerous | graded danger term (weight 10 for Steady) + lethal-next-turn penalty |

Not modelled yet (all decks): enemy deathrattles and Secrets, opponent spells from hand beyond a flat "reach" of 3.
