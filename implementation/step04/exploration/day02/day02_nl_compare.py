"""
Day-2 comparison: CFR vs MCCFR on mini-NL Leduc, full vs action-abstracted.

Four training runs, all with log-spaced exploitability checkpoints and
persistent JSON results:

    1. Full NL       — vanilla CFR, time-budgeted
    2. Full NL       — External-sampling MCCFR, 10M iterations
    3. Abstracted NL — vanilla CFR, time-budgeted
    4. Abstracted NL — External-sampling MCCFR, 10M iterations

Exploitability for each run is computed in its OWN game tree (full CFR and
full MCCFR evaluated against the full action space; abstracted variants
against the reduced action space). Day-3 will handle cross-game evaluation
with action translation.

Outputs:
    .nl_compare_results.json
    figures/day02_nl_compare.png  (2-panel: vs iters + vs wall-clock)
"""

import os
import sys
import time
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
STEP03 = os.path.abspath(os.path.join(HERE, '..', '..', '..', 'step03'))
sys.path.insert(0, STEP03)
sys.path.insert(0, HERE)

from cfr.info_set_node import InfoSetNode
from mini_nl_leduc import ALL_DEALS, MiniNLLeducState, NUM_CARDS
from nl_best_response import exploitability

MCCFR_TOTAL_ITERS = 10_000_000
MCCFR_CHECKPOINTS = [10_000, 30_000, 100_000, 300_000,
                     1_000_000, 3_000_000, 10_000_000]
CFR_TIME_BUDGET_SECONDS = 600   # 10 minutes per CFR run
CFR_CHECKPOINTS = None  # log-spaced, chosen adaptively by elapsed time

SEED = 42
RESULTS_FILE = os.path.join(HERE, '..', '.nl_compare_results.json')
FIGURE_FILE = os.path.join(HERE, '..', 'figures', 'day02_nl_compare.png')


# ---------------------------------------------------------------------------
# Vanilla CFR (time-budgeted with adaptive log checkpointing)
# ---------------------------------------------------------------------------

def _cfr(state, traversing, pi_opp, regret_buffer, node_map):
    if state.is_terminal():
        return state.get_utility(traversing)

    player = state.current_player()
    info_set = state.get_info_set(player)
    legal = state.legal_actions()
    n = len(legal)

    if info_set not in node_map:
        node_map[info_set] = (InfoSetNode(n), legal)
    node, _ = node_map[info_set]
    strat = node.get_current_strategy()

    if player == traversing:
        utils = [_cfr(state.apply_action(a), traversing, pi_opp,
                      regret_buffer, node_map) for a in legal]
        ev = sum(strat[i] * utils[i] for i in range(n))
        if info_set not in regret_buffer:
            regret_buffer[info_set] = [0.0] * n
        for i in range(n):
            regret_buffer[info_set][i] += pi_opp * (utils[i] - ev)
        return ev

    ev = 0.0
    for i, a in enumerate(legal):
        ev += strat[i] * _cfr(state.apply_action(a), traversing,
                              pi_opp * strat[i], regret_buffer, node_map)
    for i in range(n):
        node.strategy_sum[i] += pi_opp * strat[i]
    return ev


def train_cfr(abstracted: bool, time_budget_seconds: float, label: str):
    node_map: dict = {}
    iters = 0
    train_wall = 0.0

    out = {'label': label, 'kind': 'cfr', 'abstracted': abstracted,
           'iterations': [], 'exploits': [], 'train_seconds_at_ckpt': [],
           'total_infosets': None}

    # Adaptive checkpoints: 1, 3, 10, 30, 100, 300, 1000, ...
    ckpt_targets = [1, 3, 10, 30, 100, 300, 1_000, 3_000, 10_000]
    ckpt_idx = 0

    print(f"\n=== {label} (CFR, budget {time_budget_seconds:.0f}s) ===", flush=True)
    while train_wall < time_budget_seconds:
        target = ckpt_targets[ckpt_idx] if ckpt_idx < len(ckpt_targets) else iters * 3

        t0 = time.time()
        while iters < target and train_wall + (time.time() - t0) < time_budget_seconds:
            iters += 1
            for traversing in (0, 1):
                regret_buffer: dict = {}
                for deal in ALL_DEALS:
                    state = MiniNLLeducState((deal[0], deal[1]), deal[2],
                                             abstracted=abstracted)
                    _cfr(state, traversing, 1.0, regret_buffer, node_map)
                for key, deltas in regret_buffer.items():
                    node, _ = node_map[key]
                    for a in range(len(deltas)):
                        node.regret_sum[a] += deltas[a]
        train_wall += time.time() - t0

        if iters >= target or train_wall >= time_budget_seconds:
            exp = exploitability(node_map, abstracted=abstracted)
            out['iterations'].append(iters)
            out['exploits'].append(exp)
            out['train_seconds_at_ckpt'].append(train_wall)
            print(f"  iter={iters:>6,}  exploit={exp:.5f}  "
                  f"train_time={train_wall:>7.1f}s  ({iters/max(train_wall,1e-6):.1f}/s)",
                  flush=True)
            ckpt_idx += 1
            if ckpt_idx >= len(ckpt_targets):
                # time-based: next checkpoint at 3x current iter count
                ckpt_targets.append(iters * 3 if iters > 0 else 1)

    out['total_infosets'] = len(node_map)
    return out


# ---------------------------------------------------------------------------
# External-sampling MCCFR (matches findings §5 / step03 reference)
# ---------------------------------------------------------------------------

def _external_cfr(state, update_player, node_map, rng):
    if state.is_terminal():
        return state.get_utility(update_player)

    player = state.current_player()
    info_set = state.get_info_set(player)
    legal = state.legal_actions()
    n = len(legal)

    if info_set not in node_map:
        node_map[info_set] = (InfoSetNode(n), legal)
    node, _ = node_map[info_set]
    strat = node.get_current_strategy()

    if player == update_player:
        utils = [0.0] * n
        node_util = 0.0
        for i in range(n):
            utils[i] = _external_cfr(state.apply_action(legal[i]),
                                     update_player, node_map, rng)
            node_util += strat[i] * utils[i]
        for i in range(n):
            node.regret_sum[i] += utils[i] - node_util
            node.strategy_sum[i] += strat[i]
        return node_util

    r = rng.random()
    cum = 0.0
    sampled = n - 1
    for i in range(n):
        cum += strat[i]
        if r < cum:
            sampled = i
            break
    return _external_cfr(state.apply_action(legal[sampled]),
                         update_player, node_map, rng)


def train_mccfr(abstracted: bool, total_iters: int, checkpoints: list,
                label: str, seed: int):
    rng = random.Random(seed)
    node_map: dict = {}
    iters = 0
    train_wall = 0.0

    out = {'label': label, 'kind': 'mccfr', 'abstracted': abstracted,
           'iterations': [], 'exploits': [], 'train_seconds_at_ckpt': [],
           'total_infosets': None}

    print(f"\n=== {label} (MCCFR, {total_iters:,} iters) ===", flush=True)
    for target in checkpoints:
        if target > total_iters:
            break
        t0 = time.time()
        while iters < target:
            cards = rng.sample(range(NUM_CARDS), 3)
            state = MiniNLLeducState((cards[0], cards[1]), cards[2],
                                     abstracted=abstracted)
            update_player = iters % 2
            _external_cfr(state, update_player, node_map, rng)
            iters += 1
        train_wall += time.time() - t0

        exp = exploitability(node_map, abstracted=abstracted)
        out['iterations'].append(iters)
        out['exploits'].append(exp)
        out['train_seconds_at_ckpt'].append(train_wall)
        print(f"  iter={iters:>10,}  exploit={exp:.5f}  "
              f"train_time={train_wall:>7.1f}s  ({iters/max(train_wall,1e-6):>7,.0f}/s)",
              flush=True)

    out['total_infosets'] = len(node_map)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

RUNS = [
    ('Full-CFR',   'cfr',   False),
    ('Abs-CFR',    'cfr',   True),
    ('Full-MCCFR', 'mccfr', False),
    ('Abs-MCCFR',  'mccfr', True),
]


def _persist(results):
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)


def main():
    print(f"day-2 mini-NL Leduc: CFR vs MCCFR, full vs abstracted")
    print(f"MCCFR iters={MCCFR_TOTAL_ITERS:,}  CFR budget={CFR_TIME_BUDGET_SECONDS}s")

    results = {}
    t_global = time.time()

    for label, kind, abstracted in RUNS:
        if kind == 'cfr':
            results[label] = train_cfr(abstracted, CFR_TIME_BUDGET_SECONDS, label)
        else:
            results[label] = train_mccfr(abstracted, MCCFR_TOTAL_ITERS,
                                         MCCFR_CHECKPOINTS, label, SEED)
        _persist(results)

    print(f"\nTotal wall-clock: {(time.time() - t_global)/60:.1f} min")
    print(f"Results -> {RESULTS_FILE}")

    # Summary
    print()
    print(f"{'Run':<14} {'Kind':<7} {'Abs':<4} {'InfoSets':>9} "
          f"{'Final exp.':>12} {'Train time':>12}")
    print('-' * 70)
    for label, kind, abstracted in RUNS:
        r = results[label]
        print(f"{label:<14} {kind:<7} {str(abstracted):<4} "
              f"{r['total_infosets']:>9,} {r['exploits'][-1]:>12.5f} "
              f"{r['train_seconds_at_ckpt'][-1]:>10.1f}s")

    _save_plot(results)


def _save_plot(results):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping plot")
        return

    styles = {
        'Full-CFR':   ('#1565C0', 'o', '-'),
        'Abs-CFR':    ('#1565C0', 's', '--'),
        'Full-MCCFR': ('#E65100', '^', '-'),
        'Abs-MCCFR':  ('#E65100', 'D', '--'),
    }

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))

    ax = axes[0]
    for label in styles:
        r = results.get(label)
        if not r:
            continue
        c, m, ls = styles[label]
        ax.plot(r['iterations'], r['exploits'],
                color=c, marker=m, linestyle=ls,
                linewidth=2, markersize=7, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('iterations')
    ax.set_ylabel('Exploitability (own game)')
    ax.set_title('Exploitability vs iterations\n'
                 'Blue=CFR, Orange=MCCFR.  Solid=Full (4704 is), Dashed=Abstracted (936 is)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    ax = axes[1]
    for label in styles:
        r = results.get(label)
        if not r:
            continue
        c, m, ls = styles[label]
        ax.plot(r['train_seconds_at_ckpt'], r['exploits'],
                color=c, marker=m, linestyle=ls,
                linewidth=2, markersize=7, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Wall-clock training seconds')
    ax.set_ylabel('Exploitability (own game)')
    ax.set_title('Exploitability vs wall-clock')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    fig.suptitle('mini-NL Leduc — CFR vs MCCFR, Full vs Action-Abstracted',
                 fontsize=13, y=1.02)
    plt.tight_layout()
    os.makedirs(os.path.dirname(FIGURE_FILE), exist_ok=True)
    plt.savefig(FIGURE_FILE, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"Plot -> {FIGURE_FILE}")


if __name__ == "__main__":
    main()
