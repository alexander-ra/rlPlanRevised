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


def plot_leak_decomposition(dec: dict, path: str | None = None) -> str | None:
    """dec: results/decomposition_<model>_<style>_<method>.json (experiment A2).

    The headline point: deviation magnitude and COST are nearly uncorrelated. Plots each info set's
    share of total exploitability next to how far it deviates from Nash, so the King node (huge
    deviation, ~0 cost) and the `2p` Queen node (large cost) sit side by side.
    """
    if not plots_available():
        print("matplotlib unavailable; skipping leak-decomposition plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    base = dec["baseline_exploitability_chips"]
    rows = dec["info_sets"]
    order = sorted(rows, key=lambda i: rows[i]["delta_nash"], reverse=True)
    share = [100.0 * rows[i]["delta_nash"] / base for i in order]
    dev = [rows[i]["deviation"] for i in order]
    y = range(len(order))

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 5), sharey=True)
    ax.barh(list(y), share, color="tab:red", alpha=0.85)
    ax.set_yticks(list(y))
    ax.set_yticklabels(order, fontfamily="monospace")
    ax.invert_yaxis()
    ax.set_xlabel("share of total exploitability (%)")
    ax.set_title(f"Where the loss is  (total {base:.3f} chips)")
    ax.grid(True, axis="x", alpha=0.3)
    ax2.barh(list(y), dev, color="tab:blue", alpha=0.85)
    ax2.set_xlabel("|P(bet) - Nash|")
    ax2.set_title("How far from Nash")
    ax2.grid(True, axis="x", alpha=0.3)
    fig.suptitle(f"{dec.get('model', '?')} — deviation size does not predict cost", fontsize=11)
    path = path or os.path.join(_results_dir(), "leak_decomposition.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_stated_vs_executed(freqs: list, path: str | None = None) -> str | None:
    """freqs: list of results/frequency_elicitation_<model>.json dicts (experiment B4).

    Left: stated vs executed vs Nash per info set. Right: exploitability of each model's PLAYED
    strategy against the strategy built from its own STATED frequencies.
    """
    if not plots_available():
        print("matplotlib unavailable; skipping stated-vs-executed plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    # Two rows rather than one wide strip: at page width a 3-panel row shrinks to ~2 inches tall
    # and the axis labels become unreadable in the built PDF.
    fig = plt.figure(figsize=(11, 8))
    gs = fig.add_gridspec(2, len(freqs), height_ratios=[1.15, 1.0], hspace=0.45, wspace=0.25)
    axes = [fig.add_subplot(gs[0, i]) for i in range(len(freqs))]
    axes.append(fig.add_subplot(gs[1, :]))
    isets = list(freqs[0]["nash"].keys())
    x = range(len(isets))
    for ax, d in zip(axes, freqs):
        ax.plot(list(x), [d["nash"][i] for i in isets], "k--o", ms=4, label="Nash", lw=1.4)
        ax.plot(list(x), [d["executed"][i] for i in isets], "-s", ms=4,
                color="tab:green", label="executed (played)")
        ax.plot(list(x), [(d["stated"][i] if d["stated"][i] is not None else float("nan"))
                          for i in isets], "-^", ms=4, color="tab:orange", label="stated (asked)")
        ax.set_xticks(list(x))
        ax.set_xticklabels(isets, rotation=60, ha="right", fontfamily="monospace", fontsize=8)
        ax.set_ylabel("P(bet)")
        ax.set_ylim(-0.05, 1.05)
        ax.set_title(f"{d['model']}\nMAE stated {d['mae_stated_vs_nash']:.2f} vs "
                     f"executed {d['mae_executed_vs_nash']:.2f}", fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)

    ax = axes[-1]
    labels, played, stated = [], [], []
    for d in freqs:
        labels.append(d["model"].split("/")[-1][:14])
        played.append(d["exploitability_chips"]["executed"])
        stated.append(d["exploitability_chips"]["stated_if_played"])
    xs = range(len(labels))
    ax.bar([i - 0.2 for i in xs], played, width=0.4, color="tab:green", label="as played")
    ax.bar([i + 0.2 for i in xs], stated, width=0.4, color="tab:orange", label="if it played what it says")
    ax.axhline(freqs[0]["exploitability_chips"]["nash"], ls=":", color="k", label="Nash")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel("exploitability (chips)")
    ax.set_title("Playing what they SAY would be far worse than what they DO", fontsize=10)
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(fontsize=9)
    for i, (pv, sv) in enumerate(zip(played, stated)):
        ax.text(i - 0.2, pv, f" {pv:.3f}", ha="center", va="bottom", fontsize=8)
        ax.text(i + 0.2, sv, f" {sv:.3f}", ha="center", va="bottom", fontsize=8)

    path = path or os.path.join(_results_dir(), "stated_vs_executed.png")
    fig.savefig(path, dpi=130, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_exploitation_frontier(expl: dict, path: str | None = None) -> str | None:
    """expl: results/exploitation_<model>.json (experiment B6) -- the safe-exploitation trade-off."""
    if not plots_available():
        print("matplotlib unavailable; skipping exploitation-frontier plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rows = expl["rows"]
    names = list(rows)
    opps = list(rows[names[0]]["vs"])
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))

    for n in names:
        ax.scatter(rows[n]["exploitability_chips"], rows[n]["mean_chips_per_hand_vs_zoo"],
                   s=90, label=n)
        ax.annotate(n, (rows[n]["exploitability_chips"],
                        rows[n]["mean_chips_per_hand_vs_zoo"]),
                    textcoords="offset points", xytext=(8, 4), fontsize=8)
    ax.set_xlabel("exploitability (chips) — lower is safer")
    ax.set_ylabel("mean chips/hand vs the zoo — higher exploits more")
    ax.set_title("Exploitation vs exploitability")
    ax.grid(True, alpha=0.3)

    w = 0.38
    xs = range(len(opps))
    for k, n in enumerate(names):
        vals = [rows[n]["vs"][o]["mean_chips_per_hand"] for o in opps]
        ax2.bar([i + (k - 0.5) * w for i in xs], vals, width=w, label=n)
    ax2.axhline(0, color="k", lw=0.8)
    ax2.set_xticks(list(xs))
    ax2.set_xticklabels(opps, rotation=25, ha="right", fontsize=8)
    ax2.set_ylabel("chips/hand won")
    ax2.set_title("Per-opponent: the gain is only vs passive/random")
    ax2.grid(True, axis="y", alpha=0.3)
    ax2.legend(fontsize=8)

    path = path or os.path.join(_results_dir(), "exploitation_frontier.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_leduc_illegal_taxonomy(tax: dict, path: str | None = None) -> str | None:
    """tax: results/leduc_illegal_taxonomy_<model>.json -- one misconception, not confusion."""
    if not plots_available():
        print("matplotlib unavailable; skipping Leduc illegal-taxonomy plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    cats = tax["categories"]
    cnames = list(cats)
    sits = sorted(tax["by_situation"], key=lambda s: tax["by_situation"][s]["mean_illegal_mass"])
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    ax.bar(cnames, [cats[c]["mean_mass_all"] for c in cnames],
           color=["tab:red", "tab:blue", "tab:grey"])
    ax.set_ylabel("mean probability mass")
    ax.set_title(f"Illegal-action intent by category\n(total {tax['mean_illegal_mass']:.3f} over "
                 f"{tax['info_sets']} info sets)", fontsize=9)
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(True, axis="y", alpha=0.3)

    ax2.barh(sits, [tax["by_situation"][s]["mean_illegal_mass"] for s in sits], color="tab:red")
    ax2.set_xlabel("mean illegal mass")
    ax2.set_title("Localised: only round 2 with nothing due", fontsize=9)
    ax2.grid(True, axis="x", alpha=0.3)
    for i, s in enumerate(sits):
        ax2.text(tax["by_situation"][s]["mean_illegal_mass"], i,
                 f"  n={tax['by_situation'][s]['n']}", va="center", fontsize=8)

    path = path or os.path.join(_results_dir(), "leduc_illegal_taxonomy.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def plot_leduc_return_conditioning(st0: dict, path: str | None = None) -> str | None:
    """st0: results/leduc_stage0.json -- return conditioning does not steer on Leduc either."""
    if not plots_available():
        print("matplotlib unavailable; skipping Leduc return-conditioning plot.")
        return None
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    tg = st0["targets"]
    xs = sorted(float(k) for k in tg)
    ys = [tg[_tkey(tg, x)]["chips_per_hand"] for x in xs]
    es = [tg[_tkey(tg, x)]["se"] for x in xs]
    shares = [tg[_tkey(tg, x)]["data_share"] for x in xs]
    modal = float(st0["modal_return"])

    fig, ax = plt.subplots(figsize=(8, 4.6))
    ax.errorbar(xs, ys, yerr=es, marker="o", capsize=3, lw=1.4, color="tab:blue",
                label="DT vs near-Nash")
    ax.axvline(modal, ls="--", color="tab:red", alpha=0.7,
               label=f"modal return ({modal:+.0f}, {max(shares):.0%} of steps)")
    ood = [x for x in xs if tg[_tkey(tg, x)]["data_share"] == 0.0]
    for o in ood:
        ax.axvline(o, ls=":", color="tab:grey", label=f"impossible ({o:+.0f})")
    ax.set_xlabel("target return-to-go (chips)")
    ax.set_ylabel("chips/hand vs near-Nash")
    ax.set_title(f"Leduc: no steering (Pearson r = {st0['trend_pearson']:+.3f}), "
                 f"no notch at the modal return")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    path = path or os.path.join(_results_dir(), "leduc_return_conditioning.png")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)
    return path


def _tkey(tg: dict, x: float) -> str:
    for k in tg:
        if abs(float(k) - x) < 1e-12:
            return k
    raise KeyError(x)


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

    # --- follow-on experiments (A2 / B4 / B6) and Leduc -------------------------------
    import glob
    import json

    def _load_glob(pattern):
        out = []
        for p in sorted(glob.glob(os.path.join(_results_dir(), pattern))):
            with open(p, encoding="utf-8") as f:
                out.append(json.load(f))
        return out

    decs = _load_glob("decomposition_*.json")
    if decs:
        p = plot_leak_decomposition(decs[0])
        if p:
            wrote.append(p)
    else:
        missing.append("decomposition_*.json  (run: python exploitability_decomposition.py)")

    freqs = _load_glob("frequency_elicitation_*.json")
    if freqs:
        p = plot_stated_vs_executed(freqs)
        if p:
            wrote.append(p)
    else:
        missing.append("frequency_elicitation_*.json  (run: python frequency_elicitation.py)")

    expls = _load_glob("exploitation_*.json")
    if expls:
        p = plot_exploitation_frontier(expls[0])
        if p:
            wrote.append(p)
    else:
        missing.append("exploitation_*.json  (run: python exploitation_vs_zoo.py)")

    taxes = _load_glob("leduc_illegal_taxonomy_*.json")
    if taxes:
        p = plot_leduc_illegal_taxonomy(taxes[0])
        if p:
            wrote.append(p)
    else:
        missing.append("leduc_illegal_taxonomy_*.json  (run: python leduc_illegal_taxonomy.py)")

    st0 = _load("leduc_stage0.json")
    if st0:
        p = plot_leduc_return_conditioning(st0)
        if p:
            wrote.append(p)
    else:
        missing.append("leduc_stage0.json  (run: python leduc_stage0.py)")

    for p in wrote:
        print(f"  wrote {os.path.basename(p)}")
    for m in missing:
        print(f"  SKIP  missing {m}")
    print(f"{len(wrote)} figure(s) written to {_results_dir()}")


if __name__ == "__main__":
    main()
