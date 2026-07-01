"""
Exact best response and exploitability over the `Game` interface.

This generalizes step03's Leduc best-response (which runs against a CFR `node_map`) to run
against *any* opponent policy -- including an inferred opponent model. That generality is
exactly what opponent modeling needs: "given my current estimate of how you play, what is
the most I can win, and which strategy achieves it?"

Everything here is EXACT (full tree traversal, no sampling), so it is the ground truth we
measure inferred models against.

Key entry points:
  - exact_value(game, hero, p0, p1)        : exact EV for `hero` under a profile
  - best_response_value(game, hero, opp)   : exact info-set-constrained BR value (+ strategy)
  - best_response_policy(game, hero, opp)  : the BR as a deterministic policy
  - nash_gap(game, p0, p1)                 : NashConv exploitability of a profile

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations


# --- exact expected value of a profile ----------------------------------------------
def exact_value(game, hero: int, policy0, policy1) -> float:
    """Exact EV for `hero` when player 0 plays `policy0` and player 1 plays `policy1`."""
    policies = [policy0, policy1]
    total = 0.0
    for deal in game.deals():
        total += game.deal_prob(deal) * _ev(game, game.root(deal), hero, policies)
    return total


def _ev(game, state, hero, policies) -> float:
    if game.is_terminal(state):
        return game.utility(state, hero)
    player = game.current_player(state)
    dist = policies[player](game, state)
    value = 0.0
    for action, prob in dist.items():
        if prob > 0.0:
            value += prob * _ev(game, game.apply(state, action), hero, policies)
    return value


# --- info-set-constrained best response ---------------------------------------------
def best_response_value(game, hero: int, opp_policy, iters: int = 16,
                        return_strategy: bool = False):
    """Exact best-response value for `hero` vs a fixed `opp_policy`.

    Iterative refinement (same idea as step03's Leduc BR): repeatedly accumulate
    counterfactual values per hero info set, take the argmax action at each, and iterate to
    a fixpoint (reached in <= tree depth passes). Then evaluate the final deterministic BR
    exactly. The result is the highest EV `hero` can guarantee against `opp_policy`.
    """
    br = {}  # info_set -> chosen action id
    for _ in range(iters):
        cv = {}  # info_set -> {action: counterfactual value}
        for deal in game.deals():
            _accumulate(game, game.root(deal), hero, opp_policy, br,
                        game.deal_prob(deal), cv)
        changed = False
        for iset, action_vals in cv.items():
            best_a = max(action_vals, key=action_vals.get)
            if br.get(iset) != best_a:
                br[iset] = best_a
                changed = True
        if not changed:
            break

    value = _br_eval(game, hero, opp_policy, br)
    if return_strategy:
        return value, br
    return value


def _accumulate(game, state, hero, opp_policy, br, reach, cv) -> float:
    """Traverse, accumulating reach-weighted counterfactual values at hero info sets.
    Returns the hero's value at `state` under the *current* BR (for upstream nodes).

    `reach` is the counterfactual reach: chance (folded in via deal_prob at the root) times
    the opponent's action probabilities. It deliberately excludes the hero's own action
    probabilities -- that is what makes the per-info-set argmax a best response.
    """
    if game.is_terminal(state):
        return game.utility(state, hero)

    player = game.current_player(state)
    legal = game.legal_actions(state)

    if player == hero:
        iset = game.info_set(state, hero)
        slot = cv.setdefault(iset, {a: 0.0 for a in legal})
        action_values = {}
        for a in legal:
            child = _accumulate(game, game.apply(state, a), hero, opp_policy, br, reach, cv)
            slot[a] += reach * child
            action_values[a] = child
        if iset in br and br[iset] in action_values:
            return action_values[br[iset]]
        return max(action_values.values())
    else:
        dist = opp_policy(game, state)
        value = 0.0
        for a in legal:
            pa = dist.get(a, 0.0)
            if pa > 0.0:
                value += pa * _accumulate(game, game.apply(state, a), hero, opp_policy,
                                          br, reach * pa, cv)
        return value


def _br_eval(game, hero, opp_policy, br) -> float:
    total = 0.0
    for deal in game.deals():
        total += game.deal_prob(deal) * _br_eval_node(game, game.root(deal), hero,
                                                       opp_policy, br)
    return total


def _br_eval_node(game, state, hero, opp_policy, br) -> float:
    if game.is_terminal(state):
        return game.utility(state, hero)
    player = game.current_player(state)
    legal = game.legal_actions(state)
    if player == hero:
        iset = game.info_set(state, hero)
        a = br.get(iset, legal[0])
        if a not in legal:
            a = legal[0]
        return _br_eval_node(game, game.apply(state, a), hero, opp_policy, br)
    else:
        dist = opp_policy(game, state)
        value = 0.0
        for a in legal:
            pa = dist.get(a, 0.0)
            if pa > 0.0:
                value += pa * _br_eval_node(game, game.apply(state, a), hero, opp_policy, br)
        return value


def best_response_policy(game, hero: int, opp_policy, iters: int = 16):
    """The exact best response to `opp_policy`, returned as a deterministic policy."""
    _, br = best_response_value(game, hero, opp_policy, iters, return_strategy=True)

    def policy(game, state):
        legal = game.legal_actions(state)
        a = br.get(game.info_set(state))
        if a is None or a not in legal:
            a = legal[0]
        return {x: (1.0 if x == a else 0.0) for x in legal}

    return policy


# --- exploitability ------------------------------------------------------------------
def nash_gap(game, policy0, policy1) -> dict:
    """NashConv exploitability of the profile (policy0, policy1).

    Returns a dict with the two best-response gains and their sum. For zero-sum games,
    NashConv = br0 + br1, where br_p is the most player p can win by best-responding while
    the opponent holds fixed. A true Nash equilibrium has NashConv ~ 0.
    """
    br0 = best_response_value(game, 0, policy1)  # best P0 can do vs P1 (P0 utility)
    br1 = best_response_value(game, 1, policy0)  # best P1 can do vs P0 (P1 utility)
    return {"br0": br0, "br1": br1, "nash_conv": br0 + br1}


def _selftest():
    from engines import make_game
    from policies import uniform_policy
    print("best_response self-test")
    print("-" * 50)
    for name in ("kuhn", "leduc"):
        game = make_game(name)
        unif = uniform_policy()
        br0 = best_response_value(game, 0, unif)
        br1 = best_response_value(game, 1, unif)
        gap = nash_gap(game, unif, unif)
        print(f"[{name}] BR0 vs uniform = {br0:+.4f}, BR1 vs uniform = {br1:+.4f}, "
              f"NashConv(uniform,uniform) = {gap['nash_conv']:.4f}")
        print(f"        (a best responder should strictly beat a uniform-random player: "
              f"both BRs > 0 expected)")


if __name__ == "__main__":
    _selftest()
