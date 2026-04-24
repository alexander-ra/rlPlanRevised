"""
Day 1: External Sampling MCCFR on the day-1 Leduc variants.

This file is the corrected version of the earlier (buggy) external-sampling
implementation. See findings.md §5 for the bug analysis. The corrected update
rule matches step03/cfr/mccfr_external_trainer.py:

  - On the update player's turn: explore ALL legal actions and compute
    regrets from their actual counterfactual values.
  - On the opponent's turn: sample ONE action from the opponent's current
    strategy and recurse.
  - Strategy-sum is accumulated at update-player nodes only (uniform weight,
    since external sampling does not track reach probability).

Use this for quick MCCFR sanity checks. The 10M-iteration comparison used for
the report lives in day01_mccfr_compare.py.
"""

import sys
import os
import time
import random

STEP03 = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'step03'))
sys.path.insert(0, STEP03)

from cfr.info_set_node import InfoSetNode
from cfr.leduc_poker import NUM_CARDS
from cfr.leduc_poker import LeducState as OrigState
from evaluate.best_response import best_response_value

from leduc_suit_abstracted import LeducState as SuitState
from leduc_lossy_abstracted import LeducState as LossyState

TRAIN_SECONDS = 60
SEED = 42


def _suit_key(full_key: str) -> str:
    pipe = full_key.index('|')
    prefix, rest = full_key[:pipe], full_key[pipe:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return f"{int(c)//2}:{int(comm)//2}{rest}"
    return f"{int(prefix)//2}{rest}"


def _lossy_key(full_key: str) -> str:
    def b(c): return "low" if int(c) // 2 < 2 else "high"
    pipe = full_key.index('|')
    prefix, rest = full_key[:pipe], full_key[pipe:]
    if ':' in prefix:
        c, comm = prefix.split(':')
        return f"{b(c)}:{b(comm)}{rest}"
    return f"{b(prefix)}{rest}"


class _AbstractedMapProxy:
    def __init__(self, abstracted_map: dict, key_mapper):
        self._map = abstracted_map
        self._mapper = key_mapper

    def __contains__(self, key: str) -> bool:
        return self._mapper(key) in self._map

    def __getitem__(self, key: str):
        return self._map[self._mapper(key)]


VARIANTS = [
    ("Original",        OrigState,  None),
    ("Suit-Abstracted", SuitState,  _suit_key),
    ("Lossy (J/Q=low)", LossyState, _lossy_key),
]


def train_external_sampling(GameClass, seconds: int, seed: int):
    """Run correct external-sampling MCCFR for a time budget.

    Returns (node_map, iterations_completed).
    """
    rng = random.Random(seed)
    node_map: dict = {}
    iters = 0
    deadline = time.time() + seconds

    while time.time() < deadline:
        cards = rng.sample(range(NUM_CARDS), 3)
        state = GameClass((cards[0], cards[1]), cards[2])
        update_player = iters % 2
        _external_cfr(state, update_player, node_map, rng)
        iters += 1

    return node_map, iters


def _external_cfr(state, update_player: int, node_map: dict, rng: random.Random) -> float:
    """Correct external-sampling CFR traversal.

    Matches step03/cfr/mccfr_external_trainer.external_cfr:
    - Terminal -> return update_player's utility.
    - Update-player node -> explore all actions, update regret and strategy sums.
    - Opponent node -> sample one action, recurse.
    """
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
    else:
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


def compute_exploitability(node_map: dict, key_mapper=None) -> float:
    proxy = _AbstractedMapProxy(node_map, key_mapper) if key_mapper else node_map
    br0 = best_response_value(proxy, br_player=0)
    br1 = best_response_value(proxy, br_player=1)
    return (br0 + br1) / 2


def main():
    print(f"\nExternal Sampling MCCFR — {TRAIN_SECONDS}s per variant (seed={SEED})\n")
    header = f"{'Variant':<22} {'InfoSets':>9} {'Iters':>12} {'Exploit':>10}"
    print(header)
    print("-" * len(header))

    for v_name, GameClass, key_mapper in VARIANTS:
        print(f"  Training {v_name} ...", flush=True)
        node_map, iters = train_external_sampling(GameClass, TRAIN_SECONDS, SEED)
        exploit = compute_exploitability(node_map, key_mapper)
        print(f"  {v_name:<22} {len(node_map):>9,} {iters:>12,} {exploit:>10.5f}")


if __name__ == "__main__":
    main()
