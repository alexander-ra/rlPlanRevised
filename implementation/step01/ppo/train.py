"""Training loop for PPO on LunarLander-v3.

Orchestrates: rollout collection -> GAE computation -> PPO update -> logging.
"""

import numpy as np
import gymnasium as gym

import sys
sys.path.insert(0, "..")
from config import PPO_CONFIG
from utils.logger import TBLogger
from ppo.agent import PPOAgent


def train_ppo(config: dict = PPO_CONFIG):
    env = gym.make(config["env_id"])
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    agent = PPOAgent(obs_dim, n_actions, config)
    logger = TBLogger(log_dir="../../logs/ppo")

    total_steps = 0
    episode_count = 0
    episode_reward = 0.0

    state, _ = env.reset()

    while total_steps < config["total_timesteps"]:
        # Collect rollout
        rollout = {
            "states": [], "actions": [], "log_probs": [],
            "rewards": [], "dones": [], "values": [],
        }

        for _ in range(config["n_steps"]):
            action, log_prob = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            rollout["states"].append(state)
            rollout["actions"].append(action)
            rollout["log_probs"].append(log_prob)
            rollout["rewards"].append(reward)
            rollout["dones"].append(done)

            state = next_state
            episode_reward += reward
            total_steps += 1

            if done:
                logger.log_scalar("reward/episode", episode_reward, episode_count)
                episode_count += 1
                if episode_count % 10 == 0:
                    print(f"Episode {episode_count} | "
                          f"Reward: {episode_reward:.1f} | "
                          f"Steps: {total_steps}/{config['total_timesteps']}")
                episode_reward = 0.0
                state, _ = env.reset()

        # Convert rollout lists to numpy arrays
        for key in rollout:
            rollout[key] = np.array(rollout[key])

        # PPO update
        metrics = agent.update(rollout)
        logger.log_scalar("loss/policy", metrics.get("policy_loss", 0), total_steps)
        logger.log_scalar("loss/value", metrics.get("value_loss", 0), total_steps)

    agent.save("ppo_lunarlander.pt")
    env.close()
    logger.close()
    print("Training complete. Model saved to ppo_lunarlander.pt")


if __name__ == "__main__":
    train_ppo()
