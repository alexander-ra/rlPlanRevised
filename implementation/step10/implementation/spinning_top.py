"""
spinning_top.py -- transitive + cyclic decomposition of a payoff matrix
(raw step 10 L233-267, L383-405; Balduzzi et al. 2019, "Open-Ended Learning in Symmetric
Zero-Sum Games"; Math Flag L325).

WHAT THIS IS
------------
The 🔴 HAND-CODE analytical tool that answers "is my population's competitive structure REAL
SKILL (a total ranking A > B > C) or ROCK-PAPER-SCISSORS CYCLING (A > B > C > A)?". Every
antisymmetric payoff matrix splits as

        A_anti = T (transitive)  +  C (cyclic)

and the transitive ratio  ||T|| / ||A_anti||  says how much of the game is "real skill". A
ratio near 1 -> self-play / naive PBT converge to a good strategy; a ratio near 0 (pure RPS)
-> improvement is illusory and you need population DIVERSITY (the whole point of the league).

⚠ IMPORTANT CORRECTNESS NOTE (a Math Flag to verify -- WORKFLOW 0.1)
--------------------------------------------------------------------
The raw step (L383-398) sketches a decomposition that takes the TRANSITIVE part as the
rank-1 truncated SVD of A_anti (`T = s1 u1 v1^T`). That sketch does NOT satisfy the step's own
validation target "RPS should be 100% cyclic (zero transitive component)" (Validation L487):
a real antisymmetric matrix has singular values in EQUAL PAIRS (s, s, 0, ...), so its rank-1
SVD keeps HALF the Frobenius mass -- for 3x3 RPS the rank-1 SVD ratio is 1/sqrt(2) ~= 0.707,
not 0. The decomposition that actually gives "RPS = 100% cyclic" is the COMBINATORIAL HODGE
decomposition (a.k.a. HodgeRank; Jiang-Lim-Yao-Ye 2011), which Balduzzi's notion of
"game-theoretic strength" (their Section 3.2) is built on: define a skill rating per player as
its mean payoff, and let the transitive part be the rating DIFFERENCES.

    rating   r_i   = (1/n) * sum_j A_anti[i,j]          (mean margin of player i)
    transitive     T[i,j] = r_i - r_j                    (a gradient flow / total order)
    cyclic         C      = A_anti - T                    (the divergence-free remainder)

For RPS every row of A_anti sums to 0 -> all ratings 0 -> T = 0 -> transitive_ratio = 0 (100%
cyclic), matching the validation target. So `spinning_top_decomposition` (the one used by
`validate.py`) is the HODGE version; the raw-step SVD sketch is provided as
`svd_rank1_decomposition` with this caveat so the reader can compare and verify.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

import numpy as np


def antisymmetrize(A) -> np.ndarray:
    """A_anti = (A - A.T) / 2. For a zero-sum win-margin matrix this is A itself; for a
    general payoff/win-rate matrix it extracts the competitive (antisymmetric) part."""
    A = np.asarray(A, dtype=float)
    return (A - A.T) / 2.0


def hodge_ratings(A_anti) -> np.ndarray:
    """Skill ratings = the mean margin of each player (Balduzzi Sec 3.2 / HodgeRank)."""
    A_anti = np.asarray(A_anti, dtype=float)
    n = A_anti.shape[0]
    return A_anti.sum(axis=1) / n


def spinning_top_decomposition(payoff_matrix):
    """Combinatorial-Hodge transitive + cyclic decomposition of a payoff matrix.

    Returns (T, C, A_anti) with A_anti = T + C, where
        T[i,j] = r_i - r_j   (transitive: a total skill ordering / gradient flow),
        C      = A_anti - T   (cyclic: the rock-paper-scissors remainder).
    This is the decomposition used by the step's validation (RPS -> 100% cyclic).
    """
    A_anti = antisymmetrize(payoff_matrix)
    r = hodge_ratings(A_anti)
    T = r[:, None] - r[None, :]          # T[i,j] = r_i - r_j
    C = A_anti - T
    return T, C, A_anti


def svd_rank1_decomposition(payoff_matrix):
    """The raw-step SVD sketch (L389-398): transitive = rank-1 truncated SVD of A_anti.

    ⚠ Kept ONLY for comparison. Because A_anti is antisymmetric its singular values pair up,
    so this OVERSTATES the transitive part (RPS -> ratio ~0.707, not 0). Prefer
    `spinning_top_decomposition`. Returns (T, C, A_anti).
    """
    A_anti = antisymmetrize(payoff_matrix)
    U, S, Vt = np.linalg.svd(A_anti)
    T = S[0] * np.outer(U[:, 0], Vt[0, :])
    C = A_anti - T
    return T, C, A_anti


def _fro(M) -> float:
    return float(np.linalg.norm(np.asarray(M, dtype=float), ord="fro"))


def transitive_ratio(payoff_matrix, method: str = "hodge") -> float:
    """||T|| / ||A_anti|| in [0, 1]. 1 -> pure skill/transitive; 0 -> pure cyclic (RPS).

    method="hodge" (default, correct) or "svd" (the raw-step sketch, for comparison).
    """
    if method == "svd":
        T, _C, A_anti = svd_rank1_decomposition(payoff_matrix)
    else:
        T, _C, A_anti = spinning_top_decomposition(payoff_matrix)
    denom = _fro(A_anti)
    if denom < 1e-12:
        return 0.0
    return _fro(T) / denom


def cyclic_ratio(payoff_matrix, method: str = "hodge") -> float:
    """||C|| / ||A_anti||. Reported alongside the transitive ratio (they need not sum to 1
    because T and C are Frobenius-orthogonal only for the Hodge decomposition, where
    ratio_T^2 + ratio_C^2 = 1)."""
    if method == "svd":
        T, C, A_anti = svd_rank1_decomposition(payoff_matrix)
    else:
        T, C, A_anti = spinning_top_decomposition(payoff_matrix)
    denom = _fro(A_anti)
    if denom < 1e-12:
        return 0.0
    return _fro(C) / denom


def pure_skill_game(n: int = 4) -> np.ndarray:
    """A perfectly transitive test matrix: A[i,j] = i - j (a total skill order). Its
    transitive_ratio must be 1.0 (pure skill, zero cycling)."""
    idx = np.arange(n, dtype=float)
    return idx[:, None] - idx[None, :]


def _selftest():
    print("spinning_top self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)

    # Rock-Paper-Scissors: PREDICT 100% cyclic (transitive ratio ~ 0) with the Hodge split.
    rps = np.array([[0.0, -1.0, 1.0], [1.0, 0.0, -1.0], [-1.0, 1.0, 0.0]])
    tr_h = transitive_ratio(rps, "hodge")
    tr_s = transitive_ratio(rps, "svd")
    print(f"[RPS]  Hodge transitive_ratio={tr_h:.4f} (PREDICT ~0.0), "
          f"cyclic_ratio={cyclic_ratio(rps):.4f} (PREDICT ~1.0)")
    print(f"[RPS]  raw-step SVD transitive_ratio={tr_s:.4f} "
          f"(PREDICT ~0.707 -- WHY we do NOT use SVD; see module docstring)")

    # Pure-skill game: PREDICT 100% transitive (ratio ~ 1).
    skill = pure_skill_game(4)
    print(f"[skill] Hodge transitive_ratio={transitive_ratio(skill):.4f} (PREDICT ~1.0), "
          f"cyclic_ratio={cyclic_ratio(skill):.4f} (PREDICT ~0.0)")

    # Reconstruction check: T + C == A_anti exactly.
    T, C, A_anti = spinning_top_decomposition(rps)
    err = float(np.max(np.abs((T + C) - A_anti)))
    print(f"[recon] max|T+C - A_anti| = {err:.2e} (must be ~0)")


if __name__ == "__main__":
    _selftest()
