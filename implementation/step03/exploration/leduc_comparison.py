"""
Leduc Poker comparison: MCCFR variants and OpenSpiel's CFR/CFR+ implementations.
Similar to Kuhn poker test but for the larger Leduc poker game.
No custom CFR implementation (would be too complex for Leduc).
"""
import pyspiel
from open_spiel.python.algorithms import external_sampling_mccfr
from open_spiel.python.algorithms import outcome_sampling_mccfr
from open_spiel.python.algorithms import cfr as cfr_module
from open_spiel.python.algorithms import exploitability as expl
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import json
import time

game = pyspiel.load_game("leduc_poker")
relativePath = "exploration/figures/"

# Cache for results with timing
cache_data = {'iterations': [], 'es_results': [], 'os_results': [], 'osCFR_results': [], 'osCFRPlus_results': []}
maxSteps = 5000  # Reduced for faster testing

# Print steps: 100, iterations *1.5 until maxSteps
printSteps = [100]
while printSteps[-1] < maxSteps:
    printSteps.append(int(printSteps[-1] * 1.5))
printSteps = [s for s in printSteps if s <= maxSteps]

print("=" * 60)
print("LEDUC POKER COMPARISON - 5k iterations max")
print("=" * 60)
print(f"Print steps: {printSteps}\n")

# External sampling MCCFR
print("Running External Sampling MCCFR (5k iterations)...")
es_solver = external_sampling_mccfr.ExternalSamplingSolver(game)
es_start_time = time.time()
for i in range(maxSteps):
    es_solver.iteration()
    if i + 1 in printSteps:
        es_policy = es_solver.average_policy()
        es_exploit = expl.nash_conv(game, es_policy)
        elapsed = time.time() - es_start_time
        cache_data['iterations'].append(i + 1)
        cache_data['es_results'].append({'exploitability': es_exploit, 'time_elapsed': elapsed})
        print(f"  ES - Iteration {i+1:>5}: Exploit = {es_exploit:.6f} (Time: {elapsed:6.2f}s)")

# Outcome sampling MCCFR
print("\nRunning Outcome Sampling MCCFR (5k iterations)...")
os_solver = outcome_sampling_mccfr.OutcomeSamplingSolver(game)
os_start_time = time.time()
for i in range(maxSteps):
    os_solver.iteration()
    if i + 1 in printSteps:
        os_policy = os_solver.average_policy()
        os_exploit = expl.nash_conv(game, os_policy)
        elapsed = time.time() - os_start_time
        cache_data['os_results'].append({'exploitability': os_exploit, 'time_elapsed': elapsed})
        print(f"  OS - Iteration {i+1:>5}: Exploit = {os_exploit:.6f} (Time: {elapsed:6.2f}s)")

# OpenSpiel CFR
print("\nTraining OpenSpiel CFR (5k iterations)...")
os_cfr_solver = cfr_module.CFRSolver(game)
os_cfr_start_time = time.time()
for i in range(maxSteps):
    os_cfr_solver.evaluate_and_update_policy()
    if i + 1 in printSteps:
        os_cfr_policy = os_cfr_solver.average_policy()
        os_cfr_exploit = expl.nash_conv(game, os_cfr_policy)
        elapsed = time.time() - os_cfr_start_time
        cache_data['osCFR_results'].append({'exploitability': os_cfr_exploit, 'time_elapsed': elapsed})
        print(f"  OS-CFR - Iteration {i+1:>5}: Exploit = {os_cfr_exploit:.6f} (Time: {elapsed:6.2f}s)")

# OpenSpiel CFR+
print("\nTraining OpenSpiel CFR+ (5k iterations)...")
os_cfrplus_solver = cfr_module.CFRPlusSolver(game)
os_cfrplus_start_time = time.time()
for i in range(maxSteps):
    os_cfrplus_solver.evaluate_and_update_policy()
    if i + 1 in printSteps:
        os_cfrplus_policy = os_cfrplus_solver.average_policy()
        os_cfrplus_exploit = expl.nash_conv(game, os_cfrplus_policy)
        elapsed = time.time() - os_cfrplus_start_time
        cache_data['osCFRPlus_results'].append({'exploitability': os_cfrplus_exploit, 'time_elapsed': elapsed})
        print(f"  OS-CFR+ - Iteration {i+1:>5}: Exploit = {os_cfrplus_exploit:.6f} (Time: {elapsed:6.2f}s)")

# Save cache
cache_path = relativePath + 'leduc_results_cache.json'
with open(cache_path, 'w') as f:
    json.dump(cache_data, f, indent=2)
print(f"\nResults cached to '{cache_path}'")

# Extract exploitabilities
es_exploits = [r['exploitability'] for r in cache_data['es_results']]
os_exploits = [r['exploitability'] for r in cache_data['os_results']]
oscfr_exploits = [r['exploitability'] for r in cache_data.get('osCFR_results', [])]
oscfrplus_exploits = [r['exploitability'] for r in cache_data.get('osCFRPlus_results', [])]
iterations = cache_data['iterations']

print(f"\nData lengths: iterations={len(iterations)}, ES={len(es_exploits)}, OS={len(os_exploits)}, OS-CFR={len(oscfr_exploits)}, OS-CFR+={len(oscfrplus_exploits)}")

# Plot 1: Iterations
print("\nCreating iteration plot...")
plt.figure(figsize=(14, 7))
plt.plot(iterations, es_exploits, label='External Sampling MCCFR', marker='o', linewidth=2)
plt.plot(iterations, os_exploits, label='Outcome Sampling MCCFR', marker='s', linewidth=2)
if oscfr_exploits:
    plt.plot(iterations, oscfr_exploits, label='OpenSpiel CFR', marker='D', linewidth=2, color='green')
if oscfrplus_exploits:
    plt.plot(iterations, oscfrplus_exploits, label='OpenSpiel CFR+', marker='v', linewidth=2, color='purple')
plt.xscale('log')
plt.yscale('log')
all_iters = iterations
all_exploits_iter = es_exploits + os_exploits + oscfr_exploits + oscfrplus_exploits
if all_iters and all_exploits_iter:
    min_iter = min([i for i in all_iters if i > 0] or [1])
    max_iter = max(all_iters)
    min_expl_iter = min([e for e in all_exploits_iter if e > 0] or [1e-6])
    max_expl_iter = max(all_exploits_iter)
    plt.xlim([min_iter * 0.8, max_iter * 1.2])
    plt.ylim([min_expl_iter * 0.8, max_expl_iter * 1.2])

plt.xlabel('Iterations (log scale)')
plt.ylabel('Exploitability (log scale)')
plt.title('Exploitability vs Iterations: Leduc Poker - All Algorithms')
plt.legend(fontsize=10)
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plot1_path = relativePath + 'leduc_exploitability_iterations.png'
plt.savefig(plot1_path, dpi=150)
print(f"✓ Plot saved: {plot1_path}")
plt.close()

# Plot 2: Wall clock time
print("Creating wall clock time plot...")
es_times = [r['time_elapsed'] for r in cache_data['es_results']]
os_times = [r['time_elapsed'] for r in cache_data['os_results']]
oscfr_times = [r['time_elapsed'] for r in cache_data.get('osCFR_results', [])]
oscfrplus_times = [r['time_elapsed'] for r in cache_data.get('osCFRPlus_results', [])]

plt.figure(figsize=(14, 7))
plt.plot(es_times, es_exploits, label='External Sampling MCCFR', marker='o', linewidth=2)
plt.plot(os_times, os_exploits, label='Outcome Sampling MCCFR', marker='s', linewidth=2)
if oscfr_exploits:
    plt.plot(oscfr_times, oscfr_exploits, label='OpenSpiel CFR', marker='D', linewidth=2, color='green')
if oscfrplus_exploits:
    plt.plot(oscfrplus_times, oscfrplus_exploits, label='OpenSpiel CFR+', marker='v', linewidth=2, color='purple')
plt.xscale('log')
plt.yscale('log')

# Dynamic axis limits for all methods (wall clock time plot)
all_times = es_times + os_times + oscfr_times + oscfrplus_times
all_exploits = es_exploits + os_exploits + oscfr_exploits + oscfrplus_exploits
if all_times and all_exploits:
    min_time = min([t for t in all_times if t > 0] or [1e-3])
    max_time = max(all_times)
    min_expl = min([e for e in all_exploits if e > 0] or [1e-6])
    max_expl = max(all_exploits)
    plt.xlim([min_time * 0.8, max_time * 1.2])
    plt.ylim([min_expl * 0.8, max_expl * 1.2])

plt.xlabel('Wall Clock Time (seconds, log scale)')
plt.ylabel('Exploitability (log scale)')
plt.title('Exploitability vs Wall Clock Time: Leduc Poker - All Algorithms')
plt.legend(fontsize=10)
plt.grid(True, which="both", ls="--")
plt.tight_layout()
plot2_path = relativePath + 'leduc_exploitability_time.png'
plt.savefig(plot2_path, dpi=150)
print(f"✓ Plot saved: {plot2_path}")
plt.close()

print("\n" + "=" * 60)
print("LEDUC POKER RUN (5k iterations) COMPLETE - All systems OK!")
print("=" * 60)
