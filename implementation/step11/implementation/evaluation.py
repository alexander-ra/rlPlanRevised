"""
evaluation.py -- the suite runners that turn each raw-step Validation target (L556-561) into a
computed result dict. 🟢 infrastructure (calls the 🔴 cores).

Five suites (each returns a JSON-serializable dict):
  run_env_check          -> 2-player endgame consistency + random-game termination + zero-sum reward
  run_detector_check     -> the coalition detector fires on a hand-crafted cooperative log
  run_shapley_check      -> exact Shapley on glove/majority + symmetric-vs-asymmetric SLS credit
  run_training_comparison-> coalition-aware (Shapley) vs sparse MAPPO: coalition scores + win rates
  run_egta               -> projected pairwise meta-game: spinning-top ratio + meta-Nash

`validate.py` consumes these for PASS/FAIL; `tournament.py` runs them and prints tables + JSON.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here. Numbers are predictions.
"""

from __future__ import annotations

import numpy as np

from sls_game import SLSGame, SLSState, play_game, winner_rewards
from sls_endgame import verify_endgame_consistency
from coalition_detector import CoalitionDetector, make_cooperative_log, mean_offdiagonal_coalition
from shapley import exact_shapley, glove_value, majority_value, win_prob_coalition_values, shapley_credit
from agents import random_policy, default_baseline_pool
from sls_egta import pairwise_matchup_matrix, analyze_meta_game


def _state_with_hands(chip_counts) -> SLSState:
    n = len(chip_counts)
    hands = tuple(tuple(chip_counts[p] if c == p else 0 for c in range(n)) for p in range(n))
    elim = frozenset(p for p in range(n) if chip_counts[p] == 0)
    cur = next(p for p in range(n) if p not in elim)
    return SLSState(n_players=n, hands=hands, piles=(), eliminated=elim, current_player=cur)


# --- 1. environment correctness ---------------------------------------------------------
def run_env_check(cfg: dict) -> dict:
    """2-player endgame vs exact minimax + random-game termination + zero-sum rewards (raw L557)."""
    endgame = verify_endgame_consistency(chips_per_player=cfg["endgame_chips"],
                                         n_trials=cfg["endgame_trials"], seed=cfg["seed"])
    game = SLSGame(n_players=cfg["n_players"], chips_per_player=cfg["chips_per_player"])
    terminated, zero_sum = 0, 0
    n = 100
    for s in range(n):
        final, rewards = play_game(game, [random_policy] * cfg["n_players"], seed=s)
        terminated += 1 if final.done else 0
        zero_sum += 1 if abs(float(np.sum(rewards))) < 1e-9 else 0
    return {
        "endgame_mismatches": endgame["mismatches"],
        "endgame_passed": endgame["passed"],
        "random_games": n,
        "all_terminated": terminated == n,
        "all_zero_sum": zero_sum == n,
    }


# --- 2. coalition detection -------------------------------------------------------------
def run_detector_check(cfg: dict) -> dict:
    """The detector must identify a planted cooperating pair (raw L558)."""
    n = cfg["n_players"]
    log = make_cooperative_log(n, allies=(0, 1), n_helps=5)
    det = CoalitionDetector(n).ingest(log)
    pair = det.strongest_pair()
    return {
        "planted_allies": [0, 1],
        "strongest_pair": [pair[0], pair[1]] if pair else None,
        "strongest_score": pair[2] if pair else None,
        "identified_correct_pair": bool(pair and {pair[0], pair[1]} == {0, 1}),
        "coalition_matrix": np.round(det.get_coalition_scores(), 2).tolist(),
    }


# --- 3. Shapley credit ------------------------------------------------------------------
def run_shapley_check(cfg: dict) -> dict:
    """Exact Shapley on the two reference games + symmetric-vs-asymmetric SLS credit (raw L559)."""
    glove = exact_shapley(3, glove_value)
    majority = exact_shapley(3, majority_value)

    game = SLSGame(n_players=cfg["n_players"], chips_per_player=cfg["chips_per_player"])
    R = cfg["shapley_rollouts"]
    sym_vals, sym_wp = win_prob_coalition_values(game, _state_with_hands([5, 5, 5, 5]),
                                                 n_rollouts=R, seed=cfg["seed"])
    sym_credit = shapley_credit(4, sym_vals)
    asym_vals, asym_wp = win_prob_coalition_values(game, _state_with_hands([8, 8, 1, 1]),
                                                   n_rollouts=R, seed=cfg["seed"] + 1)
    asym_credit = shapley_credit(4, asym_vals)

    # symmetric spread (max-min) should be ~0; asymmetric strong-pair credit should exceed weak
    strong_pair = float(asym_credit[0] + asym_credit[1])
    weak_pair = float(asym_credit[2] + asym_credit[3])
    return {
        "glove_shapley": np.round(glove, 4).tolist(),
        "majority_shapley": np.round(majority, 4).tolist(),
        "glove_ok": bool(np.allclose(glove, [2 / 3, 1 / 6, 1 / 6], atol=1e-6)),
        "majority_ok": bool(np.allclose(majority, [1 / 3, 1 / 3, 1 / 3], atol=1e-6)),
        "symmetric_credit": np.round(sym_credit, 3).tolist(),
        "symmetric_spread": round(float(sym_credit.max() - sym_credit.min()), 3),
        "asymmetric_credit": np.round(asym_credit, 3).tolist(),
        "asym_strong_pair_credit": round(strong_pair, 3),
        "asym_weak_pair_credit": round(weak_pair, 3),
        "asym_strong_dominates": bool(strong_pair > weak_pair),
    }


# --- 4. coalition-aware training comparison --------------------------------------------
def run_training_comparison(cfg: dict) -> dict:
    """Train Shapley-reward vs sparse-reward agents; compare coalition scores + win rates
    (raw L496-499, L560). Torch-guarded -> returns {'skipped': True} without torch."""
    from learners import torch_available
    if not torch_available():
        return {"skipped": True, "reason": "torch not installed"}
    from coalition_mappo import CoalitionAwareMAPPO

    ppo = cfg["ppo"]
    results = {}
    for tag, use_shapley in (("sparse", False), ("shapley", True)):
        trainer = CoalitionAwareMAPPO(n_players=cfg["n_players"],
                                      chips_per_player=cfg["chips_per_player"],
                                      config=ppo, seed=cfg["seed"])
        hist = trainer.train(n_games=cfg["train_games"], batch_games=cfg["batch_games"],
                             use_shapley=use_shapley, alpha=cfg["alpha"], seed=cfg["seed"])
        wr = trainer.win_rate_vs_random(hero=0, n_games=cfg["eval_winrate_games"], seed=cfg["seed"])
        results[tag] = {
            "mean_coalition_score": hist["mean_coalition_score"],
            "coalition_score_curve": hist["coalition_score"],
            "win_rate_vs_random": round(wr, 4),
            "win_counts_during_training": hist["win_counts"].astype(int).tolist(),
        }
    results["shapley_higher_coalition"] = bool(
        results["shapley"]["mean_coalition_score"] > results["sparse"]["mean_coalition_score"])
    return results


# --- 5. EGTA meta-game + spinning top ---------------------------------------------------
def run_egta(cfg: dict, extra_policies=None, extra_names=None) -> dict:
    """Projected pairwise meta-game over the baseline pool (+ any trained agents), spinning-top
    decomposition + meta-Nash (raw L551-552, L561)."""
    game = SLSGame(n_players=cfg["n_players"], chips_per_player=cfg["chips_per_player"])
    names, pool = default_baseline_pool()
    if extra_policies:
        pool = pool + list(extra_policies)
        names = names + list(extra_names or [f"trained_{i}" for i in range(len(extra_policies))])
    M = pairwise_matchup_matrix(game, pool, n_games=cfg["egta_games_per_cell"], seed=cfg["seed"])
    report = analyze_meta_game(M)
    report["agent_names"] = names
    report["pairwise_matrix"] = np.round(M, 3).tolist()
    return report


if __name__ == "__main__":
    from config import SMOKE
    print("evaluation self-test (env + detector + shapley only; fast, torch-free)")
    print("-" * 72)
    print("env    :", run_env_check(SMOKE))
    print("detect :", run_detector_check(SMOKE))
    sh = run_shapley_check(SMOKE)
    print("shapley: glove_ok", sh["glove_ok"], "majority_ok", sh["majority_ok"],
          "asym_strong_dominates", sh["asym_strong_dominates"])
