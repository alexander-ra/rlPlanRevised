"""🔴 HAND-CODE: Policy (Actor) and Value (Critic) Networks for PPO.

Implement two separate MLPs:
- PolicyNetwork: obs -> action probabilities (discrete)
- ValueNetwork: obs -> scalar state value V(s)

References:
- Schulman et al. (2017) Section 3-4
"""

import torch
import torch.nn as nn
from torch.distributions import Categorical


class PolicyNetwork(nn.Module):
    """Actor network: maps observations to action probabilities."""

    def __init__(self, obs_dim: int, n_actions: int, hidden_sizes: list[int]):
        super().__init__()
        # TODO: Build MLP with ReLU activations, final softmax over actions.
        raise NotImplementedError("Implement policy network")

    def forward(self, x: torch.Tensor) -> Categorical:
        """Returns a Categorical distribution over actions."""
        raise NotImplementedError

    def get_log_prob(self, states: torch.Tensor, actions: torch.Tensor) -> torch.Tensor:
        """Compute log π(a|s) for given state-action pairs."""
        raise NotImplementedError


class ValueNetwork(nn.Module):
    """Critic network: maps observations to scalar state values."""

    def __init__(self, obs_dim: int, hidden_sizes: list[int]):
        super().__init__()
        # TODO: Build MLP with ReLU activations, single scalar output (no activation).
        raise NotImplementedError("Implement value network")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Returns V(s) scalar value."""
        raise NotImplementedError
