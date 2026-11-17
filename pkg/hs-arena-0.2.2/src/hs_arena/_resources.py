"""Locations of the data files shipped inside the package."""

from pathlib import Path

PACKAGE_DIR = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_DIR / "data"
SCHEMA_DIR = PACKAGE_DIR / "schemas"
DECK_DIR = PACKAGE_DIR / "decks"
POOL_DIR = PACKAGE_DIR / "pool"

CARDS_JSON = DATA_DIR / "cards.json"
EXCLUDED_JSON = DATA_DIR / "excluded_cards.json"
BLACKLIST_TXT = POOL_DIR / "blacklist.txt"
GREEDY_DECK = DECK_DIR / "greedy_mage.json"
GREEDY_CONFIG = PACKAGE_DIR / "agents" / "greedy_config.json"
CARD_DEFS_XML = PACKAGE_DIR / "_vendor" / "fireplace" / "cards" / "CardDefs.xml"
