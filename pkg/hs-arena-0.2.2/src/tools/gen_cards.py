"""Regenerate hs_arena/data/cards.json, excluded_cards.json and docs/card_pool.md from the vendored card XML."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hs_arena import cards  # noqa: E402


def main() -> int:
    doc = cards.write_generated()
    (ROOT / "docs" / "card_pool.md").write_text(cards.card_pool_markdown(doc) + "\n", encoding="utf-8", newline="\n")
    print(f"cards.json: {doc['count']} pool cards")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
