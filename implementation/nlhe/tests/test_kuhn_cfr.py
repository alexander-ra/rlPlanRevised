"""Gate G4 (part 1): CFR converges to Nash on Kuhn Poker.

Uses mccfr.regret_matching — the SAME primitive the NLHE traversal uses — so
this convergence is real evidence for the big-game update logic. Kuhn has an
analytic Nash and a tiny tree, so we compute exact exploitability via best
response and require it near zero.
"""
import sys
from pathlib import Path

import numpy as np
import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

import mccfr  # noqa: E402

# Kuhn: cards 0,1,2 (J,Q,K). Actions: 'p' pass/check, 'b' bet. Ante 1 each.
ACTIONS = "pb"


def is_terminal(h):
    return h in ("pp", "bp", "bb", "pbp", "pbb")


def terminal_util(h, c0, c1, player):
    """Utility for `player` at terminal history h."""
    win = 1 if (c0 > c1) else -1  # player 0's showdown result
    if h == "pp":
        u0 = win  # ante only, showdown for 1
    elif h == "bp":
        u0 = 1  # p1 folded
    elif h == "pbp":
        u0 = -1  # p0 folded
    else:  # 'bb' or 'pbb' -> showdown for 2
        u0 = 2 * win
    return u0 if player == 0 else -u0


class Kuhn:
    def __init__(self):
        self.idx = {}  # (card, history) -> row
        self.regret = np.zeros((12, 2), dtype=np.float64)
        self.stratsum = np.zeros((12, 2), dtype=np.float64)

    def _row(self, card, h):
        key = (card, h)
        if key not in self.idx:
            self.idx[key] = len(self.idx)
        return self.idx[key]

    def cfr(self, c0, c1, h, p0, p1):
        player = len(h) % 2
        if is_terminal(h):
            return terminal_util(h, c0, c1, player)
        card = c0 if player == 0 else c1
        I = self._row(card, h)
        strat = np.empty(2)
        mccfr.regret_matching(self.regret[I], 2, strat)
        reach = p0 if player == 0 else p1
        self.stratsum[I] += reach * strat
        util = np.zeros(2)
        node = 0.0
        for a in range(2):
            nh = h + ACTIONS[a]
            if player == 0:
                u = -self.cfr(c0, c1, nh, p0 * strat[a], p1)
            else:
                u = -self.cfr(c0, c1, nh, p0, p1 * strat[a])
            util[a] = u
            node += strat[a] * u
        cf = p1 if player == 0 else p0
        for a in range(2):
            self.regret[I][a] += cf * (util[a] - node)
        return node

    def train(self, iters):
        deals = [(a, b) for a in range(3) for b in range(3) if a != b]
        for _ in range(iters):
            for c0, c1 in deals:
                self.cfr(c0, c1, "", 1.0, 1.0)

    def avg_strategy(self):
        avg = {}
        for (card, h), i in self.idx.items():
            s = self.stratsum[i]
            tot = s.sum()
            avg[(card, h)] = (s / tot) if tot > 0 else np.array([0.5, 0.5])
        return avg


def _br_value(avg, responder):
    """Exact BR value vs fixed avg, respecting info sets.

    The responder must pick ONE action per (own_card, history) infoset without
    seeing the opponent's card. Kuhn is tiny (6 responder infosets), so we
    enumerate all 2^6 pure strategies and take the best expected value.
    """
    deals = [(a, b) for a in range(3) for b in range(3) if a != b]
    # responder's infosets: histories where it acts, x 3 cards
    r_hists = ["", "pb"] if responder == 0 else ["p", "b"]
    infosets = [(card, h) for card in range(3) for h in r_hists]

    def value(pure):
        def rec(c0, c1, h):
            player = len(h) % 2
            if is_terminal(h):
                return terminal_util(h, c0, c1, responder)
            card = c0 if player == 0 else c1
            if player == responder:
                a = pure[(card, h)]
                return rec(c0, c1, h + ACTIONS[a])
            s = avg.get((card, h), np.array([0.5, 0.5]))
            return sum(s[a] * rec(c0, c1, h + ACTIONS[a]) for a in range(2))
        return sum(rec(c0, c1, "") for c0, c1 in deals) / len(deals)

    best = -1e9
    for bits in range(1 << len(infosets)):
        pure = {iset: (bits >> i) & 1 for i, iset in enumerate(infosets)}
        best = max(best, value(pure))
    return best


def test_kuhn_exploitability():
    game = Kuhn()
    game.train(4000)
    avg = game.avg_strategy()
    nashconv = _br_value(avg, 0) + _br_value(avg, 1)
    exploitability = nashconv / 2.0
    assert exploitability < 0.01, f"exploitability={exploitability:.4f}"
    # spot-check a known Nash fact: player 0 bets K (card 2) at root with the
    # same frequency as it bluffs J (card 0) times 3 (alpha relationship).
    bet_J = avg[(0, "")][1]
    bet_K = avg[(2, "")][1]
    assert bet_K > 0.5, bet_K  # always-ish value bets the best hand
    assert abs(bet_K - 3 * bet_J) < 0.1, (bet_J, bet_K)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v", "-s"]))
