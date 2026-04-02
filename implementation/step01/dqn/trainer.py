import os
from stable_baselines3 import DQN

script_dir = os.path.dirname(os.path.abspath(__file__))
model_dir = os.path.abspath(os.path.join(script_dir, "../models"))
os.makedirs(model_dir, exist_ok=True)

model = DQN("MlpPolicy", "CartPole-v1", verbose=1, tensorboard_log=os.path.join(script_dir, "../logs/"))
model.learn(total_timesteps=50_000)
model.save(os.path.join(model_dir, "dqn_cartpole"))