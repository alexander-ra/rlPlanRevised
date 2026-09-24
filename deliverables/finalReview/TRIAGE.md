# Final review — triage (2026-09-24)

13 reviews (steps 01–12; step 06 in two halves) + 2 literature reports. **973 findings:
288 S1 · 589 S2 · 96 S3.** Every Bulgarian quote was script-checked against the sources;
every citation proposed was verified by the reviewer (method stated in each finding).

| Step | S1 | S2 | S3 | Step | S1 | S2 | S3 |
|---|---:|---:|---:|---|---:|---:|---:|
| 01 | 11 | 41 | 7 | 07 | 22 | 55 | 7 |
| 02 | 15 | 23 | 5 | 08 | 22 | 46 | 6 |
| 03 | 18 | 33 | 8 | 09 | 27 | 46 | 10 |
| 04 | 15 | 40 | 6 | 10 | 24 | 42 | 7 |
| 05 | 24 | 39 | 11 | 11 | 24 | 37 | 5 |
| 06a | 30 | 81 | 9 | 12 | 21 | 40 | 6 |
| 06b | 35 | 66 | 9 | | | | |

What the review found, in one paragraph: the Bulgarian text is fluent but carries real
meaning errors, about half of them from wrong entries in the settled glossary; **no figure
is legible at print size** (labels at 3–7 pt against 10.9 pt body text) and ~30 print
entirely in English because their BG versions were never generated; and, more seriously,
**several chapters' own experimental conclusions do not hold** — a harness bug (04), a
baseline mistaken for the method (08), a vacuous credit signal (11), results misread from
their own data (03, 05, 10, 12). Those are listed in § B because they are the candidate's
call.

---

## A. Decisions — glossary and typography

→ `GLOSSARY_DECISIONS.md`: ~100 rows, 3 open choices (❓ 1.10 blueprint, 2.3 self-play,
2.5 bootstrapping), everything else recommended (✅). Plus § 5 typography/bundle policy.

## B. Decisions — findings that change results (code, reruns)

Each has two options: **fix** (change code, rerun, update numbers) or **caveat** (keep the
run, rewrite the text so it claims only what the run shows). The reviewers drafted the
caveat text in every case, so "caveat" costs nothing extra.

| # | Step | Finding | What is wrong | Fix effort | Recommend |
|---|---|---|---|---|---|
| R1 | 08 | F08-C01 | The method labelled "Ganzfried" imposes the safety floor per hand, which admits only equilibrium strategies: it is Ganzfried & Sandholm's *best-equilibrium baseline* (their § 6.3), not their safe-exploitation algorithms (RWYWE, BEFFE), which risk only gifts already won. Hence the tiny gains (+0.002/hand). Verified in the code and the paper. | Small: RWYWE = the existing LP with a floor $v^* - k_t$ that moves with banked gifts; rerun the Kuhn/Leduc comparison. | **Wave 3: text correction** (name it the best-equilibrium baseline, say what RWYWE would add). **Implementing and running RWYWE stays with the candidate:** the step-08 solvers are marked "thesis foundation — must own every line", and `implementation/WORKFLOW.md` reserves experiment runs for the candidate. It is the C2 two-player baseline, so it is worth doing soon. |
| R2 | 08 | F08-C02 | The Leduc headline "global doesn't scale, local does" compares a 40-iteration cap with a 400-iteration one. | Rerun at equal budget. | **Wave 3: caveat**; the equal-budget rerun goes with R1, by the candidate. |
| R3 | 04 | F04-C01 | The action-translation harness calls every translator with the bet equal to the upper bound, so all three return the same mapping (identical 1.40153… in the results) and the agent plays its own small bets at 2×pot. "Translation error dominates" measures the bug. Verified in the code. | Moderate: fix `_strategy_with_translation`, rerun day-03 + mini/extended panels. | **Caveat now**, fix later if time. Ch. 4 does not feed a contribution; the caveat text is ready. |
| R4 | 11 | F11-C01/C02 | The printed reward formula is inverted relative to the code. The "Shapley coalition credit" is an additive game (each player's credit = own win probability), so it carries no coalition information; "coalitions can be learned" is not shown. Verified in the code. | Research-sized: a credit built on the detector's help/harm matrix + a coalition-free dense-reward control. | **Caveat now** (formula fixed, mechanism caveat added). The real fix is C2 research for Chapter II–III — worth noting there as an open item. |
| R5 | 05 | F05-C01/C02 | "Advantage losses fell" — they rose (~20 → 1 600); the "random level" 1.69 is not uniform random (2.37); the "patched" Deep CFR 64×64 numbers equal the unpatched ones. | Rerun Deep CFR (hours). | **Caveat now**; drop the patched numbers until rerun. |
| R6 | 02, 03 | F02-G03, F03-G0x | Figures cannot be regenerated in BG: plotting retrains, MCCFR is unseeded, curve data were not saved. Seeded reruns slightly change the one-pager numbers. | Small (Kuhn/Leduc CFR, minutes–an hour): add seeds + save curves + plot-only mode, rerun, update numbers. | **Fix** — otherwise 9 figures stay English. The one allowed exception to "agents do not run experiments": seeded reruns whose only purpose is regenerating figure data; stop and log if one takes over 30 minutes. |
| R7 | 10 | F10-C01…C04 | Four conclusions contradict the chapter's own data (the meta-Nash mixture is *better* than self-play, not the weakest; "mixing adds tells" wrong; best-of-run vs final iterate; rest points ≠ Nash in general). | None — the right numbers are in the results files. | **Text fix** (applied in wave 3). |
| R8 | 12 | F12-C01…C08 | "LLM 0.833" is the scripted stub (real models 0.25–0.33); the Kuhn "collapse" is a spike; ARDT fix never run; "no in-context adaptation" rests on one run. | None. | **Text fix.** |
| R9 | 03 | F03-C01…C05 | Crossover arithmetic off ×2; "×slower" is an accuracy ratio; the limit hold'em claims contradict Bowling et al. 2015 (solved by full-traversal CFR+). | None. | **Text fix.** |

## C. Applied without further decisions (wave 3)

Everything else, once A is settled: all B (Bulgarian), the T occurrences, S (sources — only
verified citations), X (structure), text-only C, and G (figures). S3 findings are applied
only where trivial. Per-chapter Opus 5.5 agents, each owning its step's files.

**Central engineering first (this session, before the per-chapter agents):**
1. Glossary files updated from `GLOSSARY_DECISIONS.md`; `figure_labels.json` merged from all
   G findings (one owner — it is shared by every chapter).
2. BG diagram text: wrap/enlarge boxes instead of overflowing; font floor fs ≥ 9.6.
3. Build: en dash, decimal comma, per-chapter footnote labels, and the `⟦MATHI…⟧`
   placeholders the pipeline left in steps 06, 08, 09.
4. Plotting scripts that the BG renderer cannot run (`plotting.py` in 02, 07, 10, 12 — no
   `__main__` or argparse clash) so every figure gets a BG twin.
5. The 76 figure captions translated (drafts are in the reviews).

**Then:** per-chapter fix agents → rebuild → `check_headings`, `check_captions`,
`render_printed.py` legibility pass → the candidate proofreads the BG bundle.

## D. Chapter I inputs — ready now

`stepNN_extract.md` × 13 + `lit_gaps.md` + `lit_evaluation.md` (+ comparison-table rows for
DeepStack, Libratus, Pluribus, ReBeL, SoG). Chapter I does not depend on wave 3 except that
own-evidence numbers must be the corrected ones (the extracts already use them, and flag
the R-items as "do not cite until rerun").
