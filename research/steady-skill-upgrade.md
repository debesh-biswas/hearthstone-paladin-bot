# Steady Paladin skill upgrade — 2026-10-27

Saved as `decks/steady-paladin/`: `SKILL.md`, `deck.json`, and `references/guide.md`. The 30-card research list is unchanged, including one Blood Knight. Existing baseline and research playbooks were not overwritten. This folder is now discoverable by the tournament's normal `decks/` scan.

The new main skill explains the deck's resource advantage, weaknesses, role changes, contextual mulligan, whole-turn planning, card packages, and conversion of board advantage into lethal pressure. The companion guide adds the exact deck map, resource tradeoffs, worked decisions and all nine class matchups. Instructions explain why an action helps win instead of specifying a fixed action priority. The legal-action and session-completion safeguards remain. No move script was added.

Default local model: `luna` (`gpt-6-luna`, medium), because Haiku reached its usage cap during earlier research. Final submission model and final deck remain undecided.

## Validation

- Course `hs-arena validate --no-game`: passed.
- Deck validator: passed; JSON exactly equals the original research candidate.
- Guide card names/quantities match the local catalog and all 30 deck slots.
- No reserved `game/` or `scratch/` inside the skill.
- The general skill-creator Python validator could not run because its interpreter lacks PyYAML. No dependency was installed; the course-specific validator is authoritative for this runtime and passed, including its real-game smoke test.
- Isolated Luna snapshot check: selected `{"seq":34,"action":{"type":"play_card","card":22,"position":1}}`, a legal Blood Knight play before the damaging Tirion trade. Checked against the snapshot's legal template. Saved response: `steady-skill-snapshot-result.json`. The example is explicitly taught in the new skill; passing this check is a targeted regression result, not evidence of generalization.

## Full games with the exact saved files

| Test | Seed | Result | Illegal | Timeouts | Forfeits |
|---|---:|---|---:|---:|---:|
| Official validator smoke versus random | 1 | Win | 0 | 0 | 0 |
| Luna Steady P1 versus greedy original Paladin P2 | 271027 | Loss | 1 | 0 | 0 |
| Greedy original Paladin P1 versus Luna Steady P2 | 271027 | Win | 1 | 0 | 0 |

**3 games, 2 wins, 2 illegal actions, 0 timeouts, 0 forfeits.** Maximum observed decision latency approximately **35.17 seconds**, measured from action-file modification time minus `(state.deadline_epoch_s - state.timeout_s)`; wall-clock estimate including recording overhead, not an instrumented monotonic timer.

Both rejected actions were `CANNOT_ATTACK`: the model attempted to attack with a minion that could not attack in the current state. It recovered using the next decision and finished each game. The conceptual playbook does not guarantee legal-action adherence; these observations remain a pilot reliability concern rather than a claim that the deck is submission-ready. No claim of improved win rate is justified by these three games.

Results and exact tested file hashes: `steady-skill-validation.json`. Full replays: `games/steady-skill-upgrade/`. No course submission, commit, or further test batch was launched.
