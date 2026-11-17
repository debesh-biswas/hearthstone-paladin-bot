"""Player interface used by the runner. Implemented by ProcessAgent and by the built-in bots."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from threading import Event
from typing import Any

from ..deck import Deck
from ..protocol import Config


@dataclass
class SeatInfo:
    """What the runner tells a player when the game starts."""

    game_id: str
    player: int  # 1 or 2
    seed: int
    player_dir: Path  # <game_dir>/pN
    config: Config


@dataclass
class Decision:
    """Outcome of one decision request.

    kind: "action"       -> `action` holds the (unvalidated) action object
          "timeout"      -> no valid answer within the decision timeout
          "exited"       -> the agent process exited before game over
          "bad_json"     -> action.json did not parse / had no valid seq or action object
          "seq_mismatch" -> action.json carried a seq larger than the pending one
          "forfeit"      -> the player loses the game now (early session termination)
          "cancelled"    -> deck submission was cancelled because the game ended
    """

    kind: str
    action: Any = None
    message: str = ""


class Player(ABC):
    kind: str = "builtin"  # "process" | "skill" | "client" | "random" | "greedy"
    requires_deck_submission = False

    def __init__(self, name: str, deck: Deck | None = None):
        self.name = name
        self.deck = deck
        self.restarts = 0
        self.notes: list[str] = []  # human-readable seat notes copied into result.json (skill seats)
        self._decision_cancelled = Event()

    def start(self, seat: SeatInfo) -> None:
        self.seat = seat
        self._decision_cancelled.clear()

    def cancel_pending(self) -> None:
        """Wake a pending deck decision when the other seat terminates the game."""
        self._decision_cancelled.set()

    @abstractmethod
    def decide(self, state: dict[str, Any]) -> Decision:
        """Answer one state.json (dict). Must return quickly for built-in bots."""

    def game_over(self, state: dict[str, Any]) -> None:
        """Deliver the final state (phase game_over)."""

    def poll_exit(self) -> Decision | None:
        """Check a managed process even while the opponent is taking its turn."""
        return None

    def restart(self) -> None:
        """Legacy compatibility hook; the 0.2.2 runner never restarts a player."""
        self.restarts += 1

    def stop(self) -> None:
        """Release resources; must be idempotent."""

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "kind": self.kind}
