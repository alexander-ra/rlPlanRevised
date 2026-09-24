"""
plotting.py -- figures for Step 08 (guarded; import fails cleanly if matplotlib is absent).

Callers do `import plotting` inside a try/except ImportError, so if matplotlib is not
installed this module simply fails to import and the JSON results are still complete.

Figures:
  - plot_pareto      : the exploitation-safety frontier (RNR canonical vs naive + method points).
  - plot_tournament  : per-method exploitation & worst-case bars + teaching-attack curves.

Run directly (`python plotting.py`) to redraw the chapter figures from the SAVED results
(results/kuhn_scale.json, results/pareto_kuhn.json) into deliverables/reports/step08/figures/
as impl_*.png. Nothing is recomputed and no results file is written.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Display names for the figures. The method ids stay as the result keys; only the
# label drawn in the figure changes. `ganzfried` is the best-equilibrium baseline of
# Ganzfried & Sandholm (a per-hand floor at v* admits only equilibrium strategies).
DISPLAY = {"ganzfried": "best equilibrium", "prime_safe": "prime-safe"}
TICK_DISPLAY = {"ganzfried": "best eq."}
FS = 10          # every text element prints at >= 8.2 pt at the chapter's print width
DPI = 300


def _minus(s: str) -> str:
    """Typographic minus for negative numbers in labels."""
    return s.replace("-0", "−0").replace("-1", "−1")


def plot_pareto(all_results, out_dir, prefix=""):
    os.makedirs(out_dir, exist_ok=True)
    for game_name, data in all_results.items():
        fig, ax = plt.subplots(figsize=(7, 4.8))
        canon = data["rnr_canonical"]
        naive = data["rnr_naive"]
        ax.plot([r["exploitation_value"] for r in naive], [r["exploitability"] for r in naive],
                "--s", color="tab:gray", ms=4, label="naive Nash/BR blend")
        # canonical RNR returns only two clusters of points: markers only, no joining line
        ax.plot([r["exploitation_value"] for r in canon], [r["exploitability"] for r in canon],
                "o", color="tab:blue", ms=7, label="RNR canonical")
        low = [r for r in canon if r["exploitability"] < 0.05]
        high = [r for r in canon if r["exploitability"] >= 0.05]
        if low:
            ax.annotate(f"p ≤ {max(r['p'] for r in low):.1f}",
                        (low[0]["exploitation_value"], low[0]["exploitability"]),
                        xytext=(12, 40), textcoords="offset points", fontsize=FS,
                        color="tab:blue", arrowprops=dict(arrowstyle="-", color="tab:blue", lw=0.8))
        if high:
            ax.annotate(f"p ≥ {min(r['p'] for r in high):.1f}",
                        (high[0]["exploitation_value"], high[0]["exploitability"]),
                        xytext=(-70, -8), textcoords="offset points", fontsize=FS,
                        color="tab:blue")
        colors = {"ganzfried": "tab:green", "prime_safe": "tab:orange",
                  "adaptation": "tab:red"}
        pts = data["points"]
        # prime_safe and adaptation share one point here (same floor, same baseline)
        merged = {}
        for name, pt in pts.items():
            key = (round(pt["exploitation_value"], 9), round(pt["exploitability"], 9))
            merged.setdefault(key, []).append(name)

        def _label(names):
            return " = ".join(DISPLAY.get(n, n) for n in names)

        for (x, y), names in merged.items():
            ax.scatter([x], [y], color=colors.get(names[0], "black"), s=110, zorder=5,
                       label=_label(names), marker="*")
        ax.set_xlabel(f"exploitation profit (EV vs {data.get('exploitee', 'opponent')})",
                      fontsize=FS)
        ax.set_ylabel("exploitability (game value − worst case; ≥ 0)", fontsize=FS)
        ax.tick_params(labelsize=FS)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=FS, loc="upper left")

        # inset: the safe corner, where the LP operating points separate
        ins = ax.inset_axes([0.55, 0.12, 0.42, 0.42])
        ins.plot([r["exploitation_value"] for r in naive], [r["exploitability"] for r in naive],
                 "--s", color="tab:gray", ms=4)
        ins.plot([r["exploitation_value"] for r in canon], [r["exploitability"] for r in canon],
                 "o", color="tab:blue", ms=7)
        for (x, y), names in merged.items():
            ins.scatter([x], [y], color=colors.get(names[0], "black"), s=110, zorder=5,
                        marker="*")
        ins.set_xlim(-0.050, -0.035)
        ins.set_ylim(-0.0005, 0.010)
        ins.set_xticks([-0.048, -0.044, -0.040, -0.036])
        ins.set_yticks([0.0, 0.004, 0.008])
        ins.tick_params(labelsize=FS - 1)
        ins.grid(True, alpha=0.3)
        ax.indicate_inset_zoom(ins, edgecolor="0.4")

        fig.tight_layout()
        path = os.path.join(out_dir, f"{prefix}pareto_{game_name}.png")
        fig.savefig(path, dpi=DPI)
        plt.close(fig)


def plot_tournament(all_results, out_dir, prefix=""):
    os.makedirs(out_dir, exist_ok=True)
    for game_name, result in all_results.items():
        methods = result["methods"]
        table = result["table"]
        # representative opponent = the first non-Nash opponent in the table.
        opp_name = next((o for o in table if o != "Nash"), next(iter(table)))
        row = table[opp_name]
        evs = [row[m].get("exploitation_value", 0.0) for m in methods]
        wcs = [row[m].get("worst_case_value", 0.0) for m in methods]

        fig, ax = plt.subplots(figsize=(7, 4.2))
        x = range(len(methods))
        w = 0.38
        ax.bar([i - w / 2 for i in x], evs, width=w, color="tab:green",
               label=f"EV vs {opp_name}")
        ax.bar([i + w / 2 for i in x], wcs, width=w, color="tab:red", label="worst-case")
        ax.axhline(result["game_value"], color="black", ls="--", lw=1,
                   label=_minus(f"Nash floor {result['game_value']:+.3f}"))
        ax.set_xticks(list(x))
        ax.set_xticklabels([TICK_DISPLAY.get(m, m) for m in methods], rotation=30,
                           ha="right", fontsize=FS)
        ax.set_ylabel("value", fontsize=FS)
        ax.tick_params(axis="y", labelsize=FS)
        ax.legend(fontsize=FS)
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, f"{prefix}methods_{game_name}.png"), dpi=DPI)
        plt.close(fig)

        # teaching-attack cumulative curves (the seed-0 run)
        ta = result.get("teaching_attack")
        if ta:
            fig2, ax2 = plt.subplots(figsize=(7, 4.2))
            total = ta.get("total")
            for method, blk in ta["methods"].items():
                curve = blk.get("cumulative_seed0")
                if curve:
                    # the curve is downsampled: map its index back to the hand number
                    xs = [i * total / len(curve) for i in range(len(curve))] if total \
                        else list(range(len(curve)))
                    ax2.plot(xs, curve, label=DISPLAY.get(method, method))
            if total:
                ax2.axvline(ta["switch_at"], color="black", ls=":", lw=1,
                            label="opponent switch")
            ax2.set_xlabel("hand", fontsize=FS)
            ax2.set_ylabel("cumulative profit", fontsize=FS)
            ax2.tick_params(labelsize=FS)
            ax2.legend(fontsize=FS)
            ax2.grid(True, alpha=0.3)
            fig2.tight_layout()
            fig2.savefig(os.path.join(out_dir, f"{prefix}teaching_{game_name}.png"), dpi=DPI)
            plt.close(fig2)


def plot_all(all_results, out_dir):
    """Convenience: if a result dict has Pareto data plot that, else the tournament view."""
    if all_results and "rnr_canonical" in next(iter(all_results.values())):
        plot_pareto(all_results, out_dir)
    else:
        plot_tournament(all_results, out_dir)


if __name__ == "__main__":
    # Plot-only: redraw the chapter figures from the saved results; nothing is recomputed.
    import json

    here = os.path.dirname(os.path.abspath(__file__))
    fig_dir = os.path.normpath(os.path.join(here, "..", "..", "..", "deliverables",
                                            "reports", "step08", "figures"))
    with open(os.path.join(here, "results", "kuhn_scale.json"), encoding="utf-8") as fh:
        kuhn = json.load(fh)
    with open(os.path.join(here, "results", "pareto_kuhn.json"), encoding="utf-8") as fh:
        pareto = json.load(fh)
    plot_tournament({"kuhn": kuhn}, fig_dir, prefix="impl_")
    plot_pareto({"kuhn": pareto}, fig_dir, prefix="impl_")
    print("wrote impl_methods_kuhn / impl_teaching_kuhn / impl_pareto_kuhn to", fig_dir)
