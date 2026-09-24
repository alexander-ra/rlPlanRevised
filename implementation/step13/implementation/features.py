"""
features.py -- turn one parsed hand (phh_parser.HandRec) into flat rows (raw step 13, Day 2
"feature engineering"; Day 1 "state tensor encoder"; Day 5 "collusion" inputs).

Three row types come out of every hand:

  seat rows      one per player per hand: the per-hand flags behind the HUD statistics
                 (VPIP, PFR, 3-bet, c-bet, WTSD ...) with their *opportunities*, so a statistic
                 is always (count / opportunities) and can be thresholded on opportunities.
  decision rows  one per action: the public state the actor faced + the action class. This is
                 the behavioural-cloning dataset and the token stream for player2vec.
  pair rows      one per pair of players in the hand: shared hand, heads-up confrontation
                 counts (decisions / bets-raises / folds each), and the chip flow between the
                 two. This is the collusion detector's input.

Definitions follow the usual tracker conventions (PokerTracker-style); the exact rule for each
opportunity is in the comments below, because that is where two trackers usually disagree.
"""
from __future__ import annotations

import numpy as np

from config import CALL, CHECK, FOLD
from phh_parser import BTN, CO, SB, HandRec

RANK_IDX = {r: i for i, r in enumerate("23456789TJQKA")}
SUIT_IDX = {s: i for i, s in enumerate("cdhs")}

# ---- column layouts -----------------------------------------------------------------------
SEAT_COLS = [
    "hand", "pid", "seat", "pos", "n",
    "vpip", "pfr", "limp", "rfi_opp", "rfi", "steal_opp", "steal",
    "tb_opp", "tb", "f3b_opp", "f3b",
    "saw_flop", "cbet_opp", "cbet", "fcb_opp", "fcb", "donk_opp", "donk", "cr_opp", "cr",
    "post_br", "post_call", "post_fold", "post_check", "wtsd", "wsd_known", "wsd_won",
    "won_nosd", "resolved",
]
SEAT_F = ["net", "contrib", "open_to", "post_size_sum", "post_size_n"]

DEC_COLS = [
    "hand", "pid", "seat", "street", "pos", "n", "n_active", "n_behind", "n_raises", "cls",
    "my_prev", "in_pos", "is_pfa", "pfa_live", "was_aggr", "facing",
    "b_paired", "b_suit", "b_top", "b_conn", "h1", "h2",
]
DEC_F = ["pot", "to_call", "size_frac", "cur_bet"]

PAIR_COLS = ["a", "b", "shared", "hu", "dec_a", "aggr_a", "fold_a", "dec_b", "aggr_b", "fold_b"]
PAIR_F = ["flow", "flow_sq", "hu_flow", "hu_flow_sq"]


def card_int(c: str) -> int:
    return RANK_IDX[c[0]] * 4 + SUIT_IDX[c[1]]


def board_feats(board: list[str]) -> tuple[int, int, int, int]:
    """(paired, max suit count, top rank 0-12, connectedness = max distinct ranks in a 5-window)."""
    if not board:
        return 0, 0, -1, 0
    ranks = [RANK_IDX[c[0]] for c in board]
    suits = [c[1] for c in board]
    paired = int(len(set(ranks)) < len(ranks))
    max_suit = max(suits.count(s) for s in set(suits))
    rs = set(ranks) | ({-1} if 12 in ranks else set())  # wheel ace
    conn = max(len([r for r in rs if lo <= r < lo + 5]) for lo in range(-1, 9))
    return paired, max_suit, max(ranks), conn


def hand_rows(h: HandRec, pids: list[int], hand_row: int):
    """Return (seat_int, seat_f, dec_int, dec_f, pair_int, pair_f) lists for one hand."""
    n = h.n
    acts = h.actions
    # ---------------- seat flags ----------------
    S = {k: [0] * n for k in SEAT_COLS[5:]}
    F = {k: [0.0] * n for k in SEAT_F}
    first_pf = [None] * n            # first pre-flop decision per player
    opener = -1                      # first pre-flop raiser
    entered = False                  # someone has voluntarily entered pre-flop (limp or raise)
    flop_first = [True] * n
    flop_bettor = -1                 # who made the first flop bet
    fcb_seen = [False] * n
    tb_seen = [False] * n
    f3b_seen = [False] * n
    checked_this_street = [False] * n
    cur_street = 0
    for r in acts:
        i = r.actor
        if r.street != cur_street:
            cur_street = r.street
            checked_this_street = [False] * n
        if r.street == 0:
            if r.kind == "cbr":
                S["vpip"][i] = 1
                S["pfr"][i] = 1
            elif r.kind == "cc" and r.to_call > 0:
                S["vpip"][i] = 1
            if first_pf[i] is None:
                first_pf[i] = r
                if r.n_raises == 0 and not entered:
                    S["rfi_opp"][i] = 1
                    if r.kind == "cbr":
                        S["rfi"][i] = 1
                        F["open_to"][i] = r.to
                    if h.positions[i] in (CO, BTN, SB) and n > 2:
                        S["steal_opp"][i] = 1
                        S["steal"][i] = int(r.kind == "cbr")
                if r.kind == "cc" and r.to_call > 0 and r.n_raises == 0:
                    S["limp"][i] = 1
            # 3-bet opportunity: facing exactly one raise, not the raiser
            if r.n_raises == 1 and i != opener and not tb_seen[i]:
                tb_seen[i] = True
                S["tb_opp"][i] = 1
                S["tb"][i] = int(r.kind == "cbr")
            # fold to 3-bet: the opener facing a re-raise
            if i == opener and r.n_raises == 2 and not f3b_seen[i]:
                f3b_seen[i] = True
                S["f3b_opp"][i] = 1
                S["f3b"][i] = int(r.kind == "f")
            if r.kind == "cbr" and opener < 0:
                opener = i
            if r.kind == "cbr" or (r.kind == "cc" and r.to_call > 0):
                entered = True
        else:
            pfa = r.pf_aggressor
            if r.street == 1:
                if flop_first[i]:
                    flop_first[i] = False
                    if i == pfa and r.n_raises == 0:
                        S["cbet_opp"][i] = 1
                        S["cbet"][i] = int(r.kind == "cbr")
                    if (i != pfa and pfa >= 0 and r.n_raises == 0
                            and not _folded_before(acts, pfa, r) and not _acted_on(acts, pfa, 1, r)):
                        S["donk_opp"][i] = 1
                        S["donk"][i] = int(r.kind == "cbr")
                if (flop_bettor == pfa and pfa >= 0 and i != pfa and r.n_raises == 1
                        and not fcb_seen[i]):
                    fcb_seen[i] = True
                    S["fcb_opp"][i] = 1
                    S["fcb"][i] = int(r.kind == "f")
                if r.kind == "cbr" and flop_bettor < 0:
                    flop_bettor = i
            if checked_this_street[i] and r.to_call > 0:
                S["cr_opp"][i] += 1
                S["cr"][i] += int(r.kind == "cbr")
            if r.kind == "cbr":
                S["post_br"][i] += 1
                F["post_size_sum"][i] += min(r.size_frac, 5.0)
                F["post_size_n"][i] += 1
            elif r.kind == "cc" and r.to_call > 0:
                S["post_call"][i] += 1
            elif r.kind == "cc":
                S["post_check"][i] += 1
                checked_this_street[i] = True
            else:
                S["post_fold"][i] += 1
    resolved = h.resolution != "showdown_unknown"
    for i in range(n):
        S["saw_flop"][i] = int(h.saw_street[i] >= 1)
        S["wtsd"][i] = int(h.saw_street[i] >= 1 and h.showdown[i])
        if h.showdown[i] and h.resolution == "showdown_known":
            S["wsd_known"][i] = 1
            S["wsd_won"][i] = int(h.win[i] > 0)
        if h.resolution == "uncontested" and h.net[i] > 0:
            S["won_nosd"][i] = 1
        S["resolved"][i] = int(resolved)
        F["net"][i] = h.net[i]
        F["contrib"][i] = h.contrib[i]
    seat_int = [[hand_row, pids[i], i, h.positions[i], n] + [S[k][i] for k in SEAT_COLS[5:]]
                for i in range(n)]
    seat_f = [[F[k][i] for k in SEAT_F] for i in range(n)]

    # ---------------- decision rows ----------------
    dec_int, dec_f = [], []
    board_by_street = [[], h.board[:3], h.board[:4], h.board[:5]]
    bf = [board_feats(b) for b in board_by_street]
    live = set(range(n))
    for r in acts:
        i = r.actor
        hc = h.hole.get(i)
        h1, h2 = (card_int(hc[:2]), card_int(hc[2:4])) if hc else (-1, -1)
        facing = 0 if r.to_call <= 0 else (1 if r.n_raises <= 1 else 2)
        pfa = r.pf_aggressor
        dec_int.append([
            hand_row, pids[i], i, r.street, h.positions[i], n, r.n_active, r.n_behind,
            min(r.n_raises, 4), r.cls, r.my_prev, int(r.in_position), int(i == pfa),
            int(r.street > 0 and pfa >= 0 and pfa in live), int(r.prev_street_aggr == i), facing,
            *bf[r.street], h1, h2,
        ])
        dec_f.append([r.pot_before, r.to_call, r.size_frac if r.kind == "cbr" else np.nan,
                      r.cur_bet])
        if r.kind == "f":
            live.discard(i)

    # ---------------- pair rows ----------------
    pot = sum(h.contrib)
    share = [w / pot if pot > 0 else 0.0 for w in h.win]
    hu_pair = None
    hu_start = None
    live = set(range(n))
    if n == 2:
        hu_pair, hu_start = (0, 1), 0
    else:
        for k, r in enumerate(acts):
            if r.kind == "f":
                live.discard(r.actor)
                if len(live) == 2 and k + 1 < len(acts):
                    hu_pair, hu_start = tuple(sorted(live)), k + 1
                    break
    hu_cnt = {}
    if hu_pair is not None:
        for r in acts[hu_start:]:
            d = hu_cnt.setdefault(r.actor, [0, 0, 0])
            d[0] += 1
            d[1] += int(r.kind == "cbr")
            d[2] += int(r.kind == "f")
    pair_int, pair_f = [], []
    for a in range(n):
        for b in range(a + 1, n):
            pa, pb = pids[a], pids[b]
            flow = h.contrib[a] * share[b] - h.contrib[b] * share[a]   # chips a -> b
            is_hu = hu_pair == (a, b) and (a in hu_cnt or b in hu_cnt)
            ca = hu_cnt.get(a, [0, 0, 0]) if is_hu else [0, 0, 0]
            cb = hu_cnt.get(b, [0, 0, 0]) if is_hu else [0, 0, 0]
            if pa > pb:  # canonical order: a < b by global id
                pa, pb, ca, cb, flow = pb, pa, cb, ca, -flow
            pair_int.append([pa, pb, 1, int(is_hu), *ca, *cb])
            hf = flow if is_hu else 0.0
            pair_f.append([flow, flow * flow, hf, hf * hf])
    return seat_int, seat_f, dec_int, dec_f, pair_int, pair_f


def _acted_on(acts, player, street, before) -> bool:
    for r in acts:
        if r is before:
            return False
        if r.street == street and r.actor == player:
            return True
    return False


def _folded_before(acts, player, before) -> bool:
    for r in acts:
        if r is before:
            return False
        if r.actor == player and r.kind == "f":
            return True
    return False
