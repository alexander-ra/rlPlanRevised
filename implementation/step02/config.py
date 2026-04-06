"""Hyperparameter configurations for Step 02 implementations."""

CFR_CONFIG = {
    "game": "kuhn_poker",
    "num_cards": 3,                          # {J, Q, K}
    "num_actions": 2,                        # PASS=0, BET=1
    "training_iterations": 100_000,          # default training run
    "convergence_checkpoints": [100, 500, 1_000, 5_000, 10_000, 50_000],
    "theoretical_game_value": -1/18,         # ≈ -0.0556
    "nash_tolerance": 1e-4,                  # 4 decimal places
    "plot_checkpoint_interval_ratio": 200,   # record every iterations/200
}
