"""Day 6: Benchmark your DQN/PPO implementations against Stable-Baselines3.

Run this after completing your implementations to generate comparison plots.
"""

import gymnasium as gym
import numpy as np
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback

from config import DQN_CONFIG, PPO_CONFIG
from utils.plotting import plot_comparison


class RewardLogCallback(BaseCallback):
    """Callback to capture per-episode rewards during SB3 training."""

    def __init__(self):
        super().__init__()
        self.episode_rewards = []
        self._current_reward = 0.0

    def _on_step(self) -> bool:
        self._current_reward += self.locals.get("rewards", [0])[0]
        dones = self.locals.get("dones", [False])
        if dones[0]:
            self.episode_rewards.append(self._current_reward)
            self._current_reward = 0.0
        return True


def benchmark_dqn():
    """Train SB3 DQN on CartPole with matching hyperparameters and compare."""
    config = DQN_CONFIG
    cb = RewardLogCallback()
    model = DQN(
        "MlpPolicy",
        config["env_id"],
        learning_rate=config["learning_rate"],
        gamma=config["gamma"],
        buffer_size=config["buffer_size"],
        batch_size=config["batch_size"],
        exploration_initial_eps=config["epsilon_start"],
        exploration_final_eps=config["epsilon_end"],
        target_update_interval=config["target_update_freq"],
        verbose=0,
    )
    model.learn(total_timesteps=config["total_episodes"] * 500, callback=cb)

    env = gym.make(config["env_id"])
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=config["eval_episodes"])
    print(f"SB3 DQN — Mean reward: {mean_reward:.2f} ± {std_reward:.2f}")
    return cb.episode_rewards


def benchmark_ppo():
    """Train SB3 PPO on LunarLander with matching hyperparameters and compare."""
    config = PPO_CONFIG
    cb = RewardLogCallback()
    model = PPO(
        "MlpPolicy",
        config["env_id"],
        learning_rate=config["learning_rate"],
        gamma=config["gamma"],
        gae_lambda=config["gae_lambda"],
        clip_range=config["clip_range"],
        ent_coef=config["entropy_coef"],
        vf_coef=config["value_loss_coef"],
        max_grad_norm=config["max_grad_norm"],
        n_steps=config["n_steps"],
        n_epochs=config["n_epochs"],
        batch_size=config["batch_size"],
        verbose=0,
    )
    model.learn(total_timesteps=config["total_timesteps"], callback=cb)

    env = gym.make(config["env_id"])
    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=config["eval_episodes"])
    print(f"SB3 PPO — Mean reward: {mean_reward:.2f} ± {std_reward:.2f}")
    return cb.episode_rewards


if __name__ == "__main__":
    print("=== DQN Benchmark ===")
    sb3_dqn_rewards = benchmark_dqn()

    print("\n=== PPO Benchmark ===")
    sb3_ppo_rewards = benchmark_ppo()

    # TODO: Load your custom implementation rewards and call plot_comparison()
    # plot_comparison(custom_dqn_rewards, sb3_dqn_rewards, "DQN: Custom vs SB3", save_path="plots/dqn_comparison.png")
    # plot_comparison(custom_ppo_rewards, sb3_ppo_rewards, "PPO: Custom vs SB3", save_path="plots/ppo_comparison.png")
