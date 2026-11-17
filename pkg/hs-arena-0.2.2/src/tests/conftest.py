"""Shared test helpers: scripted submissions, game runners, schema validators."""

from __future__ import annotations

import json
import random
import shutil
import sys
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "random_agent"

from hs_arena._resources import GREEDY_DECK  # noqa: E402
from hs_arena.protocol import Config  # noqa: E402

MANIFEST = {
    "protocol_version": "1",
    "pool_version": "basic-classic-1",
    "name": "test-agent",
    "author": "tester",
    "command": ["python", "agent.py"],
}

# Prelude for scripted agents: a random legal policy built on the SDK.
AGENT_PRELUDE = '''
import os, sys, time, json, random
from hs_arena.sdk import Agent, Action, run

def random_action(state, rng):
    ts = [t for t in state.legal_actions if t.type != "concede"]
    t = rng.choice(ts)
    if t.type == "mulligan":
        return Action.mulligan([])
    if t.type == "choose":
        return Action.choose(t.options[0].entity_id)
    if t.type == "attack":
        return Action.attack(t.attacker, rng.choice(t.targets))
    if t.type in ("play_card", "hero_power"):
        targets, choose = t.targets, None
        if t.get("choose"):
            o = rng.choice(t.choose)
            choose, targets = o.entity_id, o.targets
        target = rng.choice(targets) if targets else None
        if t.type == "hero_power":
            return Action.hero_power(target=target, choose=choose)
        return Action.play_card(t.card, target=target, choose=choose)
    return Action.end_turn()
'''


def make_submission(base: Path, body: str, name: str = "test-agent", manifest: dict | None = None,
                    deck: dict | None = None) -> Path:
    """Create a submission directory whose agent.py is AGENT_PRELUDE + body."""
    d = base / name
    d.mkdir(parents=True, exist_ok=True)
    m = dict(MANIFEST, name=name)
    if manifest:
        m.update(manifest)
    (d / "manifest.json").write_text(json.dumps(m), encoding="utf-8")
    if deck is None:
        deck = json.loads(GREEDY_DECK.read_text(encoding="utf-8"))
        deck.pop("name", None)
    (d / "deck.json").write_text(json.dumps(deck), encoding="utf-8")
    (d / "agent.py").write_text(AGENT_PRELUDE + "\n" + textwrap.dedent(body), encoding="utf-8")
    return d


def fast_config(**kw) -> Config:
    base = dict(decision_timeout_s=30.0, exit_grace_s=3.0, poll_interval_ms=10)
    base.update(kw)
    return Config(**base)


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_json(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


@pytest.fixture
def example_copy(tmp_path) -> Path:
    """A copy of examples/random_agent (so tests never touch the original)."""
    dst = tmp_path / "random_agent"
    shutil.copytree(EXAMPLE, dst)
    return dst


def random_deck_for(seed: int):
    from hs_arena.deck import random_deck

    return random_deck(random.Random(seed))


@pytest.fixture(scope="session")
def validators():
    jsonschema = pytest.importorskip("jsonschema")
    from hs_arena.protocol import SCHEMA_NAMES, load_schema

    vals = {n: jsonschema.Draft202012Validator(load_schema(n)) for n in SCHEMA_NAMES}
    st = load_schema("state")
    vals["event"] = jsonschema.Draft202012Validator(
        {"$schema": st["$schema"], "$defs": st["$defs"], "$ref": "#/$defs/event"}
    )
    return vals


def assert_valid(validator, obj, where=""):
    errors = sorted(validator.iter_errors(obj), key=lambda e: list(e.path))
    assert not errors, f"{where}: " + "; ".join(f"{list(e.path)}: {e.message[:300]}" for e in errors[:5])


def python_exe() -> str:
    return sys.executable
