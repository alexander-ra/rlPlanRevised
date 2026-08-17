"""
Train Outcome Sampling MCCFR on Leduc Hold'em and save results.

Usage:
    cd implementation/step03
    python run_os.py
    python run_os.py --iterations 50000 --seed 42 --exploration 0.6

Results are saved to results/os_results.json.
Run make_charts.py afterwards to regenerate comparison charts.
"""

import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cfr.mccfr_outcome_trainer import LeducOutcomeSamplingTrainer, DEFAULT_EPSILON
from evaluate.exploitability import compute_exploitability

CHECKPOINTS = [100, 300, 600, 1_000, 2_000, 5_000, 10_000]


def run(iterations: int = 10_000, seed: int = 42, exploration: float = DEFAULT_EPSILON,
        checkpoints: list = None, verbose: bool = True) -> dict:
    if seed is not None:
        random.seed(seed)
    if checkpoints is None:
        checkpoints = [c for c in CHECKPOINTS if c <= iterations]
        if iterations not in checkpoints:
            checkpoints.append(iterations)

    trainer = LeducOutcomeSamplingTrainer(epsilon=exploration)
    results = {
        'algorithm': 'Outcome Sampling MCCFR',
        'game': "Leduc Hold'em",
        'iterations': [],
        'exploitability': [],
        'wallclock_seconds': [],
        'config': {'num_iterations': iterations, 'seed': seed, 'exploration': exploration},
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
    parser = argparse.ArgumentParser(description='Train OS-MCCFR on Leduc Hold\'em')
    parser.add_argument('--iterations', type=int, default=10_000)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--exploration', type=float, default=DEFAULT_EPSILON)
    args = parser.parse_args()

    print('\n' + '=' * 55)
    print('  Leduc Hold\'em — Outcome Sampling MCCFR')
    print('=' * 55)
    print(f'  iterations={args.iterations:,}  seed={args.seed}  eps={args.exploration}')
    print()

    results = run(iterations=args.iterations, seed=args.seed, exploration=args.exploration)

    os.makedirs('results', exist_ok=True)
    out = 'results/os_results.json'
    with open(out, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'\n  Saved → {out}')
    print(f'  Final exploit = {results["exploitability"][-1]:.5f}')
    print()


if __name__ == '__main__':
    main()
