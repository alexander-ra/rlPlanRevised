"""Training loop for PPO on LunarLander-v3.

PPO training structure differs from DQN:
  - DQN: one environment step → one gradient step (online)
  - PPO: collect a ROLLOUT of T steps → compute GAE → do K epochs of SGD

This script orchestrates:
  1. Rollout collection (agent interacts with env for n_steps)
  2. GAE computation (advantages + returns)
  3. PPO update (K epochs of mini-batch SGD)
  4. Logging and checkpointing
"""

import os
import sys
import numpy as np
import gymnasium as gym

# Ensure imports work regardless of where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
step01_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step01_dir)

from config import PPO_CONFIG
from utils.logger import TBLogger
from ppo.agent import PPOAgent


def train_ppo(config: dict = PPO_CONFIG):
    env = gym.make(config["env_id"])
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    agent = PPOAgent(obs_dim, n_actions, config)
    logger = TBLogger(log_dir=os.path.join(step01_dir, "logs", "ppo"))

    model_dir = os.path.join(step01_dir, "models")
    os.makedirs(model_dir, exist_ok=True)
    best_path = os.path.join(model_dir, "ppo_lunarlander_best.pt")
    final_path = os.path.join(model_dir, "ppo_lunarlander.pt")

    total_steps = 0
    episode_count = 0
    episode_reward = 0.0
    recent_rewards: list[float] = []
    best_avg = -float("inf")

    state, _ = env.reset()

    while total_steps < config["total_timesteps"]:
        # ---- Phase 1: Collect a rollout of n_steps ----
        rollout: dict[str, list] = {
            "states": [], "actions": [], "log_probs": [],
            "rewards": [], "dones": [], "values": [],
        }

        for _ in range(config["n_steps"]):
            # select_action returns (action, log_prob, value)
            action, log_prob, value = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            rollout["states"].append(state)
            rollout["actions"].append(action)
            rollout["log_probs"].append(log_prob)
            rollout["rewards"].append(reward)
            rollout["dones"].append(float(done))
            rollout["values"].append(value)

            state = next_state
            episode_reward += reward
            total_steps += 1

            if done:
                recent_rewards.append(episode_reward)
                logger.log_scalar("reward/episode", episode_reward, episode_count)
                episode_count += 1
                if episode_count % 10 == 0:
                    avg = np.mean(recent_rewards[-100:]) if recent_rewards else 0
                    print(f"Episode {episode_count:4d} | "
                          f"Reward: {episode_reward:7.1f} | "
                          f"Avg(100): {avg:7.1f} | "
                          f"Steps: {total_steps}/{config['total_timesteps']}")
                episode_reward = 0.0
                state, _ = env.reset()

        # Convert rollout lists to numpy arrays
        for key in rollout:
            rollout[key] = np.array(rollout[key])

        # Store the current state as "last_state" for bootstrapping V(s_T)
        rollout["last_state"] = state

        # ---- Phase 2: PPO update ----
        metrics = agent.update(rollout)
        logger.log_scalar("loss/policy", metrics["policy_loss"], total_steps)
        logger.log_scalar("loss/value", metrics["value_loss"], total_steps)
        logger.log_scalar("entropy", metrics["entropy"], total_steps)

        # ---- Phase 3: Checkpointing ----
        if len(recent_rewards) >= 100:
            avg = np.mean(recent_rewards[-100:])
            if avg > best_avg:
                best_avg = avg
                agent.save(best_path)

            # Early stopping
            if avg >= config["reward_target"]:
                print(f"\n*** Solved at step {total_steps}! "
                      f"Avg(100) = {avg:.1f} >= {config['reward_target']} ***")
                break

    # Save final model
    agent.save(final_path)
    env.close()
    logger.close()

    final_avg = np.mean(recent_rewards[-100:]) if len(recent_rewards) >= 100 else np.mean(recent_rewards)
    print(f"\nTraining complete. Final avg reward (last 100): {final_avg:.1f}")
    print(f"Best avg reward seen: {best_avg:.1f}")
    print(f"Target: {config['reward_target']} | {'PASS ✓' if best_avg >= config['reward_target'] else 'NOT YET ✗'}")
    print(f"Best model saved to {best_path}")
    print(f"Final model saved to {final_path}")


if __name__ == "__main__":
    train_ppo()
