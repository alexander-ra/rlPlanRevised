"""
plotting.py -- every Chapter 13 data figure, drawn from the saved JSON only (no data loading,
no training). Output: plots/*.png.

    python plotting.py

Figures are 7.0 in wide and print at ~17.6 cm, so font size 10 prints at ~9.9 pt. Palette: the
validated categorical order blue, orange, aqua, yellow, magenta, green (never cycled); grey for
context points; text in neutral ink.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401
import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
R = HERE / "results"
OUT = HERE / "plots"
OUT.mkdir(exist_ok=True)
C = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300"]
GREY, INK, INK2 = "#b9b8b3", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 10, "axes.titlesize": 10.5, "axes.labelsize": 10,
                     "xtick.labelsize": 9.5, "ytick.labelsize": 9.5, "legend.fontsize": 9.5,
                     "axes.edgecolor": INK2, "axes.labelcolor": INK, "text.color": INK,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False,
                     "axes.spines.right": False, "axes.grid": True, "grid.color": "#e6e5e0",
                     "grid.linewidth": 0.6, "savefig.dpi": 250, "savefig.bbox": "tight"})


def logx(ax, ticks):
    ax.set_xscale("log")
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())


def load(name):
    return json.load(open(R / name))


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)
    print("wrote", name)


# ------------------------------------------------------------------------------------------
def fig_reliability():
    d = load("player_stats.json")["reliability"]
    ms = sorted(int(m) for m in d)
    stats = [("vpip", "VPIP"), ("pfr", "PFR"), ("three_bet", "3-bet"), ("cbet", "c-bet"),
             ("wtsd", "WTSD"), ("fold_to_cbet", "fold to c-bet")]
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    for (k, lab), col in zip(stats, C):
        y = [d[str(m)]["r"][k][0] for m in ms]
        ax.plot(ms, y, "-o", color=col, lw=2, ms=5, label=lab)
    ax.axhline(0.8, color=INK2, lw=1, ls="--")
    ax.text(ms[0], 0.815, "r = 0.8", color=INK2, fontsize=9.5, va="bottom")
    logx(ax, ms)
    ax.set_xlabel("hands per half")
    ax.set_ylabel("split-half correlation")
    ax.set_ylim(0, 1.02)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    save(fig, "reliability.png")


def fig_vpip_pfr():
    d = load("player_stats.json")
    sc = d["scatter"]
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.scatter(sc["vpip"], sc["pfr"], s=5, color=GREY, alpha=0.55, lw=0, label="IPN regulars")
    pt = d["pluribus_table"]
    pros = [(v["vpip"], v["pfr"]) for k, v in pt.items() if k != "Pluribus" and v["hands"] >= 500]
    ax.scatter(*zip(*pros), s=40, color=C[0], edgecolor="white", lw=0.8, zorder=3, label="professionals")
    ax.scatter([pt["Pluribus"]["vpip"]], [pt["Pluribus"]["pfr"]], s=80, marker="D", color=C[1],
               edgecolor="white", lw=0.8, zorder=4, label="Pluribus")
    x = np.linspace(0, 0.8, 50)
    ax.plot(x, 0.5 * x, color=INK2, lw=1, ls="--")
    ax.axvline(0.275, color=INK2, lw=1, ls="--")
    for (tx, ty, s) in [(0.06, 0.30, "TAG"), (0.60, 0.44, "LAG"), (0.06, 0.005, "tight-passive"),
                        (0.60, 0.04, "loose-passive")]:
        ax.text(tx, ty, s, fontsize=10, color=INK2)
    ax.set_xlim(0, 0.8); ax.set_ylim(0, 0.5)
    ax.set_xlabel("VPIP"); ax.set_ylabel("PFR")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False, markerscale=1.2)
    save(fig, "vpip_pfr.png")


def fig_gap():
    g = load("player_stats.json")["gap"]
    keys = ["rfi_LJ", "rfi_HJ", "rfi_CO", "rfi_BTN", "rfi_SB", "vpip_BB", "three_bet", "cbet",
            "fold_to_cbet"]
    labels = ["open LJ", "open HJ", "open CO", "open BTN", "open SB", "VPIP in BB", "3-bet",
              "c-bet", "fold to c-bet"]
    ipn = [100 * g["ipn_per_stat_median_diff"][k] for k in keys]
    pro = [100 * g["pros_per_stat_median_diff"][k] for k in keys]
    y = np.arange(len(keys))
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.barh(y - 0.2, ipn, 0.38, color=C[0], label="IPN regulars (median)")
    ax.barh(y + 0.2, pro, 0.38, color=C[1], label="professionals (median)")
    ax.axvline(0, color=INK, lw=1)
    ax.set_yticks(y); ax.set_yticklabels(labels); ax.invert_yaxis()
    ax.set_xlabel("difference from Pluribus (percentage points)")
    ax.grid(axis="y", visible=False)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, frameon=False)
    save(fig, "gap_to_pluribus.png")


def fig_bc():
    d = load("bc.json")
    runs = d["runs"]
    seeds = list(runs)
    streets = ["0", "1", "2", "3"]
    names = ["pre-flop", "flop", "turn", "river"]
    models = [("majority", "majority"), ("table", "frequency table"), ("mlp", "MLP"),
              ("mlp+stats", "MLP + player style")]
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.4), gridspec_kw={"width_ratios": [1.25, 1]})
    ax = axs[0]
    w = 0.2
    for k, (m, lab) in enumerate(models):
        if m in ("majority", "table"):
            v = [d[m]["by_street"][s]["acc"] for s in streets]
        else:
            v = [np.mean([runs[sd][m]["by_street"][s]["acc"] for sd in seeds]) for s in streets]
        ax.bar(np.arange(4) + (k - 1.5) * w, v, w * 0.92, color=[GREY, INK2, C[0], C[1]][k], label=lab)
    ax.set_xticks(range(4)); ax.set_xticklabels(names)
    ax.set_ylim(0.5, 0.8); ax.set_ylabel("accuracy (test days)")
    ax.set_title("(a) by street")
    ax.grid(axis="x", visible=False)
    ax2 = axs[1]
    qs = ["TAG", "tight-passive", "LAG", "loose-passive"]
    ql = ["TAG", "tight-\npassive", "LAG", "loose-\npassive"]
    for k, (m, col) in enumerate([("mlp", C[0]), ("mlp+stats", C[1])]):
        gain = [100 * (np.mean([runs[sd][m]["by_quadrant"][q]["acc"] for sd in seeds])
                       - d["majority"]["by_quadrant"][q]["acc"]) for q in qs]
        ax2.bar(np.arange(4) + (k - 0.5) * 0.36, gain, 0.34, color=col)
    ax2.set_xticks(range(4)); ax2.set_xticklabels(ql)
    ax2.set_ylabel("points above majority")
    ax2.set_title("(b) gain by player type")
    ax2.grid(axis="x", visible=False)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=4, frameon=False,
               bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    save(fig, "bc_accuracy.png")


def fig_reid():
    d = load("player2vec.json")["summary_reid"]
    Ns = sorted(int(n) for n in d)
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.2))
    for ax, met, title in [(axs[0], "top1", "(a) top-1"), (axs[1], "top10", "(b) top-10")]:
        for (m, lab), col in zip([("emb_mean_cos", "player2vec embedding"), ("stats_euclid", "statistics vector")], C):
            y = [100 * d[str(n)][m][met][0] for n in Ns]
            e = [100 * d[str(n)][m][met][1] for n in Ns]
            ax.errorbar(Ns, y, yerr=e, fmt="-o", color=col, lw=2, ms=5, capsize=3, label=lab)
        ch = [100 * (1 if met == "top1" else 10) / d[str(n)]["players"] for n in Ns]
        ax.plot(Ns, ch, ":", color=INK2, lw=1.5, label="chance")
        logx(ax, Ns)
        ax.set_xlabel("hands per side"); ax.set_title(title)
    axs[0].set_ylabel("same player ranked (%)")
    fig.legend(*axs[0].get_legend_handles_labels(), loc="lower center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    save(fig, "reid.png")


def fig_umap():
    u = load("clustering.json")["umap_seed0"]
    x, y, q = np.array(u["x"]), np.array(u["y"]), np.array(u["quadrant"])
    qs = ["TAG", "tight-passive", "LAG", "loose-passive"]
    fig, axs = plt.subplots(2, 2, figsize=(7.0, 5.6), sharex=True, sharey=True)
    for ax, name in zip(axs.flat, qs):
        ax.scatter(x, y, s=3, color=GREY, alpha=0.4, lw=0)
        m = q == name
        ax.scatter(x[m], y[m], s=5, color=C[0], lw=0)
        ax.set_title(f"{name} (n = {m.sum()})")
        ax.set_xticks([]); ax.set_yticks([])
        ax.grid(False)
    axs[1, 0].set_xlabel("UMAP 1"); axs[1, 1].set_xlabel("UMAP 1")
    axs[0, 0].set_ylabel("UMAP 2"); axs[1, 0].set_ylabel("UMAP 2")
    fig.tight_layout()
    save(fig, "umap_quadrants.png")


def fig_stability():
    d = load("clustering.json")
    ts = d["temporal_summary"]
    emb = d["embedding"]
    e_mean = np.mean([v["temporal_stability"] for v in emb.values()])
    e_se = np.std([v["temporal_stability"] for v in emb.values()], ddof=1) / np.sqrt(len(emb))
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.3), gridspec_kw={"width_ratios": [1, 1.2]})
    ax = axs[0]
    lab = ["statistics,\ntime split", "statistics,\nrandom split", "embedding,\ntime split", "chance"]
    val = [ts["temporal"][0], ts["random_split"][0], e_mean, ts["chance"][0]]
    err = [ts["temporal"][1], ts["random_split"][1], e_se, 0]
    ax.barh(range(4), [100 * v for v in val], 0.6, xerr=[100 * e for e in err], capsize=3,
            color=[C[0], C[2], C[1], GREY])
    ax.axvline(70, color=INK2, lw=1, ls="--")
    ax.text(71, -0.62, "plan: 70 %", fontsize=9.5, color=INK2, ha="left", va="center")
    ax.set_ylim(3.5, -0.95)
    ax.set_yticks(range(4)); ax.set_yticklabels(lab, fontsize=9.5)
    ax.set_xlim(0, 100)
    ax.set_xlabel("same cluster in both halves (%)")
    ax.set_title("(a) stability of the style cluster")
    ax.grid(axis="y", visible=False)
    ax2 = axs[1]
    b = d["bayes"]
    hs = sorted(int(k) for k in b["map_acc_at"])
    ax2.plot(hs, [100 * b["map_acc_at"][str(h)] for h in hs], "-o", color=C[0], lw=2, ms=5,
             label="posterior mode = later cluster")
    ax2.axhline(100 * b["chance_acc"], color=INK2, ls=":", lw=1.5, label="largest cluster share")
    logx(ax2, hs)
    ax2.set_xlabel("hands observed"); ax2.set_ylabel("correct type (%)")
    ax2.set_ylim(35, 75)
    ax2.set_title("(b) online Bayesian typing")
    ax2.legend(loc="lower right", frameon=False)
    fig.tight_layout()
    save(fig, "stability_bayes.png")


def fig_collusion():
    d = load("collusion_mw.json")      # headline: multiway tables (format-matched baseline)
    s = d["summary"]
    qs = d["qs"]
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.4))
    series = [("soft", "union", C[0], "-", "soft play"), ("dump", "union", C[1], "-", "chip dumping"),
              ("soft", "ch11_raw", C[0], "--", "soft play, raw help/harm"),
              ("dump", "ch11_raw", C[1], "--", "chip dumping, raw help/harm")]
    for kind, sig, col, ls, lab in series:
        y = [s[f"{kind}_q{q}"][sig]["auc"][0] for q in qs]
        e = [s[f"{kind}_q{q}"][sig]["auc"][1] for q in qs]
        axs[0].errorbar(qs, y, yerr=e, fmt=ls + "o", color=col, lw=2, ms=5, capsize=3, label=lab)
    axs[0].axhline(0.5, color=INK2, lw=1, ls=":")
    axs[0].set_ylabel("AUC"); axs[0].set_title("(a) ranking all pairs")
    for kind, col, lab in [("soft", C[0], "soft play"), ("dump", C[1], "chip dumping")]:
        for fpr, ls in (("0.01", "-"), ("0.001", "--")):
            y = [100 * s[f"{kind}_q{q}"]["union"][f"recall_at_fpr_{fpr}"][0] for q in qs]
            e = [100 * s[f"{kind}_q{q}"]["union"][f"recall_at_fpr_{fpr}"][1] for q in qs]
            axs[1].errorbar(qs, y, yerr=e, fmt=ls + "o", color=col, lw=2, ms=5, capsize=3,
                            label=f"{lab}, FPR {float(fpr) * 100:g} %")
    axs[1].set_ylabel("colluding pairs found (%)"); axs[1].set_title("(b) recall at fixed FPR")
    for ax in axs:
        logx(ax, qs)
        ax.set_xlabel("share of heads-up hands rewritten")
    h0, l0 = axs[0].get_legend_handles_labels()
    h1, l1 = axs[1].get_legend_handles_labels()
    fig.legend(h0 + h1, l0 + l1, loc="lower center", ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.24))
    fig.tight_layout()
    save(fig, "collusion.png")


def fig_bot():
    d = load("botdetect.json")
    det = d["by_B"]["250"]["detectors"]
    order = [("iforest_hud", "HUD statistics"), ("iforest_tells", "HUD + bot tells"),
             ("iforest_p2v", "embedding"), ("mlm_loss_low", "low decision loss"),
             ("ipn_distance", "distance to IPN")]
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 3.4), gridspec_kw={"width_ratios": [1, 1.1]})
    ax = axs[0]
    y = np.arange(len(order))
    a = [det[k]["auc_mean"] for k, _ in order]
    e = [det[k]["auc_se"] for k, _ in order]
    ax.barh(y, a, 0.6, xerr=e, capsize=3, color=C[0])
    ax.axvline(0.5, color=INK, lw=1, ls="--")
    for yy, (k, _), aa, ee in zip(y, order, a, e):
        r = det[k]["bot_rank_by_seed"][0]
        ax.text(0.54, yy, f"rank {r}/{det[k]['n_players_ranked']}", va="center",
                fontsize=9.5, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([lab for _, lab in order]); ax.invert_yaxis()
    ax.set_xlim(0, 1); ax.set_xlabel("AUC, Pluribus vs human blocks")
    ax.set_title("(a) unsupervised detectors")
    ax.grid(axis="y", visible=False)
    ax2 = axs[1]
    g = d["size_granularity"]
    bins = np.linspace(0, 1, 41)
    hist = np.array(g["ipn_hist"])
    ax2.bar(bins[:-1], hist, width=bins[1] - bins[0], align="edge", color=GREY, label="IPN regulars")
    top = hist.max()
    pros = [v for k, v in g["pluribus_table"].items() if k != "Pluribus" and v == v]
    ax2.scatter(pros, [top * 1.08] * len(pros), marker="|", s=160, color=C[0], lw=2, label="professionals")
    ax2.scatter([g["pluribus_table"]["Pluribus"]], [top * 1.08], marker="D", s=60, color=C[1],
                zorder=4, label="Pluribus")
    ax2.set_xlabel("share of distinct sizes, 50 post-flop bets")
    ax2.set_ylabel("players")
    ax2.set_title("(b) bet-size granularity")
    ax2.set_ylim(0, top * 1.2)
    fig.tight_layout()
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, frameon=False,
               columnspacing=0.8, handletextpad=0.3)
    save(fig, "bot_detection.png")


if __name__ == "__main__":
    fig_reliability(); fig_vpip_pfr(); fig_gap(); fig_bc(); fig_reid(); fig_umap(); fig_stability()
    if (R / "collusion_mw.json").exists():
        fig_collusion()
    fig_bot()
