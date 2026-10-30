# hearthstone-arena-skill

Course work for CS 598 A1 (Boston University, Agentic AI, Fall 2026), Homework 2: Hearthstone Agent Arena.
A skill (playbook + Python move scripts) that builds a deck and plays the Basic + Classic Hearthstone
simulator of the course's `hs-arena` runtime.

## Layout

| Path | What |
|---|---|
| `player/` | **The skill.** `SKILL.md` tells the agent to relay `scripts/move.py` for every decision; `deck.json` holds the list and its tuned weights. `client.py` is a local, model-free MCP client for tests (not submitted). |
| `decks/<name>/` | 14 candidate decks (deck.json + playbook); three also carry their own scripted pilot (`scripts/move.py`). |
| `tools/` | Local evaluation: `fastsim.py` (in-process games, no model), `tune.py`, `selfplay.py` (script-only tuning loop), `compare.py`, `pilots.py`, `tournament.py`, `latency.py`, `test_move.py` (planner self-check). |
| `research/` | Write-ups and raw results of every evaluation; `script-deck-comparison.md` is the current deck comparison. |
| `task.md` | Assignment brief, rules, grading, plan, and the decision log (§11). |
| `meta.md` | Game version, card pool, deck and strategy research. |

## The player

`scripts/move.py` reads `game/state.json` and prints one action. Deck submission comes from `deck.json`, and the mulligan
follows per-deck keep rules. In the main phase it runs a beam search over our whole turn (attacks, cards, hero power) on a
small board model. It scores end-of-turn boards with weights tuned by self-play, and it checks every action against the
legal actions. If anything fails, it falls back to the course's greedy bot. Each decision takes under 0.05 s. It uses only
the standard library and `hs_arena`, and reads only its own folder.

Current deck: **Control Paladin**. Results of the 7-deck script round robin and the tuning are in
`research/script-deck-comparison.md`.

## Setup

The course package is not stored in this repo. Download it into `pkg/`:

```bash
mkdir -p pkg && cd pkg
curl -LO https://bu-agenticai-class-fall26.vercel.app/materials/assignments/hw2/hs-arena-0.2.2.zip
unzip hs-arena-0.2.2.zip && cd hs-arena-0.2.2
python3 -m venv .venv && source .venv/bin/activate      # Python 3.10+
pip install --no-index --find-links wheels hs_arena-0.2.2-py3-none-any.whl
hs-arena version
```

## Checks and local games (no model)

```bash
source pkg/hs-arena-0.2.2/.venv/bin/activate
python tools/test_move.py                                   # planner self-check, silent on success
python tools/fastsim.py --deck player/deck.json --games 200 # our planner vs every deck, greedy-piloted
hs-arena play --p1 client:player --p2 greedy --games 4      # through the real MCP seat
python tools/selfplay.py                                    # script-only tune/sim loop; resumes; stop with Ctrl-C
```

Game outputs go to `games/` (not tracked).

## Build the submission ZIP

```bash
rm -rf dist && mkdir -p dist/control-paladin/scripts
cp player/SKILL.md player/deck.json dist/control-paladin/
cp player/scripts/move.py dist/control-paladin/scripts/
(cd dist && zip -rq control-paladin.zip control-paladin)
hs-arena validate --no-game dist/control-paladin
```

The submission itself is sent by hand through the course Slack agent. `dist/`, ZIPs and returned results are not tracked.
