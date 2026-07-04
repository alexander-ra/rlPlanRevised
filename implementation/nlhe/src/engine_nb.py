"""Numba 6-max NLHE engine: flat int32 state, mirrors engine_ref.py exactly.

State is a single int32 vector of length SLEN so cloning is one array copy —
ideal for MCCFR external-sampling traversal in nogil threads. Every rule here
must match engine_ref.py; Gate G1 (test_engine_cross.py) drives identical
random action-index scripts through both engines and asserts equal payoffs.

Action encoding (must match legal_actions ordering):
  index 0..n_actions-1 into arrays filled by `legal_actions_nb`
  kind codes: 0 FOLD, 1 CALL/CHECK, 2 RAISE
"""
from __future__ import annotations

import numpy as np
from numba import njit

from cards import BINOM, combo_index7  # noqa: F401 (combo used via rank table path)

N = 6  # fixed 6-max; positions relative, seats rotated externally for eval

# --- flat state layout (int32) ---
O_STACK = 0          # [N]
O_COMMIT = 6         # [N]
O_SBET = 12          # [N] street_bet
O_FOLD = 18          # [N]
O_ALLIN = 24         # [N]
O_ACTED = 30         # [N]
O_BOARD = 36         # [5]
O_HOLES = 41         # [2N] seat*2
S_STREET = 53
S_TOACT = 54
S_CBET = 55
S_MINR = 56
S_RAISES = 57
S_BUTTON = 58
S_FIN = 59
SLEN = 60

# rules packed as float64 array for numba (ints stored as floats, exact for our
# magnitudes): [num_players, stack, sb, bb, ante, preflop_open_bb,
#               max_raises, n_fracs, frac0, frac1, ..., include_allin]
def pack_rules(rules):
    fr = list(rules.raise_fractions)
    arr = [float(rules.num_players), float(rules.starting_stack),
           float(rules.small_blind), float(rules.big_blind), float(rules.ante),
           float(rules.preflop_open_bb), float(rules.max_raises_per_street),
           float(len(fr))]
    arr += [float(x) for x in fr]
    arr += [1.0 if rules.include_allin else 0.0]
    arr += [1.0 if getattr(rules, "use_preflop_open", False) else 0.0]
    return np.array(arr, dtype=np.float64)

# rule field indices
R_NP = 0
R_STACK = 1
R_SB = 2
R_BB = 3
R_ANTE = 4
R_OPEN = 5
R_MAXR = 6
R_NFRAC = 7
R_FRAC0 = 8  # fractions start here; include_allin is last


@njit(cache=True, inline="always")
def _active(st, p):
    return st[O_FOLD + p] == 0 and st[O_ALLIN + p] == 0


@njit(cache=True)
def _next_to_act(st, start, include_current):
    n = N
    for i in range(n):
        q = (start + i) % n
        if i == 0 and not include_current:
            continue
        if _active(st, q):
            return q
    return -1


@njit(cache=True, inline="always")
def _put(st, p, amt):
    s = st[O_STACK + p]
    if amt > s:
        amt = s
    st[O_STACK + p] -= amt
    st[O_COMMIT + p] += amt
    st[O_SBET + p] += amt
    if st[O_STACK + p] == 0:
        st[O_ALLIN + p] = 1


@njit(cache=True)
def new_hand_nb(rules, holes, board, button):
    st = np.zeros(SLEN, dtype=np.int32)
    n = N
    stack0 = np.int32(rules[R_STACK])
    for p in range(n):
        st[O_STACK + p] = stack0
    for i in range(5):
        st[O_BOARD + i] = board[i]
    for p in range(n):
        st[O_HOLES + 2 * p] = holes[2 * p]
        st[O_HOLES + 2 * p + 1] = holes[2 * p + 1]
    st[S_BUTTON] = button
    ante = np.int32(rules[R_ANTE])
    if ante > 0:
        for p in range(n):
            _put(st, p, ante)
        for p in range(n):
            st[O_SBET + p] = 0
    sb = (button + 1) % n
    bb = (button + 2) % n
    _put(st, sb, np.int32(rules[R_SB]))
    _put(st, bb, np.int32(rules[R_BB]))
    st[S_CBET] = np.int32(rules[R_BB])
    st[S_MINR] = np.int32(rules[R_BB])
    st[S_RAISES] = 0
    st[S_STREET] = 0
    first = (button + 3) % n if n > 3 else (button + 1) % n
    nt = _next_to_act(st, first, True)
    st[S_TOACT] = nt
    st[S_FIN] = 0
    return st


@njit(cache=True)
def _sum_commit(st):
    t = 0
    for p in range(N):
        t += st[O_COMMIT + p]
    return t


@njit(cache=True)
def legal_actions_nb(st, rules, out_kind, out_amt):
    """Fill out_kind/out_amt (len>=8 each); return n_actions. Mirrors ref."""
    p = st[S_TOACT]
    n_np = int(rules[R_NP])
    bb = np.int32(rules[R_BB])
    m = 0
    call_to = st[S_CBET]
    sbet_p = st[O_SBET + p]
    call_amt = call_to - sbet_p
    stack = st[O_STACK + p]
    max_to = sbet_p + stack

    if call_amt > 0:
        out_kind[m] = 0
        out_amt[m] = 0
        m += 1
    # call/check
    out_kind[m] = 1
    out_amt[m] = call_to if call_to < max_to else max_to
    m += 1

    maxr = int(rules[R_MAXR])
    can_raise = (stack > call_amt) and (st[S_RAISES] < maxr)
    if can_raise:
        pot = _sum_commit(st)
        min_to = st[S_CBET] + st[S_MINR]
        nfrac = int(rules[R_NFRAC])
        # preflop open special (gated by use_preflop_open flag)
        use_open = rules[R_FRAC0 + int(rules[R_NFRAC]) + 1] > 0.5
        is_pre_open = (use_open and st[S_STREET] == 0
                       and st[S_CBET] == bb and st[S_RAISES] == 0)
        # gather candidate raise-to values into a small local buffer
        cand = np.empty(8, dtype=np.int64)
        nc = 0
        if is_pre_open:
            openbb = rules[R_OPEN] * bb
            cand[nc] = np.int64(openbb + 0.5)
            nc += 1
        for fi in range(nfrac):
            f = rules[R_FRAC0 + fi]
            rt = st[S_CBET] + np.int64(f * (pot + call_amt) + 0.5)
            cand[nc] = rt
            nc += 1
        # emit deduped, clamped raises
        for ci in range(nc):
            rt = cand[ci]
            if rt < min_to:
                rt = min_to
            if rt > max_to:
                rt = max_to
            if rt <= st[S_CBET]:
                continue
            dup = False
            for j in range(m):
                if out_kind[j] == 2 and out_amt[j] == rt:
                    dup = True
                    break
            if dup:
                continue
            out_kind[m] = 2
            out_amt[m] = rt
            m += 1
    # all-in shove
    if rules[int(R_FRAC0 + int(rules[R_NFRAC]))] > 0.5 and stack > 0:
        if max_to > st[S_CBET]:
            dup = False
            for j in range(m):
                if out_amt[j] == max_to and out_kind[j] == 2:
                    dup = True
                    break
            if not dup:
                out_kind[m] = 2
                out_amt[m] = max_to
                m += 1
    return m


@njit(cache=True)
def _num_alive(st):
    c = 0
    for p in range(N):
        if st[O_FOLD + p] == 0:
            c += 1
    return c


@njit(cache=True)
def _betting_closed(st):
    for p in range(N):
        if _active(st, p):
            if st[O_ACTED + p] == 0 or st[O_SBET + p] != st[S_CBET]:
                return False
    return True


@njit(cache=True)
def _return_uncalled(st):
    top = -1
    second = -1
    for p in range(N):
        v = st[O_SBET + p]
        if v > top:
            second = top
            top = v
        elif v > second:
            second = v
    if top > second and second >= 0:
        for p in range(N):
            if st[O_SBET + p] == top:
                refund = top - second
                st[O_STACK + p] += refund
                st[O_COMMIT + p] -= refund
                st[O_SBET + p] = second
                break


@njit(cache=True)
def _advance_street(st, rules):
    _return_uncalled(st)
    if _num_alive(st) <= 1:
        st[S_FIN] = 1
        return
    for p in range(N):
        st[O_SBET + p] = 0
        st[O_ACTED + p] = 0
    st[S_CBET] = 0
    st[S_MINR] = np.int32(rules[R_BB])
    st[S_RAISES] = 0
    if st[S_STREET] == 3:
        st[S_FIN] = 1
        return
    st[S_STREET] += 1
    active_cnt = 0
    for p in range(N):
        if _active(st, p):
            active_cnt += 1
    first = _next_to_act(st, (st[S_BUTTON] + 1) % N, True)
    if active_cnt <= 1 or first == -1:
        _advance_street(st, rules)
        return
    st[S_TOACT] = first


@njit(cache=True)
def apply_action_nb(st, rules, kind, to_amount):
    p = st[S_TOACT]
    if kind == 0:  # fold
        st[O_FOLD + p] = 1
    elif kind == 1:  # call/check
        _put(st, p, to_amount - st[O_SBET + p])
    else:  # raise
        inc = to_amount - st[S_CBET]
        _put(st, p, to_amount - st[O_SBET + p])
        if inc >= st[S_MINR]:
            st[S_MINR] = inc
            for q in range(N):
                if q != p and _active(st, q):
                    st[O_ACTED + q] = 0
        if st[O_SBET + p] > st[S_CBET]:
            st[S_CBET] = st[O_SBET + p]
        st[S_RAISES] += 1
    st[O_ACTED + p] = 1

    if _num_alive(st) <= 1:
        _return_uncalled(st)
        st[S_FIN] = 1
        return
    if _betting_closed(st):
        _advance_street(st, rules)
    else:
        nt = _next_to_act(st, p, False)
        st[S_TOACT] = nt
        if nt == -1:
            _advance_street(st, rules)


@njit(cache=True)
def _rank7_from(holes, seat, board, table, binom):
    a = np.empty(7, dtype=np.int64)
    a[0] = holes[2 * seat]
    a[1] = holes[2 * seat + 1]
    for i in range(5):
        a[2 + i] = board[i]
    # insertion sort 7
    for i in range(1, 7):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    ci = (binom[a[0], 1] + binom[a[1], 2] + binom[a[2], 3] + binom[a[3], 4]
          + binom[a[4], 5] + binom[a[5], 6] + binom[a[6], 7])
    return table[ci]


@njit(cache=True)
def payoffs_nb(st, table, binom, out):
    n = N
    for p in range(n):
        out[p] = -st[O_COMMIT + p]
    nalive = 0
    last_alive = -1
    for p in range(n):
        if st[O_FOLD + p] == 0:
            nalive += 1
            last_alive = p
    if nalive == 1:
        out[last_alive] += _sum_commit(st)
        return
    # strengths
    strength = np.full(n, -1, dtype=np.int64)
    for p in range(n):
        if st[O_FOLD + p] == 0:
            strength[p] = _rank7_from(st[O_HOLES:O_HOLES + 2 * n], p,
                                      st[O_BOARD:O_BOARD + 5], table, binom)
    # distinct commit levels ascending
    levels = np.empty(n, dtype=np.int64)
    nl = 0
    for p in range(n):
        c = st[O_COMMIT + p]
        if c > 0:
            found = False
            for j in range(nl):
                if levels[j] == c:
                    found = True
                    break
            if not found:
                levels[nl] = c
                nl += 1
    # sort levels
    for i in range(1, nl):
        key = levels[i]
        j = i - 1
        while j >= 0 and levels[j] > key:
            levels[j + 1] = levels[j]
            j -= 1
        levels[j + 1] = key
    button = st[S_BUTTON]
    prev = 0
    for li in range(nl):
        lvl = levels[li]
        contributors = 0
        for p in range(n):
            if st[O_COMMIT + p] >= lvl:
                contributors += 1
        pot_layer = (lvl - prev) * contributors
        best = -1
        for p in range(n):
            if st[O_FOLD + p] == 0 and st[O_COMMIT + p] >= lvl:
                if strength[p] > best:
                    best = strength[p]
        if best >= 0 and pot_layer > 0:
            nw = 0
            for p in range(n):
                if st[O_FOLD + p] == 0 and st[O_COMMIT + p] >= lvl and strength[p] == best:
                    nw += 1
            share = pot_layer // nw
            rem = pot_layer - share * nw
            for p in range(n):
                if st[O_FOLD + p] == 0 and st[O_COMMIT + p] >= lvl and strength[p] == best:
                    out[p] += share
            # odd chips: earliest seat left of button among winners
            given = 0
            off = 0
            while given < rem:
                q = (button + 1 + off) % n
                if st[O_FOLD + q] == 0 and st[O_COMMIT + q] >= lvl and strength[q] == best:
                    out[q] += 1
                    given += 1
                off += 1
                if off > 2 * n:
                    break
        prev = lvl
