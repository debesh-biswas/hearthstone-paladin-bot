"""Approximate per-decision think time of skill seats from mcp_calls.jsonl.

Gap between consecutive tool calls of a seat, skipping gaps after end_turn/mulligan/submit_deck/wait,
because those include the opponent's turn. Usage: python tools/latency.py games/stageb
"""
import json, sys, statistics
from collections import defaultdict
from pathlib import Path

lat = defaultdict(list)
for f in Path(sys.argv[1]).glob("*/g_*/p*/seat/mcp_calls.jsonl"):
    name = json.loads((f.parent / "seat.json").read_text())["name"]
    calls = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    for a, b in zip(calls, calls[1:]):
        t = (a.get("arguments", {}).get("action") or {}).get("type")
        if a["tool"] == "act" and t not in ("end_turn", "mulligan", "submit_deck"):
            lat[name].append(b["time"] - a["time"])
for n, v in sorted(lat.items()):
    v.sort()
    print(f"{n:16} decisions {len(v):4}  median {statistics.median(v):5.1f}s  p95 {v[int(.95*len(v))]:5.1f}s  max {v[-1]:5.1f}s")
