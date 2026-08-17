"""
Train External Sampling MCCFR on Leduc Hold'em and save results.

Usage:
    cd implementation/step03
    python run_es.py
    python run_es.py --iterations 50000 --seed 42

Results are saved to results/es_results.json.
Run make_charts.py afterwards to regenerate comparison charts.
"""

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cfr.mccfr_external_trainer import LeducExternalSamplingTrainer
from evaluate.exploitability import compute_exploitability
from config import CFR_CONFIG

CHECKPOINTS = [100, 300, 600, 1_000, 2_000, 5_000, 10_000]


def run(iterations: int = 10_000, seed: int = 42,
        checkpoints: list = None, verbose: bool = True) -> dict:
    if seed is not None:
        random.seed(seed)
    if checkpoints is None:
        checkpoints = [c for c in CHECKPOINTS if c <= iterations]
        if iterations not in checkpoints:
            checkpoints.append(iterations)

    trainer = LeducExternalSamplingTrainer()
    results = {
        'algorithm': 'External Sampling MCCFR',
        'game': "Leduc Hold'em",
        'iterations': [],
        'exploitability': [],
        'wallclock_seconds': [],
        'config': {'num_iterations': iterations, 'seed': seed},
    }

    checkpoint_set = set(checkpoints)
    t0 = time.time()
    for i in range(1, iterations + 1):
        trainer.train_iteration()
        if i in checkpoint_set:
            exploit = compute_exploitability(trainer.node_map)
            elapsed = time.time() - t0
            results['iterations'].append(i)
            results['exploitability'].append(exploit)
            results['wallclock_seconds'].append(elapsed)
            if verbose:
                print(f"  iter={i:>7,}  exploit={exploit:.5f}  ({elapsed:.1f}s)")

    return results


def main():
    parser = argparse.ArgumentParser(description='Train ES-MCCFR on Leduc Hold\'em')
    parser.add_argument('--iterations', type=int, default=10_000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    print('\n' + '=' * 55)
    print('  Leduc Hold\'em — External Sampling MCCFR')
    print('=' * 55)
    print(f'  iterations={args.iterations:,}  seed={args.seed}')
    print()

    results = run(iterations=args.iterations, seed=args.seed)

    os.makedirs('results', exist_ok=True)
    out = 'results/es_results.json'
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\n  Saved → {out}')
    print(f'  Final exploit = {results["exploitability"][-1]:.5f}')
    print()


if __name__ == '__main__':
    main()
