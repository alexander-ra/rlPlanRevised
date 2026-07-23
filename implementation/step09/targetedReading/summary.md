# Step 09 — Targeted Reading: Multi-Agent RL

> Phase 3 of Step 09. The cropped, VIP-only distillation of the step's sources — the meat
> without the bloat. Built on the raw step's reading list
> ([`step_09_multi_agent_rl.md`](../../../planning/rawSteps/step_09_multi_agent_rl.md),
> L156–336, L461–476).

**Anti-hallucination note.** Equation/section/algorithm numbers below refer to the numbering
in each cited source; glosses are the agent's plain-language readings and the "Math Flags" are
the agent's derivations **to be checked against the PDF**. Only numbers that a source states
are attributed to it; everything else is labeled a prediction or a to-verify. Quotes are kept
to a few words (copyright).

---

## Paper 1 — Lowe et al., "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments" (MADDPG, NeurIPS 2017)

- **Link / role.** arXiv [1706.02275](https://arxiv.org/abs/1706.02275). The original **CTDE**
  algorithm; the template every later cooperative method copies.
- **Key idea (2–4 sentences).** Run DDPG per agent, but give each agent's **critic** access to
  *all* agents' observations and actions during training, while each agent's **actor** sees
  only its own observation. The centralized critic makes the environment look **stationary**
  from the learner's perspective (it can see what everyone is doing), which is precisely the
  cure for non-stationarity; the decentralized actor keeps execution realistic.
- **Key math (by source number).** *Equation 5* — the MADDPG policy gradient for agent `i`:
  $$ \nabla_{\theta_i} J(\mu_i) = \mathbb{E}_{x,a \sim \mathcal{D}}\big[\, \nabla_{\theta_i}\mu_i(a_i\mid o_i)\, \nabla_{a_i} Q_i^{\mu}(x, a_1,\dots,a_N)\big|_{a_i=\mu_i(o_i)} \big]. $$
  The **centralized** action-value $Q_i^\mu(x, a_1,\dots,a_N)$ takes the joint state `x` and
  *all* agents' actions; the **decentralized** deterministic policy $\mu_i(o_i)$ uses only
  `o_i`. That asymmetry between the two arguments *is* CTDE. The critic is trained by the usual
  TD target (their *Eq 6*) using the other agents' current policies.
- **Algorithm (pseudocode gist).** For each step: collect `(x, a, r, x')` into replay `D`; for
  each agent update its centralized critic by minimizing TD error; update its actor by *Eq 5*;
  soft-update targets. (Their Algorithm 1.)
- **Headline result.** MADDPG succeeds on mixed cooperative-competitive MPE tasks
  (cooperative navigation, predator-prey, covert communication) where independent DDPG fails;
  they also add a policy-ensemble trick for robustness (their Section 4.2). *(Cite their
  figures for exact numbers; not reproduced here.)*

---

## Paper 2 — Rashid et al., "QMIX: Monotonic Value Function Factorisation for Deep MARL" (ICML 2018)

- **Link / role.** arXiv [1803.11485](https://arxiv.org/abs/1803.11485). Cooperation **through
  structure**: value factorization for shared-reward Dec-POMDPs.
- **Key idea.** Learn per-agent utilities $Q_i(\tau_i, a_i)$ and combine them into a joint
  $Q_{tot}$ via a **mixing network** whose weights are constrained **non-negative** so the
  mixing is **monotone** in each $Q_i$. Monotonicity guarantees that maximizing each agent's
  own $Q_i$ independently maximizes $Q_{tot}$ — so decentralized greedy execution is
  consistent with the centralized argmax. (Generalizes VDN's *sum* to a state-dependent
  monotone mix.)
- **Key math (by source number).** The **monotonicity constraint** (their Section 3.1):
  $$ \frac{\partial Q_{tot}}{\partial Q_i} \ge 0 \quad \forall i, $$
  enforced by making the hypernetwork emit **non-negative** mixing weights (abs of a linear
  layer), with the global state `s` fed to the hypernetwork (not monotonically) so the mix can
  still depend richly on state. The consequence they state (the **IGM** / decomposability
  property): $\arg\max_{\mathbf a} Q_{tot} = (\arg\max_{a_1} Q_1, \dots, \arg\max_{a_N} Q_N)$.
- **Algorithm (gist).** Recurrent per-agent nets produce $Q_i$; the mixing net (non-negative
  weights from a hypernet over `s`) produces $Q_{tot}$; train end-to-end on the standard
  DQN-style TD loss over $Q_{tot}$.
- **Headline result.** Outperforms VDN and independent Q-learning on **SMAC** StarCraft
  micromanagement. *(Their Section 4 for the win-rate curves.)*
- **Where it breaks.** Monotonicity **cannot** represent joint value functions where an agent's
  utility must *decrease* while the team outcome improves (a coordinated sacrifice / nonmonotone
  interaction). WQMIX / QPLEX target exactly this class. (Raw step's Confusion, L487.)

---

## Paper 3 — Yu et al., "The Surprising Effectiveness of PPO in Cooperative Multi-Agent Games" (MAPPO, NeurIPS 2022)

- **Link / role.** arXiv [2103.01955](https://arxiv.org/abs/2103.01955). The "simple thing
  works" result and the cleanest CTDE baseline.
- **Key idea.** MAPPO is **PPO** with a **centralized value function** `V(s)` over the global
  state (used only to compute advantages during training) and, typically, **shared policy
  parameters**. No new objective; the actor stays decentralized (`π(a_i | o_i)`).
- **Key math.** No new equations — the PPO clipped-surrogate objective from Step 01 carries
  over verbatim (their Section 3). The only change is that the critic input is the global state
  `s` (or agent-specific "centralized" features) instead of `o_i`.
- **Algorithm (gist).** Standard PPO rollout + GAE + clipped update, with `V(s)` centralized
  and parameters shared across homogeneous agents; a handful of implementation details
  (value normalization, input representation, clipping, batch size) matter a lot (their
  Section 5 ablations).
- **Headline result.** Matches or beats QMIX/MADDPG across MPE, SMAC, Hanabi, and GRF with
  **on-policy** learning and modest tuning — the cautionary tale about over-engineering. *(Their
  Section 4 tables for exact numbers.)*

---

## Paper 4 — Foerster et al., "Learning with Opponent-Learning Awareness" (LOLA, AAMAS 2018)

- **Link / role.** arXiv [1709.04326](https://arxiv.org/abs/1709.04326). **Dynamic** opponent
  reasoning: optimize against the opponent's *next learning step*, not their current strategy.
  Thesis Contribution #1.
- **Key idea.** A naive learner maximizes $V^1(\theta^1, \theta^2)$ holding $\theta^2$ fixed.
  LOLA instead assumes the opponent will take **one naive gradient step** and optimizes against
  the *updated* opponent — differentiating **through** that step. This second-order term lets
  each agent *shape* the other's learning, achieving cooperation where naive learning defects.
- **Key math (by source number).** The **LOLA objective / gradient** (their Section 3, ~Eq 4–5):
  agent 1 optimizes
  $$ V^1\big(\theta^1,\ \theta^2 + \Delta\theta^2\big), \qquad \Delta\theta^2 = \eta\,\nabla_{\theta^2} V^2(\theta^1, \theta^2), $$
  and the first-order Taylor expansion gives the extra **look-ahead** term
  $$ (\nabla_{\theta^2} V^1)^\top\, \nabla_{\theta^1}\Delta\theta^2 = \eta\,(\nabla_{\theta^2} V^1)^\top\, \nabla_{\theta^1}\nabla_{\theta^2} V^2, $$
  a **mixed second derivative** (the opponent's update depends on *our* parameters). Dropping it
  recovers naive learning.
- **Algorithm (gist).** Each step: estimate the opponent's naive gradient; assume they apply
  it; compute your gradient of your value at the *look-ahead* opponent parameters (including the
  second-order term); step. (Exact on IPD via the analytic value; policy-gradient estimator
  otherwise.)
- **Headline result.** On the Iterated Prisoner's Dilemma, LOLA–LOLA reaches **tit-for-tat-like
  mutual cooperation**, whereas naive–naive converges to **mutual defection**; on iterated
  matching pennies LOLA stabilizes toward the Nash. *(Their Section 4.)*

---

## Paper 5 — Lanctot et al., "A Unified Game-Theoretic Approach to Multiagent RL" (PSRO, NeurIPS 2017)

- **Link / role.** arXiv [1711.00832](https://arxiv.org/abs/1711.00832). The **bridge** from
  game theory (Steps 2–8) to MARL; the framework for Contributions #2 and #3.
- **Key idea.** Generalize the **double oracle** / iterated best response to policies: keep a
  **population** of policies per player; form the **empirical (meta) game** whose "actions" are
  the population policies and whose payoffs are their head-to-head expected returns; solve its
  **meta-Nash** (a *meta-strategy solver*, MSS); train a new **best response** (the *oracle*,
  via RL) to the opponents' meta-Nash mixture; add it; repeat. Self-play, fictitious play, and
  the independent BR are all **special cases** (their Section 4).
- **Key math / Algorithm (by source number).** **Algorithm 1 (PSRO):**
  1. initialize each population with a (random) policy and fill the meta-payoff tensor `U`;
  2. **repeat:** compute a meta-strategy `σ` from `U` (the MSS — e.g. Nash, or their
     regret-based projected replicator dynamics);
  3. for each player, train an **oracle** best response `π'` to the opponents' `σ`-mixture;
  4. append `π'` to the population and extend `U` with the new match-ups.
  The meta-Nash `σ` is a Nash of a **normal-form game over policies**, not over primitive
  actions.
- **Headline result.** On Kuhn, Leduc, and Liar's Dice, PSRO (and its "deep" MSS variants)
  drives population exploitability down and unifies prior algorithms. *(Their Section 5.)*
- **The caveat that matters for us.** The convergence intuition assumes an **exact** best-
  response oracle. With an approximate RL oracle, each iteration adds only an *approximate* BR;
  convergence becomes empirical (raw step's OPEN question, L487–489; Bighashdel et al. 2026
  targets sample efficiency).

---

## Paper 6 — Sukhbaatar et al., "Learning Multiagent Communication with Backpropagation" (CommNet, NeurIPS 2016)

- **Link / role.** arXiv [1605.07736](https://arxiv.org/abs/1605.07736). Communication as a
  **learned, differentiable** channel — the protocol *emerges* from end-to-end training.
- **Key idea.** Agents share a continuous channel: at each communication step, agent `i` emits
  a hidden vector and **receives the mean** of the others' hidden vectors as extra input. Because
  the whole thing is differentiable, backprop *learns what to say*; no protocol is designed.
- **Key math (by source number).** The **communication update** (their Section 2 / ~Eq 1–3):
  $$ h_i^{t+1} = f^t\big(h_i^{t},\ c_i^{t}\big), \qquad c_i^{t} = \frac{1}{N-1}\sum_{j \ne i} h_j^{t}, $$
  i.e. each agent's next hidden state depends on its own state and the **mean** of the others'
  messages; stacking these modules gives multiple communication rounds.
- **Algorithm (gist).** A single big network with per-agent modules and a mean-pooling
  communication step between layers; trained by standard backprop (or policy gradient) on the
  task reward.
- **Headline result.** Helps on cooperative tasks (traffic junction, combat, bAbI-style),
  beating no-communication and discrete-protocol baselines. *(Their Section 4.)*
- **Limitation.** **Mean** aggregation discards *who* said what — fine cooperatively, weak when
  the source matters (competition). TarMAC / IC3Net add targeted/gated communication (raw step
  Confusion, L490).

---

## Supplementary (skim-level)

- **Zhong et al. (2023) — Heterogeneous-Agent RL (HARL).** arXiv
  [2304.09870](https://arxiv.org/abs/2304.09870). Drops the *homogeneous / shared-parameter*
  assumption QMIX/MAPPO lean on; sequential per-agent updates with a monotonic-improvement
  guarantee (HAPPO/HATRPO). *Role: the "what if agents differ" generalization.*
- **Bighashdel et al. (2026) — Sample-Efficient PSRO with Joint Experience BR.** arXiv
  [2602.06599](https://arxiv.org/abs/2602.06599) (AAMAS 2026). Improves the PSRO oracle's
  sample efficiency by sharing experience across BR computations. *Role: latest PSRO advance;
  bears on the approximate-oracle question.*
- **Wittner (2026) — Communication Methods in MARL (survey).** arXiv
  [2601.12886](https://arxiv.org/abs/2601.12886). A reference map of communication approaches
  (what/when/how). *Role: index for §CommNet follow-ups.*

## Consolidation surveys (raw step L461–470)

- **Shoham & Leyton-Brown (2009), *Multiagent Systems*, Ch. 6–7** ([masfoundations.org](https://www.masfoundations.org/)).
  Learning in games; how the textbook characterizes convergence difficulties (fictitious play,
  no-regret, the folk theorems). Skip Ch. 1–5 (game-theory basics from Steps 2–3).
- **Zhang, Yang & Basar (2021), "MARL: A Selective Overview of Theories and Algorithms."** arXiv
  [1911.10635](https://arxiv.org/abs/1911.10635). The canonical MARL survey. Skim §3
  (cooperative), §4 (competitive), §6 (communication); map each algorithm you built to its
  section.

---

## Worked Math Flags (agent derivations — VERIFY against the PDFs)

Raw step L324–336 marks four as mandatory.

### Flag A — MADDPG centralized-critic gradient (Lowe Eq 5)
**Claim to internalize.** The gradient factorizes into (i) the actor Jacobian
$\nabla_{\theta_i}\mu_i(o_i)$, which uses **only** `o_i`, and (ii) the critic's action-gradient
$\nabla_{a_i} Q_i(x, a_1,\dots,a_N)$ evaluated at the current joint action, which uses **all**
agents. **Why it's the CTDE prototype:** the two factors live in different information regimes
— decentralized actor, centralized critic — and the chain rule glues them. **Sanity check to
run:** with `N=1`, `x=o_1`, this collapses exactly to the single-agent DDPG gradient. If your
implementation's `N=1` path doesn't equal DDPG, the centralization wiring is wrong.

### Flag B — QMIX monotonicity ⇒ decomposability (Rashid §3.1)
**Claim.** If $\partial Q_{tot}/\partial Q_i \ge 0$ for all `i`, then a per-agent greedy
argmax is jointly greedy: $\arg\max_{\mathbf a} Q_{tot} = (\arg\max_{a_i} Q_i)_i$ (IGM).
**One-line proof sketch (to verify):** increasing any $Q_i$ (by picking `a_i`'s local argmax)
can only *increase* $Q_{tot}$ by monotonicity, and the coordinates are independent, so the
joint maximizer is the tuple of local maximizers. **Where it fails:** if some
$\partial Q_{tot}/\partial Q_i < 0$ were allowed, a local increase could *decrease* the joint
value — the "sacrifice" case QMIX cannot represent.

### Flag C — LOLA gradient (Foerster ~Eq 4)
**Claim.** LOLA's extra term over naive learning is the mixed second derivative
$\eta\,(\nabla_{\theta^2} V^1)^\top \nabla_{\theta^1}\nabla_{\theta^2} V^2$. **Derivation to
verify:** Taylor-expand $V^1(\theta^1, \theta^2 + \Delta\theta^2)$ to first order in
$\Delta\theta^2 = \eta\nabla_{\theta^2}V^2$, then take $\nabla_{\theta^1}$; the chain rule on
$\Delta\theta^2(\theta^1)$ produces the second-order term. **Sanity check:** set the
opponent's look-ahead $\eta=0$ and the term vanishes → you must recover naive learning
numerically (the exploration script's `lr_opp=0` knob is exactly this test).

### Flag D — PSRO meta-Nash + BR oracle (Lanctot Alg 1)
**Claim.** The meta-game payoff `U[i][j]` = expected return of population-policy `i` vs `j`;
the MSS returns a Nash `σ` of `U`; the oracle returns
$\arg\max_{\pi} \sum_j \sigma_{-i}(j)\, \mathbb{E}[u_i(\pi, \pi_j)]$. **Key subtlety to
verify (and the crux of the implementation):** the opponent's `σ`-mixture over *behavioral*
policies is realization-equivalent (Kuhn's theorem, perfect recall) to a **single behavioral
policy** obtained by realization-weighted averaging — so an *exact* BR to the mixture can be
computed with the standard best-response engine against that averaged policy. If you average
the mixture *behaviorally without realization weights*, the BR value is wrong. **Check:** on a
2-policy population, the realization-weighted mixture's BR value must equal
$\max$ over hero strategies of $\sum_j \sigma_j\, \text{exact\_value}(\text{hero}, \pi_j)$.

---

## Cross-source synthesis

- **Two axes organize the six papers.** *Cooperative vs competitive*: MADDPG/QMIX/MAPPO/CommNet
  target cooperation (or mixed), PSRO targets general/competitive, LOLA is the mixed-motive
  bridge. *Static vs dynamic opponent*: everyone except LOLA treats the opponent's strategy as
  fixed-while-you-respond; LOLA models the opponent's *learning*.
- **CTDE is one idea with three flavors.** MADDPG centralizes a **per-agent critic**; QMIX
  centralizes a **factorized value** with a structural (monotone) constraint; MAPPO centralizes
  a **single value function** and lets simplicity win. The trend is *less machinery, comparable
  results* — MAPPO's punchline.
- **PSRO is the through-line to the thesis.** It is Step 2's iterated best response lifted to
  policies, with a meta-Nash where CFR's regret bound used to be. Its meta-game is exactly the
  *evaluation methodology* of Contribution #3, and the absence of a population-level safety
  anchor (no minimax for N>2) is exactly the gap of Contribution #2. LOLA is the candidate
  *dynamic* upgrade to Step 7's static opponent model (Contribution #1).
- **Communication is orthogonal.** CommNet plugs into any of the above; it changes *what agents
  observe at execution*, not how they are trained.

---

## Verify when you read it (claims to confirm against the PDFs)

- **MADDPG:** that *Eq 5*'s critic really takes all agents' actions and the actor only `o_i`
  (not a shared centralized actor); and how the critic estimates other agents' policies when
  they are unknown (their Section 4.1 approximation).
- **QMIX:** that monotonicity is enforced via **non-negative mixing weights from a hypernet
  over the state** (not by constraining the state pathway), and that VDN is the *sum* special
  case.
- **MAPPO:** which implementation details their ablations (Section 5) rank as most important
  (value normalization? input? clipping?), since MAPPO's whole thesis is "details > novelty."
- **LOLA:** whether their reported cooperation uses **exact** gradients or the policy-gradient
  estimator, and whether "higher-order LOLA" (LOLA-DiCE) is needed for stability.
- **PSRO:** what MSS they actually use in the experiments (exact Nash vs **projected replicator
  dynamics**), and how they define/measure population exploitability.
- **CommNet:** whether communication is **mean** pooling in all experiments and how many
  communication rounds they stack.

---

## Key takeaways for the final summary

- **MADDPG (Eq 5) is the CTDE prototype:** decentralized actor `μ_i(o_i)`, centralized critic
  `Q_i(x, a_1..a_N)`; collapses to DDPG at `N=1` (the sanity check).
- **QMIX buys decentralized execution with a monotonicity constraint** — powerful and
  restrictive in the same stroke; it cannot represent team sacrifices.
- **MAPPO says simple wins:** PPO + centralized value + shared params matches the fancy
  methods; a caution against over-engineering the thesis.
- **LOLA reframes the opponent as a learner** via a mixed-second-derivative look-ahead term;
  turns IPD defection into cooperation; the dynamic complement to Step 7.
- **PSRO is the game-theory↔MARL bridge:** meta-game over policies + meta-Nash + BR oracle;
  self-play/fictitious-play/DO as special cases; the exact-vs-approximate-oracle gap and the
  missing N>2 safety anchor are the thesis's openings.
- **CommNet: communication can be learned, not designed** (mean-field channel), and it is
  orthogonal to the training paradigm.
- **Every equation and result above is cited by source number and flagged for verification** —
  none are measurements from a run.
