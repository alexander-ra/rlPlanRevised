"""🟢 AI-GENERATED: Learning curve and comparison plotting utilities."""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


def smooth(values: list[float], window: int = 20) -> np.ndarray:
    """Simple moving average smoothing."""
    if len(values) < window:
        return np.array(values)
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode="valid")


def plot_learning_curve(
    rewards: list[float],
    title: str = "Learning Curve",
    window: int = 20,
    target: float | None = None,
    save_path: str | None = None,
):
    """Plot episode rewards with smoothed curve and optional target line."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(rewards, alpha=0.3, color="blue", label="Raw")
    if len(rewards) >= window:
        smoothed = smooth(rewards, window)
        ax.plot(range(window - 1, len(rewards)), smoothed, color="blue", label=f"Smoothed ({window})")
    if target is not None:
        ax.axhline(y=target, color="red", linestyle="--", label=f"Target ({target})")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    plt.show()
    return fig


def plot_comparison(
    rewards_custom: list[float],
    rewards_sb3: list[float],
    title: str = "Custom vs SB3",
    window: int = 20,
    save_path: str | None = None,
):
    """Plot two learning curves side by side for comparison."""
    fig, ax = plt.subplots(figsize=(10, 5))
    for rewards, label, color in [
        (rewards_custom, "Custom", "blue"),
        (rewards_sb3, "Stable-Baselines3", "orange"),
    ]:
        ax.plot(rewards, alpha=0.2, color=color)
        if len(rewards) >= window:
            smoothed = smooth(rewards, window)
            ax.plot(range(window - 1, len(rewards)), smoothed, color=color, label=label)
    ax.set_xlabel("Episode")
    ax.set_ylabel("Reward")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150)
        print(f"Saved plot to {save_path}")
    plt.show()
    return fig
