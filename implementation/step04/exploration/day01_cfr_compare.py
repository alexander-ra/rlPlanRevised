"""
CFR comparison: Original (120 suit-deals) vs Rank-canonical (24 weighted deals).

Both variants run for the same number of CFR iterations. An iteration =
one pass over all (canonical) deals for each traversing player.

Per findings.md §4, regime-2 lossless abstraction must produce the same
exploitability-vs-iteration curve as the original engine (up to floating
point noise) because canonical weights + symmetry gives numerically
identical regret updates. The benefit lives in wall-clock time per
iteration: 24 canonical deals vs 120 full-suit deals, ~5x faster.

Outputs:
  - .cfr_compare_results.json   (exploitability at each checkpoint + timing)
  - figures/day01_cfr_compare.png
"""

import sys
import os
import time
import json

HERE = os.path.dirname(os.path.abspath(__file__))
STEP03 = os.path.abspath(os.path.join(HERE, '..', '..', 'step03'))
sys.path.insert(0, STEP03)
sys.path.insert(0, HERE)

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import ALL_DEALS, LeducState as OrigState
from evaluate.best_response import best_response_value

from leduc_rank_engine import LeducRankState, CANONICAL_DEALS

TOTAL_ITERATIONS = 10_000
# Log-spaced iteration counts at which to measure exploitability.
CHECKPOINTS = [10, 30, 100, 300, 1000, 3000, 10_000]
RESULTS_FILE = os.path.join(HERE, '.cfr_compare_results.json')
FIGURE_FILE = os.path.join(HERE, 'figures', 'day01_cfr_compare.png')


# ---------------------------------------------------------------------------
# CFR trainer, parametrised by the deal iterator
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


def run_cfr_step_original(node_map):
    """One CFR iteration over all 120 full-suit deals."""
    for traversing in (0, 1):
        regret_buffer: dict = {}
        for deal in ALL_DEALS:
            state = OrigState((deal[0], deal[1]), deal[2])
            _cfr(state, traversing, 1.0, regret_buffer, node_map)
        for key, deltas in regret_buffer.items():
            node, _ = node_map[key]
            for a in range(len(deltas)):
                node.regret_sum[a] += deltas[a]


def run_cfr_step_rank(node_map):
    """One CFR iteration over the 24 canonical rank-deals, weighted.

    Weight is folded into pi_opp at the root. This makes both the regret
    update at traversing nodes (accumulated via pi_opp) and the strategy
    update at opponent nodes (accumulated via pi_opp) naturally reflect
    the deal's multiplicity.
    """
    for traversing in (0, 1):
        regret_buffer: dict = {}
        for (r0, r1, rc), weight in CANONICAL_DEALS:
            state = LeducRankState((r0, r1), rc)
            _cfr(state, traversing, float(weight), regret_buffer, node_map)
        for key, deltas in regret_buffer.items():
            node, _ = node_map[key]
            for a in range(len(deltas)):
                node.regret_sum[a] += deltas[a]


# ---------------------------------------------------------------------------
# Exploitability against the full (unabstracted) game
# ---------------------------------------------------------------------------

class _RankKeyProxy:
    """Looks up full-game keys by stripping suits -> rank keys.

    The rank engine's node_map is keyed as "0|h" or "0:2|h" (same format
    as suit-abstracted). best_response walks the full suit-deal tree and
    emits keys like "3|h" (card id). Convert by dividing by 2.
    """
    def __init__(self, rank_map: dict):
        self._map = rank_map

    def _to_rank(self, full_key: str) -> str:
        pipe = full_key.index('|')
        prefix, rest = full_key[:pipe], full_key[pipe:]
        if ':' in prefix:
            c, comm = prefix.split(':')
            return f"{int(c)//2}:{int(comm)//2}{rest}"
        return f"{int(prefix)//2}{rest}"

    def __contains__(self, key: str) -> bool:
        return self._to_rank(key) in self._map

    def __getitem__(self, key: str):
        return self._map[self._to_rank(key)]


def exploitability_original(node_map: dict) -> float:
    br0 = best_response_value(node_map, br_player=0)
    br1 = best_response_value(node_map, br_player=1)
    return (br0 + br1) / 2


def exploitability_rank(node_map: dict) -> float:
    proxy = _RankKeyProxy(node_map)
    br0 = best_response_value(proxy, br_player=0)
    br1 = best_response_value(proxy, br_player=1)
    return (br0 + br1) / 2


# ---------------------------------------------------------------------------
# Training drivers with log-spaced checkpoints
# ---------------------------------------------------------------------------

def train_with_checkpoints(step_fn, exploit_fn, total_iters: int,
                            checkpoints: list, label: str):
    """Run CFR for total_iters, evaluating exploitability at each checkpoint.

    Returns dict with arrays: iterations, exploits, train_seconds,
    plus total wall-clock and final info-set count.
    """
    node_map: dict = {}
    iters = 0
    wall_start = time.time()
    cumulative_train_seconds = 0.0

    out = {'label': label, 'iterations': [], 'exploits': [],
           'train_seconds_at_ckpt': [], 'total_infosets': None}

    for target in checkpoints:
        if target > total_iters:
            break
        t0 = time.time()
        while iters < target:
            step_fn(node_map)
            iters += 1
        cumulative_train_seconds += time.time() - t0

        exp = exploit_fn(node_map)
        out['iterations'].append(iters)
        out['exploits'].append(exp)
        out['train_seconds_at_ckpt'].append(cumulative_train_seconds)
        print(f"  [{label}] iter={iters:>6,}  exploit={exp:.5f}  "
              f"train_time={cumulative_train_seconds:.1f}s", flush=True)

    out['total_wall_seconds'] = time.time() - wall_start
    out['total_infosets'] = len(node_map)
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print(f"\nCFR comparison — {TOTAL_ITERATIONS:,} iterations")
    print(f"  Original (regime 0): 120 full-suit deals per iteration")
    print(f"  Rank-canonical (regime 2): {len(CANONICAL_DEALS)} canonical deals, "
          f"weights sum to 120\n")

    results = {}

    print("Training Original ...")
    results['Original'] = train_with_checkpoints(
        run_cfr_step_original, exploitability_original,
        TOTAL_ITERATIONS, CHECKPOINTS, 'Original')

    print("\nTraining Rank-canonical ...")
    results['Rank-canonical'] = train_with_checkpoints(
        run_cfr_step_rank, exploitability_rank,
        TOTAL_ITERATIONS, CHECKPOINTS, 'Rank-canonical')

    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults -> {RESULTS_FILE}")

    # Summary table
    print()
    print(f"{'Variant':<18} {'InfoSets':>9} {'Train time':>12} "
          f"{'Final exploit':>15}")
    print('-' * 60)
    for v in ('Original', 'Rank-canonical'):
        r = results[v]
        print(f"{v:<18} {r['total_infosets']:>9,} "
              f"{r['train_seconds_at_ckpt'][-1]:>10.1f}s  "
              f"{r['exploits'][-1]:>15.5f}")

    # Speedup calculation
    orig_t = results['Original']['train_seconds_at_ckpt'][-1]
    rank_t = results['Rank-canonical']['train_seconds_at_ckpt'][-1]
    print(f"\nWall-clock speedup (regime 2 / regime 0): {orig_t/rank_t:.2f}x")

    # Strategy-trajectory equivalence check
    print("\nExploitability-vs-iteration equivalence check:")
    for i, target in enumerate(CHECKPOINTS):
        if i >= len(results['Original']['iterations']):
            break
        eo = results['Original']['exploits'][i]
        er = results['Rank-canonical']['exploits'][i]
        diff = abs(eo - er)
        print(f"  iter={target:>6,}  orig={eo:.5f}  rank={er:.5f}  "
              f"|Δ|={diff:.2e}")

    _save_plot(results)


def _save_plot(results):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available; skipping plot")
        return

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    colors = {'Original': '#2196F3', 'Rank-canonical': '#FF5722'}
    markers = {'Original': 'o', 'Rank-canonical': 's'}

    ax = axes[0]
    for label in ('Original', 'Rank-canonical'):
        r = results[label]
        ax.plot(r['iterations'], r['exploits'],
                color=colors[label], marker=markers[label],
                linewidth=2, markersize=7, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('CFR iterations')
    ax.set_ylabel('Exploitability (full game)')
    ax.set_title('Exploitability vs iterations\n'
                 '(expected: curves overlap — same math, different plumbing)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    ax = axes[1]
    for label in ('Original', 'Rank-canonical'):
        r = results[label]
        ax.plot(r['train_seconds_at_ckpt'], r['exploits'],
                color=colors[label], marker=markers[label],
                linewidth=2, markersize=7, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Wall-clock training seconds')
    ax.set_ylabel('Exploitability (full game)')
    ax.set_title('Exploitability vs wall-clock\n'
                 '(expected: rank-canonical is shifted left — ~5x faster)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    fig.suptitle(f'CFR @ {TOTAL_ITERATIONS:,} iterations — Original vs Rank-canonical (regime 2)',
                 fontsize=13, y=1.02)
    plt.tight_layout()
    os.makedirs(os.path.dirname(FIGURE_FILE), exist_ok=True)
    plt.savefig(FIGURE_FILE, dpi=150, bbox_inches='tight')
    print(f"\nPlot -> {FIGURE_FILE}")


if __name__ == "__main__":
    main()
