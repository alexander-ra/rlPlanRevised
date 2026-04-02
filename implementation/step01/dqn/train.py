"""Training loop for DQN on CartPole-v1.

Orchestrates: environment interaction → replay buffer storage → training steps → target sync.
"""

import os
import sys
import gymnasium as gym
import numpy as np

# Ensure imports work regardless of where the script is run from
script_dir = os.path.dirname(os.path.abspath(__file__))
step01_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, step01_dir)

from config import DQN_CONFIG
from utils.logger import TBLogger
from dqn.agent import DQNAgent


def train_dqn(config: dict = DQN_CONFIG):
    env = gym.make(config["env_id"])
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    agent = DQNAgent(obs_dim, n_actions, config)
    logger = TBLogger(log_dir=os.path.join(step01_dir, "logs", "dqn"))

    # Track recent rewards for early stopping / progress reporting
    recent_rewards = []
    best_avg = -float("inf")

    model_dir = os.path.join(step01_dir, "models")
    os.makedirs(model_dir, exist_ok=True)
    best_path = os.path.join(model_dir, "dqn_cartpole_best.pt")
    final_path = os.path.join(model_dir, "dqn_cartpole.pt")

    for episode in range(config["total_episodes"]):
        state, _ = env.reset()
        episode_reward = 0.0
        done = False

        while not done:
            # 1. Agent picks action (epsilon-greedy during training)
            action = agent.select_action(state)

            # 2. Environment executes the action
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            # 3. Store transition in replay buffer
            agent.store_transition(state, action, reward, next_state, done)

            # 4. Train: sample from buffer and do one gradient step
            agent.train_step()

            state = next_state
            episode_reward += reward

        # After each episode: decay exploration and maybe sync target
        agent.decay_epsilon()

        if (episode + 1) % config["target_update_freq"] == 0:
            agent.sync_target_network()

        # Logging
        recent_rewards.append(episode_reward)
        logger.log_scalar("reward/episode", episode_reward, episode)
        logger.log_scalar("epsilon", agent.epsilon, episode)

        avg_reward = np.mean(recent_rewards[-100:])

        if (episode + 1) % 10 == 0:
            print(f"Episode {episode+1:4d}/{config['total_episodes']} | "
                  f"Reward: {episode_reward:6.1f} | "
                  f"Avg(100): {avg_reward:6.1f} | "
                  f"Epsilon: {agent.epsilon:.3f}")

        # Save best model checkpoint whenever we beat our previous best
        if len(recent_rewards) >= 100 and avg_reward > best_avg:
            best_avg = avg_reward
            agent.save(best_path)

        # Early stopping: if we've reached the target, no need to risk forgetting
        if len(recent_rewards) >= 100 and avg_reward >= config["reward_target"]:
            print(f"\n*** Solved at episode {episode+1}! Avg(100) = {avg_reward:.1f} >= {config['reward_target']} ***")
            break

    # Also save final model
    agent.save(final_path)
    env.close()
    logger.close()

    # Final evaluation
    final_avg = np.mean(recent_rewards[-100:])
    print(f"\nTraining complete. Final avg reward (last 100): {final_avg:.1f}")
    print(f"Best avg reward seen: {best_avg:.1f}")
    print(f"Target: {config['reward_target']} | {'PASS ✓' if best_avg >= config['reward_target'] else 'NOT YET ✗'}")
    print(f"Best model saved to {best_path}")
    print(f"Final model saved to {final_path}")


if __name__ == "__main__":
    train_dqn()
