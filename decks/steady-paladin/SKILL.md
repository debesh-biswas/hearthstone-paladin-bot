---
name: steady-paladin
description: Play a resilient midrange Paladin through board control, favorable exchanges, and sustained pressure, adapting the plan to the opponent and the current position.
model: luna
---

# Steady Paladin — understand the position, then choose the line

## 1. Your objective and your deck

Win a complete game using the fixed 30-card Paladin list in `deck.json`. Choose the plays yourself. This is a **midrange deck**: early minions establish a foothold, weapons and battlecries help preserve it, and resilient threats convert that advantage into repeated attacks. It can defend against faster decks and pressure slower ones. Its name does not mean play slowly.

Our main advantage is making the opponent spend more resources answering our threats than we spend creating them. A shield absorbs a hit; Harvest Golem and Cairne leave another body; Truesilver can remove two minions with one card; Consecration can remove several while preserving our board. Those exchanges leave survivors that attack again. **The eventual payoff is damage to the enemy hero, not a permanently tidy board.**

Our weaknesses explain our choices: little draw, limited healing, no unconditional hard removal, and only one large attack buff. We cannot spend forever trading every enemy recruit or saving every card for perfect value. Nor can we race an opponent who will kill us first. We win by deciding what must be answered and what can safely be ignored.

At the first decision, call `wait`, read `deck.json`, and submit its exact `hero_class` and `cards` through `act` with the current seq. The runtime does not submit the file for you. Do not change the deck to guess the hidden opponent. Read `references/guide.md` once during setup if time permits; this skill contains the essential plan, while the guide has worked examples and matchup reasoning. Do not repeatedly reread it each turn.

## 2. Choose your role from the board, not just the class

Ask: **If we both continue our current plans, who wins first? What changes that outcome?** Use visible health, armor, board, weapons, hand, mana and revealed cards. Opponent cards not shown are possibilities, not facts.

| Position | What winning now requires | What to avoid |
|---|---|---|
| Behind and under immediate threat | Remove enough damage to survive, then build something that can contest next turn. Combine removal with a body when possible. | Developing an impressive minion that cannot stop lethal; trading for distant value while dying. |
| Board contested | Create favorable exchanges and leave useful survivors. Buffs, shields and weapons can break the stalemate. | Clearing by default when a less costly line preserves both pressure and safety. |
| Ahead on board | Protect the threats that matter, push hero damage, and make the opponent answer you. | Giving away the attack advantage by trading into harmless bodies or deploying every reserve into a clear. |
| Opponent wins a long game | Establish a clock and accept calculated risks to finish before their stronger engine takes over. | Turning every turn into an exchange of equal resources with no damage progress. |
| Opponent has faster damage | Stabilize health and board first; become aggressive once their attack cannot beat your clock. | Assuming a high hero health total makes a wide enemy board harmless. |

These roles can change within one turn. A successful Consecration can turn defense into pressure; losing your board can turn a previously correct race into a losing one. Reassess after each returned state, especially after random pings, draws, deathrattles and secrets.

## 3. Opening hand: buy useful turns

Mulligan for a sequence of plays, not a collection of individually strong cards. A hand that acts on turns one, two and three is usually better than one filled with answers and finishers. Opponent information may influence a keep only if it is actually visible.

- **Early foothold:** prioritize Argent Squire or Worgen Infiltrator. Juggler, Loot Hoarder and Ooze are useful two-drops. Protector is much better with an earlier body to shield, but can be a plain 2/2 when development matters more than its battlecry.
- **Useful follow-up:** Harvest Golem is reliable. Cleric needs a body worth buffing. Aldor is excellent against a relevant early threat, but keeping several three-drops without an early play makes a slow hand.
- **Coin and curve:** the Coin can advance a meaningful play or let two cards cooperate. Keep Truesilver with a credible early curve, more readily going second. Yeti is a possible keep with the Coin and sufficient early plays. Do not spend the Coin merely because it is available.
- **Blood Knight:** Squire plus Knight can threaten a turn-three 6/6 if the shield survives. That supports a keep with a sensible curve; Knight without a source of value is not a mandatory keep. Enemy shields are uncertain unless revealed.
- **Expensive/situational cards:** normally return Giant, Cairne, Commander, Tirion, Kings and Hammer. Consecration can be a justified keep against clearly fast, wide pressure if the rest of the hand still contests early turns.

In mulligan, send entity IDs to replace, not card IDs. An empty replacement list keeps everything.

## 4. Think in complete turns, execute one action at a time

Compare a few meaningful plans rather than scoring every action in isolation. A plan should say what we accomplish now and what useful board, health, hand and mana situation we leave for the next turn. Choose its first legal action, then update the plan from the new state.

**First establish the constraints:** can we win now; can the opponent kill us if we do not intervene; and which legal resources can act this turn? Count Taunts, Divine Shields, frozen/exhausted attackers, mana, weapon durability and the seven-minion limit. A newly played Blood Knight or Giant cannot attack immediately. Commander can.

**Then compare the consequences:** one plan may clear everything but empty our hand; another may remove only the dangerous attacker and add a Yeti. Favor the second when the remaining enemy board is manageable and the Yeti produces a better next turn. Favor the full clear when the enemy's buffs, damage engines or lethal threat make that surviving board unsafe. Spending all mana is useful only when the resulting position is useful.

**Before committing an attack, ask what it destroys or unlocks.** It may consume a shield Blood Knight could harvest, reduce Sea Giant's discount, kill a draw minion, trigger a secret, or break a weapon. Buffing or shielding first may preserve the attacker. Sometimes attacking first is correct; the reason is the resulting board, not an unconditional order rule.

Only the chosen move needs to be sent. Keep calculations concise and internal; avoid lengthy narration or writing a move program during the game. Aim to decide in seconds rather than use the full 180-second deadline.

## 5. The card packages and their purposes

### Establish bodies, then improve their exchanges

Squire and Worgen establish early attacks. Squire's shield can preserve it through a trade; Worgen's Stealth protects it from targeted interaction until it attacks. Holding an attack for a worthwhile buff can be correct, but routinely skipping damage wastes pressure. Juggler threatens extra damage from subsequent summons, including recruits and deathrattle bodies; put it before summons when compatible with the rest of the plan. Its random damage is not guaranteed lethal.

Protector and Cleric turn a body already on board into a better attacker. Think about the **trade enabled**: which minion survives, what damage is prevented, and what remains afterward? Kings can turn a ready small minion into immediate damage or a favorable trade. Putting several resources onto one minion increases exposure to transform, silence, Sap or Aldor; spread threats when that risk outweighs the immediate payoff. Do not reject a good urgent buff solely because removal might exist.

### Control the fight without surrendering development

Truesilver provides two four-damage attacks. Removing a minion with the weapon can preserve an attacker that will deal damage for several turns. Your hero pays the combat damage, so check whether that expenditure makes you lose the race. Its two-health restoration happens **before** combat damage; at full health it cannot absorb the damage you are about to take. Equipping a new weapon does not refresh a hero attack already used this turn or let a frozen hero attack.

Consecration deals two to every enemy, including the hero. Its value is not just the number of kills: it can enable several favorable trades or finish the game. Conversely, two inconsequential kills may not justify using your only answer to a larger wave. Enemy shields absorb its damage; deathrattles may leave replacement bodies. Judge the board after those effects, not just the initial health totals.

Aldor turns an enemy's attack into one while adding a 3/3. This often lets us ignore a large body or trade without losing important minions. It does not remove Taunt, shield, deathrattle, freeze effects or ongoing abilities. Ooze destroys a weapon: weigh preventing its remaining swings against needing the 3/2 now. A small dagger can be worth destroying, but saving Ooze for a credible larger weapon can also be right.

### Blood Knight: convert shields into a different kind of advantage

Blood Knight removes **all** Divine Shields and receives +3/+3 for each. Zero shields gives a 3/3, one a 6/6, two a 9/9. The benefit is both the new body and the enemy shields removed; the cost includes the friendly shields lost. It does not remove Taunt or attack on the turn it is played.

Before any shield-consuming attack, compare the board **with Knight first** against the board **with the attack first**. Enemy shields are usually valuable to strip without sacrificing an attacker. Friendly shields may be more valuable protecting a large ready attacker than adding stats to a new, exhausted body. Protector before Knight feeds its buff; Protector afterward shields the resulting threat. Choose the outcome you need.

**Concrete lesson:** with nine mana, Knight in hand, your unshielded 4/2 Commander and 1/1 recruit facing a shielded 6/6 Tirion, attacking Commander first throws it away just to remove the shield. Knight first removes the shield and creates a 6/6. If you then choose the same two attacks, Tirion ends at one health rather than five. Those attacks are still optional: assess the whole board and your survival. Do not infer that every Knight-first line guarantees a win.

When no useful shields are available, a three-mana 3/3 can be the correct tempo play. Waiting for a spectacular combination can cost more attacks than the eventual stats are worth. After growing Knight, remember that attack reduction and transforms still answer it; a second shield makes it susceptible to Big Game Hunter's attack threshold.

### Sustain pressure and close

Loot Hoarder replaces itself when it dies, while Hammer deals three and draws immediately. Draw before flexible decisions when the new card could improve the turn, but prioritize a known lethal or necessary survival line. They are limited refill, not permission to exhaust your hand carelessly.

Yeti is an independent 4/5. Harvest Golem and Cairne create successive bodies that resist a single removal wave. Deathrattles need board space and can be bypassed by silence or transform. Use these threats to maintain pressure without requiring several cards to function together.

Sea Giant costs one less for every minion on either board. A crowded enemy board can help us establish an 8/8. Calculate whether to play it before trades or Consecration shrink its discount, and reserve its board slot. But a cheap Giant is not defensive removal or Taunt: if you die next turn, its discount is irrelevant.

Commander offers four immediate attack plus a shield. Tirion offers Taunt, shield and a 5/3 deathrattle weapon: he can stabilize or force a costly answer. Ashbringer replaces an existing weapon and does not refresh an already-used hero attack. Choose Tirion with the current danger and enemy answers in mind, rather than treating eight mana as an automatic instruction to play him.

## 6. Turn an advantage into a win

Build a realistic damage clock. Ready minions and an available hero attack are repeatable pressure if they survive; Hammer, Consecration, Commander and Kings can add reach within your actual mana budget. Do not add together mutually unaffordable cards or count an exhausted/frozen attacker. Taunts block attacks but do not stop face-targeted spell damage. Account for armor and relevant visible protection.

Trade when doing so preserves more future damage, prevents a losing race, or removes an engine that will outgrow your board. Attack face when the enemy is forced to answer you and their surviving board cannot beat your clock. Being ahead does not mean remove every enemy; being behind does not mean trade into everything.

Keep a second wave when you already have sufficient pressure and a plausible clear would otherwise empty your resources. A healthy Yeti survives an unmodified four-damage Flamestrike; a shield or deathrattle can preserve something, but none is protection against every answer. Do not play around every imaginable card at once. Use opponent class, mana and revealed cards as evidence, and accept risk when holding back would lose anyway.

Reinforce can create future attackers and buff targets without spending a hand card. It can be better than overextending a valuable threat, or worse than reserving a slot for Giant/Tirion. It is a resource choice, not a compulsory last action whenever two mana remain.

## 7. Stay in the game and stay legal

Use current `legal_actions` as the authority. Every board action uses integer entity IDs from that state. Include `target` only when the template lists targets; choose a listed target when required. Positions apply only to minions. For a choice, select the allowed option(s) matching the current plan. After a rejection, inspect the error and new seq; do not repeat the rejected action unchanged.

If your preferred plan cannot be resolved quickly, take a clearly useful legal action and reassess. If no useful main-phase action is clear, `end_turn` is the safe fallback; in mulligan keep the hand with `replace: []`, and in a choice use a legal listed option if time is short. Do not exit, concede, or wait out a decision because the position is bad. Continue `wait`/`act` until GAME OVER; “no decision ready” means wait again.

Use only this working folder, the supplied card data, your visible state and history. Never inspect hidden opponent information or use the network. This is the package's modified Basic/Classic pool; use its actual card text instead of remembered modern or original-2014 versions. The game state overrides a stale assumption in this guide.
