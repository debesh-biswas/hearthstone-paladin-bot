# hearthstone-paladin-bot

A Hearthstone bot that plays Control Paladin, and plays it pretty well.

It runs on [`hs-arena`](pkg/hs-arena-0.2.2/), a Basic + Classic Hearthstone simulator built on the fireplace
engine. Every turn it searches through its possible plays (attacks, cards, hero power, in every order that
matters), scores the boards it could end up with, and takes the best one. No neural net and no model calls: one
~770-line Python file that makes each decision in under 0.05 s.

## How it did

Against the arena's three hosted opponents:

| Opponent | Deck | Record |
|---|---|---:|
| Bot 1 | Greedy Mage | **12–0** |
| Bot 2 | Face Hunter | **6–2** |
| Astra | Zoo Warlock | **3–5** |

Zero forfeits and zero illegal moves. Astra is the nemesis: when Zoo floods the board on turns 2–4 and we go
second, Paladin often never catches up. `research/submission-2-results.md` has the post-mortem, and a deck tweak
(−1 Equality, +1 Doomsayer) that wins ~4 points more of those games locally. It's not applied yet, if you want
something to try.

## How it plays

`player/scripts/move.py` reads the game state and prints one action.

- **Deck and mulligan:** the list and its tuned weights live in `player/deck.json`. The mulligan keeps cheap
  answers and adjusts for going first or second.
- **Turn search:** a beam search over the whole turn on a small board model. It knows the battlecries, spells,
  deathrattles and auras of every card in the decks it plays.
- **Scoring:** end-of-turn boards are scored on face damage, our health, enemy minions, taunts, cards drawn and
  lethal danger. The weights were tuned by thousands of bot-vs-bot games.
- **Safety:** every action is checked against the legal actions, and on any error it falls back to a simple greedy
  bot.

`player/SKILL.md` wraps it as an Agent Skill, so an LLM agent can sit in the seat and simply relay the script's
moves.

## Try it

You need Python 3.10+ (3.11 recommended; macOS's built-in `python3` is too old). The engine is included:

```bash
cd pkg/hs-arena-0.2.2
python3.11 -m venv .venv && source .venv/bin/activate
pip install --no-index --find-links wheels hs_arena-0.2.2-py3-none-any.whl
cd ../..

hs-arena play --p1 client:player --p2 greedy --games 4      # watch it beat the greedy bot
python tools/test_move.py                                   # planner self-check, silent on success
python tools/fastsim.py --deck player/deck.json --games 200 # fast games vs 15 other decks
python tools/standins.py check                              # vs rebuilt Bot 2 and Astra
```

Game logs go to `games/`. The engine's own `README.md` and `docs/` explain the CLI, the game protocol and the card
pool, and how to put an LLM agent in a seat.

## What's in here

| Path | What |
|---|---|
| `player/` | The bot. |
| `decks/` | 14 other decks we tried, each with a playbook; three have their own scripted pilot. |
| `tools/` | Model-free test bench: fast in-process games, weight tuning, self-play round robins, tournaments, and rebuilt copies of the hosted opponents. |
| `research/` | Every experiment, written up: deck comparisons, tuning runs, rebuilt opponent lists, match post-mortems. |
| `pkg/hs-arena-0.2.2/` | The `hs-arena` simulator, unmodified, AGPL-3.0 (see its `LICENSE`). |
