# Haiku deck evaluation — 2026-10-27

## Question and protocol

Does direct play by the course's small model preserve the practical promise of the Paladin candidates, and does it use Blood Knight and the other conditional cards sensibly?

Three frozen decks: original aggro Paladin (`baseline-paladin`), Steady Paladin, Counter Paladin. Each has an isolated research skill in `research/haiku-skills/`. All three have identical playbook bodies; only the name and deck data differ. Instructions cover all three lists, with explicit tradeoffs for Blood Knight, Corsair, Sea Giant, Cult Master and Wisdom. No move script is supplied: the model chooses actions directly.

Model: **`claude-haiku-5-5`, medium effort**, launched by unmodified hs-arena 0.2.2. This is the runtime's `model: haiku` mapping. Defaults retained: 180 seconds per decision, third illegal action forfeits, early exit forfeits.

Each deck plays one game in each seat orientation against (a) built-in Greedy Mage and (b) the baseline Paladin controlled by Haiku with the same playbook. Seed 172711 in every pairing/orientation. Total planned sample: 12 games, 18 model seats. Three games run concurrently. These are local tests using the existing login, not course submissions.

The baseline/Haiku-Paladin games are mirror controls. Identical seeds balance some draw/seat variation, but model sampling can differ, so results are not perfectly deterministic pairs. Two games per matchup cannot estimate a reliable win rate. The purpose is a pilot-compatibility smoke test and replay inspection, not statistical ranking or single-card causal attribution.

## Launch failure excluded from deck-strength evidence

An initial sandboxed attempt at Steady versus Greedy Mage failed because Claude Code could not access the existing login: `Not logged in`. It ended at turn zero with `forfeit_exit`, zero illegal actions and zero timeouts. Read-only authentication checks showed that the existing login worked outside the sandbox. The authenticated batch uses a separate output directory, preserving this failure rather than silently overwriting it.

Failure record: `games/haiku-deck-research/steady-paladin__greedy-mage__seat1/g_20261027_000001/result.json`. This is a real local infrastructure forfeit, not a played deck loss and not part of the planned 12-game authenticated sample.

## Artifacts and measurement

- Authenticated games and full replays: `games/haiku-deck-research-authenticated/`.
- Research skill files: `research/haiku-skills/`; existing tournament skills remain unchanged.
- Deck and skill loaders pass; playbook bodies are asserted identical.
- Per-seat `seat.json` records actual model ID, effort and reported usage.
- Decision snapshots and action records permit inspection of public board state and chosen cards. Analyze completed local games only; do not feed hidden replay information into a live player.
- Estimated observed decision latency can be computed from action-file modification time minus `(state.deadline_epoch_s - state.timeout_s)`. This includes publication/recording overhead and uses wall-clock timestamps; it is an approximate end-to-end measure, not an instrumented monotonic timer.

## Haiku results and usage-limit interruption

All 12 scheduled authenticated games produced result files, but only **five ended normally**. Seven ended with `forfeit_exit` after Claude Code reported HTTP 429: session usage limit reached, reset reported as 4am America/New_York. Some failed immediately; Steady's second Mage game was interrupted at turn 22. These are censored/infrastructure outcomes, not deck-strength losses or wins, including any apparent win when the opposing seat exited.

| Deck | Opponent pilot/deck | Normally completed | Wins–losses |
|---|---|---:|---:|
| Original Paladin | Greedy Mage | 2 | 1–1 |
| Original Paladin | Haiku original Paladin | 2 | 1–1 |
| Steady Paladin | Greedy Mage | 1 | 1–0 |
| Counter Paladin | Either opponent | 0 | Not evaluated |

Authenticated batch: **0 illegal actions, 0 timeouts, 7 exit forfeits**. Separately, the initial sandbox/login attempt adds **one more infrastructure exit forfeit**. All recorded model seats identify `claude-haiku-5-5`, medium effort. Across 335 recorded model actions, maximum estimated observed decision latency was **19.47 seconds**, using the wall-clock method above. Reported aggregate list-price usage cost was **$0.500745**; this is the harness's usage estimate, not a statement about subscription billing.

Machine-readable records: `haiku-results.json` and `haiku-summary.json`. The quota failures are preserved and excluded from the normal-game win/loss table. Already queued jobs finished with quota errors; no quota-failed game was retried.

### Card observations

- **Sea Giant:** in Steady's completed win against Greedy Mage, P1 decision 16 / turn 11, Haiku played it for five mana with three friendly and two enemy minions present. The next state confirms an 8/8 on our board. This demonstrates successful use of its live discount, not proof it caused the win.
- **Cairne:** in the later quota-interrupted Steady/Mage game, P2 decision 34 / turn 18, Haiku developed Cairne onto an empty friendly board against a Water Elemental. This is a valid late-body deployment, not evidence about that game's outcome.
- **Blood Knight never appeared in Haiku's hand** in the recorded Steady games. The batch supplies no model-play evidence for it. Counter's intended Corsair/Cult Master/Wisdom tests were also blocked by quota.

### Separate Luna follow-up

The course also permits `gpt-6-luna`, medium effort. Because the existing Codex login remained available, a separately labelled four-game follow-up tests Steady and Counter, each in both seats against **rule-based original Paladin**, seed 271027. These use copied playbooks in `research/luna-skills/` with only `model: luna` changed. No Luna result is pooled into the Haiku comparison, and this follow-up does not substitute for the unfinished Haiku-versus-Haiku matches.

## What the evidence can answer

The rule-based tournament is useful for broad, cheap screening under a fixed policy. It cannot establish each deck's potential or the value of sequencing-sensitive cards. Direct model games test pilot compatibility and reveal actual decisions, but tiny samples also cannot rank decks reliably. For final selection, use both plus package ablations and adequate seat-balanced games with the eventual pilot. This Haiku batch is incomplete because of quota, so the earlier deck recommendation remains provisional.

## Completed Luna follow-up

All four games completed normally using **gpt-6-luna, medium effort** against the unchanged greedy-controlled aggro Paladin. **Steady won 2/2; Counter won 1/2.** Zero forfeits, illegal actions or timeouts. Across 200 recorded model actions, maximum estimated observed decision latency was **8.67 seconds**. Full records and selected board observations are in `luna-results.json`.

### Blood Knight: both a payoff and a pilot failure

**Successful activation:** Counter as P2, decision 26 / turn 16: Luna played Blood Knight while its own Sea Giant and the enemy Argent Commander had Divine Shield. The next snapshot confirms both shields removed and a **9/9 Blood Knight**. It remained alive as a 9/1 at turn 20 and attacked the enemy hero. Counter won this game. This demonstrates the interaction occurred in a real model-piloted game; it does not prove consuming the Giant's shield was optimal or that Knight caused the win.

**Missed activation:** Counter as P1, decision 34 / turn 17: Luna had nine mana, Blood Knight in hand, no friendly shields, and an enemy 6/6 shielded Tirion. Blood Knight was a legal play. Instead it attacked Tirion with an unshielded 4/2 Argent Commander, losing the Commander to remove the shield, then traded a 1/1 recruit into Tirion. It subsequently played Ooze and a **3/3 Blood Knight**.

Playing Knight before those same attacks would remove the enemy shield and create a **6/6**; the two attacks would leave Tirion at one health rather than five. The observed line therefore missed concrete stats and damage at the same mana cost. This is a sequencing failure, not evidence that Blood Knight is weak. It happened despite explicit playbook guidance. No claim is made that the alternative guarantees winning the game.

The seat-visible state and observed action are saved in `fixtures/blood-knight-before-tirion-trade.state.json` and `fixtures/blood-knight-before-tirion-trade.observed-action.json`. Assertions confirmed nine mana, the legal Knight play, zero friendly shields and one shielded enemy Tirion. This is a useful regression case for the future pilot; it contains only that seat's legitimate visible state.

**Fallback deployment:** Steady as P1, decision 17 / turn 9: Luna played Knight as a 3/3 against an empty enemy board. This shows it did not always wait for the combination; it does not establish that the timing was optimal.

### Other cards

- Counter P2, decision 23 / turn 14: Sea Giant was played for seven mana. This is discount usage, not a dramatic free-Giant turn.
- Counter P2, decisions 35–37 / turn 20: Wisdom was cast on an attack-ready Tirion, then Tirion attacked. Hand size went from three before casting to two after casting to three after attacking, confirming immediate replacement draw.
- Steady P2, decision 21 / turn 14: Cairne was deployed against a developed enemy board; this alone does not quantify its value.
- **No Dread Corsair or Cult Master plays were captured** in these four Luna games. Those packages remain untested at the model-decision level.

## Final accounting and research decision

Across this session's attempts: **17 local games launched** = one sandbox/login failure, 12 authenticated Haiku games, four Luna games. **Nine normal completions**, eight infrastructure exit forfeits (one login, seven Haiku quota), **zero illegal actions and zero timeouts**. Do not pool Haiku and Luna wins, or count quota outcomes as deck strength. This is not a clean 17-game competitive benchmark.

The model tests strengthen the reason to keep Blood Knight under investigation: there is a real 9/9 payoff and a reproducible missed opportunity. They also show that written card guidance alone does not guarantee correct small-model sequencing. Retain Steady as a provisional candidate; do not declare a final winner, remove Counter on a 1/2 result, or claim the whole conditional package is validated. The unfinished Haiku matchup comparison requires available quota; it was not retried or silently replaced by Luna results.
