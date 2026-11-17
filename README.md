# hearthstone-arena-skill

Course work for CS 598 A1 (Boston University, Agentic AI, Fall 2026), Homework 2: Hearthstone Agent Arena.
An Agent Skill (playbook + Python move script) that builds a deck and plays the Basic + Classic Hearthstone
simulator of the course's `hs-arena` runtime. The homework is finished; this repo is the archive.

## Results

Final deck: **Control Paladin**, played by a script planner; the model only relays the script's moves.

| Run | vs Bot 1 (Greedy Mage) | vs Bot 2 (Face Hunter) | vs Astra (Zoo Warlock) | Total | Forfeits |
|---|---:|---:|---:|---:|---:|
| Submission 1 | 6–0 | 4–0 | 2–2 | 12–2 | 0 |
| Submission 2 | 6–0 | 2–2 | 1–3 | 9–5 | 0 |

Details: `research/submission-1-results.md`, `research/submission-2-results.md`.

## Layout

| Path | What |
|---|---|
| `player/` | **The skill.** `SKILL.md` tells the agent to relay `scripts/move.py` for every decision; `deck.json` holds the list and its tuned weights. `client.py` is a local, model-free MCP client for tests. |
| `decks/<name>/` | 14 candidate decks (deck list + playbook); three also carry their own scripted pilot. |
| `tools/` | Local evaluation, no model needed: `fastsim.py` (in-process games), `tune.py` and `selfplay.py` (weight tuning), `compare.py`, `tournament.py`, `standins.py` and `early.py` (opponent stand-ins and early-game study), `test_move.py` (planner self-check). |
| `research/` | Write-ups and raw results of every evaluation, rebuilt opponent lists (`opponents/`) and tuned weights (`weights/`). |
| `pkg/hs-arena-0.2.2/` | The course's `hs-arena` package (game engine, CLI, docs, examples), unmodified, AGPL-3.0 (see its `LICENSE`). |
| `task.md` | Assignment brief, rules, grading, plan and the decision log (§11). |
| `meta.md` | Game version, card pool, deck and strategy research. |

## The player

`scripts/move.py` reads `game/state.json` and prints one action. Deck submission comes from `deck.json`, and the
mulligan follows per-deck keep rules. In the main phase it runs a beam search over the whole turn (attacks, cards,
hero power) on a small board model, scores end-of-turn boards with weights tuned by self-play, and checks every
action against the legal actions. If anything fails, it falls back to the course's greedy bot. Each decision takes
under 0.05 s. It uses only the standard library and `hs_arena`, and reads only its own folder.

## Setup

The engine is in the repo. Python 3.10+ (3.11 recommended; macOS's built-in `python3` 3.9 is too old):

```bash
cd pkg/hs-arena-0.2.2
python3.11 -m venv .venv && source .venv/bin/activate
pip install --no-index --find-links wheels hs_arena-0.2.2-py3-none-any.whl
hs-arena version
cd ../..
```

The package `README.md` and `docs/` cover the CLI, the game protocol and the card pool.

## Play and test (no model)

```bash
source pkg/hs-arena-0.2.2/.venv/bin/activate
python tools/test_move.py                                   # planner self-check, silent on success
hs-arena validate --no-game player                          # skill format check
hs-arena play --p1 client:player --p2 greedy --games 4      # our planner vs the course greedy bot, through the real MCP seat
python tools/fastsim.py --deck player/deck.json --games 200 # fast in-process games vs every deck
python tools/standins.py check                              # vs the tuned Bot 2 and Astra stand-ins
```

Playing the skill with a model (`hs-arena play --p1 skill:player ...`) needs Claude Code (Haiku) or the Codex CLI
logged in; see the package README. Game outputs go to `games/` (not tracked).
