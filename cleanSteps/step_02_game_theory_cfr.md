# Step 2 — Game Theory + CFR Basics

**Duration:** 14 days (Tier 2)  
**Dependencies:** Step 1 (RL Basics)  
**Phase:** A — Foundation

---

## Objectives

Establish foundational competence in game theory and equilibrium computation for imperfect-information games:

1. Master the formal framework of extensive-form games: game trees, information sets, strategies, and solution concepts
2. Understand Nash equilibrium as a solution concept — its definition, existence, and computation
3. Learn the Counterfactual Regret Minimization (CFR) algorithm as the primary method for computing Nash equilibria in two-player zero-sum extensive-form games
4. Implement a complete CFR solver and exploitability evaluator on a canonical benchmark game

---

## Literature

### Textbook

**Shoham, Y. & Leyton-Brown, K. (2008).** *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations.* Cambridge University Press.  
Available: https://www.masfoundations.org/download.html

| Chapters | Topic | Focus |
|----------|-------|-------|
| 3 | Introduction to Game Theory | Normal-form games, strategy profiles, best responses |
| 4 | Computing Solution Concepts | Nash equilibrium definition, mixed strategies, existence theorem |
| 6 | Extensive-Form Games | Game trees, information sets, perfect/imperfect information, subgame perfection |

### Tutorial

**Neller, T.W. & Lanctot, M. (2013).** "An Introduction to Counterfactual Regret Minimization."  
Available: http://modelai.gettysburg.edu/2013/cfr/cfr.pdf  
*Self-contained tutorial (~30 pages) covering regret matching, extensive-form game notation, and the complete CFR algorithm with Kuhn Poker as worked example.*

### Papers

1. **Zinkevich, M., Johanson, M., Bowling, M. & Piccione, C. (2007).** "Regret Minimization in Games with Incomplete Information."  
   arXiv: https://arxiv.org/abs/0709.2092  
   *The foundational CFR paper. Establishes the counterfactual value decomposition and proves convergence in two-player zero-sum extensive-form games.*

---

## Methodology

### Phase 1: Conceptual Foundation (1 day)

Survey of core game theory concepts through structured introductory material: normal-form and extensive-form game representations, Nash equilibrium as a solution concept, the relationship between game theory and multi-agent decision making. Introduction to the concept of regret minimization as a path to equilibrium computation.

### Phase 2: Empirical Familiarization (2 days)

Hands-on experimentation with existing equilibrium solvers using the OpenSpiel framework:
- Execution of CFR on Kuhn Poker, observation of strategy convergence
- Measurement of exploitability across iteration counts
- Manual play and game tree enumeration of Kuhn Poker to build structural intuition
- Exploration of the relationship between convergence rate and iteration count

### Phase 3: Literature Study (3 days)

Structured reading program covering three sources:

1. **Neller & Lanctot (2013):** Complete reading of the CFR tutorial — regret matching fundamentals, extensive-form game notation, the CFR algorithm, and its application to Kuhn Poker. This serves as the primary pedagogical resource.

2. **Shoham & Leyton-Brown, Chapters 3, 4, 6:** Formal game-theoretic foundations — normal-form games and solution concepts (Ch 3–4), extensive-form game representation and information sets (Ch 6).

3. **Zinkevich et al. (2007):** Reference reading of the original CFR paper — counterfactual value definition (Section 3), convergence theorem and algorithm (Section 4). Focus on understanding the convergence bound structure: average overall regret after $T$ iterations is $O\left(\Delta\sqrt{|I|/T}\right)$ where $|I|$ is the number of information sets.

### Phase 4: Implementation (6 days)

From-scratch implementation in Python (NumPy only, no game-solving libraries):

**Kuhn Poker** (3-card deck: J, Q, K; 2 players; 1 betting round) serves as the benchmark game due to its analytical tractability — the Nash equilibrium is known in closed form, enabling precise validation.

| Implementation | Description | Validation Criterion |
|----------------|-------------|---------------------|
| Game engine | Card dealing, action legality, terminal payoff computation | Correct game tree with all 12 deals × action sequences |
| CFR solver | Recursive tree traversal, counterfactual value computation, regret matching, strategy accumulation | Strategy convergence to known Nash equilibrium |
| Best response calculator | Optimal counter-strategy computation against any fixed strategy | Exploitability = 0 at Nash equilibrium |
| Exploitability evaluator | $\text{exploit}(\sigma) = \text{BR}_1(\sigma_2) + \text{BR}_2(\sigma_1)$ | $O(1/\sqrt{T})$ convergence rate on log-log plot |

**Validation approach:** Three-way comparison: (1) implementation output vs known analytical Nash equilibrium for Kuhn Poker, (2) implementation output vs OpenSpiel CFR reference, (3) game value verification ($v_1^* \approx -1/18$).

### Phase 5: Synthesis (2 days)

Consolidation of theoretical and practical knowledge:
- Cross-step connection analysis: linking CFR's information-set decomposition to RL's per-state value updates (Step 1)
- Forward connection mapping to Monte Carlo CFR methods (Step 3) and exploitability as evaluation metric (Step 14)
- Identification of scope limitations: CFR convergence guarantees in 2-player zero-sum vs. N-player settings
- Preparation of step summary document

---

## Deliverables

1. **Kuhn Poker game engine** with complete game tree enumeration
2. **Vanilla CFR solver** converging to Nash equilibrium on Kuhn Poker
3. **Best response and exploitability computation** validated against known equilibrium
4. **Convergence analysis** — exploitability vs iterations plot demonstrating $O(1/\sqrt{T})$ rate
5. **Cross-validation report** — strategy comparison against analytical Nash equilibrium and OpenSpiel reference
6. **Step summary** connecting game theory foundations to the broader research progression

---

## PhD Contribution Alignment

This step provides the game-theoretic framework upon which all three thesis contributions are built:

| Concept | Downstream Application |
|---------|----------------------|
| Information sets + extensive-form representation | Formal language for modeling imperfect-information strategic interactions (all contributions) |
| Nash equilibrium computation via CFR | Baseline strategy from which safe exploitation deviates (Contribution #1, Step 8) |
| Counterfactual value decomposition | Foundation for opponent-specific counterfactual reasoning (Contribution #1, Step 7) |
| Exploitability as evaluation metric | Primary metric in the evaluation methodology (Contribution #3, Step 14) |
| Best response computation | Core subroutine for measuring agent quality throughout the research program |

> **[P6] Sequence-form reading pointer:** When reviewing Step 2 material during Step 8, revisit Shoham & Leyton-Brown Chapter 4 on sequence-form representation. The sequence-form is the mathematical backbone of all LP-based equilibrium and exploitation computation used in Step 8.

---

## Exit Criteria

- [ ] CFR solver produces strategies matching known Kuhn Poker Nash equilibrium to 4 decimal places
- [ ] Exploitability convergence at $O(1/\sqrt{T})$ verified on log-log plot
- [ ] Game value $v_1^* \approx -1/18$ verified
- [ ] Cross-validated against OpenSpiel reference implementation
- [ ] Ability to explain CFR algorithm, information sets, and exploitability from memory
- [ ] Understanding of CFR's convergence guarantees and their limitation to 2-player zero-sum games
- [ ] Step summary completed and committed to repository
- [ ] Connections to Steps 1, 3–8 identified and documented

