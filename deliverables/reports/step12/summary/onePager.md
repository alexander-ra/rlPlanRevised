<!--
OFFICIAL PhD TITLE (keep consistent across all documents):
EN: Research on the possibilities for applying Artificial Intelligence in computer games
BG: Изследване на възможностите за приложение на изкуствения интелект в компютърни игри
-->
---
title: "Step 12 One-Pager — Sequence Models and LLM Agents in Strategic Settings"
subtitle: "Research on the possibilities for applying Artificial Intelligence in computer games"
author: "Alexander Andreev"
date: "July 2026"
lang: en
---

# Step 12 One-Pager — Sequence Models and LLM Agents in Strategic Settings

**Problem.** Two post-classical ways to play a game bypass everything Steps 2-11 built.
**Sequence modelling** recasts play as conditional prediction — feed a transformer
`(return-to-go, state, action)` triples and ask for the next action given a desired return, no
value function, no self-play — and **ARDT** adds minimax relabelling for worst-case robustness.
**LLM agents** skip training entirely: hand a model the rules in English. Step 12 scores both
against an exact benchmark.

**Approach.** Kuhn Poker, where Step 2 supplies exact Nash and exact exploitability, with a narrow
port to Leduc Hold'em as a complexity check. Compared: Nash-CFR, behavioural cloning, a Decision
Transformer, ARDT, and four LLM backends (offline stub, gpt-oss-20b, Qwen2.5-7B, OpenThinker3-7B),
plus follow-ons asking *why* that ranking falls out. **All numbers below are measured** from
committed JSON, with two caveats: two results were **retracted** mid-session (an impossible `+1.59`
gap closed, and a Leduc `-0.83` from a decoder discarding 70% of the probability mass), and the
Nash reference is `0.0162` chips at 5,000 CFR iterations but `0.0061` at 50,000 — both ~0.

**Key results (measured).**

- *The step's two nominal subjects finish last.* **BC 0.055 << ARDT 0.469 < DT 0.799 < LLM
  0.833**, against Nash **0.0162**. Cloning lands within 0.04 chips of Nash by copying a near-Nash
  policy, while the DT routes that same policy through a return-conditioning channel carrying
  mostly luck — conditioning actively destroys information here.
- *Return conditioning never steers, on either game.* `high(+2) = 0.6981` vs `low(-2) = 0.6928`:
  tied, and ordered wrong. The Kuhn explanation (a 4-value payoff alphabet) was **half-refuted** on
  Leduc: 15 payoff values made the predicted artefact vanish, but steering still failed to appear
  (`r = +0.062`).
- *The models play better than they can explain.* The hypothesis going in was "knows the right
  frequency, cannot sample it"; the data says the reverse. Scored as strategies, *stated*
  frequencies are far worse than *played* ones — Qwen **0.921 vs 0.357** chips, gpt-oss **1.576 vs
  0.392**. Probe behaviour; do not ask.
- *Exploitative by default, not adaptive.* Mean gap closed **+0.38** but mean **learning -0.22**:
  against the one well-powered opponent the model captures **83%** of available exploitation from
  the first half onward and never improves. It exploits **61% harder than Nash while being 59x more
  exploitable**, and only against passive opponents.
- *Scale is irrelevant, and the LLM edge belongs to Kuhn.* **Qwen-7B beats gpt-oss-20B by +0.162
  chips/hand** over 20k hands per pair, strictly transitively. On Leduc the LLM is
  indistinguishable from the DT (`-0.463` vs `-0.454`) and cannot beat weak opponents at all
  (`-0.071` where Nash gets `+0.582`), with **100%** of its illegal-action mass a single
  misconception: folding when checking is free.
- *One scalar hides the diagnosis.* A single Queen node is **41.4%** of total exploitability, while
  value-betting the King at 1.00 where Nash mixes at 0.68 costs **0.1%** — deviation size and cost
  are nearly uncorrelated. Harness: **3 PASS / 2 FAIL**, honestly red.

**Thesis connection.** Contribution #1 gets a negative result worth having: behavioural adaptation
is *absent* in-context, so an explicit opponent model must be built rather than assumed.
Contribution #2 gets its frontier measured on one plot — 61% more exploitation for 59x the
exploitability, only against weak opposition. Contribution #3 gets the per-decision decomposition
and the measurement protocol.

**Open questions.** The named fix is ARDT's `Q(s,a)`: a state-only return estimator cannot tell
"this state is bad" from "*this action* is bad", which is why the tau sweep contradicts theory and
exploitability comes out *lowest* on the optimistic side — the default was left at the
theoretically correct value rather than switched to buy a better number. Whether the Leduc
misconception is one prompt line away. And the standing caveat: every Leduc LLM conclusion rests on
one model, one prompt style, 600 hands.
