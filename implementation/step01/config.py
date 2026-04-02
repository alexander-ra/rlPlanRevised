"""Hyperparameter configurations for Step 01 implementations."""

DQN_CONFIG = {
    "env_id": "CartPole-v1",
    "learning_rate": 1e-3,
    "gamma": 0.99,
    "buffer_size": 50_000,
    "batch_size": 64,
    "epsilon_start": 1.0,
    "epsilon_end": 0.001,
    "epsilon_decay": 0.995,
    "target_update_freq": 5,     # episodes between target network syncs
    "hidden_sizes": [128, 128],
    "total_episodes": 1500,
    "eval_episodes": 100,
    "reward_target": 475.0,
}

PPO_CONFIG = {
    "env_id": "LunarLander-v3",
    "learning_rate": 3e-4,
    "gamma": 0.99,
    "gae_lambda": 0.95,
    "clip_range": 0.2,
    "entropy_coef": 0.01,
    "value_loss_coef": 0.5,
    "max_grad_norm": 0.5,
    "n_steps": 2048,        # steps per rollout
    "n_epochs": 10,          # update epochs per rollout
    "batch_size": 64,
    "hidden_sizes": [128, 128],
    "total_timesteps": 500_000,
    "eval_episodes": 100,
    "reward_target": 200.0,
}
