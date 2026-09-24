"""
botdetect.py -- can behaviour alone pick Pluribus out of its own games? (raw step 13, Phase 1
"whether a bot is playing instead of a human"; Math Flag "bots have unusually low loss").

    python botdetect.py            # -> results/botdetect.json

GROUND TRUTH. The 10,000 released Pluribus hands: every hand has Pluribus and five of 13
professionals. The detector never sees the label; it is used only to score the result.

UNITS. Each player's hands are cut into consecutive blocks of B hands (B = 250 and 500), so a
block is "one account over a session". Pluribus gives 40 blocks of 250; the 13 humans ~160.

DETECTORS (all unsupervised, fitted on every block of every player)
  iforest_hud      Isolation Forest on the HUD statistics of the block
  iforest_tells    Isolation Forest on HUD + the bot-relevant features the Pluribus paper points at
                   (donk bets, limps from outside the small blind) and bet-size variety
  iforest_p2v      Isolation Forest on the player2vec embedding of the block (IPN-trained model)
  mlm_loss         low masked-token loss on decision tokens = unusually predictable (Math Flag)
  ipn_distance     Mahalanobis distance of the block's HUD vector from 250-hand blocks of the
                   IPN regulars (is it unlike online humans?)
Plus two descriptive, player-level measures that use the hole cards (an operator sees them):
  randomisation    conditional entropy of the pre-flop action given position, situation and the
                   exact starting hand; an equilibrium-style mixed strategy should score high
Reported: AUC of Pluribus blocks vs human blocks, and Pluribus's rank among the 14 players by
its mean block score. With one bot, "rank 1 of 14" is one observation, not a detection rate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, RESULTS, SEEDS  # noqa: E402
import player_stats as ps  # noqa: E402
import p2v  # noqa: E402

HUD = ["vpip", "pfr", "three_bet", "steal", "limp", "cbet", "fold_to_cbet", "wtsd", "afq",
       "check_raise", "post_size", "donk", "fold_to_3bet"]
SIZE_BINS = [0, 0.25, 0.4, 0.55, 0.7, 0.85, 1.05, 1.5, 2.5, np.inf]


def auc(pos, neg):
    pos, neg = np.asarray(pos), np.asarray(neg)
    gt = (pos[:, None] > neg[None, :]).mean()
    eq = (pos[:, None] == neg[None, :]).mean()
    return float(gt + 0.5 * eq)


def blocks_of(rows_sorted, B):
    k = len(rows_sorted) // B
    return [rows_sorted[i * B:(i + 1) * B] for i in range(k)]


def hud_matrix(I, F, ci, cf, groups):
    rows = np.concatenate(groups)
    owner = np.concatenate([np.full(len(g), i) for i, g in enumerate(groups)])
    I2 = I[rows].copy(); I2[:, ci["pid"]] = owner
    S = ps.sums(I2, F[rows], ci, cf, None, len(groups))
    st = ps.stats(S, min_opp=False)
    with np.errstate(invalid="ignore", divide="ignore"):
        donk = S["donk"] / S["donk_opp"]
    X = np.stack([st[k][0] if k != "donk" else donk for k in HUD], 1)
    # limps from outside the small blind
    nsb = I2[:, ci["pos"]] != 0
    limp_nsb = np.bincount(owner, (I2[:, ci["limp"]] * nsb), len(groups)) / np.maximum(
        np.bincount(owner, nsb.astype(float), len(groups)), 1)
    return X, limp_nsb


def tell_matrix(DI, DF, di, df, hand_sets, pid):
    """Bet-size variety features from the player's own decisions in the given hands."""
    out = []
    for hs in hand_sets:
        m = (DI[:, di["pid"]] == pid) & np.isin(DI[:, di["hand"]], hs)
        cls, st = DI[m, di["cls"]], DI[m, di["street"]]
        fr = DF[m, df["size_frac"]]
        post = (cls >= 3) & (st > 0)
        pre = (cls >= 3) & (st == 0)
        h, _ = np.histogram(fr[post], SIZE_BINS)
        p = h / max(h.sum(), 1)
        ent = float(-(p[p > 0] * np.log(p[p > 0])).sum())
        over = float((fr[post] > 1.05).mean()) if post.any() else np.nan
        pre_sd = float(np.std(fr[pre])) if pre.sum() > 5 else np.nan
        n_sizes = len(np.unique(np.round(fr[post], 2))) / max(post.sum(), 1)
        out.append([ent, over, pre_sd, n_sizes])
    return np.array(out)


def randomisation(DI, di, pid):
    """Mean conditional entropy (nats) of the pre-flop action given (position, facing, raises,
    exact starting hand), over groups with >= 5 decisions; hole cards are known in this data."""
    m = (DI[:, di["pid"]] == pid) & (DI[:, di["street"]] == 0)
    X = DI[m]
    h1, h2 = X[:, di["h1"]], X[:, di["h2"]]
    r1, r2 = h1 // 4, h2 // 4
    hi, lo = np.maximum(r1, r2), np.minimum(r1, r2)
    suited = (h1 % 4) == (h2 % 4)
    hand = hi * 13 + lo + 169 * suited
    g = ((X[:, di["pos"]] * 3 + X[:, di["facing"]]) * 5 + np.minimum(X[:, di["n_raises"]], 4)) * 400 + hand
    ent, wts = [], []
    for k in np.unique(g):
        a = X[g == k, di["cls"]]
        if len(a) < 5:
            continue
        p = np.bincount(a, minlength=6) / len(a)
        ent.append(-(p[p > 0] * np.log(p[p > 0])).sum()); wts.append(len(a))
    return float(np.average(ent, weights=wts)) if ent else np.nan, int(np.sum(wts))


@torch.no_grad()
def decision_loss(model, t, seed=7):
    W = p2v.windows(t)
    gen = torch.Generator(device=p2v.DEV).manual_seed(seed)
    x = torch.from_numpy(W).to(p2v.DEV)
    xm, y = p2v.mask_batch(x, gen)
    h, _ = model(xm)
    logp = torch.log_softmax(model.head(h).float(), -1)
    sel = (y >= p2v.ACT_BASE) & (y < p2v.END_BASE)
    nll = -logp.gather(-1, y.clamp(min=0)[..., None])[..., 0]
    return float(nll[sel].mean().item()) if sel.any() else np.nan


def _distinct50(fr, rng, k=50, draws=20):
    if len(fr) < k:
        return np.nan
    return float(np.mean([len(np.unique(np.round(rng.choice(fr, k, replace=False), 2))) / k
                          for _ in range(draws)]))


def size_granularity(DI, DF, di, df, names):
    rng = np.random.default_rng(0)
    post = (DI[:, di["cls"]] >= 3) & (DI[:, di["street"]] > 0)
    plu = {names[p]: _distinct50(DF[post & (DI[:, di["pid"]] == p), df["size_frac"]], rng)
           for p in range(len(names))}
    d = np.load(CACHE_ROOT / "IPN100" / "decs.npz")
    Ii, Fi = d["I"], d["F"]
    ci2 = {k: i for i, k in enumerate(d["icols"])}; cf2 = {k: i for i, k in enumerate(d["fcols"])}
    m = (Ii[:, ci2["cls"]] >= 3) & (Ii[:, ci2["street"]] > 0)
    pid, fr = Ii[m, ci2["pid"]], Fi[m, cf2["size_frac"]]
    o = np.argsort(pid, kind="stable"); pid, fr = pid[o], fr[o]
    u, st_ = np.unique(pid, return_index=True); en = np.append(st_[1:], len(pid))
    vals = np.array([_distinct50(fr[a:b], rng) for a, b in zip(st_, en) if b - a >= 200])
    thr = plu["Pluribus"]
    return {"pluribus_table": plu, "ipn_players_ge200_postflop_bets": int(len(vals)),
            "ipn_quantiles": {q: float(np.quantile(vals, q)) for q in (0.001, 0.01, 0.05, 0.5)},
            "ipn_share_at_or_below_pluribus": float((vals <= thr).mean()),
            "ipn_count_at_or_below_pluribus": int((vals <= thr).sum()),
            "ipn_hist": np.histogram(vals, bins=np.linspace(0, 1, 41))[0].tolist()}


def main():
    I, F, ci, cf, names = ps.load("PLURIBUS")
    d = np.load(CACHE_ROOT / "PLURIBUS" / "decs.npz")
    DI, DF = d["I"], d["F"]
    di = {k: i for i, k in enumerate(d["icols"])}; df = {k: i for i, k in enumerate(d["fcols"])}
    bot = names.index("Pluribus")
    pid_s = I[:, ci["pid"]]
    # token streams for p2v
    spid, shand, stok = p2v.build_streams("PLURIBUS")
    res = {"players": {names[p]: int((pid_s == p).sum()) for p in range(len(names))}, "by_B": {}}
    # player-level randomisation (hole cards known)
    res["randomisation"] = {names[p]: randomisation(DI, di, p) for p in range(len(names))}
    # IPN reference: 250-hand blocks of IPN regulars, 6-handed rows only
    Ii, Fi, cii, cfi, _ = ps.load("IPN100")
    six = np.where(Ii[:, cii["n"]] == 6)[0]
    pid_i = Ii[six, cii["pid"]]
    o = np.argsort(pid_i, kind="stable"); six, pid_i = six[o], pid_i[o]
    u, st_ = np.unique(pid_i, return_index=True); en = np.append(st_[1:], len(pid_i))
    ref_groups = []
    for a_, b_ in zip(st_, en):
        if b_ - a_ >= 500:
            ref_groups += blocks_of(six[a_:b_], 250)[:4]
    Xref, _ = hud_matrix(Ii, Fi, cii, cfi, ref_groups)
    ref_med = np.nanmedian(Xref, 0)
    Xref = np.where(np.isfinite(Xref), Xref, ref_med)
    ref_sc = StandardScaler().fit(Xref)
    Zref = ref_sc.transform(Xref)
    cov_inv = np.linalg.pinv(np.cov(Zref.T))
    res["ipn_reference_blocks"] = len(ref_groups)
    models = {}
    for s in SEEDS:
        m = p2v.Encoder().to(p2v.DEV)
        m.load_state_dict(torch.load(CACHE_ROOT / "IPN100" / f"p2v_seed{s}.pt", map_location=p2v.DEV))
        m.eval(); models[s] = m
    for B in (250, 500):
        groups, owner = [], []
        for p in range(len(names)):
            rows = np.where(pid_s == p)[0]
            for g in blocks_of(rows, B):
                groups.append(g); owner.append(p)
        owner = np.array(owner)
        y = (owner == bot).astype(int)
        Xh, limp_nsb = hud_matrix(I, F, ci, cf, groups)
        hand_sets = [I[g, ci["hand"]] for g in groups]
        Xt = np.concatenate([tell_matrix(DI, DF, di, df, [hs], p) for hs, p in zip(hand_sets, owner)])
        med = np.nanmedian(Xh, 0)
        Xh = np.where(np.isfinite(Xh), Xh, med)
        Xt = np.where(np.isfinite(Xt), Xt, np.nanmedian(Xt, 0))
        Zh = StandardScaler().fit_transform(Xh)
        Zt = StandardScaler().fit_transform(np.concatenate([Xh, limp_nsb[:, None], Xt], 1))
        feat = {"hud": Zh, "tells": Zt}
        out = {"n_blocks": int(len(groups)), "n_bot_blocks": int(y.sum()), "detectors": {},
               "feature_auc_descriptive": {}}
        # descriptive: where does Pluribus differ (single-feature AUC, NOT a detector)
        allX = np.concatenate([Xh, limp_nsb[:, None], Xt], 1)
        fnames = HUD + ["limp_non_sb", "size_entropy", "overbet_share", "preflop_size_sd", "distinct_sizes"]
        for j, fn in enumerate(fnames):
            out["feature_auc_descriptive"][fn] = {
                "auc_bot_higher": auc(allX[y == 1, j], allX[y == 0, j]),
                "bot_mean": float(allX[y == 1, j].mean()), "human_mean": float(allX[y == 0, j].mean())}
        # embeddings + decision-token loss per block
        embs, losses = {}, {}
        for s, m in models.items():
            toks = []
            for hs, p in zip(hand_sets, owner):
                sel = (spid == p) & np.isin(shand, hs)
                toks.append(stok[sel])
            E, _ = p2v.embed_players(m, toks)
            embs[s] = StandardScaler().fit_transform(E)
            losses[s] = np.array([decision_loss(m, t) for t in toks])
        for det in ("iforest_hud", "iforest_tells", "iforest_p2v", "mlm_loss_low", "ipn_distance"):
            per_seed = []
            for s in SEEDS:
                if det == "iforest_hud":
                    sc = -IsolationForest(n_estimators=500, random_state=s).fit(Zh).score_samples(Zh)
                elif det == "iforest_tells":
                    sc = -IsolationForest(n_estimators=500, random_state=s).fit(Zt).score_samples(Zt)
                elif det == "iforest_p2v":
                    sc = -IsolationForest(n_estimators=500, random_state=s).fit(embs[s]).score_samples(embs[s])
                elif det == "mlm_loss_low":
                    sc = -losses[s]
                else:
                    Z = ref_sc.transform(np.where(np.isfinite(Xh), Xh, ref_med))
                    sc = np.einsum("ij,jk,ik->i", Z, cov_inv, Z)
                present = [p for p in range(len(names)) if (owner == p).any()]
                mean_by_player = np.full(len(names), np.nan)
                for p in present:
                    mean_by_player[p] = sc[owner == p].mean()
                rank = int((mean_by_player[present] > mean_by_player[bot]).sum() + 1)
                per_seed.append({"auc": auc(sc[y == 1], sc[y == 0]), "bot_rank": rank,
                                 "n_ranked": len(present),
                                 "player_means": {names[p]: float(mean_by_player[p]) for p in present}})
            a = np.array([r["auc"] for r in per_seed])
            out["detectors"][det] = {"auc_mean": float(a.mean()),
                                     "auc_se": float(a.std(ddof=1) / np.sqrt(len(a))),
                                     "bot_rank_by_seed": [r["bot_rank"] for r in per_seed],
                                     "n_players_ranked": per_seed[0]["n_ranked"],
                                     "seed0_player_means": per_seed[0]["player_means"]}
            print(f"B={B} {det:14s} AUC={a.mean():.3f}±{a.std(ddof=1) / np.sqrt(len(a)):.3f} "
                  f"rank={[r['bot_rank'] for r in per_seed]}/{per_seed[0]['n_ranked']}", flush=True)
        out["decision_loss_by_player_seed0"] = {names[p]: float(np.mean(losses[0][owner == p]))
                                                for p in range(len(names)) if (owner == p).any()}
        res["by_B"][B] = out
    # bet-size granularity: distinct post-flop size fractions (rounded to 0.01) among 50 random
    # post-flop bets, averaged over 20 draws -- Pluribus table players and IPN regulars
    res["size_granularity"] = size_granularity(DI, DF, di, df, names)
    json.dump(res, open(RESULTS / "botdetect.json", "w"), indent=1)
    print(json.dumps(res["randomisation"], indent=1))


if __name__ == "__main__":
    main()
