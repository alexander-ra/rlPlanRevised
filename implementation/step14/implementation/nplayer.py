"""
nplayer.py -- the N-player (three-player Kuhn) side of the framework.

What extends from two players, and what does not:
  * exact expected values, unilateral best responses and NashConv extend unchanged
    (trees.TabularGame is N-player);
  * "exploitability = worst case below the game value" does NOT: there is no game value, and
    NashConv measures distance from AN equilibrium, not what a player is guaranteed
    (Lanctot et al. 2019; Szafron et al. 2013). This module computes the substitutes:
      - deviation gain     delta_i = max_{s_i'} u_i(s_i', s_-i) - u_i(s)   (NashConv component)
      - single-opponent damage   u_i(s) - min_{s_j} u_i(s_j, s_-j)   (one spiteful opponent)
      - coalition value    min_{s_j, s_k} u_i(s_i, s_j, s_k): the two opponents jointly
        minimise player i's payoff with ex-ante coordinated strategies. A linear objective over
        correlated joint strategies is minimised at a pure joint profile, so enumerating one
        member's 2^16 pure strategies and best-responding with the other is exact
        (the team-maxmin setting of Celli & Gatti 2018 / Zhang et al. 2021, used here only as an
        evaluation probe).

The adaptive three-player agent (DirBR3P) generalises Chapter 7's continuous model to two
opponents: a Dirichlet model per opponent information set, with hidden cards handled by
posterior-weighted soft counts over the joint assignments of the unseen cards; it
best-responds to the modelled pair, optionally blended with the equilibrium blueprint. It has
no safety guarantee -- that is exactly the gap Contribution 2 addresses.
"""

from __future__ import annotations

import itertools

import numpy as np

from trees import TabularGame, pure_strategies
from agents import Agent, HandRecord

PASS, BET = 0, 1


# ---------------------------------------------------------------- stationary types
def type_profile(tg: TabularGame, fn, eps: float = 0.05) -> list:
    """fn(card, history, facing_bet) -> P(bet/call). eps-smoothed like Chapter 7's types."""
    prof = []
    for p, P in enumerate(tg.players):
        B = np.zeros((len(P.infoset_strings), tg.n_actions))
        for I, s in enumerate(P.infoset_strings):
            card, hist = int(s[0]), s[1:]
            pb = fn(card, hist, "b" in hist)
            pb = (1 - eps) * pb + eps * 0.5
            B[I, BET], B[I, PASS] = pb, 1 - pb
        prof.append(B)
    return prof


def kuhn3_types(tg: TabularGame) -> dict:
    top = tg.game.num_players()  # cards 0..n; the top card is n
    return {
        "AlwaysPass": type_profile(tg, lambda c, h, f: 0.0),
        "AlwaysBet": type_profile(tg, lambda c, h, f: 1.0),
        "TightPassive": type_profile(tg, lambda c, h, f: 1.0 if c == top else 0.0),
        "LooseAggr": type_profile(tg, lambda c, h, f: 0.85),
        "Random": tg.uniform_profile(),
    }


# ---------------------------------------------------------------- batched best response
def _level_scatter(tg: TabularGame, p: int):
    P = tg.players[p]
    out = []
    for lvl in P.levels:
        S = np.zeros((len(lvl), P.n_seq))
        S[np.arange(len(lvl)), P.parent_seq[lvl]] = 1.0
        out.append((lvl, S))
    return out


def br_batch(tg: TabularGame, p: int, CV: np.ndarray) -> np.ndarray:
    """Best-response values for a batch of counterfactual-value vectors CV (batch x n_seq)."""
    P = tg.players[p]
    child = np.zeros_like(CV)
    for lvl, S in reversed(_level_scatter(tg, p)):
        sids = P.seq_id[lvl]                         # (k, A)
        mask = sids >= 0
        tot = CV + child
        vals = np.where(mask[None], tot[:, np.maximum(sids, 0)], -np.inf)   # (b, k, A)
        best = vals.max(axis=2)                      # (b, k)
        child = child + best @ S
    return CV[:, 0] + child[:, 0]


class CoalitionProbe:
    """Exact coalition value of a fixed strategy of player i against the other two."""

    def __init__(self, tg: TabularGame):
        assert tg.n_players == 3
        self.tg = tg
        self.pure = {}
        self.onehot = {}
        for p in range(3):
            self.onehot[p] = np.zeros((tg.n_term, tg.players[p].n_seq))
            self.onehot[p][np.arange(tg.n_term), tg.term_seq[:, p]] = 1.0

    def _pure(self, p):
        if p not in self.pure:
            self.pure[p] = pure_strategies(self.tg, p)
        return self.pure[p]

    def value(self, i: int, B_i: np.ndarray, chunk: int = 8192) -> float:
        tg = self.tg
        j, k = [q for q in range(3) if q != i]
        r_i = tg.realization(i, B_i)
        base = tg.term_chance * r_i[tg.term_seq[:, i]] * tg.term_util[:, i]      # (Z,)
        Rj = self._pure(j)
        best = np.inf
        for s in range(0, len(Rj), chunk):
            W = Rj[s:s + chunk][:, tg.term_seq[:, j]] * base[None]              # (b, Z)
            CVk = W @ self.onehot[k]                                            # (b, nseq_k)
            v = -br_batch(tg, k, -CVk)                                          # min over k
            best = min(best, float(v.min()))
        return best


def single_damage(tg: TabularGame, i: int, profile: list, j: int) -> float:
    """min over player j's strategies of player i's value (others fixed)."""
    w = tg._reach_terms(profile, skip=j) * (-tg.term_util[:, i])
    cv = np.bincount(tg.term_seq[:, j], weights=w, minlength=tg.players[j].n_seq)
    return -tg._br_backward(j, cv, False)


def deviation_gain(tg: TabularGame, i: int, profile: list) -> float:
    return tg.best_response(i, profile) - float(tg.values(profile)[i])


# ---------------------------------------------------------------- the adaptive 3P agent
class DirBR3P(Agent):
    adaptive = True

    def __init__(self, name: str, blueprint: list, lam: float = 1.0, refit_every: int = 50,
                 min_hands: int = 25):
        self.name, self.blueprint, self.lam = name, blueprint, lam
        self.refit_every, self.min_hands = refit_every, min_hands

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.opps = [q for q in range(tg.n_players) if q != seat]
        self.counts = {q: np.zeros((len(tg.players[q].infoset_strings), tg.n_actions))
                       for q in self.opps}
        self.B = self.blueprint[seat]
        self.n = 0
        self.n_cards = tg.n_players + 1

    def policy(self):
        return self.B

    def model(self, q):
        m = self.tg.players[q].legal_mask
        c = np.where(m, self.counts[q] + 1.0, 0.0)
        return c / c.sum(axis=1, keepdims=True)

    def observe(self, rec: HandRecord):
        tg = self.tg
        cards = rec.chances[:tg.n_players]
        hist, dec = "", []                 # (player, history-before, action)
        folded = set()
        bet = False
        for node, a in rec.decisions:
            q = int(tg.player[node])
            dec.append((q, hist, a))
            if bet and a == PASS:
                folded.add(q)
            if a == BET:
                bet = True
            hist += "p" if a == PASS else "b"
        alive = [q for q in range(tg.n_players) if q not in folded]
        revealed = set(alive) if len(alive) >= 2 else set()
        known = {self.seat: cards[self.seat]}
        for q in revealed:
            known[q] = cards[q]
        hidden = [q for q in self.opps if q not in known]
        free = [c for c in range(self.n_cards) if c not in known.values()]
        models = {q: self.model(q) for q in self.opps}

        def lik(q, c):
            L = 1.0
            P = tg.players[q]
            for (pl, h, a) in dec:
                if pl == q:
                    L *= models[q][P.infoset_index[f"{c}{h}"], a]
            return L

        assigns = [dict(zip(hidden, combo)) for combo in itertools.permutations(free, len(hidden))]
        weights = np.array([np.prod([lik(q, c) for q, c in asg.items()]) for asg in assigns]) \
            if hidden else np.array([1.0])
        weights = weights / weights.sum() if weights.sum() > 0 else np.full(len(weights), 1 / len(weights))
        for q in self.opps:
            P = tg.players[q]
            if q in known:
                for (pl, h, a) in dec:
                    if pl == q:
                        self.counts[q][P.infoset_index[f"{known[q]}{h}"], a] += 1.0
            else:
                for asg, w in zip(assigns, weights):
                    for (pl, h, a) in dec:
                        if pl == q:
                            self.counts[q][P.infoset_index[f"{asg[q]}{h}"], a] += w
        self.n += 1
        if self.n % self.refit_every == 0 and self.n >= self.min_hands:
            prof = [None] * tg.n_players
            for q in self.opps:
                prof[q] = self.model(q)
            prof[self.seat] = tg.uniform(self.seat)
            _, br = tg.best_response(self.seat, prof, return_policy=True)
            self.B = self.lam * br + (1 - self.lam) * self.blueprint[self.seat]
            self.version += 1


class Stationary3(Agent):
    def __init__(self, name, profile):
        self.name, self.profile = name, profile

    def policy(self):
        return self.profile[self.seat]


class Switching3(Agent):
    adaptive = True

    def __init__(self, name, first, second, T):
        self.name, self.first, self.second, self.T = name, first, second, T

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.first.start(tg, seat, rng); self.second.start(tg, seat, rng)
        self.t = 0

    def begin_hand(self, t):
        if t == self.T:
            self.version += 1
        self.t = t

    def policy(self):
        return (self.first if self.t < self.T else self.second).policy()


class CoalitionTeacher:
    """Two opponents that bait with stationary types until T, then play the coalition best
    response (exact, ex-ante coordinated) against the victim's CURRENT policy, re-computed
    every R hands. Implemented as a pair of Agent views sharing one planner."""

    def __init__(self, tg, probe_pure_cache, bait_profile, T, R=50):
        self.tg, self.bait, self.T, self.R = tg, bait_profile, T, R
        self.victim = None
        self.pair = None
        self.last = None

    def plan(self, t):
        if t < self.T:
            return
        if self.pair is not None and (t - self.T) % self.R != 0:
            return
        tg = self.tg
        i = self.victim.seat
        j, k = [q for q in range(3) if q != i]
        B_i = self.victim.policy()
        r_i = tg.realization(i, B_i)
        base = tg.term_chance * r_i[tg.term_seq[:, i]] * tg.term_util[:, i]
        Rj = self.pure_j
        onehot_k = np.zeros((tg.n_term, tg.players[k].n_seq))
        onehot_k[np.arange(tg.n_term), tg.term_seq[:, k]] = 1.0
        best, best_m = np.inf, 0
        for s in range(0, len(Rj), 8192):
            W = Rj[s:s + 8192][:, tg.term_seq[:, j]] * base[None]
            v = -br_batch(tg, k, -(W @ onehot_k))
            m = int(v.argmin())
            if v[m] < best:
                best, best_m = float(v[m]), s + m
        # recover member j's pure behaviour and member k's best response to it
        rj = Rj[best_m]
        Bj = tg.behaviour_from_realization(j, rj)
        prof = [None] * 3
        prof[i], prof[j] = B_i, Bj
        w = tg._reach_terms(prof, skip=k) * (-tg.term_util[:, i])
        cv = np.bincount(tg.term_seq[:, k], weights=w, minlength=tg.players[k].n_seq)
        _, Bk = tg._br_backward(k, cv, True)
        self.pair = {j: Bj, k: Bk}
        self.version_bump = True

    def agents(self, pure_j):
        self.pure_j = pure_j
        outer = self

        class View(Agent):
            adaptive = True

            def __init__(self, name):
                self.name = name

            def begin_hand(self, t):
                outer.t = t
                if self.seat == min(q for q in range(3) if q != outer.victim.seat):
                    before = outer.pair
                    outer.plan(t)
                    if outer.pair is not before:
                        self.version += 1
                elif t >= outer.T and (t - outer.T) % outer.R == 0:
                    self.version += 1

            def policy(self):
                if outer.t < outer.T or outer.pair is None:
                    return outer.bait[self.seat]
                return outer.pair[self.seat]

        return View("colluder-a"), View("colluder-b")
