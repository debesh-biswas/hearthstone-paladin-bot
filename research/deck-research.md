# Deck research — 2026-10-27

Research only. No final deck lock, no playing-skill changes. Existing `decks/` and tournament outputs are untouched. Candidate JSON files live in `research/decks/`, outside the tournament's auto-discovery directory.

Follow-up: [direct Haiku/Luna evaluation](haiku-evaluation.md) records a small model-piloted sample, quota interruptions, a successful 9/9 Blood Knight and a specific missed shield interaction. Its results are separate from the rule-based screening below. Isolated research playbooks were added for that follow-up; existing playing skills remain unchanged.

## Recommendation and scope

Develop **Paladin with early pressure, resilient minions, efficient board control, and one Blood Knight**. Keep two competing versions: `steady-paladin.json` prioritizes independently useful cards; `counter-paladin.json` tests weapon discounts and conditional draw. Neither is a proven universally best deck. Priest and persistent-token Druid are separate, legal exploratory lists, not established competitors.

Read all ten existing deck lists, reviewed the 367-card catalog and package rules, inspected relevant engine implementations and greedy scoring, consulted historical sources, and checked eight interactions in synthetic local engine positions. Those positions were created for offline research; no running game's hidden state was accessed.

The key distinction: replacing missing cards with similar-looking cards does not restore an archetype's engine. Rebuild around the strongest remaining resource advantage.

## The common weakness

Most of the current lists must establish a board, preserve it for a turn, and attack to win. Several have weak early curves, conditional cards without enough enablers, or expensive replacements for removed finishers. They frequently run out of efficient plays after their first board is answered. Their best tools punish different shapes of board:

- Wide, fragile boards lose to Consecration, Hellfire, Lightning Storm, and repeated pings.
- One enormous buffed body loses to Polymorph, Hex, Sap, Aldor, or silence.
- Slow boards lose to early pressure plus damage from hand or weapons.

The response is **mixed threats**: early minions, shields, deathrattles, a few substantial bodies, weapons, and refill. Make one answer insufficient, without filling the deck with combinations that cannot function alone. This is a hypothesis about this field, not a claim that every opponent shares one exploitable flaw.

## Each existing deck: weakness and repair

| Deck | What is actually strong | Weakness of this exact list | Research repair / how to attack it |
|---|---|---|---|
| Aggro Paladin | Truesilver, Consecration, Aldor, shields; can defend while developing | Only two turn-one minions; two Might and two Kings need targets; two Hammers are expensive tempo; six-mana cards compete with rebuilding | Increase actual early bodies; reduce naked buffs and slow burn; test Blood Knight and Cairne. Kill buff targets, strip shields, then sweep; preserve a transform for Tirion. |
| Control Paladin | Equality combinations, healing, Tirion, efficient attack reduction | Cannot pressure early; Pyromancer/Equality sequencing matters; defensive top end can yield initiative; healing alone does not remove a board | Threats in successive waves rather than all at once. Deathrattles punish one-pass clears. Aldor + Kodo is eight mana and Kodo is random among eligible targets, not guaranteed removal of the desired minion. |
| Zoo Warlock | Life Tap, Flame Imp, cheap buffs, Argus, discounted Giants | No hard reset; Soulfire discards resources; weak bodies need positioning/buffs; Giant/Frostwolf are awkward after losing board; Nightblade is poor stabilization | Test one Shadowflame in place of Nightblade, accepting sacrifice cost and shield limitations. Attack health total enough to constrain Tap; remove Juggler/Wolf before trades. Do not call all Zoo builds weak because this list loses. |
| Face Hunter | Hero-power inevitability, Bow, Kill Command, cheap pressure | Leper is now 1/1; Boar is weak without a payoff; Houndmaster needs a surviving Beast; weak refill and healing matchups; only one Unleash | Test second Unleash and one Highmane over Boar/Nightblade, becoming an aggro-midrange hybrid. Oppose with Taunts plus healing while preserving a clock; merely trading forever still loses to Steady Shot. |
| Midrange Hunter | Companion, Houndmaster, Highmane, Kill Command | No turn-one minions despite being a curve deck; many mediocre Beasts; King Krush is late; Rhino without immediate Beast follow-up can be a five-mana 2/5 | Cut Krush and low-impact Beasts for early presence and Unleash. Preserve Highmane. Rhino + Highmane requires eleven mana from hand, so it is not a normal same-turn ten-mana combo. |
| Aggro Warrior | Weapons, Frothing, Kor'kron, Grommash | No turn-one minions; crowded weapon/equip package (seven equip sources including Arathi); almost no draw; Execute requires damage; replacement weapons can strand durability | Test Battle Rage/Slam and Dread Corsair; cut overlapping expensive weapons. Frostbolt/Water Elemental and Ooze attack its central resource. Weapon density makes Corsair more natural here than in Paladin. |
| Midrange Shaman | Hex, Earth Shock, Fire Elemental, Doomhammer burst | Only Ooze/Thalnos as cheap standalone minions; many three-drops; Overload delays subsequent power turns; no Bloodlust despite tokens; expensive Flametongue needs neighbors | Rebuild the early curve and test one Bloodlust, rather than simply adding more late value. Earth Shock is especially valuable into shields/deathrattles. Doomhammer + two Rockbiters is nine mana and 16 weapon damage before armor/Taunt/freeze, if both attacks remain available. Next-turn Overload still matters. |
| Tempo Mage | Frostbolt/Fireball, Water Elemental, targeted removal | No turn-one minions; Mana Wyrm is a two-mana 1/3; Juggler has modest summon support; Pyroblast may sit dead; draw costs tempo | Test earlier bodies and less top end. Force Fireballs onto minions, then rebuild with deathrattles. Faerie Dragon avoids targeted spells/powers but still dies to combat, AoE, and eligible battlecries. |
| Tempo Rogue | Backstab, SI:7, Eviscerate, Edwin, Sap | Many cards need prior plays; few cheap activators; weak reload; weapon use costs health; no broad clear; five-mana removal is slow | Test Fan of Knives against tokens, additional draw, and tighter Combo sequencing. Sap on Tirion denies the immediate deathrattle but is not permanent removal. Edwin alone is not a win condition against Aldor/Polymorph. |
| Midrange Druid | Swipe, flexible Claw, substantial Taunts | Three-mana Wild Growth sacrifices board; seven-mana Lore draws only one; Keeper is a 2/2; slow cards do not reliably repay ramp; only one Roar | Explore a different archetype: persistent tokens + Roar, no Wild Growth. Pressure ramp turns. Roar is still powerful; it is the instant Force-of-Nature/Charge combo that is gone. |
| Greedy Mage reference | Yeti/Water Elemental curve, removal, Argent Commander | No turn-one minions; one Flamestrike; targeted removal cannot answer every threat efficiently | Pressure before turn seven, mix shield/deathrattle bodies, avoid committing all resources into Flamestrike. Its single-action lethal checks exist; it is not completely unaware of lethal. |

These are construction/interaction diagnoses, not measured causal explanations of every tournament loss.

## Overlooked cards and packages

| Card/package | Concrete advantage | Limitation and decision |
|---|---|---|
| **Blood Knight** | Three-mana 6/6 after one shield, 9/9 after two; consumes enemy shields too | Removes our shields as well. A 6/6 still loses to Aldor/Polymorph; two shields put it into Big Game Hunter range. One copy in both Paladins; do not automatically harvest a valuable friendly shield. |
| **Dread Corsair + Truesilver** | Four-attack weapon makes Corsair cost zero: weapon plus 3/3 Taunt for four mana | Only two weapon activators. With eight cards seen and no mulligan conditioning, probability of at least one of each two-copy card is 20.5%; this is not the probability of executing the combo. Keep in experimental version only. Play before the weapon's last swing breaks it. |
| **Sea Giant** | Both boards reduce cost, so enemy token strategies provide our discount too | Poor after a clear and vulnerable to hard removal. One copy, not two; calculate discount before trading, while considering enemy replies. |
| **Cult Master** | Converts expendable recruits and deathrattle trades into cards | Four-mana 4/2 is fragile and useless without trades. Play before friendly deaths; do not assume it survives a simultaneous clear. Experimental Paladin and token Druid only. |
| **Blessing of Wisdom** | One mana can replace itself immediately on an attack-ready minion and draw again later | No stats; poor when behind; costs a slot. Verified friendly-target draw, not all enemy-target edge cases. Experimental version only. |
| **Cairne** | Two sequential 4/5 bodies make one damage clear insufficient | Six mana, no immediate defensive effect, and transform/silence bypasses deathrattle. One copy complements early pressure instead of adding several slow threats. |
| **High Inquisitor Whitemane** | Can recover minions deliberately traded away this turn and add a 6/8 | Requires seven mana, friendly deaths this turn and board space. It cannot recover last turn's casualties. Source inspected, not dynamically tested; leave as later replacement for Cairne, not assumed improvement. |
| **Harrison Jones / Ooze** | Weapons are important across Paladin, Warrior, Hunter, Shaman and Rogue | Harrison costs five and is mediocre into Mage/Zoo. Start with one Ooze; test Harrison only if actual opponent mix warrants it. |
| **Earth Shock** | Silence happens before damage: removes shield/deathrattle and then hits | Shaman's overall curve still needs rebuilding. One excellent answer does not make the current list strong. |
| **Shadow Madness** | Three mana can take a small enemy minion, trade it off, and retain its deathrattle token | Needs eligible attack and a productive trade; otherwise the surviving minion returns. Verified on Harvest Golem. A concrete reason to revisit Priest. |
| **Violet Teacher + Power of the Wild** | Teacher's new token appears before the buff: Teacher becomes 4/6 and token 2/2 | Six mana together, and future cheap spells compete with board development. Verified timing in engine. |
| **Soul of the Forest / Savage Roar** | Sticky wide boards retain a next-turn threat; Roar adds 2 per attack-ready minion plus 2 hero attack | No instant Charge on new Treants. Four ready minions plus an attack-capable hero gain ten damage from one Roar before Taunts. Soul does little on an empty board; one copy. |
| **Shadowflame / Brawl** | Real recovery tools missing from current Zoo/Warrior lists | Shadowflame needs a sacrifice and damage does not bypass Divine Shield; Brawl removes our board too and leaves a random survivor. Test deliberately, not as universally good additions. |
| **Jaraxxus** | Repeated 6/6s can dominate a slow value game | Nine-mana setup and 15-health hero are dangerous against burn. Missing Handlock Giants does not erase every control-Warlock possibility, but this is lower priority than Paladin. |

Avoid multiplying conditional packages. Sword of Justice, Redemption, Righteousness, Windfury finishers, Murloc engines and Whitemane each have possible homes, but including all attractive synergies in one list creates unplayable hands. Murlocs also lost Old Murk-Eye and Warleader's health buff; this field already contains plentiful small-board punishment.

## Concrete deck candidates

All JSON files contain exactly 30 legal cards and pass `hs_arena.deck.validate_deck_data`. They are deck data, not ready-to-play skill folders.

### Steady Paladin — practical first candidate

| Qty | Card | Reason |
|---:|---|---|
| 2 | Argent Squire | Early shield body and buff target |
| 2 | Worgen Infiltrator | More turn-one pressure; protects the initial setup from targeted removal until revealed |
| 2 | Argent Protector | Preserve a meaningful attacker while adding a body |
| 2 | Knife Juggler | Early threat; recruits and deathrattle summons supply additional triggers |
| 2 | Loot Hoarder | Cheap cycling body |
| 1 | Acidic Swamp Ooze | Weapon answer without a large curve tax |
| 2 | Aldor Peacekeeper | Reduce large attackers while building our board |
| 2 | Harvest Golem | Survives a single removal wave through its token |
| 2 | Shattered Sun Cleric | Turn existing small bodies into favorable trades |
| 1 | Blood Knight | Shield counter and optional early large threat |
| 2 | Truesilver Champion | Efficient removal or eight total weapon damage |
| 2 | Consecration | Punish token boards while preserving our own |
| 1 | Blessing of Kings | One large buff; limit exposure to removal |
| 2 | Chillwind Yeti | Reliable four-mana stats; five health survives an unmodified Flamestrike |
| 1 | Hammer of Wrath | Damage plus replacement card; one rather than two |
| 1 | Argent Commander | Immediate trade/reach with shield |
| 1 | Cairne Bloodhoof | Resilient second wave |
| 1 | Tirion Fordring | Taunt/shield plus weapon finish |
| 1 | Sea Giant | One payoff for board congestion |

Compared with current aggro Paladin: remove 2 Might, 1 Kings, 1 Hammer, 1 Commander and 1 Avenging Wrath; add 2 Worgen, 1 Blood Knight, 1 Yeti, 1 Cairne and 1 Sea Giant. Six substitutions, no invented new engine.

**Counter Paladin:** replace 1 Yeti, 2 Cleric and 1 Hammer from Steady with 2 Dread Corsair, 1 Cult Master and 1 Blessing of Wisdom. This directly tests whether tempo discounts and conditional refill repay the consistency cost.

Opening plan: prioritize a real turn-one body and a playable curve; Protector needs a useful target. Do not keep Giant/Cairne/Tirion by default. Preserve Blood Knight for enemy shields when worthwhile, but do not miss several turns waiting. Establish board, use Truesilver/Consecration to retain it, and save a second wave against clears. This is a play hypothesis, not an implemented pilot.

Remaining vulnerabilities: no unconditional hard removal, little healing, limited draw in Steady, vulnerability to transforms, and Giant/Corsair dead draws. Aldor does not remove a dangerous ongoing effect. We cannot describe these as weakness-free decks.

### Board-theft Priest — exploratory counter to small boards

`board-theft-priest.json` combines Squire/Chaplain, Blademaster/Circle, Pyromancer/cheap spells, Pain, Shadow Madness, Holy Nova, Cabal and one Mass Dispel. Thoughtsteal replaces some resources; Cairne/Natalie offer late threats.

Why revisit it: Holy Nova is four mana, Shadow Madness three, Thoughtsteal two; Chaplain can build favorable early health totals. Cabal steals Juggler, Loot Hoarder or Harvest Golem rather than merely removing them. Mass Dispel can strip shields, buffs, Taunts and deathrattles before trades.

Why it may fail: no Northshire draw engine, Power Word: Shield does **not** draw, Circle is conditional and heals enemies too, Pyromancer can hurt our own board, four-attack enemies dodge Pain/Death, and there is little face reach. Two Cabals may be too slow. This candidate challenges the blanket “Priest is dead” assumption; it does not establish Priest as strong. Legality checked; no full games run for this list.

### Persistent-token Druid — exploratory alternative to ramp

`persistent-token-druid.json` replaces ramp with early bodies, Teacher, Power of the Wild, persistent Force of Nature Treants, two Roars and one Soul of the Forest. Cult Master provides conditional refill; one Giant rewards board width. Claw supplies flexible defense/reach, with Cairne/Cenarius as late pressure.

Why revisit it: old combo Druid disappeared, but persistent tokens can threaten several turns. Teacher/PotW timing is favorable. Why it may fail: no strong unconditional refill, difficult sequencing, hard-to-answer large Taunts, expensive top end, and repeated AoE beats one Soul. All new Treants must normally wait a turn to attack. Legality checked; no full games run for this list.

## Evidence and experiment design

First screen: seed start **271027**, 50 games per orientation per matchup, 100 per matchup. Both sides use the unchanged built-in greedy pilot. Four opponents: Greedy Mage, original aggro Paladin, control Paladin and Zoo. Each candidate and baseline plays 400 games; total 1,200. This deliberately targets the known opponent plus the leading local archetypes, not the entire class population.

| List | Greedy Mage | Aggro Paladin | Control Paladin | Zoo | Total |
|---|---:|---:|---:|---:|---:|
| Original aggro Paladin | 66/100 | 50/100 | 43/100 | 48/100 | 207/400 (51.75%) |
| Counter Paladin | 63/100 | 69/100 | 70/100 | 67/100 | 269/400 (67.25%) |
| Steady Paladin | 73/100 | 65/100 | 67/100 | 63/100 | 268/400 (67.00%) |

All 1,200: **0 draws, 0 forfeits, 0 illegal actions, 0 timeouts, 0 engine-voided games**. Per-decision latency is **not recorded by this built-in-bot run**, so max decision latency is unavailable. Game duration is not a substitute. These runs do not test model/tool latency.

Raw summaries: `screen-results.json`. Full local replays: `games/deck-research-20261027/`. Fresh-seed confirmation uses seed **891027**, identical lists and matchup allocation, with results recorded separately in `holdout-results.json`; see confirmation section below. Input SHA-256 hashes are in `input-hashes.json` (captured before confirmation).

Eight assertion-backed engine checks passed in synthetic positions: Blood Knight consumes both sides' shields and becomes 9/9; Truesilver discounts Corsair to zero; Sea Giant counts both boards; friendly Wisdom attack draws; Cult Master draws from a friendly trade death; Teacher token receives PotW buff; Shadow Madness retains a stolen Golem's deathrattle token when it dies under our control; Equality/Consecration clears an unshielded Yeti while preserving our Squire's shield. These are narrow interaction checks, not broad game correctness proofs.

### Pilot confounding and confidence

The greedy pilot has no dedicated handling for Blood Knight shield value, Corsair setup, Cult Master trading order, Equality combinations, or most class synergies. Its Holy Smite configuration says two damage while the actual pool card deals three. Unknown untargeted spells receive a generic score; Choose One branches are not evaluated with a full turn plan. That explains why results can underrate some decks, but it does **not** license inventing corrected win rates.

An individual 100-game matchup has roughly ±9–10 percentage points of binomial sampling uncertainty near 50–70%. Seat-swapped/shared seeds introduce pairing, and aggregate opponent weights are artificial: do not treat every game as an independent ladder sample or a one-point difference as meaningful. Baseline mirror is exactly 50% by symmetry in this design and adds little information. Full attribution requires one-card/package ablations; this research changes six or more slots at once.

Next decisions should use held-out results, actual-pilot replays, and the desired opponent mix. Prioritize: (1) original versus original + one Blood Knight; (2) remove Giant separately; (3) compare conditional draw/discount package; (4) test Priest/Druid with pilots that understand them. Keep the original lists as controls. No course attempt is needed for any of this.

## Fresh-seed confirmation and current decision

The unchanged lists completed another 1,200 games starting at seed **891027**:

| List | Greedy Mage | Aggro Paladin | Control Paladin | Zoo | Total |
|---|---:|---:|---:|---:|---:|
| Original aggro Paladin | 51/100 | 50/100 | 40/100 | 50/100 | 191/400 (47.75%) |
| Counter Paladin | 58/100 | 73/100 | 53/100 | 60/100 | 244/400 (61.00%) |
| Steady Paladin | 68/100 | 70/100 | 60/100 | 57/100 | 255/400 (63.75%) |

Across both batches: **Steady 523/800 (65.38%), Counter 513/800 (64.13%), original 398/800 (49.75%)**. The combined matchup wins per 200 games are:

| List | Greedy Mage | Aggro Paladin | Control Paladin | Zoo |
|---|---:|---:|---:|---:|
| Original | 117 (58.5%) | 100 (50.0%) | 83 (41.5%) | 98 (49.0%) |
| Counter | 121 (60.5%) | 142 (71.0%) | 123 (61.5%) | 127 (63.5%) |
| Steady | 141 (70.5%) | 135 (67.5%) | 127 (63.5%) | 120 (60.0%) |

All **2,400 games** completed with **0 draws, 0 forfeits, 0 illegal actions, 0 timeouts and 0 engine voids**. Max decision latency remains **unmeasured**. The scored candidates won 1,434 of these games; the other 966 were opponent wins. Hashes of all six distinct input deck files remained unchanged through confirmation.

**Research decision:** Steady Paladin is the first candidate to develop further because it retained its advantage over the original on fresh seeds, uses fewer conditional packages, and performed best against the known Greedy Mage bot. Counter remains a live alternative; the 1.25-point combined difference between candidates is too small to claim superiority. Improvements over the original are much larger in this specific test field, but these are greedy-versus-greedy measurements, not predictions for Astra or classmates.

Reproduce an individual run using the project environment's `hs-arena`:

```sh
pkg/hs-arena-0.2.2/.venv/bin/hs-arena play \
  --p1 greedy:research/decks/steady-paladin.json \
  --p2 greedy:decks/control-paladin/deck.json \
  --games 50 --seed 891027 --parallel 1 --out games/research-reproduction
```

Repeat with p1/p2 swapped into a distinct output directory; repeat for each opponent, candidate and seed start above. The original baseline is `decks/aggro-paladin/deck.json`; Greedy Mage is `pkg/hs-arena-0.2.2/decks/greedy_mage.json`. Each batch uses 24 runs, 50 games each. Use fresh output directories to avoid mixing or overwriting runs.

No claims of statistical significance, per-card causal benefit, model-pilot reliability, or a globally optimal deck are made. Priest/Druid remain unplayed hypotheses. A later pilot-aware evaluation is necessary before final selection.

## Sources and interpretation

1. Local authority: `pkg/hs-arena-0.2.2/data/cards.json`, `docs/handout.md`, `docs/protocol.md`, `README.md`, card implementations under `src/hs_arena/_vendor/fireplace/cards/classic/`, and `agents/greedy_bot.py` / `greedy_config.json`. Local card versions and actual engine behavior take precedence over web lists.
2. [Blizzard: Introducing the Core Set and Classic Format](https://hearthstone.blizzard.com/en-us/news/23620129/introducing-the-core-set-and-classic-format): the official Classic format restored June 2014 versions. That is not this course's modified Legacy pool.
3. [Blizzard: Patch 17.0](https://hearthstone.blizzard.com/en-gb/blog/23357896/): Priest's redesign/buffs and replacement cards motivate revisiting the class. Exact values above were checked against the local catalog.
4. [Vicious Syndicate: Classic report #1](https://www.vicioussyndicate.com/classic-vs-data-reaper-report-1/): historical matchup evidence supports examining Zoo and Shaman, but cannot rank decks in this altered pool. We borrow questions, not its win rates.
5. [Vicious Syndicate: Krea's Token Druid](https://www.vicioussyndicate.com/kreas-token-druid/): historical precedent for Teacher/Soul/Roar packages. Its complete deck and surrounding format are not claimed legal here.

All deck recommendations and local matchup diagnoses are our hypotheses or local measurements, not conclusions established by the historical sources.
