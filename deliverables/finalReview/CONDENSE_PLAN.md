# Condensing the summaries bundle — balance rule and section-by-section plan (28 Sep 2026)

Nothing has been edited yet. This file fixes *where the line is* and marks every section of the
fifteen English summaries (the Bulgarian twins have the same structure, so every verdict applies to
both). Word counts are English; the Bulgarian runs longer but scales the same way.

## Result (28 Sep 2026)

All fifteen chapters have `summaryShortEn.md` / `summaryShortBg.md`; the originals are unchanged.
The candidate chose a milder depth than §6 during the work (≈ −20 to −30 %, chapter 6 in place).
English words (checker count, tables included): **83 997 → 61 886 (−26 %)** — ch. 1 −36 %, 2 −22 %,
3 −22 %, 4 −36 %, 5 −25 %, 6 −35 %, 7 −23 %, 8 −22 %, 9 −21 %, 10 −23 %, 11 −22 %, 12 −8 %, 13 −21 %,
14 −20 %, 15 −20 %. Every pair has identical headings, figures, table rows and footnote labels; no
reference points to a missing section; the only renumbering is chapter 4 (4.13 merged into 4.2, so
the former 4.14 is 4.13 — nothing cites it). Chapter 15's stale AAMAS sentence is neutralised in the
short version only. Build: `python scripts/build_reports.py --type summaryshort --lang both --bundle-only`.

## 1. The balance rule

The summaries are meant to be **a summary of the field plus the candidate's own work**, not a
textbook. A section earns its space if it has at least one of:

- **A. Own simple explanation** of a core idea the thesis uses: an intuition, an analogy, one small
  worked example. Keep one per idea.
- **B. Own evidence**: a measured result, a prediction-vs-result reconciliation or an honest limitation.
- **C. Something later work relies on**: a definition a later chapter cites (by section number or by
  idea), a gap statement, a contribution link, a number Chapter I or Chapter 15 cites.

Cut signals, in the order they save the most:

1. **Paper retelling**: history, other authors' result tables, system-by-system walkthroughs beyond
   what later chapters use → 1–2 sentences and a citation.
2. **Repetition**: inside a chapter (takeaways and "what held up" restating the body, a worked example
   and a formal restatement of the same thing, a caption re-narrating the text) and between chapters
   (background already taught) → keep one, back-reference the rest.
3. **Derivation depth**: several equations restating a paper → keep the defining equation.
4. **Implementation detail**: configs, solver internals, serving specs → the report (move only what the
   report lacks).
5. **Catalogues** of methods or variants not used later → a sentence or a table row.
6. **Read-more boxes, "Remember" boxes, asides** → drop unless they carry a caveat the thesis needs.
7. **Conceptual diagrams** that restate the prose (not own-result plots) → keep at most one per
   chapter; own-result figures always stay.

Never cut: reconciliations, limitations, own-result figures, numbers cited by Chapter I or later
chapters, and the section headings other chapters point to (1.4, 2.8, 3.4, 7.5, 7.7, 10.7, 11.3,
11.4, 14.8 and the in-chapter references of chapters 3, 5, 8, 9, 10). Default: **keep every `##`
heading** so section numbers do not shift; a section may shrink to a short paragraph.

## 2. Where the words go

| Chapters | Now | Proposed | Change | Main source of the cut |
|---|---:|---:|---:|---|
| 1–3 | 8 971 | 5 806 | −35 % | RL history, DP/TD textbook material, MCTS walkthrough, repeated connections |
| 4–5 | 11 458 | 6 547 | −43 % | neural-network primer, layer-type tour, "Remember" boxes, retelling covered in ch. 6 and 9 |
| 6 | 20 648 | 8 580 | −58 % | five parallel seven-part system templates re-explaining the same mechanism |
| 7–9 | 15 919 | 10 775 | −32 % | re-taught Nash/MDP background, MARL catalogue, textbook diagrams, summary/report duplication |
| 10–12 | 9 308 | 6 944 | −25 % | conceptual diagrams and captions, "what held up" recaps, configs |
| 13–15 | 15 508 | 11 070 | −29 % | parser/engine detail, ch. 15 restating ch. 14, closing recaps |
| **Total** | **81 812** | **49 722** | **−39 %** | Chapter 6 alone is 37 % of the cut |

The proposal overshoots the one-third target; the easiest place to give back is the "own
explanation" trims in chapters 1–5 and 7 (keep them closer to full).

## 3. Decisions (taken 28 Sep 2026) — these override the verdicts in §6

- **Output:** a separate condensed version, bundle only. New files
  `deliverables/reports/stepNN/summary/summaryShortEn.md` and `summaryShortBg.md` sit next to the
  originals (same figure paths); the original summaries, reports and one-pagers are not touched.
  Build: `python scripts/build_reports.py --type summaryshort --lang both --bundle-only` →
  `deliverables/bundles/allSummariesShort_{en,bg}.pdf`.
- **Target:** the proposed cuts (≈ −39 %) everywhere except where the decisions below give back words.
- **Chapter 6:** trim each subsection in place and keep the seven-part template (≈ −35 to −40 %, not
  −58 %). Within that, the §6 verdicts still say what goes (compute essays, retold background,
  repeated test-time-compute framing, restated strengths/limitations); MERGE verdicts become heavy
  trims in place.
- **Conceptual diagrams:** keep them all; shorten captions only. Every "drop the diagram" verdict in
  §6 becomes "keep, caption ≤ 30 words".
- **Headings:** merges are allowed, and references to renumbered sections are updated — but a merge
  must not change the number of a section another chapter cites: 1.4, 2.8, 3.4, 7.5, 7.7, 10.7,
  14.1, 14.5, 14.7, 14.8.
- **Chapter 5 primer:** reduce to a textbook back-reference of about 100 words.

The original decision questions, for the record:

1. **Conceptual diagrams.** Keep all, keep one per chapter (plus every own-result figure), or decide
   case by case. Affects ch. 5 (grid/Pommerman schematics), 6 (five architecture diagrams, the arc
   figure), 7, 8, 9, 10 (four), 11 (four).
2. **Chapter 6 restructure.** One shared explanation of search under hidden information in 6.1, then
   each system in four short parts (opening + scorecard, gap, how it works, caveats) with a two-line
   legacy. The alternative is trimming each subsection in place (≈ −35 % instead of −58 %).
3. **Headings.** Keep every heading (no renumbering; some sections become one-paragraph stubs) or allow
   merges and update the references (e.g. 2.3→2.4, 2.7→2.8 moves Kuhn from 2.8 to 2.7; 8.4 and 9.3 stubs).
4. **Primers.** Chapter 5's neural-network primer (the thesis's only one): ~230 words, or a textbook
   back-reference (~100).
5. **Target.** −39 % as proposed, or ≈ −33 % by keeping more of the own explanations.

## 4. Flags found along the way (fix while condensing)

- Ch. 1 §1.5: "Go 10¹⁷⁰" is unsourced. Ch. 1 §1.9: the SB3 comparison is under a "do not cite until
  the text/figure run mismatch is fixed" note (F01-C01/C02).
- Ch. 4 §4.12: the action-abstraction figures plot numbers from the harness bug; check that the Pareto
  figure was regenerated from the 180-s data (F04-G04).
- Ch. 6: Noam Brown's "20 seconds ≈ 100,000×" quote has no verified primary source; SoG "+434 vs LBR"
  is unchecked; the evolution-arc figure has unsourced lane positions and a wrong DeepStack→Libratus
  link; the Pluribus "collusion" sentence is not in the paper; the 6.3.7 depth-limited-solving link is
  flagged as wrong in the review.
- Ch. 13: the note on the two reading-list papers that could not be found exists only in the summary.
- Ch. 15 §15.7: "AAMAS 2027 … only if a full draft exists by the end of September" is stale after
  28 September (deadline 8 October 2026).

## 5. Execution notes

- Edit English and Bulgarian together, chapter by chapter; keep headings, footnote labels and figure
  paths identical; rebuild and run `check_headings.py` / `check_captions.py` per chapter.
- Moving detail to a report: only where the verdict says the report lacks it (ch. 14 §14.2 LLM
  serving specs and tree size; ch. 13 missing-papers note, if kept).
- Chapter 5 has no `report_en.md`; its run details stay in the summary.
- After condensing, re-run the one-pager check: one-pagers are not touched by this plan.

---

## 6. Section-by-section verdicts

Verdicts: KEEP · TRIM ≈x % · CONDENSE→~N words · MERGE→§ · MOVE→report · OMIT.

### Chapter 1 — Reinforcement Learning Basics (3 424 → ~1 955)
Spine: MDP/Bellman, information sets (§1.4, cited by ch. 2), the DQN and PPO ideas later solvers reuse, the own from-scratch validation with its caveats. (Ch. 15's "§ 1.7" is Chapter I of the dissertation, not this §1.7.)

| § | Section | Words | Type | Verdict | Target | Reason |
|---|---|---:|---|---|---:|---|
| 1.1 | How RL became a discipline | 344 | retelling | CONDENSE | 80 | Drop the Thorndike→Watkins chronology; keep "three threads merged", DQN/PPO dates. |
| 1.2 | Agent, action, environment | 357 | own expl. + glossary | TRIM ≈40 % | 220 | Keep loop, CartPole/poker examples, exploration–exploitation; shorten glossary; drop Spinning Up box. |
| 1.3 | MDP formulation | 180 | defining derivation | TRIM ≈15 % | 150 | Keep Bellman and "Markov fails in poker"; components on one line. |
| 1.4 | Information sets | 255 | own expl. (cited) | KEEP (light) | 200 | Cited by ch. 2; cut the closing "why this matters". |
| 1.5 | Dynamic programming | 278 | textbook | CONDENSE | 110 | One sentence each for policy/value iteration; drop unsourced Go 10¹⁷⁰. |
| 1.6 | TD learning | 273 | derivation + expl. | CONDENSE | 150 | Keep Q-learning equation, TD error as surprise; drop TD(0) and SARSA. |
| 1.7 | DQN | 508 | retelling + expl. + result | TRIM ≈45 % | 280 | Keep replay, moving-target explanation, no-mixing limit; drop history, run paragraph (in 1.9), NN note. |
| 1.8 | PPO | 636 | retelling + expl. + result | TRIM ≈50 % | 310 | Keep clipping, actor–critic line, stochastic policy; drop TRPO detail, RLHF aside, network sizes. |
| 1.9 | Practical validation (lead) | 71 | own results setup | KEEP | 60 | The matched-vs-tuned caveat every conclusion depends on. |
| 1.9 › | DQN on CartPole | 305 | own results + limits | TRIM ≈35 % | 200 | Keep 477.5 @ ep. 1011, SB3 222.4→134.3, one-run caveat; Zoo hyperparameters in report §4.1. |
| 1.9 › | PPO on LunarLander | 156 | own results + limits | KEEP (light) | 140 | Shorten the list of possible causes (report §4.2). |
| 1.9 › | Takeaway | 61 | connections | KEEP | 55 | The stated reason for writing from scratch. |

### Chapter 2 — Game Theory & CFR Basics (2 645 → ~1 890)
Spine: minimax/Nash safety and its N-player failure (C2 premise), regret matching → CFR → average strategy, Kuhn (§2.8, cited by ch. 7), exploitability with the measured slope (C3 premise).

| § | Section | Words | Type | Verdict | Target | Reason |
|---|---|---:|---|---|---:|---|
| 2.1 | Single- → multi-agent | 166 | own expl. | TRIM ≈35 % | 110 | Keep "cart-pole doesn't fight back"; drop the form/Nash preview repeated in 2.2/2.4. |
| 2.2 | Extensive form & info sets | 235 | textbook (in 1.4) | TRIM ≈40 % | 140 | Two sentences on trees; back-reference 1.4 (done); one Kuhn example. |
| 2.3 | Minimax theorem | 164 | retelling | CONDENSE | 80 | Restates maximin/minimax several times; keep value and "Nash = minimax, hence safe". |
| 2.4 | Nash equilibrium | 329 | definition + gap | TRIM ≈30 % | 230 | Keep equation, existence, N-player/PPAD/Szafron; Kuhn bullets live in 2.8. |
| 2.5 | Regret matching | 187 | own worked example | KEEP | 175 | The model own-words explanation (RPS). |
| 2.6 | CFR | 365 | derivation + expl. | TRIM ≈35 % | 240 | Keep counterfactual-regret equation and reach intuition; 7-step algorithm → two sentences. |
| 2.7 | Mathematics of poker | 164 | expl. + unverified retelling | CONDENSE | 80 | One line per complexity source; Chen & Ankenman to a clause. |
| 2.8 | Kuhn poker | 321 | definition (cited) | KEEP (light) | 270 | Cited by ch. 7; trim "Why Kuhn matters" list. |
| 2.9 | Exploitability | 365 | definition + own results | TRIM ≈15 % | 310 | Keep NashConv factor 2, slope −0.52 ± 0.02, game-value counterexample. |
| 2.10 | Connections | 195 | analogies + boilerplate | TRIM ≈40 % | 115 | Keep the two analogies; forward paragraph → one sentence. |
| 2.11 | Empirical visualizations | 154 | own-result figures | KEEP | 140 | Three own figures. |

### Chapter 3 — CFR Variants & Monte Carlo Methods (2 902 → ~1 961)
Spine: the four-solver Leduc comparison at equal budget, variance–speed accounting (§3.7), crossover estimate with caveats (§3.8), Leduc definition (§3.4, cited by ch. 7–8).

| § | Section | Words | Type | Verdict | Target | Reason |
|---|---|---:|---|---|---:|---|
| 3.1 | Why vanilla CFR breaks | 272 | connections + retelling | TRIM ≈35 % | 175 | Keep scale gap and thesis anchor; CFR+/MCCFR previews repeat 3.5/3.6. |
| 3.2 | MCTS as inspiration | 311 | retelling + catalogue | CONDENSE | 90 | Drop four-phase walkthrough and table; keep "sample, don't enumerate". |
| 3.3 | Markov chains & LLN | 273 | retelling + expl. | CONDENSE | 140 | Drop Los Alamos history and the chain paragraph; keep LLN, unbiasedness, "cost is variance". |
| 3.4 | Leduc poker | 238 | definition (cited) | KEEP (light) | 200 | Keep the table; "new features" bullets → one sentence. |
| 3.5 | CFR+ | 353 | derivation + own results | TRIM ≈30 % | 250 | Keep floored-regret equation, ReLU analogy, 1 100 vs ~2 M; OpenSpiel figures to report. |
| 3.6 | MCCFR | 395 | expl. + own results | TRIM ≈35 % | 250 | Keep variants table and the ε sentence; Kuhn figures → one sentence. |
| 3.7 | Variance–speed tradeoff | 401 | own results + reconciliation | KEEP (≈−10 %) | 360 | Drop only the redundant variance equation. |
| 3.8 | Crossover point | 336 | own model + limits | KEEP (≈−10 %) | 300 | Drop the repeat of the table's 105×/233×. |
| 3.9 | Connections | 282 | connections + repetition | TRIM ≈45 % | 155 | Convergence paragraph repeats 3.7; fix "every variant outputs the average" (Bowling 2015). |

### Chapter 4 — Game Abstraction & Scaling (5 259 → ~3 117)
Spine: Δ_abs, merge-then-measure (three levels × three tools), blueprint + live patches, the Leduc results including the honestly flagged action-abstraction harness. No other file cites §4.x by number.

| § | Section | Words | Type | Verdict | Target | Reason |
|---|---|---:|---|---|---:|---|
| 4.1 | Why abstraction | 407 | expl. + numbers + recap | CONDENSE | 230 | Drop ch. 1–3 recap and three-factor bullets; keep 3.16×10¹⁷, ~10¹⁶¹, the recipe. |
| 4.2 | Routes to abstraction | 439 | own IB framing + table | TRIM ≈30 % | 300 | Keep IB equation and β list; drop two table rows; absorb 4.13 as a row. |
| 4.3 | Axes (lead) | 47 | connections | CONDENSE | 25 | One sentence. |
| 4.3 › | Information abstraction | 135 | meta + aside | CONDENSE | 50 | Keep node-map vs traversal; drop meta text and box. |
| 4.3 › | Action abstraction & translation | 418 | retelling + catalogue | CONDENSE | 220 | Keep 0.7×pot example, one line per translator, Tartanian; drop pseudo-harmonic formula. |
| 4.4 | Exploitability gap | 228 | definition | TRIM ≈40 % | 140 | Drop restated exploitability formula and box; keep Δ_abs. |
| 4.5 | EMD primer | 348 | own expl. + history | TRIM ≈45 % | 190 | Keep sand-pile analogy and HSD example; drop Monge→WGAN history. |
| 4.6 | Merging criterion (lead) | 50 | read-more | CONDENSE | 15 | Drop links. |
| 4.6 › | Level 1 lossless | 132 | own expl. + example | TRIM ≈30 % | 90 | Keep red/black Jack example; drop box. |
| 4.6 › | Level 2 bounded | 109 | own expl. + example | TRIM ≈35 % | 70 | Keep J/Q example; drop box. |
| 4.6 › | Level 3 empirical | 135 | retelling + repetition | CONDENSE | 70 | Keep 2.4×10⁹ and the Waugh pathology. |
| 4.7 | Error budget (lead) | 74 | read-more | CONDENSE | 30 | Drop links. |
| 4.7 › | Tool 1 bound | 103 | own expl. | TRIM ≈40 % | 60 | Reach-weighting explained once. |
| 4.7 › | Tool 2 EMD proxy | 63 | own result | KEEP | 55 | EMD 0 while exploitability 0.38–0.57. |
| 4.7 › | Tool 3 CFR-BR | 110 | literature (Chapter I) | TRIM ≈35 % | 70 | Keep "as low as 1/3". |
| 4.8 | Choosing in practice | 252 | retelling + repetition | TRIM ≈45 % | 140 | Keep NP-complete/k-centre and distribution-aware finding. |
| 4.9 | Build-time (lead) | 40 | read-more | CONDENSE | 10 | One line. |
| 4.9 › | GameShrink | 163 | retelling + expl. | CONDENSE | 90 | Keep signal-tree reason, 6.6 M vs 3.1 B. |
| 4.9 › | HSD+EMD+k-means | 269 | own figure + result | TRIM ≈25 % | 200 | Keep figure, 0.574 vs 0.571, blueprint definition. |
| 4.10 | Runtime patching (lead) | 59 | read-more | CONDENSE | 35 | Keep Libratus sentence. |
| 4.10 › | Coin Toss | 134 | own counterexample | KEEP (light) | 115 | The one intuition for why naive re-solving fails. |
| 4.10 › | Safe subgame solving | 133 | retelling | CONDENSE | 70 | Keep blueprint anchoring; ch. 6 covers the rest. |
| 4.10 › | Nested subgame solving | 196 | retelling + cited number | TRIM ≈45 % | 110 | Keep 119–150 vs 1 465 mbb/hand. |
| 4.11 | Architecture | 159 | repetition | CONDENSE | 70 | Keep "used since 2017 … DeepStack the exception". |
| 4.12 | Practical validation | 626 | own results | TRIM ≈25 % | 470 | Implementation list → one sentence; keep harness caveat and every number. |
| 4.13 | Deep RL counterparts | 151 | forward pointers | MERGE→4.2 | 0 | One row in the 4.2 table. |
| 4.14 | Connections | 237 | connections | TRIM ≈35 % | 150 | Keep ch. 6 vocabulary and the Pareto-methodology paragraph. |

### Chapter 5 — Neural Networks for Imperfect-Information Games (6 199 → ~3 430)
Spine: table-vs-network crossover, non-stationarity/deadly triad, own capacity and silent-failure results, Deep CFR and NFSP with Leduc numbers, the four-family map. Keep every ### heading (in-chapter references 5.2.5, 5.3.4). No `report_en.md`.

| § | Section | Words | Type | Verdict | Target | Reason |
|---|---|---:|---|---|---:|---|
| (intro) | Framing | 147 | boilerplate + scope | CONDENSE | 60 | Keep scope and deferred-implementation note. |
| 5.1 | Why neural networks | 216 | own expl. + result | TRIM ≈30 % | 150 | Numbers stated once (Deep CFR subsection). |
| 5.2 › | NN fundamentals | 591 | textbook | CONDENSE | 230 | Keep layer equation, gradient descent in words, one overfitting line. |
| 5.2 › | Putting it together on Leduc | 257 | own worked example | TRIM ≈40 % | 150 | Keep the 30-number encoding walk-through. |
| 5.2 › | Non-stationarity & deadly triad | 239 | own expl. + link | TRIM ≈35 % | 160 | Back-reference ch. 1 for target network/replay. |
| 5.3 › | Inductive bias | 269 | own expl. | CONDENSE | 110 | One mapping sentence. |
| 5.3 › | Layer types | 782 | textbook + retelling | TRIM ≈50 % | 380 | One paragraph per family + Deep Sets recipe. |
| 5.3 › | Encoding state & history | 544 | own expl. + textbook | TRIM ≈50 % | 280 | Keep one-hot vs embedding and no-leakage rule. |
| 5.3 › | Sizing & capacity | 646 | own result + textbook | TRIM ≈45 % | 360 | Keep 1.14 vs 1.49, figure, start-small recipe; drop shape catalogue. |
| 5.3 › | Training stability | 382 | own result + defs | TRIM ≈30 % | 260 | Keep reservoir sampling and the silent-bug story. |
| 5.4 › | Tabular → approximation | 183 | repetition | CONDENSE | 90 | "Two tables become two networks." |
| 5.4 › | Deep CFR & variants | 566 | retelling + own result | TRIM ≈35 % | 380 | Keep mechanics, loss, own Leduc figure; omit the reproduced Steinberger figure. |
| 5.4 › | NFSP | 302 | retelling + own result | TRIM ≈30 % | 210 | Keep two-network idea and own result. |
| 5.4 › | Trade-offs | 296 | repetition | CONDENSE | 150 | Keep wide-shallow vs deep caveat. |
| 5.5 › | Four SOTA families | 204 | frame + table | TRIM ≈30 % | 140 | Keep the table (Chapter I candidate). |
| 5.5 › | PSRO/NFSP/XFP | 181 | retelling (ch. 9) | CONDENSE | 80 | Pointer to ch. 9. |
| 5.5 › | ReBeL & SoG | 177 | retelling (ch. 6) | CONDENSE | 80 | Pointer to ch. 6. |
| 5.5 › | Model-free self-play | 217 | retelling + finding | TRIM ≈25 % | 160 | Keep Rudolph 2026 and the depth argument. |

### Chapter 6 — End-to-End Game AI Architectures (20 648 → ~8 580)
No own experiments. Spine: the seven-year arc as trade-offs on three axes; per system its headline numbers, its one guarantee and its honest caveats (Chapter I rows; ch. 9, 11, 13, 14 cite some); the synthesis tying the systems to C1–C3 and to the opponent-blind and multiplayer-safety gaps. **Structural change:** one shared explanation in 6.1 (why a state has no single value — one worked example; global policy + local re-solve; what "safe" means, pointing to ch. 4; the common guarantee shape), then each system in four short parts plus a two-line legacy.

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| 6.1 | Introduction | 945 | TRIM ≈20 % (host shared explanation) | 750 | Shrink arc paragraph; opponent-blind argument moves to 6.7.3. |
| 6.2 | DeepStack opening + scorecard | 310 | TRIM ≈15 % | 260 | Keep 492 mbb/g, 44 852 hands, non-specialist pros. |
| 6.2.1 | Gap closed | 348 | CONDENSE | 150 | Keep Claudico −91, LBR > 3 000. |
| 6.2.2 | Architecture | 251 | MERGE→6.2.3 | 80 | Offline labelling / online re-solving in two sentences. |
| 6.2.3 | Continual re-solving | 569 | TRIM ≈45 % | 300 | Keep "do nothing on the opponent's action" and the k₁ε+k₂/√T bound. |
| 6.2.4 | Caveats | 347 | TRIM ≈50 % | 170 | Keep "sparse actions void Theorem 1", self-play-values gap. |
| 6.2.5 | Compute | 207 | CONDENSE | 40 | One line. |
| 6.2.6 | Strengths & limits | 223 | MERGE→6.2.4 | 90 | Keep "LBR fails", AIVAT 85 % (ch. 14). |
| 6.2.7 | Legacy | 393 | CONDENSE | 70 | Keep range/value → C1, bound → C2. |
| 6.3 | Libratus opening + scorecard | 378 | TRIM ≈40 % | 230 | Keep 147 mbb/g, 120k hands, 99.98 %. |
| 6.3.1 | Gap closed | 303 | CONDENSE | 70 | Already told in 6.2.1 and ch. 4. |
| 6.3.2 | Architecture | 618 | TRIM ≈65 % | 200 | Three modules, 10¹⁶¹→10¹², self-improver ≠ exploitation. |
| 6.3.3 | Nested safe solving | 657 | CONDENSE | 180 | Ch. 4 teaches it; keep the 2Δ equation. |
| 6.3.4 | Caveats | 389 | TRIM ≈50 % | 190 | Keep blueprint −8 ± 15 vs +63 ± 28, one unsafe solve. |
| 6.3.5 | Compute | 284 | CONDENSE | 70 | Keep 25 M core-hours split. |
| 6.3.6 | Strengths & limits | 299 | MERGE→6.3.4 | 60 | Keep the as-if-independent significance caveat. |
| 6.3.7 | Legacy | 477 | CONDENSE | 80 | Keep 2Δ → C2, refusal to exploit → C1 foil; drop the flagged depth-limited link. |
| 6.4 | Pluribus opening + scorecard | 462 | TRIM ≈35 % | 300 | Keep 15 pros, 48 mbb/g, 8 days / $144. |
| 6.4.1 | Gap closed | 374 | TRIM ≈45 % | 200 | Keep N-player-Nash-fails (ch. 9, 11) and the C2 gap sentence. |
| 6.4.2 | Architecture | 362 | MERGE→6.4.3 | 90 | Blueprint round 1, depth-limited search elsewhere. |
| 6.4.3 | Continuation strategies | 660 | TRIM ≈55 % | 280 | Keep k = 4, searcher also chooses, "no-regret ⇒ safe only in 2p0s". |
| 6.4.4 | Caveats | 372 | TRIM ≈45 % | 200 | Keep unsafe-search quote, limping and donk-bets (ch. 13). |
| 6.4.5 | Compute | 306 | CONDENSE | 80 | 12 400 core-hours, $144, 2 CPUs. |
| 6.4.6 | Strengths & limits | 371 | MERGE→6.4.4 | 130 | Keep +48 (SE 25), AIVAT ninefold (ch. 14); drop the collusion sentence not in the paper. |
| 6.4.7 | Legacy | 363 | CONDENSE | 70 | Keep the C2 keystone; drop the unverified quote. |
| 6.5 | ReBeL opening + scorecard | 600 | TRIM ≈45 % | 330 | Keep Dong Kim 165 mbb/g, 2p0s proof, open source. |
| 6.5.1 | Gap closed | 448 | CONDENSE | 100 | RPS example moves to 6.1. |
| 6.5.2 | Architecture | 448 | MERGE→6.5.3 | 120 | Self-play loop in three sentences. |
| 6.5.3 | Public belief states | 803 | TRIM ≈50 % | 380 | Keep referee analogy, random-iteration trick, δ-bound. |
| 6.5.4 | Caveats | 456 | TRIM ≈55 % | 200 | Keep "CFR-AVG not known sound", random-belief failure. |
| 6.5.5 | Compute | 349 | CONDENSE | 90 | Hardware in one line; poker code withheld. |
| 6.5.6 | Strengths & limits | 370 | MERGE→6.5.4 | 150 | Keep Slumbot +45, belief input growth (Chapter I gap). |
| 6.5.7 | Legacy | 428 | CONDENSE | 80 | Keep beliefs → types (as thesis proposal), 2p0s frontier → C2. |
| 6.6 | SoG opening + scorecard | 611 | TRIM ≈50 % | 320 | Drop unverified quote and lineage aside. |
| 6.6.1 | Gap closed | 374 | CONDENSE | 90 | Two-traditions story is 6.1's third axis. |
| 6.6.2 | Architecture | 406 | MERGE→6.6.3 | 100 | Point-mass belief, one network. |
| 6.6.3 | Growing-Tree CFR | 921 | TRIM ≈60 % | 380 | Keep two-phase growth, belief-about-the-past intuition, Thm 1. |
| 6.6.4 | Caveats | 503 | TRIM ≈60 % | 200 | Keep 2/400 vs AlphaZero, belief blow-up, known model. |
| 6.6.5 | Compute | 352 | CONDENSE | 70 | One line. |
| 6.6.6 | Strengths & limits | 360 | MERGE→6.6.4 | 110 | Keep Slumbot +7; verify or drop +434 vs LBR. |
| 6.6.7 | Legacy | 594 | CONDENSE | 110 | Keep C1 substrate and C2 links. |
| 6.7 | Synthesis lead | 69 | TRIM | 30 | One sentence. |
| 6.7.1 | Arc in one read | 626 | TRIM ≈45 % | 330 | Keep the added/gave-up table and the metric caveat. |
| 6.7.2 | What carries forward | 214 | TRIM ≈40 % | 130 | Reuse-map caption carries the detail. |
| 6.7.3 | Why this matters for our research | 1 102 | TRIM ≈40 % | 650 | Absorbs 6.1's opponent-blind paragraph; seven ideas → three. |
| 6.7.4 | Open problems & hand-off | 346 | TRIM ≈20 % | 270 | Load-bearing for ch. 7–8. |

### Chapter 7 — Opponent Modeling (5 029 → ~3 590)
Spine: the Bayesian loop with the worked example, the keyhole problem, three models, mean vs mode (§7.5, cited by ch. 8), the four own results (§7.7 cited by ch. 8).

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Opening + where it sits | 206 | CONDENSE | 110 | Keep sensor/actuator framing. |
| 7.1 | Why opponent modeling | 299 | TRIM ≈35 % | 190 | Keep RPS picture; Nash guarantee is ch. 2. |
| 7.1 › | How much is at stake | 318 | TRIM ≈20 % | 250 | Keep 0.21–0.23, 0.11–0.28, 0.004 (Chapter I). |
| 7.2 | Bayesian core | 165 | TRIM ≈15 % | 140 | Keep detective analogy and Bayes' rule. |
| 7.2 › | Type zoo | 114 | KEEP | 105 | Reused in ch. 8, 14. |
| 7.2 › | Update by hand | 103 | KEEP | 103 | The one worked example. |
| 7.2 › | Why Dirichlet | 202 | TRIM ≈35 % | 130 | Keep posterior-mean equation. |
| 7.3 | Keyhole | 351 | TRIM ≈35 % | 230 | Showdown vs fold explained three times → once. |
| 7.4 | Three models | 445 | TRIM ≈33 % | 300 | Keep the table; bullets to one line each. |
| 7.5 | Consistency (lead) | 60 | KEEP | 55 | Cited by ch. 8. |
| 7.5 › | The flaw | 264 | TRIM ≈20 % | 210 | Keep collapse example (Chapter I). |
| 7.5 › | The fix | 346 | CONDENSE | 210 | Keep realization weights, Fy = f, the MAP program. |
| 7.5 › | Практически заключения | 215 | TRIM ≈20 % | 175 | Keep TV 0.004–0.021 and refit cost. |
| 7.6 | Confident and wrong | 254 | TRIM ≈20 % | 200 | Keep "posterior is relative". |
| 7.6 › | Robustness sweep | 277 | TRIM ≈25 % | 210 | Keep the table. |
| 7.7 | Model to money | 650 | TRIM ≈30 % | 450 | Kuhn table repeats 7.1; AlwaysFold, sanity checks, Level-k aside to report. |
| 7.8 | Non-stationary | 460 | TRIM ≈25 % | 350 | Keep both findings and ~60 false resets. |
| 7.9 | Connections | 300 | CONDENSE | 170 | Keep the sensor → actuator hand-off. |

### Chapter 8 — Safe Exploitation (5 806 → ~3 865)
Spine: one LP, different floors; three safety notions and the 2p0s assumption (C2 gap); RNR reconciliation; best equilibrium safe but barely better; Leduc global vs local with the budget caveat; teaching attack lesson.

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Opening | 249 | CONDENSE | 130 | Self-leak recap repeats 8.1/8.9. |
| 8.1 | Why safe exploitation | 472 | TRIM ≈35 % | 300 | Keep dial picture and −0.5. |
| 8.2 | Constrained optimization | 526 | TRIM ≈40 % | 320 | Keep "five methods, one engine" and EV = c·x. |
| 8.3 | Three definitions of safe | 618 | TRIM ≈30 % | 420 | Keep table and prose; RWYWE/BEFFE to two sentences. |
| 8.3 › | Where 2p0s hides | 239 | KEEP | 225 | C2 gap statement. |
| 8.4 | LP & constraint generation | 321 | CONDENSE | 100 | Pseudocode and HiGHS in report; keep 5e-4 slack (ch. 14). |
| 8.5 | RNR bang-bang | 712 | TRIM ≈27 % | 520 | Keep reconciliation, table, figure. |
| 8.6 | Best equilibrium on Kuhn | 870 | TRIM ≈30 % | 600 | Omit smoke-run blockquote and Thresholdish aside. |
| 8.7 | Subgame gadgets | 347 | TRIM ≈28 % | 250 | Caption re-narrates 8.8. |
| 8.8 | Kuhn vs Leduc | 669 | TRIM ≈22 % | 520 | "Did not converge" said three times. |
| 8.8 › | Teaching attack | 387 | TRIM ≈22 % | 300 | Keep +0.051 and 40/40 vs 0/40. |
| 8.9 | Connections | 396 | CONDENSE | 180 | Repeats 8.6/8.8 and ch. 14. |

### Chapter 9 — Multi-Agent RL (5 084 → ~3 320)
Spine: non-stationarity (dance picture), the Markov-game bridge ending in the missing N > 2 anchor, the own results with reconciliations, LOLA as the C1 hook.

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Opening + hooks | 312 | CONDENSE | 170 | Keep the three hooks. |
| 9.1 | Why MARL differs | 427 | TRIM ≈37 % | 270 | MDP recap is ch. 1. |
| 9.2 | Markov games | 406 | TRIM ≈25 % | 300 | Keep tuple, special cases, "what does not survive". |
| 9.3 | Family of methods | 499 | CONDENSE | 220 | Drop chronology and QMIX row. |
| 9.4 | Independent learning | 649 | TRIM ≈26 % | 480 | Explain the orbit once. |
| 9.5 | CTDE | 736 | TRIM ≈32 % | 500 | Textbook CTDE diagram; keep residual table and reconciliation. |
| 9.6 | PSRO | 852 | TRIM ≈30 % | 600 | Kuhn-theorem detail to report; keep both reconciliations. |
| 9.7 | CommNet | 207 | TRIM ≈18 % | 170 | Keep 0.795 vs 0.204. |
| 9.8 | LOLA | 380 | TRIM ≈26 % | 280 | Exploration-run aside to report. |
| 9.9 | Honest notes | 415 | CONDENSE | 180 | Four caveats as one-liners. |
| 9.10 | Key takeaways | 201 | TRIM ≈25 % | 150 | Keep numbers. |

### Chapter 10 — Population Training & EGT (3 798 → ~2 707)
Keep every `##` heading (10.3–10.5, 10.7 are cited).

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Opening | 281 | TRIM ≈40 % | 170 | Keep the three hooks and "league has no guarantee". |
| 10.1 | Why populations | 217 | KEEP | 217 | Wheel, ladder, dojo. |
| 10.2 | Family of methods | 302 | CONDENSE | 150 | Keep the table. |
| 10.3 | Replicator dynamics | 406 | TRIM ≈26 % | 300 | Drop the conceptual diagram. |
| 10.4 | Spinning top | 516 | TRIM ≈28 % | 370 | SVD aside to one sentence; table duplicates chart. |
| 10.5 | League | 553 | TRIM ≈28 % | 400 | Configs in report. |
| 10.6 | Diversity | 274 | CONDENSE | 170 | Table duplicates figure. |
| 10.7 | EGTA | 582 | TRIM ≈26 % | 430 | Drop the flagged pipeline figure. |
| 10.8 | Honest notes | 451 | TRIM ≈29 % | 320 | "What held up" restates 10.3–10.7. |
| 10.9 | Key takeaways | 216 | TRIM ≈17 % | 180 | Fold one bullet. |

### Chapter 11 — Coalition Formation (3 437 → ~2 470)

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Opening | 372 | TRIM ≈41 % | 220 | Keep SLS 1964, coalition-blind gap, hooks. |
| 11.1 | Third player | 344 | TRIM ≈22 % | 270 | Drop Read-more box. |
| 11.2 | Detector | 285 | TRIM ≈33 % | 190 | Keep 10.0 result and untested-false-positive caveat. |
| 11.3 | Shapley credit | 629 | TRIM ≈24 % | 480 | Keep toy table, empty core, tie-break reconciliation. |
| 11.4 | Coalition-aware MAPPO | 755 | TRIM ≈26 % | 560 | Keep equation, sweep, mechanism caveat. |
| 11.5 | EGTA & spinning top | 329 | TRIM ≈30 % | 230 | Drop the pipeline figure. |
| 11.6 | Honest notes | 392 | TRIM ≈29 % | 280 | Keep both corrections. |
| 11.7 | Key takeaways | 331 | TRIM ≈27 % | 240 | Bullet 2 repeats the caveat. |

### Chapter 12 — Sequence Models & LLM Agents (2 073 → ~1 767)
Already lean; almost all own explanation or own results.

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| 12.1 | RL as sequence prediction | 128 | KEEP | 128 | The wanted style. |
| 12.2 | Luck-vs-skill trap | 145 | KEEP | 145 | Worked example + own simulation. |
| 12.3 | ARDT | 269 | TRIM ≈26 % | 200 | Q̃(s,a) relabel in words. |
| 12.4 | Return conditioning | 354 | TRIM ≈10 % | 320 | Minor tightening. |
| 12.5 | LLMs as agents | 514 | TRIM ≈24 % | 390 | Serving specs to report; keep "quantisation unrecorded". |
| 12.6 | Exploitation & limits | 382 | TRIM ≈14 % | 330 | Keep all numbers. |
| 12.7 | Key takeaways | 237 | TRIM ≈11 % | 210 | Merge the Q̃ bullet. |

### Chapter 13 — Behavioural Analysis of Real Hand Histories (5 550 → ~4 010)

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Framing, data | 508 | TRIM ≈35 % | 320 | C1 gap restates 15.2. |
| 13.1 | Solving → reading logs | 204 | KEEP | 200 | Floor-manager analogy, data limits. |
| 13.2 | Data and parser | 409 | CONDENSE | 120 | Keep 99.77 % and the three-conventions lesson. |
| 13.3 | Statistics & sample needs | 490 | TRIM ≈20 % | 390 | Keep split-half test. |
| 13.4 | Gap to Pluribus | 312 | TRIM ≈15 % | 260 | Keep 9.3 vs 3.9 pp. |
| 13.5 | Behavioural cloning | 610 | TRIM ≈15 % | 510 | Reconciliation untouched. |
| 13.6 | player2vec | 592 | TRIM ≈30 % | 420 | Epoch runs in report. |
| 13.7 | Types & online inference | 481 | TRIM ≈15 % | 400 | Keep random-split control. |
| 13.8 | Collusion detection | 856 | TRIM ≈35 % | 560 | Literature to 1–2 sentences. |
| 13.9 | Finding a bot | 426 | TRIM ≈15 % | 360 | AUC list → a range. |
| 13.10 | Honest notes | 430 | TRIM ≈35 % | 280 | Limitations verbatim. |
| 13.11 | Key takeaways | 232 | TRIM ≈20 % | 190 | Keep Chapter I numbers. |

### Chapter 14 — Evaluation Frameworks (4 923 → ~3 700)

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Framing, C3 gap | 310 | KEEP | 290 | Chapter I §1.6. |
| 14.1 | Why it is hard | 351 | TRIM ≈25 % | 260 | Keep negotiator analogy. |
| 14.2 | Framework, readouts, zoo | 773 | CONDENSE | 450 | Readout definitions stay; LLM serving specs to report. |
| 14.3 | Rankings disagree | 590 | TRIM ≈30 % | 420 | Keep Kendall 0.36, clones, α, horizon. |
| 14.4 | AIVAT | 506 | TRIM ≈30 % | 360 | Double-count bug told once. |
| 14.5 | Joint protocol | 670 | TRIM ≈15 % | 580 | Core result. |
| 14.6 | Approximate BRs | 244 | KEEP | 220 | Checklist row 3. |
| 14.7 | Three and four players | 571 | TRIM ≈25 % | 430 | Keep coalition value and DirBR3P numbers. |
| 14.8 | Failure-mode checklist | 201 | KEEP | 200 | Cited by ch. 15. |
| 14.9 | Honest notes | 434 | TRIM ≈35 % | 280 | Ch. 15 notes → one pointer. |
| 14.10 | Key takeaways | 273 | TRIM ≈25 % | 210 | One finding per bullet. |

### Chapter 15 — Research Frontier Mapping (5 035 → ~3 360)

| § | Section | Words | Verdict | Target | Reason |
|---|---|---:|---|---:|---|
| intro | Framing | 348 | TRIM ≈40 % | 200 | "Narrowed two of three" repeated in 15.1. |
| 15.1 | Learning → research | 346 | TRIM ≈20 % | 280 | Refined RQs intact. |
| 15.2 | C1 | 363 | TRIM ≈30 % | 250 | Feasibility → back-references. |
| 15.3 | C2 | 706 | TRIM ≈30 % | 480 | Keep gap, non-claim, three rules, trader analogy. |
| 15.4 | C3 | 360 | CONDENSE | 200 | Reference §14.1, 14.5, 14.8. |
| 15.5 | Pilot 1 | 999 | TRIM ≈40 % | 620 | Keep RWYWE explanation, Chapter I numbers, S. |
| 15.6 | Pilot 2 | 895 | TRIM ≈35 % | 560 | Agent list → names; keep reconciliations. |
| 15.7 | Plan & publications | 441 | TRIM ≈30 % | 300 | Update the stale AAMAS sentence. |
| 15.8 | Honest notes | 349 | TRIM ≈25 % | 260 | Keep limitations and failed predictions. |
| 15.9 | Key takeaways | 228 | KEEP | 210 | Chapter I's source list. |
