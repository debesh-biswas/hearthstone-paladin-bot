# Alternative deck evaluation — 2026-10-28

## Question

Can a different resource plan improve our results against Control Paladin without sacrificing the Greedy Mage matchup? Candidates are original Zoo, Recovery Zoo and persistent-token Druid. Steady's recorded 3–5 result is not taken as proof of inferiority: one Control loss had an engine-verified immediate lethal that its pilot missed.

## Frozen experiment

The three research skills are in `research/alternative-skills/`, separate from existing tournament candidates. Original Zoo and Recovery Zoo have **identical playbook bodies**. Recovery changes exactly three slots: Nightblade → Shadowflame; Frostwolf Warlord → Mortal Coil; Argent Commander → Ironbeak Owl. Original Zoo's research playbook is concept-led and differs from its older Stage B playbook, so comparisons with that historical result are not isolated deck comparisons.

Druid uses the existing unmodified 30-card persistent-token draft, with a new concept-led playbook emphasizing persistent waves, actual Savage Roar lethal, correct Choose One options and resource limits. No silencing or other tech cards were added during the experiment.

All candidate decks passed the official deck validator; all skills passed the official loader. Three assertion-backed synthetic engine checks passed: buffed Flame Imp provides five-damage Shadowflame while an enemy shield absorbs its damage; Coil kills the surviving one-health body and replaces itself; Owl removes Tirion's Taunt, shield and deathrattle.

Model: **Haiku 5.5, medium effort**, choosing moves directly. Control Paladin also uses Haiku and its unchanged existing skill. Greedy Mage uses the built-in rule-based pilot. No script-player results are mixed into this experiment; the current `player/` project is untouched.

Planned allocation: each of three decks plays one game in each seat against Control Paladin and Greedy Mage, **12 games total**, using seed **280001**. This is a fresh seed relative to prior comparisons, but a single-seed screen, not a multi-seed confirmation. Actual `first_player` is taken from each result. There are three simultaneous games; each group completes before the next is launched. Detected quota/auth/network failures stop later groups and remain recorded.

This small sample tests whether the plans function and highlights pilot failures; it cannot establish reliable win rates or isolate the individual contribution of each substituted card. No course submissions are used.

## Artifacts

- Input hashes: `alternatives-input-hashes.json`.
- Match summaries: `alternatives-haiku-results.json`.
- Full game/decision records: `games/alternatives-haiku-20261028/`.
- Decision-time estimates use action-file modification time minus `(state.deadline_epoch_s - state.timeout_s)`. This is an approximate wall-clock end-to-end measure, including recording overhead, rather than an instrumented monotonic timer.

## Results

All 12 games completed by hero death using the planned models, seed and unchanged inputs. Seed 280001 selected **P1 as the first player**; each candidate therefore went first in two games and second in two. No infrastructure failures occurred.

| Candidate | Control Paladin, first / second | Greedy Mage, first / second | Total |
|---|---|---|---:|
| Original Zoo, shared research playbook | Win / Loss | Loss / Loss | **1–3** |
| Recovery Zoo | Loss / Loss | Loss / Win | **1–3** |
| Persistent-token Druid | Win / Loss | Loss / Loss | **1–3** |

**12 games, 3 candidate wins, 9 opponent wins, 0 draws, 0 forfeits and 0 timeouts.** There were **three illegal actions across all seats**: Recovery Zoo made two in its first Mage game (missing Sergeant target and unusable hero power); Control Paladin made one against Druid. Original Zoo and Druid made none. Recovery was one further illegal action away from a forfeit in that game; it recovered and completed instead.

Maximum approximate state-to-action latency: original Zoo **11.45 s**, Recovery **14.85 s**, Druid **22.07 s**. Across all model seats the maximum was also **22.07 s**, below the 180-second limit. These are the wall-clock estimates described above. Full metrics and selected card-play records: `alternatives-summary.json`.

## What the replays actually show

### Recovery Zoo: useful removal, no demonstrated improvement

Mortal Coil and Shadowflame were each played three times across the four games. In the first Control game, Coil killed a one-health Pyromancer. Shadowflame later sacrificed an 8/8 Giant to remove Guardian of Kings, Aldor and Alexstrasza. This was a meaningful board clear, yet the game was lost.

That Shadowflame also exposed a pilot error: the Giant was attack-ready, there were no Taunts/secrets preventing face damage, and the model sacrificed it without attacking. An offline replay branch confirmed that attacking face first dealt **eight additional damage**, then the same Shadowflame still cleared the same enemy board. Enemy health would be 18 instead of 26 at that point. This does **not** establish a winning full-game counterfactual. Evidence: `recovery-zoo-shadowflame-order.json`.

The second Control game also used Coil/Shadowflame but ended with an empty hand and a losing board. The removals did not guarantee a sustainable second wave. In contrast, the original Zoo's first Control win used Commander on turn 13 and Nightblade on turn 17, illustrating the type of pressure the replacement package gives up. That is an observed sequence, not a single-card causal experiment.

**Ironbeak Owl never reached the candidate's hand in any of the four games.** Its engine interaction passed, but its gameplay value is still untested. Do not describe all three new slots as model-validated.

### Druid: persistence functions, but the attack plan is fragile

In Druid's Control win, Force of Nature built successive boards, then two Taunt-form Druids of the Claw and Worgen supported a later attack. On turn 21 the model used Soul of the Forest, Roar and Power of the Wild. Control subsequently used Equality and a weapon attack to kill a Claw; Soul produced a replacement Treant. Druid then used the second Roar and attacked for lethal on turn 23.

The effect functioned, but **the second Roar was not necessary for that lethal**: the remaining ready minions already had ten attack against nine health. The final attacks did not require the Treant after Roar. This is evidence of board persistence and a completed win, not proof that Soul/Roar caused it or that every combo slot is justified.

In the other Control game, Druid ended with both Roars in hand and insufficient board pressure. Both Mage games were losses. Its risk is real: payoff cards lose value when the board is gone, while the list has limited unconditional refill. Teacher was played five times and Cult Master twice across the batch; those appearances do not by themselves prove the draw/summon package was used optimally.

### Tactical audit limit

A scan of all completed candidate decisions found no cases of choosing a minion trade/end-turn while the currently legal minion-to-face attacks alone already totaled lethal against a non-immune hero with no secrets. This scan does not cover spell/buff lethal, hero attacks, multi-step Taunt removal, positioning or all attack-order errors. It cannot certify optimal play; the Shadowflame example is one missed gain it would not detect.

## Decision

**Neither new draft earns promotion over the established decks from this screen.** Recovery does not demonstrate the Control improvement it was designed for; Druid shows a distinct functioning plan but no better overall result. Keep both in `research/alternative-skills/`, with their exact deck JSON and tested concept-led playbooks, rather than replacing an existing deck or changing the main `player/` pilot.

Original aggro Paladin remains the established benchmark from the prior broader Haiku comparison. Steady remains a legitimate candidate because one of its Control losses had a verified missed lethal. This batch does not prove either should be discarded.

Before spending a larger model budget, the next useful check is a **pilot-controlled comparison**: fixed original Zoo cards, existing versus shared research playbook, across fresh seat-balanced seeds. The new baseline's poor Mage result may reflect seed variation, playbook behavior or both; it cannot be attributed to one without that test. Only then compare targeted changes separately (e.g. one Shadowflame rather than all three substitutions) or test Druid's refill/payoff balance.

All inputs matched their recorded hashes at completion. No deck/skill was edited during the batch. No additional matches or commits were launched after these 12 games. Results are a one-seed screening sample, not reliable deck win-rate estimates.
