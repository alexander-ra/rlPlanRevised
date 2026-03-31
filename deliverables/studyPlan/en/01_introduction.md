# Individual Study Plan

## Research on the possibilities for applying Artificial Intelligence in computer games.

---

> *Superscript numerals (e.g. ^15^) refer to entries in the Glossary at the end of this document.*

## 1. Introduction

### 1.1 Research Context and Significance

Multi-agent systems operating under conditions of imperfect information^5^ represent one of the most challenging and practically relevant areas of artificial intelligence research. In such systems, autonomous agents must make strategic decisions without complete knowledge of the environment state or the intentions of other participants — a setting that arises naturally in cybersecurity (adversarial network defense), financial markets (competing algorithmic traders), autonomous system coordination, and fraud detection.

The mathematical framework for reasoning about such interactions is provided by extensive-form games^4^ with imperfect information, a branch of game theory that models sequential decision-making when players hold private information. Over the past decade, substantial progress has been achieved in computing equilibrium strategies^7^ for large-scale imperfect-information games. Landmark systems include Libratus (Brown and Sandholm, 2017) and Pluribus (Brown and Sandholm, 2019), which defeated professional human players in two-player and six-player poker respectively, as well as more general architectures such as ReBeL (Brown et al., 2020) and Student of Games (Schmid et al., 2023), which unify game-solving approaches across perfect- and imperfect-information domains.

Despite these advances, a critical limitation persists: state-of-the-art systems compute fixed equilibrium strategies that do not adapt to the specific behavioral patterns exhibited by encountered opponents. In practice, real-world adversaries rarely play optimally, and the ability to detect and exploit systematic deviations from equilibrium — while maintaining guarantees against being exploited in return — constitutes a fundamental open problem. This problem, known as safe opponent exploitation^3^, has been investigated primarily in two-player zero-sum^8^ settings. Its extension to multiplayer environments, where coalitions may form and dissolve dynamically, remains largely unexplored in the literature.

The present study plan is organized as a progressive program of fifteen study steps, grouped into seven thematic phases:

- **Phase A — Foundation** (Steps 1–2): Reinforcement learning and game-theoretic fundamentals required by all subsequent work. *(mid-February – mid-March 2026)*
- **Phase B — Scaling the Toolbox** (Steps 3–4): Monte Carlo CFR variants and game abstraction techniques for handling larger game instances. *(beginning of April – mid-April 2026)*
- **Phase C — Neural Methods for Games** (Steps 5–6): Neural network approximations of equilibrium strategies and end-to-end game AI architectures. *(mid-April – end of May 2026)*
- **Phase D — Opponent Modeling and Exploitation** (Steps 7–8): Inference from behavioral traces and safe exploitation algorithms — the thesis-critical core. *(end of May – beginning of July 2026)*
- **Phase E — Multi-Agent Dynamics** (Steps 9–11): Multi-agent reinforcement learning, population-based training, and coalition dynamics in competitive settings. *(beginning of July – mid-August 2026)*
- **Phase F — Data-Driven Approaches** (Steps 12–13): Sequence models and behavioral analysis pipelines connecting theory to real-world data. *(mid-August – beginning of September 2026)*
- **Phase G — Integration** (Steps 14–15): Evaluation framework construction and research frontier mapping. *(beginning of September – beginning of October 2026)*

*The dates above are estimates. An additional month of buffer time is built into the overall plan to accommodate unforeseen adjustments.*

Throughout the study plan, Kuhn Poker^19^ and Leduc Hold'em^20^ serve as the primary implementation testbeds. These games are chosen deliberately as pedagogical vehicles: their small state spaces (12 and approximately 936 information sets, respectively) and known analytical equilibria permit exact verification of every algorithm, while their imperfect-information structure retains the strategic complexity that the thesis demands. By working within well-understood domains, each step concentrates on algorithmic concepts rather than domain-specific engineering, maximizing the volume of theoretical material covered within the allotted timeframe. In later phases, the study plan validates generality beyond poker by applying the developed methods to matrix games, Goofspiel, So Long Sucker^45^, and anonymized real-world behavioral data.

The planned thesis contributions are formulated in domain-agnostic terms — none is specific to poker or to any other single game. The Behavioral Adaptation Framework (Contribution 1) targets arbitrary imperfect-information games; the Multi-Agent Safe Exploitation heuristics (Contribution 2) will be defined over general N-player extensive-form structures; and the Evaluation Methodology (Contribution 3) is intended for cross-domain applicability.

The study plan is aligned with the milestones of the university individual plan. Upon completion of each thematic phase, the corresponding material will be incorporated into Chapter I of the dissertation — covering the state-of-the-art analysis and the formulation of relevance, objectives, tasks, and thesis statements — which is due in November 2026. In this way, the literature review and foundational exposition accumulate incrementally rather than being composed retrospectively. Step 15 produces a detailed Chapter I outline and publication pipeline as its final deliverable.

### 1.2 Research Objective and Expected Contributions

The primary objective of this doctoral research is to develop an adaptive AI agent to be used in various computer games. The agent will start from a safe strategy but will be able to improve its outcome against sub-optimal opponents, thus removing the limitations of previous systems which rarely dynamically adapt their behavior. The research program is structured around three planned contributions:

**Contribution 1 — Behavioral Adaptation Framework.** The goal is to develop a general method for inferring and adapting to opponent strategies from observed action sequences in real time, applicable to arbitrary imperfect-information games. This contribution aims to address the gap between static equilibrium computation and dynamic, opponent-aware play.

**Contribution 2 — Multi-Agent Safe Exploitation.** This contribution will explore tractable heuristic approaches — including KL-regularized exploitation (constraining the exploitative policy to remain close to a safe reference strategy via a Kullback–Leibler divergence penalty) and equal-share baselines — for safe exploitation in small N-player games (three-player Kuhn and Leduc poker variants), seeking to extend existing results from the two-player zero-sum case. The scope is limited to the empirical validation of practical heuristics rather than a general safety theorem for arbitrary N-player settings.

**Contribution 3 — Evaluation Methodology.** The aim is to design a domain-agnostic framework for measuring agent adaptability and robustness across different game environments and opponent populations, with emphasis on identifying failure modes of existing evaluation approaches and demonstrating where standard metrics may provide misleading assessments.

