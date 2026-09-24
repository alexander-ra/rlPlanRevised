"""
aivat.py -- AIVAT (Burch, Schmid, Moravcik, Morrill & Bowling, AAAI 2018; arXiv:1612.06915).

The estimator, as defined in the paper (Eq. 1 and the "AIVAT correction terms" section):

    AIVAT(z) = sum_{z' in W} pi_a(z') v(z') / sum_{z' in W} pi_a(z')      (base value,
                                                   imaginary observations over the known
                                                   player's private cards)
             + sum_{H in partition} k_H(z)

    k_H(z) = sum_{a in A(H)} sum_{h in H} pi_a(h.a) u_h(a) / sum_{h in H} pi_a(h)
           - sum_{h in H} pi_a(h.a_O) u_h(a_O)     / sum_{h in H} pi_a(h.a_O)

where pi_a is the reach probability contributed by the players whose strategies are KNOWN
(chance, plus the agent under test), H groups states with identical betting, public cards and
private cards of the players with unknown strategies, and u_h(a) is an arbitrary value
function fixed in advance (here: node values under an equilibrium self-play profile, as in
the paper's experiments). Theorem 1 of the paper: E_z[sum_H k_H(z)] = 0, so AIVAT is unbiased
for any value function.

Because every quantity above is determined by the observed terminal z (all cards are logged in
simulation) and by the known strategies, AIVAT(z) can be tabulated for every terminal once per
strategy version. That also gives the EXACT mean and variance of the estimator:
    E[AIVAT] = sum_z P(z) AIVAT(z),   Var[AIVAT] = sum_z P(z) (AIVAT(z) - E)^2
so unbiasedness and the variance-reduction factor are checked without sampling noise.

Variants (`known`):
    "chance"        : only chance events corrected, no imaginary observations  (MIVAT-like)
    "chance+x"      : chance + the agent under test (the realistic case -- opponent unknown)
    "chance+x+y"    : both strategies known (only possible when evaluating two bots)
"""

from __future__ import annotations

import numpy as np

from trees import TabularGame, CHANCE, DECISION, TERMINAL


class AivatTables:
    """Precomputed structure for one (game, seat of the agent under test)."""

    def __init__(self, tg: TabularGame, x: int, known: str = "chance+x"):
        assert tg.n_players == 2
        self.tg, self.x, self.y, self.known = tg, x, 1 - x, known
        n = tg.n_nodes
        kind = tg.kind
        self.pa_owner = np.zeros(n, dtype=bool)        # node whose mover is in P_a
        # Players whose private cards are covered by imaginary observations. The deal of such
        # a card gets NO chance-correction term (the paper's Fig. 1: no AIVAT term at the known
        # player's own deal); keeping it would count that card's luck twice and add variance.
        # Dropping a term keeps the estimator unbiased (each k_H has mean zero, Lemma 1).
        imag = {"chance": (), "chance+x": (x,), "chance+x+y": (x, 1 - x)}[known]
        for i in range(n):
            if kind[i] == CHANCE:
                c0 = tg.children[i][0][1]
                diff = np.where(tg.priv[c0] != tg.priv[i])[0]
                dealt_to = int(diff[0]) if len(diff) else -1
                self.pa_owner[i] = dealt_to not in imag
            elif kind[i] == DECISION:
                q = tg.player[i]
                if (q == x and known in ("chance+x", "chance+x+y")) or \
                   (q == self.y and known == "chance+x+y"):
                    self.pa_owner[i] = True

        # history length is part of the key: private deals leave the public history unchanged,
        # so without it a deal node and its parent would share a part (violating property 2).
        depth = np.zeros(n, dtype=np.int32)
        for i in range(1, n):
            depth[i] = depth[tg.parent[i]] + 1

        def key(i):
            if known == "chance":
                return (int(depth[i]), tg.pub[i], tuple(tg.priv[i]))
            if known == "chance+x":
                return (int(depth[i]), tg.pub[i], int(tg.priv[i][self.y]))
            return (int(depth[i]), tg.pub[i])

        gid, groups = np.full(n, -1, dtype=np.int64), {}
        for i in range(n):
            if self.pa_owner[i] or kind[i] == TERMINAL:
                k = (kind[i] == TERMINAL,) + key(i)
                gid[i] = groups.setdefault(k, len(groups))
        self.gid, self.n_groups = gid, len(groups)
        # edge arrays (parent -> child)
        self.child = np.arange(1, n)
        self.par = tg.parent[1:]
        self.act = tg.action_in[1:]
        # depth levels for vectorised forward passes
        self.levels = [np.where(depth == d)[0] for d in range(1, depth.max() + 1)]
        self.term = tg.term_nodes
        self.term_gid = gid[self.term]
        self.edge_owned = self.pa_owner[self.par]
        self.action_width = tg.child_width

    def _edge_factor(self, B_x, B_y):
        tg = self.tg
        par = self.par
        f = np.ones(len(par))
        k = tg.kind[par]
        f[k == CHANCE] = tg.chance_prob[self.child[k == CHANCE]]
        for q, B in ((self.x, B_x), (self.y, B_y)):
            if B is None:
                continue
            m = (k == DECISION) & (tg.player[par] == q)
            f[m] = B[tg.infoset[par[m]], self.act[m]]
        return f

    def table(self, B_x: np.ndarray, V_ref: np.ndarray, B_y: np.ndarray | None = None):
        """AIVAT value of every terminal for the agent in seat x (chips, x's view)."""
        tg = self.tg
        n = tg.n_nodes
        # reach of the known players only
        f_known = self._edge_factor(B_x if self.known != "chance" else None,
                                    B_y if self.known == "chance+x+y" else None)
        pi = np.ones(n)
        for lvl in self.levels:
            pi[lvl] = pi[tg.parent[lvl]] * f_known[lvl - 1]
        # expected term per group and observed term per (group, action)
        G, W = self.n_groups, self.action_width
        own = self.edge_owned
        c, p, a = self.child[own], self.par[own], self.act[own]
        g = self.gid[p]
        u = V_ref[c]
        num_E = np.bincount(g, weights=pi[c] * u, minlength=G)
        # den_E: sum of pi(h) over distinct h in the group
        owners = np.where(self.pa_owner)[0]
        den_E = np.bincount(self.gid[owners], weights=pi[owners], minlength=G)
        ga = g * W + a
        num_O = np.bincount(ga, weights=pi[c] * u, minlength=G * W)
        den_O = np.bincount(ga, weights=pi[c], minlength=G * W)
        with np.errstate(divide="ignore", invalid="ignore"):
            E = np.where(den_E > 0, num_E / den_E, 0.0)
            O = np.where(den_O > 0, num_O / den_O, 0.0)
        kcorr = np.zeros(n)
        kcorr[c] = E[g] - O[ga]
        S = np.zeros(n)
        for lvl in self.levels:
            S[lvl] = S[tg.parent[lvl]] + kcorr[lvl]
        # base value over imaginary observations of the known players' private cards
        z = self.term
        v = tg.term_util[:, self.x]
        if self.known == "chance":
            base = v
        else:
            tg_ = self.term_gid
            num_b = np.bincount(tg_, weights=pi[z] * v, minlength=G)
            den_b = np.bincount(tg_, weights=pi[z], minlength=G)
            with np.errstate(divide="ignore", invalid="ignore"):
                base = np.where(den_b[tg_] > 0, num_b[tg_] / den_b[tg_], v)
        return base + S[z]


def exact_moments(tg: TabularGame, profile: list, values_per_terminal: np.ndarray):
    """Exact mean and variance of a per-hand estimator under the profile."""
    P = tg.terminal_probs(profile)
    m = float(P @ values_per_terminal)
    var = float(P @ (values_per_terminal - m) ** 2)
    return m, var
