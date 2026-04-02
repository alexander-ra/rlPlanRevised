"""PPO Agent — Proximal Policy Optimization with clipped surrogate objective.

High-level PPO loop (Schulman et al. 2017, Algorithm 1):
  1. Run the current policy π_old for T timesteps, collecting a rollout.
  2. Compute advantages Â_t using GAE (from gae.py).
  3. For K epochs, optimise the "clipped surrogate" objective over mini-batches:

       L^CLIP(θ) = E[ min( r(θ) · Â,  clip(r(θ), 1−ε, 1+ε) · Â ) ]

     where r(θ) = π_θ(a|s) / π_old(a|s)   (probability ratio)

  4. Also minimise a value-function loss and add an entropy bonus:
       L = - L^CLIP + c_1 · L^VF − c_2 · H[π]

WHY clipping works:
  Without clipping, a single large policy update can move π far from π_old.
  If the new policy accidentally visits a "lucky" region (high advantage),
  the ratio r(θ) can explode, causing a catastrophically large gradient step.
  Clipping r(θ) to [1−ε, 1+ε] ensures that no single update can change the
  policy by more than ε (typically 0.2 = 20%).  This is the "proximal" part —
  we stay close to the old policy, giving us trust-region-like stability
  without the computational cost of TRPO's conjugate gradient solver.

WHY entropy bonus:
  Without it, the policy can collapse to a near-deterministic distribution
  early in training — e.g. always choosing "fire left thruster".  The entropy
  term penalises low-entropy (peaked) distributions, encouraging the agent to
  keep exploring until it has strong evidence for a particular action.

References:
  - Schulman et al. (2017) "Proximal Policy Optimization Algorithms"
  - Schulman et al. (2015) "High-Dimensional Continuous Control Using GAE"
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
        """Initialise actor, critic, optimiser, and hyperparameters.

        We use a SINGLE optimiser for both networks with their respective loss
        terms combined.  This is the standard approach in most PPO implementations
        (SB3, CleanRL, SpinningUp) — it's simpler and in practice works as well
        as separate optimisers because the gradients flow through separate
        parameter sets anyway.
        """
        self.config = config
        self.obs_dim = obs_dim
        self.n_actions = n_actions

        # ---- Networks ----
        hidden = config["hidden_sizes"]
        self.policy = PolicyNetwork(obs_dim, n_actions, hidden)
        self.value = ValueNetwork(obs_dim, hidden)

        # ---- Single optimiser for both networks ----
        # chain() merges the two sets of parameters into one iterator.
        from itertools import chain
        all_params = chain(self.policy.parameters(), self.value.parameters())
        self.optimizer = optim.Adam(all_params, lr=config["learning_rate"])

        # ---- Hyperparameters ----
        self.gamma = config["gamma"]
        self.gae_lambda = config["gae_lambda"]
        self.clip_range = config["clip_range"]
        self.entropy_coef = config["entropy_coef"]
        self.value_loss_coef = config["value_loss_coef"]
        self.max_grad_norm = config["max_grad_norm"]
        self.n_epochs = config["n_epochs"]
        self.batch_size = config["batch_size"]

    def select_action(self, state: np.ndarray) -> tuple[int, float, float]:
        """Sample action from the policy distribution.

        Args:
            state: Current observation, shape (obs_dim,).

        Returns:
            action:   integer action chosen by the policy.
            log_prob: log π(action | state) — stored for computing the ratio later.
            value:    V(state) from the critic — stored for GAE computation.
        """
        # Convert to tensor.  unsqueeze(0) adds a batch dim: (obs_dim,) → (1, obs_dim).
        state_t = torch.FloatTensor(state).unsqueeze(0)

        # No gradient needed during data collection (saves memory & time).
        with torch.no_grad():
            dist = self.policy(state_t)          # Categorical distribution
            action = dist.sample()               # shape (1,)
            log_prob = dist.log_prob(action)      # shape (1,)
            value = self.value(state_t)           # shape (1, 1)

        # Return python scalars (not tensors) for storage in numpy arrays.
        return action.item(), log_prob.item(), value.squeeze().item()

    def update(self, rollout: dict) -> dict:
        """Perform the PPO update: GAE → mini-batch SGD for K epochs.

        Args:
            rollout: Dict with numpy arrays:
                states:    (T, obs_dim)
                actions:   (T,)
                log_probs: (T,)  — log π_old(a|s), stored during rollout
                rewards:   (T,)
                dones:     (T,)
                values:    (T,)  — V(s) from critic during rollout

        Returns:
            Dict of averaged loss metrics for logging.
        """
        states = rollout["states"]
        actions = rollout["actions"]
        old_log_probs = rollout["log_probs"]
        rewards = rollout["rewards"]
        dones = rollout["dones"]
        values = rollout["values"]

        # ---- Step 1: Compute bootstrap value for the last state ----
        # If the rollout didn't end with a terminal state, we need V(s_T)
        # to estimate the remaining return.  We use the last collected state.
        last_state = torch.FloatTensor(rollout["last_state"]).unsqueeze(0)
        with torch.no_grad():
            next_value = self.value(last_state).squeeze().item()

        # ---- Step 2: Compute GAE advantages and returns ----
        advantages, returns = compute_gae(
            rewards, values, dones, next_value,
            self.gamma, self.gae_lambda,
        )

        # ---- Step 3: Convert everything to tensors ----
        states_t = torch.FloatTensor(states)
        actions_t = torch.LongTensor(actions)
        old_log_probs_t = torch.FloatTensor(old_log_probs)
        advantages_t = torch.FloatTensor(advantages)
        returns_t = torch.FloatTensor(returns)

        # ---- Step 4: Normalise advantages ----
        # This is a standard trick that makes training more stable.
        # Zero-mean, unit-variance advantages ensure that roughly half of the
        # actions look "good" and half look "bad", giving balanced gradients.
        advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std() + 1e-8)

        # ---- Step 5: Mini-batch SGD for K epochs ----
        T = len(states)
        total_policy_loss = 0.0
        total_value_loss = 0.0
        total_entropy = 0.0
        n_updates = 0

        for _epoch in range(self.n_epochs):
            # Shuffle the indices for each epoch to break correlations.
            indices = np.random.permutation(T)

            for start in range(0, T, self.batch_size):
                end = start + self.batch_size
                mb_idx = indices[start:end]

                mb_states = states_t[mb_idx]
                mb_actions = actions_t[mb_idx]
                mb_old_log_probs = old_log_probs_t[mb_idx]
                mb_advantages = advantages_t[mb_idx]
                mb_returns = returns_t[mb_idx]

                # ---- Evaluate the current policy on the batch ----
                # This gives us π_new(a|s) and the entropy of π_new.
                new_log_probs, entropy = self.policy.get_log_prob(mb_states, mb_actions)
                new_values = self.value(mb_states).squeeze(-1)

                # ---- Probability ratio r(θ) = π_new / π_old ----
                # We work in log space for numerical stability:
                #   log r = log π_new - log π_old  →  r = exp(log r)
                log_ratio = new_log_probs - mb_old_log_probs
                ratio = torch.exp(log_ratio)

                # ---- Clipped surrogate objective (Equation 7) ----
                # L^CLIP = min( r·A,  clip(r, 1-ε, 1+ε)·A )
                #
                # The min() ensures that:
                #   - If A > 0 (action was good): ratio can increase to at most 1+ε
                #     → we reward the action, but not too much
                #   - If A < 0 (action was bad): ratio can decrease to at most 1-ε
                #     → we penalise the action, but not too much
                surr1 = ratio * mb_advantages
                surr2 = torch.clamp(ratio, 1.0 - self.clip_range, 1.0 + self.clip_range) * mb_advantages
                policy_loss = -torch.min(surr1, surr2).mean()

                # ---- Value function loss ----
                # Simple MSE between critic's prediction and GAE returns.
                # Some implementations clip the value loss too, but the original
                # PPO paper found it didn't help much.
                value_loss = nn.functional.mse_loss(new_values, mb_returns)

                # ---- Entropy bonus ----
                # Higher entropy = more exploration.  We SUBTRACT (maximise) entropy.
                entropy_loss = -entropy.mean()

                # ---- Combined loss ----
                # L = L^CLIP + c1 · L^VF + c2 · L^entropy
                loss = (
                    policy_loss
                    + self.value_loss_coef * value_loss
                    + self.entropy_coef * entropy_loss
                )

                # ---- Gradient step ----
                self.optimizer.zero_grad()
                loss.backward()

                # Gradient clipping prevents exploding gradients.
                # max_grad_norm = 0.5 is standard in PPO implementations.
                nn.utils.clip_grad_norm_(
                    list(self.policy.parameters()) + list(self.value.parameters()),
                    self.max_grad_norm,
                )

                self.optimizer.step()

                total_policy_loss += policy_loss.item()
                total_value_loss += value_loss.item()
                total_entropy += -entropy_loss.item()
                n_updates += 1

        # Return averaged metrics
        return {
            "policy_loss": total_policy_loss / n_updates,
            "value_loss": total_value_loss / n_updates,
            "entropy": total_entropy / n_updates,
        }

    def save(self, path: str):
        """Save both networks' weights to a single file."""
        torch.save({
            "policy": self.policy.state_dict(),
            "value": self.value.state_dict(),
        }, path)

    def load(self, path: str):
        """Load both networks' weights from a file."""
        checkpoint = torch.load(path, weights_only=True)
        self.policy.load_state_dict(checkpoint["policy"])
        self.value.load_state_dict(checkpoint["value"])
