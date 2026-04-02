import os
import gymnasium as gym
from stable_baselines3 import DQN

# Locate the saved model
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "../models/dqn_cartpole")

# Load the trained model
model = DQN.load(model_path)

env = gym.make("CartPole-v1", render_mode="human")
obs, info = env.reset()
for _ in range(1000):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()
env.close()