"""Text renderer for replay.jsonl (the public event stream of a game)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .sdk.text import event_text


def load(path: str | Path) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any] | None]:
    """Load (game.json, events, result.json) from a game directory or a replay.jsonl path."""
    path = Path(path)
    if path.is_dir():
        game_dir, replay_path = path, path / "replay.jsonl"
    else:
        game_dir, replay_path = path.parent, path
    if not replay_path.exists():
        raise FileNotFoundError(f"{replay_path}: no replay.jsonl")
    events = []
    with open(replay_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                events.append(json.loads(line))
    game = result = None
    if (game_dir / "game.json").exists():
        game = json.loads((game_dir / "game.json").read_text(encoding="utf-8"))
    if (game_dir / "result.json").exists():
        result = json.loads((game_dir / "result.json").read_text(encoding="utf-8"))
    return game, events, result


def render(game: dict[str, Any] | None, events: list[dict[str, Any]], result: dict[str, Any] | None) -> str:
    def who(i):
        return f"P{i}" if i in (1, 2) else "nobody"

    lines = []
    if game:
        lines.append(f"Game {game.get('game_id')}  seed {game.get('seed')}  runtime {game.get('runtime_version')}")
        for p in game.get("players", []):
            lines.append(f"  P{p['index']}: {p['name']} ({p['kind']}, {p['hero_class']})")
    for ev in events:
        text = event_text(ev, who)
        if ev.get("event") == "turn_start":
            lines.append("")
            lines.append(text)
        else:
            lines.append(("  " if ev.get("event") not in ("game_start", "game_over") else "") + text)
    if result:
        lines.append("")
        w = result.get("winner")
        winner = f"P{w}" if w else "none"
        lines.append(
            f"Result: winner {winner}, reason {result.get('reason')}, {result.get('turns')} turns, "
            f"illegal {result['illegal_counts']['1']}/{result['illegal_counts']['2']}, "
            f"restarts {result['restarts']['1']}/{result['restarts']['2']}, "
            f"timeouts {result['timeouts']['1']}/{result['timeouts']['2']}, {result.get('duration_s')} s"
        )
        if result.get("engine_error"):
            lines.append(f"Engine error (game voided): {result['engine_error']['message']} cards {result['engine_error']['card_ids']}")
    return "\n".join(lines)


def render_path(path: str | Path) -> str:
    return render(*load(path))
