"""
toy_rankings.py -- Phase 2 intuition: four ranking methods on three tiny meta-games.

    python toy_rankings.py      < 5 s

  RPS         : a pure cycle -- every method should be indifferent (uniform / equal ratings)
  ladder      : A > B > C > D -- every method should put A first
  exploiter   : N (an equilibrium-like agent that ties with the strong and beats the weak
                a little), E (an exploiter that loses slightly to N but crushes the weak W1, W2),
                W1, W2 (weak bots). This is the pattern the bot zoo produces.

For each: Elo (fitted to win probabilities from a logistic link on the margin), population
return (mean margin), Nash averaging, alpha-Rank at alpha = 0.1 and 100, maximal lottery.
Saves figures/toy_rankings.json.
"""

from __future__ import annotations

import json
import os

import numpy as np

import _bootstrap  # noqa: F401
import population as pop

games = {
    "rps": (["R", "P", "S"], np.array([[0, -1, 1], [1, 0, -1], [-1, 1, 0]], float)),
    "ladder": (["A", "B", "C", "D"], np.array([[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]], float)),
    "exploiter": (["N", "E", "W1", "W2"], np.array([[0.0, 0.05, 0.2, 0.2],
                                                     [-0.05, 0.0, 1.0, 1.0],
                                                     [-0.2, -1.0, 0.0, 0.0],
                                                     [-0.2, -1.0, 0.0, 0.0]])),
}
out = {}
for key, (names, M) in games.items():
    P = 1.0 / (1.0 + np.exp(-4.0 * M))           # a logistic link from margin to win probability
    np.fill_diagonal(P, 0.5)
    elo = pop.elo_fit(P)
    p_star, skill = pop.nash_average(M)
    res = {"elo": elo.tolist(), "population_return": M.mean(axis=1).tolist(),
           "nash_avg_p": p_star.tolist(), "nash_avg_skill": skill.tolist(),
           "alpharank_0.1": pop.alpharank(M, 0.1, 50).tolist(),
           "alpharank_100": pop.alpharank(M, 100.0, 50).tolist(),
           "maximal_lottery": pop.maximal_lottery(P - P.T).tolist(),
           "transitive_ratio": pop.transitive_ratio(M)}
    out[key] = {"agents": names, **res}
    print(f"\n[{key}] transitive ratio {res['transitive_ratio']:.2f}")
    for i, a in enumerate(names):
        print(f"  {a:3s} Elo {elo[i]:6.0f}  pop.return {res['population_return'][i]:+.3f}  "
              f"NashAvg p {p_star[i]:.2f} skill {skill[i]:+.3f}  "
              f"alphaRank(0.1) {res['alpharank_0.1'][i]:.2f}  alphaRank(100) {res['alpharank_100'][i]:.2f}  "
              f"max.lottery {res['maximal_lottery'][i]:.2f}")
with open(os.path.join(_bootstrap.FIG, "toy_rankings.json"), "w", encoding="utf-8") as fh:
    json.dump(out, fh, indent=1)
