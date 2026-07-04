"""Evaluation: blueprint vs baseline bots in duplicate-seat matches -> bb/100.

Agents (seat_type codes):
  0 BLUEPRINT      — average strategy from the MCCFR table (stratsum)
  1 RANDOM         — legal action weighted fold10/call60/raise30
  2 CALLING_STATION— always check/call (never folds, never raises)
  3 TAG            — tight-aggressive by a per-bucket mean-equity threshold

Duplicate seating: the blueprint plays each deck once in every seat rotation
against copies of one baseline, cancelling card luck. bb/100 aggregates per-deck
results (the i.i.d. unit) with a 95% CI. Also dumps the 169-class preflop raise
frequency for the dashboard heatmap.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from numba import njit

import engine_nb as EN
import mccfr
from actions import infoset_hash
from indexer import canonical_key, key_to_class

ART = Path(__file__).resolve().parents[1] / "artifacts"

BLUEPRINT, RANDOM, CALLING_STATION, TAG = 0, 1, 2, 3


@njit(cache=True)
def _blueprint_strategy(st, p, slot_key, stratsum, kpre, bpre, kflop, bflop,
                        kturn, bturn, kriver, briver, binom, perms, n, out):
    """Average strategy for seat p at this node -> out[0:n]. Uniform if unseen."""
    bucket = mccfr.player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                                 kriver, briver, binom, perms)
    h = infoset_hash(st, bucket)
    slot = mccfr.table_find(slot_key, h)
    if slot < 0:
        for a in range(n):
            out[a] = 1.0 / n
        return
    tot = 0.0
    for a in range(n):
        v = stratsum[slot, a]
        out[a] = v if v > 0 else 0.0
        tot += out[a]
    if tot <= 0:
        for a in range(n):
            out[a] = 1.0 / n
    else:
        for a in range(n):
            out[a] /= tot


@njit(cache=True)
def _seat_equity(st, p, kpre, bpre, mpre, kflop, bflop, mflop,
                 kturn, bturn, mturn, kriver, briver, mriver, binom, perms):
    """Mean equity of seat p's bucket at the current street (TAG proxy).

    NOTE: the mean-equity arrays are indexed by BUCKET, so we must map the
    canonical class -> bucket first (via player_bucket). Indexing them by the
    raw class was an out-of-bounds bug that segfaulted the process."""
    bucket = mccfr.player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                                 kriver, briver, binom, perms)
    s = st[EN.S_STREET]
    if s == 0:
        return mpre[bucket]
    elif s == 1:
        return mflop[bucket]
    elif s == 2:
        return mturn[bucket]
    else:
        return mriver[bucket]


@njit(cache=True)
def _choose(seat_type, st, p, rules, ok, oa, n, strat_buf,
            slot_key, stratsum, arts, eqs, binom, perms, tag_thresh):
    """Return chosen action index for the acting seat."""
    (kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver) = arts
    (mpre, mflop, mturn, mriver) = eqs
    if seat_type == BLUEPRINT:
        _blueprint_strategy(st, p, slot_key, stratsum, kpre, bpre, kflop, bflop,
                            kturn, bturn, kriver, briver, binom, perms, n, strat_buf)
        r = np.random.random()
        c = 0.0
        for a in range(n):
            c += strat_buf[a]
            if r < c:
                return a
        return n - 1
    if seat_type == CALLING_STATION:
        for a in range(n):
            if ok[a] == 1:  # call/check
                return a
        return 0
    if seat_type == RANDOM:
        # weighted fold .1 / call .6 / raise .3 over available kinds
        wsum = 0.0
        w = np.zeros(n)
        for a in range(n):
            if ok[a] == 0:
                w[a] = 0.1
            elif ok[a] == 1:
                w[a] = 0.6
            else:
                w[a] = 0.3
            wsum += w[a]
        r = np.random.random() * wsum
        c = 0.0
        for a in range(n):
            c += w[a]
            if r < c:
                return a
        return n - 1
    # TAG: raise if strong, call if medium, fold if weak & facing bet
    eq = _seat_equity(st, p, kpre, bpre, mpre, kflop, bflop, mflop,
                      kturn, bturn, mturn, kriver, briver, mriver, binom, perms)
    facing = False
    for a in range(n):
        if ok[a] == 0:
            facing = True
    if eq >= tag_thresh + 0.15:  # strong -> raise (largest non-allin, else call)
        best = -1
        for a in range(n):
            if ok[a] == 2:
                best = a
        if best >= 0:
            return best
    if eq >= tag_thresh:  # medium -> call/check
        for a in range(n):
            if ok[a] == 1:
                return a
    if facing:  # weak, facing bet -> fold
        for a in range(n):
            if ok[a] == 0:
                return a
    for a in range(n):  # weak, can check
        if ok[a] == 1:
            return a
    return 0


@njit(cache=True)
def play_hand(seat_types, holes, board, button, rules, slot_key, stratsum,
              arts, eqs, binom, perms, rank, tag_thresh, out_payoff):
    st = EN.new_hand_nb(rules, holes, board, button)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    strat_buf = np.empty(8, dtype=np.float64)
    while st[EN.S_FIN] == 0:
        p = st[EN.S_TOACT]
        n = EN.legal_actions_nb(st, rules, ok, oa)
        a = _choose(seat_types[p], st, p, rules, ok, oa, n, strat_buf,
                    slot_key, stratsum, arts, eqs, binom, perms, tag_thresh)
        EN.apply_action_nb(st, rules, int(ok[a]), int(oa[a]))
    EN.payoffs_nb(st, rank, binom, out_payoff)


def _bucket_mean_equity():
    """Per-street per-bucket mean equity (cached artifact for TAG)."""
    out = {}
    # river: mean equity per bucket from river_equity + bucket_river
    for street, kf, bf in [("river", "river_equity.npy", "bucket_river.npy")]:
        eq = np.load(ART / "river_equity.npy")
        b = np.load(ART / "bucket_river.npy")
        nb = int(b.max()) + 1
        s = np.bincount(b, weights=eq, minlength=nb)
        c = np.bincount(b, minlength=nb)
        out["river"] = (s / np.maximum(c, 1)).astype(np.float32)
    # turn/flop: mean of the histogram-implied equity (bin centers) per bucket
    for street, cdf_f, buck_f in [("turn", "turn_cdf.npy", "bucket_turn.npy"),
                                  ("flop", "flop_cdf.npy", "bucket_flop.npy")]:
        cdf = np.load(ART / cdf_f)  # (N, bins-1) cumulative
        buck = np.load(ART / buck_f)
        bins = cdf.shape[1] + 1
        centers = (np.arange(bins) + 0.5) / bins
        # recover histogram from cdf: h[0]=cdf[0], h[i]=cdf[i]-cdf[i-1], last=1-cdf[-1]
        full = np.concatenate([cdf, np.ones((cdf.shape[0], 1), np.float32)], axis=1)
        hist = np.diff(np.concatenate([np.zeros((cdf.shape[0], 1), np.float32),
                                       full], axis=1), axis=1)
        mean_eq = (hist * centers).sum(1)
        nb = int(buck.max()) + 1
        s = np.bincount(buck, weights=mean_eq, minlength=nb)
        c = np.bincount(buck, minlength=nb)
        out[street] = (s / np.maximum(c, 1)).astype(np.float32)
    # preflop: mean equity per 169 class (each class its own bucket)
    return out


def _preflop_mean_equity(samples=20000, seed=0):
    """Monte-Carlo equity vs one random opponent for each 169 preflop class."""
    import cards as C
    from indexer import decode_key, SUIT_PERMS
    from cards import BINOM
    binom = BINOM.astype(np.int64)
    keys = np.load(ART / "keys_preflop.npy")
    rank = np.load(ART / "rank7.npy")
    rng = np.random.default_rng(seed)
    out = np.empty(len(keys), dtype=np.float32)
    tmp = np.empty(2, dtype=np.int64)
    for i, key in enumerate(keys):
        decode_key(int(key), 0, binom, tmp)
        h0, h1 = int(tmp[0]), int(tmp[1])
        wins = 0.0
        for _ in range(samples):
            deck = rng.permutation(52)
            deck = deck[(deck != h0) & (deck != h1)]
            o0, o1 = int(deck[0]), int(deck[1])
            board = deck[2:7]
            our = C.PHEVAL_MAX - _pv(h0, h1, board)
            opp = C.PHEVAL_MAX - _pv(o0, o1, board)
            wins += 1.0 if our > opp else (0.5 if our == opp else 0.0)
        out[i] = wins / samples
    return out


def _pv(a, b, board):
    from phevaluator.evaluator import _evaluate_cards
    return _evaluate_cards(int(a), int(b), int(board[0]), int(board[1]),
                           int(board[2]), int(board[3]), int(board[4]))


def load_eval_artifacts():
    A = mccfr.load_artifacts()
    arts = (A["kpre"], A["bpre"], A["kflop"], A["bflop"],
            A["kturn"], A["bturn"], A["kriver"], A["briver"])
    me = _bucket_mean_equity()
    pf_cache = ART / "preflop_equity.npy"
    if pf_cache.exists():
        mpre = np.load(pf_cache)
    else:
        mpre = _preflop_mean_equity()
        np.save(pf_cache, mpre)
    eqs = (mpre, me["flop"], me["turn"], me["river"])
    return A, arts, eqs


def duplicate_match(slot_key, stratsum, baseline, n_decks=10000, seed=123,
                    tag_thresh=0.5, bb=2):
    """Blueprint (seat rotates through all 6) vs 5 baseline copies on shared
    decks. Returns (bb_per_100, ci95, preflop_raise_freq dict)."""
    A, arts, eqs = load_eval_artifacts()
    rules = _rules_arr()
    rank = A["rank"]
    binom = A["binom"]
    perms = A["perms"]
    rng = np.random.default_rng(seed)
    per_deck = np.zeros(n_decks, dtype=np.float64)
    out_payoff = np.zeros(EN.N, dtype=np.int64)
    seat_types = np.full(EN.N, baseline, dtype=np.int64)
    for d in range(n_decks):
        deck = rng.permutation(52).astype(np.int32)
        holes = deck[:12].copy()
        board = deck[12:17].copy()
        deck_total = 0.0
        for seat in range(EN.N):
            st = seat_types.copy()
            st[seat] = BLUEPRINT
            button = d % EN.N
            play_hand(st, holes, board, button, rules, slot_key, stratsum,
                      arts, eqs, binom, perms, rank, tag_thresh, out_payoff)
            deck_total += out_payoff[seat]
        per_deck[d] = deck_total / EN.N  # avg blueprint result over rotations
    bb100 = per_deck.mean() / bb * 100.0
    ci = 1.96 * per_deck.std() / np.sqrt(n_decks) / bb * 100.0
    return bb100, ci, {}


def _rules_arr():
    import json
    import engine_ref as ER
    cfg = json.loads((Path(__file__).resolve().parents[1] /
                      "config" / "default.json").read_text())
    a = cfg["abstraction"]
    rules = ER.Rules(
        num_players=cfg["game"]["num_players"],
        starting_stack=cfg["game"]["starting_stack"],
        small_blind=cfg["game"]["small_blind"], big_blind=cfg["game"]["big_blind"],
        ante=cfg["game"]["ante"], raise_fractions=tuple(a["raise_fractions"]),
        include_allin=a["include_allin"], use_preflop_open=a["use_preflop_open"],
        preflop_open_bb=a["preflop_open_bb"],
        max_raises_per_street=a["max_raises_per_street"])
    return EN.pack_rules(rules)
