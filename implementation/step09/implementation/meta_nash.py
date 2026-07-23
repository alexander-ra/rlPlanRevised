"""
meta_nash.py -- normal-form (meta-)game solvers for PSRO's meta-strategy step.

WHAT THIS IS
------------
PSRO's inner "meta-strategy solver" (MSS): given the empirical payoff matrix between the two
players' policy populations, return a meta-Nash mixture over each population (raw step
L281, L400-405; Lanctot Alg 1).

Two solvers, picked automatically:
  - ZERO-SUM  -> linear program via scipy HiGHS (exact), with a numpy fictitious-play
                 fallback if scipy is absent. All poker meta-games (Kuhn/Leduc/Goofspiel)
                 are zero-sum, so this is the load-bearing path.
  - GENERAL-SUM -> fictitious play (a heuristic; converges for zero-sum and many potential
                 games, NOT guaranteed for arbitrary general-sum -- flagged).

Also exposes `nashconv_matrix` for a matrix profile so callers can measure meta-game
exploitability without re-deriving it.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

_HAS_SCIPY = None


def _scipy_ok() -> bool:
    global _HAS_SCIPY
    if _HAS_SCIPY is None:
        try:
            import scipy  # noqa: F401
            _HAS_SCIPY = True
        except ImportError:
            _HAS_SCIPY = False
    return _HAS_SCIPY


# --- zero-sum via LP (row maximizer) ------------------------------------------------
def solve_zero_sum_lp(M):
    """Nash of a zero-sum matrix game (row payoff `M`, col payoff -M) via LP (HiGHS).

    Returns (row_mix, col_mix, game_value). Uses the standard maximin LP:
        max v  s.t.  sum_i x_i M[i,j] >= v for all j,  sum_i x_i = 1,  x >= 0.
    The column mixture is read from the dual (equivalently, solve the transposed LP).
    """
    from scipy.optimize import linprog

    M = np.asarray(M, dtype=float)
    n_row, n_col = M.shape
    shift = float(M.min())  # shift to keep the value positive (LP convenience); undone below
    Mp = M - shift + 1.0

    # variables: [x_0..x_{n_row-1}, v]; maximize v -> minimize -v
    c = np.zeros(n_row + 1)
    c[-1] = -1.0
    # constraints: for each col j:  v - sum_i x_i Mp[i,j] <= 0
    A_ub = np.zeros((n_col, n_row + 1))
    for j in range(n_col):
        A_ub[j, :n_row] = -Mp[:, j]
        A_ub[j, -1] = 1.0
    b_ub = np.zeros(n_col)
    A_eq = np.zeros((1, n_row + 1))
    A_eq[0, :n_row] = 1.0
    b_eq = np.array([1.0])
    bounds = [(0.0, None)] * n_row + [(None, None)]

    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"zero-sum LP failed: {res.message}")
    x = np.clip(res.x[:n_row], 0.0, None)
    x = x / x.sum()

    # column mixture: solve the transposed game (col is the maximizer of -M^T)
    y = _col_mix_lp(Mp)
    value = float(x @ M @ y)
    return x, y, value


def _col_mix_lp(Mp):
    from scipy.optimize import linprog

    n_row, n_col = Mp.shape
    # col minimizes row's payoff: min w s.t. sum_j y_j Mp[i,j] <= w for all i
    c = np.zeros(n_col + 1)
    c[-1] = 1.0
    A_ub = np.zeros((n_row, n_col + 1))
    for i in range(n_row):
        A_ub[i, :n_col] = Mp[i, :]
        A_ub[i, -1] = -1.0
    b_ub = np.zeros(n_row)
    A_eq = np.zeros((1, n_col + 1))
    A_eq[0, :n_col] = 1.0
    b_eq = np.array([1.0])
    bounds = [(0.0, None)] * n_col + [(None, None)]
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"zero-sum LP (col) failed: {res.message}")
    y = np.clip(res.x[:n_col], 0.0, None)
    return y / y.sum()


# --- zero-sum fictitious-play fallback (numpy-only) ---------------------------------
def fictitious_play(M, iters: int = 10000):
    """Fictitious play on a zero-sum matrix (row payoff `M`). Returns (row_mix, col_mix, value)."""
    M = np.asarray(M, dtype=float)
    n_row, n_col = M.shape
    rc = np.zeros(n_row)
    cc = np.zeros(n_col)
    rc[0] += 1.0
    cc[0] += 1.0
    for _ in range(iters):
        col_mix = cc / cc.sum()
        rc[int(np.argmax(M @ col_mix))] += 1.0
        row_mix = rc / rc.sum()
        cc[int(np.argmin(row_mix @ M))] += 1.0
    row_mix = rc / rc.sum()
    col_mix = cc / cc.sum()
    return row_mix, col_mix, float(row_mix @ M @ col_mix)


# --- general-sum fictitious play (heuristic) ----------------------------------------
def fictitious_play_general(A, B, iters: int = 10000):
    """Fictitious play for a 2-player general-sum game (row payoff A, col payoff B).

    Each player best-responds to the empirical frequency of the other. Converges for
    zero-sum and (many) potential games; NOT guaranteed for arbitrary general-sum games --
    treat the result as an approximate equilibrium and check `nashconv_matrix`.
    """
    A = np.asarray(A, dtype=float)
    B = np.asarray(B, dtype=float)
    n0, n1 = A.shape
    c0 = np.zeros(n0)
    c1 = np.zeros(n1)
    c0[0] += 1.0
    c1[0] += 1.0
    for _ in range(iters):
        y = c1 / c1.sum()
        c0[int(np.argmax(A @ y))] += 1.0
        x = c0 / c0.sum()
        c1[int(np.argmax(x @ B))] += 1.0
    return c0 / c0.sum(), c1 / c1.sum()


def nashconv_matrix(A, x, y, B=None) -> float:
    """NashConv of a matrix profile. If B is None the game is treated as zero-sum (B=-A)."""
    A = np.asarray(A, dtype=float)
    B = -A if B is None else np.asarray(B, dtype=float)
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    u0 = float(x @ A @ y)
    u1 = float(x @ B @ y)
    br0 = float(np.max(A @ y))
    br1 = float(np.max(x @ B))
    return (br0 - u0) + (br1 - u1)


def solve_meta_nash(payoff_row, payoff_col=None, fp_iters: int = 10000):
    """Dispatch: zero-sum -> LP (or FP fallback); general-sum -> general FP.

    `payoff_row` is player 0's payoff matrix over (population0 x population1). If
    `payoff_col` is None or equals -payoff_row, the meta-game is zero-sum.
    Returns (row_mix, col_mix).
    """
    A = np.asarray(payoff_row, dtype=float)
    zero_sum = payoff_col is None or np.allclose(A + np.asarray(payoff_col, float), 0.0)
    if zero_sum:
        if _scipy_ok():
            try:
                x, y, _ = solve_zero_sum_lp(A)
                return x, y
            except Exception:  # noqa: BLE001 - fall back to FP if the LP degenerates
                pass
        x, y, _ = fictitious_play(A, fp_iters)
        return x, y
    return fictitious_play_general(A, payoff_col, fp_iters)


def _selftest():
    print("meta_nash self-test")
    print("-" * 60)
    # Rock-Paper-Scissors: Nash is uniform, value 0.
    rps = np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)
    x, y = solve_meta_nash(rps)
    print(f"[RPS] row_mix={np.round(x,3).tolist()} col_mix={np.round(y,3).tolist()} "
          f"(expect ~uniform) NashConv={nashconv_matrix(rps, x, y):.4f} (expect ~0)")
    xf, yf, vf = fictitious_play(rps, 20000)
    print(f"[RPS-FP] row_mix={np.round(xf,3).tolist()} value={vf:+.4f} (expect ~0)")


if __name__ == "__main__":
    _selftest()
