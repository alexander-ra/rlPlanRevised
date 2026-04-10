import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import exploitability as expl
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import json
import time
import sys
import os

# Add step02 to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'step02'))
from cfr.cfr_trainer import KuhnTrainer

game = pyspiel.load_game("kuhn_poker")
relativePath = "exploration/figures/";

# Cache for results with timing
cache_data = {'iterations': [], 'es_results': [], 'os_results': [], 'customCRF_results': []}

#check if we have cached results to avoid rerunning everything
try:    
    with open(relativePath + 'mccfr_results_cache.json', 'r') as f:
        cache_data = json.load(f)
    print(f"Loaded cached results from '{relativePath}mccfr_results_cache.json'.")
except FileNotFoundError:
    print("No cache found, running MCCFR algorithms...")

if 'cache_data' not in locals():
    #  print exploitability after 100 and each time its *1.5 for up to 100k
    printSteps = [100]
    while printSteps[-1] < 100000:
        printSteps.append(int(printSteps[-1] * 1.5))

    # Cache for results with timing
    cache_data = {'iterations': [], 'es_results': [], 'os_results': []}

    # External sampling MCCFR
    print("Running External Sampling MCCFR...")
    es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
    es_start_time = time.time()
    for i in range(100000):
        es_solver.iteration()
        if i + 1 in printSteps:
            es_policy = es_solver.average_policy()
            es_exploit = expl.nash_conv(game, es_policy)
            elapsed = time.time() - es_start_time
            cache_data['iterations'].append(i + 1)
            cache_data['es_results'].append({'exploitability': es_exploit, 'time_elapsed': elapsed})
            print(f"External Sampling - Iteration {i+1}: Exploitability = {es_exploit:.6f} (Time: {elapsed:.2f}s)")

    # Outcome sampling MCCFR
    print("\nRunning Outcome Sampling MCCFR...")
    os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
    os_start_time = time.time()
    for i in range(100000):
        os_solver.iteration()
        if i + 1 in printSteps:
            os_policy = os_solver.average_policy()
            os_exploit = expl.nash_conv(game, os_policy)
            elapsed = time.time() - os_start_time
            cache_data['os_results'].append({'exploitability': os_exploit, 'time_elapsed': elapsed})
            print(f"Outcome Sampling - Iteration {i+1}: Exploitability = {os_exploit:.6f} (Time: {elapsed:.2f}s)")

    # custom crf from step02
    print("\nTraining Custom CFR (100k iterations)...")
    
    # Print steps at same intervals as others
    printSteps = [100]
    while printSteps[-1] < 100000:
        printSteps.append(int(printSteps[-1] * 1.5))
    
    # Theoretical value for Kuhn Poker
    theoretical_value = -1.0 / 18.0  # ≈ -0.0556
    
    cfr_start_time = time.time()
    cfr_solver = KuhnTrainer()
    cumulative_util = 0.0
    import random
    
    for i in range(100000):
        cards = [1, 2, 3]
        random.shuffle(cards)
        cumulative_util += cfr_solver.cfr(cards, "", 1.0, 1.0)
        
        if i + 1 in printSteps:
            avg_game_value = cumulative_util / (i + 1)
            cfr_exploit = abs(avg_game_value - theoretical_value)
            elapsed = time.time() - cfr_start_time
            cache_data['customCRF_results'].append({'exploitability': cfr_exploit, 'time_elapsed': elapsed})
            print(f"Custom CFR - Iteration {i+1}: Exploitability = {cfr_exploit:.6f} (Time: {elapsed:.2f}s)")
    
    # Save cache to JSON
    with open(relativePath + 'mccfr_results_cache.json', 'w') as f:
        json.dump(cache_data, f, indent=2)
    print(f"\nResults cached to '{relativePath}mccfr_results_cache.json'.")
else:
    print("Using cached results for plotting.")

# Extract exploitabilities for plotting (ensure same length)
es_exploits = [r['exploitability'] for r in cache_data['es_results']]
os_exploits = [r['exploitability'] for r in cache_data['os_results']]
cfr_exploits = [r['exploitability'] for r in cache_data.get('customCRF_results', [])]
iterations = cache_data['iterations']

# Ensure all lists have same length
min_len = min(len(iterations), len(es_exploits), len(os_exploits), len(cfr_exploits) if cfr_exploits else float('inf'))
iterations = iterations[:min_len]
es_exploits = es_exploits[:min_len]
os_exploits = os_exploits[:min_len]
cfr_exploits = cfr_exploits[:min_len] if cfr_exploits else []

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(iterations, es_exploits, label='External Sampling MCCFR', marker='o', linewidth=2)
plt.plot(iterations, os_exploits, label='Outcome Sampling MCCFR', marker='s', linewidth=2)
if cfr_exploits:
    plt.plot(iterations, cfr_exploits, label='Custom CFR (Hand-coded)', marker='^', linewidth=2, color='red')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Iterations (log scale)')
plt.ylabel('Exploitability (log scale)')
plt.title('Exploitability vs Iterations: MCCFR Variants vs Custom CFR')
plt.legend(fontsize=10)
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig(relativePath + 'mccfr_exploitability_comparison.png', dpi=150)
print(f"Figure saved as '{relativePath}mccfr_exploitability_comparison.png'")

# New plot vs wall clock time
es_times = [r['time_elapsed'] for r in cache_data['es_results']]
os_times = [r['time_elapsed'] for r in cache_data['os_results']]
cfr_times = [r['time_elapsed'] for r in cache_data.get('customCRF_results', [])]

plt.figure(figsize=(12, 6))
plt.plot(es_times, es_exploits, label='External Sampling MCCFR', marker='o', linewidth=2)
plt.plot(os_times, os_exploits, label='Outcome Sampling MCCFR', marker='s', linewidth=2)
if cfr_exploits:
    plt.plot(cfr_times, cfr_exploits, label='Custom CFR (Hand-coded)', marker='^', linewidth=2, color='red')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Wall Clock Time (seconds, log scale)')
plt.ylabel('Exploitability (log scale)')
plt.title('Exploitability vs Wall Clock Time: MCCFR Variants vs Custom CFR')
plt.legend(fontsize=10)
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plt.savefig(relativePath + 'mccfr_exploitability_time_comparison.png', dpi=150)
print(f"Figure saved as '{relativePath}mccfr_exploitability_time_comparison.png'")

