"""
Train all four CFR variants under a common wall-clock budget each,
snapshot exploitability during training, and plot exploitability vs
iterations and exploitability vs wall-clock.

Usage:
    cd implementation/step03
    python cfr/train_all_timed.py                       # 180s per algo
    python cfr/train_all_timed.py --seconds 60          # shorter test run
    python cfr/train_all_timed.py --algos vanilla cfrplus
"""

import argparse
import json
import os
import random
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
step03_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step03_dir)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from cfr.cfrplus_trainer import LeducCFRPlusTrainer
from cfr.cfr_trainer import LeducTrainer
from cfr.leduc_poker import ALL_DEALS, NUM_CARDS, LeducState
from cfr.mccfr_external_trainer import LeducExternalSamplingTrainer
from cfr.mccfr_outcome_trainer import LeducOutcomeSamplingTrainer
from evaluate.exploitability import compute_exploitability


ALGO_ORDER = ["vanilla", "cfrplus", "external", "outcome"]

DISPLAY_NAMES = {
    "vanilla": "Vanilla CFR",
    "cfrplus": "CFR+",
    "external": "MCCFR External",
    "outcome": "MCCFR Outcome",
}

COLORS = {
    "vanilla": "#1f77b4",
    "cfrplus": "#2ca02c",
    "external": "#ff7f0e",
    "outcome": "#d62728",
}


def make_runner(algo: str):
    """Return (trainer, step_fn) pair. step_fn(iter_num) runs one iteration."""
    if algo == "vanilla":
        trainer = LeducTrainer()

        def step(iter_num: int):
            for traversing_player in (0, 1):
                regret_buffer: dict[str, list[float]] = {}
                for deal in ALL_DEALS:
                    state = LeducState((deal[0], deal[1]), deal[2])
                    trainer.cfr(state, traversing_player, 1.0,
                                regret_buffer)
                for info_set, deltas in regret_buffer.items():
                    node, _ = trainer.node_map[info_set]
                    for a in range(node.num_actions):
                        node.regret_sum[a] += deltas[a]

        return trainer, step

    if algo == "cfrplus":
        trainer = LeducCFRPlusTrainer()

        def step(iter_num: int):
            w = iter_num  # linear weight, d=0
            for traversing_player in (0, 1):
                regret_buffer: dict[str, list[float]] = {}
                for deal in ALL_DEALS:
                    state = LeducState((deal[0], deal[1]), deal[2])
                    trainer.cfr(state, traversing_player, w, 1.0,
                                regret_buffer)
                for info_set, deltas in regret_buffer.items():
                    node, _ = trainer.node_map[info_set]
                    for a in range(node.num_actions):
                        node.regret_sum[a] = max(
                            node.regret_sum[a] + deltas[a], 0.0)

        return trainer, step

    if algo == "external":
        trainer = LeducExternalSamplingTrainer()

        def step(iter_num: int):
            cards = random.sample(range(NUM_CARDS), 3)
            state = LeducState((cards[0], cards[1]), cards[2])
            update_player = (iter_num - 1) % 2
            trainer.external_cfr(state, update_player)

        return trainer, step

    if algo == "outcome":
        trainer = LeducOutcomeSamplingTrainer()

        def step(iter_num: int):
            cards = random.sample(range(NUM_CARDS), 3)
            state = LeducState((cards[0], cards[1]), cards[2])
            update_player = (iter_num - 1) % 2
            trainer.outcome_cfr(state, update_player, 1.0, 1.0, 1.0)

        return trainer, step

    raise ValueError(f"unknown algo: {algo}")


def train_timed(algo: str, budget_sec: float, snapshot_growth: float = 1.25,
                progress_every_sec: float = 5.0):
    """
    Run algo until its cumulative training time reaches budget_sec.

    Snapshot cadence grows geometrically by snapshot_growth, so we get
    fine-grained points early and log-spaced points later.

    Time spent inside compute_exploitability is excluded from the budget
    so fast algos aren't penalized for having more snapshots.

    A progress line is printed every progress_every_sec training seconds.
    """
    trainer, step_fn = make_runner(algo)
    snapshots = []
    training_time = 0.0
    iter_num = 0
    next_snap_iter = 1
    next_progress_at = progress_every_sec
    last_exploit = None
    label = DISPLAY_NAMES[algo]

    while training_time < budget_sec:
        iter_num += 1
        t0 = time.perf_counter()
        step_fn(iter_num)
        t1 = time.perf_counter()
        training_time += t1 - t0

        if iter_num >= next_snap_iter:
            exploit = compute_exploitability(trainer.node_map)
            last_exploit = exploit
            snapshots.append({
                "iter": iter_num,
                "elapsed": training_time,
                "exploit": exploit,
            })
            next_snap_iter = max(iter_num + 1,
                                 int(next_snap_iter * snapshot_growth))

        if training_time >= next_progress_at:
            pct = min(100.0, 100.0 * training_time / budget_sec)
            exploit_str = (f"{last_exploit:.4f}"
                           if last_exploit is not None else "n/a")
            print(
                f"    [{label:<16}] "
                f"train={training_time:6.1f}s/{budget_sec:.0f}s "
                f"({pct:5.1f}%)  iter={iter_num:>8,}  "
                f"exploit={exploit_str}",
                flush=True,
            )
            while next_progress_at <= training_time:
                next_progress_at += progress_every_sec

    if not snapshots or snapshots[-1]["iter"] != iter_num:
        exploit = compute_exploitability(trainer.node_map)
        snapshots.append({
            "iter": iter_num,
            "elapsed": training_time,
            "exploit": exploit,
        })

    return trainer, snapshots, iter_num, training_time


def plot_iterations_chart(results: dict, out_path: str, budget: float):
    """Exploitability vs iterations — log-log, with per-algo cutoff lines."""
    fig, ax = plt.subplots(figsize=(11, 6))

    for algo in ALGO_ORDER:
        if algo not in results:
            continue
        data = results[algo]["snapshots"]
        xs = [s["iter"] for s in data]
        ys = [s["exploit"] for s in data]
        color = COLORS[algo]
        ax.plot(xs, ys, "-", color=color, linewidth=2,
                label=f"{DISPLAY_NAMES[algo]} — final {xs[-1]:,} iters")
        ax.axvline(x=xs[-1], color=color, linestyle=":", alpha=0.55,
                   linewidth=1.2)
        ax.scatter([xs[-1]], [ys[-1]], color=color, s=50, zorder=5,
                   edgecolor="white", linewidth=1.2)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Training Iterations (log scale)")
    ax.set_ylabel("Exploitability (log scale)")
    ax.set_title(
        f"Leduc Poker — Exploitability vs Iterations "
        f"({budget:.0f}s budget per algorithm)"
    )
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="lower left", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_wallclock_chart(results: dict, out_path: str, budget: float):
    """Exploitability vs wall-clock seconds."""
    fig, ax = plt.subplots(figsize=(11, 6))

    for algo in ALGO_ORDER:
        if algo not in results:
            continue
        data = results[algo]["snapshots"]
        xs = [s["elapsed"] for s in data]
        ys = [s["exploit"] for s in data]
        color = COLORS[algo]
        ax.plot(xs, ys, "-", color=color, linewidth=2,
                label=f"{DISPLAY_NAMES[algo]} — final exploit {ys[-1]:.4f}")
        ax.scatter([xs[-1]], [ys[-1]], color=color, s=50, zorder=5,
                   edgecolor="white", linewidth=1.2)

    ax.set_yscale("log")
    ax.set_xlabel("Wall-Clock Training Time (seconds)")
    ax.set_ylabel("Exploitability (log scale)")
    ax.set_title(
        f"Leduc Poker — Exploitability vs Wall-Clock "
        f"({budget:.0f}s budget per algorithm)"
    )
    ax.grid(True, alpha=0.3, which="both")
    ax.legend(loc="upper right", framealpha=0.9)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_markdown_report(results: dict, report_path: str, budget: float,
                          iter_chart_rel: str, wall_chart_rel: str):
    lines = []
    lines.append("# Leduc Poker — Timed CFR Variant Comparison\n")
    lines.append(
        f"Each algorithm was trained for **{budget:.0f} seconds** of "
        f"wall-clock training time. Exploitability was snapshotted at "
        f"geometrically spaced iteration counts.\n"
    )
    lines.append("## Final Results\n")
    lines.append(
        "| Algorithm | Iterations | Train Time (s) | "
        "Final Exploitability | Info Sets |"
    )
    lines.append(
        "|-----------|-----------:|---------------:|"
        "---------------------:|----------:|"
    )
    for algo in ALGO_ORDER:
        if algo not in results:
            continue
        r = results[algo]
        lines.append(
            f"| {r['display_name']} | {r['total_iterations']:,} | "
            f"{r['total_training_time_sec']:.1f} | "
            f"{r['final_exploitability']:.4f} | {r['num_info_sets']} |"
        )
    lines.append("")
    lines.append("## Exploitability vs Iterations (log-log)\n")
    lines.append(f"![Iterations]({iter_chart_rel})\n")
    lines.append(
        "Dotted vertical lines mark each algorithm's final iteration count "
        "— sampling-based variants run many more iterations per second, so "
        "their curves extend farther right before the 3-minute budget is "
        "exhausted. Full-traversal variants (Vanilla CFR, CFR+) cut off "
        "much earlier on the iteration axis but move far more per step.\n"
    )
    lines.append("## Exploitability vs Wall-Clock (log-y)\n")
    lines.append(f"![Wall-Clock]({wall_chart_rel})\n")
    lines.append(
        "This view normalises the comparison to compute time. CFR+ usually "
        "dominates in wall-clock convergence thanks to regret flooring and "
        "linear strategy averaging; Vanilla CFR follows a slower O(1/√T) "
        "trajectory; sampling variants reduce per-iteration cost but "
        "require many more iterations to catch up.\n"
    )

    with open(report_path, "w") as f:
        f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="Timed comparison of Leduc Poker CFR variants"
    )
    parser.add_argument("--seconds", type=float, default=180.0,
                        help="Wall-clock training budget per algorithm (seconds)")
    parser.add_argument("--algos", nargs="+", default=None,
                        help=f"Subset of {ALGO_ORDER}")
    parser.add_argument("--seed", type=int, default=42,
                        help="RNG seed for sampling variants")
    parser.add_argument("--snapshot-growth", type=float, default=1.25,
                        help="Geometric growth factor between snapshots")
    parser.add_argument("--progress-every", type=float, default=5.0,
                        help="Print a progress line every N training seconds")
    args = parser.parse_args()

    random.seed(args.seed)
    algos = args.algos or ALGO_ORDER
    budget = args.seconds

    figures_dir = os.path.join(step03_dir, "figures")
    models_dir = os.path.join(step03_dir, "models")
    os.makedirs(figures_dir, exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)

    print()
    print(f"  Training {len(algos)}/{len(ALGO_ORDER)} CFR variants for "
          f"{budget:.0f}s each ...")
    print(f"  Running now:  {', '.join(DISPLAY_NAMES[a] for a in algos)}")
    skipped = [a for a in ALGO_ORDER if a not in algos]
    if skipped:
        print(f"  Loading prior results for:  "
              f"{', '.join(DISPLAY_NAMES[a] for a in skipped)}")
    print()

    results: dict = {}

    # Load prior per-algo snapshots for algos NOT being retrained this run.
    for algo in ALGO_ORDER:
        if algo in algos:
            continue
        prior_path = os.path.join(models_dir, f"timed_{algo}_snapshots.json")
        if not os.path.exists(prior_path):
            print(f"  [{DISPLAY_NAMES[algo]:<16}] no prior results at "
                  f"{prior_path} — skipping in plots")
            continue
        try:
            with open(prior_path) as f:
                results[algo] = json.load(f)
            print(f"  [{DISPLAY_NAMES[algo]:<16}] loaded prior results "
                  f"({results[algo]['total_iterations']:,} iters, "
                  f"final_exploit="
                  f"{results[algo]['final_exploitability']:.4f})")
        except (OSError, json.JSONDecodeError) as exc:
            print(f"  [{DISPLAY_NAMES[algo]:<16}] could not load "
                  f"{prior_path}: {exc}")

    print()

    for algo in algos:
        print(f"  [{DISPLAY_NAMES[algo]:<16}] starting ...", flush=True)
        t_wall_start = time.perf_counter()
        trainer, snapshots, iters, elapsed = train_timed(
            algo, budget,
            snapshot_growth=args.snapshot_growth,
            progress_every_sec=args.progress_every,
        )
        t_wall = time.perf_counter() - t_wall_start
        final = snapshots[-1]
        print(
            f"  [{DISPLAY_NAMES[algo]:<16}] done — "
            f"iters={iters:,}  train={elapsed:.1f}s  "
            f"total_wall={t_wall:.1f}s  "
            f"final_exploit={final['exploit']:.4f}  "
            f"snapshots={len(snapshots)}"
        )
        results[algo] = {
            "display_name": DISPLAY_NAMES[algo],
            "total_iterations": iters,
            "total_training_time_sec": elapsed,
            "total_wall_time_sec": t_wall,
            "final_exploitability": final["exploit"],
            "num_info_sets": len(trainer.node_map),
            "budget_sec": budget,
            "snapshots": snapshots,
        }
        per_algo_path = os.path.join(models_dir,
                                     f"timed_{algo}_snapshots.json")
        with open(per_algo_path, "w") as f:
            json.dump(results[algo], f, indent=2)
        print(f"  [{DISPLAY_NAMES[algo]:<16}] saved → {per_algo_path}")

    combined_path = os.path.join(models_dir, "timed_all_snapshots.json")
    with open(combined_path, "w") as f:
        json.dump({"budget_sec": budget, "results": results}, f, indent=2)

    iter_chart = os.path.join(figures_dir, "exploitability_vs_iterations.png")
    wall_chart = os.path.join(figures_dir, "exploitability_vs_wallclock.png")
    plot_iterations_chart(results, iter_chart, budget)
    plot_wallclock_chart(results, wall_chart, budget)

    report_path = os.path.join(figures_dir, "timed_report.md")
    write_markdown_report(
        results, report_path, budget,
        iter_chart_rel="exploitability_vs_iterations.png",
        wall_chart_rel="exploitability_vs_wallclock.png",
    )

    print()
    print(f"  Iter chart:   {iter_chart}")
    print(f"  Wall chart:   {wall_chart}")
    print(f"  Combined JSON: {combined_path}")
    print(f"  Report:       {report_path}")
    print()


if __name__ == "__main__":
    main()
