"""
Day 1 exploration: card abstraction comparison.

Trains CFR and MCCFR-Outcome on three Leduc Poker variants for 180 seconds each,
then evaluates each learned strategy's exploitability in the ORIGINAL full game.

Variants:
  1. Original        — no abstraction (step03 baseline)
  2. Suit-Abstracted — lossless: J♠ and J♥ share one info set key
  3. Lossy (J/Q=low) — lossy: Jack and Queen are indistinguishable

Key question: does abstraction speed up convergence enough to offset the
information loss, when measured in the full game?
"""

import sys
import os
import time
import random
import json

# step03 on path for InfoSetNode and best_response
STEP03 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'step03'))
sys.path.insert(0, STEP03)

CACHE_FILE = os.path.join(os.path.dirname(__file__), '.day01_results.json')

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import ALL_DEALS, NUM_CARDS, LeducState as OrigState
from evaluate.best_response import best_response_value

from leduc_suit_abstracted import LeducState as SuitState
from leduc_lossy_abstracted import LeducState as LossyState

TRAIN_ITERATIONS = 100000
CHECKPOINT_INTERVAL = 10000  # Save checkpoint every 10k iterations
CHECKPOINTS_DIR = os.path.join(os.path.dirname(__file__), '.checkpoints')

if not os.path.exists(CHECKPOINTS_DIR):
    os.makedirs(CHECKPOINTS_DIR)

# ---------------------------------------------------------------------------
# Checkpoint save/load
# ---------------------------------------------------------------------------

def _checkpoint_path(variant_name: str) -> str:
    return os.path.join(CHECKPOINTS_DIR, f"{variant_name}.json")


def _serialize_node_map(node_map: dict) -> dict:
    """Serialize node_map to JSON-compatible format."""
    serialized = {}
    for key, (node, legal_actions) in node_map.items():
        serialized[key] = {
            'regret_sum': list(node.regret_sum),
            'strategy_sum': list(node.strategy_sum),
            'num_actions': node.num_actions,
            'legal_actions': legal_actions,
        }
    return serialized


def _deserialize_node_map(serialized: dict) -> dict:
    """Deserialize node_map from JSON format."""
    node_map = {}
    for key, data in serialized.items():
        node = InfoSetNode(data['num_actions'])
        node.regret_sum = data['regret_sum']
        node.strategy_sum = data['strategy_sum']
        node_map[key] = (node, data['legal_actions'])
    return node_map


def _load_checkpoint(variant_name: str):
    """Load checkpoint. Returns (node_map, iterations_completed) or (None, 0)."""
    path = _checkpoint_path(variant_name)
    if os.path.exists(path):
        try:
            with open(path) as f:
                ckpt = json.load(f)
            node_map = _deserialize_node_map(ckpt['node_map'])
            return node_map, ckpt['iterations']
        except Exception as e:
            print(f"  Warning: checkpoint load failed ({e}), starting fresh")
            return None, 0
    return None, 0


def _save_checkpoint(variant_name: str, node_map: dict, iterations: int):
    """Save checkpoint."""
    path = _checkpoint_path(variant_name)
    ckpt = {
        'iterations': iterations,
        'node_map': _serialize_node_map(node_map),
    }
    with open(path, 'w') as f:
        json.dump(ckpt, f)


# ---------------------------------------------------------------------------
# Training functions (parameterised by game class)
# ---------------------------------------------------------------------------

def train_cfr(GameClass, variant_name: str, target_iterations: int):
    """Vanilla CFR with checkpoint support.

    Loads checkpoint if exists, resumes from last saved iteration,
    saves checkpoint every CHECKPOINT_INTERVAL iterations.

    Returns (node_map, iterations_completed).
    """
    node_map, completed = _load_checkpoint(variant_name)
    if node_map is None:
        node_map = {}
        completed = 0

    if completed >= target_iterations:
        print(f"    (already completed {completed:,} iterations)")
        return node_map, completed

    print(f"    Starting from iteration {completed:,}...", flush=True)

    while completed < target_iterations:
        completed += 1
        for traversing in (0, 1):
            regret_buffer: dict = {}
            for deal in ALL_DEALS:
                state = GameClass((deal[0], deal[1]), deal[2])
                _cfr(state, traversing, 1.0, regret_buffer, node_map)
            for key, deltas in regret_buffer.items():
                node, _ = node_map[key]
                for a in range(len(deltas)):
                    node.regret_sum[a] += deltas[a]

        if completed % 100 == 0:
            pct = 100 * completed / target_iterations
            print(f"      {completed:,} / {target_iterations:,} ({pct:.0f}%)", flush=True)

        if completed % CHECKPOINT_INTERVAL == 0:
            _save_checkpoint(variant_name, node_map, completed)
            print(f"      ✓ Checkpoint saved", flush=True)

    _save_checkpoint(variant_name, node_map, completed)
    return node_map, completed


def _cfr(state, traversing: int, pi_opp: float, regret_buffer: dict, node_map: dict) -> float:
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
        utils = [_cfr(state.apply_action(a), traversing, pi_opp, regret_buffer, node_map)
                 for a in legal]
        ev = sum(strat[i] * utils[i] for i in range(n))
        if info_set not in regret_buffer:
            regret_buffer[info_set] = [0.0] * n
        for i in range(n):
            regret_buffer[info_set][i] += pi_opp * (utils[i] - ev)
        return ev
    else:
        ev = 0.0
        for i, a in enumerate(legal):
            ev += strat[i] * _cfr(state.apply_action(a), traversing,
                                   pi_opp * strat[i], regret_buffer, node_map)
        for i in range(n):
            node.strategy_sum[i] += pi_opp * strat[i]
        return ev




# ---------------------------------------------------------------------------
# Full-game exploitability of abstracted strategies
# ---------------------------------------------------------------------------

class _AbstractedMapProxy:
    """Makes an abstracted node_map look up-able via full-game info set keys.

    best_response_value() traverses the original LeducState tree and calls
    state.get_info_set() to get full-game keys. This proxy intercepts those
    lookups and maps them to the abstracted node_map transparently.
    """

    def __init__(self, abstracted_map: dict, key_mapper):
        self._map = abstracted_map
        self._mapper = key_mapper

    def __contains__(self, key: str) -> bool:
        return self._mapper(key) in self._map

    def __getitem__(self, key: str):
        return self._map[self._mapper(key)]


def _suit_key(full_key: str) -> str:
    """'1:4|cc/' → '0:2|cc/'  (card ids → ranks)."""
    pipe = full_key.index('|')
    prefix, rest = full_key[:pipe], full_key[pipe:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return f"{int(c)//2}:{int(comm)//2}{rest}"
    return f"{int(prefix)//2}{rest}"


def _lossy_key(full_key: str) -> str:
    """'1:4|cc/' → 'low:high|cc/'  (J/Q=low, K=high)."""
    def b(c): return "low" if int(c) // 2 < 2 else "high"
    pipe = full_key.index('|')
    prefix, rest = full_key[:pipe], full_key[pipe:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return f"{b(c)}:{b(comm)}{rest}"
    return f"{b(prefix)}{rest}"


def compute_full_game_exploitability(node_map: dict, key_mapper=None) -> float:
    """Exploitability of the strategy when played in the full (unabstracted) game.

    key_mapper translates full-game info set keys to the abstracted keys stored
    in node_map. Pass None for the original unabstracted game.
    """
    proxy = _AbstractedMapProxy(node_map, key_mapper) if key_mapper else node_map
    br0 = best_response_value(proxy, br_player=0)
    br1 = best_response_value(proxy, br_player=1)
    return (br0 + br1) / 2


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

VARIANTS = [
    ("Original",        OrigState,  None),
    ("Suit-Abstracted", SuitState,  _suit_key),
    ("Lossy (J/Q=low)", LossyState, _lossy_key),
]


def _load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except:
            return None
    return None


def _save_cache(results):
    with open(CACHE_FILE, 'w') as f:
        json.dump(results, f, indent=2)


def main():
    cached = _load_cache()
    if cached:
        print(f"\nLoading cached results from {CACHE_FILE}")
        results = [(r[0], r[1], r[2], r[3]) for r in cached]
    else:
        print(f"\nCard Abstraction Comparison — CFR, {TRAIN_ITERATIONS:,} iterations per variant")
        print(f"Exploitability measured in the ORIGINAL full game\n")
        header = f"{'Variant':<22} {'InfoSets':>9} {'Iters':>12} {'Exploit':>10}"
        print(header)
        print("-" * len(header))

        results = []

        for v_name, GameClass, key_mapper in VARIANTS:
            print(f"  Training {v_name} ...", flush=True)

            node_map, iters = train_cfr(GameClass, v_name, TRAIN_ITERATIONS)

            print(f"    Evaluating exploitability ...", flush=True)
            exploit = compute_full_game_exploitability(node_map, key_mapper)

            results.append((v_name, len(node_map), iters, exploit))
            print(f"  {v_name:<22} {len(node_map):>9,} {iters:>12,} {exploit:>10.5f}")

        _save_cache(results)

    print()
    print("Summary")
    print("-" * 65)
    print(f"{'Variant':<22} {'InfoSets':>9} {'Iters':>12} {'Exploit':>10}")
    print("-" * 65)
    for row in results:
        v, n, i, e = row
        print(f"{v:<22} {n:>9,} {i:>12,} {e:>10.5f}")

    _save_plot(results)


def _save_plot(results):
    try:
        import matplotlib
        matplotlib.use('Agg')  # Headless backend
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(10, 5))

        variants = [r[0] for r in results]
        exploits = [r[3] for r in results]
        colors = ['#2196F3', '#4CAF50', '#FF5722']

        bars = ax.bar(range(len(results)), exploits, color=colors[:len(results)], width=0.5)
        ax.set_xticks(range(len(results)))
        ax.set_xticklabels(variants, fontsize=10)
        ax.set_ylabel("Exploitability (full game)", fontsize=11)
        ax.set_title(f"Card Abstraction with CFR — {TRAIN_ITERATIONS:,} iterations\n"
                     "Lower = closer to Nash in the full game", fontsize=12)

        for bar, val in zip(bars, exploits):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                    f"{val:.4f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

        plt.tight_layout()
        out = os.path.join(os.path.dirname(__file__), 'figures', 'day01_abstraction.png')
        os.makedirs(os.path.dirname(out), exist_ok=True)
        plt.savefig(out, dpi=150)
        print(f"\nPlot saved → {out}")
    except ImportError:
        print("\n(matplotlib not available — skipping plot)")


if __name__ == "__main__":
    main()
