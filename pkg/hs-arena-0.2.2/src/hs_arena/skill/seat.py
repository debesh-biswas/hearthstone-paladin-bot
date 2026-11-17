"""The skill seat: plays a student's skill with the course agent (PLANNING.md §6).

From the runner's point of view a SkillSeat is an ordinary player. Per game it:

- creates the agent's folder (a temporary directory): a copy of the skill, ``game/`` (the pending decision as
  ``state.json`` / ``state.txt`` and ``history.jsonl``) and ``scratch/`` (free space for the game);
- starts one agent session of the model the skill picked (Claude Haiku 5.5 in Claude Code, or GPT-6-Luna in
  Codex; effort medium) with the course prompt + SKILL.md, the folder as working directory, shell and file tools,
  no sub-agents, no web tools, and the seat's game MCP server (``wait`` / ``act`` / ``history``);
- publishes every state to the MCP server's mailbox and returns the action the agent submits with ``act``;
- forfeits on the first session exit before GAME OVER (``forfeit_exit``), retaining diagnostics for staff review;
- writes its logs to ``<game_dir>/pN/seat/`` (session transcripts, MCP calls, seat.json) and deletes the folder.

A ClientSeat is the same seat driven by a plain program (an MCP client, e.g. examples/greedy_mcp_client) instead
of a model; it costs nothing and is used for testing and as an example.
McpSeat uses the same communication with externally managed subagents and reads no student skill.
All three start without a deck; the agent submits its class and card list during deck_submission.
"""

from __future__ import annotations

import json
import os
import secrets
import shutil
import sys
import tempfile
import time
from importlib import resources
from pathlib import Path
from typing import Any

from .._fileio import atomic_write_json, read_text, remove_file, write_json
from ..agents._proctree import IS_WINDOWS, ProcessTree
from ..agents.base import Decision, Player, SeatInfo
from ..cards import load as load_cards
from ..pool import load_blacklist
from ..protocol import sanitize_action
from ..sdk.text import event_text, state_to_text
from .loader import EFFORT, NOT_SHOWN, Skill

CLAUDE_TOOLS = ("Bash", "Read", "Write", "Edit", "Glob", "Grep")
CODEX_DISABLED_FEATURES = ("multi_agent", "apps", "plugins", "browser_use", "computer_use", "image_generation",
                           "hooks", "memories")
# environment variables of a surrounding Claude Code / Codex session that must not leak into the seat's session
DROP_ENV_PREFIXES = ("HS_", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_SESSION", "CLAUDE_CODE_CHILD",
                     "CLAUDE_CODE_MESSAGING", "CLAUDE_CODE_EXECPATH", "CLAUDE_PID", "CLAUDE_EFFORT", "CODEX_THREAD_ID",
                     "CODEX_SANDBOX")
COPY_SKIP = {"__pycache__", ".git", ".venv", "venv", "node_modules", ".DS_Store"}
SCRATCH_COPY_LIMIT = 20 * 1024 * 1024
COURSE_ERROR_HINTS = ("api error", "authenticat", "login", "log in", "credit", "rate limit", "rate_limit", "overloaded",
                      "quota", "usage limit", "network", "econn", "enotfound", "timed out", "connection",
                      "not recognized", "no such file", "command not found", "unauthorized", "forbidden")


def course_prompt_template() -> str:
    return resources.files("hs_arena.skill").joinpath("course_prompt.md").read_text(encoding="utf-8")


def system_prompt(skill: Skill, player: int | str = "N", timeout: float = 180, illegal_limit: int = 3) -> str:
    return course_prompt_template().format(player=player, timeout=f"{timeout:g}", illegal_limit=illegal_limit,
                                           python=sys.executable, name=skill.name, description=skill.description,
                                           body=skill.body)


def user_prompt(player: int) -> str:
    return f"You are player {player}. Your arena tools are connected to your seat. Call wait now."


def session_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(DROP_ENV_PREFIXES)}
    bindir = str(Path(sys.executable).parent)
    env["PATH"] = bindir + os.pathsep + env.get("PATH", "")  # `python` = the interpreter running hs-arena
    env.update({"PYTHONUTF8": "1", "PYTHONUNBUFFERED": "1", "PYTHONDONTWRITEBYTECODE": "1"})
    return env


def mcp_server_command(box: Path) -> list[str]:
    return [sys.executable, "-m", "hs_arena.skill.mcp_server", str(box)]


def claude_command(model_id: str, box: Path, system_file: Path) -> list[str]:
    server = {"command": sys.executable, "args": ["-m", "hs_arena.skill.mcp_server", str(box)]}
    exe = shutil.which("claude") or "claude"
    return [exe, "-p", "--model", model_id, "--effort", EFFORT, "--output-format", "stream-json", "--verbose",
            "--no-session-persistence", "--strict-mcp-config", "--mcp-config", json.dumps({"mcpServers": {"arena": server}}),
            "--tools", ",".join(CLAUDE_TOOLS),
            "--allowedTools", "mcp__arena__wait", "mcp__arena__act", "mcp__arena__history", *CLAUDE_TOOLS,
            "--disable-slash-commands", "--settings", json.dumps({"disableAllHooks": True}),
            "--permission-mode", "dontAsk", "--append-system-prompt-file", str(system_file)]


def codex_command(model_id: str, box: Path, folder: Path, path_env: str | None = None) -> list[str]:
    exe = shutil.which("codex") or "codex"
    cmd = [exe, "exec", "--ignore-user-config", "--ephemeral", "--skip-git-repo-check", "-m", model_id,
           "-s", "workspace-write", "-C", str(folder), "--json", "--color", "never",
           "-c", f'model_reasoning_effort="{EFFORT}"', "-c", 'approval_policy="never"', "-c", 'web_search="disabled"',
           "-c", "project_doc_max_bytes=0", "-c", "allow_login_shell=false"]  # no shell profile (e.g. conda init)
    # Codex's sandbox builds the shell environment itself: pass PATH so that `python` is the runtime's interpreter
    env_set = {"PATH": path_env or session_env()["PATH"], "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"}
    for key, value in env_set.items():
        cmd += ["-c", f"shell_environment_policy.set.{key}={json.dumps(value)}"]
    if IS_WINDOWS:
        cmd += ["-c", 'windows.sandbox="unelevated"']
    for feature in CODEX_DISABLED_FEATURES:
        cmd += ["--disable", feature]
    server = {"command": sys.executable, "args": ["-m", "hs_arena.skill.mcp_server", str(box)], "tool_timeout_sec": 120,
              "startup_timeout_sec": 60, "required": True, "default_tools_approval_mode": "approve"}
    for key, value in server.items():
        cmd += ["-c", f"mcp_servers.arena.{key}={json.dumps(value)}"]
    return cmd + ["-"]


def _jsonl(path: Path) -> list[dict[str, Any]]:
    out = []
    try:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            if isinstance(obj, dict):
                out.append(obj)
    except OSError:
        pass
    return out


def classify_stop(harness: str, transcript: Path, stderr_path: Path, rc: int | None) -> tuple[str, str]:
    """Who caused a session that stopped before the game was over: ("course" | "skill", detail)."""
    events = _jsonl(transcript)
    try:
        err = stderr_path.read_text(encoding="utf-8", errors="replace")[-2000:]
    except OSError:
        err = ""
    if harness == "client":
        return "skill", f"the client program exited with code {rc}"
    if harness == "claude":
        results = [e for e in events if e.get("type") == "result"]
        if results:
            r = results[-1]
            if r.get("is_error"):
                detail = r.get("result") or r.get("subtype") or "error"
                return "course", f"Claude Code reported an error: {str(detail)[:300]} (api status {r.get('api_error_status')})"
            return "skill", "the model ended its session before GAME OVER"
    elif harness == "codex":
        failed = [e for e in events if e.get("type") in ("turn.failed", "error")]
        if failed:
            e = failed[-1]
            msg = e.get("message") or (e.get("error") or {}).get("message") or json.dumps(e)[:300]
            return "course", f"Codex reported an error: {str(msg)[:300]}"
        if any(e.get("type") == "turn.completed" for e in events):
            return "skill", "the model ended its session before GAME OVER"
    low = err.lower()
    hint = next((h for h in COURSE_ERROR_HINTS if h in low), None)
    tail = " ".join(err.split())[-300:]
    if hint or not events:
        return "course", f"the {harness} session failed (exit code {rc}): {tail or 'no output'}"
    return "course", f"the {harness} session stopped without a reason (exit code {rc}); treated as course side"


def _copy_skill(src: Path, dst: Path) -> None:
    for p in src.iterdir():
        if p.name in COPY_SKIP or p.name in NOT_SHOWN:
            continue
        if p.is_dir():
            shutil.copytree(p, dst / p.name, ignore=shutil.ignore_patterns(*COPY_SKIP, "*.pyc"))
        else:
            shutil.copy2(p, dst / p.name)


def _write_card_pool(folder: Path) -> None:
    blacklist = load_blacklist()
    write_json(folder / "game" / "card_pool.json", {
        key: card for key, card in sorted(load_cards().items()) if key not in blacklist
    })


def _make_root() -> Path:
    """A fresh directory under the system temp dir with ordinary permissions. (tempfile.mkdtemp uses mode 0o700,
    which on Windows with Python 3.13+ locks out Codex's sandbox account: the agent could not use its folder.)"""
    base = Path(tempfile.gettempdir())
    while True:
        p = base / f"hs-seat-{secrets.token_hex(5)}"
        try:
            p.mkdir()
            return p
        except FileExistsError:
            continue


def _dir_size(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def _atomic_write_text(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8", newline="\n")
    for _ in range(500):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.01)
    os.replace(tmp, path)


class SkillSeat(Player):
    kind = "skill"
    requires_deck_submission = True
    harness_name: str

    def __init__(self, skill: Skill):
        super().__init__(skill.name)
        self.skill = skill
        self.source = skill.path
        self.harness_name = skill.harness
        self._init_state()

    def _init_state(self) -> None:
        self.session: ProcessTree | None = None
        self.session_no = 0
        self.skill_stops = 0
        self.course_stops = 0
        self.root: Path | None = None
        self._files: list[Any] = []
        self._exit_deadline: float | None = None
        self._stopped = False
        self._log: list[dict[str, Any]] = []
        self._stderr = None

    def describe(self) -> dict[str, Any]:
        return {"name": self.name, "kind": self.kind, "harness": self.harness_name}

    # ------------------------------------------------------------------------------------------- lifecycle

    def start(self, seat: SeatInfo) -> None:
        super().start(seat)
        self.pdir = Path(seat.player_dir).resolve()
        self.pdir.mkdir(parents=True, exist_ok=True)
        self.log_dir = self.pdir / "seat"
        self.log_dir.mkdir(exist_ok=True)
        self.decisions_dir = self.pdir / "decisions"
        if seat.config.keep_decisions:
            self.decisions_dir.mkdir(exist_ok=True)
        self.poll_s = max(0.01, seat.config.poll_interval_ms / 1000.0)
        self._stderr = open(self.pdir / "stderr.log", "a", encoding="utf-8")
        self.root = _make_root()
        self.folder = self.root / "agent"
        self.box = self.root / "mailbox"
        self.folder.mkdir()
        self.box.mkdir()
        _copy_skill(self.source, self.folder)
        (self.folder / "game").mkdir()
        _write_card_pool(self.folder)
        (self.folder / "scratch").mkdir()
        (self.box / "history.txt").write_text("", encoding="utf-8")
        (self.folder / "game" / "history.jsonl").write_text("", encoding="utf-8")
        self._prepare()
        self.say(f"{self.kind} seat: {self.describe_harness()}; agent folder {self.folder}")
        self._launch()

    def _prepare(self) -> None:
        cfg = self.seat.config
        self.system_file = self.root / "system_prompt.md"
        self.system_file.write_text(system_prompt(self.skill, self.seat.player, cfg.decision_timeout_s, cfg.illegal_limit),
                                    encoding="utf-8", newline="\n")
        shutil.copy2(self.system_file, self.log_dir / "system_prompt.md")

    def describe_harness(self) -> str:
        return f"{self.skill.model} = {self.skill.model_id} via {self.harness_name}, effort {EFFORT}"

    def say(self, msg: str) -> None:
        if self._stderr is not None:
            self._stderr.write(time.strftime("%H:%M:%S ") + "[seat] " + msg + "\n")
            self._stderr.flush()

    def note(self, msg: str) -> None:
        self.notes.append(msg)
        self.say(msg)

    # ------------------------------------------------------------------------------------------- sessions

    def _session_command(self, prompt: str) -> tuple[list[str], str | None]:
        """(command, stdin text) of one agent session."""
        if self.harness_name == "claude":
            return claude_command(self.skill.model_id, self.box, self.system_file), prompt
        system = self.system_file.read_text(encoding="utf-8")
        return codex_command(self.skill.model_id, self.box, self.folder, self._env()["PATH"]), system + "\n\n" + prompt

    def _launch(self) -> None:
        self._close_session()
        self.session_no += 1
        n = self.session_no
        prompt = user_prompt(self.seat.player)
        cmd, stdin_text = self._session_command(prompt)
        stdin_path = self.root / f"stdin_{n}.txt"
        stdin_path.write_text(stdin_text or "", encoding="utf-8", newline="\n")
        self.transcript = self.log_dir / f"session_{n}.jsonl"
        self.session_err = self.log_dir / f"session_{n}.err"
        fin = open(stdin_path, "r", encoding="utf-8")
        fout = open(self.transcript, "w", encoding="utf-8")
        ferr = open(self.session_err, "w", encoding="utf-8")
        self._files = [fin, fout, ferr]
        shown = [c if len(c) < 400 else c[:60] + "...<trimmed>" for c in cmd]
        self._log.append({"session": n, "started": round(time.time(), 3),
                          "command": shown, "prompt": prompt})
        try:
            self.session = ProcessTree(cmd, cwd=str(self.folder), env=self._env(), stderr=ferr, stdin=fin, stdout=fout)
        except OSError as e:
            self.session = None
            ferr.write(f"failed to start: {e}\n")
            ferr.flush()
            self.say(f"session {n}: failed to start {cmd[0]}: {e}")
            return
        self.say(f"session {n} started (pid {self.session.pid})")

    def _env(self) -> dict[str, str]:
        return session_env()

    def _close_session(self) -> None:
        if self.session is not None and self.session.poll() is None:
            self.session.kill_tree()
        for f in self._files:
            try:
                f.close()
            except OSError:
                pass
        self._files = []

    def _session_alive(self) -> bool:
        return self.session is not None and self.session.poll() is None

    def _on_session_stop(self) -> Decision | None:
        """Any early exit forfeits; preserve the cause for staff review, never relaunch."""
        rc = self.session.poll() if self.session is not None else None
        self._close_session()
        cause, detail = classify_stop(self.harness_name, self.transcript, self.session_err, rc)
        n = self.session_no
        self._log[-1].update({"stopped": round(time.time(), 3), "exit_code": rc, "cause": cause, "detail": detail})
        if cause == "course":
            self.course_stops += 1
        else:
            self.skill_stops += 1
        self.note(f"session {n} stopped before GAME OVER ({cause}: {detail}); game lost (forfeit_exit). "
                  "Staff may review verified course-side failures separately.")
        return Decision("exited", message=f"agent session ended before GAME OVER: {detail}")

    # ------------------------------------------------------------------------------------------- decisions

    def _who(self, i):
        me = self.seat.player
        if i is None:
            return "nobody"
        return f"P{i} (you)" if i == me else f"P{i} (opponent)"

    def _record(self, seq: int, name: str, obj: Any) -> None:
        if self.seat.config.keep_decisions:
            with open(self.decisions_dir / f"{seq:05d}.{name}.json", "w", encoding="utf-8", newline="\n") as f:
                json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))

    def _publish(self, state: dict[str, Any]) -> str:
        text = state_to_text(state)
        events = state.get("events") or []
        if events:
            with open(self.folder / "game" / "history.jsonl", "a", encoding="utf-8", newline="\n") as f:
                for ev in events:
                    f.write(json.dumps(ev, ensure_ascii=False, separators=(",", ":")) + "\n")
            with open(self.box / "history.txt", "a", encoding="utf-8", newline="\n") as f:
                for ev in events:
                    f.write(event_text(ev, self._who) + "\n")
        atomic_write_json(self.folder / "game" / "state.json", state)
        _atomic_write_text(self.folder / "game" / "state.txt", text + "\n")
        self._record(state["seq"], "state", state)
        return text

    def poll_exit(self) -> Decision | None:
        return None if self._session_alive() else self._on_session_stop()

    def decide(self, state: dict[str, Any]) -> Decision:
        seq = state["seq"]
        text = self._publish(state)
        _atomic_write_text(self.box / "state.txt", text)
        atomic_write_json(self.box / "state.json", {"seq": seq, "phase": state["phase"]})
        deadline = time.monotonic() + float(self.seat.config.decision_timeout_s)
        action_path = self.box / "action.json"
        while True:
            if self._decision_cancelled.is_set():
                return Decision("cancelled", message="game ended during deck submission")
            raw = read_text(action_path)
            if raw is not None:
                try:
                    obj = json.loads(raw)
                except ValueError:
                    obj = None
                if isinstance(obj, dict) and obj.get("seq") == seq and isinstance(obj.get("action"), dict):
                    remove_file(action_path)
                    self._record(seq, "action", {"seq": seq, "action": sanitize_action(obj["action"])})
                    return Decision("action", obj["action"])
                if isinstance(obj, dict) and isinstance(obj.get("seq"), int) and obj["seq"] < seq:
                    remove_file(action_path)  # late answer to an old seq
            if not self._session_alive():
                d = self._on_session_stop()
                if d is not None:
                    return d
            if time.monotonic() >= deadline:
                return Decision("timeout", message=f"no action for seq {seq} within {self.seat.config.decision_timeout_s:g} s")
            time.sleep(self.poll_s)

    def game_over(self, state: dict[str, Any]) -> None:
        try:
            text = self._publish(state)
            _atomic_write_text(self.box / "game_over.txt", text)
        except OSError:
            pass
        # a model session writes a short closing message after GAME OVER; give it a little more than exit_grace_s
        self._exit_deadline = time.monotonic() + max(float(self.seat.config.exit_grace_s), 30.0)

    def stop(self) -> None:
        if self._stopped or self.root is None:
            return
        self._stopped = True
        if self.session is not None and self._exit_deadline is not None:
            self.session.wait(self._exit_deadline - time.monotonic())
        self._close_session()
        try:
            if (self.box / "calls.jsonl").exists():
                shutil.copy2(self.box / "calls.jsonl", self.log_dir / "mcp_calls.jsonl")
            scratch = self.folder / "scratch"
            if scratch.exists() and any(scratch.iterdir()) and _dir_size(scratch) <= SCRATCH_COPY_LIMIT:
                shutil.copytree(scratch, self.log_dir / "scratch", dirs_exist_ok=True)
            write_json(self.log_dir / "seat.json", {
                "name": self.name, "kind": self.kind, "harness": self.harness_name,
                "model": getattr(self.skill, "model", None), "model_id": getattr(self.skill, "model_id", None),
                "effort": EFFORT if self.harness_name in ("claude", "codex") else None,
                "skill_stops": self.skill_stops, "course_stops": self.course_stops, "notes": self.notes,
                "usage": self.usage(), "sessions": self._log})
        except OSError as e:
            self.say(f"could not save seat logs: {e}")
        if self._stderr is not None:
            self._stderr.close()
            self._stderr = None
        for _ in range(20):
            shutil.rmtree(self.root, ignore_errors=True)
            if not self.root.exists():
                break
            time.sleep(0.25)

    def usage(self) -> dict[str, Any]:
        """Token / cost totals over this game's sessions, from the transcripts."""
        total: dict[str, Any] = {}
        for p in sorted(self.log_dir.glob("session_*.jsonl")):
            for e in _jsonl(p):
                if self.harness_name == "claude" and e.get("type") == "result":
                    total["cost_usd_list_price"] = round(total.get("cost_usd_list_price", 0) + (e.get("total_cost_usd") or 0), 6)
                    for k, v in (e.get("usage") or {}).items():
                        if isinstance(v, (int, float)):
                            total[k] = total.get(k, 0) + v
                elif self.harness_name == "codex" and e.get("type") == "turn.completed":
                    for k, v in (e.get("usage") or {}).items():
                        if isinstance(v, (int, float)):
                            total[k] = total.get(k, 0) + v
        return total


class ClientSeat(SkillSeat):
    """A seat driven by a program instead of a model: `client:<dir>` with client.py.

    The program is started in the agent's folder (a copy of <dir> plus game/ and scratch/) with the environment
    variable HS_ARENA_MCP holding the command (JSON list) that starts this seat's game MCP server. It is an MCP
    client like Claude Code or Codex: it starts the server, calls wait / act / history and reads game/state.json.
    """

    kind = "client"

    def __init__(self, path: str | Path):
        path = Path(path).resolve()
        if not (path / "client.py").exists():
            raise FileNotFoundError(f"{path / 'client.py'}: not found (a client seat needs client.py)")
        Player.__init__(self, path.name)
        self.skill = None
        self.source = path
        self.harness_name = "client"
        self._init_state()

    def describe_harness(self) -> str:
        return "client.py (MCP client program, no model)"

    def _prepare(self) -> None:
        self.system_file = None

    def _session_command(self, prompt: str) -> tuple[list[str], str | None]:
        return [sys.executable, "client.py"], None

    def _env(self) -> dict[str, str]:
        env = session_env()
        env["HS_ARENA_MCP"] = json.dumps(mcp_server_command(self.box))
        return env


class McpSeat(SkillSeat):
    """An externally launched agent: mcp:<workspace>, no skill parsing or process launcher.

    The orchestrator gives its subagent this workspace and connects the stdio MCP command
    `python -m hs_arena.skill.mcp_server <workspace>/arena-mailbox`. Use a fresh workspace
    for each game; the host preserves it and never starts or kills the external agent.
    """

    kind = "mcp"

    def __init__(self, path: str | Path):
        self.workspace = Path(path).resolve()
        Player.__init__(self, self.workspace.name)
        self.harness_name = "external"
        self._init_state()

    def start(self, seat: SeatInfo) -> None:
        Player.start(self, seat)
        self.pdir = Path(seat.player_dir).resolve()
        self.log_dir = self.pdir / "seat"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.decisions_dir = self.pdir / "decisions"
        if seat.config.keep_decisions:
            self.decisions_dir.mkdir(exist_ok=True)
        self.poll_s = max(0.01, seat.config.poll_interval_ms / 1000.0)
        self.folder = self.workspace
        self.folder.mkdir(parents=True, exist_ok=True)
        self.box = self.folder / "arena-mailbox"
        # Refuse stale state instead of letting an old seq or GAME OVER answer a new game.
        if (self.folder / "game").exists() or any((self.box / name).exists() for name in
                ("state.json", "action.json", "answered.txt", "game_over.txt")):
            raise FileExistsError(f"{self.workspace}: use a fresh MCP workspace for each game")
        self.box.mkdir(exist_ok=True)  # the external MCP server may have started first
        (self.folder / "game").mkdir()
        _write_card_pool(self.folder)
        (self.folder / "scratch").mkdir(exist_ok=True)
        (self.box / "history.txt").write_text("", encoding="utf-8")
        (self.folder / "game" / "history.jsonl").write_text("", encoding="utf-8")

    def _session_alive(self) -> bool:
        return True  # lifecycle belongs to the external orchestrator; missing answers time out

    def stop(self) -> None:
        if self._stopped:
            return
        self._stopped = True
        if (self.box / "calls.jsonl").exists():
            shutil.copy2(self.box / "calls.jsonl", self.log_dir / "mcp_calls.jsonl")
        write_json(self.log_dir / "seat.json", {"name": self.name, "kind": self.kind, "harness": "external",
                                               "notes": self.notes})
