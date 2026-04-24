"""
MCCFR 10M-iteration comparison: Original vs Regime 1 (suit-abstracted) vs
Regime 2 (rank-canonical).

Uses corrected external-sampling MCCFR (see findings.md §5).

Per-iteration sampling:
  - Original / Suit-Abstracted: uniform random 3-card deal from 6 cards.
  - Rank-canonical: sample a canonical rank-triple with probability
    proportional to its multiplicity (so the marginal deal distribution
    matches the original).

Exploitability is scored in the ORIGINAL full game for all three variants
(via a key-mapping proxy for the abstracted ones).

Outputs:
  - .mccfr_compare_results.json  (log-spaced checkpoints per variant)
  - figures/day01_mccfr_compare.png
"""

import sys
import os
import time
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
STEP03 = os.path.abspath(os.path.join(HERE, '..', '..', 'step03'))
sys.path.insert(0, STEP03)
sys.path.insert(0, HERE)

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import NUM_CARDS, LeducState as OrigState
from evaluate.best_response import best_response_value

from leduc_suit_abstracted import LeducState as SuitState
from leduc_rank_engine import LeducRankState, CANONICAL_DEALS

TOTAL_ITERATIONS = 10_000_000
CHECKPOINTS = [10_000, 30_000, 100_000, 300_000,
               1_000_000, 3_000_000, 10_000_000]
SEED = 42

RESULTS_FILE = os.path.join(HERE, '.mccfr_compare_results.json')
FIGURE_FILE = os.path.join(HERE, 'figures', 'day01_mccfr_compare.png')


# ---------------------------------------------------------------------------
# Deal samplers
# ---------------------------------------------------------------------------

def sample_full_deal(rng):
    """Uniform 3-card draw without replacement from 6 cards. Returns (c0, c1, cc)."""
    return tuple(rng.sample(range(NUM_CARDS), 3))


_CANONICAL_TRIPLES = [d for d, _ in CANONICAL_DEALS]
_CANONICAL_WEIGHTS = [w for _, w in CANONICAL_DEALS]


def sample_canonical_rank_deal(rng):
    """Weighted draw from the 24 canonical rank-triples.

    Marginal distribution over (rank0, rank1, rankC) matches what we'd get
    from uniform full-suit deals followed by suit-stripping — but without
    materialising the suits.
    """
    return rng.choices(_CANONICAL_TRIPLES, weights=_CANONICAL_WEIGHTS, k=1)[0]


# ---------------------------------------------------------------------------
# Correct external-sampling MCCFR
# ---------------------------------------------------------------------------

def _external_cfr(state, update_player: int, node_map: dict, rng):
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


# ---------------------------------------------------------------------------
# Variant configuration
# ---------------------------------------------------------------------------

def make_state_original(rng):
    c0, c1, cc = sample_full_deal(rng)
    return OrigState((c0, c1), cc)


def make_state_suit(rng):
    c0, c1, cc = sample_full_deal(rng)
    return SuitState((c0, c1), cc)


def make_state_rank(rng):
    r0, r1, rc = sample_canonical_rank_deal(rng)
    return LeducRankState((r0, r1), rc)


def _suit_key(full_key: str) -> str:
    pipe = full_key.index('|')
    prefix, rest = full_key[:pipe], full_key[pipe:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return f"{int(c)//2}:{int(comm)//2}{rest}"
    return f"{int(prefix)//2}{rest}"


class _KeyProxy:
    def __init__(self, m, mapper):
        self._m, self._mp = m, mapper
    def __contains__(self, k): return self._mp(k) in self._m
    def __getitem__(self, k): return self._m[self._mp(k)]


def exploitability(node_map: dict, key_mapper) -> float:
    proxy = _KeyProxy(node_map, key_mapper) if key_mapper else node_map
    br0 = best_response_value(proxy, br_player=0)
    br1 = best_response_value(proxy, br_player=1)
    return (br0 + br1) / 2


VARIANTS = [
    ('Original',        make_state_original, None),
    ('Suit (regime 1)', make_state_suit,     _suit_key),
    ('Rank (regime 2)', make_state_rank,     _suit_key),  # same key format as suit
]


# ---------------------------------------------------------------------------
# Per-variant training with log-spaced checkpoints
# ---------------------------------------------------------------------------

def train_variant(label, make_state, key_mapper, total_iters, checkpoints, seed):
    rng = random.Random(seed)
    node_map: dict = {}
    iters = 0

    out = {'label': label, 'iterations': [], 'exploits': [],
           'train_seconds_at_ckpt': [], 'total_infosets': None}
    train_wall = 0.0

    print(f"\n=== {label} ===", flush=True)
    for target in checkpoints:
        if target > total_iters:
            break
        t0 = time.time()
        while iters < target:
            state = make_state(rng)
            update_player = iters % 2
            _external_cfr(state, update_player, node_map, rng)
            iters += 1
        train_wall += time.time() - t0

        exp_t0 = time.time()
        exp = exploitability(node_map, key_mapper)
        exp_elapsed = time.time() - exp_t0

        out['iterations'].append(iters)
        out['exploits'].append(exp)
        out['train_seconds_at_ckpt'].append(train_wall)
        print(f"  iter={iters:>10,}  exploit={exp:.5f}  "
              f"train_time={train_wall:>7.1f}s  ({iters/train_wall:>7,.0f}/s)  "
              f"br_time={exp_elapsed:.1f}s", flush=True)

    out['total_infosets'] = len(node_map)
    return out


def main():
    print(f"MCCFR (corrected external sampling) — {TOTAL_ITERATIONS:,} iters per variant")
    print(f"Checkpoints: {CHECKPOINTS}")

    results = {}
    t_global = time.time()
    for label, make_state, key_mapper in VARIANTS:
        results[label] = train_variant(label, make_state, key_mapper,
                                        TOTAL_ITERATIONS, CHECKPOINTS, SEED)
        # Persist incrementally in case of interruption
        with open(RESULTS_FILE, 'w') as f:
            json.dump(results, f, indent=2)

    print(f"\nTotal wall-clock: {(time.time()-t_global)/60:.1f} min")
    print(f"Results -> {RESULTS_FILE}")

    # Summary
    print()
    print(f"{'Variant':<20} {'InfoSets':>9} {'Final exploit':>15} "
          f"{'Train time':>12}")
    print('-' * 62)
    for label, _, _ in VARIANTS:
        r = results[label]
        print(f"{label:<20} {r['total_infosets']:>9,} "
              f"{r['exploits'][-1]:>15.5f} "
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

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    styles = {
        'Original':        ('#2196F3', 'o', '-'),
        'Suit (regime 1)': ('#4CAF50', 's', '--'),
        'Rank (regime 2)': ('#FF5722', '^', ':'),
    }

    ax = axes[0]
    for label in styles:
        r = results[label]
        c, m, ls = styles[label]
        ax.plot(r['iterations'], r['exploits'],
                color=c, marker=m, linestyle=ls,
                linewidth=2, markersize=8, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('MCCFR iterations')
    ax.set_ylabel('Exploitability (full game)')
    ax.set_title('Exploitability vs iterations\n'
                 '(Original expected worst — 936 keys = more variance per key)')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    ax = axes[1]
    for label in styles:
        r = results[label]
        c, m, ls = styles[label]
        ax.plot(r['train_seconds_at_ckpt'], r['exploits'],
                color=c, marker=m, linestyle=ls,
                linewidth=2, markersize=8, label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Wall-clock training seconds')
    ax.set_ylabel('Exploitability (full game)')
    ax.set_title('Exploitability vs wall-clock')
    ax.grid(True, which='both', alpha=0.3)
    ax.legend()

    fig.suptitle(f'MCCFR @ {TOTAL_ITERATIONS:,} iterations — abstraction regimes',
                 fontsize=13, y=1.02)
    plt.tight_layout()
    os.makedirs(os.path.dirname(FIGURE_FILE), exist_ok=True)
    plt.savefig(FIGURE_FILE, dpi=150, bbox_inches='tight')
    print(f"Plot -> {FIGURE_FILE}")


if __name__ == "__main__":
    main()
