"""Compare custom DQN/PPO implementations against Stable-Baselines3 baselines.

Reads TensorBoard training logs from our custom implementations, then trains
equivalent SB3 agents, and generates side-by-side learning-curve plots saved
to deliverables/reports/step01/figures/.

Usage (from repo root):
    python implementation/step01/compare_sb3.py

Outputs:
    deliverables/reports/step01/figures/dqn_comparison.png
    deliverables/reports/step01/figures/ppo_comparison.png
    deliverables/reports/step01/figures/dqn_smoothed.png
    deliverables/reports/step01/figures/ppo_smoothed.png
"""

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

def read_last_tb_run(log_dir: Path, tag: str) -> tuple[list[int], list[float]]:
    """Return (steps, values) from the most recent TBEvent file in log_dir.

    Why the most recent file?  Each training run appends a new event file.
    We only want the final, successful run — not the aggregation of all runs.
    """
    from tensorboard.backend.event_processing.event_accumulator import EventAccumulator

    event_files = sorted(glob.glob(str(log_dir / "events.out.tfevents.*")))
    if not event_files:
        print(f"  WARNING: No event files in {log_dir}")
        return [], []

    last_file = event_files[-1]
    ea = EventAccumulator(last_file)
    ea.Reload()

    available = ea.Tags().get("scalars", [])
    if tag not in available:
        print(f"  WARNING: tag '{tag}' not in {last_file}. Available: {available}")
        return [], []

    events = ea.Scalars(tag)
    steps  = [e.step  for e in events]
    values = [e.value for e in events]
    return steps, values


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


def train_sb3_dqn(total_timesteps: int = 350_000, seed: int = 42) -> dict:
    """Train SB3 DQN on CartPole-v1 with hyperparameters matching our custom impl.

    Hyperparameter mapping:
      Our epsilon_decay=0.995/episode ≈ SB3 exploration_fraction (steps-based).
      In our final run epsilon reached 0.001 by ~episode 1380, which at ~200
      avg steps/episode corresponds to ≈270K steps → fraction ≈ 0.77 of 350K.
    """
    import gymnasium as gym
    env = Monitor(gym.make("CartPole-v1"))
    cb  = EpisodeRewardCallback()

    model = SB3_DQN(
        "MlpPolicy", env,
        learning_rate      = DQN_CONFIG["learning_rate"],
        buffer_size        = DQN_CONFIG["buffer_size"],
        batch_size         = DQN_CONFIG["batch_size"],
        gamma              = DQN_CONFIG["gamma"],
        exploration_fraction     = 0.77,
        exploration_initial_eps  = DQN_CONFIG["epsilon_start"],
        exploration_final_eps    = DQN_CONFIG["epsilon_end"],
        target_update_interval   = 1000,
        policy_kwargs      = dict(net_arch=DQN_CONFIG["hidden_sizes"]),
        seed               = seed,
        verbose            = 0,
    )
    model.learn(total_timesteps=total_timesteps, callback=cb)
    env.close()
    return {"rewards": cb.episode_rewards, "steps": cb.episode_steps}


def train_sb3_ppo(total_timesteps: int = 264_192, seed: int = 42) -> dict:
    """Train SB3 PPO on LunarLander-v3 with hyperparameters matching our custom impl."""
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
        "font.family":        "sans-serif",
        "font.size":          11,
        "axes.titlesize":     13,
        "axes.labelsize":     11,
        "axes.spines.top":    False,
        "axes.spines.right":  False,
        "axes.grid":          True,
        "grid.alpha":         0.35,
        "grid.linestyle":     "--",
        "legend.framealpha":  0.9,
        "lines.linewidth":    1.8,
    })


def plot_dqn_comparison(
    our_episodes:  list[float],
    sb3_episodes:  list[float],
    target: float,
    window: int = 100,
):
    """Two-panel figure: raw episode rewards + 100-episode rolling average."""
    figure_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("DQN on CartPole-v1 — Custom vs SB3", fontsize=14, y=1.01)

    # ---- Raw rewards ----
    ax1.set_title("Raw Episode Rewards")
    ax1.plot(our_episodes, color=C_OUR, alpha=0.4, linewidth=0.8, label="Custom DQN")
    ax1.plot(sb3_episodes, color=C_SB3, alpha=0.4, linewidth=0.8, label="SB3 DQN")
    ax1.axhline(target, color="k", linewidth=1.2, linestyle=":", label=f"Target ({target:.0f})")
    ax1.set_xlabel("Episode")
    ax1.set_ylabel("Reward")
    ax1.legend()

    # ---- Rolling average ----
    ax2.set_title(f"Rolling Average (window = {window})")
    w = window

    if len(our_episodes) >= w:
        our_avg = rolling_avg(our_episodes, w)
        our_std = rolling_std(our_episodes, w)
        our_x   = x_axis_for_rolling(our_episodes, w)
        ax2.plot(our_x, our_avg, color=C_OUR, label="Custom DQN")
        ax2.fill_between(our_x, our_avg - our_std, our_avg + our_std,
                         color=C_OUR, alpha=C_SHADE)

    if len(sb3_episodes) >= w:
        sb3_avg = rolling_avg(sb3_episodes, w)
        sb3_std = rolling_std(sb3_episodes, w)
        sb3_x   = x_axis_for_rolling(sb3_episodes, w)
        ax2.plot(sb3_x, sb3_avg, color=C_SB3, label="SB3 DQN")
        ax2.fill_between(sb3_x, sb3_avg - sb3_std, sb3_avg + sb3_std,
                         color=C_SB3, alpha=C_SHADE)

    ax2.axhline(target, color="k", linewidth=1.2, linestyle=":", label=f"Target ({target:.0f})")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel(f"Avg Reward (last {w} eps)")
    ax2.legend()

    plt.tight_layout()
    out = FIGURES_DIR / "dqn_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")


def plot_ppo_comparison(
    our_rewards:  list[float],
    our_steps:    list[int],
    sb3_rewards:  list[float],
    sb3_steps:    list[int],
    target: float,
    window: int = 50,
):
    """Two-panel figure: raw episode rewards vs steps + rolling average."""
    figure_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("PPO on LunarLander-v3 — Custom vs SB3", fontsize=14, y=1.01)

    # ---- Raw rewards vs environment steps ----
    ax1.set_title("Raw Episode Rewards")
    ax1.plot(our_steps, our_rewards, color=C_OUR, alpha=0.35, linewidth=0.8, label="Custom PPO")
    ax1.plot(sb3_steps, sb3_rewards, color=C_SB3, alpha=0.35, linewidth=0.8, label="SB3 PPO")
    ax1.axhline(target, color="k", linewidth=1.2, linestyle=":", label=f"Target ({target:.0f})")
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}K"))
    ax1.set_xlabel("Environment Steps")
    ax1.set_ylabel("Reward")
    ax1.legend()

    # ---- Rolling average vs episode index ----
    ax2.set_title(f"Rolling Average (window = {window} episodes)")
    w = window

    if len(our_rewards) >= w:
        our_avg = rolling_avg(our_rewards, w)
        our_std = rolling_std(our_rewards, w)
        our_x   = x_axis_for_rolling(our_rewards, w)
        ax2.plot(our_x, our_avg, color=C_OUR, label="Custom PPO")
        ax2.fill_between(our_x, our_avg - our_std, our_avg + our_std,
                         color=C_OUR, alpha=C_SHADE)

    if len(sb3_rewards) >= w:
        sb3_avg = rolling_avg(sb3_rewards, w)
        sb3_std = rolling_std(sb3_rewards, w)
        sb3_x   = x_axis_for_rolling(sb3_rewards, w)
        ax2.plot(sb3_x, sb3_avg, color=C_SB3, label="SB3 PPO")
        ax2.fill_between(sb3_x, sb3_avg - sb3_std, sb3_avg + sb3_std,
                         color=C_SB3, alpha=C_SHADE)

    ax2.axhline(target, color="k", linewidth=1.2, linestyle=":", label=f"Target ({target:.0f})")
    ax2.set_xlabel("Episode")
    ax2.set_ylabel(f"Avg Reward (last {w} eps)")
    ax2.legend()

    plt.tight_layout()
    out = FIGURES_DIR / "ppo_comparison.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Saved: {out}")


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


def plot_final_metrics(results: dict):
    """Bar chart comparing final performance metrics."""
    figure_style()
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle("Final Performance — Custom vs SB3", fontsize=14, y=1.01)

    # DQN
    ax = axes[0]
    dqn_data = results["dqn"]
    w = 100
    our_fin = np.mean(dqn_data["our"][-w:])  if len(dqn_data["our"]) >= w  else np.mean(dqn_data["our"])
    sb3_fin = np.mean(dqn_data["sb3"][-w:])  if len(dqn_data["sb3"]) >= w  else np.mean(dqn_data["sb3"])
    bars = ax.bar(["Custom DQN", "SB3 DQN"], [our_fin, sb3_fin],
                  color=[C_OUR, C_SB3], width=0.5, edgecolor="white")
    ax.axhline(DQN_CONFIG["reward_target"], color="k", linewidth=1.2, linestyle=":",
               label=f"Target ({DQN_CONFIG['reward_target']:.0f})")
    ax.set_title("CartPole-v1 — Final Avg Reward (last 100 ep)")
    ax.set_ylabel("Mean Reward")
    ax.set_ylim(0, 520)
    for bar, val in zip(bars, [our_fin, sb3_fin]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 8,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
    ax.legend()

    # PPO
    ax = axes[1]
    ppo_data = results["ppo"]
    w = 100
    our_fin = np.mean(ppo_data["our_r"][-w:]) if len(ppo_data["our_r"]) >= w else np.mean(ppo_data["our_r"])
    sb3_fin = np.mean(ppo_data["sb3_r"][-w:]) if len(ppo_data["sb3_r"]) >= w else np.mean(ppo_data["sb3_r"])
    bars = ax.bar(["Custom PPO", "SB3 PPO"], [our_fin, sb3_fin],
                  color=[C_OUR, C_SB3], width=0.5, edgecolor="white")
    ax.axhline(PPO_CONFIG["reward_target"], color="k", linewidth=1.2, linestyle=":",
               label=f"Target ({PPO_CONFIG['reward_target']:.0f})")
    ax.set_title("LunarLander-v3 — Final Avg Reward (last 100 ep)")
    ax.set_ylabel("Mean Reward")
    for bar, val in zip(bars, [our_fin, sb3_fin]):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"{val:.1f}", ha="center", fontsize=10, fontweight="bold")
    ax.legend()

    plt.tight_layout()
    out = FIGURES_DIR / "final_metrics.png"
    plt.savefig(out, dpi=150, bbox_inches="tight")
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

def main():
    print("=" * 60)
    print("Step 01 — Comparison: Custom implementations vs SB3")
    print("=" * 60)

    # ---- Load or build SB3 results ----
    cache = load_cache()
    if cache:
        print("\n[Using cached SB3 results — delete sb3_results_cache.json to retrain]")
        sb3_dqn = cache["sb3_dqn"]
        sb3_ppo = cache["sb3_ppo"]
    else:
        print("\n[Training SB3 DQN on CartPole-v1 ...]")
        sb3_dqn = train_sb3_dqn(total_timesteps=350_000)
        print(f"  Episodes captured: {len(sb3_dqn['rewards'])}")

        print("\n[Training SB3 PPO on LunarLander-v3 ...]")
        sb3_ppo = train_sb3_ppo(total_timesteps=264_192)
        print(f"  Episodes captured: {len(sb3_ppo['rewards'])}")

        save_cache({"sb3_dqn": sb3_dqn, "sb3_ppo": sb3_ppo})

    # ---- Read our custom training logs ----
    print("\n[Reading custom DQN logs ...]")
    _, our_dqn_rewards = read_last_tb_run(DQN_LOG_DIR, "reward/episode")
    print(f"  Episodes: {len(our_dqn_rewards)}")

    print("\n[Reading custom PPO logs ...]")
    our_ppo_steps, our_ppo_rewards = read_last_tb_run(PPO_LOG_DIR, "reward/episode")
    print(f"  Episodes: {len(our_ppo_rewards)}")

    # ---- Generate plots ----
    print("\n[Generating figures ...]")

    plot_dqn_comparison(
        our_episodes = our_dqn_rewards,
        sb3_episodes = sb3_dqn["rewards"],
        target       = DQN_CONFIG["reward_target"],
    )
    print("  dqn_comparison.png done")

    plot_ppo_comparison(
        our_rewards = [float(r) for r in our_ppo_rewards],
        our_steps   = [int(s)   for s in our_ppo_steps],
        sb3_rewards = sb3_ppo["rewards"],
        sb3_steps   = sb3_ppo["steps"],
        target      = PPO_CONFIG["reward_target"],
    )
    print("  ppo_comparison.png done")

    plot_final_metrics({
        "dqn": {
            "our": our_dqn_rewards,
            "sb3": sb3_dqn["rewards"],
        },
        "ppo": {
            "our_r": [float(r) for r in our_ppo_rewards],
            "sb3_r": sb3_ppo["rewards"],
        },
    })
    print("  final_metrics.png done")

    print(f"\nAll figures saved to: {FIGURES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
