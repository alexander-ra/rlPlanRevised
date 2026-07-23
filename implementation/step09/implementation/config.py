"""
Experiment configuration + sizing policy for Step 09.

COMPUTE REALITY CHECK (read before reaching for the 5090).
----------------------------------------------------------
This step is a MIX of exact/tabular work and tiny neural nets:
  - Matrix games, PSRO (exact BR oracle over Kuhn/Leduc/Goofspiel), meta-Nash LPs, and LOLA
    are EXACT and CPU-bound; the GPU does nothing for them.
  - The CTDE/communication learners (IL/MADDPG/MAPPO/CommNet) are small MLPs on one-step
    cooperative tasks; they run fine on CPU in seconds-to-minutes. A GPU is not needed at this
    scale -- the point is the QUALITATIVE result (CTDE beats IL, comm helps, central critic has
    lower variance), not throughput.

Per implementation/WORKFLOW.md the default is small and fast. `smoke` proves correctness
cheaply (Kuhn PSRO, small matrix/coop runs). `scale` adds Leduc PSRO and larger coop training
for a more convincing picture; rough estimates are in RUNTIME_NOTES (verify on your machine).

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
    # --- matrix games (independent-learner outcomes vs analytic Nash) ---
    "matrix_games": ["prisoners_dilemma", "matching_pennies", "stag_hunt", "battle_of_the_sexes"],
    "matrix_learn": {"steps": 4000, "lr": 0.1, "seeds": [0, 1, 2]},
    # --- PSRO ---
    "psro": {
        "kuhn_rounds": 12,
        "leduc_rounds": 6,          # small, just to prove convergence trend; raise in scale
        "matrix_game": "matching_pennies",
        "matrix_rounds": 6,
        "goofspiel_cards": 3,
        "goofspiel_rounds": 5,
        "oracle": "exact",
    },
    # --- cooperative CTDE / communication (torch; SKIP if torch absent) ---
    "coop": {
        "n_targets": 4,
        "episodes": 4000,
        "batch_episodes": 256,
        "seeds": [0],
    },
    # --- LOLA on IPD ---
    # lr_opp is the LOLA look-ahead step. At 1.0 the finite-difference LOLA settles into an
    # asymmetric partial-cooperation fixed point (~1.2/2.5); 5.0 reaches near-symmetric
    # cooperation (~2.5-2.9). See EXECUTION_NOTES.
    "lola": {"gamma": 0.96, "lr": 1.0, "lr_opp": 5.0, "steps": 150},
    "plot": True,
}

SCALE = {
    "name": "scale",
    "seed": 0,
    "matrix_games": ["prisoners_dilemma", "matching_pennies", "stag_hunt", "battle_of_the_sexes"],
    "matrix_learn": {"steps": 8000, "lr": 0.1, "seeds": [0, 1, 2, 3, 4]},
    "psro": {
        "kuhn_rounds": 20,
        "leduc_rounds": 20,         # the raw-step target: exploitability < 0.5 within 20 iters
        "matrix_game": "matching_pennies",
        "matrix_rounds": 10,
        "goofspiel_cards": 4,
        "goofspiel_rounds": 8,
        "oracle": "exact",
    },
    "coop": {
        "n_targets": 5,
        # Emergent communication needs enough GRADIENT UPDATES (one per batch): 12000/256 = ~47
        # updates leaves the channel unlearned. 20000/32 = ~625 updates lets the speaker->listener
        # protocol emerge (comm ON -> ~1.0 vs OFF -> ~1/K). See EXECUTION_NOTES.
        "episodes": 20000,
        "batch_episodes": 32,
        "seeds": [0, 1, 2],
    },
    "lola": {"gamma": 0.96, "lr": 1.0, "lr_opp": 5.0, "steps": 300},
    "plot": True,
}

CONFIGS = {"smoke": SMOKE, "scale": SCALE}

# Rough, UNVERIFIED estimates (single core / CPU). Measure on your own machine.
RUNTIME_NOTES = {
    "matrix suite": "seconds (exact-gradient learners on 2x2 games).",
    "psro kuhn (12-20 rounds)": "seconds-to-a-minute (exact BR + meta-LP each round on the "
                                "small Kuhn tree).",
    "psro leduc (up to 20 rounds)": "minutes: each round recomputes new meta rows/cols via "
                                    "exact tree traversals and one full-tree BR per player; "
                                    "cost grows with the population size squared.",
    "psro goofspiel (K=3/4)": "seconds (K=3) to a couple of minutes (K=4): exact recursion "
                              "over the (K!)^2-leaf tree.",
    "coop CTDE/comm (torch)": "seconds-to-minutes per method (small MLPs, one-step episodes).",
    "lola ipd": "a few seconds (nested finite differences over a 5-dim policy).",
    "note": "The most expensive single piece is PSRO on Leduc; keep leduc_rounds modest in "
            "smoke and only push to 20 in scale.",
}


def get_config(name: str = "smoke") -> dict:
    if name not in CONFIGS:
        raise ValueError(f"Unknown config {name!r}; choose from {sorted(CONFIGS)}")
    import copy
    return copy.deepcopy(CONFIGS[name])
