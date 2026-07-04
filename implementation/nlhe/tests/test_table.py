"""Open-addressed infoset table: insert/lookup/collision/probe correctness."""
import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import mccfr  # noqa: E402


def test_insert_lookup_roundtrip():
    cap = 1024
    slot_key, regret, strat = mccfr.make_table(cap)
    rng = np.random.default_rng(0)
    hashes = rng.integers(1, 2**62, size=500, dtype=np.uint64)  # avoid 0 sentinel
    slots = {}
    for h in hashes:
        s = mccfr.table_find_or_insert(slot_key, np.uint64(h))
        assert s >= 0
        slots[int(h)] = s
    # every key must be found at its slot, distinct keys -> distinct slots
    assert len(set(slots.values())) == len(set(int(h) for h in hashes))
    for h, s in slots.items():
        assert mccfr.table_find(slot_key, np.uint64(h)) == s


def test_probing_and_full():
    cap = 8
    slot_key, _, _ = mccfr.make_table(cap)
    # insert cap-1 keys that all collide on the same initial slot (multiples of cap)
    base = [cap * i + 3 for i in range(1, cap)]  # all map to slot 3
    got = [mccfr.table_find_or_insert(slot_key, np.uint64(h)) for h in base]
    assert len(set(got)) == len(base)  # all placed via probing
    for h in base:
        assert mccfr.table_find(slot_key, np.uint64(h)) >= 0
    # table now has cap-1 of cap slots used; one more distinct key fills it
    mccfr.table_find_or_insert(slot_key, np.uint64(999999))
    # a further distinct key must report full (-1)
    assert mccfr.table_find_or_insert(slot_key, np.uint64(123457)) == -1


def test_absent_returns_minus_one():
    cap = 64
    slot_key, _, _ = mccfr.make_table(cap)
    mccfr.table_find_or_insert(slot_key, np.uint64(42))
    assert mccfr.table_find(slot_key, np.uint64(43)) == -1


def test_regret_matching():
    out = np.empty(4)
    mccfr.regret_matching(np.array([3.0, 1.0, 0.0, -5.0]), 4, out)
    assert np.allclose(out, [0.75, 0.25, 0.0, 0.0])
    mccfr.regret_matching(np.array([-1.0, -2.0, 0.0, 0.0]), 4, out)
    assert np.allclose(out, [0.25, 0.25, 0.25, 0.25])  # all non-positive -> uniform


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
