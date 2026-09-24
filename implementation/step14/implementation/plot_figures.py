"""
plot_figures.py -- every data figure of Chapter 14, drawn from the saved results JSON only
(no simulation, no retraining). Output: deliverables/reports/step14/figures/*.png

    python plot_figures.py

Print rules (September review): figures are ~7 in wide and print at 17.6 cm, so the scale is
~1 and every text element uses fontsize >= 10; dpi 250; legends outside the data; every axis
labelled; short labels (they will be translated).
"""

from __future__ import annotations

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import deps

OUT = os.path.join(deps.REPO_ROOT, "deliverables", "reports", "step14", "figures")
os.makedirs(OUT, exist_ok=True)
FS = 10
plt.rcParams.update({"font.size": FS, "axes.titlesize": 11, "axes.labelsize": FS,
                     "xtick.labelsize": FS, "ytick.labelsize": FS, "legend.fontsize": FS,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b",
                     "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "grid.color": "#e4e3df", "grid.linewidth": 0.8})
INK, INK2 = "#0b0b0b", "#52514e"
# colour follows the agent (fixed across every figure); categorical slots of the reference palette
COL = {"Nash": "#52514e", "BestEq": "#1baf7a", "RNR(0.5)": "#2a78d6", "DirBR": "#eb6834",
       "DirBR-CP": "#e87ba4", "TypeBR": "#4a3aa7", "BR-Tight": "#eda100", "BR-Rock": "#eda100",
       "DirBR3P": "#eb6834", "Blend3P": "#2a78d6", "Nash-CFR": "#9b9a94"}
MARK = {"Nash": "s", "BestEq": "D", "RNR(0.5)": "o", "DirBR": "^", "DirBR-CP": "v",
        "TypeBR": "P", "BR-Tight": "X", "BR-Rock": "X"}
LS = {"Nash": "-", "BestEq": "-", "RNR(0.5)": "-", "DirBR": "-", "DirBR-CP": "--", "TypeBR": ":",
      "BR-Tight": "-.", "BR-Rock": "-."}
GAME = {"kuhn": "Kuhn", "leduc": "Leduc"}


def load(name):
    with open(os.path.join(deps.RESULTS_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=250, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("saved", path)


# ------------------------------------------------------------------ 1. rank heatmaps (FM4, FM1)
def fig_ranks(game):
    d = load(f"population_{game}.json")
    names = d["agents"]
    a = d["analysis"]["2000"]
    n = len(names)
    from scipy.stats import rankdata

    def rk(v, dec, higher_better=True):
        """Competition ranks (1 = best) with ties at the stated resolution."""
        x = np.round(np.asarray(v, dtype=float), dec)
        return rankdata(-x if higher_better else x, method="min") - 1
    cols = [("Exploit.", rk(a["exploitability"], 3, False)), ("Elo", rk(a["elo"], 0)),
            ("Pop. return", rk(a["population_return"], 3)), ("RRPS score", rk(a["rrps_aggregate"], 3)),
            ("Nash avg.", rk(a["nash_avg_skill"], 4)), ("VasE", np.asarray(a["iml_rank"])),
            ("α-Rank 0.1", rk(a["alpharank"]["0.1"], 3)), ("α-Rank 100", rk(a["alpharank"]["100.0"], 3))]
    R = np.array([np.asarray(c[1], dtype=float) for c in cols]).T + 1      # 1 = best
    order = np.argsort(-np.array(a["population_return"]))
    R = R[order]
    fig, ax = plt.subplots(figsize=(7.0, 0.30 * n + 1.3))
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("b", ["#184f95", "#6da7ec", "#f4f8fd"])
    ax.imshow(R, cmap=cmap, vmin=1, vmax=n, aspect="auto")
    for i in range(n):
        for j in range(len(cols)):
            v = int(R[i, j])
            ax.text(j, i, str(v), ha="center", va="center", fontsize=FS,
                    color="white" if v <= n * 0.4 else INK)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([c[0] for c in cols], rotation=30, ha="right")
    ax.set_yticks(range(n))
    ax.set_yticklabels([names[k] for k in order])
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.set_xlabel("ranking method (rank 1 = best)")
    save(fig, f"ranks_{game}.png")


# ------------------------------------------------------------------ 2. gain vs exposure (FM1)
OFFS = {"kuhn": {"Nash": (6, -12), "BestEq": (6, 4), "RNR(0.5)": (6, -4), "DirBR": (-8, 6),
                 "DirBR-CP": (6, -12), "TypeBR": (6, 4), "BR-Tight": (-10, 8)},
        "leduc": {"Nash": (6, -12), "BestEq": (6, 4), "RNR(0.5)": (6, -4), "DirBR": (-6, 8),
                  "DirBR-CP": (-10, -14), "TypeBR": (-8, -16), "BR-Rock": (6, -4)}}


def fig_gain_exposure():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3))
    for ax, game in zip(axes, ("kuhn", "leduc")):
        d = load(f"adaptation_{game}.json")
        for a, blk in d["agents"].items():
            x = blk["stationary"]["exposure_mean"]["mean"]
            y = blk["stationary"]["population_gain"]["mean"]
            e = blk["stationary"]["population_gain"]["ci95"]
            ax.errorbar(x, y, yerr=e, fmt=MARK.get(a, "o"), ms=8, color=COL[a], mec="white", mew=1.0,
                        ecolor=COL[a], zorder=3)
            dx, dy = OFFS[game].get(a, (6, 4))
            ax.annotate(a, (x, y), xytext=(dx, dy), textcoords="offset points", fontsize=FS,
                        color=INK, ha="right" if dx < 0 else "left")
        ax.set_title(GAME[game])
        ax.set_xlabel("exposure (chips/hand)")
        ax.grid(True, axis="both")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.margins(x=0.18, y=0.15)
    axes[0].set_ylabel("gain over Nash (chips/hand)")
    fig.tight_layout()
    save(fig, "gain_exposure.png")


# ------------------------------------------------------------------ 3. alpha sweep (FM4)
def fig_alpha():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.2), sharey=True)
    show = ["Nash", "BestEq", "RNR(0.5)", "DirBR", "DirBR-CP", "TypeBR"]
    for ax, game in zip(axes, ("kuhn", "leduc")):
        d = load(f"population_{game}.json")
        names = d["agents"]
        ar = d["analysis"]["2000"]["alpharank"]
        al = sorted(ar, key=float)
        x = [float(v) for v in al]
        rest = np.zeros(len(al))
        for k, nm in enumerate(names):
            ys = np.array([ar[v][k] for v in al])
            if nm in show:
                ax.plot(x, ys, LS.get(nm, "-"), color=COL[nm], lw=1.8, marker=MARK.get(nm), ms=5, label=nm)
            else:
                rest += ys
        ax.plot(x, rest, "-", color="#b5b4ae", lw=1.8, label="all others")
        ax.set_xscale("log")
        ax.set_xlabel("selection pressure α")
        ax.set_title(GAME[game])
        ax.grid(True)
    axes[0].set_ylabel("α-Rank mass")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    save(fig, "alpha_sweep.png")


# ------------------------------------------------------------------ 4. adaptation curves
def fig_adaptation():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3), sharey=True)
    for ax, game in zip(axes, ("kuhn", "leduc")):
        d = load(f"adaptation_{game}.json")
        rep = d["curves"]["capture_vs"]
        for a, ys in d["curves"]["capture"].items():
            x = np.arange(len(ys)) * 10
            lab = "BR-specialist" if a.startswith("BR-") else a
            ax.plot(x, ys, LS.get(a, "-"), color=COL[a], lw=1.6, label=lab)
        ax.axhline(1.0, color=INK2, lw=0.8, ls=":")
        ax.set_title(f"{GAME[game]}: vs {rep}")
        ax.set_xlabel("hand")
        ax.grid(True)
    axes[0].set_ylabel("share of attainable gain")
    h, l = axes[1].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.14))
    fig.tight_layout()
    save(fig, "adaptation_curves.png")


# ------------------------------------------------------------------ 5. switch + teaching (FM7)
def fig_switch_teach():
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.6), sharex=True)
    agents = ["Nash", "BestEq", "RNR(0.5)", "DirBR", "DirBR-CP", "TypeBR"]
    spec = {"kuhn": ("SW:TightPassive>LooseAggr@1000", "TEACH:TightPassive@1000"),
            "leduc": ("SW:CallingStation>Rock@1000", "TEACH:Rock@1000")}
    short = {"SW:TightPassive>LooseAggr@1000": "TightPassive → LooseAggr",
             "SW:CallingStation>Rock@1000": "CallingStation → Rock",
             "TEACH:TightPassive@1000": "bait TightPassive → attack",
             "TEACH:Rock@1000": "bait Rock → attack"}
    for col, game in enumerate(("kuhn", "leduc")):
        d = load(f"adaptation_{game}.json")
        sw, te = spec[game]
        ax = axes[0, col]
        for a in agents:
            ys = d["curves"]["switch"][sw]["gain_over_nash"][a]
            ax.plot(np.arange(len(ys)) * 10, ys, LS.get(a, "-"), color=COL[a], lw=1.5, label=a)
        ax.axvline(1000, color=INK2, lw=0.8, ls=":")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(f"{GAME[game]}: {short[sw]}")
        ax.grid(True)
        ax = axes[1, col]
        for a in agents:
            ys = d["curves"]["teach"][te]["ev_minus_vstar"][a]
            ax.plot(np.arange(len(ys)) * 10, ys, LS.get(a, "-"), color=COL[a], lw=1.5, label=a)
        ax.axvline(1000, color=INK2, lw=0.8, ls=":")
        ax.axhline(0, color=INK2, lw=0.8)
        ax.set_title(f"{GAME[game]}: {short[te]}")
        ax.set_xlabel("hand")
        ax.grid(True)
    axes[0, 0].set_ylabel("gain over Nash\n(chips/hand)")
    axes[1, 0].set_ylabel("EV − game value\n(chips/hand)")
    h, l = axes[0, 0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    save(fig, "switch_teach.png")


# ------------------------------------------------------------------ 6. estimators per window (FM5)
def fig_fm5():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.3), sharey=True)
    est = [("chips", "raw chips", "#eda100"), ("aivat", "AIVAT", "#2a78d6"), ("ev", "policy-exact", "#0b0b0b")]
    for ax, game in zip(axes, ("kuhn", "leduc")):
        d = load(f"adaptation_{game}.json")
        c = d["curves"]
        x = np.array(c["fm5_window_starts"]) + 50
        for key, lab, colr in est:
            m, s = np.array(c[f"fm5_{key}_mean"]), np.array(c[f"fm5_{key}_sd"])
            if key != "ev":
                ax.fill_between(x, m - s, m + s, color=colr, alpha=0.22 if key == "chips" else 0.30, lw=0)
            ax.plot(x, m, color=colr, lw=1.6, label=lab)
        ag, op = c["fm5_pair"]
        ax.set_title(f"{GAME[game]}: {ag} vs {op}")
        ax.set_xlabel("hand (centre of 100-hand window)")
        ax.grid(True)
    axes[0].set_ylabel("estimated share of\nattainable gain")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(0.5, -0.12))
    fig.tight_layout()
    save(fig, "fm5_estimators.png")


# ------------------------------------------------------------------ 7. learned best response (FM3)
def fig_approx():
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.4), sharey=True)
    tcol = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7"]
    for ax, game in zip(axes, ("kuhn", "leduc")):
        d = load(f"approx_br_{game}.json")
        b = d["budgets"]
        k = 0
        for t, blk in d["targets"].items():
            if blk["exact_exploitability"] < 1e-3:
                continue
            ys = [blk["by_budget"][str(x)]["ratio"] for x in b]
            ax.plot(b, ys, "-o", color=tcol[k % len(tcol)], lw=1.5, ms=4, label=t)
            k += 1
        ax.axhline(1.0, color=INK2, lw=0.8, ls=":")
        ax.axhline(0.0, color=INK2, lw=0.8)
        ax.set_xscale("log")
        ax.set_xlabel("learning budget (hands per seat)")
        ax.set_title(GAME[game])
        ax.grid(True)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.24), ncol=2, frameon=False, fontsize=FS)
    axes[0].set_ylabel("learned ÷ exact\nexploitability")
    fig.tight_layout()
    save(fig, "approx_br.png")


# ------------------------------------------------------------------ 8. three-player Kuhn (FM2, FM8)
def fig_nplayer():
    d = load("nplayer_kuhn3.json")
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4))
    ax = axes[0]
    eq = d["part1"]["equilibria"]
    w = 0.2
    seats = np.arange(3)
    series = [("CFR+", "value", "#2a78d6"), ("CFR+", "coalition", "#9ec5f4"),
              ("CFR", "value", "#eb6834"), ("CFR", "coalition", "#f5b89e")]
    for k, (e, kind, colr) in enumerate(series):
        ys = eq[e]["values"] if kind == "value" else eq[e]["coalition_value"]
        ax.bar(seats + (k - 1.5) * w, ys, width=w - 0.02, color=colr,
               label=f"{e}: {'equilibrium' if kind == 'value' else 'vs coalition'}")
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_xticks(seats)
    ax.set_xticklabels([f"seat {s}" for s in seats])
    ax.set_ylabel("value (chips/hand)")
    ax.set_title("Equilibrium seats")
    ax.grid(True, axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1, frameon=False)
    ax = axes[1]
    pr = d["part3"]["protocol"]
    agents = ["Nash", "Blend3P", "DirBR3P"]
    conds = [("independent pairs", lambda v: None), ]
    # absolute mean EV per condition (independent: mean over all pairs; colluders; teaching after switch)
    ind = []
    for a in agents:
        ind.append(None)
    x = np.arange(len(agents))
    vals = {"fixed colluders": [pr[a]["colluders_mean_ev"]["mean"] for a in agents],
            "teaching coalition": [pr[a]["teach_ev_after"]["mean"] for a in agents],
            "coalition value": [pr[a]["coalition_value_final_policy"]["mean"] for a in agents]}
    vals = {("coalition value (final policy)" if k == "coalition value" else k): v for k, v in vals.items()}
    cc = {"fixed colluders": "#1baf7a", "teaching coalition": "#e34948", "coalition value (final policy)": "#4a3aa7"}
    for k, (lab, ys) in enumerate(vals.items()):
        ax.bar(x + (k - 1) * 0.26, ys, width=0.24, color=cc[lab], label=lab)
    ax.axhline(0, color=INK2, lw=0.8)
    ax.set_axisbelow(True)
    axes[0].set_axisbelow(True)
    ax.set_xticks(x)
    ax.set_xticklabels(agents)
    ax.set_ylabel("value (chips/hand)")
    ax.set_title("Adaptive agents vs a pair")
    ax.grid(True, axis="y")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=1, frameon=False)
    fig.tight_layout()
    save(fig, "nplayer.png")


if __name__ == "__main__":
    fig_ranks("kuhn")
    fig_ranks("leduc")
    fig_gain_exposure()
    fig_alpha()
    fig_adaptation()
    fig_switch_teach()
    fig_fm5()
    fig_approx()
    fig_nplayer()
