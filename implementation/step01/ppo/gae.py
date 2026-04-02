"""🔴 HAND-CODE: Generalized Advantage Estimation (GAE).

Implement GAE-λ from:
  Schulman et al. (2015) "High-Dimensional Continuous Control Using
  Generalized Advantage Estimation" — Equation 11.

GAE(γ, λ):
  δ_t = r_t + γ * V(s_{t+1}) - V(s_t)
  A_t = Σ_{l=0}^{T-t} (γλ)^l * δ_{t+l}

This is computed efficiently in reverse (from last timestep to first).
"""

import numpy as np
import torch


def compute_gae(
    rewards: np.ndarray,
    values: np.ndarray,
    dones: np.ndarray,
    next_value: float,
    gamma: float,
    gae_lambda: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute GAE advantages and discounted returns.

    Args:
        rewards: Array of rewards, shape (T,).
        values: Array of V(s_t) estimates, shape (T,).
        dones: Array of done flags, shape (T,).
        next_value: V(s_{T+1}) bootstrap value for last state.
        gamma: Discount factor.
        gae_lambda: GAE lambda parameter.

    Returns:
        advantages: GAE advantages, shape (T,).
        returns: advantages + values (used as value targets), shape (T,).
    """
    # TODO: Implement reverse sweep GAE computation.
    #       Key: multiply by (1 - done) to zero out advantage across episode boundaries.
    raise NotImplementedError("Implement GAE")
