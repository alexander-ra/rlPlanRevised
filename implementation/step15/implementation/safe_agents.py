"""
safe_agents.py -- Ganzfried & Sandholm's safe exploitation algorithms on Chapter 14's engine.

One agent class, `GiftSafe`, implements the five algorithms of G&S (2015) Table I on the
two-player games of Chapter 14 (Kuhn, Leduc), with Chapter 14's agent interface
(start / begin_hand / policy / observe / version), so it runs in Chapter 14's match runner
next to Chapter 14's agents:

  rule='rwywe'   pi_t = argmax_{pi in SAFE(k_t)} u(pi, M)      (Alg. 2 / Alg. 6)
  rule='befewp'  full best response to M if its exploitability <= k_t, else best equilibrium
  rule='beffe'   full best response if k_t >= (T - t + 1) * its exploitability, else best eq.
  rule='besteq'  best equilibrium against M: SAFE(0)             (Sec. 6.3, their baseline)
  rule='br'      full best response to M (not safe)

k is updated every hand with gifts.gift (Alg. 6 when the opponent's card is observed, Sec. 8.2.2
when it is not). SAFE(k) is Chapter 14's one-shot sequence-form LP with the floor v* - k.

Two opponent models:
  model='gs'    G&S's own (Sec. 9.2): observed frequencies with a Dirichlet prior of 5 fictitious
                hands of the opponent's equilibrium strategy at every information set; the
                opponent's card is assumed observed after every hand; refreshed every hand.
  model='cont'  Chapter 7's continuous Dirichlet model (the one Chapter 14's DirBR / RNR / BestEq
                use): only showdown cards are seen, hidden cards get posterior-weighted soft
                counts; refreshed every `refit_every` hands (50, as in Chapter 14).

`reveal` decides what the GIFT accounting may use: 'always' (G&S's experimental assumption) or
'showdown' (the realistic case: the card is known only when the hand is shown down).

LP re-solves (RWYWE): the LP is re-solved when the model is refreshed, when k_t has fallen
below the k the current policy was solved for (needed for safety), or when k_t has grown by
more than `tol` since the last solve. Between re-solves the policy in force was solved for a
k_solved <= k_t, so its worst case is >= v* - k_t and the safety argument is unaffected.
"""

from __future__ import annotations

import numpy as np

import boot  # noqa: F401
from agents import Agent
from observation_buffer import ObservationBuffer          # Step 07
from continuous_model import ContinuousModel               # Step 07
from solvers import worst_case
import gifts

LP_MARGIN = 1e-7   # the floor is enforced at v* - k - LP_MARGIN (Chapter 14's BestEq uses 1e-7)


def floor_tiebreak(lp, opp_B, floor, ref_B, fill=None):
    """Chapter 14's floor LP, then a second stage that breaks ties: among the solutions within
    1e-9 (relative) of the optimal expected value against the model, return the one closest in
    L1 (sequence form) to the reference strategy ref_B. Without it, HiGHS returns an arbitrary
    vertex of the optimal face -- e.g. against an equilibrium-like model in Kuhn it picks the
    equilibrium that never bluffs and never bets the King (see EXECUTION_NOTES, P0)."""
    import scipy.sparse as sp
    from scipy.optimize import linprog
    B1, _ = lp.floor(opp_B, floor, fill=fill)
    c_mod = lp.c_model(opp_B)
    x1 = lp.tg.realization(lp.hero, B1)
    opt = float(c_mod @ x1)
    r_ref = lp.tg.realization(lp.hero, ref_B)
    nx, nv = lp.n_x, lp.n_v
    # variables: [x (nx), v (nv), d (nx)]
    Z = lambda r, c: sp.csr_matrix((r, c))  # noqa: E731
    A_ub = sp.vstack([
        sp.hstack([lp.A_ub, Z(lp.A_ub.shape[0], nx)]),
        sp.hstack([sp.csr_matrix(np.r_[np.zeros(nx), -1.0, np.zeros(nv - 1)]), Z(1, nx)]),   # v0 >= floor
        sp.hstack([sp.csr_matrix(-c_mod), Z(1, nv), Z(1, nx)]),                             # c.x >= opt - tol
        sp.hstack([sp.identity(nx), Z(nx, nv), -sp.identity(nx)]),                          # x - d <= r
        sp.hstack([-sp.identity(nx), Z(nx, nv), -sp.identity(nx)]),                         # -x - d <= -r
    ]).tocsr()
    tol = 1e-9 * (1.0 + abs(opt))
    b_ub = np.concatenate([lp.b_ub, [-floor], [-(opt - tol)], r_ref, -r_ref])
    A_eq = sp.hstack([lp.A_eq, Z(lp.A_eq.shape[0], nx)]).tocsr()
    c = np.concatenate([np.zeros(nx + nv), np.ones(nx)])
    bounds = list(lp.bounds) + [(0, None)] * nx
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=lp.b_eq, bounds=bounds, method="highs")
    if not res.success:
        return B1
    return lp.policy(res.x[:nx], fill)


class GiftSafe(Agent):
    adaptive = True
    needs_hand07 = True

    def __init__(self, name: str, ctx, rule: str = "rwywe", model: str = "cont",
                 reveal: str = "showdown", refit_every: int = 50, horizon: int | None = None,
                 tol: float = 0.0, prior_hands: float = 5.0, tiebreak: bool = False):
        assert rule in ("rwywe", "befewp", "beffe", "besteq", "br")
        assert model in ("cont", "gs") and reveal in ("always", "showdown")
        self.name, self.ctx, self.rule, self.model_kind = name, ctx, rule, model
        self.reveal, self.refit_every, self.T, self.tol = reveal, refit_every, horizon, tol
        self.prior_hands = prior_hands
        self.tiebreak = tiebreak

    # ------------------------------------------------------------------ lifecycle
    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        ctx = self.ctx
        self.opp = 1 - seat
        self.v_star = float(ctx.v_star[seat])
        self.lp = ctx.lps[seat]
        self.blueprint = ctx.blueprint
        if self.model_kind == "cont":
            g07 = ctx.bridge.g07
            self.model = ContinuousModel(g07, seat)
            self.buffer = ObservationBuffer(g07, seat)
        else:
            P = tg.players[self.opp]
            self.counts = np.zeros((len(P.infoset_strings), tg.n_actions))
        self.k = 0.0
        self.k_solved = None
        self.k_trace = []
        self.n_seen = 0
        self.n_solves = 0
        self.mode_trace = []           # 1 = full BR in force, 0 = otherwise (for befewp/beffe)
        self.opp_B = self._model_policy()
        self.model_version = 0
        self._last_model_version = -1
        self.B = None
        self.t = 0
        self._select(0)

    # ------------------------------------------------------------------ model
    def _model_policy(self):
        tg = self.tg
        if self.model_kind == "cont":
            return self.ctx.bridge.materialize(self.model.predicted_policy(), self.opp)
        prior = self.blueprint[self.opp]
        n = self.counts.sum(axis=1, keepdims=True)
        B = (self.counts + self.prior_hands * prior) / (n + self.prior_hands)
        return tg.normalize(self.opp, B)

    def _full_br(self):
        prof = [None, None]
        prof[self.seat] = self.tg.uniform(self.seat)
        prof[self.opp] = self.opp_B
        return self.tg.best_response(self.seat, prof, return_policy=True)[1]

    def _solve_floor(self, k):
        floor = self.v_star - max(k, 0.0) - LP_MARGIN
        self.n_solves += 1
        if self.tiebreak:
            return floor_tiebreak(self.lp, self.opp_B, floor, self.blueprint[self.seat],
                                  fill=self.blueprint[self.seat])
        return self.lp.floor(self.opp_B, floor, fill=self.blueprint[self.seat])[0]

    # ------------------------------------------------------------------ policy selection
    def _select(self, t):
        rule, k = self.rule, self.k
        model_new = self._last_model_version != self.model_version
        newB = None
        if rule == "br":
            if model_new:
                newB = self._full_br()
        elif rule == "besteq":
            if model_new:
                newB = self._solve_floor(0.0)
        elif rule == "rwywe":
            if model_new or not hasattr(self, "_br_cache"):
                self._br_cache = self._full_br()
                self._br_delta = self.v_star - worst_case(self.tg, self.seat, self._br_cache)
            if k >= self._br_delta + 1e-9:
                # the floor v* - k is slack for the full best response to the model, so it IS
                # the k-safe best response: no LP needed (exact shortcut)
                if self.B is not self._br_cache:
                    newB = self._br_cache
                self.k_solved = self._br_delta
                self.mode_trace.append(1)
            else:
                # k < k_solved forces a re-solve (safety); when k_solved is already 0 the policy
                # is the best equilibrium and a tiny negative k is LP-tolerance noise (~1e-7).
                if (model_new or self.k_solved is None or self.B is self._br_cache
                        or (k < self.k_solved - 1e-9 and self.k_solved > 0.0)
                        or k > self.k_solved + self.tol):
                    newB = self._solve_floor(k)
                    self.k_solved = max(k, 0.0)
                self.mode_trace.append(0)
        else:  # befewp / beffe
            if model_new or not hasattr(self, "_br_cache"):
                self._br_cache = self._full_br()
                self._br_delta = self.v_star - worst_case(self.tg, self.seat, self._br_cache)
                self._eq_cache = self._solve_floor(0.0)
            if rule == "befewp":
                use_br = self._br_delta <= k
            else:
                remaining = (self.T - t) if self.T is not None else np.inf
                use_br = k >= remaining * self._br_delta
            newB = self._br_cache if use_br else self._eq_cache
            self.mode_trace.append(1 if use_br else 0)
            if self.B is not None and newB is self.B:
                newB = None
        self._last_model_version = self.model_version
        if newB is not None:
            self.B = newB
            self.version += 1

    def begin_hand(self, t):
        self.t = t
        self._select(t)

    def policy(self):
        return self.B

    # ------------------------------------------------------------------ observation
    def observe(self, rec):
        tg = self.tg
        # 1. gift accounting with the policy that was in force for this hand
        if self.reveal == "always":
            seen = True
        else:
            seen = self.opp in rec.hand07.revealed
        inc = gifts.gift(tg, self.seat, self.B, self.v_star, list(rec.chances), list(rec.actions), seen)
        self.k += inc
        self.k_trace.append(self.k)
        # 2. opponent model
        self.n_seen += 1
        if self.model_kind == "cont":
            obs = self.buffer.record(rec.hand07)
            self.model.update(obs)
            if self.n_seen % self.refit_every == 0:
                self.opp_B = self._model_policy()
                self.model_version += 1
        else:
            for node, a in rec.decisions:
                if tg.player[node] == self.opp:
                    self.counts[tg.infoset[node], a] += 1.0   # card observed (G&S's assumption)
            if self.n_seen % self.refit_every == 0:
                self.opp_B = self._model_policy()
                self.model_version += 1
