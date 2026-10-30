# Alternatives after the eight-game Steady comparison

## What changed

The new all-Haiku comparison is more relevant to direct model play than the earlier large greedy-pilot screen. Steady finished 3–5, including 0–2 against Control Paladin. These are small, same-seed matchup samples, not a stable ranking. The larger Stage B sample currently favors the original aggro Paladin (14/18 wins overall; five of six versus Greedy Mage), so it should remain the benchmark rather than being displaced on the strength of the earlier greedy screen.

Replay review found a decisive pilot error: Steady had 15 ready damage against Control's unprotected 14-health hero on turn 19, then traded instead of winning. The exact position was reproduced by replaying 68 accepted actions in the offline engine; four legal face attacks won immediately. This is an exact tactical counterfactual, not a prediction about an alternative full game. No live game's hidden information was accessed or provided to a player.

The other Control loss still provides a useful construction question: how do we maintain pressure through attack reduction, repeated Taunts, healing and board clears? Adding one bigger minion is not necessarily the answer. The alternatives should change resource generation, recovery, or the way damage is delivered, rather than simply rename a Paladin list.

## Priority 1: Recovery Zoo

Candidate: `research/decks/recovery-zoo.json`, copied from the current Zoo with exactly three substitutions. **30 cards, correct class/copy limits, official deck validation passed; no games played with this variant.** It is deck data, not a new shipped skill.

| Remove | Add | Hypothesis | Cost/risk |
|---|---|---|---|
| Nightblade | Shadowflame | Convert an expendable/buffed attacker into an enemy-board clear, helping recover against developed boards | Needs a friendly sacrifice; damage does not bypass shields; loses guaranteed face damage |
| Frostwolf Warlord | Mortal Coil | Clean up a one-health minion and replace the card, instead of adding another payoff that requires an existing board | No draw if it fails to kill; cannot solve a healthy large threat |
| Argent Commander | Ironbeak Owl | Remove Taunt, shield or a crucial deathrattle to enable attacks or deny Tirion's weapon | Three-mana 2/1 is weak without a target; loses immediate Charge reach; silence alone does not kill the minion |

Keep the existing cheap minions, buffs, two Giants and Life Tap. The distinctive advantage is refill without needing a special draw card in hand. Tap is not free: two mana and two health can lose a race. Shadowflame can sacrifice a minion after it attacks when still alive; attack buffs can raise its damage, but do not assume a multi-card combination is always available. Saving some hand resources for a second wave may matter more than one spectacular clear.

Why prioritize it: the existing Zoo went 3/4 against Control Paladin in Stage B, though that is far too small for a reliable matchup estimate. It supplies a plausible contrasting resource plan and already has a working playbook. The original Zoo must remain a control when testing these changes; the new variant is not presumed better.

## Priority 2: Persistent-token Druid

Existing legal research list: `research/decks/persistent-token-druid.json`. Its premise is to generate multiple bodies, protect a wave with Soul of the Forest, then convert surviving attackers into burst through Savage Roar. It has no Wild Growth ramp package. Teacher plus Power of the Wild's timing has been engine-checked; the full list remains unplayed.

Why it addresses the question: a damage clear can leave Treants, and Roar can convert a modest surviving board into a faster clock than a sequence of plain midrange attacks. Soul is not immunity to all removal: follow-up clears, silence, board-space limits and effects on individual minions still matter. Force of Nature's new Treants do **not** have Charge. Taunts still block Roar attacks.

Specific experiment to consider later: a single Owl in place of the one Defender of Argus if Taunt walls are the recurring obstacle. Do not silently make that substitution alongside other changes; compare the fixed draft first or clearly label an ablation. This archetype is more sequencing-sensitive and can still fail from weak refill or an empty board. The missed-lethal example makes a reliable burst calculation particularly important.

## Lower priority: Board-theft Priest

Existing legal research list: `research/decks/board-theft-priest.json`, still unplayed. Shadow Madness and Cabal can turn small opposing bodies into resources; Mass Dispel can dismantle shields, Taunts, buffs and deathrattles before trades. That is interesting against some of this field.

However, Priest's lack of reliable draw and face reach may simply reproduce the problem of losing a longer resource game to Control Paladin. Chaplain/Circle/Pyromancer packages also demand careful sequencing. Keep it as a genuine alternative hypothesis, not the first response to these two Control losses.

## What to test next, without conflating the questions

1. Keep original aggro Paladin, original Zoo and Steady fixed as benchmarks. Separate decks from pilots; use the same selected model and effort across candidate/control matches.
2. Compare Recovery Zoo with original Zoo against Control, aggro Paladin and Greedy Mage. Use multiple seeds and both seat orientations; report actual `first_player` rather than assuming P1 starts.
3. Review whether Shadowflame/Owl actually get drawn and used, whether clears create a second attack wave, and whether replacing damage cards loses close races. Win rate alone does not isolate the substitutions.
4. Test token Druid with explicit attention to board persistence and lethal calculation. Do not infer its strength from a generic greedy bot's inability to plan Roar.
5. Preserve infrastructure failures separately; never silently convert them into normal deck losses or discard them without an audit trail.

This pass performed replay analysis, one deterministic replay branch and legality checks only. **No new model matches or tournament were launched.** None of these alternatives has been selected as the final submission.
