"""E3: docs/protocol.md matches the schemas — every ```json <schema> example block validates."""

import json
import re

from conftest import ROOT, assert_valid

BLOCK = re.compile(r"^```json (state|action|manifest|game|result|event)[ \t]*\n(.*?)^```", re.M | re.S)


def _blocks():
    text = (ROOT / "docs" / "protocol.md").read_text(encoding="utf-8")
    return [(m.group(1), m.group(2)) for m in BLOCK.finditer(text)]


def test_protocol_examples_validate(validators):
    blocks = _blocks()
    kinds = {k for k, _ in blocks}
    assert {"state", "action", "event"} <= kinds, f"protocol.md must contain state, action and event examples; found {kinds}"
    for n, (kind, body) in enumerate(blocks, 1):
        obj = json.loads(body)
        assert_valid(validators[kind], obj, f"protocol.md example #{n} ({kind})")


def test_protocol_mentions_every_error_code_and_event():
    from hs_arena.protocol import ERROR_CODES, load_schema

    text = (ROOT / "docs" / "protocol.md").read_text(encoding="utf-8")
    for code in ERROR_CODES:
        assert code in text, code
    for ev in load_schema("state")["$defs"]["event"]["properties"]["event"]["enum"]:
        assert f"`{ev}`" in text, ev
