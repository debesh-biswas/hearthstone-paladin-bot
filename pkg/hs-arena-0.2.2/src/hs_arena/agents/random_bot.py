"""Built-in random bot: uniform over legal action templates, uniform parameters, never concedes."""

from __future__ import annotations

import random
from typing import Any

from ..deck import Deck
from .base import Decision, Player, SeatInfo


def instantiate(template: dict[str, Any], rng: random.Random) -> dict[str, Any]:
    """Pick uniformly random parameters for one legal-action template."""
    t = template["type"]
    if t in ("play_card", "hero_power"):
        action: dict[str, Any] = {"type": t}
        if t == "play_card":
            action["card"] = template["card"]
        targets = template.get("targets")
        if template.get("choose"):
            option = rng.choice(template["choose"])
            action["choose"] = option["entity_id"]
            targets = option.get("targets")
        if targets:
            action["target"] = rng.choice(targets)
        positions = template.get("positions")
        if positions:
            action["position"] = rng.choice(positions)
        return action
    if t == "attack":
        return {"type": t, "attacker": template["attacker"], "target": rng.choice(template["targets"])}
    if t == "mulligan":
        return {"type": t, "replace": [o for o in template["options"] if rng.random() < 0.5]}
    if t == "choose":
        k = rng.randint(template["min"], template["max"])
        return {"type": t, "options": [o["entity_id"] for o in rng.sample(template["options"], k)]}
    return {"type": t}


class RandomBot(Player):
    kind = "random"

    def __init__(self, name: str, deck: Deck, seed: int = 0):
        super().__init__(name, deck)
        self._seed = seed
        self.rng = random.Random(seed)

    def start(self, seat: SeatInfo) -> None:
        super().start(seat)
        self.rng = random.Random(seat.seed * 2 + seat.player)

    def decide(self, state: dict[str, Any]) -> Decision:
        templates = [t for t in state["legal_actions"] if t["type"] != "concede"]
        if not templates:
            return Decision("action", {"type": "concede"})
        return Decision("action", instantiate(self.rng.choice(templates), self.rng))
