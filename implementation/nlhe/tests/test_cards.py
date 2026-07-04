"""Gate G2: 7-card rank table agrees with phevaluator; combo_index is a bijection."""
import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
ART = Path(__file__).resolve().parents[1] / "artifacts"
sys.path.insert(0, str(SRC))

import cards as C  # noqa: E402

RANK = np.load(ART / "rank7.npy")
BIN64 = C.BINOM.astype(np.int64)


def _py_index(combo):
    return sum(int(BIN64[c, i + 1]) for i, c in enumerate(sorted(combo)))


def test_combo_index_bijection_prefix():
    from itertools import combinations
    seen = set()
    for i, combo in enumerate(combinations(range(20), 7)):  # small universe
        idx = _py_index(combo)
        assert idx not in seen
        seen.add(idx)
    # colex indices for a 20-card universe must be a contiguous 0..C(20,7)-1
    assert max(seen) == len(seen) - 1


def test_rank_table_matches_phevaluator():
    from phevaluator.evaluator import _evaluate_cards
    rng = np.random.default_rng(7)
    for _ in range(200_000):
        cs = rng.choice(52, size=7, replace=False)
        idx = _py_index([int(x) for x in cs])
        ours = int(RANK[idx])
        theirs = C.PHEVAL_MAX - _evaluate_cards(*[int(x) for x in cs])
        assert ours == theirs


def test_stronger_is_larger():
    # royal flush must outrank a random junk hand
    rf = [C.card_from_str(x) for x in ["As", "Ks", "Qs", "Js", "Ts", "2c", "3d"]]
    junk = [C.card_from_str(x) for x in ["2c", "3d", "5h", "7s", "9c", "Jd", "Kh"]]
    assert RANK[_py_index(rf)] > RANK[_py_index(junk)]


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
