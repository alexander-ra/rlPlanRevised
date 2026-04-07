# Step 1 — Reinforcement Learning Basics

**Duration:** 14 days (Tier 2)  
**Dependencies:** None (entry point)  
**Phase:** A — Foundation  

### PhD Connection

This step feeds **Contribution #1 (Behavioral Adaptation Framework)** indirectly: the agent architecture patterns (value networks, policy networks, experience replay) will be reused when building the adaptive opponent model. More directly, this step provides the RL vocabulary and implementation skills needed for every subsequent step.

---

> **Phase Overview:** This phase covers the foundational material required for all subsequent work: reinforcement learning basics (value estimation, policy optimization, experience replay) and game-theoretic fundamentals (extensive-form games, Nash equilibrium computation, and exploitability measurement). A solid command of both domains is essential before proceeding to the more specialized topics of later phases.


## Table of Contents
- [Phase 1: Intuition (1 day)](#phase-1-intuition-1-day)
  - [Videos](#videos)
  - [Blog Posts](#blog-posts)
- [Phase 2: Exploration (2 days)](#phase-2-exploration-2-days)
  - [Day 1: Gymnasium Basics + DQN Demo](#day-1-gymnasium-basics-dqn-demo)
  - [Day 2: PPO on LunarLander + Hyperparameter Exploration](#day-2-ppo-on-lunarlander-hyperparameter-exploration)
- [Phase 3: Targeted Reading (3 days)](#phase-3-targeted-reading-3-days)
  - [Book Chapters: Sutton & Barto — Reinforcement Learning: An Introduction (2nd ed.)](#book-chapters-sutton-barto-reinforcement-learning-an-introduction-2nd-ed)
  - [Paper 1: Playing Atari with Deep Reinforcement Learning (Mnih et al., 2013/2015)](#paper-1-playing-atari-with-deep-reinforcement-learning-mnih-et-al-20132015)
  - [Paper 2: Proximal Policy Optimization Algorithms (Schulman et al., 2017)](#paper-2-proximal-policy-optimization-algorithms-schulman-et-al-2017)
  - [Optional Supplementary Reading](#optional-supplementary-reading)
  - [Math Flags](#math-flags)
- [Phase 4: Implementation (6 days)](#phase-4-implementation-6-days)
  - [Project: DQN + PPO from Scratch on Classic Control Environments](#project-dqn-ppo-from-scratch-on-classic-control-environments)
  - [Sub-phase Breakdown (6 days):](#sub-phase-breakdown-6-days)
  - [Deliverables:](#deliverables)
  - [Validation:](#validation)
- [Phase 5: Consolidation (2 days)](#phase-5-consolidation-2-days)
  - [Day 1 — Reference Skim + Gap Fill](#day-1-reference-skim-gap-fill)
  - [Day 2 — One-Pager + Learning Log](#day-2-one-pager-learning-log)
- [Exit Checklist](#exit-checklist)

## Phase 1: Intuition (1 day)

The goal is to build a mental model of what RL is and why it matters — NO math, NO code, NO papers yet. By end of day, you should be able to explain to a non-expert: "An agent takes actions in an environment, gets rewards, and learns a policy to maximize cumulative reward."

### Videos

- **Reinforcement Learning: Crash Course AI #9**  
  https://www.youtube.com/watch?v=nIgIv4IfJ6s  
  Duration: ~12m | Channel: CrashCourse  
  *Quick, accessible introduction to RL concepts: agents, environments, rewards, exploration vs exploitation. No math, no code — perfect starting point.*

- **Stanford CS234 — Lecture 1: Introduction to Reinforcement Learning (Spring 2024)**  
  https://www.youtube.com/watch?v=WsvFL-LjA6U  
  Duration: ~1h19m | Instructor: Emma Brunskill (Stanford)  
  *University-level introduction to RL: what it is, why it matters, sequential decision making under uncertainty. The most recent Stanford RL course offering.*

- **Stanford CS221 — Lecture 7: Markov Decision Processes (Autumn 2025)**  
  https://www.youtube.com/watch?v=2ZtF1j3n6XE  
  Duration: ~1h20m | Instructor: Percy Liang (Stanford)  
  *Formal MDP framework: states, actions, transitions, rewards, value iteration, policy iteration. The mathematical backbone of everything in this step.*

- **RL Course by David Silver — Lecture 1: Introduction to Reinforcement Learning**  
  https://www.youtube.com/watch?v=2pWv7GOvuf0  
  Duration: ~1h28m | Channel: DeepMind  
  *The classic RL intro lecture. Covers the agent-environment loop, rewards, value functions, exploration vs exploitation, and the RL problem formulation.*

- **Foundations of Deep RL — L1: MDPs, Exact Solution Methods, Max-ent RL**  
  https://www.youtube.com/watch?v=2GwBez0D20A  
  Duration: ~1h30m | Instructor: Pieter Abbeel  
  *More practical / deep RL focused. Covers policy gradients, value functions, model-based vs model-free. Good second perspective after Silver.*

- **Stanford CS230 — Lecture 5: Deep Reinforcement Learning (Autumn 2025)**  
  https://www.youtube.com/watch?v=4E27qlfYw0A  
  Duration: ~1h45m | Instructor: Andrew Ng (Stanford)  
  *Andrew Ng's perspective on deep RL within the broader deep learning landscape. Covers how neural networks are applied to RL problems.*

### Blog Posts

- **Lilian Weng — "A (Long) Peek into Reinforcement Learning"**  
  https://lilianweng.github.io/posts/2018-02-19-rl-overview/  
  *Comprehensive visual walkthrough of core RL concepts with diagrams. Great reference to revisit during Phase 3.*

- **OpenAI Spinning Up — "Key Concepts in RL"**  
  https://spinningup.openai.com/en/latest/spinningup/rl_intro.html  
  *Concise, well-written primer. Covers notation, episodic vs continuing, on-policy vs off-policy.*

---

## Phase 2: Exploration (2 days)

### 🎮 Interactive Exploration
- **[ReinforceJS Gridworld (Andrej Karpathy)](https://cs.stanford.edu/people/karpathy/reinforcejs/gridworld_dp.html)** — Play with Gridworld to understand Dynamic Programming and RL value functions interactively.


See the algorithms work (and fail) before reading the theory. No papers yet — just install libraries, run demos, break things.

### Day 1: Gymnasium Basics + DQN Demo

1. **Install the stack:**
   ```bash
   pip install gymnasium[classic-control,box2d] stable-baselines3[extra] tensorboard
   ```

2. **Run a random agent on CartPole:**
   ```python
   import gymnasium as gym
   env = gym.make("CartPole-v1", render_mode="human")
   obs, info = env.reset()
   for _ in range(1000):
       action = env.action_space.sample()  # random
       obs, reward, terminated, truncated, info = env.step(action)
       if terminated or truncated:
           obs, info = env.reset()
   env.close()
   ```
   *Observe: the cart falls over almost immediately. This is your baseline — random policy.*

3. **Train DQN on CartPole with SB3:**
   ```python
   from stable_baselines3 import DQN
   model = DQN("MlpPolicy", "CartPole-v1", verbose=1, tensorboard_log="./logs/")
   model.learn(total_timesteps=50_000)
   model.save("dqn_cartpole")
   ```
   *Observe: training log shows reward climbing from ~10 to 500 (max). The agent LEARNED.*

4. **Evaluate the trained agent:**
   ```python
   from stable_baselines3 import DQN
   from stable_baselines3.common.evaluation import evaluate_policy
   import gymnasium as gym
   model = DQN.load("dqn_cartpole")
   env = gym.make("CartPole-v1")
   mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
   print(f"Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
   ```

5. **Visualize with TensorBoard:**
   ```bash
   tensorboard --logdir ./logs/
   ```

### Day 2: PPO on LunarLander + Hyperparameter Exploration

1. **Train PPO on LunarLander:**
   ```python
   from stable_baselines3 import PPO
   model = PPO("MlpPolicy", "LunarLander-v3", verbose=1, tensorboard_log="./logs/")
   model.learn(total_timesteps=200_000)
   model.save("ppo_lunarlander")
   ```

2. **Experiment with hyperparameters** — Change ONE parameter at a time, retrain, compare TensorBoard curves:
   - Learning rate: try `1e-4`, `3e-4` (default), `1e-3`
   - Network size: try `policy_kwargs=dict(net_arch=[64, 64])` vs `[256, 256]`
   - Discount factor (gamma): try `0.99` (default), `0.95`, `0.999`
   - Clip range: try `0.1`, `0.2` (default), `0.3`

3. **Watch the trained agent:**
   ```python
   model = PPO.load("ppo_lunarlander")
   env = gym.make("LunarLander-v3", render_mode="human")
   obs, info = env.reset()
   for _ in range(1000):
       action, _ = model.predict(obs, deterministic=True)
       obs, reward, terminated, truncated, info = env.step(action)
       if terminated or truncated:
           obs, info = env.reset()
   ```

4. **Questions to answer by end of Day 2:**
   - Which hyperparameter had the biggest impact on learning speed?
   - Did any hyperparameter change cause training to fail entirely?
   - What's the difference in training behavior between DQN and PPO?

---

## Phase 3: Targeted Reading (3 days)

### Book Chapters: Sutton & Barto — Reinforcement Learning: An Introduction (2nd ed.)

**Link:** http://incompleteideas.net/book/the-book-2nd.html (free HTML/PDF)  
**Assigned chapters:** 1–6 + Chapter 13  
**Context — what comes before:** Nothing — Chapter 1 is the start.  
**Context — what comes after (Ch 7–17):** Ch 7–8 cover n-step methods and eligibility traces (refinements of TD). Ch 9–11 cover function approximation (the bridge to deep RL — you'll encounter this in Steps 5–6). Ch 14–16 cover psychology/neuroscience connections. Ch 17 covers frontiers. *Chapters 7–8 are useful background but not critical for Step 1; function approximation in Ch 9–11 is where the "deep" in deep RL comes from and will be relevant starting Step 5.*  
**Reading focus:**
- **Ch 1–2 (skim, ~1 hr):** Framing and multi-armed bandits. You've seen this in Phase 1 videos. Skim for notation.
- **Ch 3 (read carefully, ~2 hrs):** MDP formulation. This is the formal language for everything that follows. Make sure you understand: state, action, reward, transition, policy, value function, Bellman equation.
- **Ch 4 (read 4.1–4.4, skim rest, ~2 hrs):** Dynamic programming. Policy evaluation, policy iteration, value iteration. These are the "if you had the model" solutions.
- **Ch 5 (read 5.1–5.5, ~2 hrs):** Monte Carlo methods. Model-free learning begins here. First-visit MC, exploring starts.
- **Ch 6 (read carefully, ~3 hrs):** TD learning — the core of modern RL. TD(0), SARSA, Q-learning. This is the chapter that connects to DQN.
- **Ch 13 (read 13.1–13.4, ~2 hrs):** Policy gradient methods — REINFORCE algorithm. This connects to PPO.

### Paper 1: Playing Atari with Deep Reinforcement Learning (Mnih et al., 2013/2015)

https://arxiv.org/abs/1312.5602 (2013 workshop version) / https://arxiv.org/abs/1509.06461 (2015 Nature version)
```
├── READ:  Section 4 (Deep Q-Network architecture), Section 5 (Experiments/Results)
├── SKIM:  Abstract, Section 1 (Introduction), Section 3 (Background — you know this from S&B)
├── SKIP:  Section 2 (Related Work — not needed for Step 1)
├── MATH:  "The loss function (Eq. 3) and target network update rule — understand
│           algorithmically, no proof to work through. The key is WHY a separate
│           target network stabilizes training."
└── KEY INSIGHT: "Combining Q-learning with a deep neural network + experience replay +
    target network makes RL work on high-dimensional inputs (pixels). These three
    tricks are what turned RL from toy problems to Atari."
```

### Paper 2: Proximal Policy Optimization Algorithms (Schulman et al., 2017)

https://arxiv.org/abs/1707.06347
```
├── READ:  Sections 3–5 (Clipped surrogate objective, algorithm, experiments)
├── SKIM:  Abstract, Section 1 (Intro), Section 2 (Background — TRPO context)
├── SKIP:  Appendix (hyperparameter details — useful later for tuning, not for understanding)
├── MATH:  "The clipped objective function (Eq. 7) — understand algorithmically.
│           Why does clipping prevent catastrophically large policy updates?
│           Trace through: if the ratio r(θ) > 1+ε, the gradient is zeroed.
│           No formal proof needed."
└── KEY INSIGHT: "PPO achieves TRPO-like stability with first-order optimization only.
    The clipped objective is the key innovation — simpler, faster, and works
    just as well. This is why PPO became the default policy gradient algorithm."
```

### Optional Supplementary Reading

- **Santana (2025) — "An Introduction to Deep Reinforcement and Imitation Learning"**  
  https://arxiv.org/abs/2512.08052  
  *A recent self-contained introduction (Dec 2025) covering MDP → REINFORCE → PPO. Good for a modern perspective if S&B chapters feel dated. SKIM only — don't read front-to-back.*

- **OpenAI Spinning Up — "Intro to Policy Optimization"**  
  https://spinningup.openai.com/en/latest/spinningup/rl_intro3.html  
  *Excellent companion to Schulman's PPO paper. Cleaner notation and intuitive explanations.*

### Math Flags

No mandatory pen-and-paper proofs for Step 1. The algorithms (Q-learning, REINFORCE, PPO clipping) should be understood algorithmically. The Bellman equations in S&B Ch 3–4 should be understood as definitions, not derived from first principles.

---

## Phase 4: Implementation (6 days)

### Project: DQN + PPO from Scratch on Classic Control Environments

**Language + Framework:** Python 3.10+ / PyTorch 2.x / Gymnasium

| Component | AI Tag | Justification |
|-----------|--------|---------------|
| DQN core: Q-network, experience replay buffer, epsilon-greedy, target network sync | 🔴 HAND-CODE | This is foundational — you must understand every line. The replay buffer indexing, target network copy timing, and epsilon schedule are where the learning happens. |
| PPO core: policy network, value network, GAE computation, clipped surrogate loss, update loop | 🔴 HAND-CODE | Policy gradients are thesis-relevant (Steps 5, 7, 8 build on this). The clipping logic and advantage estimation must be internalized. |
| Gymnasium environment wrappers + reward normalization | 🟢 AI-GENERATED | Standard boilerplate. Must work, but no insight from writing it yourself. |
| Training loop scaffolding (logging, checkpointing, TensorBoard integration) | 🟢 AI-GENERATED | Plumbing code. Focus your time on the algorithms. |
| Plotting: learning curves, reward-per-episode, comparison charts | 🟢 AI-GENERATED | Visualization is important for validation but writing matplotlib code is not where insight lives. |
| Hyperparameter sweep script | 🟡 AI-ASSISTED | AI drafts the sweep structure, you define which parameters to vary and analyze the results. |

### Sub-phase Breakdown (6 days):

**Day 1 — Architecture + Scaffolding:**
- Set up project structure: `step_01/dqn/`, `step_01/ppo/`, `step_01/utils/`
- 🟢 AI-generate: env wrappers, logging utilities, TensorBoard setup
- Design DQN and PPO class interfaces (what methods, what inputs/outputs)

**Days 2–3 — DQN from Scratch:**
- 🔴 Implement: `ReplayBuffer` (circular buffer, sample batch)
- 🔴 Implement: `DQNAgent` (Q-network forward, epsilon-greedy action selection, train step with target network)
- 🔴 Implement: training loop (collect experience → store → sample → update → sync target)
- Train on CartPole-v1. Target: mean reward ≥ 475 over 100 episodes.

**Days 4–5 — PPO from Scratch:**
- 🔴 Implement: `PolicyNetwork` (actor) + `ValueNetwork` (critic)
- 🔴 Implement: GAE (Generalized Advantage Estimation) — Eq. 11 from Schulman et al. (2015) "High-Dimensional Continuous Control Using Generalized Advantage Estimation"
- 🔴 Implement: PPO update step (collect rollout → compute advantages → clipped surrogate loss → multiple epochs of minibatch updates)
- Train on LunarLander-v3. Target: mean reward ≥ 200 over 100 episodes.

**Day 6 — Validation + Benchmarking:**
- Compare your DQN vs SB3 DQN on CartPole (same hyperparameters): learning curves should be similar
- Compare your PPO vs SB3 PPO on LunarLander: learning curves should be similar
- Generate comparison plots (your implementation vs SB3)
- Document: which hyperparameters mattered most? Any bugs encountered during implementation?

### Deliverables:
- [ ] DQN agent solving CartPole-v1 (mean reward ≥ 475/500)
- [ ] PPO agent solving LunarLander-v3 (mean reward ≥ 200)
- [ ] Comparison plots: your implementation vs stable-baselines3
- [ ] Hyperparameter sensitivity notes (learning rate, network size, gamma, clip range)
- [ ] All code committed with clear README

### Validation:
- **DQN:** Compare final trained policy reward against SB3 DQN with identical hyperparameters. Reward curves should converge to similar levels (±10%). If they don't, the bug is likely in the target network update frequency or the replay buffer sampling.
- **PPO:** Compare against SB3 PPO. Check that the clipped surrogate loss decreases over training. If rewards plateau early, check GAE lambda and the number of update epochs.
- **Sanity check:** Both agents should outperform a random policy by >10x on their respective environments.

---

## Phase 5: Consolidation (2 days)

### Day 1 — Reference Skim + Gap Fill

- **Reference skim:** Skim Sutton & Barto Ch 7 (n-step methods) and Ch 9 (function approximation intro) — NOT to learn deeply, but to understand what's coming in later steps and identify any gaps from Phase 3.
- **Optional skim:** Santana (2025) arXiv:2512.08052 if not already read — for a modern unified treatment of DRL and imitation learning as context for later steps.
- Review your Phase 4 code: any components you don't fully understand? Any "it works but I don't know why" moments? Address them now.

### Day 2 — One-Pager + Learning Log

- **Write the mandatory one-pager** (Section 4.7 format). Commit to repo.
- **Initialize the Learning Log** (`learningLog.md`). This is Step 1, so:
  - **Connections:** Note the clear path from tabular Q-learning (Ch 6) → DQN (add neural network) → PPO (switch from value-based to policy-based). This progression continues into Deep CFR in Step 5.
  - **Confusions:** Log any open questions. Common ones for Step 1:
    - "Why does PPO work so much better than vanilla REINFORCE despite being conceptually similar?"
    - "When would you choose DQN over PPO, or vice versa?"
    - "How does experience replay interact with on-policy vs off-policy?"

## Exit Checklist

- [ ] DQN solving CartPole-v1 (mean reward ≥ 475) — validated against SB3
- [ ] PPO solving LunarLander-v3 (mean reward ≥ 200) — validated against SB3
- [ ] Can explain DQN algorithm from memory (Q-network, replay buffer, target network, epsilon-greedy)
- [ ] Can explain PPO algorithm from memory (policy gradient, surrogate objective, clipping, GAE)
- [ ] Can explain WHY target networks stabilize DQN training
- [ ] Can explain WHY clipping prevents catastrophic policy updates in PPO
- [ ] All 🔴 components hand-coded — no AI-generated core algorithm code
- [ ] One-pager written and committed
- [ ] Learning Log initialized (connections + confusions)
- [ ] Step notes committed to repo
