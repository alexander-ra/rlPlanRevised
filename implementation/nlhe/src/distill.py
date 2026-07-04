"""Distill the tabular blueprint into a policy network (the thesis-reusable
artifact / future piKL anchor).

The infoset hash is one-way, so we can't invert the table to features. Instead we
SAMPLE game states by random playouts, extract an info-state feature vector from
each visited state, and read the target (average) strategy from the table by
hash. Train an MLP features -> strategy with KL loss on the GPU.

Info-state features (documented slices, kept stable for reuse):
  [0:4]   street one-hot
  [4:10]  acting seat one-hot (relative position implicit via committed)
  [10]    acting seat's per-bucket mean equity (hand strength proxy, 0..1)
  [11:17] committed / starting_stack per seat
  [17:23] folded flag per seat
  [23:29] allin flag per seat
  [29]    current_bet / stack
  [30]    min_raise / stack
  [31]    pot / (n*stack)
  [32]    raises_this_street / max_raises
Target: average strategy over the (padded) MAXA abstract actions.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

import engine_nb as EN
import mccfr
from actions import infoset_hash

ART = Path(__file__).resolve().parents[1] / "artifacts"
FEAT_DIM = 33
MAXA = mccfr.MAXA


def _rules_and_art(cfg):
    import engine_ref as ER
    a = cfg["abstraction"]
    rules = ER.Rules(
        num_players=cfg["game"]["num_players"], starting_stack=cfg["game"]["starting_stack"],
        small_blind=cfg["game"]["small_blind"], big_blind=cfg["game"]["big_blind"],
        ante=cfg["game"]["ante"], raise_fractions=tuple(a["raise_fractions"]),
        include_allin=a["include_allin"], use_preflop_open=a["use_preflop_open"],
        preflop_open_bb=a["preflop_open_bb"], max_raises_per_street=a["max_raises_per_street"])
    return EN.pack_rules(rules), mccfr.load_artifacts()


def collect_dataset(slot_key, stratsum, cfg, n_states=2_000_000, seed=0):
    """Sample states via random playouts; return (X, Y, mask) for table-present
    infosets. Uses per-bucket mean equity for the hand-strength feature."""
    import evalmatch
    me = evalmatch._bucket_mean_equity()
    pf = np.load(ART / "preflop_equity.npy") if (ART / "preflop_equity.npy").exists() \
        else evalmatch._preflop_mean_equity()
    eqs = (pf, me["flop"], me["turn"], me["river"])
    rules, art = _rules_and_art(cfg)
    stack = cfg["game"]["starting_stack"]
    maxr = cfg["abstraction"]["max_raises_per_street"]
    X = np.zeros((n_states, FEAT_DIM), dtype=np.float32)
    Y = np.zeros((n_states, MAXA), dtype=np.float32)
    M = np.zeros((n_states, MAXA), dtype=np.float32)
    rng = np.random.default_rng(seed)
    ok = np.empty(8, dtype=np.int64)
    oa = np.empty(8, dtype=np.int64)
    got = 0
    while got < n_states:
        deck = rng.permutation(52).astype(np.int32)
        st = EN.new_hand_nb(rules, deck[:12], deck[12:17], int(rng.integers(6)))
        while st[EN.S_FIN] == 0 and got < n_states:
            p = st[EN.S_TOACT]
            n = EN.legal_actions_nb(st, rules, ok, oa)
            bucket = mccfr.player_bucket(st, p, art["kpre"], art["bpre"],
                                         art["kflop"], art["bflop"], art["kturn"],
                                         art["bturn"], art["kriver"], art["briver"],
                                         art["binom"], art["perms"])
            h = infoset_hash(st, bucket)
            slot = mccfr.table_find(slot_key, h)
            if slot >= 0 and stratsum[slot].sum() > 0:
                X[got] = _features(st, p, bucket, eqs, art, stack, maxr)
                row = stratsum[slot]
                tot = row[:n][row[:n] > 0].sum()
                if tot > 0:
                    for aa in range(n):
                        Y[got, aa] = max(row[aa], 0) / tot
                        M[got, aa] = 1.0
                    got += 1
            # advance by sampling an action
            a = int(rng.integers(n))
            EN.apply_action_nb(st, rules, int(ok[a]), int(oa[a]))
    return X[:got], Y[:got], M[:got]


def _features(st, p, bucket, eqs, art, stack, maxr):
    f = np.zeros(FEAT_DIM, dtype=np.float32)
    street = int(st[EN.S_STREET])
    f[street] = 1.0
    f[4 + p] = 1.0
    # hand strength via per-bucket mean equity
    from indexer import canonical_key, key_to_class
    kpre, kflop, kturn, kriver = art["kpre"], art["kflop"], art["kturn"], art["kriver"]
    mpre, mflop, mturn, mriver = eqs
    if street == 0:
        f[10] = mpre[bucket] if bucket < len(mpre) else 0.5
    elif street == 1:
        f[10] = mflop[bucket]
    elif street == 2:
        f[10] = mturn[bucket]
    else:
        f[10] = mriver[bucket]
    for s in range(EN.N):
        f[11 + s] = st[EN.O_COMMIT + s] / stack
        f[17 + s] = st[EN.O_FOLD + s]
        f[23 + s] = st[EN.O_ALLIN + s]
    f[29] = st[EN.S_CBET] / stack
    f[30] = st[EN.S_MINR] / stack
    f[31] = 0.0
    tot = 0
    for s in range(EN.N):
        tot += st[EN.O_COMMIT + s]
    f[31] = tot / (EN.N * stack)
    f[32] = st[EN.S_RAISES] / maxr
    return f


def train_policy(X, Y, M, cfg, epochs=40, device=None):
    import torch
    import torch.nn as nn
    dev = device or ("cuda" if torch.cuda.is_available() else "cpu")
    hid = cfg["distill"]["hidden"]
    layers = []
    d = FEAT_DIM
    for h in hid:
        layers += [nn.Linear(d, h), nn.ReLU()]
        d = h
    layers += [nn.Linear(d, MAXA)]
    net = nn.Sequential(*layers).to(dev)
    opt = torch.optim.AdamW(net.parameters(), lr=cfg["distill"]["lr"])
    Xt = torch.from_numpy(X).to(dev)
    Yt = torch.from_numpy(Y).to(dev)
    Mt = torch.from_numpy(M).to(dev)
    n = X.shape[0]
    ntr = int(n * 0.95)
    bs = cfg["distill"]["batch_size"]
    best = 1e9
    patience = cfg["distill"]["early_stop_patience"]
    bad = 0
    for ep in range(epochs):
        perm = torch.randperm(ntr, device=dev)
        net.train()
        for i in range(0, ntr, bs):
            idx = perm[i:i + bs]
            logits = net(Xt[idx])
            logits = logits.masked_fill(Mt[idx] == 0, -1e9)
            logp = torch.log_softmax(logits, dim=1)
            loss = -(Yt[idx] * logp).sum(1).mean()  # cross-entropy / KL up to const
            opt.zero_grad(); loss.backward(); opt.step()
        # val
        net.eval()
        with torch.no_grad():
            logits = net(Xt[ntr:]).masked_fill(Mt[ntr:] == 0, -1e9)
            p = torch.softmax(logits, dim=1)
            tv = 0.5 * (p - Yt[ntr:]).abs().sum(1).mean().item()
        if tv < best - 1e-4:
            best = tv; bad = 0
        else:
            bad += 1
            if bad >= patience:
                break
    return net, best


def distill(run_dir, cfg, slot_key, stratsum, iteration):
    import torch
    X, Y, M = collect_dataset(slot_key, stratsum, cfg)
    net, tv = train_policy(X, Y, M, cfg)
    out = Path(run_dir) / "distilled"
    out.mkdir(parents=True, exist_ok=True)
    p = out / f"policy_{iteration}.pt"
    torch.save({"state_dict": net.state_dict(), "feat_dim": FEAT_DIM,
                "maxa": MAXA, "hidden": cfg["distill"]["hidden"],
                "val_tv": tv, "n_samples": len(X)}, p)
    (out / f"policy_{iteration}.json").write_text(
        __import__("json").dumps({"val_tv": tv, "n_samples": len(X),
                                  "iteration": int(iteration)}))
    print(f"distilled policy -> {p.name} (val TV={tv:.3f}, {len(X):,} samples)")
    return tv
