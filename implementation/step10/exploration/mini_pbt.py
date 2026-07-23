"""
mini_pbt.py -- a fast PBT proxy that shows DIVERSITY COLLAPSE (raw step 10 Day 2, L139-145).

WHAT IT DOES
------------
A population of strategies (softmax genotypes over the actions of a matrix game) plays
round-robin; each generation the bottom 20% are replaced by MUTATED copies of the top 20%
(PBT's exploit + explore). We track how DIVERSE the population stays.

Instead of 10 full PPO agents (slow), each "agent" is a strategy vector -- a fast proxy that
isolates the population dynamic the raw step points at. The lesson is the same:

  - On a TRANSITIVE game (Prisoner's Dilemma, defection dominates) the population COLLAPSES to
    the single dominant strategy -- diversity -> 0. Good for a game with a clear best answer,
    fatal for a non-transitive one.
  - On a NON-TRANSITIVE game (Rock-Paper-Scissors) there is no single best answer, so naive
    PBT does NOT settle -- diversity stays high / churns. This is exactly why AlphaStar needs
    EXPLOITERS: to keep pressuring a population that would otherwise chase its own tail.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Numbers are PREDICTIONS.
"""

from __future__ import annotations

import numpy as np

from _evo_tools import GAMES, save_json, get_plt

CONFIG = {
    "games": ["prisoners_dilemma", "rock_paper_scissors"],
    "pop_size": 10,
    "generations": 60,
    "replace_fraction": 0.2,
    "mutation_std": 0.5,
    "seed": 0,
}


def _softmax(z):
    z = z - z.max()
    e = np.exp(z)
    return e / e.sum()


def _mean_pairwise_distance(strategies):
    n = len(strategies)
    if n < 2:
        return 0.0
    d = 0.0
    c = 0
    for i in range(n):
        for j in range(i + 1, n):
            d += float(np.mean(np.abs(strategies[i] - strategies[j])))
            c += 1
    return d / c


def run_pbt(A, cfg, rng):
    n_actions = A.shape[0]
    logits = [rng.standard_normal(n_actions) for _ in range(cfg["pop_size"])]
    diversity_curve = []
    mean_strategy_curve = []
    for _ in range(cfg["generations"]):
        strategies = [_softmax(z) for z in logits]
        # round-robin fitness: average payoff vs every population member
        fitness = np.zeros(cfg["pop_size"])
        for i in range(cfg["pop_size"]):
            fitness[i] = np.mean([strategies[i] @ A @ strategies[j]
                                  for j in range(cfg["pop_size"])])
        diversity_curve.append(round(_mean_pairwise_distance(strategies), 4))
        mean_strategy_curve.append(np.mean(strategies, axis=0).round(3).tolist())
        # PBT: bottom fraction copy a random top-fraction genotype + mutate
        order = np.argsort(-fitness)
        n_rep = max(1, int(cfg["replace_fraction"] * cfg["pop_size"]))
        top = order[:n_rep]
        bottom = order[-n_rep:]
        for b in bottom:
            src = top[int(rng.integers(len(top)))]
            logits[b] = logits[src] + cfg["mutation_std"] * rng.standard_normal(n_actions)
    return diversity_curve, mean_strategy_curve


def main():
    rng = np.random.default_rng(CONFIG["seed"])
    plt = get_plt()
    fig = None
    if plt is not None:
        fig, ax = plt.subplots(figsize=(7.5, 4.5))
    results = {}
    for name in CONFIG["games"]:
        A = GAMES[name]["A"]
        div, mean_strat = run_pbt(A, CONFIG, rng)
        print(f"\n[{name}]  actions={GAMES[name]['actions']}")
        print(f"   diversity (mean pairwise dist) start={div[0]} -> end={div[-1]}")
        print(f"   final mean strategy = {mean_strat[-1]}")
        pred = ("PREDICT: diversity -> ~0 (collapse to Defect)" if name == "prisoners_dilemma"
                else "PREDICT: diversity stays high / churns (no single best answer)")
        print(f"   {pred}")
        results[name] = {"diversity_curve": div, "final_mean_strategy": mean_strat[-1]}
        if plt is not None:
            ax.plot(div, label=name, lw=1.5)
    save_json("mini_pbt", results)
    if plt is not None:
        ax.set_xlabel("generation")
        ax.set_ylabel("population diversity (mean pairwise L1 distance)")
        ax.set_title("Naive PBT: diversity collapses on transitive games, churns on cyclic ones")
        ax.grid(alpha=0.3)
        ax.legend()
        import os
        from _evo_tools import FIGURES_DIR
        os.makedirs(FIGURES_DIR, exist_ok=True)
        path = os.path.join(FIGURES_DIR, "mini_pbt.png")
        fig.tight_layout()
        fig.savefig(path, dpi=120)
        plt.close(fig)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
