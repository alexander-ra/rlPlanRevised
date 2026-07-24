"""
sls_shapley_peek.py -- Exploration Day 2 (raw step 11 L154-159): apply the Shapley value to
ACTUAL SLS positions, using "coalition value = probability a coalition member wins" (raw L155).

THE IDEA
--------
In a purely competitive game there is no shared pot to divide, so we do NOT use Shapley for
payoff division. Instead the coalition VALUE of a set S in a given position is estimated as

    v(S) = P( the eventual winner is a member of S )         (Monte-Carlo rollouts, raw L155)

which satisfies v({}) = 0 and v(all) = 1. The Shapley value of this v then gives each player a
"share of the win-probability" -- a fair credit for how much their presence raises the chance the
coalition wins. This is the toy version of the credit-assignment signal the implementation phase
turns into a dense training reward (`shapley.py`).

WHAT TO WATCH (raw L559)
------------------------
- SYMMETRIC position (everyone equal)  -> credits ~ (0.25, 0.25, 0.25, 0.25).
- ASYMMETRIC position (P0, P1 strong; P2, P3 nearly out) -> credit concentrates on P0, P1.

Run from `implementation/step11/exploration/`.  Runtime: a few seconds (16 subsets x rollouts).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every number is a PREDICTION.
"""

from __future__ import annotations

import itertools
import math

import numpy as np

import _bootstrap  # noqa: F401
from sls_game import SLSGame, SLSState


def _rollout_winner(game: SLSGame, state: SLSState, rng) -> int:
    """Play a random game to the end from `state`; return the winner index."""
    from dataclasses import replace
    s = state
    while not game.is_terminal(s):
        legal = game.legal_actions(s)
        if not legal:
            nxt = game._next_with_chips([list(h) for h in s.hands], set(s.eliminated),
                                        s.current_player)
            if nxt is None:
                break
            s = replace(s, current_player=nxt)
            continue
        a = legal[int(rng.integers(len(legal)))]
        s = game.apply(s, a)
    return s.winner if s.winner is not None else -1


def coalition_win_prob(game: SLSGame, state: SLSState, n_rollouts: int = 200, seed: int = 0):
    """Estimate v(S) = P(winner in S) for EVERY subset S, from `n_rollouts` random rollouts.
    Returns a dict {frozenset: prob}. One shared rollout batch scores all subsets at once."""
    rng = np.random.default_rng(seed)
    counts = np.zeros(game.n_players)
    total = 0
    for _ in range(n_rollouts):
        w = _rollout_winner(game, state, rng)
        if 0 <= w < game.n_players:
            counts[w] += 1
            total += 1
    win_prob = counts / max(total, 1)
    values = {}
    for r in range(game.n_players + 1):
        for S in itertools.combinations(range(game.n_players), r):
            values[frozenset(S)] = float(sum(win_prob[i] for i in S))
    return values, win_prob


def shapley_from_values(n_players: int, values: dict) -> np.ndarray:
    """Shapley value of a pre-tabulated coalition-value dict (avoids re-rolling per permutation)."""
    shapley = np.zeros(n_players)
    for i in range(n_players):
        for perm in itertools.permutations(range(n_players)):
            pos = perm.index(i)
            before = frozenset(perm[:pos])
            after = before | {i}
            shapley[i] += values[after] - values[before]
        shapley[i] /= math.factorial(n_players)
    return shapley


def _state_with_hands(chip_counts) -> SLSState:
    """Build a fresh (no-piles) SLS position where player p holds `chip_counts[p]` chips of its
    own color. Used to hand-craft symmetric / asymmetric positions."""
    n = len(chip_counts)
    hands = tuple(tuple(chip_counts[p] if c == p else 0 for c in range(n)) for p in range(n))
    elim = frozenset(p for p in range(n) if chip_counts[p] == 0)
    cur = next(p for p in range(n) if p not in elim)
    return SLSState(n_players=n, hands=hands, piles=(), eliminated=elim, current_player=cur)


def main():
    print("sls_shapley_peek  (PREDICTIONS -- verify on a real run)")
    print("=" * 72)
    game = SLSGame(n_players=4, chips_per_player=7)

    print("\n[SYMMETRIC]  every player holds 5 chips")
    sym = _state_with_hands([5, 5, 5, 5])
    vals, wp = coalition_win_prob(game, sym, n_rollouts=300, seed=0)
    credit = shapley_from_values(4, vals)
    print(f"  win prob per player = {np.round(wp, 3).tolist()} (PREDICT ~uniform)")
    print(f"  Shapley credit      = {np.round(credit, 3).tolist()} (PREDICT ~[0.25]*4; sums to 1)")

    print("\n[ASYMMETRIC]  P0=8, P1=8 chips; P2=1, P3=1")
    asym = _state_with_hands([8, 8, 1, 1])
    vals, wp = coalition_win_prob(game, asym, n_rollouts=300, seed=1)
    credit = shapley_from_values(4, vals)
    print(f"  win prob per player = {np.round(wp, 3).tolist()} (PREDICT P0,P1 >> P2,P3)")
    print(f"  Shapley credit      = {np.round(credit, 3).tolist()} "
          f"(PREDICT credit concentrates on P0,P1; sums to 1)")
    print(f"  pairwise coalition {{0,1}} value = {vals[frozenset({0, 1})]:.3f} "
          f"(PREDICT close to 1 -- the strong pair almost certainly contains the winner)")

    print("\nCAVEAT: rollout-based v(S) is NOISY (raise n_rollouts to tighten). The point is the "
          "RANKING of credits, not exact digits. The implementation phase uses this same value "
          "notion but with learned value estimates + counterfactual coalition values.")


if __name__ == "__main__":
    main()
