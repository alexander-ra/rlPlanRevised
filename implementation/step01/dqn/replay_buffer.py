"""🔴 HAND-CODE: Experience Replay Buffer for DQN.

Implement a circular buffer that stores (state, action, reward, next_state, done) transitions
and supports uniform random sampling of mini-batches.

References:
- Mnih et al. (2015) Section 4: "experience replay" mechanism
- Sutton & Barto Ch 6: TD learning (for context on what gets stored)
"""

import numpy as np
import torch


class ReplayBuffer:
    """Fixed-size circular replay buffer storing transitions as numpy arrays."""

    def __init__(self, capacity: int, obs_dim: int):
        """
        Args:
            capacity: Maximum number of transitions to store.
            obs_dim: Dimension of observation space.
        """
        # TODO: Allocate pre-sized numpy arrays for states, actions, rewards,
        #       next_states, dones. Track current size and write position.
        raise NotImplementedError("Implement the replay buffer")

    def push(self, state, action, reward, next_state, done):
        """Store a single transition. Overwrites oldest if at capacity."""
        raise NotImplementedError

    def sample(self, batch_size: int):
        """Sample a random batch of transitions. Returns dict of torch tensors."""
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError
