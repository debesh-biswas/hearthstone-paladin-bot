"""Build dist/hs-arena-<version>.zip: wheel + dependency wheels + source + docs + examples + data + schemas + decks.

Usage (from the hs-arena directory):
    python tools/build_zip.py [--no-deps] [--out dist]

--no-deps skips downloading the dependency wheels (hearthstone, hearthstone_data, requests, ...); the zip then
needs network access at install time. With dependencies included, installation works offline:
    pip install --no-index --find-links wheels hs_arena-<version>-py3-none-any.whl
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hs_arena import __version__  # noqa: E402

SOURCE_ITEMS = ["pyproject.toml", "README.md", "LICENSE", "hs_arena", "docs", "examples", "tests", "tools"]
SKIP_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build"}
STUDENT_EXAMPLES = ["starter_skill", "greedy_skill", "greedy_mcp_client"]
SKIP_SUFFIXES = {".pyc", ".pyo"}


def _copy_tree(src: Path, dst: Path) -> None:
    if src.is_file():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        if any(part in SKIP_NAMES or part.endswith(".egg-info") for part in rel.parts) or p.suffix in SKIP_SUFFIXES:
            continue
        target = dst / rel
        if p.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)


def _run(cmd: list[str]) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def build(out_dir: Path, with_deps: bool, *, wheelhouse: Path | None = None,
          no_build_isolation: bool = False) -> Path:
    name = f"hs-arena-{__version__}"
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hsz-") as tmp:
        stage = Path(tmp) / name
        stage.mkdir()
        wheel_dir = Path(tmp) / "wheel"
        cmd = [sys.executable, "-m", "pip", "wheel", "--no-deps", "--wheel-dir", str(wheel_dir)]
        if no_build_isolation:
            cmd += ["--no-build-isolation", "--no-index"]
        _run(cmd + [str(ROOT)])
        wheels = list(wheel_dir.glob("hs_arena-*.whl"))
        if len(wheels) != 1:
            raise SystemExit(f"expected one hs_arena wheel, got {wheels}")
        shutil.copy2(wheels[0], stage / wheels[0].name)
        if with_deps:
            if wheelhouse is not None:
                dependencies = sorted(wheelhouse.glob("*.whl"))
                if not dependencies:
                    raise SystemExit(f"no dependency wheels in {wheelhouse}")
                (stage / "wheels").mkdir()
                for dependency in dependencies:
                    shutil.copy2(dependency, stage / "wheels" / dependency.name)
            else:
                _run([sys.executable, "-m", "pip", "download", "--only-binary", ":all:", "--platform", "any",
                      "--python-version", "3.10", "--implementation", "py", "--abi", "none", "--dest", str(stage / "wheels"),
                      str(wheels[0])])
            for w in (stage / "wheels").glob("hs_arena-*.whl"):
                w.unlink()
        for item in SOURCE_ITEMS:
            src = ROOT / item
            if src.exists():
                _copy_tree(src, stage / "src" / item)
        # top-level copies for browsing without unpacking the wheel
        for item in ("README.md", "LICENSE"):
            shutil.copy2(ROOT / item, stage / item)
        _copy_tree(ROOT / "docs", stage / "docs")
        for ex in STUDENT_EXAMPLES:  # the process-agent example (random_agent) stays in src/ for the tests
            _copy_tree(ROOT / "examples" / ex, stage / "examples" / ex)
        _copy_tree(ROOT / "hs_arena" / "data", stage / "data")
        _copy_tree(ROOT / "hs_arena" / "schemas", stage / "schemas")
        _copy_tree(ROOT / "hs_arena" / "decks", stage / "decks")
        _copy_tree(ROOT / "hs_arena" / "pool", stage / "pool")
        install = [
            f"hs-arena {__version__}",
            "",
            "Install into a fresh virtual environment (Python 3.10+, 3.11 recommended):",
            "",
            "  python -m venv .venv            (macOS: python3.11 -m venv .venv; the built-in python3 is 3.9, too old)",
            "  .venv\\Scripts\\activate        (Windows)   |   source .venv/bin/activate   (macOS/Linux/WSL)",
        ]
        if with_deps:
            install.append(f"  pip install --no-index --find-links wheels {wheels[0].name}")
        else:
            install.append(f"  pip install {wheels[0].name}          (downloads hearthstone + hearthstone_data)")
        install += ["  hs-arena version",
                    "  hs-arena play --p1 client:examples/greedy_mcp_client --p2 random --games 3   (no model needed)",
                    "",
                    "To play a skill you also need Claude Code (model: haiku) or the Codex CLI (model: luna), logged in.",
                    "The assignment is in docs/handout.md; README.md has the quick start and the setup for Windows,",
                    "WSL and macOS."]
        (stage / "INSTALL.txt").write_text("\n".join(install) + "\n", encoding="utf-8", newline="\n")
        zip_path = out_dir / f"{name}.zip"
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for p in sorted(stage.rglob("*")):
                if p.is_file():
                    z.write(p, p.relative_to(stage.parent).as_posix())
    print(f"wrote {zip_path} ({zip_path.stat().st_size / 1e6:.1f} MB)")
    return zip_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "dist"), help="output directory (default: dist/)")
    ap.add_argument("--no-deps", action="store_true", help="do not bundle dependency wheels")
    ap.add_argument("--wheelhouse", type=Path, help="bundle existing dependency wheels instead of downloading")
    ap.add_argument("--no-build-isolation", action="store_true", help="build offline using the installed build backend")
    a = ap.parse_args()
    if a.no_deps and a.wheelhouse:
        ap.error("--wheelhouse cannot be combined with --no-deps")
    build(Path(a.out), with_deps=not a.no_deps, wheelhouse=a.wheelhouse,
          no_build_isolation=a.no_build_isolation)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
