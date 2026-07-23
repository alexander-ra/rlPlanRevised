"""
egta.py -- Empirical Game-Theoretic Analysis of a policy population (raw step 10 L269-297,
L441-463; Tuyls/Perolat/Lanctot et al. 2018; Math Flag L327). Thesis Contribution #3's
prototype: the multi-agent generalisation of exploitability.

WHAT THIS IS
------------
Given a finite set of policies (the league's agents + frozen snapshots), we:

  1. build the EMPIRICAL (meta) GAME -- the normal-form payoff matrix between the policies,
     computed EXACTLY on the Leduc tree (no Monte-Carlo noise; the policies are the tabular
     extractions of the trained nets, so the whole meta-game is ground truth);
  2. solve its META-NASH mixture (reusing Step 09's zero-sum LP `solve_meta_nash`);
  3. measure the META-NASH's exploitability in the FULL game (collapse the mixture over
     behavioral policies into one behavioral policy per seat with Step 09's
     `mixture_behavioral_policy`, then Step 07 `nash_gap`), and compare it to the best
     INDIVIDUAL agent's exploitability.

Key predicted result (raw Validation L490): the meta-Nash MIXTURE is <= as exploitable as the
best single agent -- mixing over a diverse population is safer than any one policy.

CONVENTIONS
-----------
- `seat_payoff[i][j]` = exact EV for player 0 when policy i sits in seat 0 and policy j in
  seat 1 (the PSRO-style meta-matrix; used for the spinning-top decomposition of the raw
  meta-game, and it is what a fixed-seat empirical game looks like).
- `symmetric_payoff[i][j]` = seat-averaged margin of i vs j (antisymmetric, zero-sum) -- the
  right object when every agent plays BOTH seats, as in a league. Used for meta-Nash, Elo and
  the league spinning-top.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import numpy as np

import deps  # noqa: F401  (step09 + step07 on sys.path)
from best_response import exact_value, nash_gap
from psro import mixture_behavioral_policy       # reuse Step 09's realization-weighted mixture
from meta_nash import solve_meta_nash


def seat_payoff_matrix(game, policies):
    """U[i][j] = exact EV for seat 0 when policy i is seat 0 and policy j is seat 1."""
    n = len(policies)
    U = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            U[i, j] = exact_value(game, 0, policies[i], policies[j])
    return U


def symmetric_payoff_matrix(game, policies):
    """M[i][j] = 0.5 * ( v0(i as seat0 vs j as seat1) + v_i(i as seat1 vs j as seat0) ), the
    seat-averaged margin of i against j. Antisymmetric (M = -M.T) for a zero-sum game, which
    is exactly what meta-Nash / Elo / the spinning-top want for a both-seats population."""
    n = len(policies)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            v_i_seat0 = exact_value(game, 0, policies[i], policies[j])   # i in seat 0
            v_i_seat1 = exact_value(game, 1, policies[j], policies[i])   # i in seat 1
            M[i, j] = 0.5 * (v_i_seat0 + v_i_seat1)
    return M


def build_empirical_game(game, policies, symmetric: bool = True):
    """Construct the empirical meta-game payoff matrix (raw step L443-451). `symmetric=True`
    (default) returns the seat-averaged both-seats matrix; False returns the fixed-seat one."""
    return symmetric_payoff_matrix(game, policies) if symmetric else seat_payoff_matrix(game, policies)


def compute_meta_nash(payoff_matrix):
    """Meta-Nash of the empirical game (row_mix, col_mix). For the antisymmetric symmetric
    matrix, row_mix ~ col_mix (the symmetric meta-Nash mixture)."""
    return solve_meta_nash(payoff_matrix)


def meta_nash_mixture(payoff_matrix) -> np.ndarray:
    """A single mixture weight vector over the policies (average of the two meta-Nash sides;
    they coincide for a symmetric zero-sum meta-game)."""
    row_mix, col_mix = compute_meta_nash(payoff_matrix)
    mix = 0.5 * (np.asarray(row_mix, float) + np.asarray(col_mix, float))
    return mix / mix.sum()


def meta_nash_exploitability(game, policies, mixture) -> float:
    """Exploitability (full-game NashConv) of the meta-Nash mixture, played in BOTH seats.

    Collapses the mixture over the policies' behavioral strategies into one behavioral policy
    per seat (Step 09 `mixture_behavioral_policy`, valid by Leduc perfect recall), then Step 07
    `nash_gap`. This is the population's exploitability -- the Contribution-#3 metric.
    """
    mixture = np.asarray(mixture, dtype=float)
    beta0 = mixture_behavioral_policy(game, 0, policies, mixture)
    beta1 = mixture_behavioral_policy(game, 1, policies, mixture)
    return float(nash_gap(game, beta0, beta1)["nash_conv"])


def individual_exploitabilities(game, policies) -> list:
    """NashConv of each agent playing itself in both seats (its standalone exploitability)."""
    return [float(nash_gap(game, p, p)["nash_conv"]) for p in policies]


def score_matrix(symmetric_M, scale: float = 2.0) -> np.ndarray:
    """Map the seat-averaged margins to expected scores in [0,1] for Elo: S[i][j] =
    logistic(M[i][j] / scale). `scale` is roughly the payoff spread (Leduc pots are a few
    chips). S is ~antisymmetric (S[i][j] + S[j][i] ~ 1)."""
    M = np.asarray(symmetric_M, dtype=float)
    return 1.0 / (1.0 + np.exp(-M / scale))


def analyze_population(game, policies, agent_ids=None) -> dict:
    """One-shot EGTA report: empirical game, meta-Nash mixture, meta-Nash vs best-individual
    exploitability, and the Elo score matrix. Returns JSON-serializable primitives."""
    ids = list(agent_ids) if agent_ids is not None else list(range(len(policies)))
    M = symmetric_payoff_matrix(game, policies)
    mix = meta_nash_mixture(M)
    meta_expl = meta_nash_exploitability(game, policies, mix)
    indiv = individual_exploitabilities(game, policies)
    best_indiv = float(min(indiv)) if indiv else float("nan")
    return {
        "ids": ids,
        "symmetric_payoff": M.tolist(),
        "meta_nash_mixture": [round(float(w), 5) for w in mix],
        "meta_nash_exploitability": round(meta_expl, 5),
        "individual_exploitabilities": [round(v, 5) for v in indiv],
        "best_individual_exploitability": round(best_indiv, 5),
        "meta_nash_no_worse_than_best_individual": bool(meta_expl <= best_indiv + 1e-6),
        "score_matrix": score_matrix(M).tolist(),
    }


def _selftest():
    print("egta self-test")
    print("-" * 60)
    from engines import make_game
    from policies import uniform_policy
    from nash import solve_nash_cached
    game = make_game("kuhn")   # small + fast for the self-test
    nash, _ = solve_nash_cached(game, iters=2000)
    policies = [uniform_policy(), nash]
    rep = analyze_population(game, policies, ["uniform", "nash"])
    print(f"  meta-Nash mixture over [uniform, nash] = {rep['meta_nash_mixture']} "
          f"(PREDICT weight concentrates on nash)")
    print(f"  meta-Nash exploitability = {rep['meta_nash_exploitability']} vs best individual "
          f"= {rep['best_individual_exploitability']}")
    print(f"  meta-Nash <= best individual? {rep['meta_nash_no_worse_than_best_individual']} "
          f"(PREDICT True)")


if __name__ == "__main__":
    _selftest()
