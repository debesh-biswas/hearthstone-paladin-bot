"""Acceptance check C1/F1: install the built zip into a fresh venv and play 20 games greedy MCP client vs greedy.

Usage:
    python tools/smoke_install.py dist/hs-arena-<version>.zip [--python PYTHON] [--work DIR] [--games 20] [--tests]

--python   interpreter used to create the venv (default: the one running this script)
--work     where to unpack and create the venv (default: a temp dir; keep it short on Windows, e.g. C:\\arena)
--tests    also run the bundled test suite (pytest -m "not slow") against the installed package
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


def run(cmd, **kw):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("zip")
    ap.add_argument("--python", default=sys.executable)
    ap.add_argument("--work", default=None)
    ap.add_argument("--games", type=int, default=20)
    ap.add_argument("--tests", action="store_true")
    a = ap.parse_args()

    work = (Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="hs-smoke-"))).resolve()
    if work.exists() and any(work.iterdir()):
        shutil.rmtree(work)
    work.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(a.zip) as z:
        z.extractall(work)
    root = next(p for p in work.iterdir() if p.is_dir() and p.name.startswith("hs-arena-"))
    venv = work / "venv"
    run([a.python, "-m", "venv", venv])
    py = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    exe = venv / ("Scripts/hs-arena.exe" if os.name == "nt" else "bin/hs-arena")
    wheel = next(root.glob("hs_arena-*.whl"))
    if (root / "wheels").exists():
        run([py, "-m", "pip", "install", "--no-index", "--find-links", root / "wheels", wheel])
    else:
        run([py, "-m", "pip", "install", wheel])
    run([exe, "version"])
    out = work / "games"
    res = run([exe, "play", "--p1", f"client:{root / 'examples' / 'greedy_mcp_client'}", "--p2", "greedy", "--games", a.games,
               "--seed", "1", "--out", out], cwd=work, capture_output=True, text=True)
    print(res.stdout)
    games = [p for p in out.iterdir() if (p / "result.json").exists()]
    if len(games) != a.games or f"games {a.games}  counted {a.games}" not in res.stdout:
        print(f"FAILED: expected {a.games} completed games", file=sys.stderr)
        return 1
    run([exe, "replay", sorted(games)[0]], stdout=subprocess.DEVNULL)
    if a.tests:
        run([py, "-m", "pip", "install", "pytest", "jsonschema"])  # test-only dependencies (network)
        tests_dir = root / "src"
        # run against the installed package, not the source copy
        env = dict(os.environ, PYTHONPATH="")
        r = subprocess.run([str(py), "-m", "pytest", "-q", "-m", "not slow", "-p", "no:cacheprovider",
                            "--rootdir", str(tests_dir), str(tests_dir / "tests")], cwd=work, env=env)
        if r.returncode != 0:
            return r.returncode
    print(f"OK: {a.games} games completed from a fresh install in {work}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
