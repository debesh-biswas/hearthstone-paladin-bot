# Three standard decks and their pilots

2026-10-28. The cards are unchanged from the theory drafts. Each deck now has a standalone Python pilot, an MCP client for no-model evaluation, a Haiku relay skill, and a separate model-led Haiku skill. These are research implementations, not tournament-proven improvements.

## Files and modes

| Deck | Canonical scripted package | Model-led package |
|---|---|---|
| Burst Shaman | `decks/burst-shaman/` | `research/haiku-skills/burst-shaman/` |
| Infernal Warlock | `decks/infernal-warlock/` | `research/haiku-skills/infernal-warlock/` |
| Pressure Hunter | `decks/pressure-hunter/` | `research/haiku-skills/pressure-hunter/` |

Every canonical package contains:

- `deck.json`: the standard 30-card class/list in the arena's supported format.
- `strategy.md`: human/model-readable card table, win condition, mulligan, matchup roles, sequencing, weak slots and proposed isolated variations.
- `scripts/move.py`: the deterministic decision function and standalone JSON interface.
- `client.py`: the existing player's stdio MCP client adapted to load this package's pilot and public history.
- `SKILL.md`: Haiku relays script output by default; a clearly described manual fallback keeps a failed shell command from ending the session.

Model-led packages contain the identical deck JSON and strategy plus a playbook that explicitly asks Haiku to choose moves itself. This avoids changing pilot mode silently during an experiment. All six deck copies pass the official static deck validator, and all six skills pass `load_skill`.

The built-in rule bot can also consume the same canonical `deck.json`; that is a fourth, generic baseline. It does not read the strategy or use this new pilot. Therefore “rule bot” must be labelled precisely in result reports.

## Relationship to the existing player

Inspected `player/scripts/move.py`, `player/client.py`, the official greedy bot and the protocol. The existing player implements a 24-wide, up-to-20-step beam search using a small Paladin-specific transition model, followed by a legal-action check and greedy fallback. Its simulated hero power summons a Recruit; its supported spells and battlecries principally cover the Paladin list. Merely pointing it at another deck JSON would not implement these three decks' interactions.

The new code preserves `decide(state) -> action`, the JSON relay shape `{seq, action}`, and the stdio client pattern. It does **not** claim to reuse the Paladin search model or its measured performance. It uses exact root legal actions, bounded face-combination search, and explicit class/card heuristics. This is a different pilot that must be evaluated separately.

The same implementation is copied into each standalone folder and branches on the visible class/cards. Copies are intentional: an exported skill cannot depend on a sibling deck folder. The offline checker verifies their hashes remain identical. When changing shared logic, update the Shaman copy, copy it into the other two scripts folders, and rerun the offline checks. Do not modify the existing `player/` to maintain these packages.

## Decision architecture

1. **Deck submission:** read the local canonical list and submit it exactly. **Mulligan:** class-specific keeps favor an actual curve, avoid duplicate expensive keeps, and return slow combo pieces. **Choice:** score the offered options by current mana, pressure, Beast activation, Taunt access and finisher value; obey the template's cardinality.
2. **Legal expansion:** enumerate offered target, insertion-position and Choose One combinations. Choice-specific targets stay coupled to their option. Unknown IDs and invented targeting parameters never enter the action pool. Concede is excluded.
3. **Immediate lethal search:** explore supported damage, Rockbiter buffs, Doomhammer, Al'Akir, Thalnos, Fire Elemental, Beast activation, Unleash, Coin, silence of Taunts, face attacks and Hunter power. Search is bounded at roughly 4,000 visited nodes and depth 18; extra loop work can occur while unwinding. Only the first action is emitted, and it must match a current concrete legal action.
4. **Ordinary decisions:** score development, trades, removal, healing, weapons, draw and class-specific resources. Score reflects health danger and available damage; large Overload can penalize a card that strands a next-turn play. The scores are initial heuristics, not tuned coefficients.
5. **Execution:** replan from the actual next state. Do not advance a private engine, predict unknown draws, read opponent files or commit to a stale multi-action plan. Errors go to stderr; stdout is one JSON message. Phase-specific legal fallbacks keep the session alive.

The CLI reads only its local state/history/deck plus the permitted `hs_arena` catalog. An optional state argument must resolve inside the skill folder. The client uses the arena-provided stdio MCP command, not an internet connection. Runtime package files are not edited.

## Deck-specific implementation

### Burst Shaman

- Searches buff-before-swing Doomhammer lines, including actual remaining durability, prior attacks and replacement weapons. Equipping another Doomhammer does not reset attacks used.
- Public current-turn history establishes Windfury attack counts. Without a known turn boundary, the planner counts only one currently available existing attack and avoids claiming a new-weapon multi-swing line. This may miss a lethal rather than inventing a second attack.
- Searches Al'Akir/Rockbiter and Thalnos/burn lines without assuming discounted or historical mana costs. Unknown draws and Far Sight outcomes are never searched.
- Accounts for current Spell Damage in damage spells, uses Lightning Storm's minimum roll for its immediate valuation, and penalizes Overload including blocked future curve plays.
- Values Hex, Earth Shock and Owl-style silence differently from ordinary damage. Hex's Frog is not treated as an opened path in lethal search; silence can remove a Taunt.
- Distinguishes early Unbound development, Feral Spirit defense, Mana Tide refill and direct finishers. Healing, face reach, weapon replacement cost and opposing board pressure influence action scores.

### Infernal Warlock

- Distinguishes the Inferno hero-power ID from ordinary Life Tap. It will not apply Life Tap's low-health restriction to summoning an Infernal.
- Life Tap considers health, visible incoming attack, hand cap and empty-deck fatigue. Jaraxxus is heavily rejected when visible attack plus a five-point safety margin reaches 15. This margin is a heuristic; it cannot prove safety from hidden burn.
- Evaluates Hellfire's friendly damage, rejects direct self-lethal, and considers the friendly cost of Nether and Shadowflame. A selected Shadowflame donor attacks face first when that attack is currently legal and no enemy secret is present, then the actual board is reassessed.
- Evaluates Farseer healing on the correct side, Siphon Soul's heal, Owl's loss of opposing text, Ooze's weapon removal, Drake's hand-scaled health and positional Sunfury/Argus effects.
- Values Sense Demons using our publicly available remaining-card counts and late-game Jaraxxus access. It does not inspect deck order or assume an immediate safe transformation.
- Doomsayer discourages friendly development into its pending clear; the score estimates whether visible enemy attack can remove it. Enemy answers from hand remain unknown.

### Pressure Hunter

- Uses actual available Beasts for Kill Command, including companion/Hound/Hyena tokens. No Beast means three base damage, not five.
- Searches a cheap Beast or Unleash before Kill Command when mana and board space permit; searches Hunter hero-power reach separately from minion attacks.
- Handles Houndmaster targets, Hyena/Unleash setup, Tracking selection, Highmane's persistent value, Bow durability and existing-weapon replacement costs.
- Evaluates secrets as conditional defense, without claiming their effects are immediate or guaranteed. Bow durability is read from the actual state after a reveal rather than invented when a secret is played.

## Known limits

This is **not full-turn board simulation**. The lethal search excludes general minion-trade sequences, draw outcomes, most aura changes and secret resolution. It refuses to certify a line with opposing secrets or hero immunity. Heuristic play can still attack into an unknown secret. Do not interpret the search as exhaustive or engine-verified lethal detection.

Scores approximate deathrattle value and next-turn danger; they do not resolve every deathrattle, removal chain or opponent response. There is no learned matchup model. The fixed Beast lookup covers the decks and relevant common tokens, not arbitrary generated/transformed card pools. Positional Taunt scoring considers adjacent bodies, but does not search every possible preceding trade or summon. Life Tap/Jaraxxus margins may be too conservative or too optimistic against particular opponents.

An output drawn from the current template should satisfy the public protocol, but stale-state relay errors, launcher failures, unexpected host behavior and gameplay mistakes remain possible. Three rejected actions still forfeit; no playbook can promise otherwise.

## Offline verification and validation incident

- 21 regression tests pass: legal parameter combinations, required targets, Windfury counts, replacement weapons, burst ordering, Beast-dependent damage, Taunt silence, healing, Inferno, self-damage, fatigue, donor sequencing, Argus positioning, mulligan, choice bounds, each deck card's score path, exact submissions and standalone CLI/path confinement.
- 189 saved public decision states evaluated by each of three packaged pilots: **567 decisions, 0 illegal outputs, 0 fallback errors**, maximum observed in-process decision time approximately **0.0046 seconds**. These are repeated offline decisions, not 567 games or 567 unique states. Most source states come from the previous Paladin/Mage/Zoo comparison, so tactical coverage for the new lists relies on the separate fixtures.
- All six skills pass official static loading; all deck lists pass official static deck validation; paired deck files and all three script copies match by hash. Python files compile without launching clients.
- **Validation incident:** the CLI `hs-arena validate` was mistakenly used without `--no-game`. It launched three local smoke attempts, one per scripted deck. Each exited at turn zero with a CLI login error: **0 completed games, 3 exit forfeits, 0 illegal actions, 0 timeouts**, no gameplay decision latency measured. The command path was stopped and not retried. These are infrastructure failures and provide no deck evidence. They violated the intended no-game workflow and are recorded rather than omitted.

Use `load_skill`/`validate_deck_data` or explicitly `hs-arena validate --no-game` for future static checks. Never assume bare `validate` is read-only validation.

## Commands for the separate evaluation owner — not executed here

Run from the repository root with the provided environment active. Substitute any of the three deck names for `burst-shaman`.

```sh
# New script, no model; uses this folder's client.py and scripts/move.py.
hs-arena play --p1 client:decks/burst-shaman --p2 greedy

# Haiku relays that same new script.
hs-arena play --p1 skill:decks/burst-shaman --p2 greedy

# Haiku chooses moves using the conceptual guide, with the same 30 cards.
hs-arena play --p1 skill:research/haiku-skills/burst-shaman --p2 greedy

# Generic arena greedy baseline with the same 30 cards, not our script.
hs-arena play --p1 greedy:decks/burst-shaman/deck.json --p2 greedy

# Offline only; neither command starts a match or calls a model.
PYTHONDONTWRITEBYTECODE=1 python research/tests/test_candidate_pilots.py
PYTHONDONTWRITEBYTECODE=1 python research/tests/check_candidate_pilots.py
```

Do not use `tools/fastsim.py --deck ...` to claim these new scripts were evaluated: that tool imports `player/scripts/move.py` and only changes the deck. Use the supplied clients, or explicitly adapt a separate evaluation harness to import each candidate's `decide` function.

Compare fixed lists under separately labelled pilots, balance actual first player across fresh seeds, and record wins, forfeits, illegal actions and full state-to-action latency. Model relay overhead is not captured by the millisecond offline measurements. No promotion or course submission should follow from static checks alone.
