"""
plotting.py -- figures for Step 08 (guarded; import fails cleanly if matplotlib is absent).

Callers do `import plotting` inside a try/except ImportError, so if matplotlib is not
installed this module simply fails to import and the JSON results are still complete.

Figures:
  - plot_pareto      : the exploitation-safety frontier (RNR canonical vs naive + method points).
  - plot_tournament  : per-method exploitation & worst-case bars + teaching-attack curves.

NOTE (per implementation/WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def plot_pareto(all_results, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for game_name, data in all_results.items():
        fig, ax = plt.subplots(figsize=(6.5, 5))
        canon = data["rnr_canonical"]
        naive = data["rnr_naive"]
        ax.plot([r["exploitation_value"] for r in canon], [r["exploitability"] for r in canon],
                "-o", color="tab:blue", label="RNR canonical")
        ax.plot([r["exploitation_value"] for r in naive], [r["exploitability"] for r in naive],
                "--s", color="tab:gray", label="naive Nash/BR blend")
        colors = {"ganzfried": "tab:green", "prime_safe": "tab:orange",
                  "adaptation": "tab:red"}
        for name, pt in data["points"].items():
            ax.scatter([pt["exploitation_value"]], [pt["exploitability"]],
                       color=colors.get(name, "black"), s=90, zorder=5, label=name, marker="*")
        ax.set_xlabel(f"exploitation profit (EV vs {data.get('exploitee', 'opponent')})")
        ax.set_ylabel("exploitability (game value - worst-case; >= 0)")
        ax.set_title(f"Exploitation-safety frontier -- {game_name}\n"
                     "(down-and-right = better; solvers should dominate the naive blend)")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
        fig.tight_layout()
        path = os.path.join(out_dir, f"pareto_{game_name}.png")
        fig.savefig(path, dpi=130)
        plt.close(fig)


def plot_tournament(all_results, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    for game_name, result in all_results.items():
        methods = result["methods"]
        table = result["table"]
        # representative opponent = the first non-Nash opponent in the table.
        opp_name = next((o for o in table if o != "Nash"), next(iter(table)))
        row = table[opp_name]
        evs = [row[m].get("exploitation_value", 0.0) for m in methods]
        wcs = [row[m].get("worst_case_value", 0.0) for m in methods]

        fig, ax = plt.subplots(figsize=(7.5, 4.5))
        x = range(len(methods))
        w = 0.38
        ax.bar([i - w / 2 for i in x], evs, width=w, color="tab:green",
               label=f"EV vs {opp_name}")
        ax.bar([i + w / 2 for i in x], wcs, width=w, color="tab:red", label="worst-case")
        ax.axhline(result["game_value"], color="black", ls="--", lw=1,
                   label=f"Nash floor {result['game_value']:+.3f}")
        ax.set_xticks(list(x))
        ax.set_xticklabels(methods, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("value")
        ax.set_title(f"Methods vs {opp_name} -- {game_name} "
                     "(worst-case below the floor = unsafe)")
        ax.legend(fontsize=8)
        ax.grid(True, axis="y", alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(out_dir, f"methods_{game_name}.png"), dpi=130)
        plt.close(fig)

        # teaching-attack cumulative curves
        ta = result.get("teaching_attack")
        if ta:
            fig2, ax2 = plt.subplots(figsize=(7.5, 4.5))
            for method, blk in ta["methods"].items():
                curve = blk.get("cumulative_seed0")
                if curve:
                    ax2.plot(curve, label=method)
            ax2.axvline(len(curve) * ta["switch_at"] / ta["total"] if ta.get("total") else 0,
                        color="black", ls=":", lw=1, label="opponent switch")
            ax2.set_xlabel("hand (downsampled)")
            ax2.set_ylabel("cumulative profit")
            ax2.set_title(f"Teaching attack -- {game_name}: {ta['bait']} -> {ta['reveal']}")
            ax2.legend(fontsize=8)
            ax2.grid(True, alpha=0.3)
            fig2.tight_layout()
            fig2.savefig(os.path.join(out_dir, f"teaching_{game_name}.png"), dpi=130)
            plt.close(fig2)


def plot_all(all_results, out_dir):
    """Convenience: if a result dict has Pareto data plot that, else the tournament view."""
    if all_results and "rnr_canonical" in next(iter(all_results.values())):
        plot_pareto(all_results, out_dir)
    else:
        plot_tournament(all_results, out_dir)
