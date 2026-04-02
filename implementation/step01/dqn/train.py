"""Training loop for DQN on CartPole-v1.

Orchestrates: environment interaction -> replay buffer storage -> training steps -> target sync.
"""

import gymnasium as gym

import sys
sys.path.insert(0, "..")
from config import DQN_CONFIG
from utils.logger import TBLogger
from dqn.agent import DQNAgent


def train_dqn(config: dict = DQN_CONFIG):
    env = gym.make(config["env_id"])
    obs_dim = env.observation_space.shape[0]
    n_actions = env.action_space.n

    agent = DQNAgent(obs_dim, n_actions, config)
    logger = TBLogger(log_dir="../../logs/dqn")

    for episode in range(config["total_episodes"]):
        state, _ = env.reset()
        episode_reward = 0.0
        done = False

        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            agent.train_step()
            state = next_state
            episode_reward += reward

        agent.decay_epsilon()

        if (episode + 1) % config["target_update_freq"] == 0:
            agent.sync_target_network()

        logger.log_scalar("reward/episode", episode_reward, episode)
        if (episode + 1) % 10 == 0:
            print(f"Episode {episode+1}/{config['total_episodes']} | "
                  f"Reward: {episode_reward:.1f} | Epsilon: {agent.epsilon:.3f}")

    agent.save("dqn_cartpole.pt")
    env.close()
    logger.close()
    print("Training complete. Model saved to dqn_cartpole.pt")


if __name__ == "__main__":
    train_dqn()
