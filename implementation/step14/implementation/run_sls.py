"""
run_sls.py -- the protocol's N-player layers on Chapter 11's four-player So Long Sucker engine.

    python run_sls.py [--games 2000] [--seeds 3]

So Long Sucker has no exact best response in this code base, so Layer 1 (exploitability) and
the speed/recovery layer (no adaptive SLS agent was kept from Chapter 11) do not apply. What
does apply, unchanged:
  * Layer 2 on the pairwise projection of the four-player game (Chapter 11's
    `pairwise_matchup_matrix`: two seats per agent, seats shuffled), re-measured on the FIXED
    engine (Chapter 11's own scale_results.json predates its tie-break fix);
  * a coalition probe: each baseline's win rate against three independent random players
    versus against a planted alliance (two opponents that help each other, Chapter 11's
    `make_fixed_ally`) plus one random player, focal seat rotated over all four seats.
    Reference line: the equal share 1/4 (Ge et al. 2025: a target, not securable against
    heterogeneous opponents).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

import deps
import population as pop
from logutil import Logger

sys.path.append(deps.STEP11_IMPL)
from sls_game import SLSGame, play_game          # Step 11


def sls_agents():
    # this chapter also has an agents.py, so Step 11's is loaded by path under a unique name
    return deps.load_by_path(os.path.join(deps.STEP11_IMPL, "agents.py"), "step11_agents")


def pairwise_matchup_matrix(game, pool, n_games, seed):
    """Chapter 11's projection (sls_egta.pairwise_matchup_matrix), re-stated here because that
    module's imports pull in Chapters 9-10: two seats per agent, seats shuffled, margin = mean
    reward of i's seats minus mean reward of j's seats."""
    A = len(pool)
    rng = np.random.default_rng(seed)
    M = np.zeros((A, A))
    for i in range(A):
        for j in range(i + 1, A):
            margins = []
            for _ in range(n_games):
                seats = [i, i, j, j]
                rng.shuffle(seats)
                final, rewards = play_game(game, [pool[t] for t in seats], seed=int(rng.integers(1 << 30)))
                margins.append(np.mean([rewards[s] for s in range(4) if seats[s] == i]) -
                               np.mean([rewards[s] for s in range(4) if seats[s] == j]))
            M[i, j] = float(np.mean(margins))
            M[j, i] = -M[i, j]
    return M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--games", type=int, default=2000)
    ap.add_argument("--seeds", type=int, default=3)
    args = ap.parse_args()
    log = Logger("sls")
    t0 = time.time()
    A = sls_agents()
    game = SLSGame(n_players=4, chips_per_player=7)
    names = ["random", "greedy_capture", "fixed_ally_1", "betrayer_1"]
    pool = [A.BASELINE_FACTORY[n]() for n in names]
    Ms = [pairwise_matchup_matrix(game, pool, n_games=args.games, seed=100 + s)
          for s in range(args.seeds)]
    M = np.mean(Ms, axis=0)
    se = np.std(Ms, axis=0, ddof=1) / np.sqrt(args.seeds)
    n = len(names)
    # win share of i over j per game from the margin: margins are reward differences in [-4/3, 4/3]
    P = 0.5 + 0.5 * M / (4.0 / 3.0)
    np.fill_diagonal(P, 0.5)
    p_star, skill = pop.nash_average(M)
    layer2 = {"agents": names, "pairwise_margin": M.tolist(), "pairwise_margin_se": se.tolist(),
              "transitive_ratio": pop.transitive_ratio(M), "elo": pop.elo_fit(P).tolist(),
              "nash_avg_p": p_star.tolist(), "nash_avg_skill": skill.tolist(),
              "alpharank": {str(a): pop.alpharank(M, a, 50).tolist() for a in (1.0, 10.0, 100.0)},
              "maximal_lottery": pop.maximal_lottery(P - P.T).tolist(),
              "population_return": [float(np.mean(np.delete(M[i], i))) for i in range(n)]}
    log(f"layer 2: transitive ratio {layer2['transitive_ratio']:.3f}; margins\n{np.round(M, 3)}")
    log(f"layer 2: Elo {np.round(layer2['elo'], 0).tolist()}; Nash-avg p {np.round(p_star, 2).tolist()}")
    # coalition probe
    rows = {}
    for f in names:
        res = {"independent": [], "alliance": []}
        for s in range(args.seeds):
            rng = np.random.default_rng(500 + s)
            for cond in ("independent", "alliance"):
                wins = 0
                for g in range(args.games):
                    fseat = g % 4
                    others = [(fseat + k) % 4 for k in (1, 2, 3)]
                    pols = [None] * 4
                    pols[fseat] = A.BASELINE_FACTORY[f]() if f != "fixed_ally_1" else A.make_fixed_ally(others[2])
                    if cond == "independent":
                        for q in others:
                            pols[q] = A.random_policy
                    else:
                        a1, a2, r = others
                        pols[a1] = A.make_fixed_ally(a2)
                        pols[a2] = A.make_fixed_ally(a1)
                        pols[r] = A.random_policy
                    st, rew = play_game(game, pols, seed=int(rng.integers(1 << 30)))
                    wins += int(st.winner == fseat)
                res[cond].append(wins / args.games)
        rows[f] = {k: {"mean": float(np.mean(v)), "ci95": float(1.96 * np.std(v, ddof=1) / np.sqrt(len(v))),
                       "per_seed": v} for k, v in res.items()}
        rows[f]["exposure"] = rows[f]["independent"]["mean"] - rows[f]["alliance"]["mean"]
        log(f"coalition probe {f:15s}: win rate independent {rows[f]['independent']['mean']:.3f} "
            f"vs alliance {rows[f]['alliance']['mean']:.3f} (drop {rows[f]['exposure']:+.3f})")
    out = {"game": "so_long_sucker(4 players, 7 chips; Chapter 11 engine)", "games_per_cell": args.games,
           "seeds": args.seeds, "layer2": layer2, "coalition_probe": rows,
           "note": "fixed_ally_1 as focal helps the random player in the last opponent seat",
           "runtime_seconds": time.time() - t0}
    with open(os.path.join(deps.RESULTS_DIR, "sls.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, default=float)
    log(f"done in {out['runtime_seconds']:.0f} s")


if __name__ == "__main__":
    main()
