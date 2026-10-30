# infernal-warlock — theory draft

Status: unplayed research candidate, 2026-10-28. Scripted and model-led pilots use this exact list. Offline validation does not establish gameplay strength or submission readiness.

| Copies | Mana | Card |
|---:|---:|---|
| 2 | 1 | Mortal Coil |
| 2 | 1 | Voidwalker |
| 1 | 2 | Acidic Swamp Ooze |
| 2 | 2 | Doomsayer |
| 2 | 2 | Sunfury Protector |
| 2 | 3 | Earthen Ring Farseer |
| 2 | 3 | Harvest Golem |
| 1 | 3 | Ironbeak Owl |
| 1 | 3 | Sense Demons |
| 2 | 4 | Chillwind Yeti |
| 1 | 4 | Defender of Argus |
| 2 | 4 | Hellfire |
| 2 | 4 | Sen'jin Shieldmasta |
| 1 | 4 | Shadowflame |
| 2 | 4 | Twilight Drake |
| 1 | 6 | Cairne Bloodhoof |
| 2 | 6 | Siphon Soul |
| 1 | 8 | Twisting Nether |
| 1 | 9 | Lord Jaraxxus |

## Win condition and role

Survive with modest bodies and efficient resets, then make one 6/6 Infernal per turn with Jaraxxus. This attacks Control Paladin's finite answers: one expensive clear should not exhaust our supply of threats. Life Tap supplies cards before the transformation. This is a control experiment without Mountain/Molten Giants, not a historical Handlock list with arbitrary replacements.

The critical question is whether the early defensive package can buy a safe transformation. Jaraxxus does not immediately clear a threatening board; the original minion version replaces the hero at 15 health. It can lower our health and expose us to burn. Do not play it automatically at nine mana. Life Tap disappears after transformation, so preserve useful removal beforehand.

## The narrow Demon package

Only two Voidwalkers and Jaraxxus are Demons in this list. Sense Demons draws two random Demons still in the deck. If all three remain, it finds Jaraxxus with probability 2/3. If Jaraxxus and at most one Voidwalker remain, it is guaranteed to draw Jaraxxus, provided hand space allows the draw. Missing Demons produce Worthless Imps; they are not additional access to the finisher. The local engine source confirms the repeated Demon draw/fallback implementation.

Adding Dread Infernal or Siegebreaker would dilute this access. That may still be a good survival tradeoff, but it changes the central construction hypothesis. Soulfire is omitted because random discard can destroy the single win condition; this sacrifices cheap removal and reach deliberately.

## Mulligan and phases

Prioritize Voidwalker and usable early bodies. Keep Doomsayer against expected early development, not as a promise of a guaranteed clear. Mortal Coil needs a plausible one-health target. Seek Golem/Farseer into Yeti, Drake or Sen'jin. Usually return Jaraxxus, Nether, Siphon and Sense Demons. Keep a situational Hellfire only with enough early stability to survive to it.

Early: defend health without spending every card on tiny threats. Sunfury can be a plain two-drop when waiting would concede tempo. Doomsayer can deny development even if its clear kills little; when already far behind it may simply die. Do not add valuable minions to your own pending Doomsayer clear.

Middle: use Life Tap only when its health and tempo costs are affordable; leave hand space. Twilight Drake benefits from the remaining hand when its battlecry resolves, but silence collapses its bonus health. Yeti and Sen'jin are reliable alternatives rather than demanding a full hand. Position Sunfury/Argus beside the intended recipients; Argus needs four mana and is not a free emergency Taunt.

Transition: seek a quiet board or surviving Taunts before Jaraxxus. At ten mana, Jaraxxus plus the two-mana hero power costs eleven; do not assume an immediate Infernal without an actual extra-mana resource. Check visible enemy attack and plausible burst before reducing health to 15.

Afterward: spend two mana on an Infernal when safe, keep removal for meaningful threats, and turn surviving 6/6s into face damage. Do not fill the board indiscriminately into Equality. Even repeated Infernals need time to attack, and fatigue eventually limits the game.

## Interactions and failure conditions

- A ready minion can attack before Shadowflame if that preserves survival and the desired clear. Shadowflame costs four plus any body played this turn; a newly generated Infernal plus Shadowflame costs six and can clear without waiting for an attack. Never infer that a just-summoned Infernal can attack first.
- Twilight Drake is a four-damage Shadowflame donor regardless of its large health. Do not confuse health with attack.
- Nether costs eight; an Infernal afterward fits at ten mana. Nether destroys minions, but enemy deathrattles can leave new threats. Tirion can still grant a weapon unless silenced first.
- Owl can deny Tirion's shield, Taunt and weapon deathrattle. Siphon Soul alone kills Tirion but permits the weapon. Ooze is the separate answer to an existing weapon.
- Hellfire damages BOTH heroes and our board. It can make an apparently safe Jaraxxus turn unsafe. Check lethal on both sides before casting.

Control Paladin is the target hypothesis, not a promised win. Mage is the main risk because 15 health can be within burn range. Zoo and aggro Paladin test whether the deck's early plays are sufficient without Giants. Too much expensive removal may cause losses before the intended engine matters.

First variants: Sense Demons → another early defensive card if access is not the bottleneck; one Siphon → Shadow Bolt if turn-three/four removal failures dominate; one Yeti → another Shadowflame if donors survive but clears are missing. Do not add several expensive finishers before proving survival. Track Jaraxxus drawn, played, safe on the following turn, and number of Infernals that actually attack—not merely games where the card appeared.
