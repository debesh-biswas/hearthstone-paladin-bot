# hs-arena: Hearthstone Agent Arena (CS 598 HW2)

In Homework 2 you write a **skill** that builds a deck and plays Hearthstone: a playbook (`SKILL.md`), and
optionally scripts and reference files. The course runs every skill with the same agent harness, on the model
the skill picks: **Claude Haiku 5.5** in Claude Code, or **GPT-6-Luna** in Codex, both at reasoning effort
medium. This package is everything you need to build and test a skill locally, exactly the way the course
server runs it.

- **Assignment, rules, grading, dates:** [`docs/handout.md`](docs/handout.md)
- **Card pool** (367 cards, Basic + Classic): [`docs/card_pool.md`](docs/card_pool.md) or `hs-arena cards`
- **Examples:**
  - [`examples/starter_skill`](examples/starter_skill): a playbook-only skill to copy;
  - [`examples/greedy_skill`](examples/greedy_skill): a script decides every move and the agent relays it;
  - [`examples/greedy_mcp_client`](examples/greedy_mcp_client): the same bot as a plain MCP client, no model.
- **State and action format** (what your scripts read): [`docs/protocol.md`](docs/protocol.md), sections 5–9

## How a game runs

```text
hs-arena play --p1 skill:my_skill --p2 greedy

  game host (the runtime): fireplace engine, validates every action, logs the game, decides the winner
   ├── seat 1: skill seat
   │     ├── game MCP server of this seat: tools wait / act / history (shows only this seat's view)
   │     └── agent session: Claude Code (model: haiku) or Codex (model: luna), effort medium
   │           system prompt = course prompt + your SKILL.md
   │           working folder = copy of your skill + game/ + scratch/
   │           tools = the game tools, a shell, file read/write (no sub-agents, no web, no network)
   └── seat 2: the greedy bot
```

The course server starts the same thing for every game, with the course's own accounts. Locally, the agent
session runs with **your** Claude Code or Codex login.

The first MCP decision is **`deck_submission`**, sent to both agents concurrently. Each agent chooses its
class and builds its own legal 30-card deck using its skill, scripts and `game/card_pool.json`, then calls
`act(seq, {"type":"submit_deck","hero_class":"MAGE","cards":[...30 card ids...]})`.
Deck building can be dynamic or random on every game. The host validates and locks each accepted deck;
only after both are ready does it create the engine and begin mulligans. Opponent choices are hidden during
deck submission. Invalid decks are reported as `INVALID_DECK` and can be corrected with the next seq;
setup uses the same timeout and illegal-action limits as play. **The host does not read your deck.json.**

### Connect externally launched subagents (no skill launcher)

An orchestrator can launch both subagents itself, give each one its student's skill, and use the host only
for the game and MCP communication. Create a separate fresh workspace for each seat:

```text
hs-arena play --p1 mcp:work/seat1 --p2 mcp:work/seat2 --games 1 --out games
```

Each directory must exist. Give subagent 1 `work/seat1` as its working directory and connect this stdio MCP
server (use absolute paths in your orchestrator):

```text
python -m hs_arena.skill.mcp_server <absolute-seat1-workspace>/arena-mailbox
```

Do the same for seat 2. Both agents start with `wait`, submit decks, then play until GAME OVER. The host
creates `game/` (state, history, allowed card catalog) and `scratch/` inside each workspace. It never reads
SKILL.md, selects a model, starts a subagent or stops the external process. The orchestrator supplies the
agent's instructions/model/tools and manages its lifecycle; missing responses use the normal timeout policy.
Use a fresh workspace for every game; files are preserved for review. The `skill:` and `client:` modes remain
local launch conveniences and speak the same MCP protocol.

## Requirements

- **Python 3.10 or newer** (3.11 recommended): Windows 11, macOS, or Linux / WSL Ubuntu.
- For `model: haiku`: **[Claude Code](https://docs.claude.com/en/docs/claude-code)** installed and logged in
  (`claude` on your PATH). On Windows, Claude Code needs Git for Windows (Git Bash).
- For `model: luna`: the **Codex CLI** installed and logged in (`codex` on your PATH).
- Local games use your own account. One game is about 25–60 agent steps, roughly 1–3 minutes.

## Installation

The course zip `hs-arena-<version>.zip` unpacks into one directory:

```text
hs-arena-<version>/
├── hs_arena-<version>-py3-none-any.whl   # the runtime: CLI `hs-arena`, skill seat, game MCP server
├── wheels/                               # its dependencies (hearthstone, hearthstone_data, ...)
├── INSTALL.txt  README.md  LICENSE
├── docs/                                 # handout.md, protocol.md, card_pool.md
├── examples/                             # starter_skill, greedy_skill, greedy_mcp_client
├── data/  schemas/  decks/  pool/        # copies of the package data, for browsing
└── src/                                  # the full source tree, including tests/ and tools/
```

In a fresh virtual environment, from inside `hs-arena-<version>/` (no network access needed):

```text
pip install --no-index --find-links wheels hs_arena-<version>-py3-none-any.whl
hs-arena version
```

Step-by-step instructions: [Windows](#setup-on-windows-native), [WSL Ubuntu](#setup-on-wsl-ubuntu),
[macOS](#setup-on-macos). `python -m hs_arena ...` works as well as `hs-arena ...`.

## Quick start

```text
cp -r examples/starter_skill my_skill                        # Windows: Copy-Item -Recurse examples\starter_skill my_skill
hs-arena play --p1 client:examples/greedy_mcp_client --p2 random --games 3 --out games   # no model: checks the install
hs-arena validate my_skill                                   # checks the files, plays one game vs random (uses your login)
hs-arena play --p1 skill:my_skill --p2 greedy --games 3 --out games
hs-arena replay games/<game_id>                              # turn-by-turn transcript
```

`play` prints one line per game and a summary:

```text
hs-arena 0.2.2: 2 game(s) P1=starter-mage vs P2=greedy seed 11 parallel 2 -> games
g_20261022_000002  winner P1   hero_death        turns  22  illegal 0/0  restarts 0/0  timeouts 0/0  116.6s
g_20261022_000001  winner P1   hero_death        turns  24  illegal 0/0  restarts 0/0  timeouts 0/0  135.6s

side  player                        wins  illegal
P1    starter-mage                     2        0
P2    greedy                           0        0
games 2  counted 2  draws 0  voided 0  failed 0
```

## Writing a skill

### Layout

```text
my_skill/
├── SKILL.md          required: frontmatter + playbook
├── deck.json         optional: a recipe your agent may read and submit via MCP
├── scripts/          optional: code the agent can run
├── references/       optional: knowledge files the agent can read
├── requirements.txt  optional: extra Python packages for your scripts
└── README.md         optional: notes for the staff; never copied into the agent's folder
```

`SKILL.md` starts with a frontmatter block:

```markdown
---
name: frostbolt-enjoyer
description: Tempo Mage that trades early and burns face late.
model: haiku          # haiku = Claude Haiku 5.5 in Claude Code; luna = GPT-6-Luna in Codex
---

# My playbook
...
```

Everything after the frontmatter is your playbook. It is appended to the course prompt, so the agent reads it
before the game starts. `hs-arena prompt my_skill` prints the complete prompt the agent gets. The names `game`
and `scratch` are reserved at the top level of a skill.

### What the agent sees and can do

- **Game tools** (from the seat's MCP server; they show only your seat):
  - `wait`: your next decision, as text. This includes what happened since your previous decision, your
    visible state with its `seq`, and the numbered LEGAL ACTIONS. If no decision is ready yet, call it again.
  - `act(seq, action)`: submits one action, then waits for the next decision.
  - `history`: every event your seat has been shown in this game so far.
- **Its folder** (its working directory; deleted after the game):

  ```text
  SKILL.md, deck.json, scripts/, references/   a copy of your skill
  game/state.json      the pending decision as JSON (rewritten before every decision; format: docs/protocol.md §5)
  game/state.txt       the same as text (what wait shows)
  game/card_pool.json  allowed cards (id -> card data), for your deck-building policy
  game/history.jsonl   every event your seat has been shown, one JSON object per line (docs/protocol.md §8)
  scratch/             free space for notes and memory during this game
  ```

- **A shell and file read/write** inside this folder. `python` is the interpreter that runs hs-arena, so your
  scripts can `import hs_arena` (card data via `hs_arena.cards.load()`, and the engine). There are no
  sub-agents, no web tools and no network.

Actions use entity ids, the `#numbers` in the state (full format: [`docs/protocol.md`](docs/protocol.md) §6–7):

Before entities exist, `submit_deck` instead uses card-id strings from the pool. The setup state has
`you=null`, `opponent=null`, and `deck_rules`; the first `mulligan` normally has seq 2 rather than 1.
Accepted class and card lists cannot be changed during play. You may omit deck.json entirely when your
playbook or script generates the deck itself.

```text
{"type":"mulligan","replace":[ids]}          {"type":"play_card","card":24,"position":0}
{"type":"play_card","card":24,"target":41}   {"type":"attack","attacker":22,"target":37}
{"type":"hero_power"}                        {"type":"hero_power","target":37}
{"type":"choose","options":[73]}             {"type":"end_turn"}
```

Give a `target` only when the legal action lists targets. The text marks the others with `(no target)`.

### Scripts

A script typically:

1. reads `game/state.json` (and `game/history.jsonl` or its own notes in `scratch/`);
2. computes something (lethal check, trade evaluation, a search, or the whole move);
3. prints the result for the agent. The agent then submits a move with `act`.

`examples/greedy_skill/scripts/greedy_move.py` prints a complete action (`{"seq": N, "action": {...}}`), and the
playbook tells the agent to relay it unchanged.

- **Time.** Every decision has a 3-minute limit, and each tool call of the agent takes a few seconds. Keep
  scripts fast and tell the agent exactly what to run.
- **Packages.** Use Python and the standard library or dependencies bundled with hs-arena. The course does
  not install extra packages from `requirements.txt`. Keep the uncompressed skill folder within 10 MB.
- **Testing a script by hand.** Every game directory keeps the states your seat received
  (`pN/decisions/*.state.json`). Let your script take an optional path argument, as `greedy_move.py` does:
  `python scripts/greedy_move.py ../games/<game_id>/p1/decisions/00012.state.json` (run from `my_skill/`).

### Rules that the seat enforces

- **Illegal actions.** The third illegal action in a game immediately forfeits it (`forfeit_illegal`).
- **Timeout.** Each decision has 180 seconds. The first timeout immediately forfeits (`forfeit_timeout`).
  The clock starts when your decision is published; waiting for the opponent is not charged. Calling `wait`
  does not pause or reset an active decision clock.
- **Early exit.** The first session/process exit before GAME OVER immediately forfeits (`forfeit_exit`).
  There is no warning or automatic restart. Stop diagnostics are logged for staff review of course-side failures.

These rules apply during deck submission, mulligan, choices and normal play.

The full rules and the grading are in [`docs/handout.md`](docs/handout.md).

## Opponents for local testing

| Spec | Player |
|------|--------|
| `skill:<dir>` | a skill, played by the course agent with your login (also for self-play: `--p1 skill:a --p2 skill:b`) |
| `client:<dir>` | an MCP client program `<dir>/client.py` that submits its deck, e.g. `client:examples/greedy_mcp_client` |
| `mcp:<workspace>` | an externally launched agent; host reads no skill or deck files, single game per fresh workspace |
| `greedy` | the built-in Greedy Mage, with its deck (`hs_arena/decks/greedy_mage.json`) |
| `greedy:<deck.json>` | the greedy bot playing another deck |
| `random`, `random:<deck.json>` | uniformly random legal actions |

`greedy` and `client:examples/greedy_mcp_client` make the same moves; the built-in one skips the MCP round
trip. The course server also uses a second, stronger rule-based bot and an LLM agent (Astra); see the
handout.

## Game directory and logs

Every game gets `games/<game_id>/`:

| File | Content |
|------|---------|
| `game.json` | players, decks, seed, versions |
| `replay.jsonl` | the public event stream; `hs-arena replay` renders it |
| `result.json` | winner, reason, turns, illegal actions, timeouts, restarts, `notes` (seat diagnostics) |
| `pN/decisions/` | every `state.json` the seat received and every action it sent |
| `pN/stderr.log` | the seat's own log (session start and exit diagnostics) |
| `pN/seat/` | `system_prompt.md` (the exact prompt), `session_K.jsonl` (the agent's full transcript: every tool call and output), `mcp_calls.jsonl`, `seat.json` (sessions, token usage), `scratch/` (what the agent left in scratch) |

When a game goes wrong, read `pN/seat/session_1.jsonl` first.

## CLI reference

Every command has `--help`.

```text
hs-arena play --p1 SPEC --p2 SPEC [--games N] [--seed S] [--out DIR] [--parallel K]
              [--keep-decisions | --no-keep-decisions] [--timeout S] [--max-turns N]
              [--illegal-limit N] [--exit-grace S]
hs-arena validate SKILL_DIR [--no-game] [--seed S] [--timeout S] [--out DIR]
hs-arena prompt SKILL_DIR [--player 1|2]
hs-arena replay GAME_DIR | REPLAY_JSONL
hs-arena cards [--class CLASS] [--only] [--json]
hs-arena version
```

| `play` flag | Default | Meaning |
|------|---------|---------|
| `--games N` | 1 | number of games |
| `--seed S` | random | base seed; game k uses seed S + k (the seed decides who goes first and the shuffles) |
| `--out DIR` | `./games` | where the game directories are created |
| `--parallel K` | 4 | games run in parallel (each skill seat is one agent session on your account) |
| `--timeout S` | 180 | decision timeout in seconds |
| `--max-turns N` | off | end the game as a draw after N turns |
| `--illegal-limit N` | 3 | forfeit on reaching N illegal actions; use the default for course practice |

`validate` checks `SKILL.md` and `requirements.txt`, checks that `claude` or `codex` is on your
PATH, and plays one game against `random` (seed 1). It fails if the skill loses by forfeit, times out, or its
session fails. Use `--no-game` to check only the files. `play` exits with 0 when every game ran, 1 on a runtime
error, and 2 for an invalid player spec.

## Decks and the card pool

- exactly 30 cards, all from the course pool: the collectible **Basic and Classic** cards of the nine classic
  classes, without the Hall of Fame cards (e.g. Azure Drake, Leeroy Jenkins) and without the cards in
  `hs_arena/pool/blacklist.txt` (engine problems);
- class cards only of your `hero_class` (`DRUID`, `HUNTER`, `MAGE`, `PALADIN`, `PRIEST`, `ROGUE`, `SHAMAN`,
  `WARLOCK`, `WARRIOR`), plus NEUTRAL cards;
- at most 2 copies of a card, at most 1 copy of a LEGENDARY card;
- your hero is the class's default hero.

```text
hs-arena cards --class MAGE          # every card a Mage deck may use (Mage + Neutral)
hs-arena cards --class MAGE --only   # Mage cards only
hs-arena cards --json                # the full catalog as JSON (same data as hs_arena.cards.load())
```

`hs-arena validate` reports every problem with a deck at once, e.g.
`card 'EX1_284' (Azure Drake) is in the Hall of Fame and not in the pool`.

## Sample transcript

`hs-arena replay` for a `starter-mage` (P1) vs `greedy` (P2) game (lines left out are marked `...`):

```text
Game g_20261022_000001  seed 11
  P1: starter-mage (skill, MAGE)
  P2: greedy (greedy, MAGE)
Game start: P2 goes first.
  P1 mulligans 1 card(s).
  P2 mulligans 3 card(s).

--- Turn 1: P2 ---
  P2 draws a card.
  P2 plays Arcane Missiles #45.
  Jaina Proudmoore #4 (P1) takes 1 damage from Arcane Missiles #45, health 29.
  ...
--- Turn 2: P1 ---
  P1 draws a card.
  P1 plays The Coin #70.
  P1 plays Sorcerer's Apprentice #9 at position 0.
  P1 ends the turn.
...
--- Turn 24: P1 ---
  P1 draws a card.
  P1 uses Fireblast on Jaina Proudmoore #37.
  Jaina Proudmoore #37 (P2) takes 1 damage from Fireblast #5, health 2.
  P1: Argent Commander #33 attacks Jaina Proudmoore #37.
  Jaina Proudmoore #37 (P2) takes 4 damage from Argent Commander #33, health -2.
Game over: P1 wins (hero_death).

Result: winner P1, reason hero_death, 24 turns, illegal 0/0, restarts 0/0, timeouts 0/0, 135.598 s
```

The `#nn` numbers are entity ids, the ids used in actions.

## Setup on Windows (native)

Use a **short arena root** such as `C:\arena`. The vendored engine has deep package paths, and a virtual
environment deep inside your user profile can hit the 260-character path limit. In PowerShell:

```powershell
mkdir C:\arena
cd C:\arena
Expand-Archive $HOME\Downloads\hs-arena-<version>.zip -DestinationPath .
cd hs-arena-<version>
py -3.11 -m venv .venv                     # or any Python 3.10+
.\.venv\Scripts\Activate.ps1
pip install --no-index --find-links wheels hs_arena-<version>-py3-none-any.whl
hs-arena version
hs-arena play --p1 client:examples\greedy_mcp_client --p2 random --games 3 --out .\games
```

If `Activate.ps1` is blocked by the execution policy, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
once, or call `.\.venv\Scripts\hs-arena.exe` directly. Enabling long paths is recommended (PowerShell **as
Administrator**, then sign out and in again):

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name LongPathsEnabled -Value 1 -PropertyType DWORD -Force
```

Then check that your harness works in the same PowerShell window: `claude --version` (Claude Code; it needs Git
for Windows) or `codex --version`, and that you are logged in. Then:

```powershell
Copy-Item -Recurse .\examples\starter_skill .\my_skill
hs-arena validate .\my_skill
hs-arena play --p1 skill:.\my_skill --p2 greedy --games 3 --out .\games
```

## Setup on WSL Ubuntu

Keep the arena on the **Linux file system** (e.g. `~/arena`), not under `/mnt/c/...` (file access to the
Windows drive from WSL is much slower). Install and log in to Claude Code or Codex **inside WSL**.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip unzip    # Ubuntu 22.04: 3.10, 24.04: 3.12; both work
mkdir -p ~/arena && cd ~/arena
cp /mnt/c/Users/<you>/Downloads/hs-arena-<version>.zip .
unzip hs-arena-<version>.zip
cd hs-arena-<version>
python3 -m venv .venv
source .venv/bin/activate
pip install --no-index --find-links wheels hs_arena-<version>-py3-none-any.whl
hs-arena version
hs-arena play --p1 client:examples/greedy_mcp_client --p2 random --games 3 --out games
```

Game directories are plain UTF-8 files: a game played in WSL can be replayed on Windows and vice versa.

## Setup on macOS

The `python3` that comes with macOS (Xcode Command Line Tools) is Python 3.9, which is too old. Install Python
3.11 with [Homebrew](https://brew.sh) (`brew install python@3.11`) or from
[python.org](https://www.python.org/downloads/macos/). In Terminal:

```bash
mkdir -p ~/arena && cd ~/arena
cp ~/Downloads/hs-arena-<version>.zip .
unzip hs-arena-<version>.zip
cd hs-arena-<version>
python3.11 -m venv .venv                   # not plain python3: that may still be the system 3.9
source .venv/bin/activate
pip install --no-index --find-links wheels hs_arena-<version>-py3-none-any.whl
hs-arena version
hs-arena play --p1 client:examples/greedy_mcp_client --p2 random --games 3 --out games
```

If Safari already unpacked the download, `~/Downloads` holds a folder `hs-arena-<version>` instead of the zip:
copy it with `cp -R ~/Downloads/hs-arena-<version> ~/arena/`. Keep the arena in a plain local folder, not in
iCloud Drive or Dropbox. Run `source .venv/bin/activate` again in every new Terminal window.

## Running the test suite

From the source tree (`src/` in the zip), in a virtual environment (network access needed for `pytest` and
`jsonschema`):

```text
pip install -e ".[dev]"
pytest -m "not slow"        # quick suite (a few minutes); calls no model
pytest                      # everything, including the long stability and property tests
```

`python tools/smoke_install.py <zip> [--python PYTHON] [--tests]` checks a built zip end to end. It installs the
wheel into a fresh venv, plays games with the greedy MCP client, and optionally runs the quick suite.

## Development notes

- The skill seat is `hs_arena/skill/`:
  - `seat.py`: the seat, the harness commands and early-exit diagnostics;
  - `mcp_server.py`: the game MCP server;
  - `course_prompt.md`: the course prompt;
  - `loader.py`: skill validation.
- The file protocol of [`docs/protocol.md`](docs/protocol.md) (`state.json` / `action.json`, `manifest.json`)
  is what the runtime uses between itself and process players. The built-in bots, the SDK (`hs_arena.sdk`) and
  the course's own tools use it. Students do not need it.
- Package data lives inside the package:
  - `hs_arena/data/cards.json` and `excluded_cards.json`;
  - `hs_arena/schemas/*.schema.json`;
  - `hs_arena/decks/greedy_mage.json`;
  - `hs_arena/pool/blacklist.txt`;
  - the greedy bot's weights, in `hs_arena/agents/greedy_config.json`.
- `python tools/gen_cards.py` rebuilds the card data and `docs/card_pool.md` from the vendored `CardDefs.xml`.
- `python tools/build_zip.py` builds the course zip.
- Vendored fireplace: `hs_arena/_vendor/fireplace/`, pinned upstream commit
  `47a2572a000db66645bb74a425a090d51f1004fa`. The patches are listed in `UPSTREAM.txt`.
- **License**: AGPL-3.0 (see `LICENSE`), because fireplace is AGPL-3.0.
