"""PROPOSAL B1 + B3 — flop-start (rejection) sampling + soft-freeze mix.

NOT wired in. To use: copy into ../../src/, then have the daemon train loop call
`run_batch_mixed(...)` instead of `mccfr.run_batch(...)`, passing
`full_game_fraction` from config (see ./README.md and ./config.diff.md).

Idea (from convo.txt): most hands fold preflop, so most iterations only re-train
the already-converged preflop trunk. Flop-start plays preflop with the CURRENT
strategy (all seats just sample, no updates), throws away hands that end preflop,
and runs the normal learning traversal from the flop. Because the ranges entering
the flop are self-consistent with the current trunk, the postflop regrets
converge to the right values — no importance weights, no bias (this is B1). A
`full_game_fraction` of ordinary full-game iterations (B3 soft-freeze) keeps the
preflop trunk adapting as postflop tightens.

Reuses mccfr's traverse/primitives unchanged — only the game START differs.
"""
from __future__ import annotations

import numpy as np
from numba import njit, prange

import engine_nb as EN
from actions import infoset_hash
from mccfr import (traverse, player_bucket, regret_matching, table_find,
                   _sample)


@njit(cache=True)
def _advance_to_flop(st, rules, slot_key, regret,
                     kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
                     binom, perms):
    """Sample preflop with the current regret-matched strategy (all seats,
    no updates) until the hand either ends or reaches the flop.

    Returns 1 if the flop was reached (st advanced, not terminal), else 0."""
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    strat = np.empty(8, dtype=np.float64)
    while st[EN.S_FIN] == 0 and st[EN.S_STREET] == 0:
        p = st[EN.S_TOACT]
        bucket = player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                               kriver, briver, binom, perms)
        h = infoset_hash(st, bucket)
        slot = table_find(slot_key, h)
        n = EN.legal_actions_nb(st, rules, ok, oa)
        if slot >= 0:
            regret_matching(regret[slot], n, strat)
        else:
            u = 1.0 / n
            for a in range(n):
                strat[a] = u
        a = _sample(strat, n, np.random.random())
        EN.apply_action_nb(st, rules, ok[a], oa[a])
    return 1 if st[EN.S_FIN] == 0 else 0


@njit(nogil=True, parallel=True, cache=True)
def run_batch_mixed(n_iters, start_iter, full_game_fraction,
                    rules, slot_key, regret, stratsum,
                    kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
                    rank, binom, perms, prune_below, prune_on):
    """Drop-in replacement for mccfr.run_batch with two iteration types:

      Type A (prob = full_game_fraction): ordinary full-game traversal (today's
              behaviour) — keeps the preflop trunk adapting (B3 soft-freeze).
      Type B (otherwise): rejection flop-start — sample preflop, discard hands
              that fold out, learn from the flop (B1).

    Same table-race semantics as run_batch (Pluribus-style accepted races)."""
    for it in prange(n_iters):
        gi = start_iter + it
        traverser = gi % EN.N
        button = 0
        deck = np.arange(52)
        for i in range(51, 0, -1):
            j = np.random.randint(0, i + 1)
            tmp = deck[i]
            deck[i] = deck[j]
            deck[j] = tmp
        holes = deck[:12].astype(np.int32)
        board = deck[12:17].astype(np.int32)
        st = EN.new_hand_nb(rules, holes, board, button)

        if np.random.random() < full_game_fraction:
            traverse(st, traverser, rules, slot_key, regret, stratsum,
                     kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver,
                     rank, binom, perms, 0, prune_below, prune_on)
        else:
            reached = _advance_to_flop(st, rules, slot_key, regret,
                                       kpre, bpre, kflop, bflop, kturn, bturn,
                                       kriver, briver, binom, perms)
            if reached == 1:
                traverse(st, traverser, rules, slot_key, regret, stratsum,
                         kpre, bpre, kflop, bflop, kturn, bturn,
                         kriver, briver, rank, binom, perms, 0,
                         prune_below, prune_on)
            # else: hand folded out preflop -> rejected (near-free, ~microseconds)
