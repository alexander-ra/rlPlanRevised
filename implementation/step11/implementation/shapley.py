"""
shapley.py -- Shapley value + Shapley credit assignment for So Long Sucker (raw step 11 L114-159,
L322-323, L427-465, L549). 🔴 HAND-CODE: adapting Wang et al.'s Shapley-Q (AAAI 2020) to a
purely-COMPETITIVE game.

TWO USES
--------
1. `exact_shapley` / `mc_shapley`: the classical Shapley value of any coalition-value function
   v(S) -- exact (all n! orders, cheap for n=4: 24) or Monte-Carlo over sampled permutations
   (Wang et al. Section 4 approximation, for larger n).
2. `shapley_credit_*`: turn a sparse 1-winner outcome into a dense PER-PLAYER credit.

THE COMPETITIVE ADAPTATION (raw L464)
-------------------------------------
In cooperative MARL the coalition value is the team's shared Q. SLS has no shared reward, so we
define coalition value as a WINNING-PROBABILITY notion:

  - RIGOROUS (validation): v(S) = P( the eventual winner is a member of S ), estimated by random
    rollouts (`win_prob_coalition_values`). v({}) = 0, v(all) = 1, so the Shapley credit is each
    player's share of the win probability and SUMS TO 1.
  - PROXY (training, cheap -- raw L455-462): v(S) = normalized [ (sum of member value estimates) *
    (1 + synergy*|S|) ], using the critic's per-agent value estimates. A fast heuristic used every
    game inside `coalition_mappo`; NOTE it is an approximation, not the true counterfactual value.

The reference games (glove, majority) reproduce the exploration's exact answers as unit checks.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


# --- classical Shapley value ------------------------------------------------------------
def exact_shapley(n_players: int, value_function) -> np.ndarray:
    """phi_i = sum_{S subseteq N\\{i}} |S|!(n-|S|-1)!/n! * (v(S+i) - v(S)) (raw L322-323).
    `value_function(frozenset) -> float`. O(n * 2^n) via the weight form; exact."""
    phi = np.zeros(n_players)
    others = list(range(n_players))
    for i in range(n_players):
        rest = [p for p in others if p != i]
        for r in range(len(rest) + 1):
            w = math.factorial(r) * math.factorial(n_players - r - 1) / math.factorial(n_players)
            for S in itertools.combinations(rest, r):
                Sf = frozenset(S)
                phi[i] += w * (value_function(Sf | {i}) - value_function(Sf))
    return phi


def mc_shapley(n_players: int, value_function, n_perms: int = 2000, seed: int = 0) -> np.ndarray:
    """Monte-Carlo Shapley: average marginal contribution over `n_perms` random join orders
    (Wang et al. Section 4). Unbiased; variance ~1/n_perms. Use when 2^n is too big (n>~12)."""
    rng = np.random.default_rng(seed)
    phi = np.zeros(n_players)
    for _ in range(n_perms):
        perm = rng.permutation(n_players)
        S = frozenset()
        v_prev = value_function(S)
        for p in perm:
            S = S | {int(p)}
            v_cur = value_function(S)
            phi[int(p)] += v_cur - v_prev
            v_prev = v_cur
    return phi / n_perms


# --- coalition-value functions for SLS --------------------------------------------------
def win_prob_coalition_values(game, state, n_rollouts: int = 300, policies=None, seed: int = 0,
                              rotate_start: bool = False):
    """v(S) = P(winner in S), estimated by random (or given-policy) rollouts from `state`.
    Returns a dict {frozenset: prob}. One rollout batch scores every subset at once.

    `rotate_start`: if True, each rollout starts from a uniformly-random ALIVE seat instead of
    `state.current_player`. This removes the first-mover (seat-0) bias so a position that is
    symmetric in chips scores symmetrically in win-probability (raw L559 target). Averaging over
    the starting seat is the de-confounded estimate; leave False for the raw single-seat view."""
    from dataclasses import replace

    rng = np.random.default_rng(seed)
    n = game.n_players
    alive0 = [p for p in range(n) if p not in state.eliminated]
    win_counts = np.zeros(n)
    total = 0
    for _ in range(n_rollouts):
        s = state
        if rotate_start and alive0:
            s = replace(s, current_player=int(alive0[int(rng.integers(len(alive0)))]))
        while not game.is_terminal(s):
            legal = game.legal_actions(s)
            if not legal:
                nxt = game._next_with_chips([list(h) for h in s.hands], set(s.eliminated),
                                            s.current_player)
                if nxt is None:
                    break
                s = replace(s, current_player=nxt)
                continue
            if policies is not None:
                a = policies[s.current_player](game, s, rng)
            else:
                a = legal[int(rng.integers(len(legal)))]
            s = game.apply(s, a, rng=rng)
        if s.winner is not None and 0 <= s.winner < n:
            win_counts[s.winner] += 1
            total += 1
    wp = win_counts / max(total, 1)
    values = {}
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            values[frozenset(S)] = float(sum(wp[i] for i in S))
    return values, wp


def proxy_coalition_values(agent_values, synergy: float = 0.1) -> dict:
    """Fast coalition value from per-agent value estimates (raw L455-462):
        v(S) = (sum_{i in S} agent_values[i]) * (1 + synergy*|S|),  then NORMALIZED so v(all)=1.
    A cheap training-time proxy (NOT the true counterfactual value -- flagged, raw L462-464)."""
    n = len(agent_values)
    vals = np.asarray(agent_values, dtype=float)
    # shift to non-negative so the "share" interpretation holds
    vals = vals - vals.min() + 1e-6
    raw = {}
    for r in range(n + 1):
        for S in itertools.combinations(range(n), r):
            base = sum(vals[i] for i in S)
            raw[frozenset(S)] = base * (1.0 + synergy * len(S))
    full = raw[frozenset(range(n))]
    if full <= 0:
        return {k: 0.0 for k in raw}
    return {k: v / full for k, v in raw.items()}


def shapley_credit(n_players: int, values: dict) -> np.ndarray:
    """Shapley credit from a pre-tabulated value dict (avoids recomputing v inside the loop)."""
    return exact_shapley(n_players, lambda S: values[S])


def shapley_credit_from_values(agent_values, synergy: float = 0.1) -> np.ndarray:
    """End-to-end training-time credit: proxy coalition value -> Shapley. Sums to ~1."""
    n = len(agent_values)
    return shapley_credit(n, proxy_coalition_values(agent_values, synergy))


# --- reference games (unit checks; mirror shapley_playground.py) ------------------------
def glove_value(S) -> float:
    left = 1 if 0 in S else 0
    right = sum(1 for i in (1, 2) if i in S)
    return float(min(left, right))


def majority_value(S) -> float:
    return 1.0 if len(S) >= 2 else 0.0


def _selftest():
    print("shapley self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    sv = exact_shapley(3, glove_value)
    print(f"  glove exact Shapley   = {np.round(sv, 4).tolist()} (PREDICT [0.6667,0.1667,0.1667])")
    mc = mc_shapley(3, glove_value, n_perms=20000, seed=0)
    print(f"  glove MC Shapley      = {np.round(mc, 3).tolist()} (PREDICT ~ the exact value)")
    sv = exact_shapley(3, majority_value)
    print(f"  majority exact Shapley= {np.round(sv, 4).tolist()} (PREDICT [0.3333]*3)")

    # proxy credit: symmetric values -> equal credit; skewed values -> concentrated
    eq = shapley_credit_from_values([1.0, 1.0, 1.0, 1.0])
    sk = shapley_credit_from_values([3.0, 3.0, 0.2, 0.2])
    print(f"  proxy credit equal    = {np.round(eq, 3).tolist()} (PREDICT ~[0.25]*4, sums~1)")
    print(f"  proxy credit skewed   = {np.round(sk, 3).tolist()} (PREDICT P0,P1 >> P2,P3, sums~1)")
    assert abs(eq.sum() - 1.0) < 1e-6, "credit must sum to 1"


if __name__ == "__main__":
    _selftest()
