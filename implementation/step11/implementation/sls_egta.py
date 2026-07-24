"""
sls_egta.py -- Empirical Game-Theoretic Analysis of a So Long Sucker agent population (raw step 11
L501-529, L551-552). 🔴 HAND-CODE: the Contribution-#3 evaluation prototype for the N-player case.

THE PROBLEM (raw L505-513): a 4-player game has a payoff TENSOR, not a matrix --
`payoff[i,j,k,l]` = expected reward for agent-type i against types j,k,l. There is no exact
best-response / exploitability (raw L320-329), so evaluation is EMPIRICAL.

WHAT THIS DOES
--------------
1. `payoff_tensor`: the empirical 4-player payoff, one entry per multiset of 4 agent types
   (`combinations_with_replacement`), each a mean reward vector from `n_games` random games.
2. `pairwise_matchup_matrix`: PROJECT the tensor to a 2D head-to-head matrix (raw L528) -- for each
   ordered pair of types, their average reward MARGIN when matched (2 seats each) in random
   4-player games. Antisymmetric -> exactly what Step 10's spinning-top + Step 09's meta-Nash want.
3. `analyze_meta_game`: reuse Step 10 `spinning_top` (transitive vs cyclic) and Step 09
   `solve_meta_nash` (the meta-strategy over agent types) on that projected matrix.

KEY PREDICTION (raw L529, L561): SLS's projected meta-game should be strongly CYCLIC (coalition
rock-paper-scissors), i.e. cyclic component > 50% -> transitive_ratio < ~0.707.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import itertools

import numpy as np

import deps  # noqa: F401  (Step 10 + Step 09 on sys.path)
from spinning_top import transitive_ratio, cyclic_ratio, spinning_top_decomposition
from meta_nash import solve_meta_nash
from sls_game import SLSGame, play_game


def payoff_tensor(game: SLSGame, agent_pool, n_games: int = 200, seed: int = 0) -> dict:
    """Empirical payoff over all size-N multisets of agent types (raw L504-524).

    `agent_pool` is a list of SLS policies. Returns {combo (sorted tuple of type indices):
    mean reward vector over the seated agents}. For 4 seats and A types there are C(A+3,4)
    multisets -- feasible for small pools.
    """
    n = game.n_players
    rng = np.random.default_rng(seed)
    out = {}
    for combo in itertools.combinations_with_replacement(range(len(agent_pool)), n):
        total = np.zeros(n)
        for _ in range(n_games):
            seated = [agent_pool[t] for t in combo]
            final, rewards = play_game(game, seated, seed=int(rng.integers(1 << 30)))
            total += rewards
        out[tuple(combo)] = (total / n_games).tolist()
    return out


def pairwise_matchup_matrix(game: SLSGame, agent_pool, n_games: int = 200, seed: int = 0) -> np.ndarray:
    """Project to a 2D antisymmetric head-to-head matrix (raw L528). M[i][j] = average reward
    margin of type i over type j when 2 seats are type i and 2 are type j (seat assignment
    randomized to remove position bias)."""
    n = game.n_players
    A = len(agent_pool)
    rng = np.random.default_rng(seed)
    M = np.zeros((A, A))
    for i in range(A):
        for j in range(i + 1, A):
            margins = []
            for _ in range(n_games):
                seats = [i, i, j, j]
                rng.shuffle(seats)
                seated = [agent_pool[t] for t in seats]
                final, rewards = play_game(game, seated, seed=int(rng.integers(1 << 30)))
                i_rew = np.mean([rewards[s] for s in range(n) if seats[s] == i])
                j_rew = np.mean([rewards[s] for s in range(n) if seats[s] == j])
                margins.append(i_rew - j_rew)
            m = float(np.mean(margins))
            M[i][j] = m
            M[j][i] = -m       # enforce antisymmetry (zero-sum head-to-head margin)
    return M


def analyze_meta_game(M: np.ndarray) -> dict:
    """Spinning-top decomposition (Step 10, Hodge) + meta-Nash (Step 09) on the projected matrix.

    Returns transitive/cyclic ratios (Hodge, so t^2 + c^2 ~= 1) and the meta-Nash mixture over
    agent types + its participation (effective number of active types).
    """
    M = np.asarray(M, dtype=float)
    t_ratio = transitive_ratio(M, method="hodge")
    c_ratio = cyclic_ratio(M, method="hodge")
    row_mix, col_mix = solve_meta_nash(M)          # zero-sum -> LP (scipy) or FP fallback
    mix = 0.5 * (np.asarray(row_mix, float) + np.asarray(col_mix, float))
    mix = mix / mix.sum() if mix.sum() > 0 else mix
    participation = float(1.0 / np.sum(mix ** 2)) if mix.sum() > 0 else 0.0  # inverse Simpson
    return {
        "transitive_ratio": round(t_ratio, 4),
        "cyclic_ratio": round(c_ratio, 4),
        "cyclic_dominates": bool(c_ratio > t_ratio),         # raw L561 target: cyclic > 50%
        "meta_nash_mixture": [round(float(w), 4) for w in mix],
        "participation": round(participation, 3),
        "num_active": int(np.sum(np.asarray(mix) > 1e-3)),
    }


def _selftest():
    print("sls_egta self-test  (PREDICTIONS -- verify on a real run)")
    print("-" * 72)
    game = SLSGame(n_players=4, chips_per_player=5)

    # a small, torch-free agent pool: random + two "ally-biased" heuristics + greedy-capture
    from agents import random_policy, make_fixed_ally, greedy_capture_policy
    pool = [random_policy, greedy_capture_policy, make_fixed_ally(1), make_fixed_ally(2)]

    M = pairwise_matchup_matrix(game, pool, n_games=40, seed=0)
    print("  projected pairwise margin matrix M (antisymmetric):")
    print("  " + str(np.round(M, 3).tolist()))
    rep = analyze_meta_game(M)
    print(f"  transitive_ratio={rep['transitive_ratio']}  cyclic_ratio={rep['cyclic_ratio']}  "
          f"cyclic_dominates={rep['cyclic_dominates']}")
    print(f"  meta-Nash mixture={rep['meta_nash_mixture']}  num_active={rep['num_active']} "
          f"(PREDICT raw L561: SLS meta-game leans CYCLIC -- cyclic_ratio should be sizeable)")

    # reconstruction sanity: T + C == antisymmetrized M
    T, C, A = spinning_top_decomposition(M)
    print(f"  recon max|T+C - A_anti| = {float(np.max(np.abs((T + C) - A))):.2e} (must be ~0)")


if __name__ == "__main__":
    _selftest()
