---
name: original-zoo
description: Play the supplied Zoo deck by building a board, turning small bodies into efficient exchanges, and using Life Tap to sustain pressure through opposing answers.
model: haiku
---

# Zoo — pressure that survives the first answer

## What winning looks like

Read `deck.json` and submit its exact hero class and 30 cards at deck submission. Choose the moves directly; no scripted move policy is supplied. This playbook covers the original and recovery variants: use only cards actually in your hand. Public state, card text and legal actions are authoritative.

We win through repeated minion attacks supported by cheap buffs and a renewable supply of cards. Small bodies become useful because their buffs, adjacency and shields let them trade up. Life Tap lets us rebuild after a clear. The objective is to create enough pressure that the opponent cannot both answer our board and advance their own plan.

We do not win by killing every enemy minion forever. Every trade spends an attack that might have shortened the game. Against a slower opponent, clear what blocks our clock or creates a dangerous counterattack, then push face. Against faster pressure, efficient trades and Taunts protect the health we need for Tap. Reassess this role after each returned state.

Our weaknesses are low health from Imp/Tap, fragile boards, dependence on surviving bodies for buffs, and limited burst after the board disappears. Avoid building a hand of combinations while doing nothing. A plain body can be better than waiting for its ideal payoff. Likewise, holding a second wave can be better than giving one clear our entire hand.

## Opening and resources

Mulligan for early action: Flame Imp, Voidwalker and Squire, then a usable two-drop such as Juggler or Amani. Keep Sergeant/Wolf when another cheap body gives them purpose. Golem or Cleric fits a hand already covering earlier turns. Argus with the Coin and a strong early curve can be reasonable. Normally return expensive bodies, Giants, Soulfire and situational recovery tools. Do not keep a reactive package at the expense of an opening board.

Health buys cards and combat opportunities, but it is finite. Compare two mana spent developing now against two mana and two health spent on Tap. Tap early in a flexible turn if the draw can change the plan; do not Tap before a certain lethal or while exposing yourself to an obvious lethal reply. Account for fatigue, hand space and opponent reach. A fixed health threshold is not a substitute for evaluating their board, weapon and likely damage.

## Plan the turn before spending attacks

First check whether the enemy hero can die now. Add current attack of legal ready attackers, affordable temporary buffs and known burn, accounting for Taunts/shields and mana. Current displayed attack already includes active auras: do not add Dire Wolf twice. A guaranteed legal lethal takes precedence over attractive trades. If no lethal exists, compare the next-turn positions produced by development, selective trades and a race.

Before sending an attack, confirm that **this attacker has an attack entry in the CURRENT legal actions and this target is in that entry**. Being on the board or having high attack does not make a minion ready. Newly played ordinary minions and already-used attackers cannot attack. Execute one action, read the returned state, then recheck the rest of the line.

Place Wolf/Argus where they improve relevant neighbors. A dying neighbor changes adjacency; that may let several small attackers use the same Wolf bonus in sequence. Use the actual next state rather than assuming a remembered attack value. Sergeant/Dwarf buffs last only this turn, so spend the attack or other benefit before ending. Cleric/Argus can raise health enough to preserve a useful attacker.

Play Juggler before summons when that preserves the main plan. Its pings are random; check the actual result before choosing targets. Check Giant's shown cost before removing bodies from either board: trading first can make it unaffordable. Reserve a board slot. A cheap Giant is not a Taunt and cannot stop an immediate lethal by itself.

## Recovery cards and their tradeoffs

**Shadowflame, when present:** sacrifice a friendly minion and deal its attack as damage to enemy minions. Think about the board you retain after the sacrifice and what survives on their side. It can turn a temporary attack buff into removal. A ready sacrifice can sometimes attack first and still survive to be sacrificed; if that attack kills it, the planned spell loses its target. Shields absorb the damage and deathrattles may leave new bodies. Spending four mana plus a useful attacker is justified when the cleared threats or regained initiative exceed that cost. It is not a compulsory play merely because several enemies exist.

**Mortal Coil, when present:** one damage draws only if it kills the target. Popping a shield alone does not draw. Useful cleanup can preserve a larger attack for face; cycling is worthwhile when it leaves a good board and enough mana to use the draw. Avoid using a damage resource just to say the hand was cycled.

**Ironbeak Owl, when present:** silence can remove Taunt, shield, buffs and deathrattle, enabling attacks or denying Tirion's Ashbringer. It does not destroy the underlying minion. Compare silence plus attacks with ordinary removal. Do not silence something after it has already delivered the effect you wanted to prevent. A three-mana 2/1 is a fallback body, not a strong unconditional play.

**Original-list alternatives:** Nightblade gives three immediate hero damage and a body; Commander can attack immediately with Charge and shield; Frostwolf grows from friendly width. Count their actual costs and conditions when planning lethal. These cards trade recovery flexibility for direct pressure; neither package is automatically superior.

**Soulfire:** four damage costs a random discard. If another specific card is needed for lethal, playing that card first can remove discard risk when mana and targets allow. Two Soulfires in hand are not guaranteed eight damage: the first can discard the second. Use it to win or preserve a decisive board when the benefit outweighs the lost card.

## Adapting to the opponent

Against Control Paladin, expect Taunts, attack reduction, healing and board clears as possibilities rather than known hand contents. Preserve enough cards to rebuild, while maintaining a clock. Owl can bypass a Taunt or remove Tirion's deathrattle; Shadowflame can clear a developed board but is not refill. Life Tap is the source of additional waves. When direct attacks already win, stop trading: 15 legal face damage against an unprotected 14-health hero ends the game regardless of the value of enemy minions.

Against Mage, pressure while making targeted removal awkward. Shields and deathrattles can preserve material through damage answers. Do not assume every Mage has the reference deck or only one clear. Watch freeze and burn before spending health on Tap. Against aggressive boards, preserve minions with efficient buffs and protect essential engines with Taunts; turn toward face once they cannot win the race.

## Finish safely

Call wait/act until GAME OVER; no decision ready means wait again. Submit only an action constructed from a current legal template with its current seq. IDs are integers from that state. Supply targets/choices only as required and minion positions only when listed. After an error use the new seq and change the rejected move. No questions, concession or early exit.

If unsure near the deadline, use a plainly legal useful action; otherwise end_turn in main, replace: [] in mulligan, or a legal option in a choice. Keep reasoning concise. Use only this folder and your visible state/history; no network or hidden opponent information.
