"""
collusion.py -- synthetic collusion injected into real sessions, and a detector scored against
ground truth (raw step 13, Day 5 "Collusion Detection"; Validation: "Detects 100 % of injected
synthetic collusion at the chosen threshold. False positive rate on known-clean data < 5 %").

    python collusion.py            # seeds 0 1 2 -> results/collusion.json

INJECTION (real hands, rewritten, re-parsed, re-validated)
  Pick K pairs of REAL players who already share >= 300 hands and >= 30 heads-up confrontations
  (so co-occurrence is natural and cannot give them away). In a fraction q of the hands where the
  two end up heads-up against each other, the rest of the hand is rewritten from that point:
    soft play   both check or call to the end (no bet or raise against the partner)
    dumping     A bets the pot, B raises to three times, A folds: A's chips go to B
  Every rewritten hand is replayed by the parser (strict) and by pokerkit; both must accept it.

DETECTOR (per pair, from the pair table; the Chapter 11 help/harm idea, standardised)
  z_soft   Stouffer z of the two players' aggression deficit when heads-up against each other,
           relative to their own heads-up aggression against everyone else (harm withheld).
  z_dump   the chip flow between the two in their heads-up hands over its own root-sum-square
           (help given); |z| because the direction is unknown.
  union    max(z_soft, |z_dump|)
  ch11_raw the Chapter 11 score with poker events: C = net_ab + net_ba, net = help - harm with
           help = folds to the partner and harm = bets/raises at the partner, per heads-up decision.
  co_occ   shared hands / the smaller player's hands (reported; uninformative here by design).
Negatives are all other real pairs with >= 100 shared hands and >= 10 heads-up confrontations.
Their collusion status is unknown: they are *presumed* clean, which is the best available.
"""
from __future__ import annotations

import json
import sys
import time
import tomllib
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, DATA_ROOT, RESULTS, SEEDS  # noqa: E402
from features import PAIR_COLS, hand_rows  # noqa: E402
from phh_parser import ParseError, parse_hand  # noqa: E402
from validator import pk_check  # noqa: E402

RANKS, SUITS = "23456789TJQKA", "cdhs"
DECK = [r + s for r in RANKS for s in SUITS]
TYPES = ("soft", "dump")
QS = (0.1, 0.25, 0.5, 1.0)
K_PAIRS = 40


# ------------------------------------------------------------------ rewriting ---------------
def _fmt(x: float) -> str:
    return f"{round(x, 2):.2f}"


def hu_rewrite(raw: dict, a: int, b: int, kind: str, rng) -> dict | None:
    """Rewrite the hand from the point where only seats a and b are left. a = dumper for 'dump'."""
    acts = raw["actions"]
    pl_idx = [k for k, s in enumerate(acts) if not s.startswith("d ") and s.split()[1] != "sm"]
    rec = parse_hand(raw)
    n = rec.n
    live = set(range(n))
    k0 = 0 if n == 2 else None
    if k0 is None:
        for k, r in enumerate(rec.actions):
            if r.kind == "f":
                live.discard(r.actor)
                if len(live) == 2 and k + 1 < len(rec.actions):
                    k0 = k + 1
                    break
    if k0 is None or live != {a, b}:
        return None
    cut = pl_idx[k0] if k0 < len(pl_idx) else len(acts)
    prefix = acts[:cut]
    later_boards = [s for s in acts[cut:] if s.startswith("d db")]
    st = parse_hand({**raw, "actions": prefix}, prefix=True)
    street, cur_bet, sbet = st["street"], st["cur_bet"], st["street_bet"]
    last_raise, need, last_actor, order0 = st["last_raise"], set(st["need"]) & {a, b}, st["last_actor"], st["order0"]
    contrib = st["contrib"]
    known = set(st["board"])
    for h in st["hole"].values():
        known |= {h[i:i + 2] for i in range(0, len(h), 2)}
    for s in later_boards:
        c = s.split()[2]
        known |= {c[i:i + 2] for i in range(0, len(c), 2)}
    out = list(prefix)
    invested = {a: False, b: False}

    def nxt():
        order = order0 if street == 0 else list(range(n))
        if last_actor is None or last_actor not in order:
            for i in order:
                if i in need:
                    return i
            return None
        s0 = order.index(last_actor)
        for k in range(1, n + 1):
            i = order[(s0 + k) % n]
            if i in need:
                return i
        return None

    guard = 0
    while True:
        guard += 1
        if guard > 50:
            return None
        if not need:
            if street == 3:
                for i in (a, b):
                    h = st["hole"].get(i)
                    out.append(f"p{i + 1} sm {h if h else '????'}")
                break
            # deal the next street
            if later_boards:
                out.append(later_boards.pop(0))
            else:
                k = 3 if street == 0 else 1
                free = [c for c in DECK if c not in known]
                cs = list(rng.choice(free, k, replace=False))
                known |= set(cs)
                out.append("d db " + "".join(cs))
            street += 1
            cur_bet, sbet, last_raise, last_actor = 0.0, [0.0] * n, st["bb"], None
            need = {a, b}
            continue
        i = nxt()
        j = b if i == a else a
        to_call = cur_bet - sbet[i]
        pot = sum(contrib)
        act = None
        if kind == "soft":
            act = ("cc", None)
        elif kind == "dump":
            if i == a:   # the dumper
                if invested[a] and to_call > 0:
                    act = ("f", None)
                else:
                    act = ("cbr", cur_bet + pot + to_call)
            else:        # the receiver
                act = ("cbr", 3 * cur_bet) if to_call > 0 else ("cc", None)
        if act[0] == "f":
            out.append(f"p{i + 1} f")
            break
        if act[0] == "cc":
            pay = max(to_call, 0.0)
            contrib[i] += pay; sbet[i] += pay
            need.discard(i)
            out.append(f"p{i + 1} cc")
        else:
            to = round(act[1], 2)
            inc = to - cur_bet
            if inc < last_raise:
                to = round(cur_bet + last_raise, 2); inc = last_raise
            contrib[i] += to - sbet[i]; sbet[i] = to
            last_raise = max(last_raise, inc); cur_bet = to
            need = {j}
            invested[i] = True
            out.append(f"p{i + 1} cbr {_fmt(to)}")
        last_actor = i
    return {**raw, "actions": out}


# ------------------------------------------------------------------ detector ---------------
def load_pairs(which="all"):
    d = np.load(CACHE_ROOT / "IPN100" / ("pairs.npz" if which == "all" else "pairs_mw.npz"))
    return d["a"].astype(np.int64), d["b"].astype(np.int64), d["I"].astype(np.float64), d["F"].copy(), \
        {k: i for i, k in enumerate(d["icols"])}


def score(a, b, I, F, c, hands_pp):
    """All detector signals for every pair row."""
    n_players = int(max(a.max(), b.max())) + 1
    dec_tot = np.bincount(a, I[:, c["dec_a"]], n_players) + np.bincount(b, I[:, c["dec_b"]], n_players)
    agg_tot = np.bincount(a, I[:, c["aggr_a"]], n_players) + np.bincount(b, I[:, c["aggr_b"]], n_players)

    def soft_z(p, dec, agg):
        n_o = dec_tot[p] - dec
        rate = np.clip((agg_tot[p] - agg) / np.maximum(n_o, 1), 1e-3, 1 - 1e-3)
        exp = dec * rate
        return (exp - agg) / np.sqrt(np.maximum(dec * rate * (1 - rate), 1e-9))
    za = soft_z(a, I[:, c["dec_a"]], I[:, c["aggr_a"]])
    zb = soft_z(b, I[:, c["dec_b"]], I[:, c["aggr_b"]])
    z_soft = (za + zb) / np.sqrt(2)
    z_dump = F[:, 2] / np.sqrt(F[:, 3] + 1e-9)
    z_flow = F[:, 0] / np.sqrt(F[:, 1] + 1e-9)
    dec = I[:, c["dec_a"]] + I[:, c["dec_b"]]
    ch11 = ((I[:, c["fold_a"]] - I[:, c["aggr_a"]]) + (I[:, c["fold_b"]] - I[:, c["aggr_b"]])) / np.maximum(dec, 1)
    co = I[:, c["shared"]] / np.minimum(hands_pp[a], hands_pp[b])
    return {"z_soft": z_soft, "abs_z_dump": np.abs(z_dump), "abs_z_flow_all": np.abs(z_flow),
            "union": np.maximum(z_soft, np.abs(z_dump)), "ch11_raw": ch11, "co_occ": co}


def roc(scores, y):
    o = np.argsort(-scores, kind="stable")
    ys = y[o]
    tp = np.cumsum(ys); fp = np.cumsum(1 - ys)
    P, N = ys.sum(), len(ys) - ys.sum()
    tpr, fpr = tp / P, fp / N
    auc = float(np.trapezoid(np.concatenate([[0], tpr]), np.concatenate([[0], fpr])))
    out = {"auc": auc}
    for f in (0.001, 0.01, 0.05):
        k = np.searchsorted(fpr, f, side="right") - 1
        out[f"recall_at_fpr_{f}"] = float(tpr[k]) if k >= 0 else 0.0
    k90 = np.argmax(tpr >= 0.9)
    out["fpr_at_recall_0.9"] = float(fpr[k90])
    out["fpr_at_recall_1.0"] = float(fpr[np.argmax(tpr >= 1.0)])
    out["precision_at_P"] = float(ys[:int(P)].mean())
    return out


# ------------------------------------------------------------------ main -------------------
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", choices=["all", "mw"], default="all",
                    help="all tables, or multiway tables only (>= 3 seats; format-matched baseline)")
    args, _ = ap.parse_known_args()
    t0 = time.time()
    a, b, I0, F0, c = load_pairs(args.pairs)
    names = json.load(open(CACHE_ROOT / "IPN100" / "players.json"))
    pid_of = {p: i for i, p in enumerate(names)}
    files = json.load(open(CACHE_ROOT / "IPN100" / "files.json"))
    H = np.load(CACHE_ROOT / "IPN100" / "hands.npz")["H"]
    S = np.load(CACHE_ROOT / "IPN100" / "seats.npz")["I"]
    s_hand, s_pid = S[:, 0], S[:, 1]
    hands_pp = np.bincount(s_pid, minlength=len(names)).astype(float)
    key = a * 10_000_000 + b
    row_of = {int(k): i for i, k in enumerate(key)}
    shared, hu = I0[:, c["shared"]], I0[:, c["hu"]]
    evalmask = (shared >= 100) & (hu >= 10)
    cand = np.where((shared >= 300) & (hu >= 30))[0]
    base_scores = score(a, b, I0, F0, c, hands_pp)
    res = {"n_pairs_eval": int(evalmask.sum()), "n_candidates": int(len(cand)), "K": K_PAIRS,
           "types": TYPES, "qs": QS, "seeds": list(SEEDS), "runs": {}}
    # null calibration on the clean table
    strat = (shared >= 300) & (hu >= 30)
    res["n_pairs_stratum"] = int(strat.sum())
    res["null"] = {k: {"q50": float(np.median(v[strat])), "q99": float(np.quantile(v[strat], .99)),
                       "q999": float(np.quantile(v[strat], .999))} for k, v in base_scores.items()}
    # top real pairs by the union score (the "manual review" list)
    top = np.argsort(-np.where(evalmask, base_scores["union"], -np.inf))[:10]
    res["top_real_pairs"] = [{"shared": int(shared[i]), "hu": int(hu[i]),
                              **{k: float(v[i]) for k, v in base_scores.items()}} for i in top]
    # map player -> seat rows' hands (for finding shared hands)
    order = np.argsort(s_pid, kind="stable")
    cnt = np.bincount(s_pid, minlength=len(names)); st_ = np.concatenate([[0], np.cumsum(cnt)])
    hands_of = lambda p: s_hand[order[st_[p]:st_[p + 1]]]  # noqa: E731
    injected_ok = defaultdict(int)
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        perm = rng.permutation(cand)
        chosen, used = [], set()
        for i in perm:
            if a[i] in used or b[i] in used:
                continue
            chosen.append(i); used |= {int(a[i]), int(b[i])}
            if len(chosen) == K_PAIRS:
                break
        # load the shared hands of every chosen pair once
        need = defaultdict(list)          # file -> [(order, pair_row)]
        for i in chosen:
            sh = np.intersect1d(hands_of(a[i]), hands_of(b[i]))
            for h in sh:
                need[int(H[h, 0])].append((int(H[h, 1]), int(i)))
        raws = defaultdict(list)          # pair_row -> list of raw hands
        for f, lst in need.items():
            with open(DATA_ROOT / "data" / files[f], "rb") as fp:
                d = tomllib.load(fp)
            vals = list(d.values())
            for o, i in lst:
                raws[i].append(vals[o])
        print(f"seed {seed}: {len(chosen)} pairs, {sum(len(v) for v in raws.values())} shared hands "
              f"from {len(need)} files ({time.time() - t0:.0f}s)", flush=True)
        run = {}
        for kind in TYPES:
            for q in QS:
                I1, F1 = I0.copy(), F0.copy()
                y = np.zeros(len(a))
                n_rew, n_rej, n_pk_rej = 0, 0, 0
                for i in chosen:
                    pa, pb = int(a[i]), int(b[i])
                    # dumper = the pair's first player (a) by construction; direction is irrelevant to |z|
                    for raw in raws[i]:
                        try:
                            rec = parse_hand(raw)
                        except ParseError:
                            continue
                        if args.pairs == "mw" and rec.n < 3:
                            continue
                        seat = {pid_of[p]: k for k, p in enumerate(raw["players"])}
                        if pa not in seat or pb not in seat:
                            continue
                        sa, sb = seat[pa], seat[pb]
                        if rng.random() >= q:
                            continue
                        new = hu_rewrite(raw, sa, sb, kind, rng)
                        if new is None:
                            continue
                        try:
                            rec2 = parse_hand(new)
                        except ParseError:
                            n_rej += 1
                            continue
                        if not pk_check(new, False)[0]:
                            n_pk_rej += 1
                            continue
                        n_rew += 1
                        pids = [pid_of[p] for p in raw["players"]]
                        _, _, _, _, pi0, pf0 = hand_rows(rec, pids, 0)
                        _, _, _, _, pi1, pf1 = hand_rows(rec2, pids, 0)
                        for rows_i, rows_f, sign in ((pi0, pf0, -1), (pi1, pf1, 1)):
                            for ri, rf in zip(rows_i, rows_f):
                                r = row_of[ri[0] * 10_000_000 + ri[1]]
                                I1[r] += sign * np.array(ri[2:], float)
                                F1[r] += sign * np.array(rf)
                    y[i] = 1
                sc = score(a, b, I1, F1, c, hands_pp)
                # main population: the candidates' own stratum (>= 300 shared, >= 30 heads-up), so
                # sample size and co-occurrence cannot separate positives from negatives
                m1 = (shared >= 300) & (hu >= 30)
                res_k = {"rewritten_hands": n_rew, "rejected_by_parser": n_rej,
                         "rejected_by_pokerkit": n_pk_rej,
                         "signals": {k: roc(v[m1], y[m1]) for k, v in sc.items()},
                         "signals_all_pairs": {k: roc(v[evalmask], y[evalmask]) for k, v in sc.items()}}
                # detection vs heads-up sample size (union score, threshold = null 99th pct)
                thr = res["null"]["union"]["q99"]
                pos = np.where(y == 1)[0]
                res_k["pos_detail"] = [{"hu": int(hu[i]), "union": float(sc["union"][i]),
                                        "clean_union": float(base_scores["union"][i]),
                                        "detected_at_null_q99": bool(sc["union"][i] > thr)} for i in pos]
                run[f"{kind}_q{q}"] = res_k
                print(f"  {kind:4s} q={q:<4} rewritten={n_rew:5d} rej={n_rej} "
                      f"AUC union={res_k['signals']['union']['auc']:.3f} "
                      f"soft={res_k['signals']['z_soft']['auc']:.3f} dump={res_k['signals']['abs_z_dump']['auc']:.3f} "
                      f"ch11={res_k['signals']['ch11_raw']['auc']:.3f} "
                      f"R@1%={res_k['signals']['union']['recall_at_fpr_0.01']:.2f}", flush=True)
        res["runs"][seed] = run
    # summary
    summ = {}
    for cfg in res["runs"][SEEDS[0]]:
        for sig in ("union", "z_soft", "abs_z_dump", "ch11_raw", "co_occ", "abs_z_flow_all"):
            for met in ("auc", "recall_at_fpr_0.01", "recall_at_fpr_0.001", "fpr_at_recall_0.9", "precision_at_P"):
                v = np.array([res["runs"][s][cfg]["signals"][sig][met] for s in SEEDS])
                summ.setdefault(cfg, {}).setdefault(sig, {})[met] = [float(v.mean()),
                                                                     float(v.std(ddof=1) / np.sqrt(len(v)))]
    res["summary"] = summ
    res["runtime_s"] = round(time.time() - t0, 1)
    res["pairs_table"] = args.pairs
    out = "collusion.json" if args.pairs == "all" else "collusion_mw.json"
    json.dump(res, open(RESULTS / out, "w"), indent=1)


if __name__ == "__main__":
    main()
