"""Hyperparameter configurations for Step 03 implementations."""

CFR_CONFIG = {
    "game": "leduc_poker",
    "num_cards": 6,                          # {Js, Jh, Qs, Qh, Ks, Kh}
    "num_ranks": 3,                          # {J, Q, K}
    "num_suits": 2,                          # {s, h}
    "num_actions": 3,                        # FOLD=0, CALL/CHECK=1, RAISE=2
    "training_iterations": 1_000,            # small — smoke test only
    "convergence_checkpoints": [50, 100, 200, 500, 1_000],
    "theoretical_game_value": -0.0856,       # approx. (Leduc has no clean closed form)
    "nash_tolerance": 1e-2,                  # relaxed for small iteration counts
    "plot_checkpoint_interval_ratio": 100,   # record every iterations/100

    # Leduc-specific
    "max_raises_per_round": 2,               # max raises in each betting round
    "ante": 1,                               # each player antes 1
    "raise_amount_round1": 2,                # raise size in round 1
    "raise_amount_round2": 4,                # raise size in round 2
}
