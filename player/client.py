"""Local test only (not part of the skill): plays scripts/move.py through the seat's MCP server, no model.
Adapted from the package's examples/greedy_mcp_client.

    hs-arena play --p1 client:player --p2 greedy
"""

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
import move  # noqa: E402
from move import decide  # noqa: E402

move.W.update(move._deck().get("weights", {}))  # same as scripts/move.py main()


class MCPClient:
    """Minimal MCP client over stdio: one JSON-RPC message per line."""

    def __init__(self, command):
        self.proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                                     encoding="utf-8")
        self.next_id = 0

    def request(self, method, params=None):
        self.next_id += 1
        msg = {"jsonrpc": "2.0", "id": self.next_id, "method": method, "params": params or {}}
        self.proc.stdin.write(json.dumps(msg) + "\n")
        self.proc.stdin.flush()
        while True:
            line = self.proc.stdout.readline()
            if not line:
                raise RuntimeError("the MCP server closed the connection")
            reply = json.loads(line)
            if reply.get("id") == self.next_id:
                if "error" in reply:
                    raise RuntimeError(reply["error"])
                return reply["result"]

    def notify(self, method):
        self.proc.stdin.write(json.dumps({"jsonrpc": "2.0", "method": method}) + "\n")
        self.proc.stdin.flush()

    def call(self, tool, **arguments):
        result = self.request("tools/call", {"name": tool, "arguments": arguments})
        return "".join(c.get("text", "") for c in result.get("content", []))

    def close(self):
        self.proc.stdin.close()
        self.proc.wait(timeout=10)


def main():
    client = MCPClient(json.loads(os.environ["HS_ARENA_MCP"]))
    client.request("initialize", {"protocolVersion": "2024-11-05", "capabilities": {},
                                  "clientInfo": {"name": "move-client", "version": "1"}})
    client.notify("notifications/initialized")
    tools = [t["name"] for t in client.request("tools/list")["tools"]]
    print(f"tools: {tools}", file=sys.stderr)

    reply = client.call("wait")
    while not reply.startswith("GAME OVER"):
        if reply.startswith("YOUR DECISION"):
            # the text is for a model; a program reads the same state as JSON from game/state.json
            state = json.loads(Path("game/state.json").read_text(encoding="utf-8"))
            action = decide(state)
            reply = client.call("act", seq=state["seq"], action=action)
        else:
            reply = client.call("wait")  # the opponent is still playing
    print(reply.splitlines()[0], file=sys.stderr)
    client.close()


if __name__ == "__main__":
    main()
