# Online run 1: Bot 2 and Astra deck reconstruction

## Conclusion

**They did not play the same deck.** Bot 2 played Hunter in all four games; Astra played Warlock in all four. Their revealed cards identify Face Hunter and low-curve Zoo Warlock respectively. Each opponent's four games are compatible with one fixed list, but the hidden slots prevent proving that its exact list never changed.

These are the actual hosted opponents. Earlier local experiments named Astra/Steady Paladin are not evidence about the hosted Astra deck.

| Opponent | Our result | Final game turns | Confirmed slot minimum across games | Inferred slots in playable reconstruction |
|---|---|---|---:|---:|
| Bot 2: Face Hunter | 4–0 | 21, 22, 17, 18 | 21 | 9 |
| Astra: Zoo Warlock | 2–2 | 29, 21, 21, 11 | 29 | 1 |

Turn numbers are the engine's alternating-player turn counter, not rounds. All eight games ended by hero death. Our reported forfeits, illegal actions and timeouts are all zero; decision latency is not recoverable from this archive's untimestamped observations. Overall run: 12–2 across 14 games, 10 base + 2 bonus points, excluding ladder/late adjustments.

## Saved decks

- [opps_deck1-bot2-face-hunter](opps_deck1-bot2-face-hunter/reconstruction.md): 30-card hypothesis comprising two copies of each of the 15 observed names. Nine second copies are inferred. Every chosen card name was actually revealed.
- [opps_deck2-astra-zoo-warlock](opps_deck2-astra-zoo-warlock/reconstruction.md): 29 evidenced slots plus one explicitly inferred second Leper Gnome. A second Coil, second Imp Master or unseen legal card also fits.

Each folder includes standard `deck.json`, a card-by-card confidence table in `reconstruction.md`, and machine-readable `evidence.json` with game, observation sequence and played entity IDs. Both deck JSON files pass the official static validator. No gameplay was launched.

## How the evidence was counted

Read only `results.md` and the player-visible observations in `games.json` from the run 1 results archive. For each game, select events belonging to the opponent using `3 - student_seat`. Deduplicate played cards by entity ID; repeated board sightings are not extra copies. Include publicly revealed secrets, whose original play identities were hidden.

Exclude The Coin and generated tokens: Companions, Hounds, Damaged Golems and Imps. In all eight games, the final visible graveyard plus surviving board independently matches the counted collectible cards. No observed bounce/copy/resurrection package complicates those counts. Take the maximum confirmed count for each card across games, not the sum. The conclusion that these counts form one starting list is conditional on a stable deck.

Bot 2 never revealed more than 14 original cards in a game. Astra game 1 revealed 28 originals and ended with two cards still in its deck and an empty hand. Game 2 supplied evidence of the second Loot Hoarder. That explains why Astra's list is much more tightly constrained.

## Strategic difference

Bot 2 combines cheap attackers, Charge, Bow, burn and Steady Shot. It emptied its hand in all four games while 16–18 cards remained in its deck. Healing and repeated board stabilization can therefore exhaust its immediate resources. The recorded pilot sometimes spent burn on minions; this 4–0 result is evidence about the observed deck/pilot combination, not all possible Face Hunter play.

Astra combines cheap bodies with many attack buffs, persistent summons and Life Tap. It can rebuild after a clear and convert surviving minions into substantial damage. In the fourth game, the finish included Dark Iron Dwarf on Flame Imp and Soulfire to our hero. In the longest game, it played 28 original cards. Its sustained resource access distinguishes it from Bot 2 even though both use an aggressive curve.

Only four distinct revealed card names overlap: Abusive Sergeant, Argent Squire, Leper Gnome and Knife Juggler. Timber Wolf in Hunter and Dire Wolf Alpha in Warlock are different cards. These opponents are not two pilots using one shared aggro list.

No hidden cards have been recovered exactly or guessed silently. The generated lists are useful local opponent hypotheses, with their uncertainty retained alongside the deck files.

Reproduce the extraction with `python research/opponents/run1/reconstruct_run1_opponents.py` from the repository environment. This parses the archive and writes analysis artifacts; it does not run the engine, matches or a model. Source SHA-256 is recorded in `evidence.json`.
