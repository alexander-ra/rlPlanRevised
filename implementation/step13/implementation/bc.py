"""
bc.py -- behavioural cloning on real decisions (raw step 13, Day 2 "PokerBehavioralCloningModel";
Validation: "BC model: prediction accuracy > 55 % (random baseline for 7 action types = 14 %).
Accuracy by archetype: TAG > LAG > Fish").

    python bc.py                       # IPN100, seeds 0 1 2  -> results/bc.json
    python bc.py --source PLURIBUS     # the Pluribus table (all hole cards known)

TASK. Predict the action class (fold / check / call / raise small / medium / large; see
config.SIZE_EDGES) from the PUBLIC state at a decision: street, position, table size, players
left and still to act, pot and price, raises so far, who was the aggressor, board texture. Hole
cards are not used on IPN: no card is known in 86 % of hands and, where known, selected (shown
at showdown). On Pluribus every hole card is known, so a card-aware variant is added.

SPLIT. By time: IPN days 1-18 train, days 19-25 test (the players are mostly the same people, so
this measures prediction of known players' future decisions). Legal-action masking is applied to
every model: facing a bet -> {fold, call, raises}; otherwise -> {check, bets}.

MODELS (all see the same rows)
  majority      most frequent legal class given facing / not facing
  table         most frequent class per (street, facing, position, raises, players left)
  logreg        linear softmax on the state encoding
  mlp           the plan's 256-128 MLP with dropout 0.2
  mlp+stats     the same MLP + the actor's style vector from the TRAINING period (C1: does
                knowing who acts help?)
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import ACTION_NAMES, CACHE_ROOT, RESULTS, SEEDS  # noqa: E402
import player_stats as ps  # noqa: E402

DEV = "cuda" if torch.cuda.is_available() else "cpu"
POS_NAMES = ["SB", "BB", "EP", "LJ", "HJ", "CO", "BTN"]


def load_decisions(source: str):
    d = np.load(CACHE_ROOT / source / "decs.npz")
    I, F = d["I"], d["F"]
    ci = {k: i for i, k in enumerate(d["icols"])}
    cf = {k: i for i, k in enumerate(d["fcols"])}
    H = np.load(CACHE_ROOT / source / "hands.npz")["H"]
    return I, F, ci, cf, H


def onehot(v, k):
    o = np.zeros((len(v), k), np.float32)
    o[np.arange(len(v)), np.clip(v, 0, k - 1)] = 1
    return o


def encode(I, F, ci, cf, cards: bool = False) -> np.ndarray:
    """Public-state encoding (42 dims; + 17 hole-card dims if cards=True)."""
    n = I[:, ci["n"]]
    nb = np.select([n == 2, n <= 4, n <= 6], [0, 1, 2], 3)
    pot, tc, cb = F[:, cf["pot"]], F[:, cf["to_call"]], F[:, cf["cur_bet"]]
    parts = [
        onehot(I[:, ci["street"]], 4), onehot(I[:, ci["pos"]], 7), onehot(nb, 4),
        (n / 10.0)[:, None], (I[:, ci["n_active"]] / n)[:, None], (I[:, ci["n_behind"]] / n)[:, None],
        onehot(I[:, ci["n_raises"]], 5), onehot(I[:, ci["my_prev"]], 4),
        I[:, [ci["in_pos"], ci["is_pfa"], ci["pfa_live"], ci["was_aggr"]]].astype(np.float32),
        onehot(I[:, ci["facing"]], 3),
        I[:, ci["b_paired"]][:, None].astype(np.float32), (I[:, ci["b_suit"]] / 5.0)[:, None],
        ((I[:, ci["b_top"]] + 1) / 13.0)[:, None], (I[:, ci["b_conn"]] / 5.0)[:, None],
        np.log1p(pot)[:, None], np.log1p(tc)[:, None], (tc / (pot + tc + 1e-9))[:, None],
        np.log1p(cb)[:, None],
    ]
    if cards:
        h1, h2 = I[:, ci["h1"]], I[:, ci["h2"]]
        r1, r2 = h1 // 4, h2 // 4
        hi, lo = np.maximum(r1, r2), np.minimum(r1, r2)
        parts += [onehot(hi, 13), (lo / 12.0)[:, None], (r1 == r2)[:, None].astype(np.float32),
                  ((h1 % 4) == (h2 % 4))[:, None].astype(np.float32),
                  ((hi - lo) / 12.0)[:, None]]
    return np.concatenate(parts, axis=1).astype(np.float32)


def legal_mask(I, ci) -> np.ndarray:
    facing = I[:, ci["facing"]] > 0
    m = np.zeros((len(I), 6), bool)
    m[facing] = [True, False, True, True, True, True]
    m[~facing] = [False, True, False, True, True, True]
    return m


class MLP(nn.Module):
    def __init__(self, d_in, hidden=(256, 128), drop=0.2, n_out=6):
        super().__init__()
        layers, d = [], d_in
        for h in hidden:
            layers += [nn.Linear(d, h), nn.ReLU(), nn.Dropout(drop)]
            d = h
        layers.append(nn.Linear(d, n_out))
        self.net = nn.Sequential(*layers)

    def forward(self, x):
        return self.net(x)


def train_model(model, X, y, M, seed, epochs=2, bs=8192, lr=2e-3):
    torch.manual_seed(seed)
    model = model.to(DEV)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    Xg, yg, Mg = (torch.from_numpy(X).to(DEV), torch.from_numpy(y).long().to(DEV),
                  torch.from_numpy(M).to(DEV))
    n = len(X)
    steps = epochs * (n // bs)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps)
    g = torch.Generator(device=DEV).manual_seed(seed)
    model.train()
    for ep in range(epochs):
        perm = torch.randperm(n, device=DEV, generator=g)
        for k in range(n // bs):
            idx = perm[k * bs:(k + 1) * bs]
            logits = model(Xg[idx]).masked_fill(~Mg[idx], -1e9)
            loss = nn.functional.cross_entropy(logits, yg[idx])
            opt.zero_grad(set_to_none=True)
            loss.backward()
            opt.step()
            sched.step()
    return model


@torch.no_grad()
def predict(model, X, M, bs=65536):
    model.eval()
    out = []
    for k in range(0, len(X), bs):
        x = torch.from_numpy(X[k:k + bs]).to(DEV)
        m = torch.from_numpy(M[k:k + bs]).to(DEV)
        out.append(torch.log_softmax(model(x).masked_fill(~m, -1e9), -1).cpu().numpy())
    return np.concatenate(out)


def metrics(logp, y, groups: dict | None = None) -> dict:
    pred = logp.argmax(1)
    acc = (pred == y)
    nll = -logp[np.arange(len(y)), y]
    f1 = []
    for c in range(6):
        tp = ((pred == c) & (y == c)).sum(); fp = ((pred == c) & (y != c)).sum()
        fn = ((pred != c) & (y == c)).sum()
        f1.append(2 * tp / max(2 * tp + fp + fn, 1))
    out = {"acc": float(acc.mean()), "nll": float(nll.mean()), "macro_f1": float(np.mean(f1))}
    if groups:
        for gname, g in groups.items():
            out[gname] = {str(k): {"acc": float(acc[g == k].mean()), "n": int((g == k).sum())}
                          for k in np.unique(g)}
    return out


def table_baseline(Itr, ytr, Ite, ci):
    def key(I):
        na = np.minimum(I[:, ci["n_active"]], 4)
        return ((I[:, ci["street"]] * 3 + I[:, ci["facing"]]) * 7 + I[:, ci["pos"]]) * 25 + \
            np.minimum(I[:, ci["n_raises"]], 4) * 5 + na
    ktr, kte = key(Itr), key(Ite)
    K = int(max(ktr.max(), kte.max())) + 1
    cnt = np.zeros((K, 6))
    np.add.at(cnt, (ktr, ytr), 1)
    probs = (cnt + 0.5) / (cnt + 0.5).sum(1, keepdims=True)
    return np.log(probs[kte])


def player_style(source: str, day_max: int | None, hand_cut: int | None = None):
    """Standardised style vector per player from seat rows with day <= day_max (IPN) or hand
    index < hand_cut (Pluribus): the training period only, so the test period does not leak."""
    I, F, ci, cf, names = ps.load(source)
    H = np.load(CACHE_ROOT / source / "hands.npz")["H"]
    if hand_cut is not None:
        rows = np.where(I[:, ci["hand"]] < hand_cut)[0]
    else:
        rows = None if day_max is None else np.where(H[I[:, ci["hand"]], 2] <= day_max)[0]
    S = ps.sums(I, F, ci, cf, rows, len(names))
    st = ps.stats(S)
    X = np.stack([st[k][0] for k in ps.STYLE], 1)
    hands = S["hands"]
    ok = hands >= 100
    mu = np.nanmean(X[ok], 0); sd = np.nanstd(X[ok], 0) + 1e-9
    Z = (X - mu) / sd
    known = np.isfinite(Z).astype(np.float32)
    Z = np.nan_to_num(Z, nan=0.0).astype(np.float32)
    Z[~ok] = 0.0
    known[~ok] = 0.0
    extra = np.stack([np.log1p(hands) / 10.0, ok.astype(np.float32)], 1).astype(np.float32)
    quad = np.full(len(names), "unknown", dtype=object)
    reg = hands >= 500
    quad[reg] = ps.quadrant(st["vpip"][0][reg], st["pfr"][0][reg])
    return np.concatenate([Z, known, extra], 1), quad, hands


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="IPN100")
    ap.add_argument("--train-n", type=int, default=6_000_000)
    ap.add_argument("--test-n", type=int, default=2_000_000)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--bs", type=int, default=8192)
    args, _ = ap.parse_known_args()
    t0 = time.time()
    I, F, ci, cf, H = load_decisions(args.source)
    y_all = I[:, ci["cls"]]
    ok = ~((I[:, ci["facing"]] == 0) & (y_all == 0))       # drop folds when checking was free
    if args.source == "PLURIBUS":
        # all hole cards known; split by hand order (first 80 % of hands train)
        hand = I[:, ci["hand"]]
        cut = int(0.8 * (hand.max() + 1))
        tr_all = np.where(ok & (hand < cut))[0]; te_all = np.where(ok & (hand >= cut))[0]
        day_max, hand_cut = None, cut
    else:
        day = H[I[:, ci["hand"]], 2]
        tr_all = np.where(ok & (day <= 18))[0]; te_all = np.where(ok & (day >= 19))[0]
        day_max, hand_cut = 18, None
    rng_te = np.random.default_rng(12345)
    te = np.sort(rng_te.choice(te_all, min(args.test_n, len(te_all)), replace=False))
    cards = args.source == "PLURIBUS"
    Xte = encode(I[te], F[te], ci, cf, cards)
    Mte = legal_mask(I[te], ci)
    yte = y_all[te]
    style, quad, hands_tr = player_style(args.source, day_max, hand_cut)
    pid_te = I[te, ci["pid"]]
    groups = {"by_street": I[te, ci["street"]],
              "by_position": np.array(POS_NAMES)[I[te, ci["pos"]]],
              "by_facing": I[te, ci["facing"]],
              "by_quadrant": quad[pid_te].astype(str)}
    res = {"source": args.source, "n_train_available": int(len(tr_all)), "n_test": int(len(te)),
           "test_class_share": {ACTION_NAMES[c]: float((yte == c).mean()) for c in range(6)},
           "seeds": list(SEEDS), "runs": {}}
    # --- non-learned baselines (seed-independent) ---
    rng0 = np.random.default_rng(0)
    tr0 = rng0.choice(tr_all, min(args.train_n, len(tr_all)), replace=False)
    facing_tr = I[tr0, ci["facing"]] > 0
    maj = np.full((len(te), 6), -1e9, np.float32)
    for f in (False, True):
        cls = np.bincount(y_all[tr0][facing_tr == f], minlength=6)
        p = (cls + 0.5) / (cls + 0.5).sum()
        rows = (I[te, ci["facing"]] > 0) == f
        maj[rows] = np.log(p)
    res["majority"] = metrics(maj, yte, groups)
    res["table"] = metrics(table_baseline(I[tr0], y_all[tr0], I[te], ci), yte, groups)
    print(f"majority acc={res['majority']['acc']:.4f}  table acc={res['table']['acc']:.4f}", flush=True)
    per_player = {}
    for seed in SEEDS:
        rng = np.random.default_rng(seed)
        tr = rng.choice(tr_all, min(args.train_n, len(tr_all)), replace=False)
        Xtr = encode(I[tr], F[tr], ci, cf, cards); Mtr = legal_mask(I[tr], ci); ytr = y_all[tr]
        runs = {}
        specs = [("logreg", lambda d: MLP(d, hidden=()), False),
                 ("mlp", lambda d: MLP(d), False),
                 ("mlp+stats", lambda d: MLP(d), True)]
        for name, make, use_style in specs:
            Xa, Xb = Xtr, Xte
            if use_style:
                Xa = np.concatenate([Xtr, style[I[tr, ci["pid"]]]], 1)
                Xb = np.concatenate([Xte, style[pid_te]], 1)
            ts = time.time()
            m = train_model(make(Xa.shape[1]), Xa, ytr, Mtr, seed, epochs=args.epochs, bs=args.bs)
            logp = predict(m, Xb, Mte)
            runs[name] = metrics(logp, yte, groups)
            runs[name]["train_s"] = round(time.time() - ts, 1)
            if name in ("mlp", "mlp+stats"):
                acc = (logp.argmax(1) == yte).astype(float)
                u, inv = np.unique(pid_te, return_inverse=True)
                n_ = np.bincount(inv); a_ = np.bincount(inv, acc) / n_
                keep = n_ >= (300 if args.source == "IPN100" else 100)
                per_player.setdefault(name, []).append({int(p): float(a) for p, a in zip(u[keep], a_[keep])})
            print(f"  seed {seed} {name:10s} acc={runs[name]['acc']:.4f} nll={runs[name]['nll']:.4f} "
                  f"({runs[name]['train_s']}s)", flush=True)
        res["runs"][seed] = runs
    # mean +- SE over seeds
    summ = {}
    for name in res["runs"][SEEDS[0]]:
        for k in ("acc", "nll", "macro_f1"):
            v = np.array([res["runs"][s][name][k] for s in SEEDS])
            summ.setdefault(name, {})[k] = [float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))]
    d = np.array([res["runs"][s]["mlp+stats"]["acc"] - res["runs"][s]["mlp"]["acc"] for s in SEEDS])
    dn = np.array([res["runs"][s]["mlp+stats"]["nll"] - res["runs"][s]["mlp"]["nll"] for s in SEEDS])
    summ["stats_gain_acc"] = [float(d.mean()), float(d.std(ddof=1) / np.sqrt(len(d)))]
    summ["stats_gain_nll"] = [float(dn.mean()), float(dn.std(ddof=1) / np.sqrt(len(dn)))]
    res["summary"] = summ
    # per-player accuracy (seed-averaged) and its relation to quadrant
    pp = {}
    for name, lst in per_player.items():
        common = set.intersection(*[set(x) for x in lst])
        pp[name] = {p: float(np.mean([x[p] for x in lst])) for p in common}
    res["per_player_acc"] = {name: {"n_players": len(v),
                                    "median": float(np.median(list(v.values()))),
                                    "q10": float(np.quantile(list(v.values()), .1)),
                                    "q90": float(np.quantile(list(v.values()), .9)),
                                    "by_quadrant": {q: float(np.median([a for p, a in v.items() if quad[p] == q]))
                                                    for q in ("TAG", "LAG", "loose-passive", "tight-passive")
                                                    if any(quad[p] == q for p in v)}}
                             for name, v in pp.items()}
    res["runtime_s"] = round(time.time() - t0, 1)
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / ("bc.json" if args.source == "IPN100" else f"bc_{args.source}.json")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
