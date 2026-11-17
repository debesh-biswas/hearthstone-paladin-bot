"""Example submission: picks uniformly among the legal actions. Protocol demo only - it contains no LLM code.

A real submission must have an LLM core: build a prompt from state.to_text() (or your own rendering), call
your model at OPENAI_BASE_URL / MODEL with QWEN_API_KEY using any HTTP client, and turn its answer into an
Action. Keep your own memory of the game in instance attributes; the runtime only sends the current state and
the events since your previous state.
"""

import random
import sys

from hs_arena.sdk import Action, Agent, GameInfo, Result, State, run


class RandomAgent(Agent):
    def __init__(self):
        self.rng = random.Random()
        self.decisions = 0  # per-game memory lives in instance state

    def on_game_start(self, info: GameInfo) -> None:
        self.rng.seed(f"{info.game_id}-{info.player}")
        print(f"[random-agent] game {info.game_id}: I am player {info.player} playing {info.hero_class}",
              file=sys.stderr)

    def decide(self, state: State) -> Action:
        self.decisions += 1
        templates = [t for t in state.legal_actions if t.type != "concede"]
        t = self.rng.choice(templates)
        if t.type == "mulligan":
            return Action.mulligan([eid for eid in t.options if self.rng.random() < 0.5])
        if t.type == "choose":
            return Action.choose(self.rng.choice(t.options).entity_id)
        if t.type == "attack":
            return Action.attack(t.attacker, self.rng.choice(t.targets))
        if t.type in ("play_card", "hero_power"):
            targets, choose = t.targets, None
            if t.get("choose"):
                option = self.rng.choice(t.choose)
                choose, targets = option.entity_id, option.targets
            target = self.rng.choice(targets) if targets else None
            if t.type == "hero_power":
                return Action.hero_power(target=target, choose=choose)
            position = self.rng.choice(t.positions) if t.positions else None
            return Action.play_card(t.card, target=target, position=position, choose=choose)
        return Action.end_turn()

    def on_game_over(self, result: Result) -> None:
        outcome = {True: "won", False: "lost", None: "no winner"}[result.you_won]
        print(f"[random-agent] game over ({result.reason}): {outcome} after {self.decisions} decisions",
              file=sys.stderr)


if __name__ == "__main__":
    run(RandomAgent)
