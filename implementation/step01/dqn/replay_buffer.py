"""Experience Replay Buffer for DQN.

A circular buffer that stores (state, action, reward, next_state, done) transitions
and supports uniform random sampling of mini-batches.

WHY REPLAY BUFFER?
- In naive Q-learning, we update on each transition as it happens. This creates
  two problems:
  1. Consecutive transitions are highly correlated (s_t and s_{t+1} are similar),
     which biases the gradient updates.
  2. Rare but important transitions (e.g., getting a high reward) are seen only once.
- The replay buffer stores transitions and samples RANDOM mini-batches, which:
  - Breaks temporal correlation between training samples
  - Allows reuse of each transition many times
  - Makes training more stable and sample-efficient

References:
- Mnih et al. (2015) Section 4: "experience replay" mechanism
- Sutton & Barto Ch 6: TD learning (for context on what gets stored)
"""

import numpy as np
import torch


class ReplayBuffer:
    """Fixed-size circular replay buffer storing transitions as numpy arrays.

    Uses pre-allocated numpy arrays for memory efficiency. When the buffer is
    full, new transitions overwrite the oldest ones (circular/ring buffer).
    """

    def __init__(self, capacity: int, obs_dim: int):
        """
        Args:
            capacity: Maximum number of transitions to store.
            obs_dim: Dimension of observation space (e.g., 4 for CartPole).
        """
        self.capacity = capacity

        # Pre-allocate arrays — much faster than appending to Python lists.
        # Each array holds `capacity` entries. We index with `self.pos`.
        self.states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.actions = np.zeros(capacity, dtype=np.int64)
        self.rewards = np.zeros(capacity, dtype=np.float32)
        self.next_states = np.zeros((capacity, obs_dim), dtype=np.float32)
        self.dones = np.zeros(capacity, dtype=np.float32)  # 1.0 if episode ended

        # `pos` is the write cursor — where the next transition will be stored.
        # `size` tracks how many slots are actually filled (up to `capacity`).
        self.pos = 0
        self.size = 0

    def push(self, state, action, reward, next_state, done):
        """Store a single transition. Overwrites oldest if at capacity.

        This is called after every environment step:
            next_state, reward, done = env.step(action)
            buffer.push(state, action, reward, next_state, done)
        """
        # Write into the current position (overwrites old data if buffer is full)
        self.states[self.pos] = state
        self.actions[self.pos] = action
        self.rewards[self.pos] = reward
        self.next_states[self.pos] = next_state
        self.dones[self.pos] = float(done)  # convert bool → 0.0 or 1.0

        # Advance the write cursor, wrapping around to 0 when we reach capacity
        # Example: capacity=5, after positions 0,1,2,3,4 → next write goes to 0
        self.pos = (self.pos + 1) % self.capacity

        # Size grows until we fill the buffer, then stays at capacity
        self.size = min(self.size + 1, self.capacity)

    def sample(self, batch_size: int) -> dict:
        """Sample a random batch of transitions.

        Returns a dict of torch tensors ready for neural network training.
        The random sampling is what breaks the temporal correlation — this is
        the key insight of experience replay.
        """
        # Pick `batch_size` random indices from the filled portion of the buffer
        indices = np.random.randint(0, self.size, size=batch_size)

        # Convert numpy arrays to PyTorch tensors for gradient computation.
        # .float() ensures consistent dtype for the neural network.
        return {
            "states": torch.tensor(self.states[indices], dtype=torch.float32),
            "actions": torch.tensor(self.actions[indices], dtype=torch.long),
            "rewards": torch.tensor(self.rewards[indices], dtype=torch.float32),
            "next_states": torch.tensor(self.next_states[indices], dtype=torch.float32),
            "dones": torch.tensor(self.dones[indices], dtype=torch.float32),
        }

    def __len__(self):
        """Returns the number of transitions currently stored."""
        return self.size
