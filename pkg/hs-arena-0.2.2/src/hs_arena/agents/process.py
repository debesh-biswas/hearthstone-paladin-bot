"""ProcessAgent: runs a submission as a long-running process and talks to it through state.json / action.json."""

from __future__ import annotations

import json
import os
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Any

from .. import PROTOCOL_VERSION
from .._fileio import atomic_write_json, read_text, remove_file
from ..deck import Submission
from ..protocol import sanitize_action
from ._proctree import ProcessTree
from .base import Decision, Player, SeatInfo

PYTHON_TOKENS = ("python", "python3")
PASS_THROUGH_ENV = ("OPENAI_BASE_URL", "MODEL", "QWEN_API_KEY")
BAD_JSON_SETTLE_S = 1.0  # an unparseable action.json must stay unchanged this long before it counts as BAD_JSON


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


class _StderrPump(threading.Thread):
    """Copies a child's stderr into stderr.log up to a byte cap, then discards the rest (never blocks the child)."""

    def __init__(self, stream, sink, budget):
        super().__init__(daemon=True)
        self.stream = stream
        self.sink = sink
        self.budget = budget  # shared mutable [remaining_bytes, truncated_flag]
        self.lock = budget[2]

    def run(self):
        try:
            while True:
                chunk = self.stream.read1(65536) if hasattr(self.stream, "read1") else self.stream.read(65536)
                if not chunk:
                    break
                with self.lock:
                    part = chunk[: max(self.budget[0], 0)]
                    if part:
                        self.sink.write(part)
                        self.budget[0] -= len(part)
                    # the first chunk that does not fit gets the marker, also when an earlier chunk filled the
                    # budget exactly (Linux pipe reads are 64 KiB, a multiple of the default cap)
                    truncate = len(part) < len(chunk) and not self.budget[1]
                    if truncate:
                        self.budget[1] = True
                        self.sink.write(b"\n[hs-arena] stderr.log size cap reached; further output discarded\n")
                    if part or truncate:
                        self.sink.flush()
        except (OSError, ValueError):
            pass
        finally:
            try:
                self.stream.close()
            except Exception:
                pass


class ProcessAgent(Player):
    kind = "process"

    def __init__(self, submission: Submission, python_executable: str | None = None):
        super().__init__(submission.name, submission.deck)
        self.submission = submission
        self.python = python_executable or sys.executable
        self.tree: ProcessTree | None = None
        self._pump: _StderrPump | None = None
        self._stderr_file = None
        self._exit_deadline: float | None = None
        self._stopped = False

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "kind": self.kind, "author": self.submission.manifest.get("author")}

    # ---------------------------------------------------------------------------------------- lifecycle

    def start(self, seat: SeatInfo) -> None:
        super().start(seat)
        self.dir = Path(seat.player_dir).resolve()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        self.action_path = self.dir / "action.json"
        self.work_dir = self.dir / "work"
        self.work_dir.mkdir(exist_ok=True)
        self.decisions_dir = self.dir / "decisions"
        if seat.config.keep_decisions:
            self.decisions_dir.mkdir(exist_ok=True)
        self.poll_s = max(0.001, seat.config.poll_interval_ms / 1000.0)
        self._stderr_file = open(self.dir / "stderr.log", "wb")
        self._budget = [int(seat.config.stderr_cap_kb) * 1024, False, threading.Lock()]
        self._launch()

    def _command(self) -> list[str]:
        cmd = list(self.submission.command)
        if cmd and cmd[0] in PYTHON_TOKENS:
            cmd[0] = self.python
        return cmd

    def _env(self) -> dict[str, str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("HS_")}
        env.update(
            {
                "HS_STATE_FILE": str(self.state_path),
                "HS_ACTION_FILE": str(self.action_path),
                "HS_WORK_DIR": str(self.work_dir),
                "HS_PLAYER": str(self.seat.player),
                "HS_GAME_ID": self.seat.game_id,
                "HS_PROTOCOL_VERSION": PROTOCOL_VERSION,
                "PYTHONUTF8": "1",
                "PYTHONUNBUFFERED": "1",
            }
        )
        for key in PASS_THROUGH_ENV:
            if key in os.environ:
                env[key] = os.environ[key]
        return env

    def _launch(self) -> None:
        import subprocess

        try:
            self.tree = ProcessTree(self._command(), cwd=str(self.submission.path), env=self._env(), stderr=subprocess.PIPE)
        except OSError as e:
            self.tree = None
            with self._budget[2]:
                self._stderr_file.write(f"[hs-arena] failed to start agent: {e}\n".encode())
                self._stderr_file.flush()
            return
        self._pump = _StderrPump(self.tree.proc.stderr, self._stderr_file, self._budget)
        self._pump.start()

    def _alive(self) -> bool:
        return self.tree is not None and self.tree.poll() is None

    def restart(self) -> None:
        super().restart()
        if self.tree is not None:
            self.tree.kill_tree()
        if self._pump is not None:
            self._pump.join(timeout=2)
        self.tree = None
        with self._budget[2]:
            self._stderr_file.write(f"\n[hs-arena] agent exited; restarting (restart #{self.restarts})\n".encode())
            self._stderr_file.flush()
        remove_file(self.action_path)

    # ---------------------------------------------------------------------------------------- protocol

    def _record(self, seq: int, name: str, obj: Any) -> None:
        if self.seat.config.keep_decisions:
            with open(self.decisions_dir / f"{seq:05d}.{name}.json", "w", encoding="utf-8", newline="\n") as f:
                json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))

    def _write_state(self, state: dict[str, Any]) -> None:
        atomic_write_json(self.state_path, state)
        self._record(state["seq"], "state", state)

    def poll_exit(self) -> Decision | None:
        if not self._alive():
            return Decision("exited", message="agent process exited before GAME OVER")
        return None

    def decide(self, state: dict[str, Any]) -> Decision:
        seq = state["seq"]
        self._write_state(state)
        t0 = time.monotonic()
        if self.tree is None:  # restarted after an exit: launch after the new state is in place
            self._launch()
        deadline = t0 + float(self.seat.config.decision_timeout_s)
        bad_sig = None
        bad_since = 0.0
        while True:
            text = read_text(self.action_path)
            if text is not None:
                try:
                    obj = json.loads(text)
                except ValueError:
                    now = time.monotonic()
                    sig = hash(text)
                    if sig != bad_sig:
                        bad_sig, bad_since = sig, now
                    elif now - bad_since >= BAD_JSON_SETTLE_S:
                        remove_file(self.action_path)
                        return Decision("bad_json", message="action.json is not valid JSON")
                else:
                    remove_file(self.action_path)
                    bad_sig = None
                    if not isinstance(obj, dict) or not _is_int(obj.get("seq")):
                        return Decision("bad_json", message="action.json must be an object with an integer 'seq'")
                    got = obj["seq"]
                    if got < seq:
                        continue  # late answer to an old state: dropped without penalty
                    if got > seq:
                        return Decision("seq_mismatch", message=f"action.json seq {got} is ahead of the pending seq {seq}")
                    action = obj.get("action")
                    if not isinstance(action, dict):
                        return Decision("bad_json", message="action.json must contain an 'action' object")
                    self._record(seq, "action", {"seq": seq, "action": sanitize_action(action)})
                    return Decision("action", action)
            if not self._alive():
                if os.path.exists(self.action_path):
                    continue  # answered just before exiting
                rc = self.tree.poll() if self.tree is not None else None
                return Decision("exited", message=f"agent process exited (code {rc}) before the game was over")
            if time.monotonic() >= deadline:
                return Decision(
                    "timeout",
                    message=f"no valid action.json for seq {seq} within {self.seat.config.decision_timeout_s:g} s",
                )
            time.sleep(self.poll_s)

    def game_over(self, state: dict[str, Any]) -> None:
        try:
            self._write_state(state)
        except OSError:
            pass
        self._exit_deadline = time.monotonic() + float(self.seat.config.exit_grace_s)

    def stop(self) -> None:
        if self._stopped:
            return
        self._stopped = True
        if self.tree is not None:
            if self._exit_deadline is not None:
                self.tree.wait(self._exit_deadline - time.monotonic())
            self.tree.kill_tree()  # also reaps anything the agent left behind
        if self._pump is not None:
            self._pump.join(timeout=5)
        if self._stderr_file is not None:
            try:
                self._stderr_file.close()
            except OSError:
                pass
        remove_file(self.action_path)
        tmp = self.action_path.with_name(self.action_path.name + ".tmp")
        remove_file(tmp)
        shutil.rmtree(self.work_dir, ignore_errors=True)
