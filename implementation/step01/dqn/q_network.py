"""Q-Network for DQN.

A simple feedforward neural network (Multi-Layer Perceptron) that takes
an observation (state) as input and outputs a Q-value for EACH possible action.

Q(s, a) = "expected cumulative reward if I take action `a` in state `s`
           and then follow my current policy"

The agent picks the action with the highest Q-value: a* = argmax_a Q(s, a).

Architecture: obs_dim → [hidden_1, ReLU] → [hidden_2, ReLU] → n_actions
- No activation on the output layer because Q-values can be any real number
  (they represent expected rewards, which can be positive or negative).

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
            obs_dim: Dimension of observation space (e.g., 4 for CartPole).
            n_actions: Number of discrete actions (e.g., 2 for CartPole: left/right).
            hidden_sizes: List of hidden layer sizes, e.g. [64, 64].
        """
        super().__init__()

        # Build the network layer by layer.
        # For hidden_sizes=[64, 64] and obs_dim=4, n_actions=2:
        #   Linear(4, 64) → ReLU → Linear(64, 64) → ReLU → Linear(64, 2)
        layers = []
        prev_size = obs_dim  # input dimension for the first layer
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            prev_size = hidden_size
        # Final layer: maps last hidden layer to Q-value for each action
        # NO activation here — Q-values are unbounded real numbers
        layers.append(nn.Linear(prev_size, n_actions))

        # nn.Sequential chains all layers into a single callable module
        self.network = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass. Returns Q-values for all actions.

        Input:  x of shape (batch_size, obs_dim)
        Output: Q-values of shape (batch_size, n_actions)

        Example for CartPole (batch_size=32, obs_dim=4, n_actions=2):
          Input:  tensor of shape (32, 4) — 32 observations
          Output: tensor of shape (32, 2) — Q(s, left) and Q(s, right) for each
        """
        return self.network(x)
