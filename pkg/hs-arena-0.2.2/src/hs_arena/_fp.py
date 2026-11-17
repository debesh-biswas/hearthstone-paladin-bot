"""Single entry point to the vendored fireplace engine (lazy card database initialisation)."""

from __future__ import annotations

import logging
import threading

_lock = threading.Lock()
_initialized = False


def init_engine():
    """Initialise the fireplace card database once per process (about 4-5 s) and return the module."""
    global _initialized
    from ._vendor.fireplace import cards

    if not _initialized:
        with _lock:
            if not _initialized:
                logging.getLogger("fireplace").setLevel(logging.ERROR)
                if not cards.db.initialized:
                    cards.db.initialize()
                _initialized = True
    return cards
