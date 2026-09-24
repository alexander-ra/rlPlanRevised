"""Compare custom DQN/PPO implementations against Stable-Baselines3 baselines.

Reads TensorBoard training logs from our custom implementations, then trains
equivalent SB3 agents, and generates side-by-side learning-curve plots saved
to deliverables/reports/step01/figures/.

Usage (from repo root):
    python implementation/step01/compare_sb3.py              # plot from saved results
    python implementation/step01/compare_sb3.py --train-sb3  # (re)train SB3 if no cache

Outputs:
    deliverables/reports/step01/figures/dqn_comparison.png
    deliverables/reports/step01/figures/ppo_comparison.png
    deliverables/reports/step01/figures/final_metrics.png

Plotting-only by default (September 2026 final review, F01-G02/G03):
  * SB3 is trained only with --train-sb3 and only when sb3_results_cache.json is
    missing, so a plotting run can never silently retrain or rewrite results.
  * Our own curves are read from custom_results_cache.json when it exists,
    otherwise from the TensorBoard logs of the run named in DQN_RUN / PPO_RUN
    (or the only event file present). The old "file with the most entries"
    heuristic picked the 300K-step [64,64] PPO run instead of the final one.
    The first successful read writes custom_results_cache.json (commit it, like
    the SB3 cache) so later renders do not depend on the gitignored logs.
  * The logs of the April 2026 runs were never committed and are gone. Without
    them the two learning-curve figures are NOT redrawn (the saved renders are
    left untouched), and final_metrics.png uses the best rolling-100 values
    recorded from those runs (RECORDED_CUSTOM_BEST). Re-training dqn/train.py
    and ppo/train.py (ideally with a fixed seed) restores the full pipeline.
"""

import argparse
import os
import sys
import json
import glob
import numpy as np
import matplotlib
matplotlib.use("Agg")  # headless backend — no display needed
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# ---- Path setup ----
SCRIPT_DIR  = Path(__file__).parent.resolve()
REPO_ROOT   = SCRIPT_DIR.parent.parent.resolve()
FIGURES_DIR = REPO_ROOT / "deliverables" / "reports" / "step01" / "figures"
CACHE_FILE  = SCRIPT_DIR / "sb3_results_cache.json"
DQN_LOG_DIR = SCRIPT_DIR / "logs" / "dqn"
PPO_LOG_DIR = SCRIPT_DIR / "logs" / "ppo"
CUSTOM_CACHE = SCRIPT_DIR / "custom_results_cache.json"

# Event file of the final run of each algorithm, e.g. "events.out.tfevents.<...>".
# None: use the only event file in the directory, and refuse to guess among several.
DQN_RUN: str | None = None
PPO_RUN: str | None = None

# Best rolling-100 average of our final runs, as read from their TensorBoard logs
# by this script on 3 Apr 2026 (render in commit 049b4c4; report tables). Used for
# final_metrics.png only while the per-episode curves are unavailable.
RECORDED_CUSTOM_BEST = {"dqn": 477.5, "ppo": 203.6}

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPT_DIR))
from config import DQN_CONFIG, PPO_CONFIG

# ---- Colour palette (colour-blind friendly) ----
C_OUR   = "#2196F3"   # blue  — our implementation
C_SB3   = "#FF5722"   # orange — SB3 baseline
C_SHADE = 0.25        # alpha for shaded confidence bands

# ===========================================================================
# 1. TensorBoard log reading
# ===========================================================================

def read_tb_run(log_dir: Path, tag: str,
                run_file: str | None) -> tuple[list[int], list[float]]:
    """Return (steps, values) of `tag` from one explicitly chosen run.

    `run_file` names the event file of the final run. When it is None, the
    directory must hold exactly one event file. The earlier heuristics ("most
    recent file", then "file with the most entries") each picked the wrong run
    at some point, so with several files we refuse to guess.
    """
    event_files = sorted(glob.glob(str(log_dir / "events.out.tfevents.*")))
    if not event_files:
        print(f"  No event files in {log_dir}")
        return [], []
    if run_file is None:
        if len(event_files) > 1:
            print(f"  {len(event_files)} event files in {log_dir}; set the run "
                  "constant (DQN_RUN / PPO_RUN) to the final run:")
            for ef in event_files:
                print(f"     {Path(ef).name}")
            return [], []
        path = Path(event_files[0])
    else:
        path = log_dir / run_file
        if not path.exists():
            print(f"  {path} not found")
            return [], []

    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator
    ea = EventAccumulator(str(path))
    ea.Reload()
    if tag not in ea.Tags().get("scalars", []):
        print(f"  tag '{tag}' not in {path.name}")
        return [], []
    events = ea.Scalars(tag)
    print(f"  Using: {path.name} ({len(events)} entries)")
    return [e.step for e in events], [e.value for e in events]


def load_custom_results() -> dict | None:
    """Our per-episode rewards: from the committed cache, else from the logs.

    Returns {"dqn": {"rewards": [...]}, "ppo": {"rewards": [...], "steps": [...]}}
    or None when neither source is available.
    """
    if CUSTOM_CACHE.exists():
        with open(CUSTOM_CACHE) as f:
            return json.load(f)
    _, dqn_r = read_tb_run(DQN_LOG_DIR, "reward/episode", DQN_RUN)
    ppo_s, ppo_r = read_tb_run(PPO_LOG_DIR, "reward/episode", PPO_RUN)
    if not dqn_r or not ppo_r:
        return None
    data = {"dqn": {"rewards": [float(r) for r in dqn_r]},
            "ppo": {"rewards": [float(r) for r in ppo_r],
                    "steps": [int(s) for s in ppo_s]}}
    with open(CUSTOM_CACHE, "w") as f:           # new file only; never overwritten
        json.dump(data, f)
    print(f"  Custom results cached to {CUSTOM_CACHE}")
    return data


# ===========================================================================
# 2. SB3 training with captured episode rewards
# ===========================================================================

from stable_baselines3 import DQN as SB3_DQN, PPO as SB3_PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback


class EpisodeRewardCallback(BaseCallback):
    """Records every episode reward and the step at which it occurred."""

    def __init__(self, verbose=0):
        super().__init__(verbose)
        self.episode_rewards: list[float] = []
        self.episode_steps:   list[int]   = []

    def _on_step(self) -> bool:
        for info in self.locals.get("infos", []):
            if "episode" in info:
                self.episode_rewards.append(float(info["episode"]["r"]))
                self.episode_steps.append(self.num_timesteps)
        return True


def train_sb3_dqn(total_timesteps: int = 100_000, seed: int = 42) -> dict:
    """Train SB3 DQN on CartPole-v1 using RL Zoo tuned hyperparameters.

    The official RL Baselines3 Zoo provides tuned hyperparameters for
    CartPole-v1 that solve the environment in ~50K steps.  We use these
    rather than SB3 generic defaults (which are Atari-oriented and perform
    poorly on classic control tasks).

    Source: https://github.com/DLR-RM/rl-baselines3-zoo/blob/master/hyperparams/dqn.yml
    Budget: 100K steps (2× the Zoo's 50K) to give SB3 comfortable headroom.
    """
    import gymnasium as gym
    env = Monitor(gym.make("CartPole-v1"))
    cb  = EpisodeRewardCallback()

    model = SB3_DQN(
        "MlpPolicy", env,
        # RL Zoo tuned hyperparameters for CartPole-v1
        learning_rate        = 2.3e-3,
        batch_size           = 64,
        buffer_size          = 100_000,
        learning_starts      = 1000,
        gamma                = 0.99,
        target_update_interval = 10,
        train_freq           = 256,
        gradient_steps       = 128,
        exploration_fraction = 0.16,
        exploration_final_eps = 0.04,
        policy_kwargs        = dict(net_arch=[256, 256]),
        seed                 = seed,
        verbose              = 0,
    )
    model.learn(total_timesteps=total_timesteps, callback=cb)
    env.close()
    return {"rewards": cb.episode_rewards, "steps": cb.episode_steps}


def train_sb3_ppo(total_timesteps: int = 500_000, seed: int = 42) -> dict:
    """Train SB3 PPO on LunarLander-v3 with hyperparameters matching our custom impl.

    Budget matched to PPO_CONFIG["total_timesteps"] = 500_000 so both agents
    receive the same number of environment steps.
    """
    import gymnasium as gym
    env = Monitor(gym.make("LunarLander-v3"))
    cb  = EpisodeRewardCallback()

    model = SB3_PPO(
        "MlpPolicy", env,
        learning_rate = PPO_CONFIG["learning_rate"],
        n_steps       = PPO_CONFIG["n_steps"],
        batch_size    = PPO_CONFIG["batch_size"],
        n_epochs      = PPO_CONFIG["n_epochs"],
        gamma         = PPO_CONFIG["gamma"],
        gae_lambda    = PPO_CONFIG["gae_lambda"],
        clip_range    = PPO_CONFIG["clip_range"],
        ent_coef      = PPO_CONFIG["entropy_coef"],
        vf_coef       = PPO_CONFIG["value_loss_coef"],
        max_grad_norm = PPO_CONFIG["max_grad_norm"],
        policy_kwargs = dict(net_arch=dict(pi=PPO_CONFIG["hidden_sizes"],
                                           vf=PPO_CONFIG["hidden_sizes"])),
        seed          = seed,
        verbose       = 0,
    )
    model.learn(total_timesteps=total_timesteps, callback=cb)
    env.close()
    return {"rewards": cb.episode_rewards, "steps": cb.episode_steps}


# ===========================================================================
# 3. Smoothing helpers
# ===========================================================================

def rolling_avg(values: list[float], window: int = 50) -> np.ndarray:
    """Compute rolling average with the given window."""
    v = np.array(values, dtype=float)
    if len(v) < window:
        return v
    kernel = np.ones(window) / window
    # 'valid' mode: output shorter by (window-1) on each side
    return np.convolve(v, kernel, mode="valid")


def rolling_std(values: list[float], window: int = 50) -> np.ndarray:
    """Compute rolling std with the given window (for shaded bands)."""
    v = np.array(values, dtype=float)
    result = []
    for i in range(len(v) - window + 1):
        result.append(np.std(v[i : i + window]))
    return np.array(result)


def x_axis_for_rolling(values: list, window: int) -> np.ndarray:
    """Return episode indices aligned with rolling_avg output (centred)."""
    n = len(values)
    # 'valid' mode starts at index (window//2) of the original
    start = window // 2
    return np.arange(start, start + n - window + 1)


# ===========================================================================
# 4. Plotting
# ===========================================================================

def figure_style():
    """Apply a clean, publication-ready matplotlib style."""
    plt.rcParams.update({
        # sizes for figures ~7 in wide, printed at ~17.6 cm: >= 10 pt on paper
        "font.family":        "sans-serif",
        "font.size":          10.5,
        "axes.titlesize":     11,
        "axes.labelsize":     10.5,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.grid":          True,
        "grid.alpha":         0.35,
        "grid.linestyle":     "--",
        "legend.framealpha":  0.9,
        "lines.linewidth":    1.8,
    })


def plot_rolling_comparison(
    our_rewards:  list[float],
    sb3_rewards:  list[float],
    target: float,
    algo: str,
    out_name: str,
    window: int = 100,
):
    """One panel: 100-episode rolling average, ours vs SB3, on the episode index.

    The raw-reward panel of the earlier two-panel version was dropped (the text
    never refers to it), so the figure is ~7 in wide and prints near full size.
    No suptitle and no footnote: the caption carries the title, and the episode
    and step counts are in the text. Both curves share the episode index; SB3 is
    clipped to our stopping point plus a small margin, because its episodes are
    far more numerous when it fails early (short CartPole episodes).
    """
    figure_style()
    fig, ax = plt.subplots(figsize=(7.0, 3.4))

    our_n   = len(our_rewards)
    x_limit = our_n + max(window // 2, 30)
    sb3_clipped = sb3_rewards[:x_limit]

    for rewards, colour, label in ((our_rewards, C_OUR, f"Custom {algo}"),
                                   (sb3_clipped, C_SB3, f"SB3 {algo}")):
        if len(rewards) >= window:
            avg = rolling_avg(rewards, window)
            std = rolling_std(rewards, window)
            x   = x_axis_for_rolling(rewards, window)
            ax.plot(x, avg, color=colour, label=label)
            ax.fill_between(x, avg - std, avg + std, color=colour, alpha=C_SHADE)

    ax.axhline(target, color="k", linewidth=1.2, linestyle=":",
               label=f"Target ({target:.0f})")
    ax.axvline(our_n - 1, color=C_OUR, linewidth=1.5, linestyle="--", alpha=0.7,
               label="Custom stopped")
    ax.set_xlabel("Episode")
    ax.set_ylabel(f"Rolling Avg Reward ({window} ep)")
    ax.set_xlim(0, x_limit)
    ax.legend(loc="best")

    plt.tight_layout()
    out = FIGURES_DIR / out_name
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")


def plot_dqn_comparison(our_episodes: list[float], sb3_episodes: list[float],
                        target: float, window: int = 100):
    plot_rolling_comparison(our_episodes, sb3_episodes, target, "DQN",
                            "dqn_comparison.png", window)


def plot_ppo_comparison(our_rewards: list[float], sb3_rewards: list[float],
                        target: float, window: int = 100):
    # was window=50, while the text reasons in rolling-100 terms (F01-G03)
    plot_rolling_comparison(our_rewards, sb3_rewards, target, "PPO",
                            "ppo_comparison.png", window)


def plot_dqn_iterations(iteration_data: list[dict]):
    """Plot the successive DQN tuning runs as separate curves."""
    figure_style()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("DQN Hyperparameter Iteration History (CartPole-v1)", fontsize=13)

    colours = plt.cm.Blues(np.linspace(0.3, 0.9, len(iteration_data)))
    for i, run in enumerate(iteration_data):
        eps = run["episodes"]
        avgs = rolling_avg(eps, window=100)
        x    = x_axis_for_rolling(eps, window=100)
        ax.plot(x, avgs, color=colours[i], label=run["label"], linewidth=1.8)

    ax.axhline(DQN_CONFIG["reward_target"], color="k", linewidth=1.2, linestyle=":",
               label=f"Target ({DQN_CONFIG['reward_target']:.0f})")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Rolling Avg Reward (100 eps)")
    ax.legend(fontsize=9)
    plt.tight_layout()
    out = FIGURES_DIR / "dqn_iterations.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")


def _best_rolling(rewards: list[float], window: int = 100) -> float:
    """Return the best rolling-window average over the full training curve.

    This is fair regardless of early stopping: it measures peak capability,
    not where training happened to end.
    """
    arr = np.array(rewards, dtype=float)
    if len(arr) < window:
        return float(np.mean(arr))
    avgs = np.convolve(arr, np.ones(window) / window, mode="valid")
    return float(np.max(avgs))


def plot_final_metrics(best: dict):
    """Bar chart of best rolling-100 averages (fair with early stopping).

    `best` = {"dqn": (ours, sb3), "ppo": (ours, sb3)}. No suptitle: the caption
    carries it. Bar values are drawn as text, so the BG render maps "477.5" to
    "477,5" through the label mapping.
    """
    figure_style()
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4))

    panels = (("dqn", "CartPole-v1", "DQN", DQN_CONFIG["reward_target"], 570),
              ("ppo", "LunarLander-v3", "PPO", PPO_CONFIG["reward_target"], 265))
    for ax, (key, env, algo, target, ymax) in zip(axes, panels):
        ours, sb3 = best[key]
        bars = ax.bar([0, 1], [ours, sb3], color=[C_OUR, C_SB3], width=0.5,
                      edgecolor="white")
        ax.set_xticks([0, 1])
        ax.set_xticklabels([f"Custom {algo}", f"SB3 {algo}"])
        ax.axhline(target, color="k", linewidth=1.2, linestyle=":",
                   label=f"Target ({target:.0f})")
        ax.set_title(env)
        ax.set_ylim(0, ymax)
        for bar, val in zip(bars, [ours, sb3]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + ymax * 0.015,
                    f"{val:.1f}", ha="center", va="bottom", fontweight="bold")
        ax.legend(loc="upper right")      # above the target line
    axes[0].set_ylabel("Best rolling-100 avg reward")

    plt.tight_layout()
    out = FIGURES_DIR / "final_metrics.png"
    plt.savefig(out, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")


# ===========================================================================
# 5. Cache (avoid re-running SB3 training every time)
# ===========================================================================

def load_cache() -> dict | None:
    if CACHE_FILE.exists():
        with open(CACHE_FILE) as f:
            return json.load(f)
    return None


def save_cache(data: dict):
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)
    print(f"  SB3 results cached to {CACHE_FILE}")


# ===========================================================================
# 6. Main
# ===========================================================================

def main() -> int:
    ap = argparse.ArgumentParser(description="Plot custom DQN/PPO vs SB3.")
    ap.add_argument("--train-sb3", action="store_true",
                    help="train SB3 when sb3_results_cache.json is missing "
                         "(never overwrites an existing cache)")
    args = ap.parse_args()

    print("=" * 60)
    print("Step 01 — Comparison: Custom implementations vs SB3")
    print("=" * 60)

    # ---- SB3 results: the committed cache (training only on request) ----
    cache = load_cache()
    if cache:
        print("\n[Using cached SB3 results — sb3_results_cache.json]")
        sb3_dqn = cache["sb3_dqn"]
        sb3_ppo = cache["sb3_ppo"]
    elif args.train_sb3:
        print("\n[Training SB3 DQN on CartPole-v1 ...]")
        sb3_dqn = train_sb3_dqn()   # function default: 100K steps, RL Zoo settings
        print(f"  Episodes captured: {len(sb3_dqn['rewards'])}")

        print("\n[Training SB3 PPO on LunarLander-v3 ...]")
        sb3_ppo = train_sb3_ppo()   # function default: 500K steps
        print(f"  Episodes captured: {len(sb3_ppo['rewards'])}")

        save_cache({"sb3_dqn": sb3_dqn, "sb3_ppo": sb3_ppo})
    else:
        print("\nNo sb3_results_cache.json. Plotting only; pass --train-sb3 to train.")
        return 1

    # ---- Our per-episode curves ----
    print("\n[Reading custom results ...]")
    custom = load_custom_results()

    print("\n[Generating figures ...]")
    if custom:
        plot_dqn_comparison(custom["dqn"]["rewards"], sb3_dqn["rewards"],
                            DQN_CONFIG["reward_target"])
        plot_ppo_comparison(custom["ppo"]["rewards"], sb3_ppo["rewards"],
                            PPO_CONFIG["reward_target"])
        ours = {"dqn": _best_rolling(custom["dqn"]["rewards"]),
                "ppo": _best_rolling(custom["ppo"]["rewards"])}
    else:
        print("  Custom learning curves unavailable (logs not kept):")
        print("  dqn_comparison.png / ppo_comparison.png left as saved.")
        print(f"  final_metrics.png uses the recorded values {RECORDED_CUSTOM_BEST}.")
        ours = RECORDED_CUSTOM_BEST

    plot_final_metrics({
        "dqn": (ours["dqn"], _best_rolling(sb3_dqn["rewards"])),
        "ppo": (ours["ppo"], _best_rolling(sb3_ppo["rewards"])),
    })

    print(f"\nFigures in: {FIGURES_DIR}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
