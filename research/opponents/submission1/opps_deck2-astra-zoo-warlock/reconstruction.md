# Astra — Zoo Warlock

**Status: legal 30-card hypothesis, not an exact recovered deck.**

Reconstructed from submission 1 returned observations in `hw2-submission-1-control-paladin-results.zip`. Four games, all WARLOCK.
Public evidence confirms at least **29 slots** under a constant-list assumption; **1 slots are inferred**.

Use `deck.json` for local opponent testing. `evidence.json` records per-game counts and observation seq/entity evidence. This folder is a deck recipe, not a model skill.

| Card | Mana | G1 | G2 | G3 | G4 | Observed minimum | Reconstructed | Inferred |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Abusive Sergeant | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 0 |
| Argent Squire | 1 | 2 | 1 | 2 | 1 | 2 | 2 | 0 |
| Flame Imp | 1 | 2 | 1 | 1 | 2 | 2 | 2 | 0 |
| Leper Gnome | 1 | 1 | 0 | 1 | 0 | 1 | 2 | 1 |
| Mortal Coil | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| Soulfire | 1 | 2 | 1 | 1 | 1 | 2 | 2 | 0 |
| Voidwalker | 1 | 2 | 2 | 1 | 0 | 2 | 2 | 0 |
| Amani Berserker | 2 | 2 | 1 | 2 | 0 | 2 | 2 | 0 |
| Dire Wolf Alpha | 2 | 2 | 1 | 0 | 1 | 2 | 2 | 0 |
| Knife Juggler | 2 | 2 | 1 | 1 | 1 | 2 | 2 | 0 |
| Loot Hoarder | 2 | 1 | 2 | 1 | 1 | 2 | 2 | 0 |
| Harvest Golem | 3 | 2 | 2 | 2 | 0 | 2 | 2 | 0 |
| Imp Master | 3 | 1 | 0 | 1 | 0 | 1 | 1 | 0 |
| Shattered Sun Cleric | 3 | 2 | 2 | 1 | 0 | 2 | 2 | 0 |
| Dark Iron Dwarf | 4 | 2 | 2 | 0 | 1 | 2 | 2 | 0 |
| Defender of Argus | 4 | 2 | 1 | 2 | 0 | 2 | 2 | 0 |

Counts are distinct played cards, not repeated board sightings. Revealed Explosive Traps are included. The Coin, Hounds, Animal Companions, Damaged Golems and Imp tokens are excluded. Final graveyard/board counts independently match the identified starting cards in every game.

A maximum of one observed copy does **not** prove the card is a singleton. Maxima are taken across games, never summed across games. The unseen deck and opponent hand are absent from the archive.

## Reconstruction choice

Sixteen distinct card names were observed: thirteen confirmed pairs and one observed copy each of Leper Gnome, Mortal Coil and Imp Master. This fixes 29 slots if the list stayed constant. The thirtieth card is unknown.

The playable hypothesis uses a second Leper Gnome to support the aggressive curve and deathrattle reach. A second Mortal Coil, a second Imp Master, or an entirely unseen legal card also fits. No replay evidence establishes that Leper Gnome is more likely than those alternatives.

In game 1, 28 original cards were revealed, with no cards in hand and two left in the deck. Game 2 confirms the second Loot Hoarder, leaving exactly one unresolved slot across the combined evidence. Soulfire discards and unobserved cards are not assigned invented identities.

## Playing pattern and matchup

This is low-curve Zoo, not our Infernal Warlock or the earlier local Steady Paladin experiment. Flame Imp and cheap bodies contest the board; Abusive Sergeant, Dire Wolf, Cleric and Dark Iron Dwarf turn small minions into trades or damage. Argus protects a wide board, Harvest Golem/Imp Master supply bodies, and Life Tap/Loot Hoarder sustain pressure. Soulfire adds reach.

Our Control Paladin split 2–2. The fourth game ended on turn 11 after Dark Iron Dwarf buffed Flame Imp and Soulfire targeted our hero. Unlike Bot 2, this list can refill rather than simply exhausting its opening hand. The near-complete evidence leaves no space for a large hidden late-game package under a constant-list assumption.
