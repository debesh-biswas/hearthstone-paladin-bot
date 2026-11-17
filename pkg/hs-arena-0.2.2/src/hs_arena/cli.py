"""hs-arena command line: play, validate, prompt, replay, cards, version."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import FIREPLACE_COMMIT, POOL_VERSION, PROTOCOL_VERSION, RUNTIME_VERSION
from .protocol import Config


def _configure_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


# --------------------------------------------------------------------------------------------- helpers

def _check_spec(spec: str) -> list[str]:
    """Return problems with a player spec (empty if OK)."""
    from .agents import is_builtin, make_player, spec_path
    from .deck import DeckError, SubmissionError
    from .skill import SkillError

    if not is_builtin(spec) and not Path(spec_path(spec) or "").is_dir():
        return [f"{spec}: not a directory"]
    try:
        make_player(spec, 1, 0)
    except DeckError as e:
        return [f"{spec}: invalid deck: {msg}" for msg in e.errors]
    except (SubmissionError, SkillError) as e:
        return [f"{spec}: {msg}" for msg in e.errors]
    except OSError as e:
        return [f"{spec}: {e}"]
    return []


def _allocate_game_ids(out: Path, n: int) -> list[str]:
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    prefix = f"g_{day}_"
    used = 0
    if out.exists():
        for p in out.iterdir():
            m = re.fullmatch(re.escape(prefix) + r"(\d{6})", p.name)
            if m:
                used = max(used, int(m.group(1)))
    return [f"{prefix}{used + k + 1:06d}" for k in range(n)]


def _player_label(spec: str) -> str:
    """The player's name as in game.json: skill name, client dir name, manifest name, or the built-in spec."""
    from .agents import spec_kind, spec_path
    from .deck import SubmissionError, load_submission
    from .skill import SkillError, load_skill

    kind = spec_kind(spec)
    if kind in ("random", "greedy"):
        return spec
    path = Path(spec_path(spec) or spec)
    try:
        if kind == "skill":
            return load_skill(path).name
        if kind == "process":
            return load_submission(path).name
    except (SubmissionError, SkillError, OSError):
        pass
    return path.resolve().name


def _game_line(r: dict[str, Any]) -> str:
    w = r.get("winner")
    winner = f"P{w}" if w else "none"
    s = (
        f"{r['game_id']}  winner {winner:4s} {r['reason']:<17s} turns {r['turns']:>3}  "
        f"illegal {r['illegal_counts']['1']}/{r['illegal_counts']['2']}  "
        f"restarts {r['restarts']['1']}/{r['restarts']['2']}  "
        f"timeouts {r['timeouts']['1']}/{r['timeouts']['2']}  {r['duration_s']:.1f}s"
    )
    if r.get("engine_error"):
        s += f"  VOID: cards {' '.join(r['engine_error']['card_ids'])}"
    for side, notes in sorted((r.get("notes") or {}).items()):
        for n in notes:
            s += f"\n    P{side} seat: {n}"
    return s


def _run_one(args: tuple) -> dict[str, Any]:
    p1, p2, game_dir, game_id, seed, config = args
    from .runner import run_game

    try:
        return run_game(p1, p2, game_dir=game_dir, game_id=game_id, seed=seed, config=config)
    except Exception as e:  # runtime bug: report it as a failed game instead of losing the batch
        import traceback

        return {"game_id": game_id, "error": f"{type(e).__name__}: {e}", "traceback": traceback.format_exc()}


def _summary(results: list[dict[str, Any]], p1: str, p2: str) -> str:
    done = [r for r in results if "error" not in r]
    voided = [r for r in done if r["reason"] == "void_engine_error"]
    counted = [r for r in done if r["reason"] not in ("void_engine_error", "aborted")]
    w1 = sum(1 for r in counted if r["winner"] == 1)
    w2 = sum(1 for r in counted if r["winner"] == 2)
    draws = sum(1 for r in counted if r["winner"] is None)
    ill1 = sum(r["illegal_counts"]["1"] for r in done)
    ill2 = sum(r["illegal_counts"]["2"] for r in done)
    lines = [
        "",
        f"{'side':<6}{'player':<28}{'wins':>6}{'illegal':>9}",
        f"{'P1':<6}{_player_label(p1)[:27]:<28}{w1:>6}{ill1:>9}",
        f"{'P2':<6}{_player_label(p2)[:27]:<28}{w2:>6}{ill2:>9}",
        f"games {len(results)}  counted {len(counted)}  draws {draws}  voided {len(voided)}  "
        f"failed {len(results) - len(done)}",
    ]
    for r in voided:
        lines.append(f"  voided {r['game_id']}: {r['engine_error']['message']}  cards {' '.join(r['engine_error']['card_ids'])}")
    for r in results:
        if "error" in r:
            lines.append(f"  failed {r['game_id']}: {r['error']}")
    return "\n".join(lines)


# --------------------------------------------------------------------------------------------- commands

def cmd_play(a: argparse.Namespace) -> int:
    from .agents import spec_kind, spec_path

    problems = _check_spec(a.p1) + _check_spec(a.p2)
    external = [Path(spec_path(s)).resolve() for s in (a.p1, a.p2) if spec_kind(s) == "mcp"]
    if external and a.games != 1:
        problems.append("external MCP seats need a fresh workspace per game; use --games 1")
    if len(external) == 2 and external[0] == external[1]:
        problems.append("the two MCP seats must use different workspaces")
    if problems:
        for p in problems:
            print(f"error: {p}", file=sys.stderr)
        return 2
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    seed = a.seed if a.seed is not None else random.SystemRandom().randrange(1, 2**31)
    config = Config(
        decision_timeout_s=a.timeout,
        max_turns=a.max_turns,
        keep_decisions=a.keep_decisions,
        illegal_limit=a.illegal_limit,
        exit_grace_s=a.exit_grace,
    )
    ids = _allocate_game_ids(out, a.games)
    jobs = [(a.p1, a.p2, out / gid, gid, seed + k, config) for k, gid in enumerate(ids)]
    parallel = max(1, min(a.parallel, a.games))
    print(f"hs-arena {RUNTIME_VERSION}: {a.games} game(s) P1={_player_label(a.p1)} vs P2={_player_label(a.p2)} "
          f"seed {seed} parallel {parallel} -> {out}", flush=True)
    results: list[dict[str, Any]] = []
    if parallel == 1:
        for job in jobs:
            r = _run_one(job)
            results.append(r)
            print(_game_line(r) if "error" not in r else f"{r['game_id']}  FAILED {r['error']}", flush=True)
    else:
        import multiprocessing as mp
        from concurrent.futures import ProcessPoolExecutor, as_completed

        with ProcessPoolExecutor(max_workers=parallel, mp_context=mp.get_context("spawn")) as pool:
            futures = [pool.submit(_run_one, job) for job in jobs]
            try:
                for f in as_completed(futures):
                    r = f.result()
                    results.append(r)
                    print(_game_line(r) if "error" not in r else f"{r['game_id']}  FAILED {r['error']}", flush=True)
            except KeyboardInterrupt:
                for f in futures:
                    f.cancel()
                raise
        results.sort(key=lambda r: r["game_id"])
    for r in results:
        if "traceback" in r:
            print(r["traceback"], file=sys.stderr)
    print(_summary(results, a.p1, a.p2))
    return 0 if all("error" not in r for r in results) else 1


def _validate_skill(a: argparse.Namespace, path: Path) -> int:
    import shutil

    from .runner import run_game
    from .skill import MODELS, SkillError, load_skill

    print(f"Validating skill {path.resolve()}")
    try:
        skill = load_skill(path)
    except SkillError as e:
        for w in e.warnings:
            print(f"  warning: {w}")
        for err in e.errors:
            print(f"  ERROR: {err}")
        print("FAILED: fix the errors above.")
        return 1
    for w in skill.warnings:
        print(f"  warning: {w}")
    print(f"  SKILL.md: OK (name {skill.name!r}, model {skill.model} = {MODELS[skill.model]['label']}, effort medium)")
    print("  deck: chosen by the agent via MCP submit_deck at the start of each game (deck.json is optional)")
    for sub in ("scripts", "references"):
        d = skill.path / sub
        if d.is_dir():
            print(f"  {sub}/: {sum(1 for f in d.rglob('*') if f.is_file())} file(s)")
    if skill.requirements:
        print(f"  requirements.txt: {len(skill.requirements)} package(s); for local games install them into this "
              f"environment (pip install -r {skill.path / 'requirements.txt'}); the server installs them for you")
    exe = shutil.which(skill.harness)
    tool = "Claude Code" if skill.harness == "claude" else "the Codex CLI"
    harness_msg = f"'{skill.harness}' not found on PATH: install {tool} and log in"
    if a.no_game:
        if not exe:
            print(f"  warning: {harness_msg}")
        print("OK (smoke game skipped)")
        return 0
    if not exe:
        print(f"  ERROR: {harness_msg}")
        print("FAILED.")
        return 1
    print(f"  harness: {exe}")
    out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix="hs-validate-"))
    out.mkdir(parents=True, exist_ok=True)
    seed = a.seed if a.seed is not None else 1
    gid = _allocate_game_ids(out, 1)[0]
    config = Config(decision_timeout_s=a.timeout, keep_decisions=True)
    print(f"  smoke game vs random (seed {seed}, timeout {a.timeout:g} s; one real agent session with your login) "
          f"-> {out / gid}", flush=True)
    r = run_game(f"skill:{path}", "random", game_dir=out / gid, game_id=gid, seed=seed, config=config)
    print("  " + _game_line(r))
    problems = []
    if r["reason"].startswith("forfeit_") and r["winner"] == 2:
        problems.append(f"the skill lost by {r['reason']}")
    if r["timeouts"]["1"]:
        problems.append(f"the agent timed out {r['timeouts']['1']} time(s)")
    if r["restarts"]["1"]:
        problems.append(f"the agent session failed {r['restarts']['1']} time(s) and was restarted")
    if r["reason"] == "void_engine_error":
        print(f"  note: the game was voided by an engine error ({r['engine_error']['message']}); not your fault")
    if r["illegal_counts"]["1"] and not problems:
        print(f"  warning: {r['illegal_counts']['1']} illegal action(s); see {out / gid / 'replay.jsonl'}")
    logs = out / gid / "p1"
    if problems:
        for prob in problems:
            print(f"  ERROR: {prob}")
        print(f"FAILED. Seat logs: {logs / 'seat'} and {logs / 'stderr.log'}")
        return 1
    print(f"OK. Seat logs: {logs / 'seat'}")
    return 0


def cmd_validate(a: argparse.Namespace) -> int:
    from .deck import SubmissionError, load_submission
    from .runner import run_game
    from .skill import is_skill_dir

    path = Path(a.submission)
    if is_skill_dir(path) or not (path / "manifest.json").exists():
        return _validate_skill(a, path)
    print(f"Validating submission {path.resolve()}")
    try:
        sub = load_submission(path)
    except SubmissionError as e:
        for w in e.warnings:
            print(f"  warning: {w}")
        for err in e.errors:
            print(f"  ERROR: {err}")
        print("FAILED: fix the errors above.")
        return 1
    from .deck import validate_manifest_data

    for w in validate_manifest_data(sub.manifest).warnings:
        print(f"  warning: {w}")
    print(f"  manifest.json: OK (name {sub.name!r}, author {sub.manifest['author']!r}, command {sub.command})")
    print(f"  deck.json: OK ({sub.deck.hero_class}, {len(sub.deck.cards)} cards)")
    if a.no_game:
        print("OK (smoke game skipped)")
        return 0
    out = Path(a.out) if a.out else Path(tempfile.mkdtemp(prefix="hs-validate-"))
    out.mkdir(parents=True, exist_ok=True)
    seed = a.seed if a.seed is not None else 1
    gid = _allocate_game_ids(out, 1)[0]
    config = Config(decision_timeout_s=a.timeout, keep_decisions=True)
    print(f"  smoke game vs random (seed {seed}, timeout {a.timeout:g} s) -> {out / gid}", flush=True)
    r = run_game(str(path), "random", game_dir=out / gid, game_id=gid, seed=seed, config=config)
    print("  " + _game_line(r))
    problems = []
    if r["reason"].startswith("forfeit_") and r["winner"] == 2:
        problems.append(f"the agent forfeited: {r['reason']}")
    if r["restarts"]["1"]:
        problems.append(f"the agent process exited {r['restarts']['1']} time(s) before the game was over")
    if r["timeouts"]["1"]:
        problems.append(f"the agent timed out {r['timeouts']['1']} time(s)")
    if r["reason"] == "void_engine_error":
        print(f"  note: the game was voided by an engine error ({r['engine_error']['message']}); not your fault")
    if r["illegal_counts"]["1"] and not problems:
        print(f"  warning: {r['illegal_counts']['1']} illegal action(s); see {out / gid / 'replay.jsonl'}")
    stderr_log = out / gid / "p1" / "stderr.log"
    if problems:
        for p in problems:
            print(f"  ERROR: {p}")
        print(f"FAILED. Agent stderr: {stderr_log}")
        return 1
    print(f"OK. Agent stderr: {stderr_log}")
    return 0


def cmd_prompt(a: argparse.Namespace) -> int:
    from .skill import SkillError, load_skill
    from .skill.seat import system_prompt, user_prompt

    try:
        skill = load_skill(a.skill)
    except SkillError as e:
        for err in e.errors:
            print(f"error: {err}", file=sys.stderr)
        return 1
    print(system_prompt(skill, a.player, a.timeout))
    print("\n----- first message -----")
    print(user_prompt(a.player))
    return 0


def cmd_replay(a: argparse.Namespace) -> int:
    from .replay import render_path

    try:
        print(render_path(a.path))
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


def cmd_cards(a: argparse.Namespace) -> int:
    from . import cards

    catalog = list(cards.load().values())
    if a.card_class:
        cls = a.card_class.upper()
        catalog = [c for c in catalog if c["card_class"] in (cls, "NEUTRAL")] if not a.only else [
            c for c in catalog if c["card_class"] == cls
        ]
    if a.json:
        print(json.dumps(catalog, indent=1, ensure_ascii=False))
        return 0
    for c in catalog:
        if c["type"] == "MINION":
            stats = f"{c['attack']}/{c['health']}"
        elif c["type"] == "WEAPON":
            stats = f"{c['attack']}/{c['durability']}"
        else:
            stats = ""
        print(f"{c['id']:<10} {c['cost']:>2}  {c['name'][:28]:<28} {c['card_class']:<8} {c['type']:<7} {stats:<6} {c['text']}")
    print(f"{len(catalog)} cards (pool {POOL_VERSION})")
    return 0


def cmd_version(a: argparse.Namespace) -> int:
    print(f"hs-arena runtime {RUNTIME_VERSION}")
    print(f"protocol version {PROTOCOL_VERSION}")
    print(f"pool version {POOL_VERSION}")
    print(f"fireplace commit {FIREPLACE_COMMIT}")
    print(f"python {sys.version.split()[0]} ({sys.executable})")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hs-arena", description="Hearthstone Agent Arena runtime (CS 598 HW2).")
    sub = p.add_subparsers(dest="command", metavar="COMMAND")

    sp = sub.add_parser("play", help="play games between two players", description=(
        "Play games. A player is 'skill:<dir>' (a skill, played by the course agent with your Claude Code or Codex "
        "login), 'client:<dir>' (an MCP client program), 'mcp:<workspace>' (externally launched agent), 'greedy', 'random', 'greedy:<deck.json>' or "
        "'random:<deck.json>'."))
    sp.add_argument("--p1", required=True,
                    help="player 1 (skill:<dir> | client:<dir> | greedy | random | greedy:<deck> | random:<deck>)")
    sp.add_argument("--p2", required=True, help="player 2 (same forms as --p1)")
    sp.add_argument("--games", type=int, default=1, help="number of games (default 1)")
    sp.add_argument("--seed", type=int, default=None, help="base seed; game k uses seed+k (default: random)")
    sp.add_argument("--out", default="games", help="output directory for game folders (default ./games)")
    sp.add_argument("--parallel", type=int, default=4, help="games run in parallel (default 4)")
    sp.add_argument("--keep-decisions", dest="keep_decisions", action="store_true", default=True,
                    help="keep every state/action pair under pN/decisions/ (default on)")
    sp.add_argument("--no-keep-decisions", dest="keep_decisions", action="store_false",
                    help="do not keep decision files")
    sp.add_argument("--timeout", type=float, default=180.0, help="decision timeout in seconds (default 180)")
    sp.add_argument("--max-turns", type=int, default=None, help="end the game as a draw after this many turns (default off)")
    sp.add_argument("--illegal-limit", type=int, default=3, help="forfeit on reaching this many illegal actions (default 3)")
    sp.add_argument("--exit-grace", type=float, default=10.0, help="seconds an agent gets to exit after game over (default 10)")
    sp.set_defaults(func=cmd_play)

    sv = sub.add_parser("validate", help="check a skill and run one smoke game vs random",
                        description="Check SKILL.md of a skill, then play one game vs random with the "
                                    "course agent (uses your Claude Code or Codex login; --no-game skips it).")
    sv.add_argument("submission", help="skill directory")
    sv.add_argument("--timeout", type=float, default=180.0, help="decision timeout in seconds (default 180)")
    sv.add_argument("--seed", type=int, default=None, help="seed of the smoke game (default 1)")
    sv.add_argument("--out", default=None, help="where to write the smoke game (default: a temp directory)")
    sv.add_argument("--no-game", action="store_true", help="only check the files, do not run the smoke game")
    sv.set_defaults(func=cmd_validate)

    spp = sub.add_parser("prompt", help="print the prompt the course agent gets for a skill",
                         description="Print the course system prompt with the skill's SKILL.md, and the first message.")
    spp.add_argument("skill", help="skill directory")
    spp.add_argument("--player", type=int, default=1, choices=(1, 2), help="seat number shown in the prompt (default 1)")
    spp.add_argument("--timeout", type=float, default=180.0, help="decision timeout shown in the prompt (default 180)")
    spp.set_defaults(func=cmd_prompt)

    sr = sub.add_parser("replay", help="print a readable transcript of a game",
                        description="Print a turn-by-turn transcript of a game directory or replay.jsonl.")
    sr.add_argument("path", help="game directory or replay.jsonl")
    sr.set_defaults(func=cmd_replay)

    sc = sub.add_parser("cards", help="list the card pool", description="List the card pool (data/cards.json).")
    sc.add_argument("--class", dest="card_class", default=None, help="only cards a deck of this class may use")
    sc.add_argument("--only", action="store_true", help="with --class: only that class's cards (no NEUTRAL)")
    sc.add_argument("--json", action="store_true", help="print JSON instead of a table")
    sc.set_defaults(func=cmd_cards)

    sver = sub.add_parser("version", help="print runtime, protocol and pool versions", description="Print versions.")
    sver.set_defaults(func=cmd_version)
    return p


def main(argv: list[str] | None = None) -> int:
    _configure_stdout()
    parser = build_parser()
    a = parser.parse_args(argv)
    if not getattr(a, "func", None):
        parser.print_help()
        return 2
    try:
        return int(a.func(a) or 0)
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
