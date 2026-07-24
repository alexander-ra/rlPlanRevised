"""
sweep.py -- coalition-emergence sweep: WHEN does coalition-aware (Shapley) training beat the
sparse baseline on the COALITION SCORE? (Follow-on investigation; EXECUTION_NOTES Phase-4.)

WHY THIS EXISTS
---------------
The single-config runs left an ambiguous picture: the Shapley>sparse coalition-score gap was
positive at smoke (chips=5) but null/negative at scale (chips=7) -- and each was ONE seed, so the
"flip" might be noise. This grid answers the question properly:

  for each (credit_mode, alpha, synergy) cell, train `n_seeds` PAIRED seeds and a shared sparse
  baseline per seed, then report the mean +/- std of the PAIRED gap
  gap = coalition_score(shapley) - coalition_score(sparse),
  plus a crude significance flag (mean_gap > 2 * standard error). The map over `alpha` x
  `credit_mode` shows the REGIME where coalitions emerge -- or confirms they do not.

The `counterfactual` credit_mode (win-probability-share Shapley, refreshed per batch) is the
README's #1 suspected stronger signal vs the critic-value `proxy`; comparing the two is the point.

Run from `implementation/step11/implementation/`:
    python sweep.py --tier smoke           # the fast grid (minutes)
    python sweep.py --tier scale           # heavier (chips=7); background it
    python sweep.py --tier both --seeds 5

Torch is required (guarded); numpy for the stats. Writes results/sweep_<tier>.json.
"""

from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

import deps  # noqa: F401  (puts step09/step10 on sys.path for learners)
from config import SWEEP
from learners import torch_available

RESULTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def _train_one(chips, ppo, train_games, batch_games, use_shapley, alpha, credit_mode, synergy,
               cf_rollouts, eval_winrate_games, seed):
    """Train one agent population and return (mean_coalition_score, win_rate_vs_random)."""
    from coalition_mappo import CoalitionAwareMAPPO
    trainer = CoalitionAwareMAPPO(n_players=4, chips_per_player=chips, config=ppo, seed=seed)
    hist = trainer.train(n_games=train_games, batch_games=batch_games, use_shapley=use_shapley,
                         alpha=alpha, seed=seed, credit_mode=credit_mode, synergy=synergy,
                         cf_rollouts=cf_rollouts)
    wr = trainer.win_rate_vs_random(hero=0, n_games=eval_winrate_games, seed=seed)
    return float(hist["mean_coalition_score"]), float(wr)


def _cells(sweep: dict):
    """Enumerate (credit_mode, alpha, synergy) cells. synergy varies only for proxy (the
    counterfactual credit ignores it) -> no redundant counterfactual x synergy duplicates."""
    for cm in sweep["credit_modes"]:
        syns = sweep["synergies"] if cm == "proxy" else [sweep["synergies"][0]]
        for alpha in sweep["alphas"]:
            for syn in syns:
                yield cm, alpha, syn


def run_tier(tier: str, n_seeds: int) -> dict:
    t = SWEEP["tiers"][tier]
    seeds = list(range(n_seeds))
    chips, ppo = t["chips_per_player"], t["ppo"]
    tg, bg, cfr, ewg = t["train_games"], t["batch_games"], t["cf_rollouts"], t["eval_winrate_games"]

    # sparse baseline once per seed (independent of alpha/credit_mode/synergy)
    print(f"[{tier}] sparse baselines over {n_seeds} seeds ...", flush=True)
    sparse_score = {}
    sparse_wr = {}
    for s in seeds:
        sc, wr = _train_one(chips, ppo, tg, bg, False, 1.0, "proxy", 0.1, cfr, ewg, s)
        sparse_score[s], sparse_wr[s] = sc, wr
    sparse_mean = float(np.mean([sparse_score[s] for s in seeds]))

    cells = list(_cells(SWEEP))
    print(f"[{tier}] {len(cells)} cells x {n_seeds} seeds ...", flush=True)
    results = []
    for ci, (cm, alpha, syn) in enumerate(cells):
        scores, wrs, gaps = [], [], []
        for s in seeds:
            sc, wr = _train_one(chips, ppo, tg, bg, True, alpha, cm, syn, cfr, ewg, s)
            scores.append(sc); wrs.append(wr); gaps.append(sc - sparse_score[s])   # PAIRED gap
        gaps = np.array(gaps)
        gap_mean, gap_std = float(gaps.mean()), float(gaps.std(ddof=1)) if n_seeds > 1 else 0.0
        se = gap_std / np.sqrt(n_seeds) if n_seeds > 1 else float("inf")
        results.append({
            "credit_mode": cm, "alpha": alpha, "synergy": syn,
            "shapley_score_mean": float(np.mean(scores)), "shapley_score_std": float(np.std(scores, ddof=1) if n_seeds > 1 else 0.0),
            "win_rate_mean": float(np.mean(wrs)),
            "gap_mean": gap_mean, "gap_std": gap_std, "gap_se": (None if se == float("inf") else float(se)),
            "gap_significant_positive": bool(se != float("inf") and gap_mean > 2 * se),
            "n_seeds": n_seeds,
        })
        flag = "**" if results[-1]["gap_significant_positive"] else ("+" if gap_mean > 0 else "-")
        print(f"  [{ci+1:2}/{len(cells)}] {cm:14} alpha={alpha:.1f} syn={syn:.1f}  "
              f"gap={gap_mean:+.4f}+/-{(0.0 if se==float('inf') else se):.4f} {flag}", flush=True)

    return {
        "tier": tier, "chips_per_player": chips, "train_games": tg, "n_seeds": n_seeds,
        "sparse_coalition_score_mean": sparse_mean,
        "sparse_win_rate_mean": float(np.mean([sparse_wr[s] for s in seeds])),
        "cells": results,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", default="smoke", choices=["smoke", "scale", "both"])
    ap.add_argument("--seeds", type=int, default=SWEEP["n_seeds"])
    args = ap.parse_args()

    if not torch_available():
        print("[SKIP] torch not installed -> the sweep needs the neural trainer.")
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)
    tiers = ["smoke", "scale"] if args.tier == "both" else [args.tier]
    for tier in tiers:
        t0 = time.time()
        rep = run_tier(tier, args.seeds)
        rep["wall_seconds"] = round(time.time() - t0, 1)
        out = os.path.join(RESULTS_DIR, f"sweep_{tier}.json")
        with open(out, "w") as f:
            json.dump(rep, f, indent=2)
        # headline: best positive cell
        best = max(rep["cells"], key=lambda c: c["gap_mean"])
        print(f"[{tier}] done in {rep['wall_seconds']}s. sparse_score={rep['sparse_coalition_score_mean']:.4f}. "
              f"best gap {best['gap_mean']:+.4f} at {best['credit_mode']} alpha={best['alpha']} "
              f"syn={best['synergy']} (sig+={best['gap_significant_positive']}). wrote {out}", flush=True)


if __name__ == "__main__":
    main()
