# Step 12 — Intuition: Sequence Models + LLM Agents in Strategic Settings

> Phase 1 of Step 12. Words first, almost no math, no code. Goal: build the mental model of the
> **two post-classical ways to make an AI play games** before touching the papers or the
> implementation. Grounded in the raw step's Phase 1 (
> [`step_12_sequence_models_llm_agents.md`](../../../planning/rawSteps/step_12_sequence_models_llm_agents.md)
> L50-92).

---

## The one-paragraph ELI5

Everything in Steps 1-11 learned to play by either **estimating how good each move is** (value
functions, Q-learning) or **iterating toward an equilibrium** (CFR, self-play). Step 12 is about
two ideas that skip both. **First:** treat a game history as a *sentence* — a stream of
`(reward-you-still-want, situation, move)` tokens — and train a next-token predictor (a
transformer, the same architecture behind ChatGPT) to continue it. At play time you *tell it how
well you want to do* ("I want a high return") and it emits moves that historically led there.
That is the **Decision Transformer**. **Second:** take a large language model that already read
much of the internet, hand it the rules of a game in plain English, and just let it play by
reasoning in words. No training loop at all. Both work shockingly well sometimes and fail
embarrassingly other times, and the research frontier is figuring out *when* each works and how
to combine them with the equilibrium tools we already have.

---

## A concrete mental picture

Imagine two ways to teach someone poker from a stack of hand histories:

- **The Decision Transformer way.** You give the student thousands of transcribed hands, each
  labeled at the end with "this line eventually won +2 chips." The student learns the pattern
  "when the board looked like *this* and I wanted to end up +2, the move that got me there was
  *bet*." At the table you whisper the target ("aim for +2") and they replay the move that
  matched. The catch: some of those +2 outcomes happened because the player got **lucky cards**,
  not because they played well — so "aim high" can teach the student to *wish for good cards*
  rather than *play good poker*. That single failure mode (Paster et al.) is the spine of this
  step.

- **The LLM way.** You give a brilliant, well-read friend the rulebook and say "play." They
  reason out loud — "my Jack is weak, but if I bet, my opponent might fold a Queen…" — and
  sometimes bluff beautifully, sometimes try to fold when folding isn't even a legal move. They
  never trained on poker specifically; they're *reasoning*, not *optimizing*.

Kuhn Poker is our microscope: it is tiny enough that we know the **exact** optimal strategy and
can measure precisely how far any player is from it.

---

## The menu of approaches (what each does, when to reach for it, its weakness)

### Offline RL from a fixed dataset

| Approach | Core idea | Reach for it when… | Main weakness |
|---|---|---|---|
| **Behavioral cloning (BC)** | Supervised: predict the action a good player took from the state. No returns. | You just want to *imitate* demonstrated play. | Copies mistakes; no notion of "do better than the data." |
| **Conservative Q-Learning (CQL)** | Value-based offline RL; pessimistically penalizes Q-values for unseen actions. | The environment is **stochastic** (luck matters). | Still needs value estimation / Bellman backups; more moving parts. |
| **Decision Transformer (DT)** | Condition next-action prediction on **return-to-go**. Pure sequence modeling. | Data is mostly good and the game is near-deterministic. | **Conflates luck with skill** in stochastic games (Paster). |
| **Trajectory Transformer (TT)** | Tokenize *everything* (states, actions, rewards) and **beam-search** the future. | You want *planning*, not just generation. | Heavier; discretization + search cost. |
| **Adversarially Robust DT (ARDT)** | Condition on the **minimax** return — the best you can do against the *worst* opponent. | The return depends on an **adversary** (all competitive games!). | Needs good coverage of the state space; the minimax estimate is only as good as the data. |

The through-line: BC ignores returns; DT conditions on the raw return (and gets fooled by luck
and by weak opponents); ARDT conditions on the *adversarially-robust* return and, with full data
coverage, can recover **Nash**.

### LLM agents

| Approach | Core idea | Reach for it when… | Main weakness |
|---|---|---|---|
| **Zero-shot LLM** | Rules in the prompt, ask for a move. | Quick baseline; novel/verbal games. | Illegal moves; inconsistent strategy. |
| **Chain-of-thought (CoT) LLM** | Ask it to *reason step by step* first. | Reasoning helps (bluff logic, theory of mind). | Slower; long traces to parse; can rationalize bad moves. |
| **Game-theory-prompted LLM** | *Tell* it about the Nash concept and ask it to approximate. | You want to test if it can *use* theory it's told. | May parrot the concept without correct numbers. |
| **LLM + formal solver (e.g. SpinGPT/CICERO)** | LLM for language/negotiation, a solver for the strategy. | Rich social games (Diplomacy). | Engineering-heavy; two systems to align. |

---

## Development over time (a short dated lineage)

- **2020 — Conservative Q-Learning (Kumar et al.).** The value-based offline-RL baseline:
  pessimism about out-of-distribution actions. The thing DT is compared against.
- **2021 — Decision Transformer (Chen et al.) & Trajectory Transformer (Janner et al.).** The
  reframing of RL as sequence modeling arrives, twice, in the same year — DT (return-conditioned
  generation) and TT (tokenize-everything + beam search planning).
- **2022 — "You Can't Count on Luck" (Paster et al.).** The cold shower: in stochastic
  environments, conditioning on high return chases *lucky* trajectories, not *skilled* ones. A
  formal bound (their Theorem 2.1) says how bad this can get. This is *why* naive DT on poker
  data is dangerous.
- **2024 — Adversarially Robust DT (Tang et al., NeurIPS).** The fix for the *adversarial* part
  of the problem: condition on **minimax** returns via expectile regression. With full coverage
  it recovers Nash — a second road to equilibrium that needs no CFR.
- **2025 — TextArena (Guertler et al.), SpinGPT, Suspicion-Agent, Divide-Fuse-Conquer.** The
  LLM-agent track matures: 57+ competitive text games with TrueSkill scoring; explicit
  combinations of LLM reasoning with CFR strategy (SpinGPT) and with theory-of-mind planning
  (Suspicion-Agent).

---

## Common misconceptions ("easy to get wrong")

- **"Return-to-go is the reward."** No. Return-to-go at time *t* is the **sum of *future***
  rewards from *t* onward — a *target you condition on*, not a reward signal you maximize. In
  poker (reward only at showdown) the return-to-go is constant across a whole hand: the final
  chips won.
- **"High return-to-go means skilled play."** Only in (near-)deterministic games. In a stochastic
  game, high-return trajectories over-represent **lucky card deals**; conditioning on them can
  teach the model to *predict luck*, not *play well*. This is the single most important idea in
  the step.
- **"ARDT and CFR are unrelated."** ARDT reaches Nash **from offline data by supervised learning**
  with the right conditioning; CFR reaches Nash **by online self-play iteration**. Same
  destination, different road — a direct bridge back to Step 05's Deep CFR.
- **"The LLM understands the rules, so it will play legally."** Frequently false. Illegal-move
  rate is a *headline metric* for LLM game agents precisely because they attempt illegal actions.
- **"A bigger/frontier LLM would obviously be near-Nash."** Unverified and not the point. The
  interesting, honest finding is usually *where* an LLM's strategy departs from Nash (wrong bluff
  frequency, failure to adapt), not a leaderboard number.
- **"Exploitability is in big blinds."** In this codebase Step 02's `compute_exploitability`
  returns **chips** (the sum of both players' best-response values). Don't silently read it as
  mbb/h — see the implementation README for the conversion.

---

## You should be able to answer (self-check — raw L58)

1. In one or two sentences each, explain the Decision Transformer and the LLM-agent paradigms to
   a non-expert.
2. Why does conditioning a DT on high return-to-go fail in a *stochastic* game? What does the
   fix look like conceptually?
3. What does ARDT condition on instead of the raw return, and why does that make it robust to the
   opponent?
4. Name two ways an LLM can *fail* at Kuhn Poker even though it "knows the rules."
5. What is the exact quantity that lets us grade all of these methods honestly on Kuhn Poker, and
   which prior step provides it?
6. Give one reason ARDT and CFR are "two roads to the same destination," and one reason you might
   prefer ARDT in a real-world domain (hint: Step 13 / Playtech data).

---

## Key takeaways for the final summary

- **Two post-classical paradigms:** sequence-modeling offline RL (DT / TT / ARDT) and LLM
  agents. Both skip value functions *and* equilibrium iteration.
- **The central hazard is luck-vs-skill:** return-to-go conditioning conflates *lucky outcomes*
  with *skilled decisions* in stochastic games (Paster). It is the reason a naive DT on poker
  data misleads, and the design constraint carried into Step 13's Playtech pipeline.
- **ARDT is a second road to Nash:** minimax return conditioning recovers equilibrium from
  *offline* data — an offline analog of Step 08's safe exploitation and an alternative to
  Step 05's Deep CFR.
- **LLMs are complementary, not competitive, with formal tools:** they bring
  language/negotiation/theory-of-mind that CFR ignores, but pay for it with illegal moves and
  inconsistent strategy. The honest question is *where* they work.
- **Kuhn Poker is the exact-graded microscope:** Step 02's exact Nash + exploitability lets every
  method (Nash CFR, DT, ARDT, BC, LLM×prompts) be scored on one honest table.
