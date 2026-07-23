# Step 10 — Intuition: Population-Based Training + Evolutionary Game Theory

> Phase 1 of Step 10. Mental model only — no proofs, no code. Built on the raw step's
> intuition phase ([`step_10_population_training_evo_gt.md`](../../../planning/rawSteps/step_10_population_training_evo_gt.md), L41–79).

---

## 1. The core idea, in one paragraph

Through Steps 2–8 you always computed **one** thing: a single equilibrium strategy (a Nash
strategy, a CFR average, an exploiter). Step 9 kept a **population** of policies but mostly to
find that one equilibrium (PSRO's meta-Nash). Step 10 makes the population itself the object of
study. Instead of training one AI against itself (**self-play**, which can be brittle and
cycle), we train a **whole population of different AIs against each other**: the strong survive,
the weak get replaced by mutated copies of the strong — evolution, but for AI strategies. Two
questions then matter. First, *engineering*: how do you keep the population diverse and
improving (the answer that beat StarCraft II is AlphaStar's **league** with dedicated
**exploiter** agents)? Second, *mathematics*: what does a population of competing strategies
converge to in the long run? That is exactly what **evolutionary game theory** — the
**replicator dynamics** and the **spinning-top decomposition** — was built to answer.

---

## 2. A picture to hold in your head

**A dojo, not a duel.** Self-play is one fighter shadow-boxing a mirror: they get very good at
beating *themselves*, and blind to styles they never see. A **league** is a whole dojo. There
are **main students** who spar against everyone (they must become well-rounded), **specialist
sparring partners (main exploiters)** whose entire job is to find and punish one student's bad
habit, and **generalist troublemakers (league exploiters)** who probe everyone for holes. Every
so often you **photograph** a student's current form and add the photo to the wall (a *frozen*
opponent), so students must keep beating their past selves. And periodically the weakest
students **copy a champion's technique and tweak their training routine** (PBT's exploit +
explore). No coach hand-designs a curriculum — the dojo *self-organizes* into a difficulty
ladder.

Evolutionary game theory is the physics of that dojo: if you just watched the *proportions* of
each style in a huge population drift over time, the **replicator equation** predicts where they
head — sometimes to a stable mix (an **ESS**), sometimes round and round forever (rock-paper-
scissors).

---

## 3. Why self-play needs a population (non-transitivity, precisely)

Self-play assumes that "getting better" is a ladder: if I beat the strategy that beat me, I've
climbed. That is only true when the game is **transitive** — when there is a real skill order
A > B > C. Many interesting games have a **non-transitive** (cyclic) component: A beats B, B
beats C, **and C beats A** (rock-paper-scissors). In the cyclic part, beating your last opponent
does **not** mean you improved — you just *rotated*. Self-play in such a game can cycle forever,
each new strategy beating the previous one while losing to an older one it has forgotten. The
fixes all amount to **remembering a diverse population**: PSRO keeps every past best response;
the league keeps frozen snapshots and adds exploiters so no single style can dominate unchecked.

The diagnostic that makes this precise is Balduzzi's **spinning top**: every competitive payoff
matrix splits into a **transitive** part (a genuine skill ranking) and a **cyclic** part (pure
RPS). The transitive ratio ‖T‖/‖A‖ tells you how much of "getting better" is real vs illusory.
Leduc leans transitive (self-play mostly works); the coalition games of Step 11 are predicted to
be heavily cyclic (self-play will cycle — you'll *need* the diversity machinery).

---

## 4. The menu of approaches (what each does, when to reach for it, its weakness)

| Approach | What it does | Reach for it when | Main weakness |
|---|---|---|---|
| **Single self-play** | One agent trains against copies of itself | The game is transitive and you want a cheap strong agent | Cycles / overfits on non-transitive games; blind to unseen styles |
| **PSRO** (Step 9) | Grow a population of best responses; play the meta-Nash mixture | You have an exact/approx best-response oracle and want a principled equilibrium over policies | Population weight concentrates on a few policies (diversity collapse); exact oracle is slow on big games |
| **PBT** (Jaderberg 2017) | A population co-evolves weights **and** hyperparameters in parallel (exploit + explore) | You want automatic hyperparameter tuning + a diverse opponent set at once | Naive PBT alone still collapses to one style on hard games |
| **AlphaStar league** (Vinyals 2019) | PBT + three agent roles (main / main-exploiter / league-exploiter) + frozen history + prioritized matchmaking | You need robustness to *diverse* opponents in a large game | Heuristic safety only — **no formal guarantee** the main agents can't become exploitable (the Contribution-#2 gap) |
| **Replicator dynamics** (Hofbauer–Sigmund) | The ODE of population proportions under fitness-proportional selection | You want to *predict/analyze* where a population heads (Nash? ESS? cycle?) | It's an analytical lens on a *fixed* game; real training changes the game (non-stationarity) |
| **EGTA** (Tuyls 2018) | Build an empirical game over a finite policy set; its Nash approximates the true Nash | You want to *evaluate* a population (multi-agent generalization of exploitability) | Needs the O(n²) payoff matrix between policies; approximation quality depends on the sample |

---

## 5. How the field got here (a dated lineage)

- **1973–78 — Maynard Smith & Price / Taylor & Jonker: ESS + replicator dynamics.** Game
  theory meets biology: an equilibrium is a population no mutant can invade; the replicator
  equation is its dynamics. *Fixed what before it:* gave "equilibrium" a *dynamical* meaning
  (an attractor), not just a static fixed point.
- **1998/2003 — Hofbauer & Sigmund: Evolutionary Game Dynamics.** The canonical synthesis
  linking replicator dynamics, Nash, and stability. *Fixed:* unified the zoo of results into one
  framework (fixed points ↔ Nash, attractors ↔ ESS).
- **2017 — Jaderberg et al.: Population-Based Training.** Turn hyperparameter tuning into
  evolution: a population trains in parallel; the weak copy the strong (exploit) and perturb
  (explore). *Fixed:* the sequential "train → tune → retrain" loop; found better configs with
  less compute.
- **2018 — Jaderberg et al.: FTW (Capture the Flag).** PBT in a real multiplayer game; the
  population *is* a curriculum, and Elo *is* the meta-game readout. *Fixed:* showed PBT yields
  human-level cooperation/competition with no hand-designed curriculum.
- **2018 — Tuyls, Pérolat, Lanctot et al.: generalized EGTA.** A principled way to analyze a
  multi-agent system as a game over a *finite* strategy set, with approximation bounds. *Fixed:*
  gave population evaluation a theoretical footing (and PSRO its convergence rationale).
- **2019 — Balduzzi et al.: spinning top / open-ended learning.** The transitive+cyclic
  decomposition and rectified PSRO. *Fixed:* explained *why* self-play cycles (the cyclic
  component) and how to add only genuinely-improving policies.
- **2019 — Vinyals et al.: AlphaStar league.** Three agent roles + frozen history + Nash
  matchmaking beat StarCraft II. *Fixed:* PSRO/PBT diversity collapse at scale, via
  artificial selection (exploiters).

---

## 6. Common misconceptions ("easy to get wrong")

- **"If I beat the thing that beat me, I got better."** Only in the transitive component. In the
  cyclic component you merely rotated (RPS). The spinning-top ratio is how you tell.
- **"More compute makes RPS-like games converge."** No — the replicator orbit on RPS is a
  *centre*; it circles forever regardless of step count. You need a *different* method
  (population diversity), not more of the same.
- **"The league's exploiters make it *safe*."** They make it *robust in practice* (heuristic
  selection pressure). There is **no theorem** that main agents stay non-exploitable — that
  missing guarantee is precisely thesis Contribution #2.
- **"Replicator dynamics = the learning algorithm."** They're an *analytical model*; many
  learning rules only *approximate* replicator dynamics, and they assume a fixed payoff matrix,
  whereas real training is non-stationary (the game changes as agents learn).
- **"Elo is an absolute skill number."** Elo is *relative* and only well-defined up to the
  population it was computed on; in a purely cyclic population everyone's Elo is roughly equal
  (there's no transitive skill to rank).
- **"A single agent is enough if it's the meta-Nash."** The **meta-Nash mixture over a diverse
  population** is (predicted to be) less exploitable than any single agent — mixing is the point.

---

## 7. "You should be able to answer …" (self-check)

1. What do the **fixed points** of the replicator dynamics correspond to, and what extra
   property makes one an **ESS**?
2. Why does the replicator dynamics **converge** on Prisoner's Dilemma and Hawk-Dove but
   **cycle** on Rock-Paper-Scissors?
3. State the **spinning-top decomposition** in words. If a game's transitive ratio is near 0,
   what does that predict for naive self-play?
4. Name AlphaStar's **three agent roles** and say, for each, *who it trains against* and *why*.
5. What are PBT's **exploit** and **explore** operations, and what problem do they solve at once
   for multi-agent training?
6. What is the **meta-Nash of the empirical game**, and why is it a better *evaluation* target
   than "how good is my single agent"?
7. Where is the **formal safety gap** in the league design, and which thesis contribution aims to
   close it?

---

## Key takeaways for the final summary

- **Population, not point.** Steps 2–8 computed one strategy; Step 10 maintains and evolves a
  *population*. Robustness comes from diverse opponents, not a single self-play mirror.
- **Non-transitivity is the enemy of self-play.** The cyclic component of a game makes
  "improvement" illusory; the spinning-top ratio measures it, and Leduc is mostly transitive
  while FFA (Step 11) is predicted to be heavily cyclic.
- **AlphaStar's league = artificial selection.** Main / main-exploiter / league-exploiter roles
  + frozen history + PFSP matchmaking keep a population diverse and honest — the population-level
  analog of Step 7 opponent modeling and Step 8 safe exploitation, but with only *heuristic*
  safety (the Contribution-#2 gap).
- **Replicator dynamics = the analytical lens; EGTA = the evaluation lens.** Fixed points ↔
  Nash, attractors ↔ ESS, cycles ↔ non-transitivity; the meta-Nash of the empirical game is the
  multi-agent generalization of exploitability (Contribution #3).
- **PBT does two jobs at once:** co-evolve weights and hyperparameters, giving both automatic
  tuning and a built-in diverse opponent set.
