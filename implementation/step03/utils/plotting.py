"""Visualization utilities for Leduc Poker CFR results."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os


def create_convergence_chart(trainer, figures_dir: str):
    """Plot game value convergence."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(trainer.iteration_history, trainer.game_value_history,
            color='#2196F3', linewidth=1.5, label='Computed game value')
    ax.set_xlabel('Training Iterations')
    ax.set_ylabel('Average Game Value (Player 0)')
    ax.set_title('Leduc Poker — Game Value Convergence')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)

    path = os.path.join(figures_dir, 'game_value_convergence.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


def create_strategy_charts(trainer, figures_dir: str):
    """Create summary strategy chart for Leduc (top info sets by visit frequency)."""
    from cfr.leduc_poker import FOLD, CHECK_CALL, RAISE, card_str

    # Pick a representative subset: root info sets (round 0, no history)
    root_info_sets = []
    for info_set in sorted(trainer.node_map.keys()):
        if '|' in info_set:
            parts = info_set.split('|')
            if parts[1] == '':  # root of round 0
                root_info_sets.append(info_set)

    if not root_info_sets:
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    labels = []
    check_probs = []
    raise_probs = []

    for info_set in root_info_sets:
        node, legal_actions = trainer.node_map[info_set]
        avg = node.get_average_strategy()
        card_id = int(info_set.split('|')[0])
        labels.append(card_str(card_id))
        # At root, legal actions are CHECK_CALL and RAISE (no fold at root)
        c_idx = legal_actions.index(CHECK_CALL) if CHECK_CALL in legal_actions else None
        r_idx = legal_actions.index(RAISE) if RAISE in legal_actions else None
        check_probs.append(avg[c_idx] if c_idx is not None else 0)
        raise_probs.append(avg[r_idx] if r_idx is not None else 0)

    x = range(len(labels))
    ax.bar([i - 0.18 for i in x], check_probs, 0.35,
           label='Check', color='#66BB6A', edgecolor='white')
    ax.bar([i + 0.18 for i in x], raise_probs, 0.35,
           label='Raise', color='#EF5350', edgecolor='white')
    ax.set_xlabel('Private Card')
    ax.set_ylabel('Probability')
    ax.set_title('Leduc Poker — Opening Action Strategy (Round 1)')
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.15)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    path = os.path.join(figures_dir, 'strategy_analysis.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")


def create_exploitability_chart(checkpoints, exploitabilities, figures_dir: str):
    """Generate log-log plot of exploitability vs iterations."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.loglog(checkpoints, exploitabilities, 'bo-', linewidth=2,
              markersize=8, label='Measured exploitability')

    import numpy as np
    if len(checkpoints) >= 2:
        c = exploitabilities[0] * (checkpoints[0] ** 0.5)
        ref_x = np.array(checkpoints)
        ref_y = c / np.sqrt(ref_x)
        ax.loglog(ref_x, ref_y, 'r--', linewidth=1.5,
                  label=r'$O(1/\sqrt{T})$ reference')

    ax.set_xlabel('CFR Iterations')
    ax.set_ylabel('Exploitability')
    ax.set_title('Leduc Poker — CFR Convergence (log-log)')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    path = os.path.join(figures_dir, 'exploitability_convergence.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Chart saved to: {path}")
