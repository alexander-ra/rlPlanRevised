"""
bounded3p.py -- bounded-deviation exploiters for three-player Kuhn poker (the Experiment 2.1 pilot).

What "bounded" means here. There is no game value with three players, so the bound is stated
RELATIVE TO A BASELINE, in the spirit of Mueller et al. (2025)'s comparator regret: the
baseline-relative loss of a strategy sigma for seat i is

    L(sigma) = max over the two opponents' joint strategies y  of  [u_i(bp, y) - u_i(sigma, y)],

the most sigma can fall behind the equilibrium blueprint bp against ANY opponent pair -- including
a pair that coordinates (correlated / colluding play). u_i is linear in the opponents' joint
distribution, so the maximum is attained at a pure pair, and it is computed EXACTLY by the same
enumeration as Chapter 14's coalition value (2^16 pure strategies of one opponent, best response
of the other). This is a worst case over opponents, not over outcomes, and it compares with what
the blueprint would have earned against the same opponent strategies; it is not a guarantee of
any absolute payoff (the blueprint itself loses 0.119 chips/hand to a fixed colluding pair,
Chapter 14).

Two deviation rules, both on top of Chapter 14's DirBR3P opponent model (Dirichlet counts per
opponent information set, hidden cards by posterior-weighted soft counts):

  BoundedMix3P(eps)   sigma_t = (1 - lam_t) bp + lam_t BR_t, mixed in SEQUENCE FORM (so payoffs
                      are linear in lam), with
                          lam_t = conf_t * min(1, eps / L(BR_t)),   conf_t = n_t / (n_t + n0).
                      Then L(sigma_t) = lam_t L(BR_t) <= eps exactly: a per-hand baseline-relative
                      loss cap that holds against any opponents, colluding or adaptive, because it
                      holds for every fixed opponent strategy in every hand.
  KLAnchor3P(beta)    per-information-set KL-regularised best response to the model, anchored to
                      the (smoothed) blueprint:  pi(a|I) ~ bp(a|I) exp(beta_t Q(I,a)),
                      beta_t = beta * conf_t, Q in chips conditional on reaching I. This is the
                      thesis's own proposal (piKL anchors to a human policy, not to an
                      equilibrium: Jacob et al. 2022; Bakhtin et al. 2023). It has NO a-priori
                      bound; L(sigma) is only measured.
"""

from __future__ import annotations

import numpy as np

import boot  # noqa: F401
from trees import TabularGame, pure_strategies, DECISION
from nplayer import br_batch, DirBR3P


class Probe3:
    """Exact minimum, over the two other players' joint (coordinated) strategies, of a linear
    functional sum_z base[z] * r_j[seq_j(z)] * r_k[seq_k(z)] -- Chapter 14's coalition-value
    enumeration, generalised to an arbitrary terminal weight vector."""

    def __init__(self, tg: TabularGame):
        assert tg.n_players == 3
        self.tg = tg
        self._pure = {}
        self.onehot = {}
        for p in range(3):
            m = np.zeros((tg.n_term, tg.players[p].n_seq))
            m[np.arange(tg.n_term), tg.term_seq[:, p]] = 1.0
            self.onehot[p] = m
        self.calls = 0

    def pure(self, p):
        if p not in self._pure:
            self._pure[p] = pure_strategies(self.tg, p)
        return self._pure[p]

    def min_pair(self, i: int, base: np.ndarray, chunk: int = 8192) -> float:
        tg = self.tg
        j, k = [q for q in range(3) if q != i]
        Rj = self.pure(j)
        best = np.inf
        for s in range(0, len(Rj), chunk):
            W = Rj[s:s + chunk][:, tg.term_seq[:, j]] * base[None]
            v = -br_batch(tg, k, -(W @ self.onehot[k]))
            best = min(best, float(v.min()))
        self.calls += 1
        return best

    def coalition_value(self, i: int, B_i: np.ndarray) -> float:
        tg = self.tg
        r = tg.realization(i, B_i)
        return self.min_pair(i, tg.term_chance * r[tg.term_seq[:, i]] * tg.term_util[:, i])

    def rel_loss(self, i: int, B_i: np.ndarray, B_ref: np.ndarray) -> float:
        """max over opponent pairs of u_i(ref) - u_i(B): the baseline-relative worst case."""
        tg = self.tg
        d = tg.realization(i, B_i) - tg.realization(i, B_ref)
        return -self.min_pair(i, tg.term_chance * d[tg.term_seq[:, i]] * tg.term_util[:, i])


def others_reach(tg: TabularGame, seat: int, profile: list) -> np.ndarray:
    """Chance x other players' reach summed over the histories of each of seat's info sets."""
    P = tg.players[seat]
    rho = np.zeros(len(P.infoset_strings))
    nodes = np.where((tg.kind == DECISION) & (tg.player == seat))[0]
    val = tg.reach_chance[nodes].copy()
    for q in range(tg.n_players):
        if q == seat:
            continue
        r = tg.realization(q, profile[q])
        val *= r[tg.node_seq[nodes, q]]
    np.add.at(rho, tg.infoset[nodes], val)
    return rho


def kl_soft_response(tg: TabularGame, seat: int, profile: list, anchor: np.ndarray,
                     beta: float) -> np.ndarray:
    """Backward pass over seat's info sets: at each, pi ~ anchor * exp(beta * Q/rho), where Q is
    the counterfactual action value (continuation under the policy already chosen below) and
    rho the others' reach of the info set, so Q/rho is in chips. beta = 0 returns the anchor;
    beta -> infinity the best response."""
    P = tg.players[seat]
    w = tg._reach_terms(profile, skip=seat) * tg.term_util[:, seat]
    cv = np.bincount(tg.term_seq[:, seat], weights=w, minlength=P.n_seq)
    rho = others_reach(tg, seat, profile)
    childsum = np.zeros(P.n_seq)
    B = np.zeros((len(P.infoset_strings), tg.n_actions))
    for lvl in reversed(P.levels):
        sids = P.seq_id[lvl]
        mask = sids >= 0
        Q = np.where(mask, cv[np.maximum(sids, 0)] + childsum[np.maximum(sids, 0)], 0.0)
        Qn = Q / np.maximum(rho[lvl], 1e-12)[:, None]
        logit = np.where(mask, np.log(np.maximum(anchor[lvl], 1e-300)) + beta * Qn, -np.inf)
        logit -= logit.max(axis=1, keepdims=True)
        pi = np.where(mask, np.exp(logit), 0.0)
        pi /= pi.sum(axis=1, keepdims=True)
        B[lvl] = pi
        np.add.at(childsum, P.parent_seq[lvl], (pi * Q).sum(axis=1))
    return tg.normalize(seat, B)


class _Model3P(DirBR3P):
    """DirBR3P's opponent model with the refit disabled (subclasses decide the response)."""

    def __init__(self, name, blueprint, probe: Probe3, n0: float = 100.0, refit_every: int = 50,
                 min_hands: int = 25):
        super().__init__(name, blueprint, lam=1.0, refit_every=10 ** 12, min_hands=min_hands)
        self.probe, self.n0, self.every = probe, n0, refit_every

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.trace = []

    def model_profile(self):
        prof = [None] * self.tg.n_players
        for q in self.opps:
            prof[q] = self.model(q)
        return prof

    def observe(self, rec):
        super().observe(rec)
        if self.n % self.every == 0 and self.n >= self.min_hands:
            self.conf = self.n / (self.n + self.n0)
            self.refit(rec.t)
            self.version += 1


class BoundedMix3P(_Model3P):
    def __init__(self, name, blueprint, probe, eps: float | None, **kw):
        super().__init__(name, blueprint, probe, **kw)
        self.eps = eps

    def refit(self, t):
        tg, s = self.tg, self.seat
        prof = self.model_profile()
        prof[s] = tg.uniform(s)
        _, br = tg.best_response(s, prof, return_policy=True)
        bp = self.blueprint[s]
        delta = self.probe.rel_loss(s, br, bp)
        cap = 1.0 if (self.eps is None or delta <= self.eps) else self.eps / delta
        lam = self.conf * cap
        r = (1 - lam) * tg.realization(s, bp) + lam * tg.realization(s, br)
        self.B = tg.behaviour_from_realization(s, r, fill=bp)
        self.trace.append({"t": int(t), "lam": float(lam), "delta_br": float(delta),
                           "bound": float(lam * delta), "conf": float(self.conf)})


class KLAnchor3P(_Model3P):
    def __init__(self, name, blueprint, probe, beta: float, smooth: float = 0.02, **kw):
        super().__init__(name, blueprint, probe, **kw)
        self.beta, self.smooth = beta, smooth

    def refit(self, t):
        tg, s = self.tg, self.seat
        prof = self.model_profile()
        prof[s] = tg.uniform(s)
        m = tg.players[s].legal_mask
        anchor = (1 - self.smooth) * self.blueprint[s] + self.smooth * m / m.sum(axis=1, keepdims=True)
        self.B = kl_soft_response(tg, s, prof, anchor, self.beta * self.conf)
        self.trace.append({"t": int(t), "beta": float(self.beta * self.conf), "conf": float(self.conf)})
