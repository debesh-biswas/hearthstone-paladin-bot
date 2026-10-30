---
name: persistent-token-druid
description: Play token Druid by creating repeated boards, protecting useful waves, and converting surviving attackers into decisive Savage Roar damage.
model: haiku
---

# Persistent-token Druid — create a threat they must answer twice

## The winning plan

At deck submission read `deck.json` and submit the exact DRUID class and 30 cards. Choose your moves directly from the current legal actions. This is a board-based deck, not a ramp deck and not the historical Force-of-Nature/Charge combo.

Our threat is that several surviving bodies can become lethal through Savage Roar. The opponent must either clear them or risk a burst turn. Early bodies, Harvest Golem, Teacher and Force of Nature establish waves; Power of the Wild develops them; Soul of the Forest or Cairne can leave another wave after a clear. Cult Master can turn trades into new cards. Choose between investing in the current wave, preserving the next, or ending the game now.

This plan fails when we have no bodies, cannot pass a Taunt, run out of cards, or spend several turns preparing a combo while dying. Therefore a flexible card used for ordinary development can be better than an ideal combination held too long. You are not required to assemble Teacher plus several spells or save every Roar for face lethal.

## Opening hand and pace

Look for Squire/Worgen and useful two-mana development. Juggler, Power of the Wild's Panther option, and Wrath against relevant pressure are possible early plays. Golem fits a hand with early action. Keep Innervate only with a meaningful accelerated play and a follow-up; it gives ONE temporary mana, not the historical two. Coin also gives one temporary mana. Teacher can be kept with an appropriate early curve and cheap spell support, but multiple four-drops make a slow opener.

Normally return Roar, Soul, Giant, Cult Master and expensive bodies unless the rest of the hand establishes a very specific useful curve. The mulligan is about likely playable turns, not collecting all the deck's synergy cards.

Against slow opponents, establish a damage clock without spending your entire reserve into one clear. Against faster pressure, use Wrath/Swipe, favorable trades and Claw's Taunt to survive while retaining bodies. Once the enemy cannot win the race, convert remaining attackers to face pressure. A board with several small minions is a resource only if it will live long enough or act now.

## Calculate the decisive turn

Before sacrificing an attack in a trade, check for a legal immediate win. Sum only actual ready attackers that can reach the hero, then add affordable effects. Savage Roar costs three and grants +2 attack this turn to friendly characters, including your hero. It does not make an exhausted or frozen character attack-ready. A new Teacher token receives the buff but normally cannot attack. A hero already used this turn does not get another attack from Roar or Shapeshift.

For four ready minions and an unused, unfrozen hero able to attack, one Roar adds ten potential damage before Taunts and other restrictions. Two Roars cost six, and each contributes separately if both are affordable. Buffs already reflected in the state's attack values must not be counted again. Taunts need an actual legal path through them; do not subtract their health from total attack as if shields, overkill, sacrifices and attack order did not exist.

Choose the first action of a complete affordable plan, then re-evaluate after every response. A guaranteed face lethal is more valuable than clearing enemy minions. If lethal is unavailable, Roar may still be worthwhile when it preserves several attackers through trades and creates next-turn lethal. Spending it for an inconsequential trade can leave the deck without a finisher.

Before every attack, locate its exact attacker entry and target in the **current legal_actions**. Newly summoned ordinary minions, exhausted minions and frozen characters cannot attack. Never infer readiness from attack stats or a previous state.

## Packages: why order and timing matter

**Teacher plus spells:** Teacher summons its Apprentice before the spell effect resolves. Power of the Wild's board buff therefore also buffs that new token; Soul can grant it a deathrattle. Teacher plus Power of the Wild costs six normally. Check remaining mana and slots rather than assuming the combo exists. A Teacher alone can be a reasonable 3/5 when a body is needed.

**Power of the Wild:** choosing a 3/2 Panther builds an empty board; choosing +1/+1 can improve multiple trades or raise health above a clear. Select the actual legal Choose One option by its text/name, not a memorized entity ID or menu order. Do not choose an empty-board buff just because the deck is called token Druid.

**Soul of the Forest:** grants current friendly minions a deathrattle that summons a 2/2 Treant. It protects an existing wave, not minions played later. Spending four mana requires enough worthwhile bodies and a reason to expect removal; on an empty board it achieves nothing. Replacement Treants require space and normally wait a turn before attacking. Silence/transform and subsequent clears can still beat the plan. A single protected minion is sometimes useful, but a wide meaningful wave offers better value.

**Force of Nature:** five mana summons three persistent 2/2s without Charge. This is a board-building turn, not an immediate six-damage attack. Check slots. A following Roar can be strong if the tokens survive, but the opponent gets a turn to respond.

**Cult Master:** draw from friendly minions dying while its effect is active. Plan it before useful sacrifice trades to refill, but keep enough mana/health to survive and use the cards. It is a fragile four-mana 4/2; playing it without a draw can be necessary development but is not the payoff. Do not assume it draws safely through any simultaneous clear that also kills it.

**Juggler, Argus and Giant:** Juggler before summons adds random pings, not guaranteed damage. Place Argus between the actual neighbors whose buff/Taunt improves the position. Giant counts bodies on both sides: plan its cost and slot before trading them away. A discounted 8/8 cannot attack immediately and has no inherent Taunt.

**Wrath and Swipe:** Wrath chooses three damage to a minion or one damage plus a draw. Favor killing a meaningful threat when cycling would leave you behind; the draw mode need not kill to draw. Swipe deals four to its target enemy and one to other enemies, including the enemy hero when a minion is targeted. Consider shields and deathrattle survivors. Do not use the primary four damage as guaranteed face damage when targeting a minion.

**Druid of the Claw and late threats:** Claw's 4/4 Charge option supplies immediate damage; its 4/6 Taunt option stabilizes and can preserve other attackers. Choose according to the position, with the mandatory choice field from the legal template. Cairne gives two waves, but no immediate protection. Cenarius can buff an established army or summon Taunts when an empty/defensive board needs them; check slots and the legal choice text. Neither card is an automatic play just because mana permits.

## Matchup aims and limits

Against Control Paladin, maintain pressure through successive boards rather than making one enormous target for Aldor. Soul can leave Treants after a destruction clear, but a follow-up Consecration can remove them. Work toward a turn where surviving attackers plus Roar pass the visible defenses; this list has no silence, so Taunt walls require actual damage and careful order. Do not promise yourself an answer not in the deck.

Against Mage, recognize that one-health tokens invite pings and buffed health or deathrattles can change clear efficiency. Five health survives an unmodified four-damage Flamestrike, but damaged Teacher may not. Use visible information to manage risk; never assume a hidden clear is present or absent with certainty. Against aggressive opponents, use removal and Taunts to keep bodies alive, then take the attack advantage when safe.

## Operational safety

Keep calling wait/act until GAME OVER; no decision ready means wait again. Use the current seq and construct each action from the current legal template. IDs are integer entities from the state. A Choose One play must include a listed choose ID and that option's required target, if any. Positions are only for minions with listed legal positions. Recheck after draws, pings, trades and choice effects. After rejection read the new state; do not repeat the rejected move.

Do not stop, concede or ask for help during a game. If time is short, take a simple legal action; fall back to end_turn in main, replace: [] in mulligan, or an allowed choice. Keep reasoning brief enough for 180 seconds per decision. Use only this folder, your visible state/history and supplied card data; no network or hidden information. Current card text overrides historical memory.
