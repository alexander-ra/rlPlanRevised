"""🔴 HAND-CODE: PPO Agent.

Implement the full PPO agent with clipped surrogate objective.

Key steps per update cycle:
1. Collect n_steps of experience (rollout)
2. Compute GAE advantages
3. For n_epochs: shuffle data into mini-batches, compute:
   - ratio = π_new(a|s) / π_old(a|s)
   - clipped surrogate loss = -min(ratio * A, clip(ratio, 1-ε, 1+ε) * A)
   - value loss = MSE(V(s), returns)
   - entropy bonus for exploration
4. Update policy and value networks

References:
- Schulman et al. (2017) Algorithm 1, Equation 7
- Key: understand WHY clipping prevents catastrophic policy updates
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .networks import PolicyNetwork, ValueNetwork
from .gae import compute_gae


class PPOAgent:
    """PPO Agent with clipped surrogate objective."""

    def __init__(self, obs_dim: int, n_actions: int, config: dict):
        """
        Args:
            obs_dim: Dimension of observation space.
            n_actions: Number of discrete actions.
            config: Hyperparameter dict (see config.py PPO_CONFIG).
        """
        # TODO: Create policy and value networks.
        #       Set up optimizers. Store config.
        #       Initialize rollout storage buffers.
        raise NotImplementedError("Implement PPO agent init")

    def select_action(self, state: np.ndarray) -> tuple[int, float]:
        """Sample action from policy and return (action, log_prob)."""
        raise NotImplementedError

    def update(self, rollout: dict) -> dict:
        """Perform PPO update using collected rollout data.

        Args:
            rollout: Dict with keys: states, actions, log_probs, rewards, dones, values

        Returns:
            Dict of loss metrics for logging.

        Key implementation details:
        - Compute GAE advantages from rollout
        - Normalize advantages (zero mean, unit std)
        - For each epoch: shuffle into mini-batches, compute clipped loss
        - The clipped objective (Eq. 7): L^CLIP = min(r_t * A_t, clip(r_t, 1-ε, 1+ε) * A_t)
        """
        raise NotImplementedError

    def save(self, path: str):
        """Save model weights."""
        raise NotImplementedError

    def load(self, path: str):
        """Load model weights."""
        raise NotImplementedError
