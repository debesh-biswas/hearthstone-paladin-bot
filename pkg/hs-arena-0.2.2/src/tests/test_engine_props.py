"""A4: legal-action templates are exactly what the engine accepts; invalid actions get the expected error code."""

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import pytest

from helpers_engine import property_worker


def _run(seeds, max_points):
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as pool:
        return list(pool.map(property_worker, seeds, [max_points] * len(seeds)))


def _merge(results):
    total = {"points": 0, "valid": 0, "invalid": 0, "failures": []}
    for r in results:
        for k in ("points", "valid", "invalid"):
            total[k] += r[k]
        total["failures"] += r["failures"]
    return total


def test_property_small():
    """Quick version for every test run (one game)."""
    t = _merge([property_worker(7, 60)])
    assert t["points"] > 20
    assert not t["failures"], t["failures"][:5]


@pytest.mark.slow
def test_property_1000_decision_points():
    seeds = list(range(100, 116))
    t = _merge(_run(seeds, 200))
    print(f"decision points {t['points']}, valid instantiations {t['valid']}, invalid actions {t['invalid']}")
    assert t["points"] >= 1000
    assert t["invalid"] >= 1000
    assert not t["failures"], t["failures"][:10]
