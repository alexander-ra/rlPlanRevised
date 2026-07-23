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

import default_policy
import engine_nb as EN
import mccfr
from actions import infoset_hash
from indexer import canonical_key, key_to_class

ART = Path(__file__).resolve().parents[1] / "artifacts"

BLUEPRINT, RANDOM, CALLING_STATION, TAG = 0, 1, 2, 3


@njit(cache=True)
def _blueprint_strategy(st, p, slot_key, stratsum, kpre, bpre, kflop, bflop,
                        kturn, bturn, kriver, briver, binom, perms, n, out,
                        use_defaults, ok, n_buckets, eq_street):
    """Average strategy for seat p at this node -> out[0:n].

    use_defaults: 0 = UNIFORM fallback (byte-identical to the original live
    behaviour). 1 = A2 nearest-visited-bucket -> A1 pot-odds heuristic. 2 = A2
    only (borrow a learned neighbour, else UNIFORM — no A1). 3 = SANE-PASSIVE
    fallback: one-hot on action index 0 (= fold if facing a bet, else check;
    `legal_actions_nb` always emits the most-passive action first) on
    unseen/zero-mass nodes, while TRAINED nodes keep their mixed average. This
    isolates 'fix the fallback' from 'argmax the trained mixes' for the fork
    diagnosis. Trained infosets are unchanged in all modes. `ok`/`n_buckets`/
    `eq_street` are read only off-path.

    Returns 1 if this decision used a FALLBACK path (unseen node / zero average
    mass -> default policy, incl. A2 borrow), else 0 (a genuinely trained table
    row). The caller accumulates these to report per-eval 'fraction of actions
    played by the untrained/unknown policy' (coverage-in-play)."""
    bucket = mccfr.player_bucket(st, p, kpre, bpre, kflop, bflop, kturn, bturn,
                                 kriver, briver, binom, perms)
    h = infoset_hash(st, bucket)
    slot = mccfr.table_find(slot_key, h)
    if slot < 0:
        if use_defaults == 3:  # sane-passive one-hot (fold-if-facing / else check)
            for a in range(n):
                out[a] = 0.0
            out[0] = 1.0
            return 1
        if use_defaults != 0:
            my_eq = eq_street[bucket]
            if default_policy.nearest_bucket_strategy(
                    st, n_buckets, my_eq, eq_street, slot_key, stratsum, n, out):
                return 1
            if use_defaults == 1:  # A2 miss: ==1 -> A1 heuristic; ==2 -> uniform (A2-only)
                default_policy.heuristic_default(st, p, n, ok, my_eq, out)
                return 1
        for a in range(n):
            out[a] = 1.0 / n
        return 1
    tot = 0.0
    for a in range(n):
        v = stratsum[slot, a]
        out[a] = v if v > 0 else 0.0
        tot += out[a]
    if tot <= 0:
        if use_defaults == 3:  # sane-passive one-hot (fold-if-facing / else check)
            for a in range(n):
                out[a] = 0.0
            out[0] = 1.0
            return 1
        if use_defaults != 0:
            my_eq = eq_street[bucket]
            if default_policy.nearest_bucket_strategy(
                    st, n_buckets, my_eq, eq_street, slot_key, stratsum, n, out):
                return 1
            if use_defaults == 1:  # A2 miss: ==1 -> A1 heuristic; ==2 -> uniform (A2-only)
                default_policy.heuristic_default(st, p, n, ok, my_eq, out)
                return 1
        for a in range(n):
            out[a] = 1.0 / n
        return 1
    else:
        for a in range(n):
            out[a] /= tot
        return 0


@njit(cache=True)
def _purify_strategy(strat, n, mode, thresh):
    """In-place post-process of strat[0:n] (already a valid distribution).

    mode 0 = off (no-op; byte-identical to unpurified). mode 1 = drop mass
    below `thresh` and renormalize (falls back to argmax if everything is
    filtered, which cannot happen at n<=4 with thresh<=0.5 but is guarded
    anyway). mode 2 = argmax (deterministic one-hot on the top action)."""
    if mode == 0:
        return
    if mode == 2:
        best = 0
        bv = strat[0]
        for a in range(1, n):
            if strat[a] > bv:
                bv = strat[a]
                best = a
        for a in range(n):
            strat[a] = 1.0 if a == best else 0.0
        return
    tot = 0.0
    for a in range(n):
        if strat[a] < thresh:
            strat[a] = 0.0
        tot += strat[a]
    if tot <= 0.0:
        best = 0
        bv = strat[0]
        for a in range(1, n):
            if strat[a] > bv:
                bv = strat[a]
                best = a
        for a in range(n):
            strat[a] = 1.0 if a == best else 0.0
    else:
        for a in range(n):
            strat[a] /= tot


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
            slot_key, stratsum, arts, eqs, binom, perms, tag_thresh, use_defaults,
            purify_mode, purify_thresh, counts):
    """Return chosen action index for the acting seat. `counts` (int64[2]) is
    accumulated ONLY for the blueprint seat: counts[0]=total decisions,
    counts[1]=decisions that fell back to the untrained/default policy."""
    (kpre, bpre, kflop, bflop, kturn, bturn, kriver, briver) = arts
    (mpre, mflop, mturn, mriver) = eqs
    if seat_type == BLUEPRINT:
        s = st[EN.S_STREET]
        if s == 0:
            eq_street = mpre
        elif s == 1:
            eq_street = mflop
        elif s == 2:
            eq_street = mturn
        else:
            eq_street = mriver
        n_buckets = eq_street.shape[0]
        fb = _blueprint_strategy(st, p, slot_key, stratsum, kpre, bpre, kflop, bflop,
                            kturn, bturn, kriver, briver, binom, perms, n, strat_buf,
                            use_defaults, ok, n_buckets, eq_street)
        counts[0] += 1
        counts[1] += fb
        _purify_strategy(strat_buf, n, purify_mode, purify_thresh)
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
              arts, eqs, binom, perms, rank, tag_thresh, out_payoff, use_defaults,
              purify_mode, purify_thresh, counts):
    st = EN.new_hand_nb(rules, holes, board, button)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    strat_buf = np.empty(8, dtype=np.float64)
    while st[EN.S_FIN] == 0:
        p = st[EN.S_TOACT]
        n = EN.legal_actions_nb(st, rules, ok, oa)
        a = _choose(seat_types[p], st, p, rules, ok, oa, n, strat_buf,
                    slot_key, stratsum, arts, eqs, binom, perms, tag_thresh,
                    use_defaults, purify_mode, purify_thresh, counts)
        EN.apply_action_nb(st, rules, int(ok[a]), int(oa[a]))
    EN.payoffs_nb(st, rank, binom, out_payoff)


def _bfile(street, n):
    """Size-suffixed bucket-assignment file (bucket_flop_100.npy) if it exists,
    else the unsuffixed default — mirrors mccfr.load_artifacts so eval and
    training agree on buckets for any configured size."""
    p = ART / f"bucket_{street}_{n}.npy"
    return p if p.exists() else ART / f"bucket_{street}.npy"


def _bucket_mean_equity(buckets_cfg=None):
    """Per-street per-bucket mean equity (cached artifact for TAG), for the
    bucket sizes in `buckets_cfg` (so small-game evals use their own buckets).
    buckets_cfg=None -> live default.json's buckets (matches `_cfg_or_default`'s
    pattern; `distill.collect_dataset` calls this with no args)."""
    if buckets_cfg is None:
        buckets_cfg = _cfg_or_default(None)["buckets"]
    out = {}
    # river: mean equity per bucket from river_equity + bucket_river
    for street in ["river"]:
        eq = np.load(ART / "river_equity.npy")
        b = np.load(_bfile("river", buckets_cfg["river"]))
        nb = int(b.max()) + 1
        s = np.bincount(b, weights=eq, minlength=nb)
        c = np.bincount(b, minlength=nb)
        out["river"] = (s / np.maximum(c, 1)).astype(np.float32)
    # turn/flop: mean of the histogram-implied equity (bin centers) per bucket
    for street, cdf_f in [("turn", "turn_cdf.npy"), ("flop", "flop_cdf.npy")]:
        cdf = np.load(ART / cdf_f)  # (N, bins-1) cumulative
        buck = np.load(_bfile(street, buckets_cfg[street]))
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


def _cfg_or_default(cfg):
    if cfg is not None:
        return cfg
    import json
    return json.loads((Path(__file__).resolve().parents[1] /
                       "config" / "default.json").read_text())


def load_eval_artifacts(cfg=None):
    cfg = _cfg_or_default(cfg)
    A = mccfr.load_artifacts(cfg["buckets"])
    arts = (A["kpre"], A["bpre"], A["kflop"], A["bflop"],
            A["kturn"], A["bturn"], A["kriver"], A["briver"])
    me = _bucket_mean_equity(cfg["buckets"])
    pf_cache = ART / "preflop_equity.npy"
    if pf_cache.exists():
        mpre = np.load(pf_cache)
    else:
        mpre = _preflop_mean_equity()
        np.save(pf_cache, mpre)
    eqs = (mpre, me["flop"], me["turn"], me["river"])
    return A, arts, eqs


def duplicate_match(slot_key, stratsum, baseline, n_decks=10000, seed=123,
                    tag_thresh=0.5, bb=2, use_defaults=0, cfg=None,
                    purify_mode=0, purify_thresh=0.0):
    """Blueprint (seat rotates through all 6) vs 5 baseline copies on shared
    decks. Returns (bb_per_100, ci95, preflop_raise_freq dict).

    use_defaults: 0 = uniform fallback at untrained infosets (default, live
    behaviour). Non-zero = A1+A2 output-side default policy (proposal A).
    cfg: config dict (game rules + buckets); None -> live default.json.

    `stratsum` is generic: pass the average-strategy table for the deployed
    (average) policy, or the `regret` table for the current/regret-matched
    policy (Phase 7A item 0) — `_blueprint_strategy` positive-part-normalizes
    whichever array it is given, so no other code path differs.
    purify_mode/purify_thresh: 0 = off (byte-identical), 1 = drop mass below
    `purify_thresh` and renormalize, 2 = argmax (deterministic top action).

    Third return value is a stats dict: `fallback_frac` = fraction of the
    blueprint's decisions that used the untrained/default (fallback) policy
    rather than a genuinely trained table row (coverage-in-play), plus the raw
    `n_decisions` / `n_fallback` counts."""
    cfg = _cfg_or_default(cfg)
    A, arts, eqs = load_eval_artifacts(cfg)
    rules = _rules_arr(cfg)
    bb = cfg["game"]["big_blind"]
    rank = A["rank"]
    binom = A["binom"]
    perms = A["perms"]
    rng = np.random.default_rng(seed)
    per_deck = np.zeros(n_decks, dtype=np.float64)
    out_payoff = np.zeros(EN.N, dtype=np.int64)
    seat_types = np.full(EN.N, baseline, dtype=np.int64)
    counts = np.zeros(2, dtype=np.int64)  # [total blueprint decisions, fallback ones]
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
                      arts, eqs, binom, perms, rank, tag_thresh, out_payoff,
                      int(use_defaults), int(purify_mode), float(purify_thresh),
                      counts)
            deck_total += out_payoff[seat]
        per_deck[d] = deck_total / EN.N  # avg blueprint result over rotations
    bb100 = per_deck.mean() / bb * 100.0
    ci = 1.96 * per_deck.std() / np.sqrt(n_decks) / bb * 100.0
    n_dec = int(counts[0])
    stats = {"n_decisions": n_dec, "n_fallback": int(counts[1]),
             "fallback_frac": (float(counts[1]) / n_dec) if n_dec > 0 else 0.0}
    return bb100, ci, stats


def _rules_arr(cfg=None):
    import engine_ref as ER
    cfg = _cfg_or_default(cfg)
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
