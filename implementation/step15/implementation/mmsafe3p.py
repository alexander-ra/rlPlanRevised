"""
mmsafe3p.py -- Ganzfried & Sandholm's safe exploitation with the MAXIMIN floor, three players.

G&S (2015, Sec. 2.3): "For general-sum and multiplayer games, our methodology applies
straightforwardly if we replace the minimax value with the maximin value." This module makes that
remark concrete for three-player Kuhn poker, with the maximin value taken against a COORDINATED
pair of opponents (ex-ante correlation: the team-maxmin value, maximin3p.py):

    v_mm      = max_sigma min_{joint y} u_i(sigma, y)
    SAFE(k)   = { sigma : min_{joint y} u_i(sigma, y) >= v_mm - k }        (coalition value)
    MM-RWYWE  pi_t = argmax_{sigma in SAFE(k_t)} u_i(sigma, model);  k_1 = 0;
              k_{t+1} = k_t + min_{joint pure y consistent with hand t} u_i(pi_t, y) - v_mm.

Why the guarantee carries over (G&S's Lemmas 6.2-6.3 with the joint opponent in place of the
single one): the opponents' realised joint pure strategy is consistent with what was observed,
so the pessimistic increment is <= u_i(pi_t, y_t) - v_mm in expectation for ANY (correlated,
adaptive) joint strategy y_t; pi_t's coalition value is >= v_mm - k_t, so k never goes below 0.
Summing: sum_t E u_i(pi_t, y_t) >= T v_mm against any opponents, colluding or not.

The consistent set: with the opponents' cards observed (G&S's experimental assumption, 'always'),
each opponent must play its observed actions at the information sets it visited; with only
showdown cards observed ('showdown'), the minimum also runs over every assignment of the unseen
cards. Everything is exact: the minimum over joint pure strategies enumerates the unique pure
realisation plans of the smaller opponent (6,561 or 10,000 here) and best-responds with the
other, restricted to the observed actions.
"""

from __future__ import annotations

import itertools

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

import boot  # noqa: F401
from trees import TabularGame, pure_strategies, CHANCE, TERMINAL
from bounded3p import _Model3P

LP_MARGIN = 1e-7
ACCEPT_TOL = 2e-6       # the oracle must confirm coalition value >= v_mm - k - ACCEPT_TOL (LP tolerance)
CUT_POOL: dict = {}      # per seat: cuts are valid constraints for any model and any floor
MAX_CUTS = 3000


def br_batch_forced(tg: TabularGame, p: int, CV: np.ndarray, forced: dict | None) -> np.ndarray:
    """Chapter 14's batched best response (nplayer.br_batch) with some info sets forced."""
    P = tg.players[p]
    child = np.zeros_like(CV)
    for lvl in reversed(P.levels):
        sids = P.seq_id[lvl]
        mask = sids >= 0
        if forced:
            mask = mask.copy()
            for r, I in enumerate(lvl):
                a = forced.get(int(I))
                if a is not None:
                    keep = np.zeros_like(mask[r]); keep[a] = True
                    mask[r] &= keep
        tot = CV + child
        vals = np.where(mask[None], tot[:, np.maximum(sids, 0)], -np.inf)
        best = vals.max(axis=2)
        S = np.zeros((len(lvl), P.n_seq))
        S[np.arange(len(lvl)), P.parent_seq[lvl]] = 1.0
        child = child + best @ S
    return CV[:, 0] + child[:, 0]


class CoalitionOracle:
    """Exact minimum of u_i over the two other players' joint pure strategies (optionally
    restricted to observed actions) for seat i of a three-player TabularGame."""

    def __init__(self, tg: TabularGame, i: int):
        self.tg, self.i = tg, i
        others = [q for q in range(3) if q != i]
        uniq = {q: np.unique(pure_strategies(tg, q), axis=0) for q in others}
        self.j = min(others, key=lambda q: len(uniq[q]))       # enumerate the smaller one
        self.k = [q for q in others if q != self.j][0]
        self.Rj = uniq[self.j]                                  # (R, nseq_j) unique pure plans
        self.Mj = self.Rj[:, tg.term_seq[:, self.j]]            # (R, Z)
        self.onehot_k = np.zeros((tg.n_term, tg.players[self.k].n_seq))
        self.onehot_k[np.arange(tg.n_term), tg.term_seq[:, self.k]] = 1.0
        self._cv_cache = {}
        self.calls = 0

    def base(self, x: np.ndarray) -> np.ndarray:
        tg = self.tg
        return tg.term_chance * x[tg.term_seq[:, self.i]] * tg.term_util[:, self.i]

    def _cv(self, base, key=None):
        if key is not None and key in self._cv_cache:
            return self._cv_cache[key]
        cv = self.Mj @ (base[:, None] * self.onehot_k)          # (R, nseq_k)
        if key is not None:
            if len(self._cv_cache) > 8:
                self._cv_cache.clear()
            self._cv_cache[key] = cv
        return cv

    def row_mask(self, forced_j: dict) -> np.ndarray:
        P = self.tg.players[self.j]
        m = np.ones(len(self.Rj), dtype=bool)
        for I, a in forced_j.items():
            m &= self.Rj[:, P.seq_id[I, a]] > 0.5
        return m

    def min_value(self, base, forced_j=None, forced_k=None, key=None) -> float:
        self.calls += 1
        cv = self._cv(base, key)
        if forced_j:
            cv = cv[self.row_mask(forced_j)]
            if len(cv) == 0:
                return np.inf
        v = -br_batch_forced(self.tg, self.k, -cv, forced_k)
        return float(v.min())

    def argmin_pair(self, base):
        """The minimising coordinated pure pair: (value, r_j, r_k)."""
        tg = self.tg
        cv = self._cv(base)
        v = -br_batch_forced(tg, self.k, -cv, None)
        m = int(v.argmin())
        rj = self.Rj[m]
        w = rj[tg.term_seq[:, self.j]] * base * -1.0
        cvk = np.bincount(tg.term_seq[:, self.k], weights=w, minlength=tg.players[self.k].n_seq)
        _, Bk = tg._br_backward(self.k, cvk, True)
        return float(v[m]), rj, tg.realization(self.k, Bk)

    def cut(self, rj, rk) -> np.ndarray:
        """c with u_i(x, pair) = c . x."""
        tg = self.tg
        w = tg.term_chance * tg.term_util[:, self.i] * rj[tg.term_seq[:, self.j]] * rk[tg.term_seq[:, self.k]]
        return np.bincount(tg.term_seq[:, self.i], weights=w, minlength=tg.players[self.i].n_seq)


def walk3(tg: TabularGame, chances, actions):
    """Replay a hand; the decision list [(node, action)] or None if illegal."""
    i, ci, ai, out = 0, 0, 0, []
    while tg.kind[i] != TERMINAL:
        if tg.kind[i] == CHANCE:
            if ci >= len(chances):
                return None
            a = chances[ci]; ci += 1
        else:
            if ai >= len(actions):
                return None
            a = actions[ai]; ai += 1
            out.append((i, a))
        if a < 0 or a >= tg.child_width or tg.child_of[i, a] < 0:
            return None
        i = tg.child_of[i, a]
    return out


def revealed_players(tg: TabularGame, decisions) -> set:
    """Kuhn: the cards of every player who did not fold are shown if two or more remain."""
    folded, bet = set(), False
    for node, a in decisions:
        q = int(tg.player[node])
        if bet and a == 0:
            folded.add(q)
        if a == 1:
            bet = True
    alive = [q for q in range(tg.n_players) if q not in folded]
    return set(alive) if len(alive) >= 2 else set()


class MMSafe3P(_Model3P):
    """rule='rwywe': the k-safe best response with the maximin floor; rule='besteq': k frozen
    at 0 (the best maximin strategy against the model -- the analogue of the best equilibrium)."""

    def __init__(self, name, blueprint, probe, oracles: dict, v_mm: list, mm_profile: list,
                 rule: str = "rwywe", reveal: str = "always", tol: float = 0.02, **kw):
        super().__init__(name, blueprint, probe, **kw)
        self.oracles, self.v_mm_all, self.rule, self.reveal, self.tol = oracles, v_mm, rule, reveal, tol
        self.mm_profile = mm_profile

    def start(self, tg, seat, rng):
        super().start(tg, seat, rng)
        self.orc = self.oracles[seat]
        self.v_mm = float(self.v_mm_all[seat])
        self.k, self.k_solved = 0.0, None
        self.k_trace, self.n_solves, self.n_cuts_added, self.unconverged = [], 0, 0, 0
        self.model_version, self._seen_version = 0, -1
        self.cuts = CUT_POOL.setdefault(seat, [])
        self.F, self.f = tg.treeplex_matrix(seat)
        self.B = None
        self._select()

    # -------------------------------------------------------------- model / policy
    def refit(self, t):
        self.model_version += 1

    def _c_model(self):
        tg, s = self.tg, self.seat
        prof = self.model_profile()
        w = tg.term_chance * tg.term_util[:, s]
        for q in self.opps:
            w = w * tg.realization(q, prof[q])[tg.term_seq[:, q]]
        return np.bincount(tg.term_seq[:, s], weights=w, minlength=tg.players[s].n_seq)

    def _solve(self, k):
        """max c_model . x  s.t. coalition value(x) >= v_mm - k, by constraint generation."""
        tg, s = self.tg, self.seat
        n = tg.players[s].n_seq
        floor = self.v_mm - max(k, 0.0) - LP_MARGIN
        c = -self._c_model()
        A_eq = self.F
        x, val = None, -np.inf
        for it in range(200):
            if self.cuts:
                A_ub = sp.csr_matrix(-np.asarray(self.cuts))
                b_ub = -floor * np.ones(len(self.cuts))
            else:
                A_ub, b_ub = None, None
            res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=self.f,
                          bounds=[(0, None)] * n, method="highs")
            if not res.success:
                raise RuntimeError(res.message)
            x = res.x
            val, rj, rk = self.orc.argmin_pair(self.orc.base(x))
            if val >= floor - ACCEPT_TOL:
                break
            self.cuts.append(self.orc.cut(rj, rk))
            if len(self.cuts) > MAX_CUTS:
                del self.cuts[0]
            self.n_cuts_added += 1
        self.n_solves += 1
        if val < floor - ACCEPT_TOL:    # not converged: fall back to the maximin strategy (safe)
            self.unconverged += 1
            return self.mm_profile[s]
        return tg.behaviour_from_realization(s, x, fill=self.blueprint[s])

    def _select(self):
        k = self.k if self.rule == "rwywe" else 0.0
        model_new = self._seen_version != self.model_version
        if model_new:
            tg, s = self.tg, self.seat
            prof = self.model_profile(); prof[s] = tg.uniform(s)
            self._br = tg.best_response(s, prof, return_policy=True)[1]
            self._br_cv = self.orc.min_value(self.orc.base(tg.realization(s, self._br)))
            self._seen_version = self.model_version
        newB = None
        if self._br_cv >= self.v_mm - max(k, 0.0):
            if self.B is not self._br:
                newB = self._br
            self.k_solved = self.v_mm - self._br_cv
        elif (model_new or self.k_solved is None or self.B is self._br
              or (k < self.k_solved - 1e-9 and self.k_solved > 0.0) or k > self.k_solved + self.tol):
            newB = self._solve(k)
            self.k_solved = max(k, 0.0)
        if newB is not None:
            self.B = newB
            self.version += 1
            self._base_B = self.orc.base(self.tg.realization(self.seat, self.B))
            self._key = ("pol", self.version, id(self))

    def begin_hand(self, t):
        self._select()

    # -------------------------------------------------------------- gift accounting
    def _forced_sets(self, rec):
        tg, j, k = self.tg, self.orc.j, self.orc.k
        cards = list(rec.chances[:3])
        acts = [a for _, a in rec.decisions]
        if self.reveal == "always":
            known = {q: cards[q] for q in range(3)}
        else:
            known = {self.seat: cards[self.seat]}
            for q in revealed_players(tg, rec.decisions):
                known[q] = cards[q]
        hidden = [q for q in (j, k) if q not in known]
        free = [c for c in range(4) if c not in known.values()]
        out = []
        for combo in itertools.permutations(free, len(hidden)):
            ch = list(cards)
            for q, c in zip(hidden, combo):
                ch[q] = c
            ch += list(rec.chances[3:])
            dec = walk3(tg, ch, acts)
            if dec is None:
                continue
            fj = {int(tg.infoset[nd]): int(a) for nd, a in dec if tg.player[nd] == j}
            fk = {int(tg.infoset[nd]): int(a) for nd, a in dec if tg.player[nd] == k}
            out.append((fj, fk))
        return out

    def observe(self, rec):
        inc = min(self.orc.min_value(self._base_B, fj, fk, key=self._key)
                  for fj, fk in self._forced_sets(rec)) - self.v_mm
        self.k += inc
        self.k_trace.append(self.k)
        super().observe(rec)      # model counts; refit() marks a new model every 50 hands


class OracleProbe:
    """Probe3's interface (coalition_value, rel_loss) on top of the faster CoalitionOracle
    (unique pure plans of the smaller opponent). Same exact minimum; checked against Probe3."""

    def __init__(self, tg: TabularGame, oracles: dict | None = None):
        self.tg = tg
        self.orc = oracles if oracles is not None else {i: CoalitionOracle(tg, i) for i in range(3)}

    def coalition_value(self, i, B_i):
        o = self.orc[i]
        return o.min_value(o.base(self.tg.realization(i, B_i)))

    def rel_loss(self, i, B_i, B_ref):
        o = self.orc[i]
        d = self.tg.realization(i, B_i) - self.tg.realization(i, B_ref)
        return -o.min_value(o.base(d))
