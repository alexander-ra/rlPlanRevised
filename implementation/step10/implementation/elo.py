"""
elo.py -- the Elo rating system for the league (raw step 10 L346 [AI-ASSISTED], FTW Math Flag
L187-192: "the Elo matrix IS the meta-game").

WHAT THIS IS
------------
A relative skill measure. Given the pairwise results between agents, Elo assigns each agent a
scalar rating such that the expected score between two agents is a logistic function of their
rating difference:

    E_a = 1 / (1 + 10^((R_b - R_a) / 400))          (expected score of a vs b)
    R_a <- R_a + K * (S_a - E_a)                     (update after observing score S_a)

We drive it from EXACT expected scores (win-probabilities computed from the league's exact
payoff matrix -- see `egta.py`), so the ratings are deterministic given the agents. Elo is the
league's readout of "who is strong against whom", i.e. the empirical-game meta-structure.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. numpy-only.
"""

from __future__ import annotations

import numpy as np

DEFAULT_RATING = 1200.0


def expected_score(rating_a: float, rating_b: float) -> float:
    """Expected score (win prob + half draw prob) of A vs B under the logistic Elo model."""
    return 1.0 / (1.0 + 10.0 ** ((rating_b - rating_a) / 400.0))


def update_pair(rating_a: float, rating_b: float, score_a: float, k: float = 32.0):
    """One Elo update from an observed score `score_a` in [0,1] for A vs B. Zero-sum in rating
    space (B gains what A loses). Returns (new_a, new_b)."""
    ea = expected_score(rating_a, rating_b)
    delta = k * (score_a - ea)
    return rating_a + delta, rating_b - delta


def ratings_from_score_matrix(ids, score_matrix, k: float = 16.0, passes: int = 200,
                              seed: int = 0):
    """Fit Elo ratings to an expected-score matrix.

    `score_matrix[i][j]` = expected score of agent i vs agent j in [0,1] (0.5 = even; must be
    ~antisymmetric: S[i][j] + S[j][i] ~ 1). We sweep all ordered pairs `passes` times in a
    seeded random order, applying the Elo update toward the observed expected score, which
    converges the ratings to a consistent ranking. Returns {id: rating}.
    """
    ids = list(ids)
    n = len(ids)
    S = np.asarray(score_matrix, dtype=float)
    ratings = {a: DEFAULT_RATING for a in ids}
    rng = np.random.default_rng(seed)
    pairs = [(i, j) for i in range(n) for j in range(n) if i != j]
    for _ in range(passes):
        rng.shuffle(pairs)
        for i, j in pairs:
            ra, rb = ratings[ids[i]], ratings[ids[j]]
            na, _nb = update_pair(ra, rb, float(S[i, j]), k=k)
            ratings[ids[i]] = na   # update only i; j is updated when (j,i) is visited
    return ratings


def _selftest():
    print("elo self-test")
    print("-" * 60)
    # Transitive ladder A>B>C: A beats B and C, B beats C. Ratings must order A > B > C.
    ids = ["A", "B", "C"]
    S = np.array([[0.5, 0.75, 0.9],
                  [0.25, 0.5, 0.75],
                  [0.1, 0.25, 0.5]])
    r = ratings_from_score_matrix(ids, S, k=16, passes=300)
    order = sorted(ids, key=lambda a: -r[a])
    print(f"  ratings={ {a: round(v,1) for a,v in r.items()} } -> order={order} "
          f"(PREDICT A > B > C)")
    # RPS (fully cyclic, all pairwise 0.5 by symmetry of the cycle) -> ratings ~ equal.
    Srps = np.array([[0.5, 0.5, 0.5], [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]])
    rr = ratings_from_score_matrix(["R", "P", "S"], Srps, k=16, passes=300)
    spread = max(rr.values()) - min(rr.values())
    print(f"  RPS-even ratings spread={spread:.2f} (PREDICT ~0: no transitive skill to rank)")


if __name__ == "__main__":
    _selftest()
