"""
plotting.py  [INF]  -- figures for the run session.

All plotting is GUARDED: if matplotlib is not installed, `plots_available()` is False and every
function no-ops with a message instead of crashing. Three figures support the step's story:

  1. return-conditioning curve : exploitability vs target return-to-go (incl. the impossible/OOD
     point) -- shows return conditioning working, then breaking out of distribution.
  2. bet-prob by card          : root P(bet) per card under high vs low conditioning -- the
     Paster luck-vs-skill signature.
  3. exploitability bars       : the comparison-table headline, one bar per agent.

Saves PNGs under `results/`. NOTE (per WORKFLOW.md): written but NOT executed here.
"""

from __future__ import annotations

import os


def plots_available() -> bool:
    try:
        import matplotlib  # noqa: F401
        return True
    except Exception:
        return False


def _results_dir() -> str:
    d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    os.makedirs(d, exist_ok=True)
    return d


def plot_return_conditioning(rc: dict, path: str | None = None) -> str | None:
    """rc: {target_return: {"exploitability_chips": ...}} from train_dt.return_conditioning..."""
    if not plots_available():
        print("matplotlib unavailable; skipping return-conditioning plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = sorted(rc.keys())
    ys = [rc[x]["exploitability_chips"] for x in xs]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(xs, ys, marker="o")
    ax.set_xlabel("target return-to-go (chips)")
    ax.set_ylabel("exploitability (chips)")
    ax.set_title("DT: exploitability vs return conditioning")
    ax.grid(True, alpha=0.3)
    path = path or os.path.join(_results_dir(), "return_conditioning.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_bet_prob_by_card(ls: dict, path: str | None = None) -> str | None:
    """ls: {card: {"p_bet_high":..,"p_bet_low":..}} from train_dt.luck_vs_skill_experiment."""
    if not plots_available():
        print("matplotlib unavailable; skipping bet-prob-by-card plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cards = sorted(ls.keys())
    labels = {1: "J", 2: "Q", 3: "K"}
    high = [ls[c]["p_bet_high"] for c in cards]
    low = [ls[c]["p_bet_low"] for c in cards]
    x = range(len(cards))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar([i - 0.2 for i in x], high, width=0.4, label="high return")
    ax.bar([i + 0.2 for i in x], low, width=0.4, label="low return")
    ax.set_xticks(list(x))
    ax.set_xticklabels([labels.get(c, str(c)) for c in cards])
    ax.set_ylabel("root P(bet)")
    ax.set_title("Luck vs skill: bet frequency by card")
    ax.legend()
    path = path or os.path.join(_results_dir(), "bet_prob_by_card.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_exploitability_bars(rows: list, path: str | None = None) -> str | None:
    """rows: comparison_table row dicts (each with 'agent' + 'exploitability_chips')."""
    if not plots_available():
        print("matplotlib unavailable; skipping exploitability-bars plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    names = [r["agent"] for r in rows]
    vals = [r["exploitability_chips"] for r in rows]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(range(len(names)), vals)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.set_ylabel("exploitability (chips)")
    ax.set_title("Exploitability by method (lower = closer to Nash)")
    ax.grid(True, axis="y", alpha=0.3)
    path = path or os.path.join(_results_dir(), "exploitability_bars.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_tau_sweep(sweep: dict, path: str | None = None) -> str | None:
    """sweep: the dict written by tau_sweep.py -> results/tau_sweep_<profile>.json."""
    if not plots_available():
        print("matplotlib unavailable; skipping tau-sweep plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    taus = sorted(float(t) for t in sweep["taus"])
    cells = sweep["taus"]
    expl = [cells[_key(cells, t)]["exploitability"]["mean"] for t in taus]
    err = [cells[_key(cells, t)]["exploitability"]["se"] for t in taus]
    tgt = [cells[_key(cells, t)]["robust_target"]["mean"] for t in taus]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.errorbar(taus, expl, yerr=err, marker="o", capsize=4, label="ARDT exploitability")
    ax.axhline(sweep["dt_baseline"]["mean"], ls="--", color="tab:red",
               label=f"vanilla DT ({sweep['dt_baseline']['mean']:.3f})")
    ax.axhline(sweep["nash_reference"]["mean"], ls=":", color="tab:green",
               label=f"Nash ({sweep['nash_reference']['mean']:.3f})")
    ax.set_xscale("log")
    ax.set_xlabel("expectile tau  (low = pessimistic / minimax side, per ARDT Eq. 7)")
    ax.set_ylabel("exploitability (chips)")
    ax.set_title("ARDT: exploitability vs expectile tau")
    ax.grid(True, alpha=0.3)
    ax2 = ax.twinx()
    ax2.plot(taus, tgt, marker="s", color="tab:purple", alpha=0.5,
             label="mean relabel target")
    ax2.set_ylabel("mean relabel target (chips)", color="tab:purple")
    lines, labels = ax.get_legend_handles_labels()
    l2, lb2 = ax2.get_legend_handles_labels()
    ax.legend(lines + l2, labels + lb2, fontsize=8, loc="best")
    path = path or os.path.join(_results_dir(), "tau_sweep.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def _key(cells: dict, t: float) -> str:
    """Match a float tau back to its JSON string key."""
    for k in cells:
        if abs(float(k) - t) < 1e-12:
            return k
    raise KeyError(t)


def _load(name: str):
    import json
    p = os.path.join(_results_dir(), name)
    if not os.path.isfile(p):
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def main():
    """Draw every figure from MEASURED results on disk.

    RUN-SESSION REWRITE (2026-07-25). This module previously had only a `_selftest()` that
    plotted HARD-CODED numbers ({"DT": 0.20, "ARDT": 0.05}) into results/. That was the only
    PNG-producing code path in the whole step, so following the runbook would have committed a
    FABRICATED figure -- a direct WORKFLOW section 0 violation. The self-test is gone; figures
    now come only from results/*.json written by real runs.
    """
    import argparse

    ap = argparse.ArgumentParser(description="Render Step 12 figures from measured results.")
    ap.add_argument("--profile", default=os.environ.get("STEP12_PROFILE", "SMOKE").upper())
    args = ap.parse_args()
    prof = args.profile

    print(f"plotting: profile={prof}  matplotlib={plots_available()}")
    wrote, missing = [], []

    dt_exp = _load(f"dt_experiments_{prof}.json")
    if dt_exp:
        rc = {float(k): v for k, v in dt_exp["return_conditioning"].items()}
        ls = {int(k): v for k, v in dt_exp["luck_vs_skill"].items()}
        wrote += [p for p in (plot_return_conditioning(rc), plot_bet_prob_by_card(ls)) if p]
    else:
        missing.append(f"dt_experiments_{prof}.json  (run: python train_dt.py)")

    # Results are tagged by LLM backend (comparison_<profile>_<llm>.json); render one bar chart
    # per backend so the stub and each real model keep their own figure.
    import glob
    comps = sorted(glob.glob(os.path.join(_results_dir(), f"comparison_{prof}_*.json")))
    if comps:
        import json
        for cpath in comps:
            with open(cpath, encoding="utf-8") as f:
                comp = json.load(f)
            tag = comp.get("llm", "unknown")
            p = plot_exploitability_bars(
                comp["rows"], os.path.join(_results_dir(), f"exploitability_bars_{tag}.png"))
            if p:
                wrote.append(p)
    else:
        missing.append(f"comparison_{prof}_*.json  (run: python comparison_table.py)")

    sweep = _load(f"tau_sweep_{prof}.json")
    if sweep:
        p = plot_tau_sweep(sweep)
        if p:
            wrote.append(p)
    else:
        missing.append(f"tau_sweep_{prof}.json  (run: python tau_sweep.py)")

    for p in wrote:
        print(f"  wrote {os.path.basename(p)}")
    for m in missing:
        print(f"  SKIP  missing {m}")
    print(f"{len(wrote)} figure(s) written to {_results_dir()}")


if __name__ == "__main__":
    main()
