"""
population.py -- Layer 2: ranking agents from a (meta-)payoff matrix.

Input convention: M is an n x n matrix, M[i, j] = expected payoff per hand of agent i against
agent j, averaged over both seats (antisymmetric for a zero-sum game: M = -M^T).

Methods
-------
elo_fit              Elo ratings fitted by maximum likelihood to pairwise win probabilities
                     (Elo 1978 logistic model, 400-point scale, mean 1500).
session_win_prob     P(agent i ends a K-hand session ahead) from the per-hand mean and SD
                     (normal approximation) -- turns chip results into the win/loss outcomes
                     that Elo needs.
meta_nash            one Nash equilibrium of the symmetric zero-sum meta-game (LP, HiGHS) --
                     the EGTA meta-strategy of Chapters 9-10.
nash_average         Balduzzi et al. (2018): the maximum-entropy Nash equilibrium p* of the
                     meta-game; each agent's Nash-averaged skill is (M p*)_i. Invariant to
                     adding copies of agents.
alpharank            Omidshafiei et al. (2019): stationary distribution of the evolutionary
                     Markov chain over monomorphic populations (single-population form with
                     the local selection model, as OpenSpiel's default), fixation probability
                     rho = (1 - e^{-u}) / (1 - e^{-m u}),  u = alpha (M[r,s] - M[s,r]).
                     alpharank_multipop covers N-player games (one population per seat,
                     Eqs. 4-9 of the paper).
maximal_lottery      VasE (Lanctot et al. 2023): the maximal lottery = the Nash equilibrium of
                     the symmetric zero-sum game given by the pairwise majority MARGIN matrix;
                     iterative_ml ranks by peeling off support levels (OpenSpiel's IML).
transitive_ratio     the Hodge (spinning-top) decomposition from Chapter 10 (step10/spinning_top.py).
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.stats import norm, kendalltau

import deps

_st = deps.spinning_top()


# ---------------------------------------------------------------- Elo
def session_win_prob(mu: np.ndarray, sd: np.ndarray, K: int) -> np.ndarray:
    """P(i ahead after K hands) = Phi(sqrt(K) mu / sd); 0.5 on the diagonal."""
    with np.errstate(divide="ignore", invalid="ignore"):
        z = np.sqrt(K) * mu / np.where(sd > 0, sd, np.inf)
    P = norm.cdf(z)
    np.fill_diagonal(P, 0.5)
    return P


def elo_fit(P: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Ratings r minimising the cross-entropy between P[i,j] and 1/(1+10^((r_j-r_i)/400))."""
    n = P.shape[0]
    if mask is None:
        mask = ~np.eye(n, dtype=bool)
    k = np.log(10) / 400.0

    def loss(r):
        d = k * (r[:, None] - r[None, :])
        q = 1.0 / (1.0 + np.exp(-d))
        q = np.clip(q, 1e-12, 1 - 1e-12)
        L = -(P * np.log(q) + (1 - P) * np.log(1 - q))
        g = (q - P) * k
        grad = (g * mask).sum(axis=1) - (g * mask).sum(axis=0)
        return float((L * mask).sum()), grad

    res = minimize(loss, np.zeros(n), jac=True, method="L-BFGS-B")
    r = res.x - res.x.mean() + 1500.0
    return r


# ---------------------------------------------------------------- Nash of the meta-game
def meta_nash(M: np.ndarray) -> np.ndarray:
    """A maximin mixture of the symmetric zero-sum game M (LP)."""
    n = M.shape[0]
    c = np.zeros(n + 1); c[-1] = -1.0
    A_ub = np.hstack([-M.T, np.ones((n, 1))])          # v - sum_i p_i M[i,j] <= 0
    res = linprog(c, A_ub=A_ub, b_ub=np.zeros(n),
                  A_eq=np.hstack([np.ones((1, n)), [[0.0]]]), b_eq=[1.0],
                  bounds=[(0, None)] * n + [(None, None)], method="highs")
    p = np.maximum(res.x[:n], 0)
    return p / p.sum()


def game_value(M: np.ndarray, p: np.ndarray) -> float:
    return float((p @ M).min())


def nash_support_candidates(M: np.ndarray, eps: float) -> np.ndarray:
    """Agents that carry positive mass in SOME eps-Nash equilibrium (one LP per agent)."""
    n = M.shape[0]
    v = game_value(M, meta_nash(M))
    A_ub = -M.T                                     # -(M^T p) <= -(v - eps)
    b_ub = -(v - eps) * np.ones(n)
    keep = []
    for i in range(n):
        c = np.zeros(n); c[i] = -1.0
        res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=np.ones((1, n)), b_eq=[1.0],
                      bounds=[(0, None)] * n, method="highs")
        if res.success and -res.fun > 1e-4:
            keep.append(i)
    return np.asarray(keep, dtype=int)


def nash_average(M: np.ndarray, tol: float = 1e-6):
    """Balduzzi et al. (2018) Nash averaging: max-entropy Nash p*, skills M p*.

    The Nash set {p : M^T p >= v} is taken with a fixed numerical tolerance tol * max|M|
    (1e-6 relative), identical for every call. The entropy maximisation is solved on the
    agents that can carry mass in some equilibrium (found by one LP each), which keeps the
    convex program well conditioned when several agents are near-tied."""
    import cvxpy as cp
    n = M.shape[0]
    scale = max(1.0, float(np.abs(M).max()))
    eps = tol * scale
    v = game_value(M, meta_nash(M))
    S = nash_support_candidates(M, eps)
    ps = None
    if len(S) == 1:
        ps = np.zeros(n); ps[S[0]] = 1.0
    elif len(S) > 1:
        A = M[S].T
        feasible = lambda x: x is not None and (A @ x).min() >= v - 10 * eps and abs(x.sum() - 1) < 1e-6
        q = cp.Variable(len(S), nonneg=True)
        prob = cp.Problem(cp.Maximize(cp.sum(cp.entr(q))), [cp.sum(q) == 1, A @ q >= v - eps])
        cand = []
        try:
            prob.solve(solver=cp.CLARABEL)
            if prob.status == "optimal":
                cand.append(np.maximum(np.asarray(q.value).ravel(), 0))
        except Exception:
            pass
        r = minimize(lambda x: float(np.sum(x * np.log(np.maximum(x, 1e-300)))),
                     np.ones(len(S)) / len(S), method="SLSQP", bounds=[(0, 1)] * len(S),
                     constraints=[{"type": "eq", "fun": lambda x: x.sum() - 1},
                                  {"type": "ineq", "fun": lambda x: A @ x - (v - eps)}],
                     options={"ftol": 1e-14, "maxiter": 2000})
        cand.append(np.maximum(r.x, 0))
        cand = [x for x in cand if feasible(x)]
        if cand:     # keep the feasible candidate with the largest entropy
            ent = [float(-np.sum(x[x > 0] * np.log(x[x > 0]))) for x in cand]
            ps = np.zeros(n); ps[S] = cand[int(np.argmax(ent))]
    if ps is None:           # fall back to the LP equilibrium (not max-entropy)
        ps = meta_nash(M)
    ps = ps / ps.sum()
    return ps, M @ ps


# ---------------------------------------------------------------- alpha-rank
def _rho(u: np.ndarray, m: int) -> np.ndarray:
    out = np.full_like(u, 1.0 / m, dtype=float)
    nz = ~np.isclose(u, 0.0, atol=1e-14)
    un = u[nz]
    # numerically stable (1 - e^{-u}) / (1 - e^{-m u})
    with np.errstate(over="ignore", invalid="ignore"):
        num = -np.expm1(-un)
        den = -np.expm1(-m * un)
        val = num / den
        # large negative u: ratio -> e^{(m-1)u}  (tiny); large positive u: -> 1 - e^{-u}
        bad = ~np.isfinite(val)
        val[bad] = np.where(un[bad] < 0, np.exp((m - 1) * un[bad]), 1.0)
    out[nz] = val
    return out


def _stationary(C: np.ndarray) -> np.ndarray:
    n = C.shape[0]
    A = np.vstack([C.T - np.eye(n), np.ones((1, n))])
    b = np.zeros(n + 1); b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(A, b, rcond=None)
    pi = np.maximum(pi, 0)
    return pi / pi.sum()


def alpharank(M: np.ndarray, alpha: float, m: int = 50) -> np.ndarray:
    """Single-population alpha-Rank with the local selection model (symmetric 2-player)."""
    n = M.shape[0]
    U = alpha * (M - M.T)                   # U[r, s] = alpha (M[r,s] - M[s,r])
    R = _rho(U, m)                          # R[r, s] = fixation prob of mutant r in s-population
    C = np.zeros((n, n))
    eta = 1.0 / (n - 1)
    for s in range(n):
        for r in range(n):
            if r != s:
                C[s, r] = eta * R[r, s]
        C[s, s] = 1.0 - C[s].sum()
    return _stationary(C)


def alpharank_multipop(tables: list, alpha: float, m: int = 50) -> np.ndarray:
    """Multi-population alpha-Rank (one population per seat), Omidshafiei et al. Eqs. 4-9.
    tables[k] is an array of shape (n_1, ..., n_K) with population k's payoff per profile.
    Returns the stationary distribution over profiles (C-order flattening)."""
    shape = tables[0].shape
    K = len(shape)
    profiles = list(np.ndindex(*shape))
    idx = {p: i for i, p in enumerate(profiles)}
    N = len(profiles)
    eta = 1.0 / sum(n - 1 for n in shape)
    C = np.zeros((N, N))
    for i, s in enumerate(profiles):
        for k in range(K):
            f_res = tables[k][s]
            for tau in range(shape[k]):
                if tau == s[k]:
                    continue
                t = list(s); t[k] = tau; t = tuple(t)
                u = alpha * (tables[k][t] - f_res)
                C[i, idx[t]] = eta * _rho(np.array([u]), m)[0]
        C[i, i] = 1.0 - C[i].sum()
    return _stationary(C)


# ---------------------------------------------------------------- VasE
def maximal_lottery(margin: np.ndarray) -> np.ndarray:
    """Maximal lottery = maximin mixture of the (antisymmetric) margin game."""
    return meta_nash(margin)


def iterative_ml(margin: np.ndarray, zero_tol: float = 1e-6) -> list:
    """Iterative maximal lotteries: rank levels (list of lists of indices, best first)."""
    remaining = list(range(margin.shape[0]))
    levels = []
    while remaining:
        sub = margin[np.ix_(remaining, remaining)]
        if len(remaining) == 1:
            levels.append(remaining[:]); break
        p = maximal_lottery(sub)
        win = [remaining[i] for i in np.argsort(-p) if p[i] > zero_tol]
        levels.append(win)
        remaining = [r for r in remaining if r not in win]
    return levels


def iml_rank(margin: np.ndarray) -> np.ndarray:
    """Rank position (0 = best) per agent from the IML levels (ties share a level)."""
    ranks = np.zeros(margin.shape[0])
    pos = 0
    for lvl in iterative_ml(margin):
        for i in lvl:
            ranks[i] = pos
        pos += len(lvl)
    return ranks


# ---------------------------------------------------------------- spinning top
def transitive_ratio(M: np.ndarray) -> float:
    return float(_st.transitive_ratio(M, "hodge"))


def hodge_ratings(M: np.ndarray) -> np.ndarray:
    return _st.hodge_ratings(_st.antisymmetrize(M))


# ---------------------------------------------------------------- helpers
def ranks_from_scores(s: np.ndarray) -> np.ndarray:
    """0 = best; ties broken by order."""
    order = np.argsort(-np.asarray(s), kind="stable")
    r = np.empty(len(s), dtype=int)
    r[order] = np.arange(len(s))
    return r


def tau(a, b) -> float:
    return float(kendalltau(a, b).statistic)
