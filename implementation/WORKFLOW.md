# Implementation Workflow (Steps 7+) — AI-Assisted Phase Build

**Status:** Active from Step 07 onward. Applies to all future steps (7–15).
**Governs:** how each `implementation/stepNN/` folder is produced.
**Supersedes:** the AI-assistance restrictions in `planning/rawSteps/step_*.md` (for Steps 7+).
**Audience:** the AI agent that builds a step's phase folders — and the human who runs and verifies afterward.

---

## 0. The one hard rule — write now, verify later

**All code in these phases is WRITTEN now and EXECUTED / VERIFIED later by the human, in
separate sessions. The agent never runs anything** — no training, no plotting, no
benchmarks, no notebooks.

Consequences that are **not** optional:

- **Never report results as if observed.** Nothing was run this session. Do not write
  "we measured / observed / got 0.03 exploitability." There are no measurements yet.
- **Frame every number as a prediction.** "Expected outcomes" are *targets to verify*,
  derived from the raw step's validation section, from theory, or from prior steps —
  always labeled as such ("expected", "target", "should converge to …").
- **In reading summaries, never invent.** Equations, theorems, and reported results must
  trace to a real source (cite section / equation / link). If you are unsure, say so —
  do **not** fill the gap with a plausible-looking number or formula.
- **Write code as if it must run unchanged.** The agent cannot smoke-test, so compensate
  with discipline: deterministic seeds, explicit imports, small default configs, type
  hints, and an honest "most likely to break when you run this" note.

Everything below serves this rule.

### 0.1 When a real run contradicts a prediction

Once code is actually executed (by the human, or by the agent when explicitly asked to run
it), an "expected outcome" will sometimes not match what happened. When it doesn't:

1. **Suspect a bug first, not the prediction.** A mismatch is the most common place a real
   defect hides. Before concluding "the prediction was just wrong," verify the run itself:
   re-read the relevant code path, check inputs/config/seeds, and confirm the observed
   behavior is genuinely the mathematically/theoretically correct outcome (a tiny targeted
   check — a print, a hand computation — is worth more than a plausible story). Only call it
   "expected, prediction was off" **after** you have actively ruled out an implementation
   error. Silently trusting the number is exactly the failure §0 warns about, in reverse.
2. **Keep the original assumption; don't rewrite history.** The pre-run prediction is a
   legitimate artifact — it shows what theory led you to expect. Leave it in place.
3. **Append what really happened and why the two diverged.** Add a clearly-labeled
   "what actually happened (observed on a real run)" note next to the prediction, naming
   the source of the confusion (an ambiguous term, an off-by-one mental model, a config
   that means something other than assumed). The gap between prediction and reality is
   usually the most instructive part of the step — capture it, don't erase it.
4. **Check whether the lesson still holds.** Often the headline takeaway survives even when
   the mechanism differs; say so explicitly. If the takeaway itself changes, update it.

This mirrors real research: you form a hypothesis, run the experiment, and report the
result **and** the reconciliation — never just quietly edit the hypothesis to match.

---

## 1. Why this exists (the retired restriction)

The raw step specs were written with a self-imposed restriction: a three-tier
AI-assistance policy (hand-code / AI-assisted / AI-generated tags) plus a "build from
scratch, own every line" rule, enforced by each step's Exit Checklist.

Given how much AI coding tooling has improved — and the expectation that it keeps
improving — that restriction is **retired for Steps 7+**. AI now writes all of the phase
code and notes; the human runs, debugs, refines, and writes the final consolidation.

The raw steps remain the **source of truth for _what_ to learn** (topics, papers,
validation targets, day structure). This document governs **_how_ the
`implementation/stepNN/` folder is produced**. The raw steps are **not edited**.

---

## 2. How the agent should approach a step

- **Read the raw step first** (`planning/rawSteps/step_NN_*.md`) end to end — it defines
  the topics, papers, day structure, deliverables, and validation targets.
- **Ground your work in it.** Cite raw-step line ranges for anything you carry over
  (deliverables, thresholds, paper reading lists).
- **Reuse, don't reinvent.** Import prior-step engines and utilities (§6).
- **Prefer clarity over cleverness.** A future reader and the human runner must
  understand each file from its own docstring / README.
- **When genuinely blocked or ambiguous, leave a clearly marked `NOTE:` / `TODO:`** in the
  deliverable rather than guessing silently or inventing a result.

---

## 3. Per-step folder layout

```
implementation/stepNN/
├── README.md            # step-level overview + index of the phase folders
├── intuition/           # Phase 1 — concept doc (no code)
├── exploration/         # Phase 2 — runnable code + README (not executed)
├── targetedReading/     # Phase 3 — condensed VIP-only summary
├── implementation/      # Phase 4 — full code + README + expected outcomes (not executed)
└── consolidation/       # Phase 5 — NOT produced by the agent (done by hand after runs)
```

Phase folders use **semantic names** (no number prefixes). `consolidation/` stays absent
until the human has executed and refined everything.

---

## 4. Phase contracts

Each phase maps 1:1 to the raw step's phase. Each deliverable ends with a
**"Key takeaways for the final summary"** block (§5).

### 4.1 intuition/ → `intuition.md` (no code)

**Goal:** build the mental model before any math or code.
**Suggested structure:**
- One-paragraph ELI5 of the core problem and why it matters.
- A concrete analogy / mental picture.
- The **different approaches** to the idea, compared — what each does, when you'd reach
  for it, and its main weakness (a small comparison table is welcome).
- **Development over time** — the lineage as a short dated timeline, each entry saying
  what it fixed about the one before.
- Common misconceptions / "easy to get wrong" notes.
- A short "you should be able to answer …" self-check (reuse the raw step's intuition
  questions).

**Guardrails:** words first; at most light notation, and only where it genuinely
clarifies; no implementation detail.
**Done when:** a non-expert could read it and explain the idea, the menu of approaches,
and roughly how the field got here.

### 4.2 exploration/ → runnable code (unexecuted) + `README.md`

**Goal:** let the human learn by running and tinkering — see it work and fail before the
theory.
**Code requirements:**
- **Fast and deterministic by default** — seed everything; small iteration / hand counts
  so a run is seconds-to-minutes.
- **Print clearly and save artifacts** — tables to stdout, plots/caches to a `figures/`
  subfolder.
- **Guard optional dependencies** (e.g. OpenSpiel) behind import checks with a helpful
  message; the core must run on the repo's own engines.
- One obvious entry point per script (`if __name__ == "__main__":`).

**README must cover (the four points that matter):**
- **What each script does.**
- **How to play with it** — a knobs table (parameter → effect → "try this").
- **What to watch out for** — pitfalls, misleading signals, common bugs.
- **How to read the results** — what each printout / plot means and what
  "expected / good" looks like (labeled as predictions, per §0).
- Plus a rough **runtime estimate** per script.

**Done when:** the human can run a script and, guided only by the README, know what to
expect and how to interpret it.

### 4.3 targetedReading/ → `summary.md`

**Goal:** the cropped, VIP-only distillation of the step's sources — the meat without the
bloat (long intros, related-work surveys, repeated boilerplate).
**Per source (from the raw step's reading list):**
- Full citation + link, and a one-line **role** ("why this is in the step").
- The **key idea** in 2–4 sentences.
- The **key math** — equations / theorems *by their number in the source*, with a
  plain-language gloss; for theorems, the **assumptions** and what breaks when they fail.
- The **algorithm** as short pseudocode if the source gives one.
- The **headline result** — and the source's own numbers only if you can cite them.

**Plus:**
- A cross-source **synthesis** (how the line of work progresses; agreements / tensions).
- **Worked "Math Flags"** the raw step marks mandatory (e.g. a by-hand Bayesian update),
  clearly labeled as the agent's derivation **to be checked**.
- A **"verify when you read it"** list — claims the human should confirm against the PDF.

**Guardrails (anti-hallucination):** short quotes only (copyright); cite section / eq for
every formula or result; never invent numbers; flag uncertainty explicitly; for non-open
papers, summarize from the open arXiv / author copy plus the raw step's
READ / MATH / KEY-INSIGHT notes, and say which you used.
**Done when:** the human grasps each source's contribution and the through-line without
opening the PDFs, and knows exactly what to double-check.

### 4.4 implementation/ → full code (unexecuted) + `README.md`

**Goal:** the step's core artifact, built complete and ready for the human to run and
validate.
**Code requirements:**
- Complete and **import-clean** against prior-step paths (§6); type hints + docstrings;
  deterministic seeds.
- **Two configs:** a fast **"smoke"** default (seconds–minutes; proves correctness on
  Kuhn/Leduc) and an optional **"5090-scale"** config (§7).
- A **self-contained validation harness** — scripts that, when run, check the raw step's
  validation targets, print pass/fail, and save results (JSON) + figures.
- A short **"static self-review"** — what the agent verified by reading (imports resolve,
  shapes/types line up, edge cases handled), since it could not run anything.

**README must cover:**
- **What was built** — module-by-module map + entry points, each mapped to the raw step's
  deliverable / validation item (cite line ranges).
- **How to verify** — exact commands in order, what each should print, and the
  **pass/fail thresholds** (from the raw step's Validation section), framed as targets (§0).
- **Expected outcomes** — predictions per experiment, labeled as predictions.
- **Likely-to-break list** — the spots most apt to need debugging on first run, with hints.

**Done when:** the human can follow the README to run, validate against the targets, and
debug efficiently — without reverse-engineering the code.

### 4.5 consolidation/ (deferred — human-written)

Not produced by the agent. Written by the human after running / refining everything; it
weaves the per-phase "Key takeaways" into the step's one-pager + learning-log entry.
(If the agent is ever asked to draft it, it must be from **verified** results, not
predictions.)

---

## 5. "Key takeaways for the final summary" blocks

Every phase deliverable ends with a short block titled
**`## Key takeaways for the final summary`**, listing the handful of must-remember points
that phase produced. They are the threads the human stitches together in consolidation,
so each should be:
- **concrete** (a claim, a number-to-verify, a relationship — not a vague topic),
- **self-contained** (readable without re-opening the whole phase),
- **forward-looking** where relevant (note connections to other steps / the thesis).

---

## 6. Cross-cutting conventions

- **Import, never copy** foundation code — reuse prior-step engines/utilities
  (e.g. step02 Kuhn engine, step03 Leduc engine + best-response / exploitability). See
  `implementation/step04/phase4/README.md`.
- **Entry scripts assume the repo root** as the working directory; add a minimal
  `sys.path` bootstrap at the top of cross-step scripts so imports resolve from root.
- **Determinism:** seed Python / NumPy / (PyTorch if used) and expose the seed as a
  parameter, so the human gets reproducible runs.
- **Naming:** `snake_case.py`; phase docs are `intuition.md` / `summary.md`; every code
  folder has a `README.md`; runtime artifacts go to a `figures/` subfolder.
- **Self-describing folders:** a reader should understand a phase folder from its own
  README / doc alone.
- **The agent never runs code** (restating §0).

---

## 7. Compute budget & experiment sizing

Hardware available for runs: **an RTX 5090.**

- **Default to small / fast experiments.** The toy testbeds (Kuhn, Leduc) are
  exact-solvable and validate correctness cheaply. Do **not** enlarge an experiment when
  bigger size adds no real insight.
- **Scale up when it pays off.** If a larger experiment would clearly demonstrate
  something meaningful **and** is estimated to finish in a **reasonable time
  (~a couple of hours on the 5090)**, make it bigger — more hands, seeds, iterations, a
  larger game, or a richer abstraction.
- **Always state a rough runtime / compute estimate** for each runnable script.
- Ship **two configs** where it helps: a fast **"smoke"** default and an optional
  **"5090-scale"** config for the convincing result.

---

## 8. Definition of done per step

- [ ] `intuition/intuition.md` — ELI5, analogy, approaches compared, dated lineage,
      misconceptions, self-check, key takeaways.
- [ ] `exploration/` — fast/seeded (unexecuted) code + README (what / play / watch-out /
      read-results + runtime estimates), key takeaways.
- [ ] `targetedReading/summary.md` — per-source VIP notes (cited math/results), synthesis,
      worked math flags (to-verify), "verify when you read it" list, key takeaways.
- [ ] `implementation/` — complete (unexecuted) code + validation harness, smoke vs
      5090-scale configs, README (module map + how-to-verify + expected outcomes +
      likely-to-break), static self-review, key takeaways.
- [ ] No fabricated results anywhere; every number is sourced or labeled a prediction (§0).
- [ ] `consolidation/` — left for the human, after running and refining the code.
