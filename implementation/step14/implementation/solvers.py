"""
solvers.py -- equilibrium blueprints and the one-shot safe-exploitation LPs.

Blueprints: OpenSpiel's C++ CFR / CFR+ solvers, converted to this chapter's behaviour arrays
and cached (results/cache/). Chapter 3 wrote CFR from scratch; here the solver is only a
supplier of reference strategies, so the audited C++ implementation is used.

Safe exploitation (two-player zero-sum): Chapter 8 solved "maximise EV against the model
subject to a worst-case floor" by constraint generation (add one adversary best response per
iteration). That loop did not converge on full Leduc within its caps (Chapter 8, Leduc table).
Here the worst case is written in closed form with the opponent's sequence-form dual
(Koller, Megiddo & von Stengel 1996; the standard zero-sum sequence-form LP):

    min_y  x^T A_h y   s.t.  F_o y = f_o, y >= 0     =     max_v  f_o^T v   s.t.  F_o^T v <= A_h^T x

so one LP solves each method exactly:
    maxmin        : max  v_0
    RNR(p)        : max  p * c_model . x + (1 - p) * v_0          (Johanson et al. 2007)
    floor(f)      : max  c_model . x      s.t.  v_0 >= f          (best equilibrium when f = v*)
The result is cross-checked against Chapter 8's constraint-generation solver on Kuhn in
run_validation.py.
"""

from __future__ import annotations

import os

import numpy as np
import pyspiel
import scipy.sparse as sp
from scipy.optimize import linprog

import deps
from trees import TabularGame

CACHE = os.path.join(deps.RESULTS_DIR, "cache")
os.makedirs(CACHE, exist_ok=True)


# ---------------------------------------------------------------- blueprints (CFR / CFR+)
def cfr_profile(tg: TabularGame, iters: int, algo: str = "cfrplus", tag: str = "") -> list:
    """Average strategy of OpenSpiel's C++ CFR+ (or CFR) after `iters` iterations, cached."""
    name = tg.game_string.replace("(", "_").replace(")", "").replace("=", "")
    path = os.path.join(CACHE, f"{name}_{algo}_{iters}{tag}.npz")
    if os.path.exists(path):
        d = np.load(path)
        return [d[f"p{p}"] for p in range(tg.n_players)]
    solver = pyspiel.CFRPlusSolver(tg.game) if algo == "cfrplus" else pyspiel.CFRSolver(tg.game)
    for _ in range(iters):
        solver.evaluate_and_update_policy()
    prof = tg.from_pyspiel_policy(solver.average_policy())
    np.savez(path, **{f"p{p}": prof[p] for p in range(tg.n_players)})
    return prof


def mccfr_profile(tg: TabularGame, iters: int, seed: int) -> list:
    """External-sampling MCCFR average strategy (seeded) -- a different approximate
    equilibrium, used for the three-player equilibrium-multiplicity check."""
    name = tg.game_string.replace("(", "_").replace(")", "").replace("=", "")
    path = os.path.join(CACHE, f"{name}_esmccfr_{iters}_s{seed}.npz")
    if os.path.exists(path):
        d = np.load(path)
        return [d[f"p{p}"] for p in range(tg.n_players)]
    solver = pyspiel.ExternalSamplingMCCFRSolver(tg.game, seed=seed)
    for _ in range(iters):
        solver.run_iteration()
    prof = tg.from_pyspiel_policy(solver.average_policy())
    np.savez(path, **{f"p{p}": prof[p] for p in range(tg.n_players)})
    return prof


# ---------------------------------------------------------------- sequence-form LPs
class SafeLP:
    """Pre-assembled LP data for hero seat h in a two-player zero-sum TabularGame."""

    def __init__(self, tg: TabularGame, hero: int):
        assert tg.n_players == 2
        self.tg, self.hero, self.opp = tg, hero, 1 - hero
        A = tg.payoff_matrix_2p()                    # u0 = r0^T A r1
        self.A_h = A if hero == 0 else -A.T.tocsr()  # hero utility, rows = hero sequences
        self.F_h, self.f_h = tg.treeplex_matrix(hero)
        self.F_o, self.f_o = tg.treeplex_matrix(self.opp)
        self.n_x = tg.players[hero].n_seq
        self.n_v = self.F_o.shape[0]
        # inequality block:  F_o^T v - A_h^T x <= 0
        self.A_ub = sp.hstack([-self.A_h.T, self.F_o.T]).tocsr()
        self.b_ub = np.zeros(self.A_ub.shape[0])
        self.A_eq = sp.hstack([self.F_h, sp.csr_matrix((self.F_h.shape[0], self.n_v))]).tocsr()
        self.b_eq = self.f_h
        self.bounds = [(0, None)] * self.n_x + [(None, None)] * self.n_v
        self._value = None

    def c_model(self, opp_B: np.ndarray) -> np.ndarray:
        """Hero's expected payoff per hero sequence against a fixed opponent behaviour."""
        r_o = self.tg.realization(self.opp, opp_B)
        return np.asarray(self.A_h @ r_o).ravel()

    def _solve(self, obj_x, obj_v0, extra_ub=None):
        c = np.zeros(self.n_x + self.n_v)
        c[:self.n_x] = -obj_x
        c[self.n_x] = -obj_v0
        A_ub, b_ub = self.A_ub, self.b_ub
        if extra_ub is not None:
            row, rhs = extra_ub
            A_ub = sp.vstack([A_ub, sp.csr_matrix(row)]).tocsr()
            b_ub = np.concatenate([b_ub, [rhs]])
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=self.A_eq, b_eq=self.b_eq,
                      bounds=self.bounds, method="highs")
        if not res.success:
            raise RuntimeError(f"LP failed: {res.message}")
        x = res.x[:self.n_x]
        v0 = res.x[self.n_x]
        return x, v0

    def policy(self, x, fill=None) -> np.ndarray:
        return self.tg.behaviour_from_realization(self.hero, x, fill=fill)

    def game_value(self) -> float:
        if self._value is None:
            x, v0 = self._solve(np.zeros(self.n_x), 1.0)
            self._value = float(v0)
            self._maxmin_x = x
        return self._value

    def maxmin(self, fill=None):
        self.game_value()
        return self.policy(self._maxmin_x, fill)

    def rnr(self, opp_B: np.ndarray, p: float, fill=None):
        x, v0 = self._solve(p * self.c_model(opp_B), 1.0 - p)
        return self.policy(x, fill), float(v0)

    def floor(self, opp_B: np.ndarray, floor: float, fill=None):
        row = np.zeros(self.n_x + self.n_v)
        row[self.n_x] = -1.0                       # -v0 <= -floor
        x, v0 = self._solve(self.c_model(opp_B), 0.0, extra_ub=(row, -floor))
        return self.policy(x, fill), float(v0)


def worst_case(tg: TabularGame, hero: int, B_h: np.ndarray) -> float:
    """Hero's worst-case expected value in its seat (the opponent best-responds)."""
    prof = [None, None]
    prof[hero] = B_h
    prof[1 - hero] = tg.uniform(1 - hero)
    return -tg.best_response(1 - hero, prof)


def seat_exposure(tg: TabularGame, hero: int, B_h: np.ndarray, v_star: float) -> float:
    """v*_seat - worst-case value: how far below the game value a best responder can push
    the hero's current seat strategy (>= 0; 0 for an equilibrium strategy)."""
    return float(v_star - worst_case(tg, hero, B_h))
