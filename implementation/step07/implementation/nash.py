"""
A Nash baseline via vanilla CFR over the `Game` interface.

We need an (approximate) equilibrium strategy for three reasons:
  1. as a *safe* baseline the adaptive exploiter can fall back to,
  2. as one of the opponent types in the zoo ("a tough, non-exploitable opponent"),
  3. as a sanity check -- exact_value(nash, nash) must hit the known game value.

This is a clean, engine-agnostic vanilla CFR (full-tree, no sampling). It is NOT a copy of
step02/step03's trainers -- those are tied to their own `cfr` package and node classes;
this one speaks the Step 07 `Game` interface so the same call works for Kuhn and Leduc.
You can (and should) cross-check its output against step02/step03's trained strategies and
against OpenSpiel -- see implementation/README.md.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
Known checks:  Kuhn game value for player 0 = -1/18 ~= -0.0556.
"""

from __future__ import annotations

import json
import os


def _regret_matching(regret_sum: dict, legal: list) -> dict:
    positive = {a: regret_sum[a] if regret_sum[a] > 0.0 else 0.0 for a in legal}
    total = sum(positive.values())
    if total > 0.0:
        return {a: positive[a] / total for a in legal}
    p = 1.0 / len(legal)
    return {a: p for a in legal}


def _cfr(game, state, r0: float, r1: float, nodes: dict) -> float:
    """Vanilla CFR. Returns the node's expected utility FOR PLAYER 0.

    Player 1's regrets use the negated value because player 1 maximizes -u0 (zero-sum).
    Chance is uniform over deals and handled by the caller (equal weight per deal), so it
    is omitted here -- a uniform constant does not change regret-matching or the average.
    """
    if game.is_terminal(state):
        return game.utility(state, 0)

    player = game.current_player(state)
    legal = game.legal_actions(state)
    iset = game.info_set(state, player)

    node = nodes.get(iset)
    if node is None:
        node = {"regret_sum": {a: 0.0 for a in legal},
                "strategy_sum": {a: 0.0 for a in legal}}
        nodes[iset] = node

    strategy = _regret_matching(node["regret_sum"], legal)

    util = {}
    node_util = 0.0  # u0 of this node under `strategy`
    for a in legal:
        if player == 0:
            child = _cfr(game, game.apply(state, a), r0 * strategy[a], r1, nodes)
        else:
            child = _cfr(game, game.apply(state, a), r0, r1 * strategy[a], nodes)
        util[a] = child
        node_util += strategy[a] * child

    own_reach = r0 if player == 0 else r1
    cf_reach = r1 if player == 0 else r0
    for a in legal:
        # Regret in the acting player's own utility units.
        advantage = util[a] - node_util
        regret = advantage if player == 0 else -advantage
        node["regret_sum"][a] += cf_reach * regret
        node["strategy_sum"][a] += own_reach * strategy[a]

    return node_util


def solve_nash(game, iters: int = 20000):
    """Run vanilla CFR for `iters` iterations. Returns (policy, table).

    `table` maps info_set -> {action: average_probability}; `policy` wraps it via
    tabular_policy and works for either player (info sets are player-specific).
    """
    from policies import tabular_policy

    nodes = {}
    for _ in range(iters):
        for deal in game.deals():
            _cfr(game, game.root(deal), 1.0, 1.0, nodes)

    table = {}
    for iset, node in nodes.items():
        ssum = node["strategy_sum"]
        total = sum(ssum.values())
        if total > 0.0:
            table[iset] = {a: ssum[a] / total for a in ssum}
        else:
            n = len(ssum)
            table[iset] = {a: 1.0 / n for a in ssum}

    return tabular_policy(table), table


# --- caching so we only pay for CFR once per (game, iters) --------------------------
_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_cache")


def solve_nash_cached(game, iters: int = 20000):
    """Same as solve_nash but persists the table to implementation/_cache/.

    The table is keyed by (game name, iters). Delete the _cache folder to force a retrain.
    Returns (policy, table).
    """
    from policies import tabular_policy

    os.makedirs(_CACHE_DIR, exist_ok=True)
    path = os.path.join(_CACHE_DIR, f"nash_{game.name}_{iters}.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
        # JSON keys are strings; action ids were ints -> restore them.
        table = {iset: {int(a): p for a, p in dist.items()} for iset, dist in raw.items()}
        return tabular_policy(table), table

    policy, table = solve_nash(game, iters)
    serializable = {iset: {str(a): p for a, p in dist.items()} for iset, dist in table.items()}
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(serializable, fh, indent=2)
    return policy, table


def _selftest():
    from engines import make_game
    from best_response import exact_value, nash_gap

    print("nash self-test")
    print("-" * 50)

    game = make_game("kuhn")
    nash, table = solve_nash(game, iters=30000)
    v0 = exact_value(game, 0, nash, nash)
    gap = nash_gap(game, nash, nash)
    print(f"[kuhn] exact_value(Nash,Nash) for P0 = {v0:+.4f}  (known -1/18 = {-1/18:+.4f})")
    print(f"[kuhn] NashConv(Nash,Nash) = {gap['nash_conv']:.4f}  (expect ~0)")
    print(f"[kuhn] #info sets solved = {len(table)} (expect 12)")

    # Leduc is bigger; use fewer iters in the self-test just to confirm it runs.
    game = make_game("leduc")
    nash, table = solve_nash(game, iters=300)
    gap = nash_gap(game, nash, nash)
    print(f"[leduc] (300 iters, smoke only) NashConv = {gap['nash_conv']:.4f}, "
          f"#info sets = {len(table)}")


if __name__ == "__main__":
    _selftest()
