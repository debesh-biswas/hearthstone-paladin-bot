"""Atomic JSON file exchange shared by the runtime and the SDK.

Writers write ``<name>.tmp`` in the same directory and ``os.replace()`` it onto the final name, so readers
never observe a partial file. On Windows ``os.replace`` (and ``os.remove``) fail with ``PermissionError`` while
another process holds the target open, so both are retried for a short while.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

_RETRY_S = 5.0
_RETRY_SLEEP_S = 0.005


def atomic_write_json(path: str | os.PathLike, obj: Any) -> None:
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    data = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(data)
    deadline = time.monotonic() + _RETRY_S
    while True:
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            if time.monotonic() > deadline:
                raise
            time.sleep(_RETRY_SLEEP_S)


def read_text(path: str | os.PathLike) -> str | None:
    """Return the file content, or None if the file does not exist (or vanished while opening)."""
    deadline = time.monotonic() + _RETRY_S
    while True:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return None
        except PermissionError:
            # Windows: the file is being replaced right now.
            if time.monotonic() > deadline:
                raise
            time.sleep(_RETRY_SLEEP_S)


def remove_file(path: str | os.PathLike) -> None:
    deadline = time.monotonic() + _RETRY_S
    while True:
        try:
            os.remove(path)
            return
        except FileNotFoundError:
            return
        except PermissionError:
            if time.monotonic() > deadline:
                raise
            time.sleep(_RETRY_SLEEP_S)


def write_json(path: str | os.PathLike, obj: Any, indent: int | None = 2) -> None:
    """Pretty-printed JSON for log/result files (also written atomically)."""
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent)
        f.write("\n")
    os.replace(tmp, path)


def load_json(path: str | os.PathLike) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
