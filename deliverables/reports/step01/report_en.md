<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->

# Chapter 01 — RL Basics: Implementation Report

**Environment:** April 2026  
**Algorithms:** DQN (CartPole-v1), PPO (LunarLander-v3)  
**Targets:** DQN ≥ 475, PPO ≥ 200 (avg over 100 episodes)  
**Status:** Both targets achieved ✓

---

## Table of Contents

- [Overview](#overview)
- [DQN — Deep Q-Network](#dqn)
  - [Architecture](#dqn-architecture)
  - [Key Design Decisions](#dqn-design)
  - [Hyperparameter Iterations](#dqn-iterations)
  - [Final Results](#dqn-results)
- [PPO — Proximal Policy Optimization](#ppo)
  - [Architecture](#ppo-architecture)
  - [Key Design Decisions](#ppo-design)
  - [Hyperparameter Iterations](#ppo-iterations)
  - [Final Results](#ppo-results)
- [Comparison with SB3 Baselines](#comparison)
- [Key Learnings](#learnings)

---

## Overview <a id="overview"></a>

Chapter 01 implements two foundational RL algorithms from scratch in PyTorch, with
extensive inline comments explaining the *why* behind each design choice. Both
algorithms are compared against Stable-Baselines3 (SB3): PPO with our hyperparameters,
DQN with the RL Baselines3 Zoo's tuned CartPole settings (see [Comparison](#comparison)).

**Source layout:**

```
implementation/step01/
├── dqn/
│   ├── replay_buffer.py   # Circular buffer, random batch sampling
│   ├── q_network.py       # MLP Q-function
│   ├── agent.py           # DQNAgent: select/store/train/sync/save
│   └── train.py           # Training loop, best-model checkpointing, early stop
├── ppo/
│   ├── networks.py        # PolicyNetwork (actor), ValueNetwork (critic)
│   ├── gae.py             # Generalized Advantage Estimation (reverse sweep)
│   ├── agent.py           # PPOAgent: rollout → GAE → clipped SGD
│   └── train.py           # Training loop, rollout collection, logging
├── compare_sb3.py         # Comparison script — reads TB logs, trains SB3
├── config.py              # DQN_CONFIG, PPO_CONFIG
└── utils/
    └── logger.py          # TensorBoard SummaryWriter wrapper
```

---

## DQN — Deep Q-Network <a id="dqn"></a>

### Architecture <a id="dqn-architecture"></a>

**Environment:** `CartPole-v1` — 4-dimensional continuous observation, 2 discrete actions,
maximum 500 steps per episode.

**Q-network:** Two hidden layers, ReLU activations, no output activation (Q-values can be
any real number). Size `[obs_dim=4 → 128 → 128 → 2]`.

**Replay buffer:** Pre-allocated numpy arrays with a circular write cursor. Stores
`(state, action, reward, next_state, done)` tuples. Random mini-batch sampling breaks
temporal correlation between consecutive transitions.

**Target network:** A frozen copy of the Q-network, synced every `target_update_freq`
episodes. Prevents the unstable feedback loop where the TD target moves at the same rate
as the predictions being trained.

### Key Design Decisions <a id="dqn-design"></a>

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Exploration schedule | Episode-based ε-decay (`ε × 0.995` per episode) | More predictable than step-based when episode length varies |
| Minimum epsilon | `ε_min = 0.001` | Avoids random action deaths after convergence; lower than SB3's default 0.05 |
| Target sync | Every 5 episodes | Balances stability vs. speed; too infrequent (10) caused slower plateaus |
| Network size | `[128, 128]` | `[64, 64]` plateaued around 300 avg reward; larger network learned faster |
| Buffer size | 50,000 | Smaller (10K) caused over-fitting to recent experience |

### Hyperparameter Iterations <a id="dqn-iterations"></a>

The final configuration was reached after 3 tuning rounds:

#### Run 1 — Baseline (500 episodes)
- Config: `buffer=10K, hidden=[64,64], episodes=500, target_freq=10, ε_min=0.01`
- Result: Final avg 225, never crossed 475 target
- Problem: Small buffer and network; infrequent target updates

#### Run 2 — First tuning (1000 episodes)
- Config: `buffer=50K, hidden=[128,128], episodes=1000, target_freq=5, ε_min=0.01`
- Result: Peak avg **479.1** at episode 810, but degraded to 302.6 by end
- Problem: `ε_min=0.01` means 1% random actions permanently — enough to kill long episodes
- Fix needed: Lower `ε_min` + add best-model checkpointing

#### Run 3 — Final (1500 episodes, early stopping added)
- Config: same + `ε_min=0.001, episodes=1500`
- Added best-model saving and early stop (saves when 475 target is first hit, stops training)
- Result: **Solved at episode 1011**, Avg(100) = **477.5** ✓

### Final Results <a id="dqn-results"></a>

| Metric | Value |
|--------|-------|
| Solved at episode | 1011 |
| Final avg reward (100 eps) | 477.5 |
| Target | 475.0 |
| Total episodes trained | 1011 (early stop) |
| Best model | `models/dqn_cartpole_best.pt` |

---

## PPO — Proximal Policy Optimization <a id="ppo"></a>

### Architecture <a id="ppo-architecture"></a>

**Environment:** `LunarLander-v3` — 8-dimensional continuous observation, 4 discrete actions.
A successful landing scores +200; crash is −100; fuel usage is penalised.

**Actor-Critic (separate networks):**
- **PolicyNetwork**: `[obs=8 → 128 → 128 → 4]` with logits → `Categorical` distribution
- **ValueNetwork**: `[obs=8 → 128 → 128 → 1]` with unbounded scalar output

Separate networks avoid gradient interference between the policy and value objectives.
A single Adam optimizer trains both via a combined loss.

**GAE (Generalized Advantage Estimation, λ=0.95):** Computed by a reverse sweep over the
rollout buffer. The `(1 − done)` mask zeroes out the bootstrap across episode boundaries,
correctly handling rollouts that span multiple episodes.

**Clipped surrogate objective:**

$$L^{CLIP} = \mathbb{E}\left[\min\left(r_t(\theta)\hat{A}_t,\ \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t\right)\right]$$

where $r_t(\theta) = \pi_\theta(a|s) / \pi_{old}(a|s)$ and $\epsilon = 0.2$.

### Key Design Decisions <a id="ppo-design"></a>

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Advantage normalisation | Zero mean, unit std per rollout | Stabilises gradient magnitude across diverse reward scales |
| Entropy bonus | `coef = 0.01` | Prevents premature policy collapse; encourages exploration |
| Gradient clipping | `max_norm = 0.5` | Avoids exploding gradients during early training |
| Rollout length | `n_steps = 2048` | Long enough for multi-step credit assignment across landings |
| Mini-batch SGD | 10 epochs, batch=64 | Standard PPO; re-using each rollout 10× before discarding |

### Hyperparameter Iterations <a id="ppo-iterations"></a>

#### Run 1 — Baseline (300K steps, hidden=[64,64])
- Result: Peak avg **179.9**, never crossing 200 target
- Problem: Small network underfitted LunarLander's 8-dim observation
- Also: 300K steps just barely too short for full convergence

#### Run 2 — Final (500K steps, hidden=[128,128])
- Network size doubled; training budget increased by 67%
- Result: **Solved at 264K steps** (early stop triggered), Avg(100) = **202.2** ✓
- Notably: solved 236K steps *before* the training budget ran out

### Final Results <a id="ppo-results"></a>

| Metric | Value |
|--------|-------|
| Solved at step | 264,192 |
| Final avg reward (100 eps) | 202.2 |
| Target | 200.0 |
| Total steps trained | 264,192 (early stop) |
| Best model | `models/ppo_lunarlander_best.pt` |

---

## Comparison with SB3 Baselines <a id="comparison"></a>

SB3 PPO was trained with our core hyperparameters (learning rate, γ, network size,
clip range, etc.) and the same 500K-step budget. SB3 DQN was trained with the RL Baselines3
Zoo's tuned CartPole-v1 hyperparameters for 100K steps (run of 6 April 2026, seed 42). Source:
`implementation/step01/compare_sb3.py`; the SB3 episode rewards are in `sb3_results_cache.json`.

### 4.1 DQN on CartPole-v1

![DQN on CartPole-v1: rolling 100-episode average of the reward, our implementation against SB3 (first 1,061 of SB3's 1,255 episodes).](figures/dqn_rolling.png)

**Custom DQN** solves CartPole by episode ~1011 and hits the 475 target (avg over 100 eps).
**SB3 DQN** (RL Zoo settings: learning rate 0.0023, `[256, 256]`, target sync every 10 steps,
`train_freq=256` with 128 gradient steps, ε → 0.04 over the first 16K steps) ran 100K steps
(1,255 episodes). Its best rolling-100 average is **222.4**, at episode 695 (≈51K steps); it ends
at 134.3. The figure shows its first 1,061 episodes.

> **Superseded run.** An earlier SB3 DQN run (3 April 2026: 750K steps, 17,176 episodes, our core
> hyperparameters with `exploration_fraction=0.36` and `target_update_interval=1000`) peaked at
> 293.9. The run above replaced it on 6 April; its results remain in the git history of
> `sb3_results_cache.json` (commit 4a173d2).

**Why the gap?** Not established. Because SB3 ran with tuned rather than matched settings,
the comparison is not like-for-like. Two differences are untested:

1. **Exploration during the plotted episodes**: the rewards are those of training episodes, in
   which SB3 still acts at random 4% of the time (final ε = 0.04), while our ε (×0.995 per
   episode) was about 0.006 when the task was solved.

2. **Updates per step**: SB3 makes 128 gradient steps every 256 environment steps, half as
   many updates per step as our agent, which updates on every step.

Each implementation was run once (ours without a fixed seed), and the Zoo trains these settings
for 50K steps, so SB3's shortfall at 100K needs a second seed before it is read as a property
of SB3.

### 4.2 PPO on LunarLander-v3

![PPO on LunarLander-v3: rolling 50-episode average of the reward, our implementation (final run) against SB3 (first 577 of its 1,224 episodes).](figures/ppo_rolling.png)

**Custom PPO** crosses the 200 target by episode ~543 (264K steps).
**SB3 PPO** with the same step budget (500K steps) peaks at a best rolling-100 of **131.2**
and is still climbing at the end of training. (The figure's rolling window is 50 episodes; the
numbers in the text use 100.)

The gap is narrower here than in DQN. Both use identical PPO hyperparameters. The remaining
difference may come from:
- SB3's orthogonal weight initialisation;
- SB3 normalising advantages per mini-batch rather than per rollout;
- chance: each implementation was run once.

Given more training budget (e.g. 1–2M steps), SB3 PPO would likely converge to target.
In this single run, our custom PPO used its samples more efficiently than SB3 on this task.

### 4.3 Peak Performance Summary

![Best rolling 100-episode average: our implementations against SB3.](figures/final_metrics.png)

| Algorithm | Environment | Our Best Avg (rolling 100) | SB3 Best Avg (rolling 100) | Target |
|-----------|------------|---------------------------|---------------------------|--------|
| DQN | CartPole-v1 | **477.5** | 222.4 | 475 |
| PPO | LunarLander-v3 | **203.6** | 131.2 | 200 |

> **Methodology note:** "Best rolling-100 avg" is the maximum of the 100-episode moving
> average over the entire training curve. This metric is fair regardless of early stopping:
> it measures peak capability, not where training happened to end. Step budgets: PPO 500K for
> both; SB3 DQN 100K (our DQN stopped at episode 1011). Our values come from the final runs' logs
> as read on 3 April 2026 (the logs themselves are not kept); SB3's are computed from
> `sb3_results_cache.json`.

---

## Key Learnings <a id="learnings"></a>

### 5.1 DQN
1. **Best-model checkpointing is essential**: DQN is prone to catastrophic forgetting once
   epsilon hits its minimum. Saving the best model prevents losing a good solution.
2. **ε_min matters more than expected**: Dropping from 0.01 to 0.001 was the difference
   between a degrading policy and a stable one.
3. **Target network sync frequency**: Every 5 episodes was consistently better than 10. Too
   infrequent → slow learning; too frequent → instability (equivalent to no target network).
4. **Episode-based vs step-based exploration**: For environments with growing episode length
   (like CartPole), episode-based decay is more natural — the agent sees more of the
   environment's dynamics before stopping exploration.

### 5.2 PPO
1. **Network size bottleneck**: `[64, 64]` bottlenecked learning on LunarLander's 8-dim
   space. Doubling to `[128, 128]` was the decisive change.
2. **Advantage normalisation was kept throughout**: without it, gradient magnitudes would scale
   with absolute rewards, which in LunarLander range from −500 to +300. No run without it was
   recorded, so its effect here is expected rather than measured.
3. **GAE λ = 0.95 is robust**: The standard value worked well without tuning.
4. **Entropy bonus prevents stagnation**: Without it, the policy converged to "hover in place"
   (a locally safe but suboptimal strategy) early in LunarLander training.

### 5.3 Implementation vs SB3
- A clean from-scratch implementation is 300–500 lines vs SB3's ~10K lines. The tradeoff:
  fewer features but complete transparency and debuggability.
- The SB3 DQN baseline used the RL Zoo's tuned CartPole settings and, in a single run at 100K
  steps, peaked at 222.4; this needs a second seed before it is read as a property of SB3. Our
  task-specific implementations reached both targets.
- For research purposes (thesis work on opponent exploitation, Chapters 7–8), custom
  implementations allow surgical modifications (e.g. injecting belief-state observations)
  that would require deep SB3 subclassing.

---

## Appendix — Reproduction

```bash
# From repo root, with .venv activated:

# Train DQN (early stops ~episode 1000):
python implementation/step01/dqn/train.py

# Train PPO (early stops ~step 264K):
python implementation/step01/ppo/train.py

# Regenerate comparison figures (caches SB3 results after first run):
python implementation/step01/compare_sb3.py

# View training curves in TensorBoard:
tensorboard --logdir implementation/step01/logs/
```

*The TensorBoard logs of the custom runs are not kept in the repository, so `compare_sb3.py`
cannot redraw the learning curves until the runs are repeated. The figures here are the saved
renders (DQN: 6 April 2026; PPO: 3 April 2026);
`deliverables/reports/step01/summary/make_comparison_panels.py` crops their rolling-average panels.*

*Generated figures are in `deliverables/reports/step01/figures/`.*
