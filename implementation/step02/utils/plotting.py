"""Visualization utilities for Kuhn Poker CFR results."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from cfr.kuhn_poker import PASS, BET, CARD_NAMES

import os


def create_convergence_chart(trainer, figures_dir: str):
    """Plot game value convergence to theoretical -1/18."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(trainer.iteration_history, trainer.game_value_history,
            color='#2196F3', linewidth=1.5, label='Computed game value')
    ax.axhline(y=-1/18, color='#F44336', linestyle='--', linewidth=1.5,
               label=f'Theoretical value (-1/18 ≈ {-1/18:.4f})')
    ax.set_xlabel('Training Iterations')
    ax.set_ylabel('Average Game Value (Player 1)')
    ax.set_title('Convergence of Game Value to Nash Equilibrium')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    path = os.path.join(figures_dir, 'game_value_convergence.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
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
                        f'{h:.2f}', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Probability')
    ax.set_title(title)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.15)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')


def create_strategy_charts(trainer, figures_dir: str):
    """Create 4-panel strategy visualization (same layout as original)."""
    fig = plt.figure(figsize=(14, 12))
    fig.suptitle("Kuhn Poker — CFR Strategy Analysis", fontsize=16,
                 fontweight='bold', y=0.98)
    gs = gridspec.GridSpec(2, 2, hspace=0.4, wspace=0.35,
                           top=0.92, bottom=0.06, left=0.08, right=0.95)

    card_labels = ['J (card 1)', 'Q (card 2)', 'K (card 3)']

    # Player 1: opening action
    ax1 = fig.add_subplot(gs[0, 0])
    _bar_chart(ax1, ['1', '2', '3'], card_labels, trainer,
               'Player 1: Opening Action', 'Player 1 Card')

    # Player 2: response to pass
    ax2 = fig.add_subplot(gs[0, 1])
    _bar_chart(ax2, ['1p', '2p', '3p'], card_labels, trainer,
               'Player 2: Response to Pass', 'Player 2 Card')

    # Player 2: response to bet (fold vs call)
    ax3 = fig.add_subplot(gs[1, 0])
    _bar_chart(ax3, ['1b', '2b', '3b'], card_labels, trainer,
               'Player 2: Response to Bet (fold vs call)', 'Player 2 Card',
               pass_label='Fold (pass)', bet_label='Call (bet)')

    # Player 1: facing bet after passing
    ax4 = fig.add_subplot(gs[1, 1])
    _bar_chart(ax4, ['1pb', '2pb', '3pb'], card_labels, trainer,
               'Player 1: Facing Bet After Passing', 'Player 1 Card',
               pass_label='Fold (pass)', bet_label='Call (bet)')

    path = os.path.join(figures_dir, 'strategy_analysis.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


def create_exploitability_chart(checkpoints, exploitabilities, figures_dir: str):
    """Generate log-log plot of exploitability vs iterations."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(checkpoints, exploitabilities, 'bo-', linewidth=2,
              markersize=8, label='Measured exploitability')

    # Reference O(1/√T) line
    import numpy as np
    if len(checkpoints) >= 2:
        c = exploitabilities[0] * (checkpoints[0] ** 0.5)
        ref_x = np.array(checkpoints)
        ref_y = c / np.sqrt(ref_x)
        ax.loglog(ref_x, ref_y, 'r--', linewidth=1.5,
                  label=r'$O(1/\sqrt{T})$ reference')

    ax.set_xlabel('CFR Iterations')
    ax.set_ylabel('Exploitability')
    ax.set_title('CFR Convergence: Exploitability vs Iterations (log-log)')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    path = os.path.join(figures_dir, 'exploitability_convergence.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")
