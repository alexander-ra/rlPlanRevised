"""
Experiment configuration + sizing policy for Step 10.

COMPUTE REALITY CHECK (read before reaching for the 5090)
---------------------------------------------------------
This step is a MIX of exact/tabular analysis and small neural training:
  - Replicator dynamics, the spinning-top decomposition, EGTA meta-Nash, Elo, and the PSRO /
    CFR baselines are EXACT and CPU-bound; the GPU does nothing for them.
  - The PBT LEAGUE is the only neural piece: a handful of small MLP agents (obs dim ~33) doing
    short Leduc self-play rollouts. It runs on CPU for the `smoke` config; the `scale` config
    (more agents, more episodes, more epochs) is where a GPU (the RTX 5090) helps, though even
    scale is modest by deep-RL standards -- Leduc is tiny.

Per implementation/WORKFLOW.md the default is small and fast. `smoke` proves correctness
cheaply; `scale` is the convincing run. Rough (UNVERIFIED) runtime estimates are in
RUNTIME_NOTES -- measure on your own machine.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_HERE, "results")
PLOTS_DIR = os.path.join(_HERE, "plots")


SMOKE = {
    "name": "smoke",
    "seed": 0,
    # --- evolutionary dynamics (replicator) ---
    "replicator": {
        "games": ["prisoners_dilemma", "hawk_dove", "rock_paper_scissors", "stag_hunt"],
        "T": 6000, "dt": 0.01,
        # a couple of starts so Stag Hunt shows both basins
        "starts": {"stag_hunt": [[0.8, 0.2], [0.2, 0.8]]},
    },
    # --- spinning-top decomposition targets ---
    "spinning_top": {
        "psro_leduc_rounds": 8,     # build a PSRO meta-game to decompose (Step 09 reuse)
        "include_league": True,     # also decompose the league meta-game (if torch present)
    },
    # --- the PBT league (torch; SKIP if torch absent) ---
    "league": {
        "num_main": 3, "num_main_exploiters": 2, "num_league_exploiters": 2,
        "hidden": 64, "base_lr": 3e-3, "base_entropy": 0.02,
        "episodes_per_epoch": 96, "epochs": 15,
        "freeze_every": 5, "pbt_every": 6, "pbt_fraction": 0.34,
        "pfsp_p": 1.0, "elo_k": 16.0, "score_scale": 2.0, "seed": 0,
    },
    # --- baselines for the comparison table ---
    "baselines": {
        "psro_leduc_rounds": 12,        # Step 09 PSRO on Leduc
        "selfplay_epochs": 15,          # single self-play agent (torch)
        "selfplay_episodes_per_epoch": 96,
        "cfr_iters": 2000,              # Step 07 CFR Nash (the ~0-exploitability reference)
    },
    "plot": True,
}

SCALE = {
    "name": "scale",
    "seed": 0,
    "replicator": {
        "games": ["prisoners_dilemma", "hawk_dove", "rock_paper_scissors", "stag_hunt"],
        "T": 20000, "dt": 0.005,
        "starts": {"stag_hunt": [[0.8, 0.2], [0.2, 0.8], [0.55, 0.45], [0.45, 0.55]]},
    },
    "spinning_top": {
        "psro_leduc_rounds": 20,
        "include_league": True,
    },
    "league": {
        "num_main": 4, "num_main_exploiters": 2, "num_league_exploiters": 2,
        "hidden": 128, "base_lr": 3e-3, "base_entropy": 0.02,
        "episodes_per_epoch": 512, "epochs": 120,   # raw step L438: "100+ training epochs"
        "freeze_every": 10, "pbt_every": 12, "pbt_fraction": 0.25,
        "pfsp_p": 1.5, "elo_k": 16.0, "score_scale": 2.0, "seed": 0,
    },
    "baselines": {
        "psro_leduc_rounds": 20,
        "selfplay_epochs": 120,
        "selfplay_episodes_per_epoch": 512,
        "cfr_iters": 20000,
    },
    "plot": True,
}

CONFIGS = {"smoke": SMOKE, "scale": SCALE}

# Rough, UNVERIFIED estimates (single core / CPU unless noted). Measure on your own machine.
RUNTIME_NOTES = {
    "replicator suite": "seconds (numpy Euler integration on 2-3 strategy games).",
    "spinning-top suite": "seconds + the PSRO-Leduc build (minutes; see PSRO note).",
    "psro leduc (12-20 rounds)": "minutes: each round = exact tree traversals + one full-tree "
                                 "best response per player; cost ~ population size squared.",
    "league smoke (15 epochs, 7 agents)": "minutes on CPU: per epoch = 7 tabular extractions "
                                          "(tree walks with net forwards) + an O(n^2) exact "
                                          "meta-matrix + 7 * ~96 short rollouts + PPO updates.",
    "league scale (120 epochs, deeper nets)": "the big one: tens of minutes to a couple of "
                                              "hours; a GPU helps the PPO updates. Leduc keeps "
                                              "the exact-eval part cheap even at scale.",
    "selfplay baseline (torch)": "similar per-epoch cost to one league agent.",
    "cfr nash (20000 iters on Leduc)": "minutes (full-tree vanilla CFR); cached to _cache/.",
    "note": "The most expensive pieces are the SCALE league and PSRO-on-Leduc. Keep league "
            "epochs / episodes_per_epoch modest in smoke; only push to scale for the "
            "convincing exploitability-decrease curve.",
}


def get_config(name: str = "smoke") -> dict:
    if name not in CONFIGS:
        raise ValueError(f"Unknown config {name!r}; choose from {sorted(CONFIGS)}")
    import copy
    return copy.deepcopy(CONFIGS[name])
