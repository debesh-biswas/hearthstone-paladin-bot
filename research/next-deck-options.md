# Alternatives beyond surviving a board clear

Follow-up: these theory drafts now have scripted and model-led packages. See [candidate-pilot-handoff.md](candidate-pilot-handoff.md) for implementation, offline checks and the separately recorded validation-launch incident. The original theory-only activity described below remains distinct from that later work.

2026-10-28. Theorycrafting only. No matches, model evaluations or engine simulations were run for these candidates. Existing results remain unchanged. None is selected; the existing player and skills are untouched. New folders contain a fixed deck JSON and concept-led strategy document, not a runnable SKILL.md. The evaluation owner can attach the established runtime/legality wrapper without confusing these drafts with validated skills.

## What the earlier evidence does and does not say

Steady went 3–5 in the supplied comparison; one Control loss contained a verified missed lethal. The later original Zoo, Recovery Zoo and token Druid each went 1–3 in a small screening batch. These samples do not establish a reliable ranking or justify permanently discarding the lists.

The structural concern is shared: many payoffs require a friendly board to survive. Blood Knight concentrates attack into an answerable minion; Roar is stranded without attackers; Zoo lost Doomguard and Power Overwhelming and can expend its remaining reach defending the board. Recovery cards alone do not restore a credible finishing clock. Control Paladin can trade health, clears and Taunts for enough time to exhaust those threats. That is a deck-building hypothesis supported by observed failure modes, not a statistically established explanation of every loss.

Three different solutions deserve comparison. These are research priorities, not estimated win rates.

| Priority | Candidate | Different route to victory | Main reason it might fail |
|---|---|---|---|
| 1 | [Burst Shaman](../decks/burst-shaman/strategy.md) | Early pressure transitions into weapons and spell damage from hand | Overload, freeze/Ooze, insufficient healing and draw |
| 2 | [Infernal Warlock](../decks/infernal-warlock/strategy.md) | Repeated 6/6s make finite removal insufficient | Dies before a safe Jaraxxus turn; 15-health hero is vulnerable to burn |
| 3 | [Pressure Hunter](../decks/pressure-hunter/strategy.md) | Lower curve plus sticky Highmanes, hero-power pressure and Kill Command | Limited refill and healing; Beast-dependent cards can strand |

Shaman is the first general-field hypothesis. Warlock is the most distinct anti-control experiment. Hunter is a lower-complexity comparison with fewer multi-card dependencies, but not necessarily a stronger deck.

## Why the card removals matter

Historical Aggro Shaman uses the same pressure-to-burst transition, but its published list includes absent Leeroy/Azure Drake and cheaper versions of Rockbiter, Hex and Flametongue. Borrow the strategic mechanism, not its performance claims or mana arithmetic. See [Icy Veins' 2021 Classic Aggro Shaman guide](https://www.icy-veins.com/hearthstone/classic-aggro-shaman-deck).

The Jaraxxus approach is based on the actual available minion and local implementation: `src/hs_arena/_vendor/fireplace/cards/classic/warlock.py`, classes EX1_323, EX1_tk33 and EX1_317. Sense Demons can concentrate access when other Demons are excluded. This gives up useful defensive Demons and does not magically replace Handlock's absent Giants.

All exact costs and availability were taken from the bundled `data/cards.json`. Reading source establishes intended interactions; it does not substitute for runtime verification. The actual pool is not historical Classic and online tier rankings cannot be transferred to it.

## Other options considered

| Direction | Useful idea | Reason not to construct it ahead of these three |
|---|---|---|
| Enrage Warrior | Battle Rage can refill; Grommash plus Inner Rage provides 12 Charge damage for eight mana | Existing aggro Warrior already uses weapons/Grommash. A real redesign needs to prove damaged-board draw consistency without Acolyte, rather than merely adding more conditional activators. Worth a subsequent focused pass. |
| Malygos Shaman | Large spell-damage burst | Nine-mana Malygos plus two one-mana Bolts costs eleven. Far Sight discounts are uncertain; a one-turn-surviving Malygos is not a dependable combo. Thalnos supports smaller, immediately playable bursts instead. |
| Ancestral Spirit Shaman | Repeated large minions can resist destruction | Silence/transform and tempo losses remain; Earth Elemental's Overload can block the recovery turn. This retains more of the original dependency on board survival. |
| Freeze Mage | Stall into Alexstrasza and burn | No Ice Block or Ice Lance removes key safety and damage tools. A promising-looking paper combo is insufficient without a full survival/damage budget. |
| Miracle Rogue | Auctioneer can convert cheap spells into access | Missing Conceal, Azure Drake and Leeroy, plus weaker Preparation, make the historical engine/finisher substantially less transferable. |
| Board-theft Priest | Convert opposing minions into resources; disrupt buffs | Existing legal research list remains available. Theft thresholds and matchup dependence make it a targeted counter rather than the leading broad-field hypothesis. |

## Evaluation handoff — requested work for the separate testing owner

Start with Shaman if budget is limited. Compare it with existing midrange Shaman using the same model, effort, runtime wrapper and equivalent instruction quality. Include established aggro Paladin, Control Paladin, tempo Mage and Zoo. Built-in Greedy Mage can be an additional sanity opponent but does not replace model-piloted opposition. For Hunter, retain existing midrange Hunter as its direct baseline.

Use multiple fresh seeds and balance the actual first-player assignment; player-slot order alone does not establish who starts. A useful initial screen is five seed pairs per matchup (ten games), still too small to certify superiority. Expand only a promising, interpretable result. Freeze the deck/playbook within a batch and record exact inputs. Change one package at a time afterward.

Record games/wins by matchup and actual first player; hero-death versus forfeit outcomes; all rejected actions; timeouts and maximum full decision latency. Audit whether a lost game had a missed lethal, unspent usable damage, incorrect target, premature resource use or impossible combo plan. Do not relabel losses as wins after finding pilot errors.

Candidate-specific evidence:

- Shaman: damage delivered by weapon/spells; cards stranded by Overload; weapon destruction/freeze; lack of Taunt access; whether held burn could actually have formed lethal.
- Warlock: survival to nine mana; Jaraxxus access with/without Sense Demons; safe transformation; Infernals generated versus those that attack; dying to burn afterward.
- Hunter: Beast availability for Kill Command/Houndmaster; Highmane attacks and deathrattle value; damage-versus-healing race; empty-hand losses; unused hero-power opportunities that were actually affordable.

Every pilot should calculate immediate lethal, then necessary survival, then its deck-specific plan. Execute only current legal-action templates with current entity IDs and seq; re-read after every action, random result or rejection. Targeted battlecries require the offered target fields. Never assume an attractive theoretical sequence is legal merely because its total mana fits.

No new performance numbers exist yet. Static legality is a prerequisite, not evidence of strength. These drafts deliberately remain separate from shipped skill changes.
