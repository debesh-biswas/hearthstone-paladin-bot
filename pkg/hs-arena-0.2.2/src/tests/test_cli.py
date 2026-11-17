"""E1 every CLI command has --help and is exercised; E2 replay transcript."""

import json
import subprocess
import sys

import pytest

from conftest import ROOT, make_submission
from hs_arena.cli import main

COMMANDS = ["play", "validate", "prompt", "replay", "cards", "version"]


@pytest.mark.parametrize("cmd", COMMANDS)
def test_help(cmd, capsys):
    with pytest.raises(SystemExit) as e:
        main([cmd, "--help"])
    assert e.value.code == 0
    assert "usage" in capsys.readouterr().out.lower()


def test_top_level_help_and_console_script():
    out = subprocess.run([sys.executable, "-m", "hs_arena", "--help"], capture_output=True, text=True, timeout=120)
    assert out.returncode == 0
    for cmd in COMMANDS:
        assert cmd in out.stdout


def test_version(capsys):
    assert main(["version"]) == 0
    out = capsys.readouterr().out
    assert "protocol version 1" in out and "pool version basic-classic-1" in out and "fireplace commit" in out


def test_cards(capsys):
    assert main(["cards", "--class", "MAGE", "--json"]) == 0
    data = json.loads(capsys.readouterr().out)
    assert data and {c["card_class"] for c in data} == {"MAGE", "NEUTRAL"}
    assert main(["cards", "--class", "mage", "--only"]) == 0
    out = capsys.readouterr().out
    assert "Fireball" in out and "Chillwind Yeti" not in out


def test_play_and_replay(tmp_path, capsys):
    out_dir = tmp_path / "games"
    assert main(["play", "--p1", "greedy", "--p2", "random", "--games", "2", "--parallel", "1", "--seed", "5",
                 "--out", str(out_dir), "--no-keep-decisions"]) == 0
    printed = capsys.readouterr().out
    assert "games 2  counted 2" in printed and "winner" in printed
    dirs = sorted(out_dir.iterdir())
    assert len(dirs) == 2 and dirs[0].name.startswith("g_")
    assert main(["replay", str(dirs[0])]) == 0
    text = capsys.readouterr().out
    assert "--- Turn 1:" in text and "Game over:" in text and "Result: winner" in text
    assert main(["replay", str(dirs[0] / "replay.jsonl")]) == 0
    assert main(["replay", str(tmp_path / "nope")]) == 2
    # game ids continue in the same output directory
    assert main(["play", "--p1", "random", "--p2", "random", "--seed", "6", "--out", str(out_dir)]) == 0
    assert len(list(out_dir.iterdir())) == 3


def test_play_rejects_bad_specs(tmp_path, capsys):
    assert main(["play", "--p1", str(tmp_path / "missing"), "--p2", "greedy", "--out", str(tmp_path)]) == 2
    bad_deck = tmp_path / "deck.json"
    bad_deck.write_text(json.dumps({"hero_class": "MAGE", "cards": ["CS2_029"] * 30}), encoding="utf-8")
    assert main(["play", "--p1", f"greedy:{bad_deck}", "--p2", "random", "--out", str(tmp_path)]) == 2
    err = capsys.readouterr().err
    assert "CS2_029" in err and "30 times" in err


def test_validate_ok_and_failures(tmp_path, capsys, example_copy):
    assert main(["validate", str(example_copy), "--out", str(tmp_path / "v"), "--timeout", "30"]) == 0
    assert "OK" in capsys.readouterr().out
    crashing = make_submission(tmp_path, "raise SystemExit(1)\n", name="crasher")
    assert main(["validate", str(crashing), "--out", str(tmp_path / "v2"), "--timeout", "30"]) == 1
    assert "forfeit_exit" in capsys.readouterr().out
    broken = make_submission(tmp_path, "pass\n", name="broken", manifest={"protocol_version": "9"})
    assert main(["validate", str(broken), "--no-game"]) == 1
    assert "protocol_version" in capsys.readouterr().out


def test_readme_has_replay_sample():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "hs-arena replay" in readme
    assert "--- Turn" in readme, "README must contain a sample replay transcript"
