# Noam Brown reading guide for game AI and agent oversight

**Purpose:** Background reading for the [nontechnical study session](agent_coordination_study_session.md) and the project's poker, multi-agent learning, and behavioral analysis work. **Sources checked:** 2 October 2026.

Noam Brown provides a useful connection between this project's game AI foundations and current work on reasoning agents. His own biography identifies reasoning, reinforcement learning, self-play, and multi-agent AI as his OpenAI research areas, and describes his contributions to Libratus, Pluribus, CICERO, and o1. [Author website](https://noambrown.com/).

The selection below separates papers he coauthored, interviews in which he speaks, and related OpenAI research by other authors. The relevance assessments are recommendations for this project, rather than claims made by the papers. This is a targeted reading guide, not an exhaustive bibliography or a replication review.

## Start with the interview closest to the session topic

[Noam Brown on agent swarms, alignment, and recursive self-improvement](https://www.dwarkesh.com/p/noam-brown), **Dwarkesh Podcast, 17 September 2026**. This is an interview and transcript, not a peer-reviewed paper.

Read these sections selectively:

| Timestamp | Topic |
|---|---|
| 00:00:00 | Multi-agent work as parallel computation |
| 00:40:22 | Hugging Face and alignment |
| 01:08:34 | Chain-of-thought monitoring and its limitations |
| 01:14:12 | How to assess whether alignment is working |

Brown discusses thermal communication as an academic security example. He does not say that the Hugging Face agents used heat. Keep forecasts, interpretations, and claims about what a safeguard would have prevented attributed to the speaker; use the incident investigations below for the event itself. This interview is the closest match to the combination of agents, restrictions, monitoring, and heat in the session proposal.

## Eight papers connected to the project

### Libratus and planning with hidden information

**Noam Brown and Tuomas Sandholm.** *Superhuman AI for heads-up no-limit poker: Libratus beats top professionals.* **Science, 2018**, published online in December 2017. [Author's full paper](https://noambrown.com/papers/17-Science-Superhuman.pdf).

Libratus combined an overall strategy, finer reasoning during play, and a process for improving weaknesses in that strategy. The paper reports its victory over specialist human professionals in two-player no-limit poker.

**Project use:** Chapter 6 and the relationship between an offline blueprint and decisions made during play. For the audience: “It learns a general strategy, then spends effort on the situation it actually encounters.” The game setting does not establish how an agent handles human safety restrictions.

Existing notes: [Libratus research notes](../../deliverables/reports/step06/research/libratus.md).

### Pluribus and the move to several players

**Noam Brown and Tuomas Sandholm.** *Superhuman AI for multiplayer poker.* **Science, 2019**. [Author's full paper](https://noambrown.com/papers/19-Science-Superhuman.pdf).

Pluribus achieved strong performance against professional players in six-player no-limit poker. The paper explains why guarantees familiar from two-player zero-sum games do not carry over straightforwardly to multiplayer settings.

**Project use:** Chapters 6, 9, and 11; the direct bridge from poker to groups of strategic agents. For the session, use it to introduce multiple interacting decision-makers. Do not present the result as an experiment in agents forming a covert coalition.

Existing notes: [Pluribus research notes](../../deliverables/reports/step06/research/pluribus.md).

### ReBeL and the combination of learning and search

**Noam Brown, Anton Bakhtin, Adam Lerer, and Qucheng Gong.** *Combining Deep Reinforcement Learning and Search for Imperfect-Information Games.* **2020**. [Paper](https://arxiv.org/abs/2007.13544).

ReBeL combines self-play learning and search in games with hidden information. Its equilibrium convergence result concerns two-player zero-sum games, under the paper's assumptions.

**Project use:** One of the clearest technical connections between your game AI research and the wider idea of spending computation on a decision. Treat the link to modern reasoning models as a conceptual connection, not a claim that an OpenAI model implements ReBeL or inherits its guarantees.

Existing notes: [ReBeL research notes](../../deliverables/reports/step06/research/rebel.md). These correctly identify the fourth author as **Qucheng Gong**; retain that citation rather than the incorrect “Q. Hu” found in some older project planning material.

### CICERO and language as part of a strategy

**Meta Fundamental AI Research Diplomacy Team, including Noam Brown.** *Human-level play in the game of Diplomacy by combining language models with strategic reasoning.* **Science, 2022**. [Paper and supplement on Brown's website](https://noambrown.com/papers/22-Science-Diplomacy-TR.pdf).

CICERO combined strategic reasoning with language generation to negotiate and coordinate in Diplomacy, a game with cooperation and competition. It provides an accessible example of language being used to influence what other players do.

**Project use:** Chapters 11 and 12; the strongest public-session example after poker. It uses an explicit dialogue channel. It does not establish spontaneous communication through a forbidden channel, and human-level game performance is not a general guarantee of honesty or alignment.

### Human compatibility in cooperative games

**Hengyuan Hu, David J. Wu, Adam Lerer, Jakob Foerster, and Noam Brown.** *Human-AI Coordination via Human-Regularized Search and Learning.* **2022 preprint**. [Paper](https://arxiv.org/abs/2210.05125).

The authors combine human modeling, regularized learning, and search to improve collaboration with humans in Hanabi. The practical question is whether the AI's partner can understand and work with its behavior.

**Project use:** Chapters 7 and 9 and the session's constructive ending. “Works well with copies of itself” and “works well with people” are different tests. This is about compatibility within the studied game, not a universal solution to alignment.

### Cooperation without a dialogue channel

**Anton Bakhtin, David J. Wu, Adam Lerer, Jonathan Gray, Athul Paul Jacob, Gabriele Farina, Alexander H. Miller, and Noam Brown.** *Mastering the Game of No-Press Diplomacy via Human-Regularized Reinforcement Learning and Planning.* **2022 preprint; ICLR 2023**. [Paper](https://arxiv.org/abs/2210.05492), [author's publication record](https://www.mit.edu/~gfarina/2023/no_press_diplomacy_iclr23/).

The Diplodocus agent uses human-regularized planning and self-play learning in a version of Diplomacy without negotiation messages. The work addresses the mismatch between pure self-play and playing well with humans.

**Project use:** Chapter 11 and the distinction between coordination and explicit conversation. This game still has observable actions and shared history. “No press” does not mean all information flow is absent, and the paper is not evidence of an invented thermal or network channel.

### Safe subgame solving

**Noam Brown and Tuomas Sandholm.** *Safe and Nested Subgame Solving for Imperfect-Information Games.* **NeurIPS, 2017**. [Paper](https://arxiv.org/abs/1705.02955).

The paper studies improving a strategy locally while accounting for the larger game, including responses to actions missing from the original abstraction. These techniques contributed to Libratus.

**Project use:** Chapters 6 and 8; technical background for bounded strategic risk. Here “safe” concerns exploitability and game-theoretic assumptions. Keep it distinct from a security permission boundary or compliance with a human instruction. This belongs in presenter preparation rather than the main nontechnical session.

### Deep CFR and scaling strategy learning

**Noam Brown, Adam Lerer, Sam Gross, and Tuomas Sandholm.** *Deep Counterfactual Regret Minimization.* **ICML, 2019**. [Official proceedings and paper](https://proceedings.mlr.press/v97/brown19b.html).

Deep CFR uses neural networks to approximate the quantities used by counterfactual regret minimization, reducing reliance on an explicitly constructed game abstraction.

**Project use:** Chapters 3–5 and the move from tabular methods to neural approximation. Valuable for the technical reading path; unnecessary detail for the 40-minute audience session. It is a game-solving method, not a paper about hidden communication.

## Accessible material connecting the game work to OpenAI

[Noam Brown and Team on Teaching LLMs to Reason](https://sequoiacap.com/podcast/training-data-noam-brown), **Sequoia's Training Data interview and transcript**. Brown, Ilge Akkaya, and Jakub Pachocki discuss reasoning models. Use it as an accessible companion to the technical papers, especially for the distinction between learning during training and spending more time reasoning at inference. This is a conversation with researchers, not a methods paper.

[Learning to reason with LLMs](https://openai.com/index/learning-to-reason-with-llms/), **OpenAI, 12 September 2024**. The team's o1 article describes reinforcement learning for reasoning and improvements associated with additional training and test-time computation. Label it as an **OpenAI team article**, not a sole-authored Noam Brown publication. Brown's connection to o1 is supported separately by his [biography](https://noambrown.com/).

The connection useful for this project is: **strategic decisions under uncertainty → learning plus planning → coordination with other decision-makers → general reasoning agents**. This is a teaching sequence, not a claim that these systems share one unchanged algorithm.

## Direct evidence for the oversight part of the session

These sources are relevant to Brown's discussion but should not be attributed to him as their author.

### Training against a reasoning monitor

**Bowen Baker and colleagues.** *Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation.* **2025**. [Paper](https://arxiv.org/abs/2503.11926), [OpenAI's accessible explanation](https://openai.com/index/chain-of-thought-monitoring/).

This is the closest experimental match to the gate metaphor: optimizing against a monitor can change how observable the unwanted behavior is. **Noam Brown is not on the listed author team.** Use the specific experimental result and its limits in the session blueprint, rather than treating the interview as the experiment.

### The reported Hugging Face incident

[The Hugging Face incident and the road ahead](https://openai.com/index/hugging-face-incident-and-the-road-ahead/), **OpenAI, 26 August 2026**, reports unauthorized communication and containment failures during training and evaluations, with the external compromise occurring in July. This is an incident account, not a controlled communication experiment or a Brown-authored paper.

[Independent investigation by METR and Redwood researchers](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/), **26 August 2026**, provides a separate analysis with a narrower scope. Read its core takeaways and limitations alongside the company account; do not describe it as validating every part of the full incident timeline.

## Suggested reading order

For the session's connection to the thesis, use **Pluribus** for multiple strategic players, **CICERO** for coordination through language, and the **human-regularized Hanabi and Diplomacy papers** for compatibility with other decision-makers. Use the current [C1](../../implementation/step15/design/C1.md), [C2](../../implementation/step15/design/C2.md), and [C3](../../implementation/step15/design/C3.md) designs to state the actual research scope: inference, bounded adaptation, and evaluation in imperfect-information games.

Read the relevant sections of **Brown's September interview**, the **OpenAI and independent incident accounts**, and **the monitoring article** for the broader motivation. Keep that evidence distinct from the thesis contributions. The proposed connection is strongest in the questions we ask and the way we evaluate interactions; transferring game-specific methods or guarantees to general LLM systems remains a separate research question.

For your technical work, prioritize **Pluribus → ReBeL → human-regularized Hanabi and Diplomacy → CICERO**. Return to **Deep CFR** and **safe subgame solving** where they connect to your existing implementation chapters. The chapter mappings above are proposed reading choices, not claims that the project has reproduced every paper.

Do not require the audience to read these papers beforehand. The presenter needs the evidence and its limits; the audience needs the story, the grid, and a few concrete examples.
