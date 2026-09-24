"""
clustering.py -- style clustering, temporal stability, embedding-vs-statistics comparison and
online Bayesian typing (raw step 13, Day 4 "Style Classification"; Validation: "4 k-means
clusters correspond to recognizable archetypes. Temporal stability > 70 %"; Math Flag
"Bayesian posterior update for player type estimation").

    python clustering.py            # needs player_stats.py and p2v.py outputs -> results/clustering.json

1. k-means (k = 4, the plan's four archetypes; silhouette for k = 2..8) on the standardised
   style vector of the 2,906 regulars (>= 500 hands); centroids read back in raw units.
2. Agreement with the VPIP x PFR quadrants (adjusted Rand index) for the statistics clusters and
   for k-means on the player2vec embeddings; k-NN recovery of the quadrant from the embedding.
3. Temporal stability: each regular's hands split into the first and second chronological half,
   both halves assigned to the full-data centroids. Compared with a RANDOM split of the same
   player's hands (sampling noise only) and with chance (sum of squared cluster shares).
4. Online typing: the four clusters become the types of a Bayesian model (Chapter 7); the
   posterior over a player's type is updated hand by hand on their first 500 hands, and the
   truth is the cluster of the same player's LATER hands (players with >= 1,000 hands).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.metrics import adjusted_rand_score, silhouette_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CACHE_ROOT, RESULTS, SEEDS  # noqa: E402
import player_stats as ps  # noqa: E402

CORE = ["vpip", "pfr", "three_bet", "steal", "limp", "cbet", "fold_to_cbet", "wtsd", "afq",
        "check_raise", "post_size"]
EVENTS = [("vpip", None), ("pfr", None), ("limp", None), ("tb", "tb_opp"), ("cbet", "cbet_opp"),
          ("wtsd", "saw_flop"), ("steal", "steal_opp")]


def style_from_rows(I, F, ci, cf, row_groups, fill=None):
    rows = np.concatenate(row_groups)
    owner = np.concatenate([np.full(len(r), i) for i, r in enumerate(row_groups)])
    I2 = I[rows].copy(); I2[:, ci["pid"]] = owner
    S = ps.sums(I2, F[rows], ci, cf, None, len(row_groups))
    st = ps.stats(S, min_opp=False)
    X = np.stack([st[k][0] for k in CORE], 1)
    if fill is not None:
        X = np.where(np.isfinite(X), X, fill)
    return X


def name_cluster(c):
    """Archetype name from a centroid in raw units (plan thresholds, see player_stats)."""
    loose = c["vpip"] >= ps.LOOSE_AT
    aggr = c["pfr"] >= ps.AGGR_RATIO * c["vpip"]
    return {(True, True): "LAG", (True, False): "loose-passive", (False, True): "TAG",
            (False, False): "tight-passive"}[(bool(loose), bool(aggr))]


def main():
    I, F, ci, cf, names = ps.load("IPN100")
    H = np.load(CACHE_ROOT / "IPN100" / "hands.npz")["H"]
    pid = I[:, ci["pid"]]
    order = np.argsort(pid, kind="stable")
    cnt = np.bincount(pid)
    starts = np.concatenate([[0], np.cumsum(cnt)])
    regs = np.where(cnt >= 500)[0]
    rows_of = {int(p): order[starts[p]:starts[p + 1]] for p in regs}   # chronological (stable)
    Xraw = style_from_rows(I, F, ci, cf, [rows_of[int(p)] for p in regs])
    med = np.nanmedian(Xraw, 0)
    n_imputed = int((~np.isfinite(Xraw)).sum())
    X = np.where(np.isfinite(Xraw), Xraw, med)
    sc = StandardScaler().fit(X)
    Z = sc.transform(X)
    st_all = ps.stats(ps.sums(I, F, ci, cf))
    quad = ps.quadrant(st_all["vpip"][0][regs], st_all["pfr"][0][regs])
    out = {"n_regulars": int(len(regs)), "features": CORE, "n_imputed_values": n_imputed}
    # --- 1. k selection + k=4 over seeds ---
    sil = {}
    for k in range(2, 9):
        lab = KMeans(k, n_init=10, random_state=0).fit_predict(Z)
        sil[k] = float(silhouette_score(Z, lab, sample_size=2000, random_state=0))
    out["silhouette"] = sil
    km_runs, labels = [], []
    for s in SEEDS:
        km = KMeans(4, n_init=20, random_state=s).fit(Z)
        cent = sc.inverse_transform(km.cluster_centers_)
        cdict = [dict(zip(CORE, map(float, c))) for c in cent]
        lab = km.labels_
        km_runs.append({"centroids": cdict, "names": [name_cluster(c) for c in cdict],
                        "sizes": np.bincount(lab, minlength=4).tolist(),
                        "ari_vs_quadrants": float(adjusted_rand_score(quad, lab))})
        labels.append(lab)
    out["kmeans4"] = km_runs
    out["kmeans4_seed_agreement_ari"] = [float(adjusted_rand_score(labels[0], labels[i]))
                                         for i in range(1, len(labels))]
    km0 = KMeans(4, n_init=20, random_state=0).fit(Z)
    lab0 = km0.labels_
    # contingency of cluster vs quadrant
    out["contingency_seed0"] = {int(c): {q: int(((lab0 == c) & (quad == q)).sum())
                                         for q in np.unique(quad)} for c in range(4)}
    # --- 2. embeddings ---
    emb = {}
    for s in SEEDS:
        f = CACHE_ROOT / "IPN100" / f"p2v_seed{s}.npz"
        if not f.exists():
            continue
        d = np.load(f)
        assert np.array_equal(d["pids"], regs), "p2v regulars differ from clustering regulars"
        E = StandardScaler().fit_transform(d["E"])
        labE = KMeans(4, n_init=20, random_state=s).fit_predict(E)
        knn_e = cross_val_score(KNeighborsClassifier(15), E, quad, cv=5).mean()
        knn_s = cross_val_score(KNeighborsClassifier(15), Z, quad, cv=5).mean()
        # cosine similarity within vs between quadrants
        En = d["E"] / np.linalg.norm(d["E"], axis=1, keepdims=True)
        rng = np.random.default_rng(s)
        pick = rng.choice(len(En), min(1500, len(En)), replace=False)
        Sm = En[pick] @ En[pick].T
        same = quad[pick][:, None] == quad[pick][None, :]
        off = ~np.eye(len(pick), dtype=bool)
        from sklearn.neighbors import NearestNeighbors
        kd = NearestNeighbors(n_neighbors=6).fit(E).kneighbors(E)[0][:, -1]
        eps = float(np.median(kd))          # k-distance heuristic (min_samples = 5)
        db = DBSCAN(eps=eps, min_samples=5).fit_predict(E)
        emb[s] = {"ari_emb_kmeans_vs_quadrants": float(adjusted_rand_score(quad, labE)),
                  "ari_emb_kmeans_vs_stats_kmeans": float(adjusted_rand_score(lab0, labE)),
                  "knn15_quadrant_acc_emb": float(knn_e), "knn15_quadrant_acc_stats": float(knn_s),
                  "cos_within_quadrant": float(Sm[same & off].mean()),
                  "cos_between_quadrant": float(Sm[~same].mean()),
                  "dbscan_clusters": int(len(set(db)) - (1 if -1 in db else 0)),
                  "dbscan_noise_share": float((db == -1).mean()), "dbscan_eps": eps}
        # temporal stability in embedding space
        Eh1 = StandardScaler().fit(d["E"]).transform(d["E_h1"])
        Eh2 = StandardScaler().fit(d["E"]).transform(d["E_h2"])
        kmE = KMeans(4, n_init=20, random_state=s).fit(E)
        a1, a2 = kmE.predict(Eh1), kmE.predict(Eh2)
        pE = np.bincount(kmE.labels_, minlength=4) / len(kmE.labels_)
        emb[s]["temporal_stability"] = float((a1 == a2).mean())
        emb[s]["chance"] = float((pE ** 2).sum())
        if s == SEEDS[0]:
            import umap
            U = umap.UMAP(n_neighbors=30, min_dist=0.2, random_state=0).fit_transform(E)
            out["umap_seed0"] = {"x": U[:, 0].round(3).tolist(), "y": U[:, 1].round(3).tolist(),
                                 "quadrant": quad.tolist(), "vpip": st_all["vpip"][0][regs].round(3).tolist(),
                                 "loss_late": [None if not np.isfinite(v) else round(float(v), 4)
                                               for v in d["loss_late"]]}
    out["embedding"] = emb
    # --- 3. temporal stability of statistics clusters ---
    ts = []
    for s in SEEDS:
        rng = np.random.default_rng(200 + s)
        h1, h2, r1, r2 = [], [], [], []
        for p in regs:
            rows = rows_of[int(p)]
            m = len(rows) // 2
            h1.append(rows[:m]); h2.append(rows[m:])
            perm = rng.permutation(len(rows))
            r1.append(rows[perm[:m]]); r2.append(rows[perm[m:]])
        km = KMeans(4, n_init=20, random_state=s).fit(Z)
        p_share = np.bincount(km.labels_, minlength=4) / len(regs)

        def assign(groups):
            Xg = style_from_rows(I, F, ci, cf, groups, fill=med)
            return km.predict(sc.transform(Xg))
        a1, a2 = assign(h1), assign(h2)
        b1, b2 = assign(r1), assign(r2)
        ts.append({"temporal": float((a1 == a2).mean()), "random_split": float((b1 == b2).mean()),
                   "chance": float((p_share ** 2).sum())})
        # half-level style drift for the figure: vpip change between halves
        if s == SEEDS[0]:
            X1 = style_from_rows(I, F, ci, cf, h1, fill=med); X2 = style_from_rows(I, F, ci, cf, h2, fill=med)
            out["half_vpip"] = {"h1": X1[:, 0].round(4).tolist(), "h2": X2[:, 0].round(4).tolist()}
    out["temporal_stability_stats"] = ts
    for key in ("temporal", "random_split", "chance"):
        v = np.array([t[key] for t in ts])
        out.setdefault("temporal_summary", {})[key] = [float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))]
    # --- 4. online Bayesian typing ---
    out["bayes"] = bayes_typing(I, ci, rows_of, regs, km0, sc, med, F, cf)
    json.dump(out, open(RESULTS / "clustering.json", "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("silhouette", "kmeans4_seed_agreement_ari", "temporal_summary")}, indent=1))
    print(json.dumps(km_runs[0], indent=1)[:1500])
    print(json.dumps(emb, indent=1)[:2000])
    print(json.dumps(out["bayes"], indent=1)[:1500])


def bayes_typing(I, ci, rows_of, regs, km, sc, med, F, cf, n_first=500, checkpoints=(10, 25, 50, 100, 200, 500)):
    """Types = k-means clusters; per-type Bernoulli rates of per-hand events pooled over members."""
    Xall = style_from_rows(I, F, ci, cf, [rows_of[int(p)] for p in regs], fill=med)
    lab = km.predict(sc.transform(Xall))
    rates = np.zeros((4, len(EVENTS)))
    for t in range(4):
        rows = np.concatenate([rows_of[int(p)] for p, l in zip(regs, lab) if l == t])
        for j, (ev, opp) in enumerate(EVENTS):
            num = I[rows, ci[ev]].sum()
            den = len(rows) if opp is None else I[rows, ci[opp]].sum()
            rates[t, j] = (num + 1) / (den + 2)
    prior = np.bincount(lab, minlength=4) / len(lab)
    elig = [p for p in regs if len(rows_of[int(p)]) >= 1000]
    later = [rows_of[int(p)][n_first:] for p in elig]
    truth = km.predict(sc.transform(style_from_rows(I, F, ci, cf, later, fill=med)))
    hits = {c: 0 for c in checkpoints}
    conf90 = []
    post_traj = []
    lr1, lr0 = np.log(rates), np.log(1 - rates)
    for k, p in enumerate(elig):
        rows = rows_of[int(p)][:n_first]
        ll = np.zeros((n_first, 4))
        for j, (ev, opp) in enumerate(EVENTS):
            x = I[rows, ci[ev]].astype(float)
            o = np.ones(len(rows)) if opp is None else I[rows, ci[opp]].astype(float)
            ll += (o * x)[:, None] * lr1[None, :, j] + (o * (1 - x))[:, None] * lr0[None, :, j]
        cum = np.log(prior)[None, :] + np.cumsum(ll, 0)
        post = np.exp(cum - cum.max(1, keepdims=True)); post /= post.sum(1, keepdims=True)
        for c in checkpoints:
            hits[c] += int(post[c - 1].argmax() == truth[k])
        ok = np.where((post[:, truth[k]] >= 0.9))[0]
        # first hand after which the posterior on the true type stays >= 0.9
        stay = None
        if len(ok):
            bad = np.where(post[:, truth[k]] < 0.9)[0]
            stay = int(bad.max() + 2) if len(bad) and bad.max() + 1 < n_first else (1 if not len(bad) else None)
        conf90.append(stay)
        if k < 40:
            post_traj.append(post[:, truth[k]][[c - 1 for c in checkpoints]].round(3).tolist())
    reached = [c for c in conf90 if c is not None]
    return {"types_rates": {f"type{t}": dict(zip([e for e, _ in EVENTS], rates[t].round(4).tolist()))
                            for t in range(4)},
            "prior": prior.round(4).tolist(), "players": len(elig),
            "map_acc_at": {c: hits[c] / len(elig) for c in checkpoints},
            "share_reaching_stable_0.9_within_500": len(reached) / len(elig),
            "hands_to_stable_0.9_median": float(np.median(reached)) if reached else None,
            "hands_to_stable_0.9_q75": float(np.quantile(reached, .75)) if reached else None,
            "chance_acc": float((np.bincount(truth, minlength=4) / len(truth)).max()),
            "sample_trajectories": post_traj}


if __name__ == "__main__":
    main()
