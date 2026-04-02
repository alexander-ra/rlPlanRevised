"""🔴 HAND-CODE: Q-Network for DQN.

Implement a simple MLP that maps observations to Q-values for each action.

References:
- Mnih et al. (2015) Section 4: network architecture
- Sutton & Barto Ch 6.5: Q-learning
"""

import torch
import torch.nn as nn


class QNetwork(nn.Module):
    """MLP Q-network: obs_dim -> hidden layers -> n_actions."""

    def __init__(self, obs_dim: int, n_actions: int, hidden_sizes: list[int]):
        """
        Args:
            obs_dim: Dimension of observation space.
            n_actions: Number of discrete actions.
            hidden_sizes: List of hidden layer sizes, e.g. [64, 64].
        """
        super().__init__()
        # TODO: Build a sequential MLP with ReLU activations.
        #       Input: obs_dim, Output: n_actions (no activation on output).
        raise NotImplementedError("Implement the Q-network")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass. Returns Q-values for all actions."""
        raise NotImplementedError
