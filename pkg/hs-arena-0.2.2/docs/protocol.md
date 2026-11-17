# hs-arena protocol reference

Protocol version **1** · card pool `basic-classic-1` · runtime 0.2.2

> **Students: you do not implement this protocol.** You submit a skill, and the course agent plays it through the
> seat's game MCP server (README, "Writing a skill"). What you need from this document is the **format of the
> data** your skill sees: before every decision the skill seat writes the pending `state.json` (section 5, with
> the legal-action templates of section 6) to `game/state.json` in the agent's folder, every event the seat has
> been shown to `game/history.jsonl` (one section 8 event per line), and the agent submits one action object of
> section 7 with the `act` tool (`act` takes the `seq` separately, so the object is just `{"type": ...}`).
> Rejected actions carry the error codes of section 9. Sections 1-4, 10, 11, 13 and 15 describe the file
> protocol that the course's seats and bots use internally.

This is the normative description of how the hs-arena runtime talks to an agent. The JSON Schemas shipped inside
the package are normative as well: `hs_arena/schemas/{state,action,manifest,game,result}.schema.json` (load them
with `hs_arena.protocol.load_schema("state")` etc.). Every entry of `state.events` and every line of
`replay.jsonl` follows `state.schema.json#/$defs/event`. All complete examples in this document are real files
from games (some trimmed for length) and are validated against the schemas by the test suite.

If you write your agent in Python with the SDK (`hs_arena.sdk.run`), sections 1-4 are implemented for you. You
still need sections 5-11 to understand what you receive and what you may answer.

Conventions used everywhere:

- All files are UTF-8 JSON without BOM, `\n` line endings; non-ASCII characters appear unescaped.
- Entity ids (`entity_id`, `card`, `attacker`, `target`, `choose`, option ids) are positive JSON **integers**,
  unique and stable within one game. `"88"` or `true` is not an entity id.
- Card ids (`card_id`) are strings such as `"CS2_029"`. Tokens, Choose One options, transformed minions and The
  Coin have card ids that are not in `cards.json` (for example `GAME_005` The Coin, `skele21` Damaged Golem,
  `EX1_160a`, `EX1_165t2`). Always use the inline `name` and `text` of the state.
- `player` is `1` or `2`.

Contents:
[1 Model](#1-model) ·
[2 Game directory](#2-game-directory) ·
[3 Process launch](#3-process-launch) ·
[4 Handshake](#4-handshake) ·
[5 state.json](#5-statejson) ·
[6 legal_actions](#6-legal_actions-action-templates) ·
[7 action.json](#7-actionjson) ·
[8 Events](#8-events) ·
[9 Validation and error codes](#9-validation-and-error-codes) ·
[10 Failure handling](#10-failure-handling) ·
[11 Game over](#11-game-over-and-process-shutdown) ·
[12 game.json and result.json](#12-gamejson-and-resultjson) ·
[13 manifest.json and deck.json](#13-manifestjson-and-deckjson) ·
[14 Windows and WSL](#14-windows-and-wsl-notes) ·
[15 Other languages](#15-writing-an-agent-in-another-language)

## 0. MCP deck submission (skill, client and external MCP seats)

Both seats first receive `phase: "deck_submission"`, `turn: 0`, and their own `seq: 1` concurrently. The
engine is not created yet. `you`, `opponent` and `choice` are null; `deck_rules` contains `pool_version`,
`hero_classes`, `deck_size` (30), `max_copies` (2) and `max_legendary_copies` (1). The complete allowed
card catalog is in `game/card_pool.json` (id -> card data); the host never reads a student's deck.json.
The agent follows its skill to build a deck, optionally dynamically or randomly, and calls `act` with:

```json action
{
  "seq": 1,
  "action": {
    "type": "submit_deck", "hero_class": "MAGE",
    "cards": [
      "NEW1_012", "NEW1_012", "EX1_608", "EX1_608", "CS2_024", "CS2_024", "EX1_277", "EX1_277", "CS2_023",
      "CS2_023", "EX1_012", "EX1_556", "EX1_556", "CS2_182", "CS2_182", "CS2_033", "CS2_033", "CS2_029",
      "CS2_029", "CS2_022", "CS2_022", "CS2_179", "CS2_179", "EX1_028", "EX1_028", "CS2_200", "CS2_200",
      "EX1_067", "EX1_067", "CS2_032"
    ]
  }
}
```

`hero_class` is case-insensitive. Card ids are strings, not game entity ids. The normal pool, class, size,
blacklist and duplicate-copy rules are enforced. A rejected submission returns `INVALID_DECK` with specific
validation errors in `last_action_result`, increments illegal_count, and requests a corrected deck with a new
seq. Other actions during setup return `WRONG_PHASE`; `concede` is allowed. The first timeout, first early
exit and third-illegal-action forfeits also apply during setup. The first accepted class/card list is immutable for
that game. A second submit_deck during mulligan/main/choice returns WRONG_PHASE.

Neither agent sees the opponent's deck or class during setup. After both decks are valid the host creates
the seeded engine; P1 then P2 mulligan (normally seq 2), followed by the randomly chosen first player.
`game_start` appears with the first mulligan, not at deck submission. A successful deck action counts in
`result.decisions`; replay contains `deck_submitted` with only the player's index. Before a successful setup,
game.json has null class/deck for unsubmitted seats. If setup ends early, both receive game_over with
null you/opponent, and result.first_player is null because no engine or first player existed.

For externally managed subagents, use `--p1 mcp:<fresh-workspace1> --p2 mcp:<fresh-workspace2> --games 1`.
Each agent's stdio server is `python -m hs_arena.skill.mcp_server <workspace>/arena-mailbox`. The host
reads no SKILL.md and launches no agent in this mode; the orchestrator supplies the skill and lifecycle.
Existing skill: and client: modes are optional local launchers. Built-in bots and legacy manifest.json
process agents already have host-configured decks and skip deck_submission; sections 1–4 describe that
legacy process transport. MCP uses the same seq/action semantics through wait / act / history.

## 1. Model

- **One persistent process per player per game.** The runtime starts both agent processes when the game starts
  (before the first state is written) and kills them after the game is over. Memory is simply process state.
  Every game is a new process; nothing persists between games.
- **Two files per player.** The runtime writes `state.json`, the agent answers with `action.json`. Nothing else
  is exchanged: the agent's stdin is the null device and its stdout is discarded.
- **Only the pending player is addressed.** A new `state.json` is written only to the player whose decision is
  pending. The other process keeps running and simply sees no new state (it may think ahead). Everything that
  happened in the meantime arrives as `events` in your next state.
- **`seq`.** Every `state.json` written to a player carries a new `seq`: 1, 2, 3, ... per player, incremented for
  every state including re-issued decisions and the final `game_over` state. An `action.json` must echo the `seq`
  of the state it answers.
- **Atomic writes.** Write the complete content to a temporary file *in the same directory*, then rename it onto
  the final name with an atomic replace (`os.replace()` in Python). The runtime writes `state.json.tmp` and
  replaces `state.json`; agents should write `action.json.tmp` and replace `action.json` (the SDK does exactly
  this). Never write `action.json` in place. As a safety net for writers that are not atomic, an `action.json`
  that does not parse only counts as `BAD_JSON` after its content has stayed unchanged for 1 s.
- **Polling, no file watchers.** Both sides poll with a short sleep: the runtime every 50 ms, the SDK every 50 ms
  by default. Detect a new state by a `seq` greater than the last one you handled, not by modification time or
  file existence: `state.json` is replaced, never deleted, during the game.
- The runtime deletes `action.json` right after reading it. Agents never delete or modify `state.json`.

## 2. Game directory

`hs-arena play` creates one directory per game under `--out` (default `./games`). The game id is
`g_<YYYYMMDD>_<NNNNNN>` (UTC date; the counter continues after the highest id already present in `--out`).

```text
<out>/<game_id>/
├── game.json            players, decks, versions, seed (public)
├── replay.jsonl         public event stream, one event per line, appended while the game runs
├── result.json          outcome, written at the end
├── engine_errors.log    only when the game was voided by an engine error
├── p1/
│   ├── state.json       runtime -> agent 1 (atomic replace); the final game_over state stays here
│   ├── action.json      agent 1 -> runtime (atomic replace); deleted by the runtime after reading
│   ├── stderr.log       agent 1's stderr, capped at 512 KB, plus notes from the runtime
│   ├── work/            HS_WORK_DIR: private scratch space for this game; deleted after the game
│   └── decisions/       with --keep-decisions (default): 00001.state.json, 00001.action.json, ...
└── p2/                  same for player 2
```

- Built-in bots (`greedy`, `random`) run inside the runtime; their `pN/` directory stays empty.
- `decisions/<seq>.state.json` is a copy of every state written (including the final one).
  `decisions/<seq>.action.json` is a copy of every answer that reached action validation (section 9), reduced to
  the known fields of its action type. Answers rejected earlier (`BAD_JSON`, `SEQ_MISMATCH`), timeouts, exits and
  dropped late answers leave no action copy. Both copies are compact single-line JSON.
- `pN/` is private to player N (it contains your hand). `game.json` and `replay.jsonl` only contain public
  information (deck lists are public) and are the files meant to be shared as a replay.

## 3. Process launch

The runtime starts the command from `manifest.json` (section 13) roughly as
`subprocess.Popen(command, cwd=<submission dir>, env=..., stdin=DEVNULL, stdout=DEVNULL, stderr=PIPE)`:

- `command` is a list of strings, executed **without a shell** (no pipes, globbing, `&&` or `$VAR` expansion).
  The working directory is the absolute path of the submission directory, so relative script paths such as
  `agent.py` resolve against it.
- If `command[0]` is exactly `python` or `python3`, it is replaced by the interpreter that runs `hs-arena`
  (`sys.executable`). Your Python dependencies must therefore be installed in that environment. Any other first
  element is executed as given and looked up on `PATH` (for example `node`, `java`).
- The agent inherits the runtime's environment, except that every variable starting with `HS_` is removed and
  replaced by the runtime's own:

| Variable | Value |
|----------|-------|
| `HS_STATE_FILE` | absolute path of `pN/state.json` |
| `HS_ACTION_FILE` | absolute path of `pN/action.json` |
| `HS_WORK_DIR` | absolute path of `pN/work/`, a private scratch directory for this game |
| `HS_PLAYER` | `1` or `2` |
| `HS_GAME_ID` | the game id, e.g. `g_20261013_000001` |
| `HS_PROTOCOL_VERSION` | `1` |
| `OPENAI_BASE_URL`, `MODEL`, `QWEN_API_KEY` | passed through from the runtime's environment (when set there): your LLM endpoint, model name and key |
| `PYTHONUTF8=1`, `PYTHONUNBUFFERED=1` | always set, to avoid encoding and buffering surprises on Windows |

- **stdout is ignored**: print debugging is safe and never interferes with the protocol.
- **stderr is captured** into `pN/stderr.log`, at most 512 KB per game (`stderr_cap_kb`). Beyond the cap a line
  `[hs-arena] stderr.log size cap reached; further output discarded` is written and the rest is discarded; the
  agent is never blocked by its output. The runtime also writes its own notes there (failed launch, early exits).
- **Do not write into the submission directory.** The same submission may play several games at the same time
  (`--parallel`), each with its own process and work directory, sharing the code directory. Use `HS_WORK_DIR`
  for files; it is private to this game and is deleted when the game ends.
- The process runs in its own process group (Windows: a job object; POSIX: a new session). When the game ends
  the runtime kills the whole tree, including any child processes the agent started (section 11).
- If the command cannot be started at all (e.g. executable not found), the error is written to `stderr.log` and
  the decision counts as `AGENT_EXITED`; the runtime retries the launch for the re-issued decision (section 10).
- The decision clock starts when `state.json` is written. Interpreter start-up and imports of a freshly started
  process count against the first decision it has to answer.

## 4. Handshake

What an agent does (this is exactly the SDK's loop):

```text
last_seq = 0
loop:
    read state.json                        # missing or unparseable: sleep 50 ms and retry
    if state.seq <= last_seq: sleep 50 ms and retry
    last_seq = state.seq
    if state.phase == "game_over": exit (any exit code)
    action = decide(state)
    write {"seq": state.seq, "action": action} to action.json.tmp
    os.replace(action.json.tmp, action.json)
```

What the runtime does for each decision (state `seq = n` for player `i`):

```text
1. write state.json (seq n) atomically; start the decision clock (decision_timeout_s, default 180 s)
   (there is no automatic process restart)
2. poll action.json every 50 ms:
     file missing                         -> keep waiting
     content does not parse               -> once it has been unchanged for 1 s: delete it -> BAD_JSON
     content parses                       -> delete it, then:
         not an object, or seq not an integer   -> BAD_JSON
         seq <  n                               -> late answer to an old state: dropped silently, keep waiting
         seq >  n                               -> SEQ_MISMATCH
         "action" missing or not an object      -> BAD_JSON
         otherwise                              -> validate the action (section 9)
     agent process has exited             -> AGENT_EXITED (immediate forfeit, section 10)
     clock expired                        -> TIMEOUT (immediate forfeit)
3. accepted -> apply it; the next state (seq n+1) goes to whoever has to decide next (often you again)
   rejected -> illegal_count += 1; the SAME decision is re-issued to you as seq n+1 with last_action_result
```

Flow of a game:

- **Mulligan after setup.** MCP seats first submit decks (section 0). The first in-engine state of each player
  has `phase: "mulligan"` and `turn: 0`. Both players
  mulligan before turn 1; the runtime serves them one after the other, player 1 then player 2, independent of who
  goes first (the `game_start` event tells you `first_player`). The player going second is offered 4 cards and
  receives The Coin (`GAME_005`) after the mulligan.
- **Turns.** During your turn you receive consecutive states (each with `seq + 1`) until you send `end_turn` or
  the game ends. You receive no states during the opponent's turn; its events arrive in your next state.
- **Choices.** When a card creates a pending choice (in this pool: Tracking, "draw one of the top 3 cards"), the
  next state has `phase: "choice"` and only `choose` and `concede` are legal. *Choose One* cards (Druid) are not
  a choice phase: they are played with a single `play_card` action carrying `choose`.
- **Deadline.** Every state carries `timeout_s` and `deadline_epoch_s`. If no `action.json` with the pending
  `seq` has arrived by then, the runtime records `TIMEOUT` and immediately ends the game with
  `forfeit_timeout`. Late answers cannot resume the game.
- **Game over.** The runtime writes a final state with `phase: "game_over"` and `result` to every player, waits
  up to `exit_grace_s` (10 s) for the process to exit and then kills its process tree (section 11).

## 5. state.json

`state.json` is rewritten for every decision. It contains the full current view of the game for you, the legal
action templates and the events since the previous state you received. The full history is **not** included:
keeping memory and managing your context is the agent's job.

### 5.1 Top-level fields

| Field | Type | Meaning |
|-------|------|---------|
| `protocol_version` | `"1"` | protocol version |
| `game_id` | string | the game id (same as `HS_GAME_ID`) |
| `seq` | integer ≥ 1 | this state's sequence number; echo it in `action.json` |
| `player` | `1` \| `2` | which player you are |
| `turn` | integer ≥ 0 | global turn counter: `0` during the mulligan, `1` = first player's first turn, `2` = second player's first turn, ... |
| `phase` | string | `"deck_submission"`, `"mulligan"`, `"main"`, `"choice"` or `"game_over"` |
| `timeout_s` | number | seconds you have for this decision (`decision_timeout_s`, default 180); in `game_over` the exit grace (10) |
| `deadline_epoch_s` | number | wall-clock deadline (Unix epoch seconds, runtime clock) by which `action.json` must be in place; computed just before the file is written, so it is slightly conservative. In `game_over`: when your process will be killed |
| `you` | object | your side, full information (5.2) |
| `opponent` | object | the opponent's side, public information only (5.2) |
| `choice` | object \| null | `{"kind": "mulligan", "source": null}` in the mulligan; `{"kind": "choice" \| "discover", "source": {entity_id, card_id, name} \| null}` in the choice phase (`source` is the card that created the choice); `null` otherwise |
| `legal_actions` | array | action templates (section 6); at least one in every phase except `game_over`, where it is empty |
| `events` | array | everything that happened since the previous state sent to **you**, in order, in your view (section 8) |
| `last_action_result` | object \| null | `null`, or the reason your previous answer was rejected: `{"accepted": false, "error": <code>, "message": <text>, "illegal_count": n, "illegal_limit": 3}`. Such a state re-issues the same decision |
| `result` | object \| null | `null` until `game_over`; then `{"winner": 1 \| 2 \| null, "you_won": true \| false \| null, "reason": <reason>}` (section 11) |

### 5.2 `you` and `opponent`

Both are null during deck_submission or game_over before the engine was created. During play they are
objects as below. The setup-only `deck_rules` field is described in section 0.

| Field | `you` | `opponent` | Meaning |
|-------|:-----:|:----------:|---------|
| `hero` | yes | yes | hero object (below) |
| `hero_power` | yes | yes | hero power object (below); the opponent's `usable` is always `false` |
| `weapon` | yes | yes | equipped weapon `{entity_id, card_id, name, attack, durability}` or `null` |
| `mana` | yes | yes | mana available right now; `0` for the player whose turn it is not (mana is only spent on your own turn, so the opponent's is always `0` while you decide; `max_mana` is their crystal count) |
| `max_mana` | yes | yes | mana crystals (0-10) |
| `overloaded` | yes | yes | crystals locked by Overload this turn |
| `overload_next_turn` | yes | yes | crystals that will be locked next turn |
| `hand` | yes | - | your hand, left to right (hand card objects) |
| `hand_size` | - | yes | number of cards in the opponent's hand |
| `board` | yes | yes | minions left to right; the index in this list is the board position |
| `secrets` | yes | - | your secrets in play: `{entity_id, card_id, name}` |
| `secrets_count` | - | yes | number of opponent secrets in play |
| `deck_remaining` | yes | yes | cards left in the deck |
| `deck_remaining_counts` | yes | - | `{card_id: count}` of the cards left in your deck (no order, zero counts omitted) |
| `fatigue` | yes | yes | fatigue counter: the next draw from an empty deck deals `fatigue + 1` damage |
| `graveyard` | yes | yes | `[{card_id, name}]` of that player's minions, spells and weapons that went to the graveyard, oldest first (tokens and The Coin included). Only cards that were in a hand or in play at some point are listed |

Hero object: `entity_id`, `card_id`, `name`, `hero_class` (`MAGE`, ...), `health` (can be ≤ 0 in the final
state), `max_health`, `armor`, `attack` (current attack, including weapon and buffs), `can_attack`, `frozen`,
`immune`.

Hero power object: `entity_id`, `card_id`, `name`, `cost`, `usable` (yours: a `hero_power` template is present
in `legal_actions`), `text`.

Minion object (both boards): `entity_id`, `card_id`, `name`, `attack`, `health` (current), `max_health`,
`can_attack` (it can attack right now; only meaningful for the side whose turn it is), `taunt`, `divine_shield`,
`frozen`, `stealth`, `windfury`, `charge`, `poisonous`, `deathrattle` (has a deathrattle), `spell_damage`
(integer), `silenced`, `text` (the printed card text; when `silenced` is true the minion has lost it, and it stays
here for reference only). The printed text also keeps keywords the minion has lost without a Silence: a popped
Divine Shield or a Stealth broken by attacking. The flags (`divine_shield`, `stealth`) are the current truth;
`to_text()` adds `(Divine Shield already lost)` / `(Stealth already lost)` after the text in that case.

Hand card object: `entity_id`, `card_id`, `name`, `type` (`MINION`, `SPELL` or `WEAPON`), `cost` (current cost,
including modifiers), `attack` and `health` (minions), `attack` and `durability` (weapons), `text`, `playable`
(a `play_card` template for it is present in `legal_actions`).

Card `text` is plain text (markup and `$`/`#` markers removed) and is inline for every visible card;
`hs_arena/data/cards.json` (`hs_arena.cards.load()`) has the whole pool for offline preprocessing.

### 5.3 Examples

Mulligan, first state of player 1 (complete file):

```json state
{
  "protocol_version": "1",
  "game_id": "g_20261013_000001",
  "seq": 1,
  "player": 1,
  "turn": 0,
  "phase": "mulligan",
  "timeout_s": 180.0,
  "deadline_epoch_s": 1791915727.759,
  "you": {
    "hero": {
      "entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore", "hero_class": "MAGE", "health": 30,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 5, "card_id": "HERO_08bp", "name": "Fireblast", "cost": 2, "usable": false,
      "text": "Deal 1 damage."
    },
    "weapon": null,
    "mana": 0,
    "max_mana": 0,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand": [
      {
        "entity_id": 8, "card_id": "EX1_608", "name": "Sorcerer's Apprentice", "type": "MINION", "cost": 2,
        "attack": 3, "health": 2, "text": "Your spells cost (1) less.", "playable": false
      },
      {
        "entity_id": 21, "card_id": "CS2_033", "name": "Water Elemental", "type": "MINION", "cost": 4, "attack": 3,
        "health": 6, "text": "Freeze any character damaged by this minion.", "playable": false
      },
      {
        "entity_id": 20, "card_id": "CS2_182", "name": "Chillwind Yeti", "type": "MINION", "cost": 4, "attack": 4,
        "health": 5, "text": "", "playable": false
      }
    ],
    "board": [],
    "secrets": [],
    "deck_remaining": 27,
    "deck_remaining_counts": {
      "CS2_022": 2, "CS2_023": 2, "CS2_024": 2, "CS2_029": 2, "CS2_032": 1, "CS2_033": 1, "CS2_179": 2,
      "CS2_182": 1, "CS2_200": 2, "EX1_012": 1, "EX1_028": 2, "EX1_067": 2, "EX1_277": 2, "EX1_556": 2,
      "EX1_608": 1, "NEW1_012": 2
    },
    "fatigue": 0,
    "graveyard": []
  },
  "opponent": {
    "hero": {
      "entity_id": 37, "card_id": "HERO_08", "name": "Jaina Proudmoore", "hero_class": "MAGE", "health": 30,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 38, "card_id": "HERO_08bp", "name": "Fireblast", "cost": 2, "usable": false,
      "text": "Deal 1 damage."
    },
    "weapon": null,
    "mana": 0,
    "max_mana": 0,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand_size": 4,
    "board": [],
    "secrets_count": 0,
    "deck_remaining": 26,
    "fatigue": 0,
    "graveyard": []
  },
  "choice": {"kind": "mulligan", "source": null},
  "legal_actions": [{"type": "mulligan", "options": [8, 21, 20], "min": 0, "max": 3}, {"type": "concede"}],
  "events": [{"event": "game_start", "first_player": 1}],
  "last_action_result": null,
  "result": null
}
```

Main phase (player 2, Druid, turn 18; two of the five hand cards and their templates removed for length). Note the
Choose One template for Starfall, the attack limited to the Taunt minion Misha, the opponent's draw without card
id and your own draw with card id:

```json state
{
  "protocol_version": "1",
  "game_id": "g_20261013_000004",
  "seq": 24,
  "player": 2,
  "turn": 18,
  "phase": "main",
  "timeout_s": 180.0,
  "deadline_epoch_s": 1791915753.183,
  "you": {
    "hero": {
      "entity_id": 37, "card_id": "HERO_06", "name": "Malfurion Stormrage", "hero_class": "DRUID", "health": 15,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 38, "card_id": "HERO_06bp", "name": "Shapeshift", "cost": 2, "usable": true,
      "text": "+1 Attack this turn. +1 Armor."
    },
    "weapon": null,
    "mana": 9,
    "max_mana": 9,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand": [
      {
        "entity_id": 62, "card_id": "CS2_172", "name": "Bloodfen Raptor", "type": "MINION", "cost": 2, "attack": 3,
        "health": 2, "text": "", "playable": true
      },
      {
        "entity_id": 55, "card_id": "NEW1_007", "name": "Starfall", "type": "SPELL", "cost": 5,
        "text": "Choose One - Deal 5 damage to a minion; or 2 damage to all enemy minions.", "playable": true
      },
      {
        "entity_id": 58, "card_id": "CS2_005", "name": "Claw", "type": "SPELL", "cost": 1,
        "text": "Give your hero +2 Attack this turn. Gain 2 Armor.", "playable": true
      }
    ],
    "board": [
      {
        "entity_id": 60, "card_id": "EX1_049", "name": "Youthful Brewmaster", "attack": 3, "health": 1,
        "max_health": 2, "can_attack": true, "taunt": false, "divine_shield": false, "frozen": false,
        "stealth": false, "windfury": false, "charge": false, "poisonous": false, "deathrattle": false,
        "spell_damage": 0, "silenced": false,
        "text": "Battlecry: Return a friendly minion from the battlefield to your hand."
      }
    ],
    "secrets": [],
    "deck_remaining": 17,
    "deck_remaining_counts": {
      "CS2_008": 1, "CS2_012": 2, "CS2_120": 1, "CS2_182": 2, "EX1_029": 1, "EX1_154": 2, "EX1_155": 2,
      "EX1_160": 2, "EX1_165": 2, "EX1_169": 2
    },
    "fatigue": 0,
    "graveyard": [
      {"card_id": "EX1_049", "name": "Youthful Brewmaster"}, {"card_id": "EX1_166", "name": "Keeper of the Grove"},
      {"card_id": "CS2_172", "name": "Bloodfen Raptor"}, {"card_id": "EX1_166", "name": "Keeper of the Grove"},
      {"card_id": "GAME_005", "name": "The Coin"}, {"card_id": "CS2_008", "name": "Moonfire"},
      {"card_id": "CS2_005", "name": "Claw"}, {"card_id": "NEW1_007", "name": "Starfall"}
    ]
  },
  "opponent": {
    "hero": {
      "entity_id": 4, "card_id": "HERO_05", "name": "Rexxar", "hero_class": "HUNTER", "health": 24,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 5, "card_id": "HERO_05bp", "name": "Steady Shot", "cost": 2, "usable": false,
      "text": "Deal 2 damage to the enemy hero."
    },
    "weapon": {"entity_id": 14, "card_id": "EX1_536", "name": "Eaglehorn Bow", "attack": 3, "durability": 2},
    "mana": 0,
    "max_mana": 9,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand_size": 1,
    "board": [
      {
        "entity_id": 22, "card_id": "EX1_534", "name": "Savannah Highmane", "attack": 6, "health": 5,
        "max_health": 5, "can_attack": false, "taunt": false, "divine_shield": false, "frozen": false,
        "stealth": false, "windfury": false, "charge": false, "poisonous": false, "deathrattle": true,
        "spell_damage": 0, "silenced": false, "text": "Deathrattle: Summon two 2/2 Hyenas."
      },
      {
        "entity_id": 33, "card_id": "CS2_182", "name": "Chillwind Yeti", "attack": 4, "health": 5, "max_health": 5,
        "can_attack": false, "taunt": false, "divine_shield": false, "frozen": false, "stealth": false,
        "windfury": false, "charge": false, "poisonous": false, "deathrattle": false, "spell_damage": 0,
        "silenced": false, "text": ""
      },
      {
        "entity_id": 84, "card_id": "NEW1_032", "name": "Misha", "attack": 4, "health": 1, "max_health": 4,
        "can_attack": false, "taunt": true, "divine_shield": false, "frozen": false, "stealth": false,
        "windfury": false, "charge": false, "poisonous": false, "deathrattle": false, "spell_damage": 0,
        "silenced": false, "text": "Taunt"
      }
    ],
    "secrets_count": 1,
    "deck_remaining": 15,
    "fatigue": 0,
    "graveyard": [
      {"card_id": "CS2_172", "name": "Bloodfen Raptor"}, {"card_id": "EX1_049", "name": "Youthful Brewmaster"},
      {"card_id": "DS1_175", "name": "Timber Wolf"}, {"card_id": "DS1_185", "name": "Arcane Shot"},
      {"card_id": "DS1_184", "name": "Tracking"}, {"card_id": "EX1_029", "name": "Leper Gnome"},
      {"card_id": "EX1_539", "name": "Kill Command"}, {"card_id": "NEW1_031", "name": "Animal Companion"}
    ]
  },
  "choice": null,
  "legal_actions": [
    {"type": "play_card", "card": 62, "targets": null, "positions": [0, 1], "choose": null},
    {
      "type": "play_card",
      "card": 55,
      "targets": null,
      "positions": null,
      "choose": [
        {
          "entity_id": 72, "card_id": "NEW1_007a", "name": "Stellar Drift",
          "text": "Deal 2 damage to all enemy minions.", "targets": null
        },
        {
          "entity_id": 73, "card_id": "NEW1_007b", "name": "Starlord", "text": "Deal 5 damage to a minion.",
          "targets": [22, 33, 60, 84]
        }
      ]
    },
    {"type": "play_card", "card": 58, "targets": null, "positions": null, "choose": null},
    {"type": "attack", "attacker": 60, "targets": [84]},
    {"type": "hero_power", "targets": null},
    {"type": "end_turn"},
    {"type": "concede"}
  ],
  "events": [
    {"event": "end_turn", "player": 2},
    {"event": "turn_start", "turn": 17, "player": 1},
    {"event": "draw", "player": 1},
    {
      "event": "attack",
      "player": 1,
      "attacker": {"entity_id": 25, "card_id": "DS1_175", "name": "Timber Wolf"},
      "target": {"entity_id": 60, "card_id": "EX1_049", "name": "Youthful Brewmaster"}
    },
    {
      "event": "damage",
      "player": 2,
      "entity_id": 60,
      "card_id": "EX1_049",
      "name": "Youthful Brewmaster",
      "amount": 1,
      "health_after": 1,
      "source": {"entity_id": 25, "card_id": "DS1_175", "name": "Timber Wolf"}
    },
    {
      "event": "damage",
      "player": 1,
      "entity_id": 25,
      "card_id": "DS1_175",
      "name": "Timber Wolf",
      "amount": 3,
      "health_after": -2,
      "source": {"entity_id": 60, "card_id": "EX1_049", "name": "Youthful Brewmaster"}
    },
    {"event": "death", "player": 1, "entity_id": 25, "card_id": "DS1_175", "name": "Timber Wolf"},
    {
      "event": "play_card", "player": 1, "card_id": "EX1_534", "name": "Savannah Highmane", "entity_id": 22,
      "cost": 6, "target": null, "position": 0, "choose": null
    },
    {"event": "end_turn", "player": 1},
    {"event": "turn_start", "turn": 18, "player": 2},
    {"event": "draw", "player": 2, "card_id": "CS2_005", "entity_id": 58}
  ],
  "last_action_result": null,
  "result": null
}
```

Choice phase created by Tracking (player 1, Hunter; two hand cards removed for length):

```json state
{
  "protocol_version": "1",
  "game_id": "g_20261013_000001",
  "seq": 6,
  "player": 1,
  "turn": 4,
  "phase": "choice",
  "timeout_s": 180.0,
  "deadline_epoch_s": 1791915749.624,
  "you": {
    "hero": {
      "entity_id": 4, "card_id": "HERO_05", "name": "Rexxar", "hero_class": "HUNTER", "health": 29,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 5, "card_id": "HERO_05bp", "name": "Steady Shot", "cost": 2, "usable": false,
      "text": "Deal 2 damage to the enemy hero."
    },
    "weapon": null,
    "mana": 1,
    "max_mana": 2,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand": [
      {
        "entity_id": 30, "card_id": "CS2_120", "name": "River Crocolisk", "type": "MINION", "cost": 2, "attack": 2,
        "health": 3, "text": "", "playable": false
      },
      {
        "entity_id": 15, "card_id": "EX1_536", "name": "Eaglehorn Bow", "type": "WEAPON", "cost": 3, "attack": 3,
        "durability": 2, "text": "Whenever a friendly Secret is revealed, gain +1 Durability.", "playable": false
      },
      {
        "entity_id": 18, "card_id": "EX1_539", "name": "Kill Command", "type": "SPELL", "cost": 3,
        "text": "Deal 3 damage. If you control a Beast, deal 5 damage instead.", "playable": false
      }
    ],
    "board": [],
    "secrets": [],
    "deck_remaining": 24,
    "deck_remaining_counts": {
      "CS2_120": 1, "CS2_172": 2, "CS2_182": 1, "DS1_070": 2, "DS1_175": 2, "DS1_184": 1, "DS1_185": 2,
      "EX1_029": 2, "EX1_049": 2, "EX1_534": 1, "EX1_536": 1, "EX1_539": 1, "EX1_554": 1, "EX1_610": 1,
      "EX1_611": 2, "NEW1_031": 2
    },
    "fatigue": 0,
    "graveyard": [{"card_id": "GAME_005", "name": "The Coin"}, {"card_id": "DS1_184", "name": "Tracking"}]
  },
  "opponent": {
    "hero": {
      "entity_id": 37, "card_id": "HERO_06", "name": "Malfurion Stormrage", "hero_class": "DRUID", "health": 28,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": false, "immune": false
    },
    "hero_power": {
      "entity_id": 38, "card_id": "HERO_06bp", "name": "Shapeshift", "cost": 2, "usable": false,
      "text": "+1 Attack this turn. +1 Armor."
    },
    "weapon": null,
    "mana": 0,
    "max_mana": 2,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand_size": 3,
    "board": [
      {
        "entity_id": 79, "card_id": "EX1_160t", "name": "Panther", "attack": 3, "health": 2, "max_health": 2,
        "can_attack": false, "taunt": false, "divine_shield": false, "frozen": false, "stealth": false,
        "windfury": false, "charge": false, "poisonous": false, "deathrattle": false, "spell_damage": 0,
        "silenced": false, "text": ""
      }
    ],
    "secrets_count": 0,
    "deck_remaining": 25,
    "fatigue": 0,
    "graveyard": [{"card_id": "CS2_008", "name": "Moonfire"}, {"card_id": "EX1_160", "name": "Power of the Wild"}]
  },
  "choice": {"kind": "choice", "source": {"entity_id": 7, "card_id": "DS1_184", "name": "Tracking"}},
  "legal_actions": [
    {
      "type": "choose",
      "options": [
        {
          "entity_id": 25, "card_id": "DS1_175", "name": "Timber Wolf", "type": "MINION", "cost": 1, "attack": 1,
          "health": 1, "text": "Your other Beasts have +1 Attack."
        },
        {
          "entity_id": 35, "card_id": "EX1_029", "name": "Leper Gnome", "type": "MINION", "cost": 1, "attack": 1,
          "health": 1, "text": "Deathrattle: Deal 2 damage to the enemy hero."
        },
        {
          "entity_id": 6, "card_id": "DS1_184", "name": "Tracking", "type": "SPELL", "cost": 1,
          "text": "Look at the top 3 cards of your deck. Draw one and discard the others."
        }
      ],
      "min": 1,
      "max": 1
    },
    {"type": "concede"}
  ],
  "events": [
    {
      "event": "play_card", "player": 1, "card_id": "DS1_184", "name": "Tracking", "entity_id": 7, "cost": 1,
      "target": null, "position": null, "choose": null
    }
  ],
  "last_action_result": null,
  "result": null
}
```

Final state (player 1 lost; hand and boards trimmed). `legal_actions` is empty, `timeout_s` is the exit grace:

```json state
{
  "protocol_version": "1",
  "game_id": "g_20261013_000001",
  "seq": 20,
  "player": 1,
  "turn": 14,
  "phase": "game_over",
  "timeout_s": 10.0,
  "deadline_epoch_s": 1791915559.114,
  "you": {
    "hero": {
      "entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore", "hero_class": "MAGE", "health": -1,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": true, "immune": false
    },
    "hero_power": {
      "entity_id": 5, "card_id": "HERO_08bp", "name": "Fireblast", "cost": 2, "usable": false,
      "text": "Deal 1 damage."
    },
    "weapon": null,
    "mana": 0,
    "max_mana": 7,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand": [
      {
        "entity_id": 35, "card_id": "CS2_032", "name": "Flamestrike", "type": "SPELL", "cost": 7,
        "text": "Deal 4 damage to all enemy minions.", "playable": false
      }
    ],
    "board": [
      {
        "entity_id": 6, "card_id": "NEW1_012", "name": "Mana Wyrm", "attack": 2, "health": 3, "max_health": 3,
        "can_attack": false, "taunt": false, "divine_shield": false, "frozen": false, "stealth": false,
        "windfury": false, "charge": false, "poisonous": false, "deathrattle": false, "spell_damage": 0,
        "silenced": false, "text": "Whenever you cast a spell, gain +1 Attack."
      }
    ],
    "secrets": [],
    "deck_remaining": 20,
    "deck_remaining_counts": {
      "CS2_022": 2, "CS2_023": 2, "CS2_024": 1, "CS2_029": 1, "CS2_033": 1, "CS2_179": 1, "CS2_200": 2,
      "EX1_012": 1, "EX1_028": 2, "EX1_067": 2, "EX1_277": 2, "EX1_556": 2, "EX1_608": 1
    },
    "fatigue": 0,
    "graveyard": [
      {"card_id": "EX1_608", "name": "Sorcerer's Apprentice"},
      {"card_id": "CS2_179", "name": "Sen'jin Shieldmasta"}, {"card_id": "CS2_033", "name": "Water Elemental"},
      {"card_id": "CS2_029", "name": "Fireball"}, {"card_id": "CS2_024", "name": "Frostbolt"}
    ]
  },
  "opponent": {
    "hero": {
      "entity_id": 37, "card_id": "HERO_08", "name": "Jaina Proudmoore", "hero_class": "MAGE", "health": 26,
      "max_health": 30, "armor": 0, "attack": 0, "can_attack": false, "frozen": true, "immune": false
    },
    "hero_power": {
      "entity_id": 38, "card_id": "HERO_08bp", "name": "Fireblast", "cost": 2, "usable": false,
      "text": "Deal 1 damage."
    },
    "weapon": null,
    "mana": 1,
    "max_mana": 7,
    "overloaded": 0,
    "overload_next_turn": 0,
    "hand_size": 4,
    "board": [
      {
        "entity_id": 52, "card_id": "CS2_182", "name": "Chillwind Yeti", "attack": 4, "health": 2, "max_health": 5,
        "can_attack": false, "taunt": false, "divine_shield": false, "frozen": false, "stealth": false,
        "windfury": false, "charge": false, "poisonous": false, "deathrattle": false, "spell_damage": 0,
        "silenced": false, "text": ""
      },
      {
        "entity_id": 63, "card_id": "EX1_028", "name": "Stranglethorn Tiger", "attack": 5, "health": 2,
        "max_health": 5, "can_attack": true, "taunt": false, "divine_shield": false, "frozen": false,
        "stealth": false, "windfury": false, "charge": false, "poisonous": false, "deathrattle": false,
        "spell_damage": 0, "silenced": false, "text": "Stealth"
      }
    ],
    "secrets_count": 0,
    "deck_remaining": 17,
    "fatigue": 0,
    "graveyard": [
      {"card_id": "skele21", "name": "Damaged Golem"}, {"card_id": "GAME_005", "name": "The Coin"},
      {"card_id": "CS2_023", "name": "Arcane Intellect"}, {"card_id": "EX1_608", "name": "Sorcerer's Apprentice"},
      {"card_id": "EX1_556", "name": "Harvest Golem"}, {"card_id": "CS2_024", "name": "Frostbolt"},
      {"card_id": "CS2_029", "name": "Fireball"}
    ]
  },
  "choice": null,
  "legal_actions": [],
  "events": [
    {"event": "end_turn", "player": 1},
    {"event": "turn_start", "turn": 14, "player": 2},
    {"event": "draw", "player": 2},
    {
      "event": "play_card",
      "player": 2,
      "card_id": "CS2_024",
      "name": "Frostbolt",
      "entity_id": 44,
      "cost": 2,
      "target": {"entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore"},
      "position": null,
      "choose": null
    },
    {
      "event": "damage", "player": 1, "entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore", "amount": 3,
      "health_after": 9, "armor_absorbed": 0, "armor_after": 0, "source": {"entity_id": 44, "card_id": "CS2_024", "name": "Frostbolt"}
    },
    {
      "event": "play_card",
      "player": 2,
      "card_id": "CS2_029",
      "name": "Fireball",
      "entity_id": 57,
      "cost": 4,
      "target": {"entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore"},
      "position": null,
      "choose": null
    },
    {
      "event": "damage", "player": 1, "entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore", "amount": 6,
      "health_after": 3, "armor_absorbed": 0, "armor_after": 0, "source": {"entity_id": 57, "card_id": "CS2_029", "name": "Fireball"}
    },
    {
      "event": "attack",
      "player": 2,
      "attacker": {"entity_id": 52, "card_id": "CS2_182", "name": "Chillwind Yeti"},
      "target": {"entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore"}
    },
    {
      "event": "damage",
      "player": 1,
      "entity_id": 4,
      "card_id": "HERO_08",
      "name": "Jaina Proudmoore",
      "amount": 4,
      "health_after": -1,
      "source": {"entity_id": 52, "card_id": "CS2_182", "name": "Chillwind Yeti"}
    },
    {"event": "game_over", "winner": 2, "reason": "hero_death"}
  ],
  "last_action_result": null,
  "result": {"winner": 2, "you_won": false, "reason": "hero_death"}
}
```

A re-issued decision after a rejected answer only differs in `last_action_result` and the `illegal_action` event
(excerpt of a real state; the agent had sent `{"type": "play_card", "card": 35, "target": 4}` for a minion
without a battlecry target):

```jsonc
{
  "seq": 4, "phase": "main",
  "legal_actions": [
    {"type": "play_card", "card": 35, "targets": null, "positions": [0], "choose": null},
    {"type": "play_card", "card": 74, "targets": null, "positions": null, "choose": null},
    {"type": "end_turn"}, {"type": "concede"}
  ],
  "events": [{"event": "illegal_action", "player": 1, "error": "ILLEGAL_TARGET", "illegal_count": 2}],
  "last_action_result": {
    "accepted": false, "error": "ILLEGAL_TARGET",
    "message": "card 35 (Leper Gnome) takes no target; omit 'target' (got 4)",
    "illegal_count": 2, "illegal_limit": 3
  }
  // ... all other fields as usual
}
```

## 6. legal_actions (action templates)

Each entry of `legal_actions` is a template listing the allowed parameter values; you answer with **one**
concrete action built from one template. Templates avoid a cross-product explosion of positions × targets ×
options.

- The list is exact: every concrete action you can build from a template is legal, and nothing else is.
- `concede` is present in every phase except `game_over` and is always the last entry.
- Main phase order: one `play_card` per playable hand card (hand order), one `attack` per character that can
  attack and has at least one legal target (your hero first, then minions left to right), `hero_power` if usable,
  `end_turn`, `concede`.
- `targets: null` means the action takes **no** target: do not send `target`. A list means a target is
  **required** and must be one of the listed entity ids (sorted ascending). The list already accounts for Taunt,
  Stealth, Immune, "can't be targeted by spells or Hero Powers" and similar rules.
- `positions` is `null` for spells and weapons (do not send `position`). For minions it lists the insert indexes
  `0 .. len(board)`: 0 = leftmost; omit `position` to play the minion rightmost.
- `choose` is `null` unless the card is a *Choose One* card. Then the template's own `targets` is `null`, each
  option carries its own `targets`, and you must send exactly one option's `entity_id` as `choose` (plus a
  `target` from that option's list when it is not `null`). Only options that can be played right now are listed;
  for example Starfall's single-target option disappears when there is no minion to target.
- `hero_power` has the same `targets` semantics. The schema also allows an optional `choose` on it (Choose One
  hero powers); none of the nine default hero powers uses it.

| Template | Phase | Fields |
|----------|-------|--------|
| `play_card` | main | `card` (entity id in your hand), `targets`, `positions`, `choose` |
| `attack` | main | `attacker` (your hero or minion), `targets` (never empty) |
| `hero_power` | main | `targets` (and optionally `choose`) |
| `end_turn` | main | - |
| `concede` | deck_submission, mulligan, main, choice | - |
| `submit_deck` | deck_submission | no entity parameters; submit hero_class and cards (section 0) |
| `mulligan` | mulligan | `options` (entity ids of your starting hand), `min` (0), `max` (number of options) |
| `choose` | choice | `options` (card objects: `entity_id`, `card_id`, `name`, `type`, `cost`, `attack`/`health` for minions, `text`), `min`, `max` |

Real templates from games (partial snippets):

```jsonc
// phase "main"
{"type": "play_card", "card": 24, "targets": [4, 21, 37, 41, 50, 52], "positions": null, "choose": null}  // Fireball
{"type": "play_card", "card": 62, "targets": null, "positions": [0, 1], "choose": null}                   // a minion
{"type": "play_card", "card": 58, "targets": null, "positions": null, "choose": null}                    // Claw (untargeted spell)
{"type": "play_card", "card": 41, "targets": null, "positions": [0, 1],                                  // Keeper of the Grove
 "choose": [{"entity_id": 97, "card_id": "EX1_166a", "name": "Moonfire", "text": "Deal 2 damage.", "targets": [4, 22, 37, 64]},
            {"entity_id": 98, "card_id": "EX1_166b", "name": "Dispel", "text": "Silence a minion.", "targets": [22, 64]}]}
{"type": "attack", "attacker": 21, "targets": [37, 41, 50, 52]}
{"type": "hero_power", "targets": [4, 21, 37, 41, 50, 52]}                                               // Fireblast
{"type": "hero_power", "targets": null}                                                                  // Shapeshift
{"type": "end_turn"}
{"type": "concede"}
// phase "mulligan"
{"type": "mulligan", "options": [8, 21, 20], "min": 0, "max": 3}
// phase "choice"
{"type": "choose", "options": [{"entity_id": 25, "card_id": "DS1_175", "name": "Timber Wolf", "type": "MINION", "cost": 1,
                                "attack": 1, "health": 1, "text": "Your other Beasts have +1 Attack."}, ...], "min": 1, "max": 1}
```

## 7. action.json

```text
{"seq": <the seq of the state you answer>, "action": {"type": <action type>, ...fields of that type...}}
```

| Action type | Fields |
|-------------|--------|
| `play_card` | `card` (required); `target` (required if the template's targets, or the chosen option's targets, is a list; otherwise omit it or send `null`); `position` (minions only, optional: omitted or `null` = rightmost); `choose` (required if the template's `choose` is a list; otherwise omit it or send `null`) |
| `attack` | `attacker`, `target` (both required) |
| `hero_power` | `target` (same rule as for `play_card`); `choose` (only if the template has one) |
| `end_turn` | none |
| `concede` | none; legal in every phase, the opponent wins |
| `mulligan` | `replace`: entity ids from `options` to shuffle back into the deck (any number between `min` and `max`); optional: omitted, `null` or `[]` keeps the whole hand |
| `choose` | `options`: list of option entity ids, between `min` and `max` of them (Tracking: exactly one) |

Unknown extra fields (at the top level or inside `action`) are ignored and **never logged**: decision copies and
logs keep only the known fields of the action type. You cannot leak prompts or reasoning into any log file even
if you add them.

One complete file per action type (taken from the games of the examples above):

Mulligan: put back entity 8, keep the rest.

```json action
{"seq": 1, "action": {"type": "mulligan", "replace": [8]}}
```

Mulligan: keep everything (`replace` could also be omitted).

```json action
{"seq": 1, "action": {"type": "mulligan", "replace": []}}
```

Play a minion at position 0 (leftmost).

```json action
{"seq": 24, "action": {"type": "play_card", "card": 62, "position": 0}}
```

Play an untargeted spell (no `target`, no `position`).

```json action
{"seq": 24, "action": {"type": "play_card", "card": 58}}
```

Play a targeted spell (Fireball on entity 41).

```json action
{"seq": 9, "action": {"type": "play_card", "card": 24, "target": 41}}
```

Choose One: Starfall's option 73 (Starlord) needs a target; option 72 (Stellar Drift) does not.

```json action
{"seq": 24, "action": {"type": "play_card", "card": 55, "choose": 73, "target": 84}}
```

```json action
{"seq": 24, "action": {"type": "play_card", "card": 55, "choose": 72}}
```

Attack the Taunt minion 84 with minion 60.

```json action
{"seq": 24, "action": {"type": "attack", "attacker": 60, "target": 84}}
```

Hero power with a target (Fireblast) and without one (Shapeshift).

```json action
{"seq": 3, "action": {"type": "hero_power", "target": 37}}
```

```json action
{"seq": 24, "action": {"type": "hero_power"}}
```

End the turn; concede.

```json action
{"seq": 24, "action": {"type": "end_turn"}}
```

```json action
{"seq": 24, "action": {"type": "concede"}}
```

Pick one Tracking option.

```json action
{"seq": 6, "action": {"type": "choose", "options": [25]}}
```

Extra fields are allowed and dropped.

```json action
{"seq": 24, "action": {"type": "end_turn", "why": "nothing useful left"}, "notes": "ignored, never logged"}
```

## 8. Events

`state.events` contains the events since the previous state sent to you, in order, as **you** see them.
`replay.jsonl` contains all events of the game, one compact JSON object per line, in the **public** view. Both
use the same vocabulary. The public view hides what the opponent could not see:

- your draws: you get `card_id` and `entity_id`; everybody else gets `{"event": "draw", "player": n}`;
- your mulligan: you get `replaced_card_ids` and `drawn_card_ids`; everybody else only the count `replaced`;
- your pick in a choice (Tracking): you get `card_id` and `name`; everybody else only `{"event": "choose", "player": n}`;
- your secrets: you get the `play_card` event and `secret_played` with `card_id` and `name`; everybody else gets
  **no** `play_card` event for it, only `{"event": "secret_played", "player": n}`.

Everything else is identical in both views. `illegal_action` and `agent_failure` are public during play. `agent_restart` is a legacy event.
The first in-engine state of a player starts with `game_start` (player 2's first mulligan state also contains
player 1's public `mulligan` event). During deck submission a seat only receives its own retry events. A
process only receives the events from its first state on.

| Event | Fields | Notes |
|-------|--------|-------|
| `deck_submitted` | `player` | replay-only setup event; no class or card ids |
| `game_start` | `first_player` | first in-engine event, after deck submission |
| `turn_start` | `turn`, `player` | |
| `draw` | `player`; own view: `card_id`, `entity_id`; fatigue: `fatigue_damage` | a fatigue tick has `fatigue_damage` and no card; a `damage` event on the hero follows |
| `mulligan` | `player`, `replaced` (count); own view: `replaced_card_ids`, `drawn_card_ids` | |
| `play_card` | `player`, `card_id`, `name`, `entity_id`, `cost`, `target` (`{entity_id, card_id, name}` or `null`), `position` (minions: insert index; otherwise `null`), `choose` (`{card_id, name}` of the Choose One option or `null`) | own secrets: own view only |
| `choose` | `player`; own view: `card_id`, `name` | one per picked option of a choice phase |
| `hero_power` | `player`, `card_id`, `name`, `target` (ref or `null`) | |
| `attack` | `player`, `attacker` (ref), `target` (ref) | |
| `damage`, `heal` | `player` (controller of the damaged/healed character), `entity_id`, `card_id`, `name`, `amount` (≥ 1), `health_after` (can be ≤ 0), `source` (ref; omitted when there is no card source, e.g. fatigue); damage to a hero also: `armor_absorbed`, `armor_after` | heroes and minions. On a hero, armor takes damage first: `armor_absorbed` of the `amount` came off the armor (`0` without armor) and health dropped by `amount - armor_absorbed` |
| `armor_gained` | `player`, `entity_id`, `card_id`, `name` (the hero), `amount` (≥ 1), `armor_after`, `source` (ref, when a card caused it) | Armor Up!, Shield Block, Armorsmith, ... |
| `summon` | `player`, `entity_id`, `card_id`, `name` | a minion entered the board other than by being played from hand: tokens, deathrattle summons, transformation results; a stolen minion appears as a `summon` on its new controller's side |
| `death` | `player`, `entity_id`, `card_id`, `name` | minions only; a hero's death ends the game (`game_over`) |
| `divine_shield_lost` | `player`, `entity_id`, `card_id`, `name` | a minion's Divine Shield is gone: it absorbed a hit (that hit has no `damage` event, since no damage was dealt) or an effect removed it (Silence, Blood Knight) |
| `leave_board` | `player`, `entity_id`, `card_id`, `name` | a minion left the board without dying, e.g. returned to hand or transformed (Polymorph: `leave_board` of the old minion, then `summon` of the Sheep) |
| `secret_played` | `player`; own view: `card_id`, `name` | |
| `secret_revealed` | `player`, `card_id`, `name` | a secret left play (triggered or destroyed) |
| `weapon_equipped` | `player`, `card_id`, `name`, `attack`, `durability` | |
| `weapon_destroyed` | `player`, `card_id`, `name` | broken or replaced |
| `end_turn` | `player` | |
| `illegal_action` | `player`, `error` (error code), `illegal_count` | section 9 |
| `agent_failure` | `player`, `error` | first timeout or early exit; section 10 |
| `agent_restart` | `player`, `restart_count` | legacy replay event; not emitted by 0.2.2 |
| `game_over` | `winner` (`1`, `2` or `null`), `reason` | last event of every game |

"ref" is `{"entity_id", "card_id", "name"}`. Examples (one event object each, all from real games):

`game_start`, `turn_start`, `end_turn`:

```json event
{"event": "game_start", "first_player": 1}
```

```json event
{"event": "turn_start", "turn": 18, "player": 2}
```

```json event
{"event": "end_turn", "player": 1}
```

`draw`: own view, public view, fatigue tick (followed by a `damage` event without `source`):

```json event
{"event": "draw", "player": 2, "card_id": "CS2_005", "entity_id": 58}
```

```json event
{"event": "draw", "player": 1}
```

```json event
{"event": "draw", "player": 1, "fatigue_damage": 1}
```

```json event
{"event": "damage", "player": 1, "entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore", "amount": 1, "health_after": 29, "armor_absorbed": 0, "armor_after": 0}
```

`mulligan`: own view, public view:

```json event
{"event": "mulligan", "player": 1, "replaced": 1, "replaced_card_ids": ["EX1_608"], "drawn_card_ids": ["CS2_029"]}
```

```json event
{"event": "mulligan", "player": 1, "replaced": 1}
```

`play_card`: targeted spell, minion, Choose One minion with a target:

```json event
{"event": "play_card", "player": 1, "card_id": "CS2_029", "name": "Fireball", "entity_id": 24, "cost": 4, "target": {"entity_id": 41, "card_id": "EX1_608", "name": "Sorcerer's Apprentice"}, "position": null, "choose": null}
```

```json event
{"event": "play_card", "player": 1, "card_id": "EX1_534", "name": "Savannah Highmane", "entity_id": 22, "cost": 6, "target": null, "position": 0, "choose": null}
```

```json event
{"event": "play_card", "player": 2, "card_id": "EX1_166", "name": "Keeper of the Grove", "entity_id": 41, "cost": 4, "target": {"entity_id": 20, "card_id": "DS1_070", "name": "Houndmaster"}, "position": 1, "choose": {"card_id": "EX1_166b", "name": "Dispel"}}
```

`choose`: own view, public view:

```json event
{"event": "choose", "player": 1, "card_id": "CS2_172", "name": "Bloodfen Raptor"}
```

```json event
{"event": "choose", "player": 1}
```

`hero_power`, `attack`:

```json event
{"event": "hero_power", "player": 1, "card_id": "HERO_08bp", "name": "Fireblast", "target": {"entity_id": 37, "card_id": "HERO_08", "name": "Jaina Proudmoore"}}
```

```json event
{"event": "hero_power", "player": 2, "card_id": "HERO_06bp", "name": "Shapeshift", "target": null}
```

```json event
{"event": "attack", "player": 2, "attacker": {"entity_id": 41, "card_id": "EX1_608", "name": "Sorcerer's Apprentice"}, "target": {"entity_id": 4, "card_id": "HERO_08", "name": "Jaina Proudmoore"}}
```

`damage`, `heal`:

```json event
{"event": "damage", "player": 2, "entity_id": 37, "card_id": "HERO_08", "name": "Jaina Proudmoore", "amount": 1, "health_after": 29, "armor_absorbed": 0, "armor_after": 0, "source": {"entity_id": 5, "card_id": "HERO_08bp", "name": "Fireblast"}}
```

A 6-damage Fireball on a Warrior with 4 armor: the armor is gone and health drops by 2.

```json event
{"event": "damage", "player": 2, "entity_id": 37, "card_id": "HERO_01", "name": "Garrosh Hellscream", "amount": 6, "health_after": 28, "armor_absorbed": 4, "armor_after": 0, "source": {"entity_id": 24, "card_id": "CS2_029", "name": "Fireball"}}
```

`armor_gained` (hero power Armor Up!):

```json event
{"event": "armor_gained", "player": 2, "entity_id": 37, "card_id": "HERO_01", "name": "Garrosh Hellscream", "amount": 2, "armor_after": 2, "source": {"entity_id": 38, "card_id": "HERO_01bp", "name": "Armor Up!"}}
```

```json event
{"event": "heal", "player": 1, "entity_id": 4, "card_id": "HERO_09", "name": "Anduin Wrynn", "amount": 2, "health_after": 20, "source": {"entity_id": 10, "card_id": "CS1_112", "name": "Holy Nova"}}
```

`summon`, `death`, `leave_board`:

```json event
{"event": "summon", "player": 2, "entity_id": 71, "card_id": "skele21", "name": "Damaged Golem"}
```

```json event
{"event": "death", "player": 2, "entity_id": 41, "card_id": "EX1_608", "name": "Sorcerer's Apprentice"}
```

```json event
{"event": "leave_board", "player": 2, "entity_id": 83, "card_id": "EX1_165t2", "name": "Druid of the Claw"}
```

`secret_played` (own view, public view), `secret_revealed`:

```json event
{"event": "secret_played", "player": 1, "card_id": "EX1_610", "name": "Explosive Trap"}
```

```json event
{"event": "secret_played", "player": 1}
```

```json event
{"event": "secret_revealed", "player": 1, "card_id": "EX1_610", "name": "Explosive Trap"}
```

`weapon_equipped`, `weapon_destroyed`:

```json event
{"event": "weapon_equipped", "player": 1, "card_id": "EX1_536", "name": "Eaglehorn Bow", "attack": 3, "durability": 2}
```

```json event
{"event": "weapon_destroyed", "player": 1, "card_id": "EX1_536", "name": "Eaglehorn Bow"}
```

`illegal_action`, `agent_failure`, `game_over`:

```json event
{"event": "illegal_action", "player": 1, "error": "BAD_JSON", "illegal_count": 1}
```

```json event
{"event": "agent_failure", "player": 1, "error": "AGENT_EXITED"}
```

```json event
{"event": "game_over", "winner": 2, "reason": "hero_death"}
```

An example `replay.jsonl` ending at the third illegal action (public view):

```text
{"event":"game_start","first_player":2}
{"event":"illegal_action","player":1,"error":"WRONG_PHASE","illegal_count":1}
{"event":"mulligan","player":1,"replaced":0}
{"event":"mulligan","player":2,"replaced":2}
{"event":"turn_start","turn":1,"player":2}
{"event":"draw","player":2}
{"event":"end_turn","player":2}
{"event":"turn_start","turn":2,"player":1}
{"event":"draw","player":1}
{"event":"illegal_action","player":1,"error":"ILLEGAL_TARGET","illegal_count":2}
{"event":"illegal_action","player":1,"error":"BAD_JSON","illegal_count":3}
{"event":"game_over","winner":2,"reason":"forfeit_illegal"}
```

## 9. Validation and error codes

Each answer is checked in this order; the first failing check determines the error code:

1. **File** (process agents only): `action.json` parses (an unparseable file counts once it has been unchanged
   for 1 s) → `BAD_JSON`; it is an object with an integer `seq` → `BAD_JSON`; `seq` smaller than the pending
   one → dropped silently, no penalty; `seq` larger → `SEQ_MISMATCH`; `action` is an object → `BAD_JSON`.
2. **Type**: `action.type` is one of the action types → `UNKNOWN_ACTION_TYPE` (during setup, anything except
   submit_deck/concede is rejected as WRONG_PHASE).
3. **Phase**: the type is allowed in the current phase (deck_submission: `submit_deck`, `concede`;
   mulligan: `mulligan`, `concede`; choice: `choose`,
   `concede`; main: `play_card`, `attack`, `hero_power`, `end_turn`, `concede`) → `WRONG_PHASE`.
4. **References and engine rules**, per type:
   - `end_turn`, `concede`: always accepted in their phases (other fields are ignored).
   - `play_card`: `card` is a card in your hand → `NOT_YOUR_ENTITY`; it is playable now (a template exists) →
     `CARD_NOT_PLAYABLE`; Choose One: `choose` present → `CHOOSE_REQUIRED`, one of the option ids →
     `ILLEGAL_CHOICE`; `choose` sent for a card without options → `ILLEGAL_CHOICE`; target: present when required →
     `TARGET_REQUIRED`, one of the allowed ids → `ILLEGAL_TARGET`, absent when `targets` is `null` →
     `ILLEGAL_TARGET`; position: absent for non-minions → `ILLEGAL_POSITION`, one of `positions` →
     `ILLEGAL_POSITION`.
   - `attack`: `attacker` is your hero or one of your minions → `NOT_YOUR_ENTITY`; it can attack now →
     `CANNOT_ATTACK`; `target` present → `TARGET_REQUIRED`; allowed → `ILLEGAL_TARGET`.
   - `hero_power`: usable now → `HERO_POWER_UNUSABLE`; then `choose` and `target` as for `play_card`.
   - `mulligan`: `replace` (if present) is a list of integers without duplicates, all from `options`, with a
     length between `min` and `max` → `ILLEGAL_CHOICE`.
   - `choose`: `options` is a list of integers without duplicates, all option entity ids, with a length between
     `min` and `max` → `ILLEGAL_CHOICE`.
5. **Apply**: the engine executes the action. If the engine itself raises on an action that passed validation,
   the game is voided (section 10).

| Code | When |
|------|------|
| `BAD_JSON` | `action.json` is not valid JSON (and stayed unchanged for 1 s), is not an object, has no integer `seq`, or has no `action` object |
| `SEQ_MISMATCH` | `seq` is larger than the `seq` of the pending state |
| `WRONG_PHASE` | a known action type that is not allowed in the current phase (e.g. `end_turn` during the mulligan) |
| `UNKNOWN_ACTION_TYPE` | `type` missing, not a string, or not one of `play_card`, `attack`, `hero_power`, `end_turn`, `concede`, `mulligan`, `choose` |
| `NOT_YOUR_ENTITY` | `play_card.card` is not a card in your hand, or `attack.attacker` is not one of your characters (wrong id, opponent's entity, not an integer) |
| `CARD_NOT_PLAYABLE` | the card is in your hand but cannot be played now (not enough mana, board full, no valid target, ...) |
| `TARGET_REQUIRED` | the template (or the chosen option) has a `targets` list but no `target` was sent |
| `ILLEGAL_TARGET` | `target` is not in the allowed list, or a `target` was sent although `targets` is `null` |
| `ILLEGAL_POSITION` | `position` is not in `positions`, or a `position` was sent for a spell or weapon |
| `CHOOSE_REQUIRED` | a Choose One card (or hero power) was played without `choose` |
| `ILLEGAL_CHOICE` | `choose` is not one of the options or was sent for a card without options; invalid `mulligan.replace` or `choose.options` (not a list of ids, duplicates, unknown ids, wrong count) |
| `CANNOT_ATTACK` | the attacker is yours but cannot attack now (just played, already attacked, frozen, 0 attack, no legal target, ...) |
| `HERO_POWER_UNUSABLE` | the hero power cannot be used now (already used this turn, not enough mana, no valid target) |
| `AGENT_EXITED` | the agent process exited (or could not be started) before the game was over |
| `TIMEOUT` | no `action.json` with the pending `seq` arrived within `decision_timeout_s` |
| `INVALID_DECK` | submitted class/card list violates the card pool, class, 30-card size, blacklist or copy limits |

`message` in `last_action_result` is a human-readable explanation that names the offending value and the allowed
ones, e.g. `"action 'end_turn' is not allowed in phase 'mulligan'; allowed: ['mulligan', 'concede']"`.

## 10. Failure handling

- **Illegal actions.** Each rejected answer adds 1 to `illegal_count`, which never resets during a game.
  The default `illegal_limit` is 3 and is an inclusive threshold: the third illegal action forfeits immediately
  with `forfeit_illegal`. The first two re-issue the decision with a new seq and error feedback.
- **Timeout.** The first unanswered decision after 180 seconds forfeits immediately with `forfeit_timeout`.
  It increments `timeouts`, not `illegal_count`. There is no retry. The clock starts when the state is
  published, not when the agent reads it. Waiting for the opponent is not charged; `wait` cannot reset a clock.
- **Agent exit.** The first managed process/session exit before GAME OVER forfeits with `forfeit_exit`.
  No warning or automatic restart occurs. Timeouts and exits emit a public `agent_failure` event with
  `player` and `error` (`TIMEOUT` or `AGENT_EXITED`). Diagnostics remain available for staff review of
  verified infrastructure failures. Externally managed `mcp:` processes remain the orchestrator's
  responsibility; if they disappear without replying, their first unanswered decision times out and forfeits.
- **Engine errors void the game.** If the simulator raises while applying an action that passed validation (a
  card bug), the game is voided: `reason: "void_engine_error"`, `winner: null`, both agents get a final state,
  `result.json` gets `engine_error` with the exception message and the card ids involved, `engine_errors.log`
  gets the traceback, and the `play` summary lists the game as voided. Voided games do not count for anybody;
  the cards are candidates for `hs_arena/pool/blacklist.txt`.
- **Interrupted runtime.** If the runtime is interrupted (Ctrl+C), the game ends with `reason: "aborted"` and
  `winner: null`; agents still receive a final state.
- **Turn cap.** Off by default. With `--max-turns N` a game whose turn counter exceeds N ends as a draw with
  `reason: "max_turns"`.

## 11. Game over and process shutdown

- When the game ends, every player whose process was started gets a final state (`seq + 1`, also when it was not
  their decision) with `phase: "game_over"`, empty `legal_actions`, the last `events` (ending with `game_over`),
  `result` and, if the game ended because of your illegal action, the corresponding `last_action_result`.
  `timeout_s` is the exit grace (`exit_grace_s`, 10 s, `--exit-grace`) and `deadline_epoch_s` is when the process
  will be killed.
- Do not answer the final state; exit (the exit code is ignored). The SDK calls `on_game_over(result)` and
  returns from `run()`.
- After the grace period the runtime kills the agent's whole process tree (Windows: job object termination and
  `taskkill /T`; POSIX: `SIGTERM` to the process group, `SIGKILL` 0.5 s later). Child processes are killed even
  if the agent itself exited in time. Then `work/` is deleted; `state.json` (the final state) and `stderr.log`
  remain.

| `reason` | `winner` | When |
|----------|----------|------|
| `hero_death` | 1 or 2 | a hero died |
| `draw` | `null` | both heroes died at the same time |
| `concede` | the other player | a player sent `concede` |
| `forfeit_illegal` | the other player | a player's third illegal action |
| `forfeit_timeout` | the other player | the first decision timeout |
| `forfeit_exit` | the other player | the first early process/session exit |
| `forfeit_restart` | the other player | legacy replay reason; not emitted by 0.2.2 |
| `void_engine_error` | `null` | the engine crashed; the game does not count |
| `max_turns` | `null` | `--max-turns` was exceeded |
| `aborted` | `null` | the runtime was interrupted |

`you_won` in `result` is `true`/`false` when there is a winner and `null` otherwise.

The final state of the forfeiting player in a real game (excerpt):

```jsonc
{
  "seq": 7, "player": 2, "turn": 0, "phase": "game_over", "timeout_s": 10.0,
  "legal_actions": [],
  "events": [
    {"event": "illegal_action", "player": 2, "error": "UNKNOWN_ACTION_TYPE", "illegal_count": 3},
    {"event": "game_over", "winner": 1, "reason": "forfeit_illegal"}
  ],
  "last_action_result": {"accepted": false, "error": "UNKNOWN_ACTION_TYPE", "message": "unknown action type 'fly'; ...",
                         "illegal_count": 3, "illegal_limit": 3},
  "result": {"winner": 1, "you_won": false, "reason": "forfeit_illegal"}
  // ... you, opponent, ...
}
```

## 12. game.json and result.json

`game.json` is written when the game starts: `game_id`, `seed`, `created_at` (ISO 8601, UTC), `runtime_version`,
`protocol_version`, `pool_version`, `fireplace_commit`, `decision_timeout_s`, `illegal_limit` and `players`
(`index`, `name` from the skill's frontmatter, the client directory, the manifest or the bot name, `kind` =
`skill` | `client` | `process` | `greedy` | `random`, `hero_class`, `deck` = the 30 card ids).

```json game
{
  "game_id": "g_20261013_000001",
  "seed": 3,
  "created_at": "2026-10-13T18:19:07+00:00",
  "runtime_version": "0.1.0",
  "protocol_version": "1",
  "pool_version": "basic-classic-1",
  "fireplace_commit": "47a2572a000db66645bb74a425a090d51f1004fa",
  "decision_timeout_s": 180.0,
  "illegal_limit": 3,
  "players": [
    {
      "index": 1,
      "name": "random-example",
      "kind": "process",
      "hero_class": "MAGE",
      "deck": [
        "NEW1_012", "NEW1_012", "EX1_608", "EX1_608", "CS2_024", "CS2_024", "EX1_277", "EX1_277", "CS2_023",
        "CS2_023", "EX1_012", "EX1_556", "EX1_556", "CS2_182", "CS2_182", "CS2_033", "CS2_033", "CS2_029",
        "CS2_029", "CS2_022", "CS2_022", "CS2_179", "CS2_179", "EX1_028", "EX1_028", "CS2_200", "CS2_200",
        "EX1_067", "EX1_067", "CS2_032"
      ]
    },
    {
      "index": 2,
      "name": "greedy",
      "kind": "greedy",
      "hero_class": "MAGE",
      "deck": [
        "NEW1_012", "NEW1_012", "EX1_608", "EX1_608", "CS2_024", "CS2_024", "EX1_277", "EX1_277", "CS2_023",
        "CS2_023", "EX1_012", "EX1_556", "EX1_556", "CS2_182", "CS2_182", "CS2_033", "CS2_033", "CS2_029",
        "CS2_029", "CS2_022", "CS2_022", "CS2_179", "CS2_179", "EX1_028", "EX1_028", "CS2_200", "CS2_200",
        "EX1_067", "EX1_067", "CS2_032"
      ]
    }
  ]
}
```

`result.json` is written when the game is over:

| Field | Meaning |
|-------|---------|
| `game_id`, `seed` | as in `game.json` |
| `winner` | `1`, `2` or `null` |
| `reason` | see the table in section 11 |
| `first_player` | who took turn 1, or null when setup ended before the engine existed |
| `turns` | final value of the turn counter |
| `illegal_counts` | `{"1": n, "2": m}` illegal actions per player (including timeouts and exits) |
| `restarts` | legacy counter; always zero under the 0.2.2 rules |
| `timeouts` | timeouts per player |
| `duration_s` | wall-clock duration of the game (excluding the one-time card database load) |
| `decisions` | accepted actions per player |
| `players` | `[{index, name, kind}]` |
| `notes` | only when there are any: seat notes per player, e.g. `{"1": ["session 1 stopped before GAME OVER ...; game lost (forfeit_exit)."]}` (early-exit diagnostics) |
| `engine_error` | only for voided games: `{"message": "<ExceptionType>: <text>", "card_ids": [...]}` |

A normal game and a forfeit:

```json result
{
  "game_id": "g_20261013_000001",
  "seed": 3,
  "winner": 2,
  "reason": "hero_death",
  "first_player": 1,
  "turns": 14,
  "illegal_counts": {"1": 0, "2": 0},
  "restarts": {"1": 0, "2": 0},
  "timeouts": {"1": 0, "2": 0},
  "duration_s": 1.479,
  "decisions": {"1": 19, "2": 26},
  "players": [{"index": 1, "name": "random-example", "kind": "process"}, {"index": 2, "name": "greedy", "kind": "greedy"}]
}
```

```json result
{
  "game_id": "g_20261013_000001",
  "seed": 9,
  "winner": 1,
  "reason": "forfeit_illegal",
  "first_player": 2,
  "turns": 0,
  "illegal_counts": {"1": 0, "2": 6},
  "restarts": {"1": 0, "2": 0},
  "timeouts": {"1": 0, "2": 0},
  "duration_s": 0.513,
  "decisions": {"1": 1, "2": 0},
  "players": [{"index": 1, "name": "greedy", "kind": "greedy"}, {"index": 2, "name": "buggy", "kind": "process"}]
}
```

## 13. manifest.json and deck.json

A **legacy process-agent** directory needs `manifest.json` and `deck.json` at its root. Student skills instead
need SKILL.md; deck.json is an optional recipe consumed by the agent, never the host (section 0).

| `manifest.json` field | Rule |
|-----------------------|------|
| `protocol_version` | must be `"1"` |
| `pool_version` | must be `"basic-classic-1"` |
| `name` | 1-64 characters from letters, digits, `_`, `.`, `-`, starting with a letter or digit |
| `author` | non-empty string (your student id) |
| `command` | non-empty list of non-empty strings, run with the submission directory as cwd (section 3) |

Unknown fields produce a warning and are ignored.

```json manifest
{
  "protocol_version": "1",
  "pool_version": "basic-classic-1",
  "name": "frostbolt-enjoyer",
  "author": "U12345678",
  "command": ["python", "agent.py"]
}
```

```json manifest
{
  "protocol_version": "1",
  "pool_version": "basic-classic-1",
  "name": "node-example",
  "author": "U12345678",
  "command": ["node", "agent.js"]
}
```

`deck.json` has `hero_class` (`DRUID`, `HUNTER`, `MAGE`, `PALADIN`, `PRIEST`, `ROGUE`, `SHAMAN`, `WARLOCK` or
`WARRIOR`; case-insensitive) and `cards` (exactly 30 card ids). An optional `name` is allowed; an optional
`pool_version` must match the runtime's pool. Deck rules: every card is in the pool (`hs-arena cards`,
`docs/card_pool.md`); class cards only of your `hero_class`, plus NEUTRAL cards; at most 2 copies of a card; at
most 1 copy of a LEGENDARY card. Your hero is the class's default hero.

```jsonc
{"hero_class": "MAGE", "cards": ["NEW1_012", "NEW1_012", "EX1_608", "EX1_608", "CS2_024", "CS2_024", /* ... 30 ids */]}
```

## 14. Windows and WSL notes

- `os.replace` is atomic only within one volume: keep the temporary file in the same directory as the target
  (`action.json.tmp` next to `action.json`).
- On Windows, replacing or opening a file can fail with "access denied" (`PermissionError`) for a moment while the
  other side has it open. The runtime and the SDK retry for up to 5 s; agents in other languages should retry
  their rename and read too.
- Open every JSON file as UTF-8 explicitly (`encoding="utf-8"` in Python); the Windows default code page is not
  UTF-8. The runtime sets `PYTHONUTF8=1` for agents.
- Keep the arena at a short path such as `C:\arena`: the vendored engine has deep package paths and the classic
  260-character path limit can bite when the installation or the game directories live deep in your profile.
  Enabling long paths (registry value `LongPathsEnabled`, see the README) removes the limit.
- WSL: keep the project and the game directories on the Linux file system (e.g. `~/arena`), not under `/mnt/c`.
  Polling and atomic renames on the Windows drive mounted into WSL are much slower.
- Files are identical on both sides (UTF-8, `\n`): a game directory written on Windows can be read with
  `hs-arena replay` in WSL and vice versa.

## 15. Writing an agent in another language

Python is the supported language (the SDK is provided), but the only interface is the file protocol: any program
that polls `HS_STATE_FILE`, writes `HS_ACTION_FILE` atomically with the right `seq` and exits on `game_over` is
a valid agent. Checklist:

1. Read the paths from `HS_STATE_FILE`, `HS_ACTION_FILE` and `HS_WORK_DIR`; never hard-code them.
2. Poll `state.json` every ~50 ms; treat a missing or unparseable file as "not yet"; act only when `seq` is larger
   than the last one you handled.
3. Exit when `phase` is `game_over`.
4. Build the action from one template of `legal_actions`, following section 7 exactly (`target`, `position` and
   `choose` only where the template allows them).
5. Write `{"seq": ..., "action": ...}` to `action.json.tmp` and rename it onto `action.json`; retry the rename
   briefly on Windows "access denied" errors.
6. Write logs to stderr or `HS_WORK_DIR`, never into your submission directory.
7. Put the interpreter or binary in `manifest.json` `command`, e.g. `["node", "agent.js"]`. It must be available
   on the machine that runs the game.

A complete Node.js agent that plays the first legal action (protocol demo only, no LLM):

```js
// agent.js - minimal hs-arena agent without the Python SDK
const fs = require("fs");
const STATE = process.env.HS_STATE_FILE, ACTION = process.env.HS_ACTION_FILE;
let lastSeq = 0;

function readState() {
  try { return JSON.parse(fs.readFileSync(STATE, "utf8")); } catch { return null; }  // missing or mid-replace
}

function writeAction(obj) {
  const tmp = ACTION + ".tmp";
  fs.writeFileSync(tmp, JSON.stringify(obj), "utf8");
  for (let i = 0; ; i++) {
    try { fs.renameSync(tmp, ACTION); return; }          // atomic replace (MoveFileEx on Windows)
    catch (e) { if (i > 100) throw e; Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 20); }
  }
}

function decide(state) {
  const t = state.legal_actions.find((a) => a.type !== "concede");
  switch (t.type) {
    case "mulligan": return { type: "mulligan", replace: [] };
    case "choose": return { type: "choose", options: [t.options[0].entity_id] };
    case "attack": return { type: "attack", attacker: t.attacker, target: t.targets[0] };
    case "play_card": case "hero_power": {
      const a = { type: t.type };
      if (t.type === "play_card") a.card = t.card;
      let targets = t.targets;
      if (t.choose) { a.choose = t.choose[0].entity_id; targets = t.choose[0].targets; }
      if (targets) a.target = targets[0];
      return a;                                           // no position: the minion goes rightmost
    }
    default: return { type: "end_turn" };
  }
}

setInterval(() => {
  const state = readState();
  if (!state || state.seq <= lastSeq) return;
  lastSeq = state.seq;
  if (state.phase === "game_over") process.exit(0);
  writeAction({ seq: state.seq, action: decide(state) });
}, 50);
```

Test it like any submission: `hs-arena validate <dir>` and `hs-arena play --p1 <dir> --p2 greedy`.
