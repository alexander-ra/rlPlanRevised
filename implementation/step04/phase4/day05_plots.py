"""Render the §8 Pareto frontier plot.

Default: the frontier of the final 180-second CFR+ benchmark
(`.day07_cfrplus_results.json`, written by `day07_cfrplus_panels.py`) —
the same runs the chapter text and the three CFR+ panels report. For each
configuration the mean full-game exploitability of its three runs is
plotted against its information-set count (both log scale), one colour per
game, and the non-dominated points of each game are joined by a step line.
Action-abstraction configurations are drawn hollow: in the current harness
every abstract small bet is played as the large bet and the translators
never engage (final review F04-C01), so their values describe that
deployment rule, not translation quality.

`--smoke-test`: the original plot of the smoke-test runs in
`.day05_pareto.json` (vanilla CFR, 200/100 iterations), written to
`figures/day05_pareto_smoke.png`. Not used in the chapter.

This script only reads result files; it never trains or re-saves them.

Output: `phase4/figures/day05_pareto.png`.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from statistics import mean

_HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(_HERE, "figures")
CFRPLUS_JSON = os.path.join(_HERE, ".day07_cfrplus_results.json")
OUTPUT_PNG = os.path.join(FIG_DIR, "day05_pareto.png")
SMOKE_JSON = os.path.join(_HERE, ".day05_pareto.json")
SMOKE_PNG = os.path.join(FIG_DIR, "day05_pareto_smoke.png")

if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# game -> (legend label, colour, marker)
GAMES = {
    "fixed": ("Fixed-limit Leduc", "#1f77b4", "o"),
    "mini": ("Mini-NL Leduc", "#d95f02", "s"),
    "extended": ("Extended Leduc", "#1b9e77", "^"),
}
ACTION_ABS_CONFIGS = {"mini_action_abs", "ext_suit_action", "ext_triple"}

# Configurations that land on (almost) the same point share one label.
POINT_GROUPS = {
    ("fixed", ("Suit iso", "full bucket p", "full bucket i")):
        "Suit isomorphism / rank buckets",
    ("fixed", ("k3 perfect", "k5 perfect")): "k3/k5, perfect recall",
    ("fixed", ("k3 imperfect", "k5 imperfect")): "k3/k5, imperfect recall",
}
LABELS = {
    ("fixed", "Full CFR+"): "Full game",
    ("fixed", "k2 perfect"): "k2, perfect recall",
    ("fixed", "k2 imperfect"): "k2, imperfect recall",
    ("mini", "Full mini-NL"): "Full game",
    ("mini", "Action abs"): "Action abstraction",
    ("extended", "Full extended"): "Full game",
    ("extended", "Suit iso"): "Suit isomorphism",
    ("extended", "Suit + action"): "Suits + actions",
    ("extended", "Suit + action + buckets"): "Suits + actions + buckets",
}
# Label placement (offset in points, horizontal alignment), chosen so that
# neither the English nor the ~15 % longer Bulgarian labels collide.
PLACEMENT = {
    ("fixed", "Full game"): ((7, 0), "left", "center"),
    ("fixed", "Suit isomorphism / rank buckets"): ((7, 0), "left", "center"),
    ("fixed", "k2, perfect recall"): ((3, 8), "left", "bottom"),
    ("fixed", "k2, imperfect recall"): ((0, -9), "center", "top"),
    ("fixed", "k3/k5, perfect recall"): ((7, 0), "left", "center"),
    ("fixed", "k3/k5, imperfect recall"): ((-3, 8), "right", "bottom"),
    ("mini", "Full game"): ((-7, 0), "right", "center"),
    ("mini", "Action abstraction"): ((7, 0), "left", "center"),
    ("extended", "Full game"): ((0, 9), "center", "bottom"),
    ("extended", "Suit isomorphism"): ((-7, 0), "right", "center"),
    ("extended", "Suits + actions"): ((7, 0), "left", "center"),
    ("extended", "Suits + actions + buckets"): ((0, 9), "center", "bottom"),
}


def _points(rows):
    """[(game, label, info_sets, mean exploitability, action_abs)]."""
    by_cfg = defaultdict(list)
    for r in rows:
        if r.get("exploitability") is None:
            continue
        by_cfg[(r["panel"], r["label"], r["config"])].append(r)
    singles = {}
    for (game, label, config), rs in by_cfg.items():
        singles[(game, label)] = (
            round(mean(r["info_sets"] for r in rs)),
            mean(r["exploitability"] for r in rs),
            config in ACTION_ABS_CONFIGS,
        )
    points = []
    used = set()
    for (game, members), shown in POINT_GROUPS.items():
        found = [singles[(game, m)] for m in members if (game, m) in singles]
        if not found:
            continue
        used.update((game, m) for m in members)
        points.append((game, shown, round(mean(f[0] for f in found)),
                       mean(f[1] for f in found), found[0][2]))
    for key, (info, expl, action) in singles.items():
        if key in used:
            continue
        points.append((key[0], LABELS.get(key, key[1]), info, expl, action))
    return points


def _frontier(pts):
    """Non-dominated (info_sets, exploitability) points, smallest game first."""
    front = []
    for info, expl in sorted(pts):
        if not front or expl < front[-1][1]:
            front.append((info, expl))
    return front


def plot_cfrplus():
    if not os.path.exists(CFRPLUS_JSON):
        print(f"missing: {CFRPLUS_JSON}. Run day07_cfrplus_panels.py first.")
        return 1
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    with open(CFRPLUS_JSON) as f:
        rows = json.load(f)
    points = _points(rows)

    os.makedirs(FIG_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5.8))
    for game, (name, colour, marker) in GAMES.items():
        gp = [p for p in points if p[0] == game]
        if not gp:
            continue
        front = _frontier([(p[2], p[3]) for p in gp])
        fx = [p[0] for p in front]
        fy = [p[1] for p in front]
        ax.step(fx, fy, where="post", color=colour, linewidth=1.3,
                alpha=0.7, zorder=2)
        for _, label, info, expl, action in gp:
            ax.scatter([info], [expl], s=55, marker=marker, zorder=3,
                       facecolors="none" if action else colour,
                       edgecolors=colour, linewidths=1.5)
            (dx, dy), ha, va = PLACEMENT.get((game, label),
                                             ((7, 0), "left", "center"))
            ax.annotate(label, (info, expl), xytext=(dx, dy),
                        textcoords="offset points", ha=ha, va=va,
                        fontsize=10, color="#222222",
                        bbox=dict(boxstyle="square,pad=0.1", fc="white",
                                  ec="none", alpha=0.85))
        # empty proxy lines carry the legend entries: the Bulgarian renderer
        # translates plot(label=...), not labels stored inside handles
        ax.plot([], [], color=colour, marker=marker, markersize=7,
                linewidth=1.3, label=name)
    ax.plot([], [], color="#555555", marker="o", markerfacecolor="none",
            linestyle="none", markersize=7,
            label="Action abstraction (see text)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(15, 60000)
    ax.set_ylim(1e-6, 100)
    ax.set_xlabel("Number of information sets", fontsize=11)
    ax.set_ylabel("Full-game exploitability", fontsize=11)
    ax.tick_params(labelsize=10)
    ax.grid(True, which="major", linestyle="--", alpha=0.3)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2,
              fontsize=10, frameon=False)

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {OUTPUT_PNG}")
    return 0


# --------------------------------------------------------------------------
# Original smoke-test plot (kept for reference; not used in the chapter)
# --------------------------------------------------------------------------

def plot_smoke_test():
    if not os.path.exists(SMOKE_JSON):
        print(f"missing: {SMOKE_JSON}. Run day05_pareto.py first.")
        return 1
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    os.makedirs(FIG_DIR, exist_ok=True)
    with open(SMOKE_JSON) as f:
        rows = json.load(f)

    pts = [(r["info_sets"], r["exploit_gap"], r["name"], r["emd_proxy"])
           for r in rows
           if r["info_sets"] is not None and r["exploit_gap"] is not None]
    if not pts:
        print("no usable points; nothing to plot.")
        return 0

    eps = 1e-6
    grouped = defaultdict(list)
    for info_sets, exploit_gap, name, emd_proxy in pts:
        grouped[(max(info_sets, 1), max(exploit_gap, eps))].append(
            (name, emd_proxy))

    xs, ys, labels, sizes = [], [], [], []
    for (x, y), members in sorted(grouped.items()):
        emd_values = [m[1] for m in members if m[1] is not None]
        xs.append(x)
        ys.append(y)
        labels.append(_short_label([m[0] for m in members]))
        sizes.append(80.0 if not emd_values
                     else 80.0 + 20.0 * max(emd_values))

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(xs, ys, s=sizes, alpha=0.7)
    for x, y, lbl in zip(xs, ys, labels):
        ha = "right" if x > 3000 else "left"
        dx = -5 if ha == "right" else 5
        ax.annotate(lbl, (x, y), fontsize=7, xytext=(dx, 5),
                    textcoords="offset points", ha=ha)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(xs) * 0.75, max(xs) * 1.35)
    ax.set_ylim(min(ys) * 0.5, max(ys) * 1.9)
    ax.set_xlabel("info-set count")
    ax.set_ylabel("exploitability gap Δ_abs (full game)")
    ax.set_title("Smoke test (vanilla CFR, 200/100 iterations) — zero gaps "
                 "drawn at 1e-6\n(marker size scales with EMD proxy)")
    ax.grid(True, which="both", linestyle="--", alpha=0.3)
    fig.tight_layout()
    fig.savefig(SMOKE_PNG, dpi=150)
    plt.close(fig)
    print(f"Saved: {SMOKE_PNG}")
    return 0


def _short_label(names: list) -> str:
    names = sorted(names)
    if set(names) == {
        "day3_translator_nearest",
        "day3_translator_probability_split",
        "day3_translator_pseudo_harmonic",
    }:
        return "day3 translators"
    if set(names) == {"day2_k3_perfect", "day2_k5_perfect"}:
        return "day2 k3/k5 perfect"
    if set(names) == {"day2_k3_imperfect", "day2_k5_imperfect"}:
        return "day2 k3/k5 imperfect"
    if set(names) == {
        "day1_rank_canonical",
        "day2_full_imperfect",
        "day2_full_perfect",
    }:
        return "lossless/full buckets"
    if len(names) == 1:
        return names[0].replace("_", " ")
    return "\n".join(n.replace("_", " ") for n in names)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-test", action="store_true",
                    help="plot the old smoke-test runs instead")
    args = ap.parse_args()
    return plot_smoke_test() if args.smoke_test else plot_cfrplus()


if __name__ == "__main__":
    raise SystemExit(main())
