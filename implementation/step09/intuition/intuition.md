# Step 09 — Intuition: Multi-Agent RL

> Phase 1 of Step 09. Mental model only — no proofs, no code. Built on the raw step's
> intuition phase ([`step_09_multi_agent_rl.md`](../../../planning/rawSteps/step_09_multi_agent_rl.md), L46–84, L148–152).

---

## 1. The core idea, in one paragraph

In single-agent RL (Steps 1, 6) the agent learns by trial and error against a **fixed**
world: the environment's dynamics don't care that you're getting better. In Steps 2–8 you
went one level up and computed **equilibria** — strategies that are optimal against a
*perfectly rational* opponent who has already finished thinking. Multi-agent RL (MARL) lives
in between and is harder than both: several agents **learn at the same time in a shared
world**, so from any one agent's point of view the "environment" (which includes the other
agents) **keeps changing** as everyone updates. That is **non-stationarity**, and it breaks
the core assumption behind single-agent RL. It creates two brand-new problems that simply
don't exist for one agent: **coordination** (how do cooperating agents learn to work together
without being told how?) and **credit assignment** (when the team wins, whose actions
mattered?).

---

## 2. A picture to hold in your head

**Learning to dance with a partner who is also learning to dance.** If your partner's steps
were fixed, you could memorize a routine that fits them (single-agent RL). If your partner
were a flawless professional, you could study their known style and prepare the perfect
counter (equilibrium computation). But when *both* of you are beginners improving in real
time, every adjustment you make changes what they should do, and vice-versa. You step on each
other's toes, over-correct, oscillate — until, sometimes, you accidentally lock into a rhythm
(a coordinated equilibrium) and sometimes you keep cycling forever (Matching Pennies). The
whole field is about *stacking the deck so the accidental synchronization happens reliably*.

Three ways the field tames the moving partner:

- **Independent Learning (IL):** pretend the partner is part of the floor. Simple; fails
  exactly because the floor is moving.
- **Centralized training, decentralized execution (CTDE):** during *practice* let a coach see
  both dancers at once (a **centralized critic**); at *showtime* each dancer moves on their
  own. The coach's view is stationary even though each dancer's isn't.
- **PSRO:** keep a *roster* of trained routines, figure out the best *mixture* to rehearse
  against (a game **over routines**), then train one new routine that beats that mixture, and
  add it to the roster. Repeat. This is iterative best response (Step 2) lifted to the space
  of whole policies.

---

## 3. Why single-agent RL breaks here (non-stationarity, precisely)

A single-agent RL agent assumes a **stationary MDP**: `P(s' | s, a)` and `R(s, a)` do not
change over training, which is what makes a fixed optimal value function `Q*` exist to
converge to. In MARL, from agent `i`'s perspective the transition and reward *also depend on
the other agents' policies* `π_{-i}`, which are **changing every update**. So the target
`Q*` that agent `i` is chasing is itself moving — the "ground" shifts under the value
iteration. Consequences you will actually see in the exploration scripts:

- **Cycling instead of convergence** (Matching Pennies): each learner keeps chasing the
  other, tracing loops in strategy space that never settle.
- **Coordination failure** (Stag Hunt): learners drift to the *safe* equilibrium even when a
  better *joint* one exists, because unilateral moves toward it are punished.
- **Equilibrium selection** (Battle of the Sexes): two good pure equilibria exist and the
  learners must somehow agree which — nothing in independent learning breaks the tie.

CTDE and PSRO are two different structural fixes; LOLA is a third (change the *gradient* so
each agent accounts for the other's *upcoming* update).

---

## 4. The menu of approaches (compared)

| Approach | What it does | When you'd reach for it | Main weakness |
|----------|--------------|-------------------------|---------------|
| **Independent Learning (IL)** | Each agent runs its own single-agent RL, treating others as environment. | A quick baseline; near-stationary settings. | Non-stationarity → cycling, coordination failure. It's the *control* that shows why the rest exist. |
| **MADDPG** (CTDE, continuous) | Each agent's **critic** sees *all* agents' obs+actions during training; each **actor** sees only its own obs at execution. | Mixed cooperative-competitive tasks; the canonical CTDE template. | Critic input grows with #agents; off-policy actor-critic is fiddly. |
| **QMIX** (CTDE, value factorization) | Combine per-agent `Q_i` into a joint `Q_tot` via a **monotonic** mixing network so `argmax` decomposes per agent. | Cooperative, discrete, shared-reward (Dec-POMDP). | Monotonicity limits which joint value functions it can represent (no "sacrifice for the team"). |
| **MAPPO** (CTDE, on-policy) | Just PPO with a **centralized value function** `V(global state)` and shared params. | Cooperative MARL where you want a simple, strong baseline. | "Simple" but tuning-sensitive; on-policy sample cost. |
| **PSRO** | Maintain a population of policies; solve a **meta-Nash** over the population; train a **best response** to that mixture; add it; repeat (double oracle). | Competitive/general games; when you want a *game-theoretic* convergence target, not "hope self-play works". | Cost per iteration (a full BR each round); approximate BR oracle weakens guarantees. |
| **LOLA** | Optimize your reward assuming the opponent will take **one learning step**; differentiate *through* their update. | 2-player differentiable games where naive learning fails (IPD). | Assumes you know the opponent's learning rule + can differentiate through it. |
| **Learned communication (CommNet)** | Agents broadcast a **differentiable message**; each receives the **mean** of the others' and feeds it into its policy — the protocol is *learned*, not designed. | Cooperative tasks with partial observability. | Mean aggregation discards *who* said what; less useful in competition. |

Two axes cut across the table:

- **What is centralized, and when?** IL centralizes nothing. CTDE centralizes the *critic /
  value* at **training** only (execution stays decentralized). PSRO centralizes a whole
  *meta-game solve* between training rounds. Communication centralizes *information* at
  execution via a learned channel.
- **Do you model the opponent as static or as a learner?** Equilibrium methods (Steps 2–6)
  and Step 7's opponent model treat the opponent's strategy as *fixed while you respond*.
  **LOLA** is the odd one out: it treats the opponent as a *learner* and anticipates their
  next update — dynamic, not static.

---

## 5. How the idea developed over time

- **2016 — CommNet (Sukhbaatar et al., NeurIPS).** Shows a *learned*, differentiable
  communication channel can emerge from end-to-end training — no one designs the protocol.
- **2017 — MADDPG (Lowe et al., NeurIPS).** The first clean **CTDE** algorithm: centralized
  critics make each agent's world look stationary during training; decentralized actors keep
  execution realistic. The template every cooperative method copies.
- **2017 — PSRO (Lanctot et al., NeurIPS).** Unifies self-play, fictitious play, and the
  double oracle under one **meta-game** framework — the **bridge** from game theory (Steps
  2–8) to MARL (Steps 9–11).
- **2018 — QMIX (Rashid et al., ICML).** Cooperation *through structure*: a **monotonic**
  mixing network that trades expressiveness for **decomposability** (decentralized argmax).
- **2018 — LOLA (Foerster et al., AAMAS).** Cooperation *through look-ahead*: differentiate
  through the opponent's learning step; naive defectors in the Prisoner's Dilemma become
  conditional cooperators.
- **2022 — MAPPO (Yu et al., NeurIPS).** The "surprising effectiveness" result: plain PPO +
  centralized value + shared parameters matches or beats QMIX/MADDPG across many cooperative
  tasks. A cautionary tale about over-engineering.
- **2023–2026 — refinements.** HARL (heterogeneous agents), sample-efficient PSRO, targeted
  communication surveys — smoothing the assumptions QMIX/MAPPO/CommNet make.

The through-line: **learn to talk (CommNet) → centralize the critic (MADDPG) → bring game
theory to a population (PSRO) → factorize the value (QMIX) → look ahead at the opponent's
learning (LOLA) → and then realize the simple thing (MAPPO) often wins** — and, next,
**make any of this work when there is no minimax theorem (N > 2 players — the thesis).**

---

## 6. [P9] The Markov-games bridge (EFG ↔ MARL)

Steps 2–8 reasoned about **extensive-form games (EFGs)**: a game *tree*, **information sets**
grouping histories a player can't tell apart, and **counterfactual values** feeding
regret-based solvers (CFR) that provably converge to a Nash equilibrium in 2-player
zero-sum. Step 9 reasons about **Markov (stochastic) games**, the MARL formalism. Here is the
half-page of notation that connects the two so the switch doesn't feel like starting over.

A **Markov game** is the tuple

$$ \big(\, \mathcal{S},\ \{\mathcal{A}_i\}_{i=1}^{N},\ P,\ \{R_i\}_{i=1}^{N},\ \{\Omega_i\},\ O,\ \gamma \,\big) $$

with states `s ∈ S`, one action set `A_i` per agent, transition
`P(s' | s, a_1,…,a_N)` driven by the **joint** action, per-agent rewards
`R_i(s, a_1,…,a_N)`, and (in the partially observed / Dec-POMDP case) observations
`o_i = O_i(s)`. Each agent has a policy `π_i(a_i | o_i)`; together they form a **joint
policy** `π = (π_1,…,π_N)`. Special cases you already know:

- `N = 1` → an ordinary **MDP** (Step 1).
- `N = 2`, `R_1 = -R_2`, one state → a **matrix game** (this step's testbed).
- Sequential, imperfect-information, zero-sum → an **EFG** (Steps 2–8), which is a Markov game
  whose "state" is a *history* and whose partial observability is exactly an **information
  set**.

**What is preserved across the bridge:**

- *Sequential decisions under uncertainty* — a policy still maps what-you-know to a
  distribution over actions (`π_i(a_i | o_i)` is the Markov-game name for the EFG's
  behavioral strategy at an info set).
- *Partial observability* — the EFG information set becomes the Dec-POMDP observation `o_i`;
  "you can't condition on what you can't see" survives verbatim.
- *Equilibrium as the solution concept* — Nash still means "no agent gains by unilateral
  deviation." PSRO's meta-Nash is Nash *one level up*, over policies.

**What is lost (why you can't just run CFR):**

- *The exact game-tree structure and perfect recall.* CFR's counterfactual decomposition
  needs the tree and perfect recall; general Markov games (loops, simultaneous moves, N > 2)
  don't give you that clean tree, so regret-per-info-set no longer factorizes.
- *Regret-based convergence guarantees.* Outside 2-player zero-sum, CFR's "average strategy →
  Nash" theorem simply does not apply. MARL falls back to gradient/value learning, whose
  convergence is *not* guaranteed (hence cycling).
- *The minimax value anchor.* In 2p zero-sum a Nash strategy guarantees the game value
  against *any* opponent (this is what made Step 8's "safe exploitation" coherent). For
  N > 2 there is **no such single value** — the precise gap Contribution #2 inherits.

So the vocabulary maps cleanly (behavioral strategy ↔ decentralized policy; info set ↔
observation; counterfactual value ↔ centralized critic estimate), but the *guarantees* do
not travel. Steps 9–11 trade CFR's provable convergence for MARL's generality and then try
to buy some of the guarantees back — PSRO via the meta-game, the thesis via structure.

---

## 7. Common misconceptions (easy to get wrong)

- **"Independent learners will converge if I just train longer."** No — in Matching Pennies
  they *cycle* forever; more compute traces bigger loops, not convergence. Non-stationarity
  is structural, not a budget problem.
- **"Self-play always converges to Nash."** Only reliably in 2-player zero-sum with the right
  averaging (and even then it's the *average* iterate, à la CFR/fictitious play, not the last
  one). In general games self-play can cycle or collapse. PSRO exists precisely because
  "hope self-play works" isn't a guarantee.
- **"CTDE means the agents communicate."** No. CTDE centralizes the *critic/value at training
  time*; at execution each actor is on its own with **no** message passing. Communication
  (CommNet) is a *separate* mechanism you add on top.
- **"MADDPG's actor uses the centralized critic at execution."** No — only during training
  (to compute gradients). At execution the actor sees just its own observation; that
  asymmetry *is* the algorithm.
- **"QMIX can represent any team value function."** No — the monotonicity constraint
  (`∂Q_tot/∂Q_i ≥ 0`) forbids cases where one agent's value must *drop* for the team to
  improve (sacrifice plays). It's a deliberate expressiveness-for-tractability trade.
- **"PSRO with a PPO oracle inherits PSRO's convergence guarantee."** The double-oracle
  guarantee assumes **exact** best responses. An approximate (RL) oracle can stall or add a
  weak policy; convergence becomes empirical, not proven.
- **"LOLA is just opponent modeling (Step 7)."** Step 7 infers the opponent's *current*
  strategy; LOLA anticipates their *next learning update*. Static read vs dynamic trajectory
  — different objects, and combining them is a thesis idea, not a solved thing.
- **"Two players and three players are basically the same."** The minimax value anchor that
  every 2p-zero-sum guarantee rests on **does not exist for N > 2** (§6). Three players is a
  different mathematical world.

---

## 8. You should be able to answer

If the intuition has landed, you can explain — to a non-expert — each of these (raw step
L148–152, L500–509):

1. Why is MARL fundamentally different from single-agent RL *and* from equilibrium
   computation? (Non-stationarity: the other agents are learning too.)
2. What is the difference between **independent learning**, **CTDE**, and **PSRO**?
3. Why does QMIX restrict its mixing network to be **monotone**?
4. In self-play, when does the learned strategy converge to Nash and when does it cycle?
5. What is the **double-oracle loop** in PSRO (population → meta-Nash → best response → add)?
6. How does **LOLA's gradient** achieve cooperation where naive learners defect?
7. Where does the **2-player zero-sum assumption** enter, and why does the safety anchor from
   Step 8 vanish for N > 2? (The minimax value; §6.)

---

## 9. Where to build this intuition (from the raw step)

Pointers the raw step recommends for Phase 1 (watch/read; don't study formally yet):

- **Introduction to Multi-Agent RL (MATLAB, ~15m).** Robot-vacuum grid-world intro to
  cooperative vs adversarial agents and non-stationarity.
- **CS224R Lec 4 — Actor-Critic (Finn, Stanford, ~1h).** The actor-critic building block
  under MADDPG and every CTDE method.
- **MADDPG in PyTorch (Machine Learning with Phil, ~2h).** A full CTDE walkthrough.
- **Self-Play (Noam Brown, Cooperative AI Summer School 2024, ~56m).** PSRO + population
  methods in competitive *and* cooperative settings.
- **Amato (2024) — "An Initial Introduction to Cooperative MARL"** (arXiv 2405.06161),
  Sections 1–3 — a gentle conceptual on-ramp if the videos feel fast.
- **Parable of the Polygons** (ncase.me/polygons) — local rules → macro structure, the MARL
  emergence intuition in an interactive.

---

## Key takeaways for the final summary

- **Non-stationarity is THE problem.** Every method in this step is a different structural
  answer to "the other agents are learning while I learn, so my world won't hold still."
- **CTDE = centralize the critic at training, decentralize the actor at execution.** That
  training/execution asymmetry (sharpest in MADDPG, simplest in MAPPO) makes the world look
  stationary to the learner without cheating at showtime.
- **PSRO is the game-theory ↔ MARL bridge.** It runs iterative best response (Step 2) over a
  *population of policies* and solves a **meta-Nash** between them — giving a principled
  convergence target instead of "hope self-play works." Self-play is PSRO with a population of
  one.
- **LOLA reframes the opponent as a learner.** Differentiating through the opponent's update
  is *dynamic* opponent modeling — distinct from Step 7's static read, and a candidate to
  combine with it (Contribution #1).
- **The Markov-games bridge preserves the vocabulary but not the guarantees.** Behavioral
  strategy ↔ decentralized policy, info set ↔ observation, counterfactual value ↔ centralized
  critic — but CFR's convergence and the minimax value anchor do **not** cross into N > 2.
  That missing anchor is exactly the open problem for Contribution #2.
- **Simple often wins (MAPPO).** In cooperative MARL, implementation quality beats algorithmic
  novelty as often as not — worth remembering before over-engineering the thesis's methods.
