"""Render the §8 Pareto frontier plot from `.day05_pareto.json`.

A single matplotlib figure with `info_sets` on the x-axis (log scale)
and `exploit_gap` on the y-axis (log scale, with zeros clipped to a
small positive epsilon so they remain visible). One marker per
configuration, with the EMD-proxy shown as marker size where available.

Output: `phase4/figures/day05_pareto.png`.
"""

import json
import os
import sys
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(_HERE, "figures")
INPUT_JSON = os.path.join(_HERE, ".day05_pareto.json")
OUTPUT_PNG = os.path.join(FIG_DIR, "day05_pareto.png")

if _HERE not in sys.path:
    sys.path.insert(0, _HERE)


def main():
    if not os.path.exists(INPUT_JSON):
        print(f"missing: {INPUT_JSON}. Run day05_pareto.py first.")
        return 1

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plot rendering.")
        return 0

    os.makedirs(FIG_DIR, exist_ok=True)
    with open(INPUT_JSON) as f:
        rows = json.load(f)

    # Filter to rows with both info_sets and exploit_gap.
    pts = [(r["info_sets"], r["exploit_gap"], r["name"], r["emd_proxy"])
           for r in rows
           if r["info_sets"] is not None and r["exploit_gap"] is not None]
    if not pts:
        print("no usable points; nothing to plot.")
        return 0

    eps = 1e-6
    grouped = defaultdict(list)
    for info_sets, exploit_gap, name, emd_proxy in pts:
        x = max(info_sets, 1)
        y = max(exploit_gap, eps)
        grouped[(x, y)].append((name, emd_proxy))

    xs = []
    ys = []
    labels = []
    sizes = []
    for (x, y), members in sorted(grouped.items()):
        names = [m[0] for m in members]
        emd_values = [m[1] for m in members if m[1] is not None]
        xs.append(x)
        ys.append(y)
        labels.append(_short_label(names))
        sizes.append(80.0 if not emd_values
                     else 80.0 + 20.0 * max(emd_values))

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(xs, ys, s=sizes, alpha=0.7)
    for x, y, lbl in zip(xs, ys, labels):
        ha = "right" if x > 3000 else "left"
        dx = -5 if ha == "right" else 5
        ax.annotate(lbl, (x, y), fontsize=7,
                    xytext=(dx, 5), textcoords="offset points",
                    ha=ha)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(min(xs) * 0.75, max(xs) * 1.35)
    ax.set_ylim(min(ys) * 0.5, max(ys) * 1.9)
    ax.set_xlabel("info-set count")
    ax.set_ylabel("exploitability gap Δ_abs (full game)")
    ax.set_title("Phase 4 — Pareto frontier across abstraction "
                 "configurations\n(marker size scales with EMD proxy)")
    ax.grid(True, which="both", linestyle="--", alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=150)
    print(f"Saved: {OUTPUT_PNG}")
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


if __name__ == "__main__":
    raise SystemExit(main())
