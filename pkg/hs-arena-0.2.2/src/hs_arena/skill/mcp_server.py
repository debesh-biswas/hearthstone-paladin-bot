"""The game MCP server of one seat: tools wait, act and history over stdio (JSON-RPC, one message per line).

    python -m hs_arena.skill.mcp_server <mailbox_dir>

The server is bound to one seat when it starts; no tool takes a seat or player argument. It talks to the skill
seat (hs_arena.skill.seat) through files in the mailbox directory:

    state.txt / state.json   the pending decision (text for the model; {"seq", "phase"}), written by the seat
    action.json              {"seq", "action"} written here by act; the seat picks it up and deletes it
    answered.txt             the last seq this server submitted an action for
    history.txt              every event this seat has been shown, one line each (appended by the seat)
    game_over.txt            the final state text, written by the seat when the game is over
    calls.jsonl              one line per tool call (audit log)
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any

WAIT_S = float(os.environ.get("HS_MCP_WAIT_S", "45"))
POLL_S = 0.1

INT = {"type": "integer"}
INTS = {"type": "array", "items": {"type": "integer"}}
ACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "enum": ["submit_deck", "mulligan", "play_card", "attack", "hero_power", "choose", "end_turn", "concede"]},
        "card": INT, "target": INT, "attacker": INT, "position": INT, "choose": INT, "replace": INTS, "options": INTS,
        "hero_class": {"type": "string"},
        "cards": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["type"],
    "additionalProperties": False,
}
TOOLS = [
    {"name": "wait",
     "description": "Wait (up to about 45 s) for your next decision. Returns what happened since your previous decision, "
                    "your visible state with its seq, and the LEGAL ACTIONS; or GAME OVER. The first decision asks you "
                    "to submit your hero class and 30-card deck. If no decision is ready yet, "
                    "call wait again. The same state is in game/state.json (JSON) and game/state.txt in your folder.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "act",
     "description": "Submit exactly one action for the pending decision (use the seq shown by wait), then wait for your "
                    "next decision like wait. During deck_submission use {type:submit_deck, hero_class, cards}; "
                    "the accepted deck is locked for this game. Include only the fields the legal action needs; add a target only when "
                    "the legal action lists targets.",
     "inputSchema": {"type": "object", "properties": {"seq": INT, "action": ACTION_SCHEMA},
                     "required": ["seq", "action"], "additionalProperties": False}},
    {"name": "history",
     "description": "Every event you have been shown in this game so far, in order (your own visible log). "
                    "Also in game/history.jsonl in your folder.",
     "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}},
]


def _read(path: Path) -> str | None:
    for _ in range(50):
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        except PermissionError:  # Windows: being replaced right now
            time.sleep(0.01)
    return None


def _read_json(path: Path, default: Any) -> Any:
    text = _read(path)
    try:
        return json.loads(text) if text else default
    except ValueError:
        return default


def _answered(box: Path) -> int:
    try:
        return int((_read(box / "answered.txt") or "0").strip() or 0)
    except ValueError:
        return 0


def wait_state(box: Path) -> str:
    deadline = time.monotonic() + WAIT_S
    while True:
        over = _read(box / "game_over.txt")
        if over is not None:
            return "GAME OVER. No more actions are needed.\n" + over
        state = _read_json(box / "state.json", {})
        seq = state.get("seq", 0)
        if seq > _answered(box):
            text = _read(box / "state.txt") or ""
            return f"YOUR DECISION (seq {seq}):\n{text}"
        if time.monotonic() >= deadline:
            return "No decision for you yet (waiting for the opponent or game setup). Call wait again."
        time.sleep(POLL_S)


def act(box: Path, args: dict[str, Any]) -> str:
    seq = args.get("seq")
    action = args.get("action")
    state = _read_json(box / "state.json", {})
    if not isinstance(seq, int) or isinstance(seq, bool) or not isinstance(action, dict):
        return "act needs an integer seq and an action object; nothing submitted.\n" + wait_state(box)
    if seq != state.get("seq") or seq <= _answered(box):
        return (f"seq {seq} is not the pending decision (stale or already answered); nothing submitted.\n"
                + wait_state(box))
    tmp = box / "action.json.tmp"
    tmp.write_text(json.dumps({"seq": seq, "action": action}), encoding="utf-8")
    os.replace(tmp, box / "action.json")
    tmp = box / "answered.txt.tmp"
    tmp.write_text(str(seq), encoding="utf-8")
    os.replace(tmp, box / "answered.txt")
    return f"Submitted seq {seq}: {json.dumps(action)}\n" + wait_state(box)


def history(box: Path) -> str:
    text = _read(box / "history.txt")
    return "EVENTS SO FAR (your view):\n" + (text.rstrip("\n") if text else "(none yet)")


def handle(box: Path, req: dict[str, Any]) -> dict[str, Any] | None:
    method = req.get("method")
    if "id" not in req:
        return None  # notification
    if method == "initialize":
        result: dict[str, Any] = {
            "protocolVersion": (req.get("params") or {}).get("protocolVersion", "2024-11-05"),
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "hs-arena-seat", "version": "1"},
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        p = req.get("params") or {}
        name, args = p.get("name"), p.get("arguments") or {}
        with open(box / "calls.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({"time": round(time.time(), 3), "tool": name, "arguments": args}) + "\n")
        if name == "wait":
            text = wait_state(box)
        elif name == "act":
            text = act(box, args)
        elif name == "history":
            text = history(box)
        else:
            return {"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32602, "message": f"unknown tool {name!r}"}}
        result = {"content": [{"type": "text", "text": text}]}
    elif method == "ping":
        result = {}
    else:
        return {"jsonrpc": "2.0", "id": req["id"], "error": {"code": -32601, "message": f"unknown method {method!r}"}}
    return {"jsonrpc": "2.0", "id": req["id"], "result": result}


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    box = Path(argv[0]).resolve()
    box.mkdir(parents=True, exist_ok=True)
    for stream in (sys.stdin, sys.stdout):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass
    for line in sys.stdin:
        if not line.strip():
            continue
        req: Any = None
        try:
            req = json.loads(line)
            reply = handle(box, req)
        except Exception as exc:  # never die on one bad request
            rid = req.get("id") if isinstance(req, dict) else None
            reply = {"jsonrpc": "2.0", "id": rid, "error": {"code": -32603, "message": str(exc)}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
