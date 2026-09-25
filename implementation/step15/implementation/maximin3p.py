"""
maximin3p.py -- the maximin (team-maxmin) value of each seat of three-player Kuhn poker.

    python maximin3p.py            -> results/maximin3p.json

Ganzfried & Sandholm (2015, Sec. 2.3) note that their safe-exploitation methodology "applies
straightforwardly" to multiplayer games if the minimax value is replaced by the maximin value:
the most a player can guarantee against every strategy of the others. When the others may
coordinate (correlate their play, as colluders do), that value is the team-maxmin value with
ex-ante coordination (Celli & Gatti 2018; Zhang, An & Cerny 2021; Zhang, Farina & Sandholm 2023):

    v_mm(i) = max_{sigma_i} min_{joint y of the other two} u_i(sigma_i, y).

The inner minimum of a linear function over correlated joint strategies is attained at a pure
pair, so it is computed exactly by Chapter 14's enumeration (2^16 pure strategies of one
opponent, best response of the other). The outer maximisation is a sequence-form LP solved by
constraint generation: max v s.t. v <= u_i(x, pair) for every pair generated so far, x in
seat i's treeplex; the oracle adds the pair that minimises u_i(x, .) until it cannot push the
value below v. This is the conservative N-player floor the gap analysis calls "very
conservative"; it is computed here only as a reference line for the pilot of Experiment 2.1.
"""

from __future__ import annotations

import json
import os
import time

import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

import boot
import trees
import solvers
from nplayer import br_batch
from bounded3p import Probe3
from log15 import Logger


def pair_coeffs(tg, i, rj, rk):
    """c[s] = sum over terminals with seq_i = s of chance * u_i * r_j * r_k (u_i = c . x)."""
    j, k = [q for q in range(3) if q != i]
    w = tg.term_chance * tg.term_util[:, i] * rj[tg.term_seq[:, j]] * rk[tg.term_seq[:, k]]
    return np.bincount(tg.term_seq[:, i], weights=w, minlength=tg.players[i].n_seq)


def oracle(tg, pr, i, x):
    """The coordinated pair (pure) that minimises u_i(x, .); returns (value, r_j, r_k)."""
    j, k = [q for q in range(3) if q != i]
    base = tg.term_chance * x[tg.term_seq[:, i]] * tg.term_util[:, i]
    Rj = pr.pure(j)
    best, best_m = np.inf, 0
    for s in range(0, len(Rj), 8192):
        W = Rj[s:s + 8192][:, tg.term_seq[:, j]] * base[None]
        v = -br_batch(tg, k, -(W @ pr.onehot[k]))
        m = int(v.argmin())
        if v[m] < best:
            best, best_m = float(v[m]), s + m
    rj = Rj[best_m]
    w = rj[tg.term_seq[:, j]] * base * -1.0
    cv = np.bincount(tg.term_seq[:, k], weights=w, minlength=tg.players[k].n_seq)
    _, Bk = tg._br_backward(k, cv, True)
    rk = tg.realization(k, Bk)
    return best, rj, rk


def maximin(tg, pr, i, init_B, max_iter=500, tol=1e-9, log=None):
    F, f = tg.treeplex_matrix(i)
    n = tg.players[i].n_seq
    x = tg.realization(i, init_B)
    cuts = []
    history = []
    for it in range(max_iter):
        val, rj, rk = oracle(tg, pr, i, x)
        cuts.append(pair_coeffs(tg, i, rj, rk))
        # LP over [x, v]: max v  s.t.  v - c.x <= 0 for each cut, F x = f, x >= 0
        C = np.asarray(cuts)
        A_ub = sp.hstack([sp.csr_matrix(-C), sp.csr_matrix(np.ones((len(cuts), 1)))]).tocsr()
        A_eq = sp.hstack([F, sp.csr_matrix((F.shape[0], 1))]).tocsr()
        c = np.zeros(n + 1); c[-1] = -1.0
        res = linprog(c, A_ub=A_ub, b_ub=np.zeros(len(cuts)), A_eq=A_eq, b_eq=f,
                      bounds=[(0, None)] * n + [(None, None)], method="highs")
        if not res.success:
            raise RuntimeError(res.message)
        x, v_up = res.x[:n], float(res.x[-1])
        history.append({"iter": it, "oracle_value_of_previous_x": val, "lp_upper_bound": v_up})
        if log and it % 10 == 0:
            log(f"  seat {i} it {it}: upper {v_up:.6f}, last oracle {val:.6f}")
        if val >= v_up - tol:
            break
    val, _, _ = oracle(tg, pr, i, x)
    return {"value": float(val), "upper_bound": float(v_up), "iterations": len(history),
            "gap": float(v_up - val), "strategy": tg.behaviour_from_realization(i, x).tolist(),
            "history": history}


def main():
    log = Logger("maximin3p")
    t0 = time.time()
    tg = trees.load("kuhn3")
    bp = solvers.cfr_profile(tg, 100000, algo="cfrplus")
    pr = Probe3(tg)
    out = {"game": "kuhn_poker(players=3)", "seats": {}}
    for i in range(3):
        r = maximin(tg, pr, i, bp[i], log=log)
        r["blueprint_coalition_value"] = pr.coalition_value(i, bp[i])
        r["blueprint_value"] = float(tg.values(bp)[i])
        out["seats"][str(i)] = r
        log(f"seat {i}: maximin value {r['value']:+.5f} (LP upper {r['upper_bound']:+.5f}, "
            f"{r['iterations']} cuts); blueprint value {r['blueprint_value']:+.5f}, "
            f"blueprint coalition value {r['blueprint_coalition_value']:+.5f}")
    vals = [out["seats"][str(i)]["value"] for i in range(3)]
    out["seat_average_maximin"] = float(np.mean(vals))
    out["equal_share"] = 0.0
    out["runtime_seconds"] = time.time() - t0
    with open(os.path.join(boot.RESULTS_DIR, "maximin3p.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    log(f"seat-average maximin {out['seat_average_maximin']:+.5f}; done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
