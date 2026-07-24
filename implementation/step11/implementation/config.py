"""
config.py -- smoke vs 5090-scale experiment configs for Step 11 (WORKFLOW S7; raw L438, L495,
L504). 🟢 infrastructure.

- SMOKE  : fast, CPU, seconds-to-a-few-minutes -- proves correctness on tiny SLS (5 chips).
- SCALE  : the convincing run on an RTX 5090 (raw L495 "5000+ games"); budget ~a couple hours.

`get_config(name)` returns a plain dict consumed by `evaluation.py` / `tournament.py`. Seeds are
explicit so runs are reproducible.
"""

from __future__ import annotations

SMOKE = {
    "name": "smoke",
    "n_players": 4,
    "chips_per_player": 5,           # small tree -> fast games + tractable endgame check
    # training (coalition_mappo)
    "train_games": 400,
    "batch_games": 64,
    "alpha": 0.3,                    # sparse/Shapley blend (raw L488)
    "ppo": {"hidden": 128, "lr": 3e-4, "epochs": 3, "minibatch": 512},
    # evaluation
    "eval_winrate_games": 300,
    "egta_games_per_cell": 60,
    "endgame_chips": 2,              # exact 2-player endgame solver: keep tiny
    "endgame_trials": 20,
    "shapley_rollouts": 300,
    "seed": 0,
}

SCALE = {
    "name": "scale",
    "n_players": 4,
    "chips_per_player": 7,           # the canonical SLS size (raw L92)
    "train_games": 6000,             # raw L495: "5000+ games"
    "batch_games": 128,
    "alpha": 0.3,
    "ppo": {"hidden": 256, "lr": 3e-4, "epochs": 4, "minibatch": 1024},
    "eval_winrate_games": 1000,
    "egta_games_per_cell": 300,
    "endgame_chips": 3,              # a bit deeper endgame; still exactly solvable
    "endgame_trials": 40,
    "shapley_rollouts": 1000,
    "seed": 0,
}

CONFIGS = {"smoke": SMOKE, "scale": SCALE}


# --- coalition-emergence sweep (sweep.py) -------------------------------------------------
# Maps WHEN coalition-aware training beats the sparse baseline on the coalition score. Every cell
# runs `n_seeds` PAIRED seeds (same seeds for the sparse baseline) so the gap carries error bars --
# the smoke->scale single-seed flip (EXECUTION_NOTES Phase-4) needs this to separate signal/noise.
# Axes: alpha (sparse<->credit blend), credit_mode (proxy vs counterfactual win-prob-share),
# synergy (proxy only). `scale` uses fewer train_games than SCALE (raw L495 says the DIRECTION shows
# well before 6000 games) to keep the grid tractable.
SWEEP = {
    "alphas": [0.0, 0.1, 0.3, 0.5, 0.7],
    "credit_modes": ["proxy", "counterfactual"],
    "synergies": [0.1, 0.3],          # proxy only (counterfactual ignores synergy)
    "n_seeds": 5,
    "tiers": {
        "smoke": {"chips_per_player": 5, "train_games": 400, "batch_games": 64,
                  "ppo": {"hidden": 128, "lr": 3e-4, "epochs": 3, "minibatch": 512},
                  "eval_winrate_games": 200, "cf_rollouts": 120},
        "scale": {"chips_per_player": 7, "train_games": 1500, "batch_games": 128,
                  "ppo": {"hidden": 256, "lr": 3e-4, "epochs": 4, "minibatch": 1024},
                  "eval_winrate_games": 400, "cf_rollouts": 150},
    },
}

RUNTIME_NOTES = """
Rough runtime estimates (VERIFY on your machine -- nothing was run here):
  SMOKE (CPU):
    - env / detector / shapley / endgame checks : seconds
    - coalition_mappo train (2 x 400 games)     : ~2-6 min on CPU (torch)
    - EGTA pairwise matrix (small pool)         : ~1-2 min
    -> full `tournament.py --config smoke`      : ~5-10 min
  SCALE (RTX 5090):
    - coalition_mappo train (2 x 6000 games)    : ~1-2 h (the dominant cost; nets are small so
                                                  the GPU helps the PPO updates more than the
                                                  CPU-bound SLS rollouts -- expect CPU-bound)
    - EGTA + spinning top                       : ~10-20 min
    -> full `tournament.py --config scale`      : ~1.5-2.5 h
NOTE: SLS rollouts are pure-Python and CPU-bound; the 5090 mainly accelerates the PPO minibatch
math. If the SCALE train dominates, reduce `train_games` first -- the coalition-score DIRECTION
(Shapley > sparse) should be visible well before 6000 games.
"""


def get_config(name: str) -> dict:
    if name not in CONFIGS:
        raise ValueError(f"unknown config {name!r}; choose from {list(CONFIGS)}")
    return CONFIGS[name]


if __name__ == "__main__":
    for n, c in CONFIGS.items():
        print(f"[{n}] chips={c['chips_per_player']} train_games={c['train_games']} "
              f"egta_games/cell={c['egta_games_per_cell']} endgame_chips={c['endgame_chips']}")
    print(RUNTIME_NOTES)
