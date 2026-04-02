"""🔴 HAND-CODE: DQN Agent.

Implement the full DQN agent: epsilon-greedy action selection, training step
(sample from buffer, compute TD target with target network, update Q-network),
and target network synchronization.

References:
- Mnih et al. (2015) Algorithm 1
- Key: understand WHY the target network stabilizes training
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .q_network import QNetwork
from .replay_buffer import ReplayBuffer


class DQNAgent:
    """DQN Agent with target network and experience replay."""

    def __init__(self, obs_dim: int, n_actions: int, config: dict):
        """
        Args:
            obs_dim: Dimension of observation space.
            n_actions: Number of discrete actions.
            config: Hyperparameter dict (see config.py DQN_CONFIG).
        """
        # TODO: Create Q-network and target network (same architecture).
        #       Initialize optimizer. Set up epsilon schedule.
        #       Create replay buffer.
        raise NotImplementedError("Implement DQN agent init")

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Epsilon-greedy action selection.

        During training: with probability epsilon select random action,
        otherwise select argmax_a Q(s, a).
        During eval: always greedy (epsilon=0).
        """
        raise NotImplementedError

    def train_step(self) -> float | None:
        """Sample batch from replay buffer and perform one gradient update.

        Returns the loss value, or None if buffer doesn't have enough samples.

        Key steps:
        1. Sample batch from replay buffer
        2. Compute current Q-values: Q(s, a) from Q-network
        3. Compute target: r + gamma * max_a' Q_target(s', a') * (1 - done)
        4. Loss = MSE(current Q, target)
        5. Backprop and update Q-network
        """
        raise NotImplementedError

    def sync_target_network(self):
        """Copy Q-network weights to target network."""
        raise NotImplementedError

    def decay_epsilon(self):
        """Decay epsilon according to schedule."""
        raise NotImplementedError

    def save(self, path: str):
        """Save model weights."""
        raise NotImplementedError

    def load(self, path: str):
        """Load model weights."""
        raise NotImplementedError
