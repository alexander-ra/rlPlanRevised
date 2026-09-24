"""Hyperparameter configurations for Step 02 implementations."""

CFR_CONFIG = {
    "game": "kuhn_poker",
    "num_cards": 3,                          # {J, Q, K}
    "num_actions": 2,                        # PASS=0, BET=1
    "training_iterations": 100_000,          # default training run
    # Log-spaced checkpoints up to the full training run, so the exploitability
    # curve (fig. "exploitability_convergence") covers the same 100k iterations
    # as the game-value curve.
    "convergence_checkpoints": [100, 300, 1_000, 3_000, 10_000, 30_000, 100_000],
    "seed": 0,                               # random.seed for cfr/train.py
    "convergence_seeds": [0, 1, 2, 3, 4],    # one incremental run per seed
    "theoretical_game_value": -1/18,         # ≈ -0.0556
    "nash_tolerance": 1e-4,                  # 4 decimal places
    "plot_checkpoint_interval_ratio": 200,   # record every iterations/200
}
