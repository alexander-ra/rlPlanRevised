"""Generalized Advantage Estimation (GAE-λ).

Background — why advantages matter:
  Policy gradient methods update the policy using:
    ∇J ≈ E[ ∇ log π(a|s) · Ψ ]
  where Ψ is some estimate of "how good was the action we took?"

  If Ψ = total_return:  unbiased but HIGH variance (noisy gradients).
  If Ψ = V(s):          low variance but HIGH bias (doesn't measure action quality).

  GAE offers a smooth trade-off between these extremes using a λ ∈ [0, 1]:
    λ = 0  →  one-step TD advantage  (low variance, high bias)
    λ = 1  →  Monte-Carlo advantage  (high variance, low bias)
    λ ≈ 0.95 is the sweet spot for most tasks (Schulman et al. 2015).

GAE formula (Equation 11):
  δ_t     = r_t + γ · V(s_{t+1}) − V(s_t)          [TD residual]
  A_t^GAE = Σ_{l=0}^{T-t} (γλ)^l · δ_{t+l}        [exponentially-weighted sum]

This is computed efficiently by sweeping BACKWARD from the last timestep:
  A_{T-1} = δ_{T-1}
  A_{t}   = δ_t + (γλ) · A_{t+1}     (for t = T-2, T-3, …, 0)

The (1 − done) mask zeroes out the bootstrap whenever an episode ended,
because V(s_{t+1}) is meaningless after a terminal state.

References:
  Schulman et al. (2015) "High-Dimensional Continuous Control Using
  Generalized Advantage Estimation" — Equation 11
"""

import numpy as np


def compute_gae(
    rewards: np.ndarray,
    values: np.ndarray,
    dones: np.ndarray,
    next_value: float,
    gamma: float,
    gae_lambda: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute GAE advantages and value-function targets (returns).

    Args:
        rewards:    shape (T,).  Rewards received at each timestep.
        values:     shape (T,).  V(s_t) estimates from the critic.
        dones:      shape (T,).  1.0 if episode ended at step t, else 0.0.
        next_value: V(s_T) — bootstrap value for the state AFTER the last
                    step in the rollout.  If the rollout ended at a terminal
                    state this will be 0, but if the rollout was truncated
                    mid-episode we need the critic's estimate to avoid bias.
        gamma:      Discount factor (e.g. 0.99).
        gae_lambda: GAE lambda (e.g. 0.95).

    Returns:
        advantages: shape (T,).  GAE advantages A_t^{GAE(γ,λ)}.
        returns:    shape (T,).  Value targets = advantages + values.
                    The critic is trained to minimise MSE(V(s), returns).
    """
    T = len(rewards)
    advantages = np.zeros(T, dtype=np.float32)

    # ---- Reverse sweep: compute GAE from last timestep backward ----
    # We accumulate the running GAE estimate in `gae`.
    gae = 0.0
    for t in reversed(range(T)):
        # If this was the last step in the rollout, the "next value" is the
        # bootstrap.  Otherwise it's the critic's estimate at t+1.
        if t == T - 1:
            next_val = next_value
            # If the episode actually ended at the last step, the bootstrap
            # should be 0 (no future rewards).  The (1 - done) handles this.
            next_non_terminal = 1.0 - dones[t]
        else:
            next_val = values[t + 1]
            next_non_terminal = 1.0 - dones[t]

        # ---- TD residual δ_t ----
        # δ_t = r_t + γ · V(s_{t+1}) · (1 − done_t) − V(s_t)
        #
        # (1 − done_t) zeroes out the bootstrap when the episode ended at step t,
        # because the "next state" is terminal and has no future value.
        delta = rewards[t] + gamma * next_val * next_non_terminal - values[t]

        # ---- Recursive GAE accumulation ----
        # A_t = δ_t + (γλ) · (1 − done_t) · A_{t+1}
        #
        # The (1 − done_t) also resets the running advantage across episode
        # boundaries — if episode ended at step t, the advantage at t should
        # NOT carry information from the next episode's advantages.
        gae = delta + gamma * gae_lambda * next_non_terminal * gae

        advantages[t] = gae

    # ---- Compute returns (value targets) ----
    # returns_t = A_t + V(s_t)
    #
    # Why?  The advantage is A_t = Q(s,a) − V(s), so:
    #   returns_t = Q(s,a) = A_t + V(s)
    # This gives us the "target" that the critic should have predicted.
    # We train the critic to minimise MSE(V(s), returns).
    returns = advantages + values

    return advantages, returns
