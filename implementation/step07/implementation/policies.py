"""
Policies, simulation, and replay for Step 07.

A *policy* is the single currency every component speaks:

    policy(game, state) -> {action_id: probability}      # over the legal actions only

Opponent types, Nash strategies, best responses, and inferred models are all just
policies. This module also provides:

  - sample_action / play_hand : roll a hand out under two policies
  - replay                    : re-derive the (player, info_set, action) decisions of a
                                fixed action sequence under a *hypothetical* deal. This is
                                the workhorse for partial-observability marginalization:
                                given a public action sequence and a guessed opponent card,
                                it tells us which opponent info sets were visited.
  - tabular_policy / uniform_policy / blend_policies : common constructors

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

from collections import namedtuple

# One recorded decision. `legal_actions` is kept so downstream code never has to re-derive
# the action set for an info set (it is constant given the info set, but explicit is safer).
Decision = namedtuple("Decision", ["player", "info_set", "action", "legal_actions"])

# One played hand, from the deal to the terminal payoff.
Hand = namedtuple("Hand", ["deal", "actions", "decisions", "utilities", "revealed"])


# --- sampling ------------------------------------------------------------------------
def sample_action(dist: dict, rng):
    """Sample an action id from {action: prob}. Deterministic given `rng`."""
    r = rng.random()
    cumulative = 0.0
    last = None
    for action, prob in sorted(dist.items()):
        last = action
        cumulative += prob
        if r < cumulative:
            return action
    return last  # floating-point guard: return the last action if probs underflow


# --- simulation ----------------------------------------------------------------------
def play_hand(game, policies, deal, rng) -> Hand:
    """Play one hand of `game` from `deal` with policies = [policy_p0, policy_p1]."""
    state = game.root(deal)
    decisions = []
    actions = []
    while not game.is_terminal(state):
        player = game.current_player(state)
        dist = policies[player](game, state)
        action = sample_action(dist, rng)
        decisions.append(Decision(player, game.info_set(state, player), action,
                                   tuple(game.legal_actions(state))))
        actions.append(action)
        state = game.apply(state, action)
    utilities = (game.utility(state, 0), game.utility(state, 1))
    revealed = frozenset(game.revealed_privates(state))
    return Hand(tuple(deal), tuple(actions), tuple(decisions), utilities, revealed)


def replay(game, deal, actions) -> list:
    """Re-derive the Decision list for a *fixed* action sequence under `deal`.

    The action sequence is public, so replaying it with a hypothetical `deal` reconstructs
    each player's info set along the path -- exactly what the likelihoods need to score a
    candidate opponent strategy when the opponent's card was never revealed.
    """
    state = game.root(deal)
    decisions = []
    for action in actions:
        player = game.current_player(state)
        decisions.append(Decision(player, game.info_set(state, player), action,
                                   tuple(game.legal_actions(state))))
        state = game.apply(state, action)
    return decisions


# --- constructors --------------------------------------------------------------------
def uniform_policy():
    """Uniform over legal actions everywhere."""
    def policy(game, state):
        legal = game.legal_actions(state)
        p = 1.0 / len(legal)
        return {a: p for a in legal}
    return policy


def tabular_policy(table: dict):
    """Wrap an info_set -> {action: prob} table as a policy.

    Missing info sets fall back to uniform; the table is restricted to the legal actions
    and renormalized defensively so an inferred/edited table can never produce an illegal
    or unnormalized distribution.
    """
    def policy(game, state):
        legal = game.legal_actions(state)
        probs = table.get(game.info_set(state))
        if probs is None:
            p = 1.0 / len(legal)
            return {a: p for a in legal}
        restricted = {a: max(0.0, float(probs.get(a, 0.0))) for a in legal}
        total = sum(restricted.values())
        if total <= 0.0:
            p = 1.0 / len(legal)
            return {a: p for a in legal}
        return {a: v / total for a, v in restricted.items()}
    return policy


def blend_policies(policies: list, weights: list):
    """Behavioral mixture: the weighted-average action distribution at each info set.

    Used by the adaptive exploiter to interpolate between an exploitative response and a
    safe (Nash) baseline. Note this is a *behavioral* blend (mix the distributions), which
    differs from a mixture over deterministic strategies -- here we want the former.
    """
    total_w = float(sum(weights))
    norm = [w / total_w for w in weights] if total_w > 0 else [1.0 / len(weights)] * len(weights)

    def policy(game, state):
        legal = game.legal_actions(state)
        out = {a: 0.0 for a in legal}
        for pol, w in zip(policies, norm):
            dist = pol(game, state)
            for a in legal:
                out[a] += w * dist.get(a, 0.0)
        total = sum(out.values())
        if total <= 0.0:
            p = 1.0 / len(legal)
            return {a: p for a in legal}
        return {a: v / total for a, v in out.items()}
    return policy


def materialize(game, policy, player: int) -> dict:
    """Walk the whole tree and read `policy`'s distribution at every info set owned by
    `player`. Returns info_set -> {action: prob}. Handy for printing/diffing strategies."""
    table = {}
    for deal in game.deals():
        _materialize_node(game, game.root(deal), policy, player, table)
    return table


def _materialize_node(game, state, policy, player, table):
    if game.is_terminal(state):
        return
    cur = game.current_player(state)
    if cur == player:
        iset = game.info_set(state, player)
        if iset not in table:
            table[iset] = dict(policy(game, state))
    for a in game.legal_actions(state):
        _materialize_node(game, game.apply(state, a), policy, player, table)


# --- self-test -----------------------------------------------------------------------
def _selftest():
    import random
    from engines import make_game

    print("policies self-test")
    print("-" * 50)
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        rng = random.Random(1)
        pols = [uniform_policy(), uniform_policy()]
        hand = play_hand(game, pols, rng.choice(game.deals()), rng)
        # replay must reproduce the exact same decisions for the same deal+actions.
        again = replay(game, hand.deal, hand.actions)
        same = [d.action for d in again] == list(hand.actions)
        print(f"[{name}] hand actions={hand.actions} util={hand.utilities} "
              f"revealed={sorted(hand.revealed)} replay_ok={same}")


if __name__ == "__main__":
    _selftest()
