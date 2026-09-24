"""
p2v.py -- a player2vec-style behavioural embedding for poker (raw step 13, Day 3 "Player
Embedding Model"; Wang et al. 2024, arXiv:2404.04234: events as tokens, a Transformer trained
with masked-token prediction, a player vector pooled from its outputs).

    python p2v.py                  # seeds 0 1 2 -> results/player2vec.json + cached embeddings

TOKENS (vocabulary of 180). Each hand a player sits in becomes
    [position x table-size]  [street x facing x multiway x action] ...  [how the hand ended]
e.g. BTN@6-max, preflop/unopened/multiway/raise_m, flop/unopened/heads-up/raise_s, END_won.
Bet sizes enter through the three raise-size buckets. Hole cards are not tokens (unknown on IPN).

MODEL. 4-layer Transformer encoder, d = 128, 4 heads, 256-token windows of one player's
chronological stream, BERT-style masking (15 %; 80/10/10). Trained on days 1-18 only.

EVALUATION (the embedding has no labels, so it is tested on what it should capture)
  re-identification  embed a player from N hands of days 1-18 and from N other hands of days
                     19-25 (never seen in training); rank all players by similarity; top-1 /
                     top-10 / MRR. Same test for the hand-crafted style vector, and for both.
                     This is also the multi-accounting question: can one person be recognised
                     from behaviour alone?
  consistency        per-player masked-token loss on days 19-25 (the Math Flag's "behavioural
                     consistency"; bots were predicted to have unusually low loss).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, RESULTS, SEEDS  # noqa: E402
import player_stats as ps  # noqa: E402

DEV = "cuda" if torch.cuda.is_available() else "cpu"
PAD, MASK, CLS, UNK = 0, 1, 2, 3
N_SPECIAL = 4
POS_BASE = N_SPECIAL                       # 7 positions x 4 table-size bins = 28
ACT_BASE = POS_BASE + 28                   # 4 streets x 3 facing x 2 multiway x 6 actions = 144
END_BASE = ACT_BASE + 144                  # folded / won uncontested / showdown
VOCAB = END_BASE + 3
WIN = 256


def nbin(n):
    return np.select([n == 2, n <= 4, n <= 6], [0, 1, 2], 3)


def build_streams(source: str):
    """Token stream of every player: arrays (pid, hand, token) sorted by player then time."""
    d = np.load(CACHE_ROOT / source / "decs.npz")
    DI = d["I"]; ci = {k: i for i, k in enumerate(d["icols"])}
    s = np.load(CACHE_ROOT / source / "seats.npz")
    SI = s["I"]; cs = {k: i for i, k in enumerate(s["icols"])}
    # decision tokens
    mw = (DI[:, ci["n_active"]] > 2).astype(np.int64)
    tok_d = ACT_BASE + (((DI[:, ci["street"]] * 3 + DI[:, ci["facing"]]) * 2 + mw) * 6
                        + DI[:, ci["cls"]])
    # start tokens
    tok_s = POS_BASE + SI[:, cs["pos"]] * 4 + nbin(SI[:, cs["n"]])
    # end tokens: folded if the player's last decision was a fold
    key_d = DI[:, ci["hand"]].astype(np.int64) * 16 + DI[:, ci["seat"]]
    key_s = SI[:, cs["hand"]].astype(np.int64) * 16 + SI[:, cs["seat"]]
    last = np.zeros(len(DI), bool)
    last[:-1] = key_d[1:] != key_d[:-1]; last[-1] = True
    folded_keys = key_d[last & (DI[:, ci["cls"]] == 0)]
    folded = np.isin(key_s, folded_keys)
    tok_e = np.where(folded, END_BASE, np.where(SI[:, cs["won_nosd"]] == 1, END_BASE + 1, END_BASE + 2))
    pid = np.concatenate([SI[:, cs["pid"]], DI[:, ci["pid"]], SI[:, cs["pid"]]])
    hand = np.concatenate([SI[:, cs["hand"]], DI[:, ci["hand"]], SI[:, cs["hand"]]])
    sub = np.concatenate([np.full(len(SI), -1, np.int64), np.arange(len(DI), dtype=np.int64),
                          np.full(len(SI), 1 << 40, np.int64)])
    tok = np.concatenate([tok_s, tok_d, tok_e]).astype(np.int16)
    o = np.lexsort((sub, hand, pid))
    return pid[o].astype(np.int32), hand[o].astype(np.int32), tok[o]


def player_index(pid):
    u, st = np.unique(pid, return_index=True)
    en = np.append(st[1:], len(pid))
    return {int(p): (a, b) for p, a, b in zip(u, st, en)}


def windows(tokens: np.ndarray, win=WIN) -> np.ndarray:
    n = int(math.ceil(len(tokens) / win))
    out = np.full((n, win), PAD, np.int64)
    flat = out.reshape(-1)
    flat[:len(tokens)] = tokens
    return out


class Encoder(nn.Module):
    def __init__(self, d=128, layers=4, heads=4, ff=512, drop=0.1):
        super().__init__()
        self.tok = nn.Embedding(VOCAB, d, padding_idx=PAD)
        self.pos = nn.Embedding(WIN, d)
        layer = nn.TransformerEncoderLayer(d, heads, ff, drop, batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, layers)
        self.norm = nn.LayerNorm(d)
        self.head = nn.Linear(d, VOCAB)

    def forward(self, x):
        pad = x == PAD
        h = self.tok(x) + self.pos(torch.arange(x.shape[1], device=x.device))[None]
        h = self.enc(h, src_key_padding_mask=pad)
        return self.norm(h), pad


def mask_batch(x, gen, p=0.15):
    cand = x >= N_SPECIAL
    r = torch.rand(x.shape, device=x.device, generator=gen)
    sel = cand & (r < p)
    y = torch.where(sel, x, torch.full_like(x, -100))
    r2 = torch.rand(x.shape, device=x.device, generator=gen)
    xm = x.clone()
    xm[sel & (r2 < 0.8)] = MASK
    rnd = torch.randint(N_SPECIAL, VOCAB, x.shape, device=x.device, generator=gen)
    swap = sel & (r2 >= 0.8) & (r2 < 0.9)
    xm[swap] = rnd[swap]
    return xm, y


def train(W: np.ndarray, seed: int, epochs=4, bs=256, lr=5e-4):
    torch.manual_seed(seed)
    model = Encoder().to(DEV)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    Wg = torch.from_numpy(W).to(DEV)
    steps = epochs * (len(W) // bs)
    sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=lr, total_steps=steps, pct_start=0.1)
    gen = torch.Generator(device=DEV).manual_seed(seed)
    model.train()
    losses = []
    for ep in range(epochs):
        perm = torch.randperm(len(W), device=DEV, generator=gen)
        tot, cnt = 0.0, 0
        for k in range(len(W) // bs):
            x = Wg[perm[k * bs:(k + 1) * bs]]
            xm, y = mask_batch(x, gen)
            with torch.autocast("cuda", dtype=torch.bfloat16, enabled=DEV == "cuda"):
                h, _ = model(xm)
                logits = model.head(h)
            loss = nn.functional.cross_entropy(logits.float().reshape(-1, VOCAB), y.reshape(-1),
                                               ignore_index=-100)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step()
            tot += loss.item(); cnt += 1
        losses.append(tot / cnt)
        print(f"    epoch {ep}: mlm loss {losses[-1]:.4f}", flush=True)
    return model, losses


@torch.no_grad()
def embed_windows(model, W: np.ndarray, bs=1024):
    """Mean- and max-pooled final states per window (+ token counts for weighting)."""
    model.eval()
    mean_o, max_o, cnt_o = [], [], []
    for k in range(0, len(W), bs):
        x = torch.from_numpy(W[k:k + bs]).to(DEV)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=DEV == "cuda"):
            h, pad = model(x)
        h = h.float()
        keep = (~pad).float()[..., None]
        c = keep.sum(1).clamp(min=1)
        mean_o.append(((h * keep).sum(1) / c).cpu().numpy())
        max_o.append(h.masked_fill(pad[..., None], -1e4).max(1).values.cpu().numpy())
        cnt_o.append(c[:, 0].cpu().numpy())
    return np.concatenate(mean_o), np.concatenate(max_o), np.concatenate(cnt_o)


def embed_players(model, groups: list[np.ndarray]):
    """groups[i] = token array of one player (subset). Returns (mean-pool, max-pool) vectors."""
    Ws, owner = [], []
    for i, t in enumerate(groups):
        w = windows(t)
        Ws.append(w); owner.append(np.full(len(w), i))
    W = np.concatenate(Ws); owner = np.concatenate(owner)
    mn, mx, c = embed_windows(model, W)
    E1 = np.zeros((len(groups), mn.shape[1])); E2 = np.full((len(groups), mx.shape[1]), -1e4)
    wsum = np.bincount(owner, c, minlength=len(groups))
    np.add.at(E1, owner, mn * c[:, None])
    E1 /= wsum[:, None]
    np.maximum.at(E2, owner, mx)
    return E1, E2


@torch.no_grad()
def mlm_loss(model, t: np.ndarray, seed: int) -> float:
    W = windows(t)
    gen = torch.Generator(device=DEV).manual_seed(seed)
    x = torch.from_numpy(W).to(DEV)
    xm, y = mask_batch(x, gen)
    h, _ = model(xm)
    logits = model.head(h)
    loss = nn.functional.cross_entropy(logits.reshape(-1, VOCAB), y.reshape(-1), ignore_index=-100,
                                       reduction="sum")
    n = (y != -100).sum().item()
    return loss.item() / max(n, 1)


def retrieval(A: np.ndarray, B: np.ndarray, metric="cos") -> dict:
    """A[i] and B[i] describe the same player; rank all A for each B."""
    if metric == "cos":
        a = A / (np.linalg.norm(A, axis=1, keepdims=True) + 1e-9)
        b = B / (np.linalg.norm(B, axis=1, keepdims=True) + 1e-9)
        S = b @ a.T
    else:
        S = -((B[:, None, :] - A[None, :, :]) ** 2).sum(-1)
    return rank_stats(S)


def rank_stats(S):
    true = S[np.arange(len(S)), np.arange(len(S))]
    rank = (S > true[:, None]).sum(1)          # 0 = best
    return {"n": int(len(S)), "top1": float((rank == 0).mean()), "top10": float((rank < 10).mean()),
            "mrr": float((1.0 / (rank + 1)).mean()), "chance_top1": 1.0 / len(S)}


def zsim(S):
    return (S - S.mean(1, keepdims=True)) / (S.std(1, keepdims=True) + 1e-9)


def style_of(seat_rows_by_player, I, F, ci, cf, n_players, mu=None, sd=None):
    """Style vectors from given seat-row subsets (no minimum thresholds; NaN -> population)."""
    rows = np.concatenate(seat_rows_by_player)
    owner = np.concatenate([np.full(len(r), i) for i, r in enumerate(seat_rows_by_player)])
    I2 = I[rows].copy(); I2[:, ci["pid"]] = owner
    S = ps.sums(I2, F[rows], ci, cf, None, len(seat_rows_by_player))
    st = ps.stats(S, min_opp=False)
    X = np.stack([st[k][0] for k in ps.STYLE], 1)
    X = np.where(np.isfinite(X), X, np.nanmean(X, 0))
    return X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--epochs", type=int, default=4)
    ap.add_argument("--seeds", type=int, nargs="*", default=list(SEEDS))
    args, _ = ap.parse_known_args()
    t0 = time.time()
    src = "IPN100"
    pid, hand, tok = build_streams(src)
    H = np.load(CACHE_ROOT / src / "hands.npz")["H"]
    day = H[hand, 2]
    print(f"stream: {len(tok):,} tokens, {len(np.unique(pid)):,} players ({time.time() - t0:.0f}s)",
          flush=True)
    idx = player_index(pid)
    # ---- training windows: days 1-18, players with >= 50 hands there ----
    Ws = []
    for p, (a, b) in idx.items():
        m = day[a:b] <= 18
        t = tok[a:b][m]
        if len(t) >= 150:
            Ws.append(windows(t))
    Wtr = np.concatenate(Ws)
    print(f"train windows: {len(Wtr):,}", flush=True)
    # ---- evaluation sets ----
    SI_d = np.load(CACHE_ROOT / src / "seats.npz")
    I, F = SI_d["I"], SI_d["F"]
    ci = {k: i for i, k in enumerate(SI_d["icols"])}; cf = {k: i for i, k in enumerate(SI_d["fcols"])}
    seat_pid = I[:, ci["pid"]]
    seat_day = H[I[:, ci["hand"]], 2]
    order = np.argsort(seat_pid, kind="stable")
    cnt = np.bincount(seat_pid)
    starts = np.concatenate([[0], np.cumsum(cnt)])

    def seat_rows(p):
        return order[starts[p]:starts[p + 1]]

    early_n = np.bincount(seat_pid[seat_day <= 18], minlength=len(cnt))
    late_n = np.bincount(seat_pid[seat_day >= 19], minlength=len(cnt))
    Ns = (50, 100, 200, 400)
    res = {"vocab": VOCAB, "window": WIN, "train_windows": int(len(Wtr)), "seeds": args.seeds,
           "runs": {}}
    regs = np.where(cnt >= 500)[0]
    for seed in args.seeds:
        ts = time.time()
        print(f"seed {seed}: training", flush=True)
        model, losses = train(Wtr, seed, epochs=args.epochs)
        run = {"train_loss": losses, "train_s": round(time.time() - ts, 1), "reid": {}}
        rng = np.random.default_rng(100 + seed)
        for N in Ns:
            elig = np.where((early_n >= N) & (late_n >= N))[0]
            gA, gB, sA, sB = [], [], [], []
            for p in elig:
                a, b = idx[int(p)]
                ph, pt = hand[a:b], tok[a:b]
                uh = np.unique(ph)
                e_h = uh[H[uh, 2] <= 18]; l_h = uh[H[uh, 2] >= 19]
                ea = np.sort(rng.choice(e_h, N, replace=False)); la = np.sort(rng.choice(l_h, N, replace=False))
                gA.append(pt[np.isin(ph, ea)]); gB.append(pt[np.isin(ph, la)])
                rows = seat_rows(int(p))
                rh = I[rows, ci["hand"]]
                sA.append(rows[np.isin(rh, ea)]); sB.append(rows[np.isin(rh, la)])
            A1, A2 = embed_players(model, gA); B1, B2 = embed_players(model, gB)
            XA = style_of(sA, I, F, ci, cf, len(elig)); XB = style_of(sB, I, F, ci, cf, len(elig))
            mu, sd = XA.mean(0), XA.std(0) + 1e-9
            ZA, ZB = (XA - mu) / sd, (XB - mu) / sd
            r = {"players": int(len(elig)),
                 "emb_mean_cos": retrieval(A1, B1), "emb_max_cos": retrieval(A2, B2),
                 "stats_euclid": retrieval(ZA, ZB, "euclid")}
            a1 = A1 / np.linalg.norm(A1, axis=1, keepdims=True); b1 = B1 / np.linalg.norm(B1, axis=1, keepdims=True)
            Se = b1 @ a1.T
            Ss = -((ZB[:, None, :] - ZA[None, :, :]) ** 2).sum(-1)
            r["combined"] = rank_stats(zsim(Se) + zsim(Ss))
            run["reid"][N] = r
            print(f"  N={N}: players={len(elig)} top1 emb={r['emb_mean_cos']['top1']:.3f} "
                  f"max={r['emb_max_cos']['top1']:.3f} stats={r['stats_euclid']['top1']:.3f} "
                  f"both={r['combined']['top1']:.3f}", flush=True)
        # ---- per-regular embeddings (all hands; first / second chronological half) + MLM loss ----
        g_all, g_h1, g_h2, loss_late = [], [], [], []
        for p in regs:
            a, b = idx[int(p)]
            ph, pt = hand[a:b], tok[a:b]
            uh = np.unique(ph)
            mid = uh[len(uh) // 2]
            g_all.append(pt); g_h1.append(pt[ph < mid]); g_h2.append(pt[ph >= mid])
        E_all, _ = embed_players(model, g_all)
        E_h1, _ = embed_players(model, g_h1)
        E_h2, _ = embed_players(model, g_h2)
        for p in regs:
            a, b = idx[int(p)]
            m = day[a:b] >= 19
            t = tok[a:b][m]
            loss_late.append(mlm_loss(model, t, 7) if len(t) >= 300 else np.nan)
        np.savez(CACHE_ROOT / src / f"p2v_seed{seed}.npz", pids=regs, E=E_all, E_h1=E_h1, E_h2=E_h2,
                 loss_late=np.array(loss_late))
        torch.save(model.state_dict(), CACHE_ROOT / src / f"p2v_seed{seed}.pt")
        run["loss_late"] = {"n": int(np.isfinite(loss_late).sum()),
                            "median": float(np.nanmedian(loss_late)),
                            "q10": float(np.nanquantile(loss_late, .1)),
                            "q90": float(np.nanquantile(loss_late, .9))}
        res["runs"][seed] = run
    # summary over seeds
    summ = {}
    for N in Ns:
        for m in ("emb_mean_cos", "emb_max_cos", "stats_euclid", "combined"):
            for k in ("top1", "top10", "mrr"):
                v = np.array([res["runs"][s]["reid"][N][m][k] for s in args.seeds])
                summ.setdefault(str(N), {}).setdefault(m, {})[k] = [
                    float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0]
        summ[str(N)]["players"] = res["runs"][args.seeds[0]]["reid"][N]["players"]
    res["summary_reid"] = summ
    res["runtime_s"] = round(time.time() - t0, 1)
    json.dump(res, open(RESULTS / "player2vec.json", "w"), indent=1)
    print(json.dumps(summ, indent=1)[:2500])


if __name__ == "__main__":
    main()
