"""Gate G1: engine_ref and engine_nb must agree on 10k random playouts.

Both engines are driven by the SAME sequence of legal-action *indices*. If they
enumerate legal actions identically and apply them identically, the same index
picks the same action, and terminal payoffs must match. This validates
enumeration, application, side pots and showdown in one shot.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
ART = Path(__file__).resolve().parents[1] / "artifacts"
sys.path.insert(0, str(SRC))

import engine_ref as ER  # noqa: E402
import engine_nb as EN  # noqa: E402
from cards import BINOM  # noqa: E402

RANK = np.load(ART / "rank7.npy")
BIN64 = BINOM.astype(np.int64)


def _rank_fn(hole, board):
    a = sorted(list(hole) + list(board))
    ci = sum(int(BIN64[c, i + 1]) for i, c in enumerate(a))
    return int(RANK[ci])


def _deal(rng):
    deck = rng.permutation(52)
    holes = [[int(deck[2 * i]), int(deck[2 * i + 1])] for i in range(6)]
    board = [int(deck[12 + i]) for i in range(5)]
    return holes, board


def _play_ref(rules, holes, board, choices, button=0):
    s = ER.new_hand(rules, holes, board, button=button)
    ci = 0
    while not ER.is_terminal(s):
        kinds, amts = ER.legal_actions(s)
        k = choices[ci] % len(kinds)
        ci += 1
        ER.apply_action(s, kinds[k], amts[k])
    return ER.payoffs(s, _rank_fn), ci


def _play_nb(rules_arr, holes, board, choices, button=0):
    holes_flat = np.array([c for h in holes for c in h], dtype=np.int32)
    board_arr = np.array(board, dtype=np.int32)
    st = EN.new_hand_nb(rules_arr, holes_flat, board_arr, button)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    ci = 0
    while st[EN.S_FIN] == 0:
        m = EN.legal_actions_nb(st, rules_arr, ok, oa)
        k = choices[ci] % m
        ci += 1
        EN.apply_action_nb(st, rules_arr, int(ok[k]), int(oa[k]))
    out = np.zeros(6, dtype=np.int64)
    EN.payoffs_nb(st, RANK, BIN64, out)
    return out, ci


def test_cross_10k():
    rules = ER.Rules()
    rules_arr = EN.pack_rules(rules)
    rng = np.random.default_rng(12345)
    n_games = 10000
    mismatches = 0
    first_bad = None
    for g in range(n_games):
        holes, board = _deal(rng)
        choices = rng.integers(0, 1000, size=200)
        button = g % 6
        pr, cr = _play_ref(rules, holes, board, choices, button)
        pn, cn = _play_nb(rules_arr, holes, board, choices, button)
        if list(pr) != list(pn):
            mismatches += 1
            if first_bad is None:
                first_bad = (g, holes, board, list(pr), list(pn))
        # zero-sum sanity
        assert sum(pr) == 0, (g, pr)
        assert int(sum(pn)) == 0, (g, pn)
    assert mismatches == 0, f"{mismatches}/{n_games} mismatch; first={first_bad}"


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "-s"]))
