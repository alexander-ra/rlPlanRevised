"""
Day 1 exploration — Deep CFR on Leduc Hold'em (OpenSpiel, PyTorch).

Three sub-tasks from the Phase 2 brief:

  1. Run OpenSpiel's Deep CFR on Leduc and measure exploitability.
  2. Compare convergence against tabular MCCFR (OpenSpiel external-sampling
     MCCFR — see README for why we don't pull in step03's custom engine here).
  3. Sweep network sizes (32,32), (64,64), (128,128,128) to see how capacity
     affects convergence and final exploitability.

Outputs:
  figures/day01_deep_cfr_vs_mccfr.png   exploitability vs wall-time
  figures/day01_network_sizes.png       exploitability per Deep CFR config
  logs/day01_results.json               raw curves + metadata
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict

# Make sibling `_openspiel_patch.py` importable when run as a script.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pyspiel
import torch

from open_spiel.python import policy as policy_lib
from open_spiel.python.algorithms import (
    exploitability,
    external_sampling_mccfr as mccfr,
)
from open_spiel.python.pytorch import deep_cfr

import _openspiel_patch  # noqa: F401 — monkey-patches Deep CFR advantage-net training


HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")
LOG_DIR = os.path.join(HERE, "logs")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# Deep CFR runner
# ---------------------------------------------------------------------------

@dataclass
class DeepCFRRun:
    label: str
    layers: tuple
    checkpoints: list = field(default_factory=list)   # outer-iteration count
    exploitabilities: list = field(default_factory=list)
    wall_times: list = field(default_factory=list)    # seconds elapsed
    advantage_losses_final: dict = field(default_factory=dict)
    policy_loss_final: float = 0.0
    num_traversals: int = 0
    total_iterations: int = 0


def run_deep_cfr(
    game: pyspiel.Game,
    layers: tuple,
    total_iterations: int,
    num_traversals: int,
    checkpoint_every: int,
    seed: int,
    label: str,
) -> DeepCFRRun:
    """Train Deep CFR in chunks of `checkpoint_every` outer iterations so we
    can sample exploitability along the way without rebuilding the solver."""
    torch.manual_seed(seed)
    run = DeepCFRRun(
        label=label,
        layers=tuple(layers),
        num_traversals=num_traversals,
        total_iterations=total_iterations,
    )

    print(f"\n[Deep CFR] {label}: layers={layers}, "
          f"iters={total_iterations}, traversals/iter={num_traversals}")

    t0 = time.perf_counter()
    completed = 0
    while completed < total_iterations:
        step = min(checkpoint_every, total_iterations - completed)
        solver = deep_cfr.DeepCFRSolver(
            game,
            policy_network_layers=tuple(layers),
            advantage_network_layers=tuple(layers),
            num_iterations=completed + step,
            num_traversals=num_traversals,
            learning_rate=1e-3,
            batch_size_advantage=128,
            batch_size_strategy=1024,
            memory_capacity=int(1e6),
            seed=seed,
        )
        # We rebuild the solver and run from 0 each checkpoint. That's wasteful
        # but matches OpenSpiel's API (no public "resume" / "step N more iters"
        # method), and it gives clean, comparable training curves. For modest
        # iteration counts (<= ~50) the overhead is acceptable.
        _, adv_losses, policy_loss = solver.solve()

        avg_policy = policy_lib.tabular_policy_from_callable(
            game, solver.action_probabilities
        )
        expl = exploitability.exploitability(game, avg_policy)
        elapsed = time.perf_counter() - t0

        completed += step
        run.checkpoints.append(completed)
        run.exploitabilities.append(expl)
        run.wall_times.append(elapsed)
        def _to_float(x):
            return float(x) if x is not None else float("nan")

        run.advantage_losses_final = {
            str(p): [_to_float(x) for x in losses] for p, losses in adv_losses.items()
        }
        run.policy_loss_final = _to_float(policy_loss)

        last_adv = adv_losses[0][-1] if adv_losses[0] else None
        print(
            f"  iter={completed:>3d} | expl={expl:.4f} | "
            f"elapsed={elapsed:6.1f}s | "
            f"adv_loss[0][-1]={_to_float(last_adv):.4f} | "
            f"policy_loss={_to_float(policy_loss):.4f}"
        )

    return run


# ---------------------------------------------------------------------------
# Tabular MCCFR baseline
# ---------------------------------------------------------------------------

@dataclass
class MCCFRRun:
    label: str = "tabular_external_mccfr"
    checkpoints: list = field(default_factory=list)
    exploitabilities: list = field(default_factory=list)
    wall_times: list = field(default_factory=list)


def run_tabular_mccfr(
    game: pyspiel.Game,
    iterations: int,
    checkpoint_every: int,
    seed: int,
) -> MCCFRRun:
    print(f"\n[Tabular MCCFR] external-sampling, iters={iterations}, "
          f"checkpoint_every={checkpoint_every}")
    np.random.seed(seed)
    solver = mccfr.ExternalSamplingSolver(
        game, mccfr.AverageType.SIMPLE
    )
    run = MCCFRRun()

    t0 = time.perf_counter()
    for i in range(1, iterations + 1):
        solver.iteration()
        if i == 1 or i % checkpoint_every == 0 or i == iterations:
            avg_policy = solver.average_policy()
            expl = exploitability.exploitability(game, avg_policy)
            elapsed = time.perf_counter() - t0
            run.checkpoints.append(i)
            run.exploitabilities.append(expl)
            run.wall_times.append(elapsed)
            print(f"  iter={i:>6d} | expl={expl:.4f} | elapsed={elapsed:5.1f}s")
    return run


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_deep_cfr_vs_mccfr(deep_run: DeepCFRRun, mccfr_run: MCCFRRun, out_path: str):
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))

    # Left: vs outer-iterations (different units per algorithm — log x).
    ax[0].plot(mccfr_run.checkpoints, mccfr_run.exploitabilities,
               marker="o", ms=3, label="Tabular MCCFR (iterations)", color="C0")
    ax[0].plot(deep_run.checkpoints, deep_run.exploitabilities,
               marker="s", ms=5, label=f"Deep CFR ({deep_run.label})", color="C3")
    ax[0].set_xscale("log")
    ax[0].set_yscale("log")
    ax[0].set_xlabel("Outer iterations (log)")
    ax[0].set_ylabel("Exploitability (log)")
    ax[0].set_title("Convergence in 'iterations' (unit differs per method)")
    ax[0].grid(True, which="both", alpha=0.3)
    ax[0].legend()

    # Right: vs wall-clock seconds — the only honest cross-method axis.
    ax[1].plot(mccfr_run.wall_times, mccfr_run.exploitabilities,
               marker="o", ms=3, label="Tabular MCCFR", color="C0")
    ax[1].plot(deep_run.wall_times, deep_run.exploitabilities,
               marker="s", ms=5, label=f"Deep CFR ({deep_run.label})", color="C3")
    ax[1].set_xlabel("Wall-clock seconds")
    ax[1].set_ylabel("Exploitability (log)")
    ax[1].set_yscale("log")
    ax[1].set_title("Convergence in wall time")
    ax[1].grid(True, which="both", alpha=0.3)
    ax[1].legend()

    fig.suptitle("Leduc Hold'em: Deep CFR vs tabular external-sampling MCCFR")
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  saved {out_path}")


def plot_network_size_sweep(runs: list[DeepCFRRun], out_path: str):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, r in enumerate(runs):
        ax.plot(r.checkpoints, r.exploitabilities,
                marker="o", label=f"{r.label}  layers={r.layers}", color=f"C{i}")
    ax.set_xlabel("Deep CFR outer iterations")
    ax.set_ylabel("Exploitability (log)")
    ax.set_yscale("log")
    ax.set_title("Leduc Hold'em — Deep CFR network-size sweep")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=130)
    plt.close(fig)
    print(f"  saved {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true",
                        help="Smoke-test (tiny iteration counts).")
    parser.add_argument("--deep-cfr-iters", type=int, default=120)
    parser.add_argument("--deep-cfr-traversals", type=int, default=40)
    parser.add_argument("--deep-cfr-checkpoint-every", type=int, default=30)
    parser.add_argument("--mccfr-iters", type=int, default=50_000)
    parser.add_argument("--mccfr-checkpoint-every", type=int, default=2_500)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--skip-sweep", action="store_true",
                        help="Only run the baseline Deep CFR + MCCFR comparison.")
    args = parser.parse_args()

    if args.quick:
        args.deep_cfr_iters = 6
        args.deep_cfr_traversals = 10
        args.deep_cfr_checkpoint_every = 2
        args.mccfr_iters = 2_000
        args.mccfr_checkpoint_every = 200

    game = pyspiel.load_game("leduc_poker")
    print(f"Loaded game: {game.get_type().long_name}")
    print(f"  info_state_tensor_size = {game.information_state_tensor_size()}")
    print(f"  num_distinct_actions   = {game.num_distinct_actions()}")
    print(f"  num_players            = {game.num_players()}")

    # ---- Baseline Deep CFR (64,64) ----
    baseline_deep_cfr = run_deep_cfr(
        game,
        layers=(64, 64),
        total_iterations=args.deep_cfr_iters,
        num_traversals=args.deep_cfr_traversals,
        checkpoint_every=args.deep_cfr_checkpoint_every,
        seed=args.seed,
        label="(64,64) baseline",
    )

    # ---- Tabular MCCFR baseline ----
    mccfr_run = run_tabular_mccfr(
        game,
        iterations=args.mccfr_iters,
        checkpoint_every=args.mccfr_checkpoint_every,
        seed=args.seed,
    )

    plot_deep_cfr_vs_mccfr(
        baseline_deep_cfr, mccfr_run,
        os.path.join(FIG_DIR, "day01_deep_cfr_vs_mccfr.png"),
    )

    # ---- Network-size sweep ----
    sweep_runs = [baseline_deep_cfr]
    if not args.skip_sweep:
        for layers, label in [((32, 32), "(32,32) small"),
                              ((128, 128, 128), "(128,128,128) large")]:
            r = run_deep_cfr(
                game,
                layers=layers,
                total_iterations=args.deep_cfr_iters,
                num_traversals=args.deep_cfr_traversals,
                checkpoint_every=args.deep_cfr_checkpoint_every,
                seed=args.seed,
                label=label,
            )
            sweep_runs.append(r)
        plot_network_size_sweep(
            sweep_runs,
            os.path.join(FIG_DIR, "day01_network_sizes.png"),
        )

    # ---- Persist raw results ----
    out = {
        "args": vars(args),
        "game": game.get_type().short_name,
        "deep_cfr_runs": [asdict(r) for r in sweep_runs],
        "tabular_mccfr": asdict(mccfr_run),
    }
    def _json_default(o):
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(f"not JSON serializable: {type(o)}")

    out_path = os.path.join(LOG_DIR, "day01_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=_json_default)
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
