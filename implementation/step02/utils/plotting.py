"""Visualization utilities for Kuhn Poker CFR results.

Plot-only mode (no training): redraw every figure from the saved results,

    cd implementation/step02
    python utils/plotting.py

reads models/cfr_results.json (written by cfr/train.py) and
models/convergence.json (written by evaluate/convergence.py) and writes the
three PNGs into deliverables/reports/step02/summary/ and .../step02/figures/.
scripts/figures/render_bg_figures.py runs this same entry point to produce the
Bulgarian twins (*_bg.png).
"""

import locale
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

_STEP02_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _STEP02_DIR not in sys.path:
    sys.path.insert(0, _STEP02_DIR)

from cfr.kuhn_poker import PASS, BET, CARD_NAMES  # noqa: E402

# Printed at ~17.6 cm (6.9 in) wide, a figure saved ~8 in wide is scaled by
# ~0.87, so 10 pt prints at ~8.7 pt and 9.6 pt at ~8.4 pt (floor: 8.2 pt).
FS = 10
FS_SMALL = 9.6
DPI = 300


def _num(value: float, fmt: str = '%.2f') -> str:
    """Format a number with the active LC_NUMERIC (decimal comma in BG runs)."""
    return locale.format_string(fmt, value)


def create_convergence_chart(trainer, figures_dir: str):
    """Plot the running mean of the sampled payoffs against -1/18."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(trainer.iteration_history, trainer.game_value_history,
            color='#2196F3', linewidth=1.5,
            label='Running mean of sampled payoffs')
    ax.axhline(y=-1/18, color='#F44336', linestyle='--', linewidth=1.5,
               label=f'Theoretical value (-1/18 ≈ {-1/18:.4f})')
    ax.set_xlabel('Training Iterations', fontsize=FS)
    ax.set_ylabel('Payoff to Player 0 (running mean)', fontsize=FS)
    ax.tick_params(labelsize=FS)
    ax.legend(loc='lower right', fontsize=FS)
    ax.grid(True, alpha=0.3)

    path = os.path.join(figures_dir, 'game_value_convergence.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


def _bar_chart(ax, info_sets, labels, trainer, title, xlabel,
               pass_label='Pass', bet_label='Bet'):
    """Helper for strategy bar charts."""
    p_pass, p_bet = [], []
    for info in info_sets:
        if info in trainer.node_map:
            avg = trainer.node_map[info].get_average_strategy()
            p_pass.append(avg[PASS])
            p_bet.append(avg[BET])
        else:
            p_pass.append(0)
            p_bet.append(0)

    x = range(len(labels))
    bars1 = ax.bar([i - 0.18 for i in x], p_pass, 0.35,
                   label=pass_label, color='#66BB6A', edgecolor='white')
    bars2 = ax.bar([i + 0.18 for i in x], p_bet, 0.35,
                   label=bet_label, color='#EF5350', edgecolor='white')

    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            if h > 0.02:
                ax.text(bar.get_x() + bar.get_width()/2., h + 0.02,
                        _num(h), ha='center', va='bottom', fontsize=FS_SMALL)

    ax.set_xlabel(xlabel, fontsize=FS)
    ax.set_ylabel('Probability', fontsize=FS)
    ax.set_title(title, fontsize=10.5)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.tick_params(labelsize=FS)
    ax.set_ylim(0, 1.3)
    # compact spacing: the Bulgarian labels ("Плащане (залог)") are ~40 % longer
    ax.legend(fontsize=FS_SMALL, loc='upper center', ncol=2, handlelength=1.2,
              handletextpad=0.5, columnspacing=1.0)
    ax.grid(True, alpha=0.3, axis='y')


def create_strategy_charts(trainer, figures_dir: str):
    """Create the 4-panel strategy visualization (players numbered 0 and 1)."""
    fig = plt.figure(figsize=(8, 6.6))
    gs = gridspec.GridSpec(2, 2, hspace=0.55, wspace=0.35,
                           top=0.95, bottom=0.08, left=0.09, right=0.98)

    card_labels = ['J', 'Q', 'K']

    # Player 0: opening action
    ax1 = fig.add_subplot(gs[0, 0])
    _bar_chart(ax1, ['1', '2', '3'], card_labels, trainer,
               'Player 0: opening action', 'Player 0 card')

    # Player 1: response to pass
    ax2 = fig.add_subplot(gs[0, 1])
    _bar_chart(ax2, ['1p', '2p', '3p'], card_labels, trainer,
               'Player 1: response to a pass', 'Player 1 card')

    # Player 1: response to bet (fold vs call)
    ax3 = fig.add_subplot(gs[1, 0])
    _bar_chart(ax3, ['1b', '2b', '3b'], card_labels, trainer,
               'Player 1: response to a bet', 'Player 1 card',
               pass_label='Fold (pass)', bet_label='Call (bet)')

    # Player 0: facing bet after passing
    ax4 = fig.add_subplot(gs[1, 1])
    _bar_chart(ax4, ['1pb', '2pb', '3pb'], card_labels, trainer,
               'Player 0: facing a bet after passing', 'Player 0 card',
               pass_label='Fold (pass)', bet_label='Call (bet)')

    path = os.path.join(figures_dir, 'strategy_analysis.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


def create_exploitability_chart(checkpoints, exploitabilities, figures_dir: str,
                                lo=None, hi=None):
    """Log-log plot of exploitability vs iterations.

    exploitabilities: one value per checkpoint (the mean over seeds when lo/hi
    are given); lo/hi: optional per-checkpoint min and max over the seeds.
    """
    import numpy as np

    fig, ax = plt.subplots(figsize=(8, 4.6))
    band = lo is not None and hi is not None
    if band:
        ax.fill_between(checkpoints, lo, hi, color='#1f77b4', alpha=0.18,
                        linewidth=0, label='Range over seeds (min–max)')
    ax.loglog(checkpoints, exploitabilities, 'bo-', linewidth=2, markersize=6,
              label='Mean exploitability over seeds' if band
              else 'Measured exploitability')

    # Reference O(1/√T) line: slope fixed at -1/2, intercept fitted to all
    # points in log space (not anchored to the first point alone).
    if len(checkpoints) >= 2:
        x = np.array(checkpoints, dtype=float)
        y = np.array(exploitabilities, dtype=float)
        c = np.exp(np.mean(np.log(y) + 0.5 * np.log(x)))
        ax.loglog(x, c / np.sqrt(x), 'r--', linewidth=1.5,
                  label=r'$O(1/\sqrt{T})$ reference')

    ax.set_xlabel('CFR Iterations', fontsize=FS)
    ax.set_ylabel('Exploitability', fontsize=FS)
    ax.tick_params(labelsize=FS)
    ax.legend(fontsize=FS)
    ax.grid(True, alpha=0.3, which='both')

    path = os.path.join(figures_dir, 'exploitability_convergence.png')
    fig.savefig(path, dpi=DPI, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


if __name__ == "__main__":
    # Plot-only mode: read the saved results, never train or rewrite them.
    import json
    import types

    here = os.path.dirname(os.path.abspath(__file__))
    models = os.path.join(here, "..", "models")
    step_dir = os.path.join(here, "..", "..", "..",
                            "deliverables", "reports", "step02")
    out_dirs = [os.path.join(step_dir, "summary"),
                os.path.join(step_dir, "figures")]

    with open(os.path.join(models, "cfr_results.json")) as f:
        res = json.load(f)

    class _Avg:
        def __init__(self, row):
            self.row = row

        def get_average_strategy(self):
            return [self.row["p_pass"], self.row["p_bet"]]

    stub = types.SimpleNamespace(
        node_map={k: _Avg(v) for k, v in res["strategies"].items()},
        iteration_history=res.get("iteration_history", []),
        game_value_history=res.get("game_value_history", []))

    conv_path = os.path.join(models, "convergence.json")
    conv = None
    if os.path.exists(conv_path):
        with open(conv_path) as f:
            conv = json.load(f)

    for out in out_dirs:
        os.makedirs(out, exist_ok=True)
        create_strategy_charts(stub, out)
        if stub.iteration_history:
            create_convergence_chart(stub, out)
        if conv is not None:
            create_exploitability_chart(conv["checkpoints"],
                                        conv["exploitabilities"], out,
                                        lo=conv.get("min"), hi=conv.get("max"))
