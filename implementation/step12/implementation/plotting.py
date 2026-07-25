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


def _selftest():
    print("plotting self-test")
    print("-" * 40)
    print(f"matplotlib available: {plots_available()}")
    if plots_available():
        p = plot_exploitability_bars([
            {"agent": "Nash-CFR", "exploitability_chips": 0.001},
            {"agent": "DT", "exploitability_chips": 0.20},
            {"agent": "ARDT", "exploitability_chips": 0.05},
        ])
        print(f"wrote demo figure -> {p}")


if __name__ == "__main__":
    _selftest()
