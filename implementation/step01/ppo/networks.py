"""Policy (Actor) and Value (Critic) Networks for PPO.

PPO uses the actor-critic architecture — two separate networks that serve
complementary roles:

  Actor  (PolicyNetwork): Decides WHAT to do.  Maps observations → action
         probabilities.  Trained to maximise expected return via the clipped
         surrogate objective.

  Critic (ValueNetwork):  Evaluates HOW GOOD a state is.  Maps observations →
         scalar V(s).  Trained to minimise MSE between predicted and actual
         returns, and used to compute advantages (GAE) that tell the actor
         which actions were better than expected.

Why separate networks?
  Sharing weights (a single trunk) can cause gradient interference: what's
  good for predicting value isn't always good for choosing actions.  Keeping
  them separate avoids this coupling and makes debugging easier — you can
  monitor each loss independently.

References:
  - Schulman et al. (2017) "Proximal Policy Optimization Algorithms", Sec 3-4
  - Mnih et al. (2016) "Asynchronous Methods for Deep RL" (A3C baselines)
"""

import torch
import torch.nn as nn
from torch.distributions import Categorical


class PolicyNetwork(nn.Module):
    """Actor network: maps observations to a categorical action distribution.

    Architecture:  obs → FC+ReLU → FC+ReLU → … → logits → Softmax → Categorical

    The output is a torch.distributions.Categorical object.  This is convenient
    because we can:
      • sample actions:          dist.sample()
      • get log-probabilities:   dist.log_prob(action)
      • get entropy:             dist.entropy()
    all in one place, and torch handles the numerical stability (log-sum-exp
    trick) inside Categorical for us.
    """

    def __init__(self, obs_dim: int, n_actions: int, hidden_sizes: list[int]):
        super().__init__()

        # ---- Build the MLP dynamically from hidden_sizes ----
        # Example: obs_dim=8, hidden_sizes=[64,64], n_actions=4
        #   → Linear(8,64) → ReLU → Linear(64,64) → ReLU → Linear(64,4)
        layers: list[nn.Module] = []
        prev_size = obs_dim
        for h in hidden_sizes:
            layers.append(nn.Linear(prev_size, h))
            layers.append(nn.ReLU())
            prev_size = h

        # Final layer outputs raw logits (one per action).
        # We do NOT apply softmax here because Categorical accepts raw logits
        # and internally applies log-softmax, which is more numerically stable
        # than softmax → log.
        layers.append(nn.Linear(prev_size, n_actions))

        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> Categorical:
        """Forward pass: observation → Categorical distribution.

        Args:
            x: Observation tensor, shape (batch, obs_dim) or (obs_dim,).

        Returns:
            Categorical distribution parameterised by the network's logits.
        """
        logits = self.net(x)                    # shape: (batch, n_actions)
        return Categorical(logits=logits)       # internally does softmax

    def get_log_prob(self, states: torch.Tensor, actions: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Compute log π(a|s) and entropy H(π(·|s)) for given state-action pairs.

        This is used during the PPO update: we need log π_new(a|s) to compute
        the probability ratio  r(θ) = π_new / π_old.  We also return entropy
        which is added as a bonus to encourage exploration.

        Args:
            states:  shape (batch, obs_dim)
            actions: shape (batch,) — integer actions

        Returns:
            log_probs: shape (batch,)
            entropy:   shape (batch,)
        """
        dist = self.forward(states)
        return dist.log_prob(actions), dist.entropy()


class ValueNetwork(nn.Module):
    """Critic network: maps observations to scalar state value V(s).

    Architecture:  obs → FC+ReLU → FC+ReLU → … → scalar (no activation)

    The output has NO activation because V(s) can be any real number —
    positive (good state) or negative (bad state).  For LunarLander-v3,
    values typically range from about -200 (crash) to +250 (perfect landing).
    """

    def __init__(self, obs_dim: int, hidden_sizes: list[int]):
        super().__init__()

        layers: list[nn.Module] = []
        prev_size = obs_dim
        for h in hidden_sizes:
            layers.append(nn.Linear(prev_size, h))
            layers.append(nn.ReLU())
            prev_size = h

        # Single scalar output — the estimated state value V(s).
        layers.append(nn.Linear(prev_size, 1))

        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass: observation → V(s) scalar.

        Args:
            x: Observation tensor, shape (batch, obs_dim) or (obs_dim,).

        Returns:
            Value estimates, shape (batch, 1).  Squeeze to (batch,) where needed.
        """
        return self.net(x)
