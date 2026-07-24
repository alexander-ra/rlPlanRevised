"""
shapley_playground.py -- Exploration Day 2 (raw step 11 L112-152): compute Shapley values and
the CORE on two classic toy cooperative games, to build intuition for the two ideas the
implementation reuses (Shapley = FAIRNESS / credit; the core = STABILITY).

TWO GAMES WITH KNOWN ANSWERS (the correctness anchors -- raw L137-152)
----------------------------------------------------------------------
- GLOVE GAME: players {0,1,2}; player 0 has a LEFT glove, players 1 and 2 each a RIGHT glove.
  A matched pair is worth $1, so v(S) = min(#left in S, #right in S).
    * Shapley value  = (2/3, 1/6, 1/6)   -- player 0 is scarce, so worth more.
    * Core           = {(1, 0, 0)}       -- any coalition without player 0 is worth 0, so 0 has
                                            all the leverage. Fairness (Shapley) != stability (core)!
- 3-PLAYER MAJORITY GAME: any 2+ players win together. v(S) = 1 if |S| >= 2 else 0.
    * Shapley value  = (1/3, 1/3, 1/3)   -- symmetric, equal split.
    * Core           = EMPTY              -- no allocation is stable; every pair can be undercut by
                                            another pair. This is the SLS situation (raw L325-326):
                                            a purely competitive / simple game has an empty core, so
                                            coalitions are INHERENTLY UNSTABLE and will be betrayed.

Pure numpy + itertools (self-contained; no engine needed). `scipy` is used ONLY for the core
feasibility LP and is guarded -- without it the analytic answers above are printed as targets.

Run from `implementation/step11/exploration/`.  Runtime: instant.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every number is a PREDICTION.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


def shapley_value(n_players: int, value_function) -> np.ndarray:
    """Exact Shapley value by averaging marginal contributions over ALL join orders (raw
    L119-134). `value_function(coalition_frozenset) -> float`. O(n!) -- fine for n <= 8."""
    shapley = np.zeros(n_players)
    for i in range(n_players):
        for perm in itertools.permutations(range(n_players)):
            pos = perm.index(i)
            before = frozenset(perm[:pos])
            after = before | {i}
            shapley[i] += value_function(after) - value_function(before)
        shapley[i] /= math.factorial(n_players)
    return shapley


def core_feasibility(n_players: int, value_function):
    """Is the core non-empty? The core is {x : sum_i x_i = v(N); sum_{i in S} x_i >= v(S) for all
    S}. Solve a feasibility LP (minimize 0). Returns (feasible, allocation_or_None).

    Guarded: if scipy is absent, returns (None, None) -- caller prints the analytic target.
    """
    try:
        from scipy.optimize import linprog
    except ImportError:
        return None, None

    full = frozenset(range(n_players))
    vN = value_function(full)
    # inequalities  -sum_{i in S} x_i <= -v(S)  for every non-empty proper coalition S
    A_ub, b_ub = [], []
    for r in range(1, n_players):
        for S in itertools.combinations(range(n_players), r):
            row = [-1.0 if i in S else 0.0 for i in range(n_players)]
            A_ub.append(row)
            b_ub.append(-value_function(frozenset(S)))
    A_eq = [[1.0] * n_players]
    b_eq = [vN]
    res = linprog(c=[0.0] * n_players, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=[(0.0, None)] * n_players, method="highs")
    return bool(res.success), (np.round(res.x, 4).tolist() if res.success else None)


# --- the two games ----------------------------------------------------------------------
def glove_value(S) -> float:
    left = 1 if 0 in S else 0                    # player 0 holds the only left glove
    right = sum(1 for i in (1, 2) if i in S)     # players 1, 2 hold right gloves
    return float(min(left, right))


def majority_value(S) -> float:
    return 1.0 if len(S) >= 2 else 0.0


def main():
    print("shapley_playground  (PREDICTIONS -- verify on a real run)")
    print("=" * 72)

    print("\n[GLOVE GAME]  v(S) = min(#left, #right); player 0 = left, players 1,2 = right")
    sv = shapley_value(3, glove_value)
    print(f"  Shapley value = {np.round(sv, 4).tolist()}   (PREDICT [0.6667, 0.1667, 0.1667])")
    feas, alloc = core_feasibility(3, glove_value)
    print(f"  core non-empty? {feas}  example allocation = {alloc}   "
          f"(PREDICT feasible; the unique core point is (1, 0, 0) -- player 0 takes everything)")
    print("  --> FAIRNESS (Shapley) and STABILITY (core) can disagree sharply.")

    print("\n[3-PLAYER MAJORITY]  v(S) = 1 if |S| >= 2 else 0")
    sv = shapley_value(3, majority_value)
    print(f"  Shapley value = {np.round(sv, 4).tolist()}   (PREDICT [0.3333, 0.3333, 0.3333])")
    feas, alloc = core_feasibility(3, majority_value)
    print(f"  core non-empty? {feas}   (PREDICT False -- the core is EMPTY; no stable split; "
          "any pair is undercut by another pair -- the SLS instability, raw L325-326)")

    print("\nCONNECT TO SLS (raw L154-159): a coalition's 'value' = its members' probability of "
          "winning. With 2^4 = 16 subsets, exact Shapley is cheap for 4 players; the challenge is "
          "that the coalition structure CHANGES EVERY TURN (dynamic, not static).")


if __name__ == "__main__":
    main()
