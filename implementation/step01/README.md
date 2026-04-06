# Step 01 — Reinforcement Learning Basics: Implementation

**PhD Context:** This step is part of the official research program:
- **EN:** Research on the possibilities for applying Artificial Intelligence in computer games
- **BG:** Изследване на възможностите за приложение на изкуствения интелект в компютърни игри

DQN + PPO from scratch on classic control environments.

> **Environment setup:** See the [project-level README](../../README.md#python-environment-setup).
> The project uses a single `.venv` at the repository root shared across all steps.

## Structure

```
step01/
├── dqn/
│   ├── replay_buffer.py    # 🔴 HAND-CODE: Circular replay buffer
│   ├── q_network.py        # 🔴 HAND-CODE: Q-network (MLP)
│   ├── agent.py            # 🔴 HAND-CODE: DQN agent (epsilon-greedy, train step, target sync)
│   └── train.py            # Training loop for DQN on CartPole-v1
├── ppo/
│   ├── networks.py         # 🔴 HAND-CODE: PolicyNetwork (actor) + ValueNetwork (critic)
│   ├── gae.py              # 🔴 HAND-CODE: Generalized Advantage Estimation
│   ├── agent.py            # 🔴 HAND-CODE: PPO agent (rollout, clipped surrogate loss, update)
│   └── train.py            # Training loop for PPO on LunarLander-v3
├── utils/
│   ├── env_wrappers.py     # 🟢 AI-GENERATED: Gymnasium wrappers + reward normalization
│   ├── logger.py           # 🟢 AI-GENERATED: TensorBoard logging utilities
│   └── plotting.py         # 🟢 AI-GENERATED: Learning curves, comparison charts
├── config.py               # Hyperparameter configs for DQN and PPO
├── benchmark.py            # Day 6: Compare your impl vs SB3
└── verify_setup.py         # Run to verify all dependencies work
```

## Targets

- **DQN on CartPole-v1:** mean reward ≥ 475 over 100 episodes
- **PPO on LunarLander-v3:** mean reward ≥ 200 over 100 episodes

## Implementation Plan (6 days)

### Day 1 — Architecture + Scaffolding
- Design DQN and PPO class interfaces (what methods, what inputs/outputs)
- The utils/ files and train loops are already provided — focus on the algorithm modules

### Days 2–3 — DQN from Scratch
- Implement `ReplayBuffer` — circular buffer with `push()` and `sample()` (returns torch tensors)
- Implement `QNetwork` — simple MLP: obs_dim → hidden → n_actions
- Implement `DQNAgent` — epsilon-greedy selection, train step with target network, sync
- **Key insight:** The target network is a *delayed copy* of the Q-network. Without it, the TD target shifts on every update, destabilizing training. Understand *why*, not just *how*.
- Train on CartPole-v1 until mean reward ≥ 475

### Days 4–5 — PPO from Scratch
- Implement `PolicyNetwork` (actor → Categorical distribution) + `ValueNetwork` (critic → scalar)
- Implement `compute_gae()` — reverse sweep, multiply by `(1 - done)` at episode boundaries
- Implement `PPOAgent.update()` — the clipped surrogate loss is the core:
  ```
  ratio = π_new(a|s) / π_old(a|s)
  L = -min(ratio * A, clip(ratio, 1-ε, 1+ε) * A)
  ```
  Trace through: if ratio > 1+ε, the gradient is zeroed → prevents catastrophically large updates.
- Train on LunarLander-v3 until mean reward ≥ 200

### Day 6 — Validation + Benchmarking
- Run `benchmark.py` to train SB3 DQN/PPO with matching hyperparameters
- Compare learning curves: your implementation vs SB3 (should converge to similar levels ±10%)
- If DQN doesn't converge: check target network update frequency and replay buffer sampling
- If PPO plateaus early: check GAE lambda and number of update epochs

## Debugging Tips

| Symptom | Likely Cause |
|---------|-------------|
| DQN reward stuck at ~10 | Target network not syncing, or epsilon not decaying |
| DQN reward oscillates wildly | Target update too frequent, or learning rate too high |
| PPO reward doesn't improve | GAE computation wrong (check done masking), or clip range too tight |
| PPO reward collapses after improving | Too many update epochs (try 4 instead of 10), or no advantage normalization |
| Both agents worse than random | Check action selection — are you passing the right observation shape? |
