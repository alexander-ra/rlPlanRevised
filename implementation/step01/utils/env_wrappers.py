"""🟢 AI-GENERATED: Gymnasium environment wrappers and reward normalization."""

import numpy as np
import gymnasium as gym


class RewardNormalizer(gym.Wrapper):
    """Normalize rewards using a running mean and std."""

    def __init__(self, env, clip: float = 10.0):
        super().__init__(env)
        self.clip = clip
        self._reward_mean = 0.0
        self._reward_var = 1.0
        self._count = 1e-4  # avoid division by zero

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self._count += 1
        delta = reward - self._reward_mean
        self._reward_mean += delta / self._count
        self._reward_var += delta * (reward - self._reward_mean)
        std = np.sqrt(self._reward_var / self._count) + 1e-8
        normalized = np.clip(reward / std, -self.clip, self.clip)
        return obs, normalized, terminated, truncated, info


class EpisodeMonitor(gym.Wrapper):
    """Track episode rewards and lengths, storing them in info dict."""

    def __init__(self, env):
        super().__init__(env)
        self._episode_reward = 0.0
        self._episode_length = 0

    def reset(self, **kwargs):
        self._episode_reward = 0.0
        self._episode_length = 0
        return self.env.reset(**kwargs)

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        self._episode_reward += reward
        self._episode_length += 1
        if terminated or truncated:
            info["episode"] = {
                "reward": self._episode_reward,
                "length": self._episode_length,
            }
        return obs, reward, terminated, truncated, info


def make_env(env_id: str, normalize_reward: bool = False, monitor: bool = True):
    """Create a Gymnasium environment with optional wrappers."""
    env = gym.make(env_id)
    if monitor:
        env = EpisodeMonitor(env)
    if normalize_reward:
        env = RewardNormalizer(env)
    return env
