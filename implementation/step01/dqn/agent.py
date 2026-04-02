"""DQN Agent — the complete algorithm from Mnih et al. (2015).

Combines three key ideas that made deep RL work on high-dimensional problems:

1. EXPERIENCE REPLAY: Store transitions in a buffer, sample random mini-batches
   → breaks temporal correlations between consecutive training samples.

2. TARGET NETWORK: A separate, slowly-updated copy of the Q-network used to
   compute TD targets. Without it, both the prediction and the target shift
   on every update, creating a "moving target" problem that destabilizes training.
   Think of it like this: if you're trying to hit a bullseye but someone keeps
   moving the target, you'll never converge. The target network "freezes" the
   target for a while so the main network can learn.

3. EPSILON-GREEDY EXPLORATION: With probability ε, take a random action instead
   of the greedy one. ε starts high (explore) and decays toward 0 (exploit).
   This balances discovering new strategies vs. using what we've already learned.

The training step (Algorithm 1 from the paper):
  1. Sample batch of (s, a, r, s', done) from replay buffer
  2. Compute current Q-values: Q(s, a) using the MAIN network
  3. Compute TD target: y = r + γ * max_a' Q_TARGET(s', a') * (1 - done)
     - Uses TARGET network for stability
     - (1 - done) zeroes out the future value at terminal states
  4. Loss = MSE(Q(s,a), y)  — push our prediction toward the target
  5. Gradient descent step on the main network only

References:
- Mnih et al. (2015) Algorithm 1
"""

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from .q_network import QNetwork
from .replay_buffer import ReplayBuffer


class DQNAgent:
    """DQN Agent with target network and experience replay."""

    def __init__(self, obs_dim: int, n_actions: int, config: dict):
        self.obs_dim = obs_dim
        self.n_actions = n_actions
        self.gamma = config["gamma"]               # discount factor for future rewards
        self.batch_size = config["batch_size"]      # mini-batch size for training

        # --- Epsilon-greedy schedule ---
        # Start with lots of exploration (ε=1.0 → 100% random), then decay
        self.epsilon = config["epsilon_start"]
        self.epsilon_end = config["epsilon_end"]
        self.epsilon_decay = config["epsilon_decay"]

        # --- Q-Network (the "online" or "main" network) ---
        # This is the network we actually train with gradient descent.
        self.q_network = QNetwork(obs_dim, n_actions, config["hidden_sizes"])

        # --- Target Network (frozen copy of Q-network) ---
        # Same architecture, but weights are only updated periodically by copying
        # from the main network. This provides stable TD targets.
        self.target_network = QNetwork(obs_dim, n_actions, config["hidden_sizes"])
        # Initialize target with same weights as main network
        self.target_network.load_state_dict(self.q_network.state_dict())
        # IMPORTANT: Set target to eval mode — we never compute gradients for it
        self.target_network.eval()

        # --- Optimizer ---
        # Adam is the standard choice. Only optimizes the MAIN network parameters.
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=config["learning_rate"])

        # --- Replay Buffer ---
        self.buffer = ReplayBuffer(config["buffer_size"], obs_dim)

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Epsilon-greedy action selection.

        During training:
          - With probability ε → random action (EXPLORE)
          - With probability 1-ε → argmax_a Q(s, a) (EXPLOIT)
        During eval: always greedy.
        """
        if training and np.random.random() < self.epsilon:
            # EXPLORE: pick a random action uniformly
            return np.random.randint(self.n_actions)

        # EXPLOIT: pick the action with highest Q-value
        # torch.no_grad() tells PyTorch not to track gradients — saves memory
        # and compute since we're only doing inference here, not training
        with torch.no_grad():
            state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
            # unsqueeze(0) adds a batch dimension: shape (4,) → (1, 4)
            q_values = self.q_network(state_tensor)  # shape: (1, n_actions)
            # .argmax().item() finds the index of the max Q-value and converts to int
            return q_values.argmax(dim=1).item()

    def store_transition(self, state, action, reward, next_state, done):
        """Store a transition in the replay buffer."""
        self.buffer.push(state, action, reward, next_state, done)

    def train_step(self) -> float | None:
        """Sample batch from replay buffer and perform one gradient update.

        Returns the loss value, or None if buffer doesn't have enough samples.
        """
        # Don't train until we have enough samples for a full batch
        # (early in training, the buffer is still filling up)
        if len(self.buffer) < self.batch_size:
            return None

        # --- Step 1: Sample a random mini-batch ---
        batch = self.buffer.sample(self.batch_size)
        states = batch["states"]           # (batch_size, obs_dim)
        actions = batch["actions"]         # (batch_size,)
        rewards = batch["rewards"]         # (batch_size,)
        next_states = batch["next_states"] # (batch_size, obs_dim)
        dones = batch["dones"]             # (batch_size,) — 1.0 if terminal

        # --- Step 2: Compute current Q-values: Q(s, a) ---
        # q_network outputs Q-values for ALL actions: shape (batch_size, n_actions)
        # .gather(1, actions.unsqueeze(1)) selects the Q-value for the action
        # that was actually taken in each transition.
        # Example: if actions=[0, 1, 0] and Q=[[1.2, 0.8], [0.5, 1.1], [0.9, 0.3]]
        #   → gather selects [1.2, 1.1, 0.9]
        current_q = self.q_network(states).gather(1, actions.unsqueeze(1)).squeeze(1)

        # --- Step 3: Compute TD target using TARGET network ---
        #   y = r + γ * max_a' Q_target(s', a') * (1 - done)
        #
        # WHY (1 - done)? If the episode ended (done=1), there IS no next state,
        # so the future value is 0. The target becomes just the raw reward.
        with torch.no_grad():  # no gradients for target computation!
            # max(dim=1).values gives the best Q-value at the next state
            next_q_max = self.target_network(next_states).max(dim=1).values
            # The Bellman target: immediate reward + discounted future value
            td_target = rewards + self.gamma * next_q_max * (1.0 - dones)

        # --- Step 4: Compute loss ---
        # MSE between our current estimate and the TD target
        # This pushes Q(s,a) toward r + γ * max Q_target(s', a')
        loss = nn.functional.mse_loss(current_q, td_target)

        # --- Step 5: Gradient descent ---
        self.optimizer.zero_grad()  # clear old gradients
        loss.backward()             # compute new gradients
        self.optimizer.step()       # update weights

        return loss.item()  # .item() converts single-element tensor to Python float

    def sync_target_network(self):
        """Copy Q-network weights to target network.

        This is the "hard update" — every N episodes, the target network
        is fully replaced with the current Q-network weights. Between updates,
        the target network stays frozen, providing stable training targets.
        """
        self.target_network.load_state_dict(self.q_network.state_dict())

    def decay_epsilon(self):
        """Decay epsilon after each episode.

        Multiplicative decay: ε = max(ε_end, ε * decay_rate)
        This gradually shifts from exploration (random actions) to exploitation
        (greedy actions) as the agent learns a better policy.
        """
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)

    def save(self, path: str):
        """Save model weights to disk."""
        torch.save({
            "q_network": self.q_network.state_dict(),
            "target_network": self.target_network.state_dict(),
            "optimizer": self.optimizer.state_dict(),
            "epsilon": self.epsilon,
        }, path)

    def load(self, path: str):
        """Load model weights from disk."""
        checkpoint = torch.load(path, weights_only=True)
        self.q_network.load_state_dict(checkpoint["q_network"])
        self.target_network.load_state_dict(checkpoint["target_network"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])
        self.epsilon = checkpoint["epsilon"]
