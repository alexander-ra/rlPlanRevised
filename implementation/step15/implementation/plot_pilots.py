"""
plot_pilots.py -- every data figure of Chapter 15, drawn from the saved results JSON only
(no simulation, no re-solving). Output: deliverables/reports/step15/figures/*.png

    python plot_pilots.py [--only name ...]

Print rules (September review): figures are 7 in wide and print at 17.6 cm, so the scale is ~1
and every text element uses fontsize >= 10; dpi 250; legends outside the data; every axis
labelled; short labels (they will be translated). Colours follow the agent across figures and
continue Chapter 14's assignment (Nash grey, BestEq aqua, RNR blue, DirBR orange).
"""

from __future__ import annotations

import argparse
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import boot

OUT = boot.FIG_DIR
os.makedirs(OUT, exist_ok=True)
FS = 10
plt.rcParams.update({"font.size": FS, "axes.titlesize": 11, "axes.labelsize": FS,
                     "xtick.labelsize": FS, "ytick.labelsize": FS, "legend.fontsize": FS,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#52514e", "axes.labelcolor": "#0b0b0b",
                     "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "grid.color": "#e4e3df", "grid.linewidth": 0.8})
INK, INK2, GRID = "#0b0b0b", "#52514e", "#e4e3df"
COL = {"Nash": "#52514e", "BestEq": "#1baf7a", "RNR(0.5)": "#2a78d6", "DirBR": "#eb6834",
       "RWYWE": "#4a3aa7", "RWYWE-rev": "#e87ba4", "RWYWE-tb": "#008300", "BEFEWP": "#eda100",
       "BEFFE": "#9b9a94", "Best Equilibrium": "#1baf7a", "Best response": "#eb6834",
       "DirBR3P": "#eb6834", "Blend3P": "#2a78d6", "Maximin": "#e34948", "MM-BestEq": "#e34948",
       "MM-RWYWE": "#e34948", "MM-RWYWE-sd": "#e34948"}
MARK = {"Nash": "s", "BestEq": "D", "RNR(0.5)": "o", "DirBR": "^", "RWYWE": "*", "RWYWE-rev": "P",
        "RWYWE-tb": "X", "BEFEWP": "v"}
LABEL = {"RWYWE-rev": "RWYWE (cards shown)", "RWYWE": "RWYWE (showdown)"}
GAME = {"kuhn": "Kuhn", "leduc": "Leduc"}


def load(name):
    with open(os.path.join(boot.RESULTS_DIR, name), encoding="utf-8") as fh:
        return json.load(fh)


def exists(name):
    return os.path.exists(os.path.join(boot.RESULTS_DIR, name))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=250, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    print("saved", path)


# ------------------------------------------------------------------ P0: replication of G&S Table I
def fig_gs_replication():
    d = load("gs_replication.json")
    rules = ["rwywe", "befewp", "beffe", "besteq", "br"]
    names = {"rwywe": "RWYWE", "befewp": "BEFEWP", "beffe": "BEFFE", "besteq": "Best equilibrium",
             "br": "Best response"}
    col = {"rwywe": COL["RWYWE"], "befewp": COL["BEFEWP"], "beffe": "#9b9a94",
           "besteq": COL["BestEq"], "br": COL["DirBR"]}
    classes = [("random", "Random"), ("sophisticated", "Near-equilibrium"), ("dynamic", "Dynamic")]
    fig, axes = plt.subplots(1, 3, figsize=(7.0, 3.0))
    ticks = {"random": [0.0, 0.2, 0.4], "sophisticated": [-0.05, 0.0, 0.05], "dynamic": [-0.15, -0.05, 0.0]}
    for ax, (c, title) in zip(axes, classes):
        y = np.arange(len(rules))[::-1]
        for yy, r in zip(y, rules):
            e = d["table"][r][c]
            ax.errorbar(e["ev"], yy, xerr=e["ev_ci95"], fmt="o", color=col[r], ms=6, capsize=2, zorder=3)
            ax.plot(e["gs"], yy, marker="|", color=INK, ms=14, mew=2, zorder=4)
        ax.axvline(d["setup"]["v_star"], color=INK2, lw=0.8, ls=":")
        ax.set_yticks(y)
        ax.set_yticklabels([names[r] for r in rules] if ax is axes[0] else [])
        ax.set_title(title)
        ax.set_xticks(ticks[c])
        ax.set_xticklabels([f"{t:g}" for t in ticks[c]])
        lo, hi = min(ticks[c]), max(ticks[c])
        ax.set_xlim(lo - 0.25 * (hi - lo), hi + 0.25 * (hi - lo))
        ax.grid(axis="x")
        ax.set_xlabel("chips/hand")
    fig.text(0.5, -0.13, "dot: this replication (95 % CI)   bar: G&S (2015), Table I   dotted: v*",
             ha="center", fontsize=FS, color=INK2)
    fig.tight_layout(w_pad=1.0)
    save(fig, "gs_replication.png")


# ------------------------------------------------------------------ P1: gain vs exposure, two games
def fig_gain_exposure():
    games = [g for g in ("kuhn", "leduc") if exists(f"protocol2p_{g}.json")]
    fig, axes = plt.subplots(1, len(games), figsize=(7.0, 3.1))
    axes = np.atleast_1d(axes)
    order = ["Nash", "BestEq", "BEFEWP", "RWYWE", "RWYWE-rev", "RNR(0.5)", "DirBR"]
    for ax, g in zip(axes, games):
        d = load(f"protocol2p_{g}.json")
        for a in order:
            if a not in d["agents"]:
                continue
            s = d["agents"][a]["stationary"]
            x, y = s["exposure_mean"]["mean"], s["population_gain"]["mean"]
            ax.errorbar(x, y, yerr=s["population_gain"]["ci95"], xerr=s["exposure_mean"]["ci95"],
                        fmt=MARK.get(a, "o"), color=COL[a], ms=8 if a != "RWYWE" else 11, capsize=2,
                        label=LABEL.get(a, a), zorder=3)
        ax.set_xscale("symlog", linthresh=0.02)
        ax.set_title(GAME[g])
        ax.set_xlabel("mean exposure (chips/hand)")
        ax.grid(True)
        ax.set_ylim(bottom=-0.02 * ax.get_ylim()[1])
    axes[0].set_ylabel("gain over Nash (chips/hand)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="lower center", ncol=4, frameon=False, bbox_to_anchor=(0.5, -0.13))
    fig.tight_layout(rect=(0, 0.1, 1, 1))
    save(fig, "rwywe_gain_exposure.png")


# ------------------------------------------------------------------ P1: the teaching attack over the match
def fig_teach(game="kuhn", bait_S="TightPassive", bait_k="LooseAggr"):
    """(a) running match-level safety S under a teaching attack whose bait gives few gifts;
    (b) RWYWE's bank k under a bait that gives many -- spent after the switch."""
    d = load(f"protocol2p_{game}.json")
    T = d["switch_at"]
    curS = d["curves"]["teach"][f"TEACH1:{bait_S}@{T}"]
    curK = d["curves"]["teach"][f"TEACH1:{bait_k}@{T}"]
    agents = ["BestEq", "RWYWE", "RNR(0.5)", "DirBR"]
    x = np.arange(len(curS["ev_minus_vstar"]["Nash"])) * 10
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.0, 4.8), sharex=True,
                                 gridspec_kw={"height_ratios": [1.5, 1.0]})
    for a in agents:
        run = np.asarray(curS["cum_ev_minus_vstar"][a]) / (x + 1)
        a1.plot(x, run, color=COL[a], lw=2, label=LABEL.get(a, a))
    a1.axhline(0, color=INK, lw=0.8)
    a1.axvline(T, color=INK2, lw=0.8, ls=":")
    others = [a for a in agents if a != "DirBR"]
    endv = np.mean([np.asarray(curS["cum_ev_minus_vstar"][a])[-1] / (x[-1] + 1) for a in others])
    a1.text(120, 0.022, "BestEq, RWYWE and RNR(0.5)\n" + f"overlap; S ends at {endv:+.3f}",
            fontsize=FS, color=INK2, va="bottom")
    a1.set_ylabel("running S\n(chips/hand)")
    a1.set_title(f"(a) bait {bait_S}, then best response every hand", loc="left")
    a1.grid(True)
    a1.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0), frameon=False)
    a2.plot(x, curK["k"]["RWYWE"], color=COL["RWYWE"], lw=2)
    a2.axvline(T, color=INK2, lw=0.8, ls=":")
    a2.set_ylabel("RWYWE bank k\n(chips)")
    a2.set_title(f"(b) bait {bait_k}: the bank is spent after the switch", loc="left")
    a2.set_xlabel("hand (attack from hand %d)" % T)
    a2.grid(True)
    fig.tight_layout()
    save(fig, f"rwywe_teach_{game}.png")


# ------------------------------------------------------------------ P2: gain vs baseline-relative loss
def _bd_color(i, n):
    ramp = ["#c9c3f0", "#a69be2", "#7f70cf", "#5b4bb8", "#3b2d8f"]
    return ramp[min(i, len(ramp) - 1)]


def fig_bounded_frontier():
    d = load("bounded3p.json")
    S = d["summary"]
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    bd = [a for a in d["agents"] if a.startswith("BD(")]
    kl = [a for a in d["agents"] if a.startswith("KL(")]

    def pt(a):
        s = S[a]["indep"]
        return s["L_max"]["max"], s["gain"]["mean"], s["gain"]["ci95"]
    xs, ys = zip(*[pt(a)[:2] for a in bd])
    ax.plot(xs, ys, "-", color="#7f70cf", lw=1.5, zorder=2)
    bd_off = {"BD(0.01)": (4, 6), "BD(0.03)": (4, -14), "BD(0.1)": (4, -14), "BD(0.3)": (6, -14),
              "BD(inf)": (6, -14)}
    for a in bd:
        x, y, e = pt(a)
        ax.errorbar(x, y, yerr=e, fmt="o", color="#5b4bb8", ms=7, capsize=2, zorder=3)
        ax.annotate("ε=" + a[3:-1].replace("inf", "∞"), (x, y), textcoords="offset points",
                    xytext=bd_off.get(a, (4, -12)), fontsize=FS, color=INK2)
    xs, ys = zip(*[pt(a)[:2] for a in kl])
    ax.plot(xs, ys, "-", color="#1baf7a", lw=1.5, zorder=2)
    kl_off = {"KL(1)": (6, 4), "KL(3)": (6, 4), "KL(10)": (-46, -4), "KL(30)": (-46, 0)}
    for a in kl:
        x, y, e = pt(a)
        ax.errorbar(x, y, yerr=e, fmt="D", color="#127d57", ms=6, capsize=2, zorder=3)
        ax.annotate("β=" + a[3:-1], (x, y), textcoords="offset points", xytext=kl_off.get(a, (4, 5)),
                    fontsize=FS, color=INK2)
    for a, m, off in (("DirBR3P", "^", (6, -14)), ("Blend3P", "o", (-30, 8))):
        if a in S:
            x, y, e = pt(a)
            ax.errorbar(x, y, yerr=e, fmt=m, color=COL[a], ms=7, capsize=2, zorder=4)
            ax.annotate(a, (x, y), textcoords="offset points", xytext=off, fontsize=FS, color=INK)
    ax.set_xscale("log")
    ax.set_xlim(0.006, 2.2)
    ax.set_ylim(-0.02, 0.33)
    ax.set_xlabel("worst-case loss relative to the blueprint, L (chips/hand)")
    ax.set_ylabel("gain over the blueprint\n(chips/hand)")
    ax.grid(True)
    from matplotlib.lines import Line2D
    hs = [Line2D([], [], color="#5b4bb8", marker="o", lw=1.5, label="capped mixture BD(ε)"),
          Line2D([], [], color="#127d57", marker="D", lw=1.5, label="KL anchor KL(β)")]
    ax.legend(handles=hs, loc="upper left", frameon=False)
    fig.tight_layout()
    save(fig, "bounded3p_frontier.png")


def fig_bounded_coalition():
    """Gain against independent pairs vs seat-averaged EV under adaptive colluders (after the
    switch), for every three-player agent; equal share (0) and the seat-averaged maximin value."""
    d = load("bounded3p.json")
    S = d["summary"]
    mm = load("maximin3p.json")
    fig, ax = plt.subplots(figsize=(7.0, 3.9))

    def pt(a):
        return S[a]["indep"]["gain"]["mean"], S[a]["teach"]["seat_avg_ev"]["mean"], S[a]["teach"]["seat_avg_ev"]["ci95"]
    bd = [a for a in d["agents"] if a.startswith("BD(")]
    kl = [a for a in d["agents"] if a.startswith("KL(")]
    for group, col, mk, lab in ((bd, "#5b4bb8", "o", "capped mixture BD(ε)"),
                                (kl, "#127d57", "D", "KL anchor KL(β)")):
        xs, ys, es = zip(*[pt(a) for a in group])
        ax.plot(xs, ys, "-", color=col, lw=1.5, zorder=2)
        ax.errorbar(xs, ys, yerr=es, fmt=mk, color=col, ms=6, capsize=2, zorder=3, label=lab)
    single = [("Nash", "s", "#52514e", "blueprint", (6, -12)), ("DirBR3P", "^", "#eb6834", "DirBR3P", (-20, 8)),
              ("Blend3P", "o", "#2a78d6", "Blend3P", (6, 4)), ("Maximin", "s", "#e34948", "maximin", (6, 6)),
              ("MM-RWYWE", "*", "#e34948", "MM-RWYWE", (6, 6))]
    for a, m, c, lab, off in single:
        x, y, e = pt(a)
        ax.errorbar(x, y, yerr=e, fmt=m, color=c, ms=10 if m == "*" else 7, capsize=2, zorder=4)
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=off, fontsize=FS, color=INK)
    ax.axhline(0, color=INK, lw=1)
    ax.text(0.305, 0.004, "equal share", ha="right", va="bottom", color=INK, fontsize=FS)
    ax.axhline(mm["seat_average_maximin"], color="#e34948", lw=1, ls="--")
    ax.text(0.305, mm["seat_average_maximin"] - 0.006, "maximin value", ha="right", va="top",
            color=INK, fontsize=FS)
    ax.set_xlabel("gain over the blueprint vs independent pairs (chips/hand)")
    ax.set_ylabel("EV under adaptive\ncolluders (chips/hand)")
    ax.grid(True)
    ax.legend(loc="lower left", frameon=False)
    fig.tight_layout()
    save(fig, "bounded3p_coalition.png")


FIGS = {"gs": fig_gs_replication, "gain_exposure": fig_gain_exposure, "teach": fig_teach,
        "frontier": fig_bounded_frontier, "coalition": fig_bounded_coalition}
NEEDS = {"gs": ["gs_replication.json"], "gain_exposure": ["protocol2p_kuhn.json"],
         "teach": ["protocol2p_kuhn.json"], "frontier": ["bounded3p.json"],
         "coalition": ["bounded3p.json", "maximin3p.json"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="+", default=None)
    args = ap.parse_args()
    for k, fn in FIGS.items():
        if args.only and k not in args.only:
            continue
        if not all(exists(n) for n in NEEDS[k]):
            print("skip", k, "(results missing)")
            continue
        fn()


if __name__ == "__main__":
    main()
