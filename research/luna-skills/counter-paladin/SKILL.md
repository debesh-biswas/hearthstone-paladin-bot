---
name: counter-paladin
description: Play a complete Hearthstone game with the supplied Paladin research deck.
model: luna
---

# Paladin research playbook

Read deck.json and submit exactly its hero_class and 30 cards through act at deck_submission. You choose all game actions yourself; do not implement or run an automated move policy. Card text in the current state and legal action templates are authoritative.

Call wait, then act with the pending seq; continue through every decision until GAME OVER. Only use legal entity IDs, targets, choices and positions. After rejection use the newly issued seq. No decision ready means wait again, not completion. Decide promptly within 180 seconds; when uncertain choose a safe legal action and continue. Never access network, outside files or hidden information.

## Mulligan
Keep Argent Squire/Worgen Infiltrator and a playable 2/3-mana curve. Protector needs another minion. Keep Truesilver with a good early curve, especially going second. Keep Blood Knight with Squire only when the resulting curve is reasonable; never assume an enemy class before it is visible. Replace expensive minions and situational spells. Do not keep Dread Corsair without Truesilver. Do not keep duplicate expensive situational cards.

## Turn planning
Before each action consider the whole affordable turn: lethal, enemy lethal, favorable trades, development, then face pressure. Count actual mana, Taunts, shields, ready attackers, weapon durability and board slots. Charge can attack immediately; ordinary summons cannot. Draw early when it can change the plan, but do not miss lethal or sacrifice tempo merely to draw. Preserve board against faster decks, apply pressure against slow decks. Do not always trade or always attack face.

Play Juggler before summons; buffs/shields before the attacks they improve. Use Truesilver to remove important minions efficiently or push lethal. Spend its remaining durability before replacing it when beneficial; avoid unnecessary weapon replacement. Consecration deals two to enemies including hero, but shields absorb damage. Aldor reduces attack, not ongoing abilities or deathrattles. Consider Ooze's weapon value versus needing an early body. Reinforce with spare mana when useful; do not overfill the board. Play around likely clears without holding so much that you lose initiative.

## Cards present in some versions
Use only cards actually in your deck/hand; the following covers all research variants.
- Blood Knight consumes ALL current Divine Shields and gains +3/+3 for each. Strip enemy shields before damaging those minions when advantageous. Compare consuming our shields against keeping them for favorable trades. A shielded friendly attacker can trade first to spend its shield productively, then Blood Knight can remove remaining enemy shields. One shield makes Knight 6/6; two make it 9/9. It can be played as a 3/3 when tempo requires; do not wait forever or force the combo. Account for Aldor/Polymorph/Hex risk. Playing Protector before versus after Knight changes both stats and shield retention.
- Dread Corsair costs zero with Truesilver or Ashbringer equipped. Play it before a last weapon swing breaks the weapon if that improves the turn. A four-mana 3/3 Taunt is a fallback, not an automatic keep.
- Sea Giant counts minions on BOTH boards. Compare playing it before trades reduce its discount, but do not leave lethal threats alive just for a cheaper Giant. Need a free friendly board slot.
- Cult Master should precede friendly sacrifice trades when affordable; count immediate draws and whether it leaves enough mana to use them. It is fragile and should not be held forever for an ideal combo.
- Blessing of Wisdom on an attack-ready friendly minion draws on its attack; prefer immediate value. Do not spend a whole turn setting it up on a fragile exhausted minion.
- Worgen has Stealth until attacking; consider a next-turn buff, but do not skip useful damage without a reason.
- Cairne survives damage removal as a second body; silence/transform bypasses that. Tirion offers defense and Ashbringer but is also vulnerable to silence/transform. Do not overcommit into a known clear.
- Blessing of Might/Kings on a ready attacker can improve a trade or lethal; vulnerable all-in buffs can lose to hard removal. Shattered Sun and Protector can improve trades before attacks. Hammer draws and deals three. Argent Commander has Charge and Divine Shield. Avenging Wrath splits damage randomly; never treat all eight as guaranteed face damage with enemy minions present.

Use private reasoning for calculations. Keep tool calls and decisions focused; no long narration is needed. Finish every game, including losses.
