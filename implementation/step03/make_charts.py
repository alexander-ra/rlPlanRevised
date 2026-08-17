"""
Generate convergence charts from saved algorithm result JSONs.

Usage:
    cd implementation/step03
    python make_charts.py
    python make_charts.py --results-dir results --figures-dir figures

Reads results/es_results.json and results/os_results.json produced by
run_es.py and run_os.py, then generates:
  - figures/convergence_iterations.png
  - figures/convergence_wallclock.png

Separating data collection (run_*.py) from chart generation (make_charts.py)
lets you re-style charts without rerunning expensive training.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RESULTS_FILES = {
    'es': 'results/es_results.json',
    'os': 'results/os_results.json',
}
FIGURES_DIR = 'figures'

ALGORITHM_STYLES = {
    'External Sampling MCCFR': {
        'color': '#2196F3', 'marker': 'o', 'linestyle': '-',
        'label': 'ES-MCCFR (custom, Leduc)',
    },
    'Outcome Sampling MCCFR': {
        'color': '#FF5722', 'marker': 's', 'linestyle': '-',
        'label': 'OS-MCCFR (custom, Leduc)',
    },
}


def load_results(results_files: dict) -> list:
    all_results = []
    for key, path in results_files.items():
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            all_results.append(data)
            print(f"  Loaded: {path}  ({data['algorithm']}, "
                  f"{len(data['iterations'])} checkpoints)")
        else:
            print(f"  Warning: {path} not found — run run_{key}.py first")
    return all_results


def make_charts(all_results: list, figures_dir: str) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

    os.makedirs(figures_dir, exist_ok=True)

    # Chart 1: Exploitability vs Iterations
    fig, ax = plt.subplots(figsize=(10, 6))
    added_ref = False
    for res in all_results:
        algo = res['algorithm']
        style = ALGORITHM_STYLES.get(algo, {
            'color': 'gray', 'marker': '^', 'linestyle': '-', 'label': algo,
        })
        x = res['iterations']
        y = res['exploitability']
        ax.loglog(x, y, color=style['color'], marker=style['marker'],
                  linestyle=style['linestyle'], linewidth=2, markersize=6,
                  label=style['label'])
        if not added_ref and len(x) >= 2:
            c = y[0] * (x[0] ** 0.5)
            ref_x = np.array(x)
            ref_y = c / np.sqrt(ref_x)
            ax.loglog(ref_x, ref_y, 'k--', linewidth=1, alpha=0.4,
                      label=r'$O(1/\sqrt{T})$ reference')
            added_ref = True

    ax.set_xlabel('MCCFR Iterations', fontsize=12)
    ax.set_ylabel('Exploitability', fontsize=12)
    ax.set_title("Leduc Hold'em — Exploitability vs Iterations (log-log)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    p1 = os.path.join(figures_dir, 'convergence_iterations.png')
    fig.savefig(p1, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved → {p1}")

    # Chart 2: Exploitability vs Wall-clock Time
    fig, ax = plt.subplots(figsize=(10, 6))
    for res in all_results:
        algo = res['algorithm']
        style = ALGORITHM_STYLES.get(algo, {
            'color': 'gray', 'marker': '^', 'linestyle': '-', 'label': algo,
        })
        x = res['wallclock_seconds']
        y = res['exploitability']
        ax.loglog(x, y, color=style['color'], marker=style['marker'],
                  linestyle=style['linestyle'], linewidth=2, markersize=6,
                  label=style['label'])

    ax.set_xlabel('Wall-clock Time (seconds)', fontsize=12)
    ax.set_ylabel('Exploitability', fontsize=12)
    ax.set_title("Leduc Hold'em — Exploitability vs Wall-clock Time (log-log)",
                 fontsize=13, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, which='both', alpha=0.3)
    fig.tight_layout()
    p2 = os.path.join(figures_dir, 'convergence_wallclock.png')
    fig.savefig(p2, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved → {p2}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate MCCFR convergence charts from saved JSON results')
    parser.add_argument('--results-dir', default='results')
    parser.add_argument('--figures-dir', default=FIGURES_DIR)
    args = parser.parse_args()

    results_files = {
        k: os.path.join(args.results_dir, os.path.basename(v))
        for k, v in RESULTS_FILES.items()
    }

    print('\n  Loading results...')
    all_results = load_results(results_files)

    if not all_results:
        print('\n  No result files found. Run run_es.py and/or run_os.py first.')
        return

    print(f'\n  Generating charts → {args.figures_dir}/')
    make_charts(all_results, args.figures_dir)
    print(f'\n  Done — {len(all_results)} algorithm(s) plotted.\n')


if __name__ == '__main__':
    main()
