# Publication pipeline and first-publication plan (Chapter 15)

*Stage deadlines from the individual study plan (`oldSources/ind_plan_A_Andreev_EN.md`): every
stage ends with "writing and presenting a report (publication of an article)". Stage I — analysis,
Chapter I: 11.2026. Stage II — theoretical research, Chapter II: 04.2027. Stage III — practical
solving, Chapter III: 01.2028. Stage IV — experimental research, Chapter IV: 08.2028. General
conclusions 09.2028; formatting 12.2028; abstract 01.2029; preliminary defence 02.2029; defence
04.2029.*

*Venue dates. Verified 2026-09-25 on the official pages: AAMAS 2027 main track — abstracts
1 Oct 2026, papers 8 Oct 2026, notification 21 Dec 2026, conference 3–7 May 2027 (Hanoi).
IEEE CoG 2027 — full papers 1 Mar 2027 (Aizuwakamatsu; from the search listing of the official
site, conference dates differ between listings — confirm). University of Ruse 65th Annual
Scientific Conference — 23–24 Oct 2026, proceedings "Proceedings of the University of Ruse"
(submission deadline not shown — confirm with the supervisors). CompSysTech (University of Ruse)
— 2026 edition's deadline was 30 Mar 2026; the 2027 date is not yet announced. All other dates
are **estimates from the annual cycle** and must be confirmed when the calls appear; aggregator
sites were found unreliable (one "ICML 2027" call on them belongs to a linguistics conference).
The national minimum requirements for the degree (points per publication type, indexing) were
not checked here and should be confirmed with the supervisors.*

## The pipeline

| # | Working title | Contribution → chapter | Venue (deadline) | Content source | Stage it serves |
|---|---|---|---|---|---|
| 1 | **Gain, speed and exposure: evaluating adaptive agents in two- and three-player imperfect-information games** | C3 → Ch. IV (definitions in Ch. II) | IEEE CoG 2027, full paper (1 Mar 2027). Stretch: AAMAS 2027 (8 Oct 2026) only if a full draft exists by 30 Sep 2026 | Chapter 14's protocol and failure modes; Chapter 15's RWYWE result (match-level safety) | II (submitted before 04.2027) |
| 2 | **What hand histories reveal: re-identification, collusion and bot detection on two million online poker hands** | C1 (data side) + fair play → Ch. III | IEEE Transactions on Games (journal, rolling; submit 06.2027), or IEEE CoG 2028 (est. Mar 2028) if Playtech data arrive and are added | Chapter 13 (IPN + Pluribus; injected colluders) | III |
| 3 | **Safe exploitation beyond two players: maximin-floor gift accounting and baseline-relative loss caps in three-player poker** | C2 → Ch. II | IJCAI-ECAI 2027 (est. Jan 2027) or, if not ready, AAMAS 2028 (est. early Oct 2027) | Chapter 15 pilots P2 extended by Experiments 2.0–2.1 (three-player Kuhn exact; three-player Leduc with a learned coalition exploiter) | II / III |
| 4 | **Within-match opponent inference with a safety budget in N-player poker** | C1 → Ch. III | NeurIPS 2027 (est. May 2027) or AAAI-28 (est. Aug 2027) | Experiment 1.1 (+ 1.2 real-data arm) | III |
| 5 | **Detect, then bound: coalition-aware exploitation against colluding opponents** | C2 × C1 → Ch. III–IV | AAMAS 2028 (est. early Oct 2027) or IEEE CoG 2028 (est. Mar 2028) | Experiment 2.2 | III / IV |
| 6 | **A cross-game protocol for evaluating adaptive and colluding agents in imperfect-information games** | C3 → Ch. IV | JAIR, TMLR or IEEE Transactions on Games (journal; submit 06–08.2028) | Experiment 3.1 with C1/C2 agents as subjects | IV |

Local reports (the "report (publication of an article)" of each stage, if the supervisors want
a University of Ruse venue in addition): the 65th Annual Scientific Conference (Oct 2026) for a
short Bulgarian paper on Chapter I's analysis and the three gaps; CompSysTech 2027 (est.
Mar 2027) for a short paper on the two-player safe-exploitation baseline (Experiment 2.0), which
is complete now.

Readiness today (September 2026): Paper 1 — results complete (Chapters 14–15), needs writing;
Paper 2 — results complete (Chapter 13), needs a data decision; Paper 3 — pilot complete for
three-player Kuhn, Leduc arm to build; Papers 4–6 — designed.

## The first publication — plan

**Choice: Paper 1, the joint evaluation protocol (C3), with the RWYWE result.**

**Why this one and not Chapter 13's pipeline.**

1. *It is the yardstick for everything after it.* Papers 3–6 measure their agents with this
   protocol; publishing it first lets them cite a reviewed definition instead of re-arguing it.
2. *It is complete and exact.* Every number comes from exact computation on games enumerated from
   OpenSpiel and validated against OpenSpiel and five earlier chapters; nothing depends on data
   access, labels or licences.
3. *It carries the thesis's framing.* Adaptation versus safety, and the three-player coalition
   exposure, are the core of C1 and C2; a reader of Paper 1 sees the research programme.
4. *Chapter 13's paper is stronger later.* Its real-data results lack labels (IPN 2009) and its
   headline would change if the Playtech data arrive; waiting costs little.
5. *Risk, and how it is handled.* C3's gap is narrowed (the RRPS benchmark already combines return
   and exploitability for one game). The paper therefore leads with the failure modes — each
   existing metric misses a named, reproduced failure — and with what RRPS does not have:
   N-player coalition exposure, within-match speed and recovery, and match-level safety.

**Venue.** IEEE CoG 2027 full paper (8 pages + references; deadline 1 Mar 2027). CoG is the main
games-AI venue, fits the dissertation's official topic ("AI in computer games"), and its
deadline falls inside Stage II, after Chapter I is delivered. **Stretch option:** AAMAS 2027 main
track (abstract 1 Oct, paper 8 Oct 2026; 8 pages), which would make Paper 1 the Stage I article —
only if a complete draft exists by 30 Sep, because Chapter I (26 pages) is due in the same month.
If rejected from AAMAS, the reviews feed the CoG version.

**Title (working).** *Gain, speed and exposure: evaluating adaptive agents in two- and
three-player imperfect-information games.*

**Content (8 pages).**

1. Introduction (0.75 p): why adaptive agents break exploitability, rankings and NashConv; the
   failure-mode list (Chapter 14's checklist); contributions.
2. Related work (0.75 p): worst case, variance reduction, population ratings, RRPS, opponent-
   modelling protocols; the gap.
3. The protocol (1.5 p): readouts (gain, capture, h50/r50, exposure / coalition value,
   match-level safety, confidence); the exact engine; the zoo; switching, teaching and colluding
   opponents.
4. Results on Kuhn and Leduc (2 p): rankings disagree (Elo vs exploitability τ = 0.36 on Leduc);
   gain/exposure separates BestEq, RNR, DirBR; teaching attack; RWYWE — safe over the match while
   its per-hand loss after a switch is positive (the reason for match-level safety);
   confidence (hands per window, AIVAT; Pluribus hands).
5. Three players (1.5 p): NashConv ≈ 0 equilibria lose 0.06–0.17 chips/hand more to a pair; the
   adaptive agent that tops Elo and Nash averaging loses 0.47 under a coalition teaching attack;
   maximin value as a reference line.
6. Limitations and outlook (0.5 p): toy games, learned exploiters with budgets for larger games.
7. Reproducibility statement: code and seeds.

**Length.** 8 pages + references (CoG full paper); an AAMAS version would be 8 pages + references
in the AAMAS format.

**Milestones.** Outline and figures from Chapters 14–15: 10.2026 (in parallel with Chapter I);
full draft: 01.2027; supervisor review: 02.2027; submission: 1 Mar 2027.
