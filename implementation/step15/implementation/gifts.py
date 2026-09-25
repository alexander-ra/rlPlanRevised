"""
gifts.py -- Ganzfried & Sandholm's gift accounting for repeated two-player zero-sum games.

Source (read in full, 2026-09-25): S. Ganzfried and T. Sandholm, "Safe Opponent Exploitation",
ACM Transactions on Economics and Computation 3(2), Article 8, 2015 (DOI 10.1145/2716322);
PDF from the authors' CMU page. The relevant pieces:

  * Def. 4.1  a strategy for the repeated game is SAFE if it guarantees a worst-case payoff of
              at least v* per period in expectation.
  * Alg. 2    RWYWE: k_1 = 0; at iteration t play pi_t = argmax_{pi in SAFE(k_t)} u(pi, M)
              (the k_t-safe best response to the opponent model M, i.e. worst case >= v* - k_t);
              update k_{t+1} = k_t + u(pi_t, a_t) - v*, where u(pi_t, a_t) is the expected payoff
              of OUR MIXED strategy against the opponent's observed action (expectation over our
              own randomisation, not our realised action -- that is RWYW, which is not safe,
              Prop. 6.1).
  * Alg. 6    extensive-form games of imperfect information, opponent's private information
              observed at the end of the hand: the update uses tau_hat, "a best response to pi_t
              subject to the constraint that it plays a_t on the path of play with private
              information theta_t"; k_{t+1} = k_t + u(pi_t, tau_hat) - v*.  (Prop. 8.7: safe.)
  * Sec. 8.2.2  private information NOT observed: tau_hat is the best response "subject to the
              constraint that he plays a_t with some private information" -- i.e. the minimum
              over every private card consistent with the observation.
  * Sec. 9    Kuhn experiments: frequency model with a Dirichlet prior of 5 fictitious hands at
              the (unique) equilibrium of player 2, opponent's card assumed observed after every
              hand, all algorithms adapted with Alg. 6's pessimistic update.

Why the update is safe (the argument of Lemmas 6.2/6.3 and Prop. 8.7, restated for the code):
the opponent's actual pure strategy s satisfies the constraint, so u(pi_t, tau_hat) <=
u(pi_t, s) for every realisation, hence E[k_{t+1} - k_t] <= u(pi_t, tau_t) - v*; and because
pi_t's worst case is >= v* - k_t, k never goes below 0.  Summing: total expected payoff >= T v*.

Everything below is exact on Chapter 14's array trees (trees.TabularGame).
"""

from __future__ import annotations

import numpy as np

import boot  # noqa: F401
from trees import TabularGame, CHANCE, DECISION, TERMINAL


def constrained_br_value(tg: TabularGame, hero: int, B_h: np.ndarray, forced: dict) -> float:
    """Hero's expected value when the opponent best-responds to B_h subject to playing the
    action forced[I] at each opponent information set I in `forced` (two-player zero-sum)."""
    o = 1 - hero
    P = tg.players[o]
    prof = [None, None]
    prof[hero] = B_h
    prof[o] = tg.uniform(o)
    w = tg._reach_terms(prof, skip=o) * tg.term_util[:, o]
    cv = np.bincount(tg.term_seq[:, o], weights=w, minlength=P.n_seq)
    childsum = np.zeros(P.n_seq)
    for lvl in reversed(P.levels):
        sids = P.seq_id[lvl]
        mask = sids >= 0
        if forced:
            mask = mask.copy()
            for r, I in enumerate(lvl):
                a = forced.get(int(I))
                if a is not None:
                    keep = np.zeros_like(mask[r])
                    keep[a] = True
                    mask[r] &= keep
        vals = np.where(mask, cv[np.maximum(sids, 0)] + childsum[np.maximum(sids, 0)], -np.inf)
        np.add.at(childsum, P.parent_seq[lvl], vals.max(axis=1))
    return -float(cv[0] + childsum[0])


def _walk(tg: TabularGame, chances: list, actions: list):
    """Replay a hand on the tree; returns the decision (node, action) list, or None if a chance
    outcome is illegal on this path (e.g. a substituted card clashes with the board)."""
    i, ci, ai = 0, 0, 0
    out = []
    while tg.kind[i] != TERMINAL:
        if tg.kind[i] == CHANCE:
            if ci >= len(chances):
                return None
            a = chances[ci]
            ci += 1
        else:
            if ai >= len(actions):
                return None
            a = actions[ai]
            ai += 1
            out.append((i, a))
        if a < 0 or a >= tg.child_width or tg.child_of[i, a] < 0:
            return None
        i = tg.child_of[i, a]
    return out


def forced_sets(tg: TabularGame, hero: int, chances: list, actions: list, card_observed: bool):
    """One `forced` dict per private card of the opponent that is consistent with what the hero
    observed. The opponent's private card is the chance outcome at position `opp` (OpenSpiel
    deals seat 0, then seat 1). With the card observed there is exactly one set."""
    o = 1 - hero
    if card_observed:
        cands = [chances[o]]
    else:
        # every card the opponent could hold: any outcome of its deal node that keeps the replay legal
        cands = list(range(tg.child_width))
    out = []
    for c in cands:
        ch = list(chances)
        ch[o] = c
        dec = _walk(tg, ch, actions)
        if dec is None:
            continue
        forced = {int(tg.infoset[n]): int(a) for n, a in dec if tg.player[n] == o}
        out.append(forced)
    if not out:
        raise RuntimeError("no consistent private card -- replay bug")
    return out


def gift(tg: TabularGame, hero: int, B_h: np.ndarray, v_star: float, chances: list,
         actions: list, card_observed: bool) -> float:
    """k-increment of Alg. 6 (card observed) or Sec. 8.2.2 (card not observed):
    min over consistent private cards of u(pi_t, tau_hat) - v*."""
    return min(constrained_br_value(tg, hero, B_h, f) for f in
               forced_sets(tg, hero, chances, actions, card_observed)) - v_star
