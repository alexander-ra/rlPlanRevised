"""
Shared likelihood machinery for the opponent models.

The one idea here: the likelihood of a hand under a candidate opponent strategy is the
product of that strategy's probabilities for the *opponent's* actions only (the hero's
actions are fixed data). When the opponent's card is hidden, we marginalize that product
over every card the opponent could have held.

  opp_logprob(game, opp, deal, actions, policy)
      log P(opponent's observed actions | policy), assuming the opponent held `deal`.

  marginal_loglik(game, opp, candidate_deals, actions, policy)
      log of the average of exp(opp_logprob) over the candidate deals -- i.e. the
      partial-observability-marginalized log-likelihood of the hand.

A small probability floor avoids -inf blowups when a strategy assigns (near) zero mass to
an action that was nonetheless observed. (The smoothed types never do this; Nash and exact
best responses can, which is why the floor matters.)

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import math

_LOG_FLOOR = math.log(1e-12)  # log of the smallest probability we will trust


def logsumexp(values) -> float:
    """Numerically stable log(sum(exp(v))). Returns -inf for an all-empty/-inf input."""
    finite = [v for v in values if v != -math.inf]
    if not finite:
        return -math.inf
    m = max(finite)
    s = sum(math.exp(v - m) for v in finite)
    return m + math.log(s)


def opp_logprob(game, opp: int, deal, actions, policy, floor: bool = True) -> float:
    """log P(opponent's actions | policy) assuming the opponent held `deal`.

    Steps the public action sequence and accumulates log-probability only at the
    opponent's decision nodes.
    """
    state = game.root(deal)
    total = 0.0
    for a in actions:
        player = game.current_player(state)
        if player == opp:
            dist = policy(game, state)
            pa = dist.get(a, 0.0)
            lp = math.log(pa) if pa > 0.0 else -math.inf
            if floor:
                lp = max(lp, _LOG_FLOOR)
            total += lp
        state = game.apply(state, a)
    return total


def marginal_loglik(game, opp: int, candidate_deals, actions, policy,
                    floor: bool = True) -> float:
    """Partial-observability-marginalized log-likelihood of one hand under `policy`.

    Uniform prior over the candidate deals, so this is logsumexp(per-deal logprobs) minus
    log(#candidate deals). With a single candidate deal (a showdown) it reduces to
    opp_logprob.
    """
    if not candidate_deals:
        return 0.0  # opponent never acted / no consistent deal: a no-op observation
    lps = [opp_logprob(game, opp, d, actions, policy, floor) for d in candidate_deals]
    return logsumexp(lps) - math.log(len(candidate_deals))
