"""
Experiment configuration + sizing policy for Step 07.

COMPUTE REALITY CHECK (read this before reaching for the 5090).
---------------------------------------------------------------
Everything in this step is *tabular*: CFR over a few hundred info sets, exact tree
traversals for best response, exact expected values, and a small SciPy convex program for
the consistent model. This is CPU-bound, single-threaded Python. The RTX 5090 does NOT
accelerate any of it -- there are no neural nets or GPU kernels here. So "scale up on the
5090" does not apply to Step 07; scaling here just means *more hands / more CFR iterations*,
which costs CPU time. (The GPU will matter in later steps that learn function approximators.)

Per implementation/WORKFLOW.md the default is small and fast. `smoke` runs in well under a
minute of CPU and is enough to see every qualitative result. `scale` tightens the Nash
solves and grows the sample sizes for publication-quality curves; rough CPU estimates are
in RUNTIME_NOTES below (verify them on your machine -- they are estimates, not measurements).

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os

_HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(_HERE, "results")
PLOTS_DIR = os.path.join(_HERE, "plots")


SMOKE = {
    "name": "smoke",
    "games": ["kuhn"],
    "hero": 0,
    "nash_iters": {"kuhn": 20000, "leduc": 2000},
    "detection_hands": 400,
    "exploit_hands": 2000,
    "refit_every": 50,
    "min_hands_before_exploit": 25,
    "safety": 0.0,
    "seeds": [0, 1, 2],
    "models": ["type_based", "continuous"],   # consistent is opt-in (scipy + slower)
    "include_consistent": False,
    "include_level_k": True,
    "level_k_levels": [1, 2],
    # first/second are per-game: the zoo type names differ between Kuhn and Leduc.
    "nonstationarity": {"first": {"kuhn": "TightPassive", "leduc": "Rock"},
                        "second": {"kuhn": "LooseAggressive", "leduc": "Maniac"},
                        "switch_at": 1000, "total": 2000},
    "plot": True,
}

SCALE = {
    "name": "scale",
    "games": ["kuhn", "leduc"],
    "hero": 0,
    "nash_iters": {"kuhn": 200000, "leduc": 40000},
    "detection_hands": 4000,
    "exploit_hands": 20000,
    "refit_every": 200,
    "min_hands_before_exploit": 100,
    "safety": 0.0,
    "seeds": [0, 1, 2, 3, 4],
    "models": ["type_based", "continuous", "consistent"],
    "include_consistent": True,
    "include_level_k": True,
    "level_k_levels": [1, 2, 3],
    "nonstationarity": {"first": {"kuhn": "TightPassive", "leduc": "Rock"},
                        "second": {"kuhn": "LooseAggressive", "leduc": "Maniac"},
                        "switch_at": 10000, "total": 20000},
    "plot": True,
}

CONFIGS = {"smoke": SMOKE, "scale": SCALE}

# Rough, UNVERIFIED CPU estimates (single core). Measure on your own machine.
RUNTIME_NOTES = {
    "kuhn smoke": "well under 1 min total (Kuhn is tiny).",
    "leduc smoke": "~1-3 min (Leduc CFR + traversals are heavier).",
    "kuhn scale": "a few minutes (200k CFR iters + 20k-hand matches x seeds).",
    "leduc scale": "tens of minutes to ~1-2 h depending on the consistent model and "
                   "40k CFR iters; if it drags, drop nash_iters or disable consistent.",
    "consistent model": "the SciPy solve dominates; Kuhn is fast (13 vars), Leduc is the "
                        "slow part -- start with Kuhn only.",
}


def get_config(name: str = "smoke") -> dict:
    if name not in CONFIGS:
        raise ValueError(f"Unknown config {name!r}; choose from {sorted(CONFIGS)}")
    return dict(CONFIGS[name])  # a shallow copy so callers can tweak freely
