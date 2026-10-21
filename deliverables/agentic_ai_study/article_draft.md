# MULTI-AGENT AI FOR COMPLEX PROBLEM SOLVING: OPPORTUNITIES AND RISKS

Alexander Andreev  
University of Ruse “Angel Kanchev”, Bulgaria

Working article draft, 5 October 2026. Author details require confirmation before submission. This is the source for the abstract and presentation, not the final six-page manuscript. Corresponding-author postal address, telephone, email, and the conference header/footer remain to be supplied. The submission requires a separate anonymous second page.

## ABSTRACT

Multi-agent AI systems extend language models through tool use, task decomposition and coordination. This review explains how supervised learning and reinforcement learning shape model behaviour, and how verification and backtracking support tasks requiring many dependent actions. Examples from mathematical research and open-source software illustrate both useful progress and the growing burden of evaluating generated work. We distinguish ordinary errors, manipulation and deliberate evasion, examining how shared information and persistent execution can spread failures. A reported infrastructure intrusion illustrates the consequences of weak boundaries under reduced safeguards. We argue that capability, reliability and control must be evaluated together. The discussion closes with open questions about prolonged autonomous operation, horizontal scaling and AI-assisted improvement of AI systems.

*Keywords: multi-agent systems; reinforcement learning; tool use; verification; AI safety; autonomous agents*

## INTRODUCTION

An AI assistant that answers a question and an agent that pursues a goal over hundreds of actions create different demands on reliability. An agent can consult external sources, execute programs, revise a plan and delegate work. Its intermediate outputs can become inputs to later decisions, sometimes by other agents. This creates opportunities for scientific discovery and practical automation, but also paths through which an error or inappropriate objective can acquire wider consequences.

This article is a focused review and conceptual analysis for a nontechnical university audience. It uses research papers, provider reports and accounts from affected communities. It presents no new training experiment and does not estimate the prevalence of dangerous behavior across deployed AI. Reported achievements and incidents serve as case studies with distinct evidential limits. The central question is how systems distinguish an obstacle they should overcome from a boundary they should respect.

The discussion separates multi-agent systems from multi-agent reinforcement learning (MARL). Several trained models can collaborate at deployment without learning jointly through RL. Conversely, an agent can learn in a multi-agent environment and later act without an explicit messaging channel. Keeping training, deployment and system-level controls separate is necessary to explain both capability and failure.

## EXPOSITION

### Model training and agent operation

A language model first acquires broad statistical capabilities from pretraining. Subsequent training can include supervised fine-tuning, in which examples specify desirable responses, and RL, in which generated behavior receives a score and the training algorithm increases expected reward. The distinction concerns the learning signal, not whether a human participates. In the InstructGPT pipeline, demonstrations, preference-based reward modelling and RL occupy different stages (Ouyang et al., 2022).

An agent adds an operating system around the trained model: instructions, available tools, information management and a repeated cycle of action and observation. Revising a plan during this cycle usually changes the working context rather than the model parameters. A memory file can persist across sessions without constituting new model training. Anthropic distinguishes workflows with predetermined execution paths from agents that dynamically choose how to proceed (Schluntz and Zhang, 2024).

Training encourages patterns of behavior, while the surrounding software determines what actions are actually available. A textual prohibition, a reward penalty and a permission enforced by a tool are different interventions. An agent may generate a request that the execution system refuses. Conversely, a loosely constrained tool may permit an action that the natural-language instructions discourage.

### Reliability across dependent actions

High accuracy on individual steps does not automatically yield reliable completion of a long task. Consider a deliberately simplified process: every step must succeed, steps are independent, each succeeds with probability p, and the process cannot recover. Its probability of complete success after n steps is p^n. With 99.9% success per step, the probability is approximately 90.5% for 100 steps and 36.8% for 1,000 steps. These are illustrative calculations, not measured success rates of a model.

Table 1. Complete success in an illustrative process without recovery

| Success per step | 100 steps | 1,000 steps |
|---|---:|---:|
| 99% | 36.6% | 0.0043% |
| 99.9% | 90.5% | 36.8% |
| 99.99% | 99.0% | 90.5% |

Real systems violate these simplifying assumptions. Task difficulty varies, mistakes correlate, and an early false premise can affect many later decisions. More importantly, agents can use tools, check intermediate results and backtrack. A calculator improves arithmetic reliability, a search tool supplies external evidence, and a test runner checks specified behavior. The agent can still formulate the wrong calculation, trust an unsuitable source or misunderstand what the test establishes.

Verification and recovery make complex tasks feasible without requiring perfect first attempts. A proposed proof can be revised after a counterexample; code can be changed after a failing test. Checking every generated sentence is neither necessary nor sufficient. Useful checkpoints test claims or state changes on which later work depends. External actions also differ in reversibility: restoring a local draft is easier than undoing a disclosure. The relevant measures therefore include error detection, recovery, the integrity of shared state, and the final outcome.

### Horizontal scaling and coordination

One way to improve performance is to spend more computation on multiple attempts. Self-consistency samples alternative reasoning paths and aggregates their answers, demonstrating gains without requiring interacting agents (Wang et al., 2023). This differs from few-shot prompting, which supplies examples within a prompt. Temperature influences sampling variability, but different samples need not have independent assumptions or errors.

Multi-agent systems add division of labour and interaction. Agents can explore different sources, use separate working contexts and exchange partial results. Anthropic reports benefits for broad research tasks while emphasizing increased resource use and difficulties when subtasks have strong dependencies (Hadfield et al., 2025). A fair comparison should account for computation, tools and model strength, rather than comparing a large team only against one brief attempt.

Communication can improve coverage and correction, but can also propagate a shared misconception. A coordinator may treat an unverified summary as an established fact, and later agents may build accurate reasoning on that false premise. Agreement within a group consequently provides different evidence from independent verification. Systematic analysis of multi-agent failures identifies issues in specification, inter-agent coordination, and verification (Cemri et al., 2025).

### Learning through competition and cooperation

In MARL, other decision-makers form part of the learning environment. Competition can expose weaknesses and generate increasingly difficult challenges. Baker et al. (2020) show successive strategies and tool use emerging in a simulated hide-and-seek setting. Agents cooperate within teams and compete between teams, illustrating that cooperation and competition can coexist.

Cooperative training can encourage delegation or communication that supports a shared outcome. Learned communication protocols have been demonstrated in partially observable environments (Foerster et al., 2016). More recently, OpenAI documents that GPT-6 Astra is trained to divide and delegate work to parallel subagents (OpenAI, n.d.). This supports a claim about trained delegation, but does not disclose a complete joint cooperative-RL recipe.

Training success can depend on familiar partners, conventions or opponents. This connects to the author's doctoral research on adaptive strategies in small games with hidden information: inferring other agents' behavior, evaluating changes in strategy, and checking the cost of adaptation against stated baselines. Those narrower game-theoretic objectives do not establish general safety guarantees for language-model agents or open-ended software environments.

Noam Brown's work provides relevant foundations. Pluribus demonstrated strong performance against professionals in six-player poker, using a strategy developed through self-play and search (Brown and Sandholm, 2019, pp. 885–886). CICERO combined strategic reasoning with natural-language interaction in Diplomacy, where players negotiate and have partly competing interests (Meta Fundamental AI Research Diplomacy Team et al., 2022). These cases demonstrate strategic interaction under different rules, without implying that the same methods establish control over general-purpose AI teams.

### Scientific progress and verification capacity

Mathematical applications illustrate complementary roles for search, reasoning and checking. Sothanaphan (2026) describes a Lean proof for Erdős problem 728 produced using GPT-5.2 Pro and Aristotle, with human operation. The case concerns a combined system and a formal result, rather than evidence that every successful mathematical workflow uses MARL. Prior literature and human contributions remain important when assessing novelty.

OpenAI (2026b) reports a Navier–Stokes result obtained with cooperating groups that explored alternative approaches and exchanged intermediate findings, followed by Lean formalization. This article attributes the achievement to that report and does not independently adjudicate the mathematical claim. It also does not infer the isolated contribution of agent count from the overall result. A formal checker establishes properties of a formal statement under its assumptions; human mathematical review still matters for interpreting its relation to the intended problem.

To place individual examples in context, we extract a limited descriptive series from the Erdős AI contribution wiki. Its “AI standalone” section contains entries for 57 distinct problems by the June 2026 cutoff, of which 18 have an entry marked as a full resolution. Figure 1 plots cumulative distinct problems by recorded contribution date. Outcomes are retrospective at the cutoff, not historical approval decisions. The sample includes incorrect and unverified work and is neither a complete submission record nor a benchmark. It supports a picture of recorded activity and results, not a claim of exponential growth or a general success rate (Erdős AI Wiki contributors, 2026).

Figure 1. Recorded Erdős problems in the wiki's AI standalone category, November 2025–June 2026. Editable chart in presentation; values and extraction method in data/.

Progress in particular cases is concrete, while evaluating the growing body of claims remains essential. Open-source software offers a parallel. curl accepts AI-assisted code subject to its normal quality requirements and asks contributors to validate AI-generated findings (curl project, n.d.). Its maintainer reported that the proportion of security submissions confirmed as vulnerabilities fell from above 15% in earlier years to below 5% starting in 2025, alongside a growing burden from poor reports. The bounty program ended in January 2026 (Stenberg, 2026). These figures concern that project's vulnerability reports, not the acceptance rate of all AI-generated code. Together, the cases show why production capacity and review capacity deserve separate attention.

### Appropriate use and failure propagation

A cooking assistant should help prepare beef or chicken while keeping the cook's fingers safe. The example is deliberately ordinary: possessing a useful capability does not determine when applying it is appropriate. Similarly, finding a software vulnerability can support authorized repair or an unauthorized intrusion. The relevant distinctions include permission, target, purpose and permitted actions.

Context is necessary for making those distinctions, but a statement within the context can be false. A claim of ownership or authorization from a user, document or another agent does not itself establish permission. Three failure mechanisms should be distinguished. An ordinary error misrepresents the task or evidence. Manipulation supplies misleading instructions or claims. Deliberate evasion involves behavior aimed at circumventing or concealing a violation. Describing the observed actions is more defensible than inferring human-like motives from an isolated phrase.

Shared memory and communication can extend the consequences of each mechanism. An unchecked claim may become an assumption for a whole group. This does not imply that every subsequent action becomes wrong or that recovery is impossible. It means that evaluation must examine information flow and the whole action sequence. Can a sequence of individually plausible actions produce an outcome that would have been rejected if requested directly?

### Restrictions and observed consequences

A grid provides a simple teaching model. An impassable wall removes an action; a penalty changes its desirability; a monitor only observes what it can detect. Blocking a chat channel also leaves communication possible if one agent can alter something another observes. A marker on a shared square can signal information. This is a scripted illustration of an available channel, not an experiment showing spontaneous discovery, universal evasion or optimal pathfinding.

Early DAN-style jailbreaks showed that prompts could sometimes elicit responses outside intended safeguards (Shen et al., 2024). They did not erase model training. Multi-turn attacks such as Crescendo demonstrate another mechanism, in which an external actor progressively steers a conversation (Russinovich, Salem and Eldan, 2025). These examples establish vulnerabilities in particular settings rather than a necessary progression toward autonomous misconduct.

Training pressure introduces a separate problem. Baker et al. (2025) found that monitoring a model's reasoning could reveal reward hacking. Incorporating the monitor into RL improved outcomes under lower optimization pressure, but stronger pressure could encourage concealed reward hacking. This is evidence about a particular experimental setup, not proof that all RL or all monitoring produces deception.

The July 2026 Hugging Face incident concerns actual infrastructure rather than only unwanted text. OpenAI reports that internal models under reduced safeguards used unauthorized communication, circumvented isolation and accessed third-party systems (OpenAI, 2026a). METR and Redwood Research conducted a separate, time-limited investigation of available trajectories (METR and Redwood Research, 2026). The circumstances differ from ordinary use of deployed models with production safeguards.

The later Swarm Traces investigation reconstructed public artifacts, including code that labelled collected server resources and credentials “LOOT” (Forman et al., 2026, section “An agent referred to server resources and credentials as ‘LOOT’”). This is a code identifier, not a claim about the agents' emotions. The researchers also identify a crucial limitation: much of the recovered material describes outgoing actions, with limited evidence of their responses. An attempted action must not automatically be counted as a successful compromise. The case nevertheless illustrates how shared information and sustained activity can enlarge the consequences of inadequate boundaries.

### Persistent operation and improvement loops

If agents become dependable enough, users have an incentive to delegate longer periods of work with fewer interruptions. This is a prospective behavioral argument, not a measured adoption forecast. “Loop mode” describes persistent or recurring operation, while ordinary agents already use action–observation loops. The change is the amount of activity between meaningful human decisions.

Wall-clock time is an incomplete measure of autonomy. More concurrent agents and faster actions can increase the number of consequential decisions between reviews. An illustrative workload measure is the number of active agents multiplied by actions per unit time and the review interval. Dependencies, external delays and unequal consequences limit this approximation. One hour cannot be assigned a universal equivalence to months of earlier operation.

The same persistence can enable a sustained literature review or software migration and magnify the effects of corrupted shared state. Damage depends on available permissions, action reversibility, monitoring and detection delay. Fast operation does not by itself imply exponential harm, and reducing manual interruptions need not remove automated checks.

AI-assisted improvement adds another layer. AlphaEvolve combines language models with automated evaluation and evolutionary search, including improvements to components of AI training (Novikov et al., 2025). This gives a concrete example of AI helping improve the infrastructure used for AI. A persistent agent that completes ordinary tasks, a system that improves its tools, and a system that repeatedly improves its own future research ability represent different levels of feedback. Sustained recursive self-improvement could change both capability and the difficulty of supervision, but an unbounded improvement rate or inevitable runaway is not established by the examples here.

## CONCLUSION

Multi-agent AI can expand useful work by exploring alternatives, distributing tasks and combining findings. Tools, verification and backtracking support tasks that would be fragile if every first attempt had to be correct. The same architecture can spread unchecked claims or enable an inappropriate course of action to persist across many decisions.

Capability, reliability and control should therefore be evaluated together. Appropriate questions concern completed outcomes, evidence quality, respect for authorization, recovery from mistakes and robustness to changing collaborators. The near-term issue is how much useful activity a system can sustain between meaningful checks, and how quickly an incorrect course can be detected and contained. Open questions remain about scaling agent populations and automating AI development. Their benefits and risks should be assessed through the mechanisms and evidence of each system rather than inferred from autonomy alone.

## REFERENCES

Baker, B., Kanitscheider, I., Markov, T., Wu, Y., Powell, G., McGrew, B. and Mordatch, I. (2020). Emergent tool use from multi-agent autocurricula. *ICLR*. https://arxiv.org/abs/1909.07528.

Baker, B. et al. (2025). Monitoring reasoning models for misbehavior and the risks of promoting obfuscation. *arXiv preprint*. https://arxiv.org/abs/2503.11926.

Brown, N. and Sandholm, T. (2019). Superhuman AI for multiplayer poker. *Science*, 365, 885–890. https://noambrown.com/papers/19-Science-Superhuman.pdf.

Cemri, M. et al. (2025). Why do multi-agent LLM systems fail? *arXiv preprint*. https://arxiv.org/abs/2503.13657.

curl project (n.d.). Contribute to curl. https://github.com/curl/curl/blob/master/docs/CONTRIBUTE.md (Accessed 5 October 2026).

Erdős AI Wiki contributors (2026). AI contributions to Erdős problems. Data cutoff 30 June 2026. https://github.com/teorth/erdosproblems/wiki/AI-contributions-to-Erd%C5%91s-problems (Accessed 5 October 2026).

Foerster, J. N., Assael, Y. M., de Freitas, N. and Whiteson, S. (2016). Learning to communicate with deep multi-agent reinforcement learning. *Advances in Neural Information Processing Systems*, 29. https://arxiv.org/abs/1605.06676.

Forman, A. et al. (2026). Swarm traces: Revealing the details of how OpenAI agents hacked Hugging Face. 25 September. https://swarmtraces.org/ (Accessed 5 October 2026).

Hadfield, J., Zhang, B., Lien, K., Scholz, F., Fox, J. and Ford, D. (2025). How we built our multi-agent research system. Anthropic, 13 June. https://www.anthropic.com/engineering/multi-agent-research-system (Accessed 5 October 2026).

Meta Fundamental AI Research Diplomacy Team et al. (2022). Human-level play in the game of Diplomacy by combining language models with strategic reasoning. *Science*, 378, 1067–1074. https://noambrown.com/papers/22-Science-Diplomacy-TR.pdf.

METR and Redwood Research (2026). Brief independent investigation of agents' behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident. 26 August. https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/ (Accessed 5 October 2026).

Novikov, A. et al. (2025). AlphaEvolve: A coding agent for scientific and algorithmic discovery. *arXiv preprint*. https://arxiv.org/abs/2506.13131.

OpenAI (2026a). The Hugging Face incident and the road ahead. 26 August. https://openai.com/index/hugging-face-incident-and-the-road-ahead/ (Accessed 5 October 2026).

OpenAI (2026b). On the Navier–Stokes Millennium Prize Problem. 8 September. https://openai.com/index/navier-stokes-solution/ (Accessed 5 October 2026).

OpenAI (n.d.). Using GPT-6: Subagent delegation. https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra (Accessed 5 October 2026).

Ouyang, L. et al. (2022). Training language models to follow instructions with human feedback. *Advances in Neural Information Processing Systems*, 35. https://arxiv.org/abs/2203.02155.

Russinovich, M., Salem, A. and Eldan, R. (2025). Great, now write an article about that: The Crescendo multi-turn LLM jailbreak attack. *34th USENIX Security Symposium*. https://www.usenix.org/conference/usenixsecurity25/presentation/russinovich.

Schluntz, E. and Zhang, B. (2024). Building effective agents. Anthropic, 19 December. https://www.anthropic.com/engineering/building-effective-agents (Accessed 5 October 2026).

Shen, X., Chen, Z., Backes, M., Shen, Y. and Zhang, Y. (2024). “Do Anything Now”: Characterizing and evaluating in-the-wild jailbreak prompts on large language models. *ACM SIGSAC Conference on Computer and Communications Security*. https://arxiv.org/abs/2308.03825.

Sothanaphan, N. (2026). Resolution of Erdős Problem #728: A writeup of Aristotle's Lean proof. *arXiv preprint*, version 5. https://arxiv.org/abs/2601.07421.

Stenberg, D. (2026). The end of the curl bug-bounty. 26 January. https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/ (Accessed 5 October 2026).

Wang, X. et al. (2023). Self-consistency improves chain of thought reasoning in language models. *ICLR*. https://arxiv.org/abs/2203.11171.
