# Step 12 — Learning Log

> Phase 5 of Step 12. A short, first-person reflection stitched from the per-phase "Key takeaways"
> and the actual runs. Verified numbers only (see [`onePager.md`](onePager.md) for the full table and
> artifact caveats).

---

## What I set out to learn

Two things that are supposed to make classical game solving unnecessary. First, **sequence
modelling**: reframe RL as conditional sequence prediction, feed a transformer
`(return-to-go, state, action)` triples, and steer it at inference by asking for a high return — no
value function, no Bellman backup, no self-play. Second, **LLM agents**: hand a language model the
rules in English and let it play, with no training at all. Kuhn Poker was the testbed precisely
because its Nash equilibrium and exploitability are *exactly* computable, so both ideas get an
honest, ground-truthed score instead of an anecdote.

I expected to learn where each method sits relative to Nash. What I actually learned is that both of
them lose to the dumbest baseline in the file, and that most of my effort went into finding out
whether my *measurements* were real.

## What clicked, phase by phase

- **Intuition.** The Decision Transformer's trick is genuinely elegant: conditioning replaces
  optimisation. The catch, which the intuition doc names and I did not take seriously enough until I
  measured it, is that the conditioning signal has to *mean* something the agent controls.
- **Exploration.** The coin-flip probe is the whole step in eight lines. Action A pays 0.5 for
  certain; B pays 1.0 with probability 0.4 (EV 0.4). Condition on "return = 1.0" and you recover
  **only** B-trajectories, so return-conditioned cloning learns the **worse** action —
  `P(B | R=1.0) = 1.00` measured, exactly as predicted. Every later result is a variation on that.
- **Targeted reading.** Reading ARDT properly was worth more than any single run. Equations 6 and 7
  settle the τ convention in one line (α→0 is the min), and Algorithm 1 line 7 quietly reveals that
  the relabel target is `Q̃(s_t, a_t)` — a state-**action** value — which is precisely what my
  implementation does not have.
- **Implementation + runs.** The comparison table was the moment the step stopped being what I
  thought it was: **BC 0.055 chips, ARDT 0.469, DT 0.799, LLM 0.833, Nash 0.016.** The two methods
  the step is named after finished last, behind a baseline I included only for contrast.

## Where reality bit back (the instructive part)

1. **My headline explanation was half wrong, and Leduc is what proved it.** When return
   conditioning failed on Kuhn I explained it with a mechanism I still like: the return's magnitude
   encodes *which betting line was played*, its sign is card luck, and R = −1 (the modal, fold
   payoff) therefore selects "the folding line" — the DT passes at 11 of 12 info sets there. That
   story predicts the effect should weaken with a richer payoff alphabet. Leduc has 15 payoff values
   instead of 4, and **the notch vanished exactly as predicted** — *but steering still did not
   appear* (`r = +0.062`). So I explained the notch and not the failure. The failure is deeper than
   my mechanism, and I would not have found that out without porting to a second game.
2. **The hypothesis I was most confident about was backwards.** I predicted LLMs would know the
   right mixing frequency but be unable to sample it. Asked directly, Qwen answers **"50%" at 11 of
   12 info sets** and gpt-oss answers **~0% at 8 of 12** — and playing their own stated frequencies
   would make them **2.6× and 4.0× more exploitable** than they actually are. They play better than
   they can explain. I have stopped treating "ask the model what it's doing" as a measurement.
3. **Four separate results looked like discoveries and were artefacts.** A seat-0 return that
   looked like an engine bias (1.7 SE of noise — caught by computing the *exact* game value). An
   in-context learning result of +1.59 (impossible: >1 means beating the exact best response —
   caught by working the ceiling out by hand: K→+2, Q→0, J→−1 ⇒ +0.333). A monotone Leduc trend that
   vanished at 20× the hands. And a confident Leduc LLM number produced by a decoder that had thrown
   away 70% of the probability mass and **inverted** the model's policy. Each one was plausible,
   quotable, and wrong.
4. **The runbook would have committed a fabricated figure.** `plotting.py` shipped with only a
   self-test that plotted hard-coded numbers into `results/` — and it was the *only* PNG-producing
   path in the step. Following the documented steps literally would have put invented data in the
   repo under a real-looking filename.

And a methodological echo of Steps 9–11: every one of those artefacts was caught by a *cheap
consistency check against something exactly computable* — an exact game value, an exact
best-response ceiling, a standard error, a mass-conservation diagnostic. None was caught by staring
at the number.

## Headline lessons I'm keeping

- **Conditioning on a quantity the agent does not control cannot steer it.** In a zero-sum
  imperfect-information game the realised return is dominated by the opponent's private card and
  actions. No amount of payoff granularity fixes that — which is exactly why ARDT's relabeling
  matters, and why the DT itself is the wrong instrument for Step 13's fixed logs.
- **A scalar score ranks methods; it does not diagnose them.** Over-betting the King — the failure I
  had written up as a headline — costs **0.1%** of the leak. One Queen node costs **41.4%**.
  Deviation magnitude and cost are nearly uncorrelated, and I only saw that because I decomposed it.
- **Measure behaviour, not self-report.**
- **Instrument the measurement, not just the result.** Reporting unmapped/illegal probability mass
  instead of quietly renormalising it away is what caught the Leduc decoder bug *and* turned into a
  finding in its own right (the `FOLD_WHEN_FREE` misconception).
- **A protocol choice can invent your result.** At temperature 0 an LLM plays a pure strategy, so
  every measured "frequency" is 0 or 1 and exploitability becomes a lottery over which pure strategy
  it landed on. The default that was right for the offline stub was wrong for every real model.

## Connections (Steps 2–11 → Step 12)

- **[Step 2] exact Kuhn CFR + exploitability → [Step 12] the ruler.** Every method here — DT, ARDT,
  BC, four LLM backends — is coerced into Step 02's 12-info-set `node_map` and scored by the same
  exact metric. Without that anchor none of the artefacts above would have been detectable.
- **[Step 7] opponent zoo + exact best response → [Step 12] both the ARDT training data and the
  exploitation axis.** `make_type_zoo` supplies the mixed opponents; `best_response_policy` supplies
  the ceiling that exposed the false B5 result.
- **[Step 5] neural equilibrium → [Step 12] ARDT** as the offline sibling: same destination
  (minimax/Nash), opposite data regime (a fixed dataset instead of self-play iteration).
- **[Steps 9–11] "suspect the measurement first"** → applied four times here, and it paid every
  time. Step 11's seat-0 tie-break artefact and Step 12's seat-0 sampling scare are the same lesson
  in two different disguises.
- **[Step 12] → [Step 13]:** the `PokerStateEncoder` is the concrete artifact that carries (now
  exercised on two streets and a board card), and the ARDT `Q(s,a)` fix is the named change to make
  before touching Playtech logs. **[Step 12] → [Step 14]:** the per-decision decomposition, the
  temperature protocol, and the exploitation-vs-exploitability frontier are three concrete
  components of the evaluation methodology.

## Confusions

- **Why does return conditioning fail even with a 15-value payoff ladder?** → **PARTIALLY
  ANSWERED.** The payoff-alphabet explanation is dead (Leduc killed the notch without restoring
  steering). My current best account — the return is dominated by uncontrollable factors — is
  consistent with two games but is not yet a measurement.
- **Would the paper's `Q(s,a)` relabeling actually close the ARDT gap?** → **LIKELY, UNTESTED.** The
  reasoning is concrete (a state-only target cannot separate "bad state" from "bad action"), and the
  τ-sweep behaviour fits it, but I have not implemented it.
- **Is τ=0.9 measuring better for the reason I think?** → **OPEN.** I believe it is the R1 folding
  artefact in reverse, not evidence that optimism is correct. Deliberately not acted on.
- **Is the Leduc collapse a property of LLMs or of Qwen-7B?** → **OPEN — the biggest caveat in the
  step.** One model, one prompt style, 600 hands.
- **How much of the 23.4% illegal intent survives a one-line prompt fix?** → **OPEN, cheap to
  answer.** If "you may check for free" removes it, the finding is about prompting; if not, it is
  about comprehension. Those are very different claims.

## Open threads

- Implement ARDT's coupled `Q(s,a)` estimators (Eqs. 8–11) plus the Algorithm-1 warm-up; re-check
  targets #3 and #4.
- Run a second model on Leduc before any Leduc claim is quoted outside this step.
- Test the `FOLD_WHEN_FREE` prompt fix.
- Optional: SCALE profile, OpenThinker3's remaining prompt styles, and exact Leduc exploitability
  (which needs the step02/step03 `cfr` package collision solved).
