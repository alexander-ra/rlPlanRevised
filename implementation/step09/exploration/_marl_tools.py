"""
Shared tools for the Step 09 exploration scripts.

Pure-numpy building blocks reused across the matrix-game / non-stationarity / PSRO-peek /
LOLA scripts:

  - GAMES                : the four canonical 2x2 matrix games (payoffs + analytic Nash).
  - expected_payoffs     : exact expected reward of a mixed profile in a 2x2 game.
  - IGA learners         : infinitesimal-gradient-ascent (naive policy-gradient) dynamics --
                           the "independent learners" baseline the raw step calls for
                           (L118-121, L365-378). Exact gradients, so the dynamics are
                           deterministic and the cycling/convergence is crisp.
  - matrix meta-Nash     : fictitious play on a payoff matrix (numpy-only) -- used by the
                           PSRO peek so we do not need scipy here.
  - save_json / maybe_plot : artifact helpers (matplotlib guarded).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Every "expected"
number in the scripts' output is a PREDICTION to verify on a real run.
"""

from __future__ import annotations

import json
import os

import numpy as np

# --- The four canonical matrix games ------------------------------------------------
# Convention: A[i][j] = row-player reward, B[i][j] = col-player reward, action 0 listed first.
GAMES = {
    "prisoners_dilemma": {
        "A": [[3.0, 0.0], [5.0, 1.0]],
        "B": [[3.0, 5.0], [0.0, 1.0]],
        "actions": ["Cooperate", "Defect"],
        "nash": "Unique pure NE (Defect, Defect) = (1, 1); Defect strictly dominates. "
                "Naive learners converge here even though (C,C)=(3,3) is better for both.",
        "predict": "Both action-0 (Cooperate) probabilities -> 0 (mutual defection).",
    },
    "matching_pennies": {
        "A": [[1.0, -1.0], [-1.0, 1.0]],
        "B": [[-1.0, 1.0], [1.0, -1.0]],
        "actions": ["Heads", "Tails"],
        "nash": "Unique NE is mixed 50/50; zero-sum. The mixed NE is a SADDLE, so naive "
                "gradient learners orbit it rather than converge (Singh-Kearns-Mansour 2000).",
        "predict": "p and q ORBIT (0.5, 0.5) in a closed loop; neither settles.",
    },
    "stag_hunt": {
        "A": [[4.0, 0.0], [3.0, 3.0]],
        "B": [[4.0, 3.0], [0.0, 3.0]],
        "actions": ["Stag", "Hare"],
        "nash": "Two pure NE: (Stag,Stag)=(4,4) is payoff-dominant; (Hare,Hare)=(3,3) is "
                "risk-dominant (safe). Plus a mixed NE. Which one learners reach depends on "
                "initialization (basin of attraction).",
        "predict": "From optimistic init -> (Stag,Stag); from pessimistic init -> (Hare,Hare).",
    },
    "battle_of_the_sexes": {
        "A": [[2.0, 0.0], [0.0, 1.0]],
        "B": [[1.0, 0.0], [0.0, 2.0]],
        "actions": ["Opera", "Football"],
        "nash": "Two pure NE (Opera,Opera)=(2,1) and (Football,Football)=(1,2) + one mixed. "
                "A coordination / equilibrium-SELECTION problem: both prefer to agree, but on "
                "different options.",
        "predict": "Learners lock onto ONE of the two pure NE (which one depends on init), or "
                   "cycle near the inefficient mixed NE.",
    },
}


def game_matrices(name: str):
    g = GAMES[name]
    return np.array(g["A"], dtype=float), np.array(g["B"], dtype=float)


# --- exact expected payoffs of a 2x2 mixed profile ----------------------------------
def expected_payoffs(A, B, p: float, q: float):
    """Expected (row, col) reward when row plays action 0 w.p. p and col action 0 w.p. q."""
    pr = np.array([p, 1.0 - p])
    pc = np.array([q, 1.0 - q])
    return float(pr @ A @ pc), float(pr @ B @ pc)


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


def _grad_row_logit(A, p: float, q: float) -> float:
    """d(row expected reward)/d(theta_row), with p = sigmoid(theta_row)."""
    pc = np.array([q, 1.0 - q])
    dR_dp = float(A[0] @ pc - A[1] @ pc)  # value of raising P(action 0)
    return dR_dp * p * (1.0 - p)


def _grad_col_logit(B, p: float, q: float) -> float:
    """d(col expected reward)/d(theta_col), with q = sigmoid(theta_col)."""
    pr = np.array([p, 1.0 - p])
    dR_dq = float(pr @ B[:, 0] - pr @ B[:, 1])
    return dR_dq * q * (1.0 - q)


def run_independent_learners(name: str, steps: int = 4000, lr: float = 0.1,
                             init=(0.5, 0.5), seed: int = 0):
    """Two INDEPENDENT gradient learners (naive IGA) on a 2x2 game.

    Each learner ascends its OWN expected reward, treating the opponent's CURRENT policy as
    a fixed environment -- the textbook independent-learning setup whose blind spot is that
    the opponent is *also* moving (non-stationarity). Returns the (p, q) trajectory.
    """
    rng = np.random.default_rng(seed)  # only used to jitter the init reproducibly
    A, B = game_matrices(name)
    # logits from the requested init probabilities, with a tiny reproducible jitter so
    # symmetric games do not sit exactly on an unstable ridge.
    p0 = float(np.clip(init[0] + 0.01 * (rng.random() - 0.5), 1e-3, 1 - 1e-3))
    q0 = float(np.clip(init[1] + 0.01 * (rng.random() - 0.5), 1e-3, 1 - 1e-3))
    tr = np.log(p0 / (1 - p0))
    tc = np.log(q0 / (1 - q0))

    ps = np.empty(steps + 1)
    qs = np.empty(steps + 1)
    p, q = _sigmoid(tr), _sigmoid(tc)
    ps[0], qs[0] = p, q
    for t in range(1, steps + 1):
        gr = _grad_row_logit(A, p, q)
        gc = _grad_col_logit(B, p, q)
        # simultaneous update: both use the OTHER's policy from BEFORE this step.
        tr += lr * gr
        tc += lr * gc
        p, q = _sigmoid(tr), _sigmoid(tc)
        ps[t], qs[t] = p, q
    return ps, qs


# --- matrix meta-Nash via fictitious play (numpy-only; used by the PSRO peek) --------
def fictitious_play_matrix(payoff_row, iters: int = 5000):
    """Fictitious play on a 2-player ZERO-SUM matrix `payoff_row` (row's payoff = -col's).

    Returns (row_mixture, col_mixture, value_estimate). Converges to a Nash of the matrix
    for zero-sum games (Robinson 1951). We only use it on the PSRO meta-game, which is
    zero-sum whenever the underlying game is.
    """
    M = np.array(payoff_row, dtype=float)
    n_row, n_col = M.shape
    row_count = np.zeros(n_row)
    col_count = np.zeros(n_col)
    # seed with one arbitrary action each
    row_count[0] += 1
    col_count[0] += 1
    for _ in range(iters):
        col_mix = col_count / col_count.sum()
        best_row = int(np.argmax(M @ col_mix))
        row_count[best_row] += 1
        row_mix = row_count / row_count.sum()
        best_col = int(np.argmin(row_mix @ M))
        col_count[best_col] += 1
    row_mix = row_count / row_count.sum()
    col_mix = col_count / col_count.sum()
    value = float(row_mix @ M @ col_mix)
    return row_mix, col_mix, value


# --- artifact helpers ---------------------------------------------------------------
def figures_dir() -> str:
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
    os.makedirs(d, exist_ok=True)
    return d


def save_json(name: str, payload: dict) -> str:
    path = os.path.join(figures_dir(), name)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    return path


def get_plt():
    """Return a headless matplotlib.pyplot, or None if matplotlib is not installed."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        return plt
    except Exception:  # noqa: BLE001 - matplotlib is optional here
        return None
