"""
[P5] Level-k / cognitive-hierarchy opponents.

Iterated strategic reasoning gives a principled ladder of "increasingly clever" opponents:

  Level 0 : non-strategic baseline -- uniform random here.
  Level k : best-responds to Level (k-1).

This is a great stress test for opponent modeling: a Level-2 player is a *deterministic*
best response to a best response, which looks nothing like the rule-based types, yet it is
still a fixed (stationary) strategy a good model should pin down and exploit. The
cognitive-hierarchy variant (best-respond to a Poisson mixture of all lower levels) is also
provided.

A Level-k policy must play whichever seat it sits in, so we compute the best-response
strategy for BOTH seats and merge them. That is unambiguous because info sets are
seat-disjoint (the action history's parity encodes who is to act).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from functools import lru_cache

from policies import uniform_policy, blend_policies
from best_response import best_response_value

# memo: (game.name, k) -> info_set -> action id
_LEVEL_TABLES: dict = {}


def _best_response_table(game, prev_policy) -> dict:
    """Merge the deterministic best responses for both seats vs `prev_policy`."""
    _, br0 = best_response_value(game, 0, prev_policy, return_strategy=True)
    _, br1 = best_response_value(game, 1, prev_policy, return_strategy=True)
    table = {}
    table.update(br0)  # player 0's info sets
    table.update(br1)  # player 1's info sets (disjoint from player 0's)
    return table


def _policy_from_table(table: dict, eps: float = 0.02):
    """Deterministic (lightly eps-smoothed) policy from an info_set -> action table."""
    def policy(game, state):
        legal = game.legal_actions(state)
        a = table.get(game.info_set(state))
        if a is None or a not in legal:
            a = legal[0]
        if eps <= 0.0:
            return {x: (1.0 if x == a else 0.0) for x in legal}
        u = eps / len(legal)
        dist = {x: u for x in legal}
        dist[a] += (1.0 - eps)
        return dist
    return policy


def level_k_policy(game, k: int, eps: float = 0.02):
    """The Level-k policy for `game`. Level 0 is uniform random."""
    if k <= 0:
        return uniform_policy()
    key = (game.name, k)
    if key not in _LEVEL_TABLES:
        prev = level_k_policy(game, k - 1, eps)
        _LEVEL_TABLES[key] = _best_response_table(game, prev)
    return _policy_from_table(_LEVEL_TABLES[key], eps)


def _poisson_weights(k: int, tau: float) -> list:
    """Truncated Poisson weights over levels 0..k-1 (cognitive hierarchy)."""
    import math
    w = [math.exp(-tau) * tau ** j / math.factorial(j) for j in range(k)]
    total = sum(w)
    return [x / total for x in w] if total > 0 else [1.0 / k] * k


def cognitive_hierarchy_policy(game, k: int, tau: float = 1.5, eps: float = 0.02):
    """Best-respond to a Poisson(tau)-weighted behavioral mixture of levels 0..k-1."""
    if k <= 0:
        return uniform_policy()
    lowers = [level_k_policy(game, j, eps) for j in range(k)]
    weights = _poisson_weights(k, tau)
    mixed_lower = blend_policies(lowers, weights)
    table = _best_response_table(game, mixed_lower)
    return _policy_from_table(table, eps)


def add_level_k_types(zoo: dict, game, levels=(1, 2), eps: float = 0.02) -> dict:
    """Add Level-1, Level-2, ... policies to an existing type zoo (in place) and return it."""
    for k in levels:
        zoo[f"Level{k}"] = level_k_policy(game, k, eps)
    return zoo


def _selftest():
    from engines import make_game
    from best_response import exact_value, best_response_value

    print("level_k self-test")
    print("-" * 50)
    game = make_game("kuhn")
    l0 = level_k_policy(game, 0)
    l1 = level_k_policy(game, 1)
    l2 = level_k_policy(game, 2)
    # Level 1 best-responds to uniform: it must beat uniform as both players.
    v_l1_vs_l0_p0 = exact_value(game, 0, l1, l0)
    v_l1_vs_l0_p1 = exact_value(game, 1, l0, l1)
    print(f"[kuhn] Level1 vs Level0: P0 EV={v_l1_vs_l0_p0:+.4f}, P1 EV={v_l1_vs_l0_p1:+.4f} "
          f"(both should be > 0)")
    # Level 2 is the BR to Level 1, so it should beat Level 1.
    v = best_response_value(game, 0, l1)
    print(f"[kuhn] BR value vs Level1 (P0) = {v:+.4f}")
    print(f"[kuhn] tables cached for: {list(_LEVEL_TABLES)}")


if __name__ == "__main__":
    _selftest()
