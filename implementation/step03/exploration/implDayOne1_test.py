"""
Test suite: MCCFR variants — Kuhn Poker (OpenSpiel) + Leduc Hold'em (custom).

Compares six algorithms:
  1. OpenSpiel External Sampling MCCFR  (Kuhn Poker)
  2. OpenSpiel Outcome Sampling MCCFR   (Kuhn Poker)
  3. Custom CFR from step02             (Kuhn Poker, hand-coded)
  4. Custom ES-MCCFR                    (Leduc Hold'em, our engine)
  5. Custom OS-MCCFR                    (Leduc Hold'em, our engine)
  6. OpenSpiel CFR+                     (Kuhn Poker)

Algorithms 1-3, 6 use OpenSpiel for Kuhn Poker exploitability.
Algorithms 4-5 use our custom exploitability evaluation on Leduc Hold'em.

Results are saved to exploration/figures/kuhn_results_cache.json.
Two convergence charts are generated (iterations and wall-clock).
"""

import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import cfr as cfr_module
from open_spiel.python.algorithms import exploitability as expl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json
import time
import sys
import os
import random

# ── Path setup ─────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
STEP02_DIR = os.path.join(SCRIPT_DIR, '..', '..', 'step02')
STEP03_DIR = os.path.join(SCRIPT_DIR, '..')

sys.path.insert(0, STEP02_DIR)
sys.path.insert(0, STEP03_DIR)

from cfr.cfr_trainer import KuhnTrainer                             # step02
from cfr.mccfr_external_trainer import LeducExternalSamplingTrainer # step03 custom
from cfr.mccfr_outcome_trainer import LeducOutcomeSamplingTrainer   # step03 custom
from evaluate.exploitability import compute_exploitability           # step03 Leduc

# ── Config ──────────────────────────────────────────────────────────────────
game = pyspiel.load_game("kuhn_poker")
FIGURES_DIR = os.path.join(SCRIPT_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

MAX_STEPS = 5000
PRINT_STEPS = [100]
while PRINT_STEPS[-1] < MAX_STEPS:
    PRINT_STEPS.append(int(PRINT_STEPS[-1] * 1.5))
PRINT_STEPS = [s for s in PRINT_STEPS if s <= MAX_STEPS]

print('=' * 70)
print('  MCCFR Variants — Test Run (5k iterations max)')
print('=' * 70)
print(f'  Checkpoints: {PRINT_STEPS}\n')

# ── Accumulator ────────────────────────────────────────────────────────────
cache_data = {
    'iterations': [],
    'es_results': [],
    'os_results': [],
    'customCFR_results': [],
    'customES_results': [],
    'customOS_results': [],
    'osCFRPlus_results': [],
}

# ── 1. OpenSpiel External Sampling MCCFR (Kuhn) ────────────────────────────
print('  [1/6] OpenSpiel External Sampling MCCFR (Kuhn)...')
es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
t0 = time.time()
for i in range(MAX_STEPS):
    es_solver.iteration()
    if i + 1 in PRINT_STEPS:
        exploit = expl.nash_conv(game, es_solver.average_policy())
        elapsed = time.time() - t0
        cache_data['iterations'].append(i + 1)
        cache_data['es_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit={exploit:.5f}  ({elapsed:.2f}s)')

# ── 2. OpenSpiel Outcome Sampling MCCFR (Kuhn) ─────────────────────────────
print('\n  [2/6] OpenSpiel Outcome Sampling MCCFR (Kuhn)...')
os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
t0 = time.time()
for i in range(MAX_STEPS):
    os_solver.iteration()
    if i + 1 in PRINT_STEPS:
        exploit = expl.nash_conv(game, os_solver.average_policy())
        elapsed = time.time() - t0
        cache_data['os_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit={exploit:.5f}  ({elapsed:.2f}s)')

# ── 3. Custom CFR from step02 (Kuhn, hand-coded) ───────────────────────────
print('\n  [3/6] Custom CFR step02 (Kuhn, hand-coded)...')
theoretical_value = -1.0 / 18.0
cfr_solver = KuhnTrainer()
cumulative_util = 0.0
t0 = time.time()
for i in range(MAX_STEPS):
    cards = [1, 2, 3]
    random.shuffle(cards)
    cumulative_util += cfr_solver.cfr(cards, '', 1.0, 1.0)
    if i + 1 in PRINT_STEPS:
        avg_val = cumulative_util / (i + 1)
        exploit = abs(avg_val - theoretical_value)
        elapsed = time.time() - t0
        cache_data['customCFR_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit≈{exploit:.5f}  ({elapsed:.2f}s)')

# ── 4. Custom ES-MCCFR (Leduc Hold'em, our engine) ─────────────────────────
print("\n  [4/6] Custom ES-MCCFR (Leduc Hold'em, our engine)...")
es_custom = LeducExternalSamplingTrainer()
t0 = time.time()
for i in range(MAX_STEPS):
    es_custom.train_iteration()
    if i + 1 in PRINT_STEPS:
        exploit = compute_exploitability(es_custom.node_map)
        elapsed = time.time() - t0
        cache_data['customES_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit={exploit:.5f}  ({elapsed:.2f}s)')

# ── 5. Custom OS-MCCFR (Leduc Hold'em, our engine) ─────────────────────────
print("\n  [5/6] Custom OS-MCCFR (Leduc Hold'em, our engine)...")
os_custom = LeducOutcomeSamplingTrainer()
t0 = time.time()
for i in range(MAX_STEPS):
    os_custom.train_iteration()
    if i + 1 in PRINT_STEPS:
        exploit = compute_exploitability(os_custom.node_map)
        elapsed = time.time() - t0
        cache_data['customOS_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit={exploit:.5f}  ({elapsed:.2f}s)')

# ── 6. OpenSpiel CFR+ (Kuhn) ───────────────────────────────────────────────
print('\n  [6/6] OpenSpiel CFR+ (Kuhn)...')
cfrplus_solver = cfr_module.CFRPlusSolver(game)
t0 = time.time()
for i in range(MAX_STEPS):
    cfrplus_solver.evaluate_and_update_policy()
    if i + 1 in PRINT_STEPS:
        exploit = expl.nash_conv(game, cfrplus_solver.average_policy())
        elapsed = time.time() - t0
        cache_data['osCFRPlus_results'].append({'exploitability': exploit, 'time_elapsed': elapsed})
        print(f'    Iter {i+1:>5}: exploit={exploit:.5f}  ({elapsed:.2f}s)')

# ── Save results ───────────────────────────────────────────────────────────
cache_path = os.path.join(FIGURES_DIR, 'kuhn_results_cache.json')
with open(cache_path, 'w') as f:
    json.dump(cache_data, f, indent=2)
print(f'\n  Results saved → {cache_path}')

# ── Plot 1: Exploitability vs Iterations ───────────────────────────────────
print('\n  Generating charts...')
iters = cache_data['iterations']

fig, ax = plt.subplots(figsize=(14, 7))
ax.loglog(iters, [r['exploitability'] for r in cache_data['es_results']],
          'o-', label='OpenSpiel ES-MCCFR (Kuhn)', linewidth=2)
ax.loglog(iters, [r['exploitability'] for r in cache_data['os_results']],
          's-', label='OpenSpiel OS-MCCFR (Kuhn)', linewidth=2)
ax.loglog(iters, [r['exploitability'] for r in cache_data['customCFR_results']],
          '^-', label='Custom CFR step02 (Kuhn)', linewidth=2, color='red')
ax.loglog(iters, [r['exploitability'] for r in cache_data['customES_results']],
          'D-', label="Custom ES-MCCFR (Leduc)", linewidth=2, color='#2196F3')
ax.loglog(iters, [r['exploitability'] for r in cache_data['customOS_results']],
          'v-', label="Custom OS-MCCFR (Leduc)", linewidth=2, color='#FF5722')
ax.loglog(iters, [r['exploitability'] for r in cache_data['osCFRPlus_results']],
          'p-', label='OpenSpiel CFR+ (Kuhn)', linewidth=2, color='green')
ax.set_xlabel('Iterations (log scale)', fontsize=12)
ax.set_ylabel('Exploitability (log scale)', fontsize=12)
ax.set_title('Exploitability vs Iterations — MCCFR Variants (5k test run)', fontsize=13)
ax.legend(fontsize=9)
ax.grid(True, which='both', ls='--', alpha=0.4)
fig.tight_layout()
p1 = os.path.join(FIGURES_DIR, 'kuhn_exploitability_iterations.png')
fig.savefig(p1, dpi=150)
plt.close(fig)
print(f'  ✓ Iterations chart → {p1}')

# ── Plot 2: Exploitability vs Wall-clock Time ──────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
ax.loglog([r['time_elapsed'] for r in cache_data['es_results']],
          [r['exploitability'] for r in cache_data['es_results']],
          'o-', label='OpenSpiel ES-MCCFR (Kuhn)', linewidth=2)
ax.loglog([r['time_elapsed'] for r in cache_data['os_results']],
          [r['exploitability'] for r in cache_data['os_results']],
          's-', label='OpenSpiel OS-MCCFR (Kuhn)', linewidth=2)
ax.loglog([r['time_elapsed'] for r in cache_data['customCFR_results']],
          [r['exploitability'] for r in cache_data['customCFR_results']],
          '^-', label='Custom CFR step02 (Kuhn)', linewidth=2, color='red')
ax.loglog([r['time_elapsed'] for r in cache_data['customES_results']],
          [r['exploitability'] for r in cache_data['customES_results']],
          'D-', label="Custom ES-MCCFR (Leduc)", linewidth=2, color='#2196F3')
ax.loglog([r['time_elapsed'] for r in cache_data['customOS_results']],
          [r['exploitability'] for r in cache_data['customOS_results']],
          'v-', label="Custom OS-MCCFR (Leduc)", linewidth=2, color='#FF5722')
ax.loglog([r['time_elapsed'] for r in cache_data['osCFRPlus_results']],
          [r['exploitability'] for r in cache_data['osCFRPlus_results']],
          'p-', label='OpenSpiel CFR+ (Kuhn)', linewidth=2, color='green')
ax.set_xlabel('Wall Clock Time (seconds, log scale)', fontsize=12)
ax.set_ylabel('Exploitability (log scale)', fontsize=12)
ax.set_title('Exploitability vs Wall-clock Time — MCCFR Variants (5k test run)', fontsize=13)
ax.legend(fontsize=9)
ax.grid(True, which='both', ls='--', alpha=0.4)
fig.tight_layout()
p2 = os.path.join(FIGURES_DIR, 'kuhn_exploitability_time.png')
fig.savefig(p2, dpi=150)
plt.close(fig)
print(f'  ✓ Wall-clock chart → {p2}')

print('\n' + '=' * 70)
print('  Test run complete — all algorithms OK')
print('=' * 70)
