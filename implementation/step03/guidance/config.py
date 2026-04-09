"""
Configuration parameters for Step 03: MCCFR Variants

This module centralizes hyperparameters and settings for external sampling
and outcome sampling MCCFR on Kuhn Poker.
"""

# ─────────────────────────────────────────────────────────────
# MCCFR Training Parameters
# ─────────────────────────────────────────────────────────────

# Number of iterations (samples) for convergence
# Typical: 10k for quick exploration, 100k for detailed convergence study
NUM_ITERATIONS = 10000

# Logging interval: log exploitability every N iterations
LOG_INTERVAL = 1000

# Convergence checkpoint: store full policy every N iterations
# (for convergence analysis and strategy extraction)
CHECKPOINT_INTERVAL = 1000

# Random seed for reproducibility
RANDOM_SEED = 42

# ─────────────────────────────────────────────────────────────
# MCCFR Variant-Specific Settings
# ─────────────────────────────────────────────────────────────

# External Sampling MCCFR
EXTERNAL_SAMPLING = {
    'name': 'External Sampling MCCFR',
    'averaging_type': 'SIMPLE',  # SIMPLE or FULL
    # SIMPLE: updates opponent average policy on opponent nodes (faster)
    # FULL:   separate pass for full averaging (more unbiased for n>2)
    'description': 'Sample chance nodes; deterministic agent traversal'
}

# Outcome Sampling MCCFR
OUTCOME_SAMPLING = {
    'name': 'Outcome Sampling MCCFR',
    'exploration_factor': 0.6,  # Mix exploration with current policy
    # Exploration: exploration_factor * uniform + (1-exploration_factor) * policy
    'description': 'Sample all nodes from current policy'
}

# ─────────────────────────────────────────────────────────────
# Game Configuration
# ─────────────────────────────────────────────────────────────

GAME_NAME = 'kuhn_poker'

# Kuhn poker structure
KUHN_STRUCTURE = {
    'num_players': 2,
    'cards': [1, 2, 3],  # Jack, Queen, King
    'actions': ['p', 'b'],  # Pass, Bet (use pass to mean fold or check)
    'num_info_sets_per_player': 12,
    'max_history_length': 4,  # Max action sequence
}

# Nash equilibrium targets (for reference)
NASH_TARGETS = {
    'p1_jack_bluff_prob': 1/3,     # Bet with Jack ≈ 1/3
    'p1_queen_check_prob': 1.0,    # Check with Queen (fold to bet)
    'p1_king_bet_prob': 1.0,       # Always bet with King
    'p1_equilibrium_value': -1/18,  # Expected value for P1 at equilibrium
    'exploitability_target': 0.0,   # Perfect equilibrium = zero exploitability
}

# ─────────────────────────────────────────────────────────────
# Analysis Parameters
# ─────────────────────────────────────────────────────────────

# Variance analysis (analyze_mccfr.py)
VARIANCE_ANALYSIS = {
    'num_independent_runs': 5,
    'iterations_per_run': 5000,
    'seed_base': 42,  # Seeds: 42, 43, 44, ...
}

# Convergence analysis
CONVERGENCE_ANALYSIS = {
    'plot_log_log': True,           # Plot log(exploitability) vs log(iterations)
    'expected_slope': -0.5,         # Theoretical O(1/√T) = slope -0.5
    'slope_tolerance': 0.1,         # Allow ±0.1 deviation from theory
}

# ─────────────────────────────────────────────────────────────
# Output & Logging
# ─────────────────────────────────────────────────────────────

OUTPUT_DIR = 'implementation/step03'

# Results files
RESULTS_FILES = {
    'main_comparison': 'mccfr_comparison_results.json',
    'detailed_analysis': 'mccfr_detailed_analysis.json',
    'strategy_comparison': 'strategy_comparison.json',
    'convergence_plot_data': 'convergence_data.json',
}

# ─────────────────────────────────────────────────────────────
# Experimental Design
# ─────────────────────────────────────────────────────────────

# Extended experiments (for future use)
EXTENDED_EXPERIMENTS = {
    'large_scale_convergence': {
        'num_iterations': 100000,
        'log_interval': 5000,
        'enabled': False,  # Turn on for detailed convergence study
    },
    'variance_stability_test': {
        'num_runs': 20,
        'iterations': 10000,
        'enabled': False,  # Turn on for statistical significance
    },
    'strategy_evolution_tracking': {
        'track_individual_infosets': False,
        'checkpoint_every_n_iters': 100,
    }
}

# ─────────────────────────────────────────────────────────────
# Reproducibility & Debugging
# ─────────────────────────────────────────────────────────────

VERBOSE_LOGGING = True
SAVE_INTERMEDIATE_POLICIES = False  # Save policy snapshots during training
DEBUG_MODE = False  # Print detailed trace information
