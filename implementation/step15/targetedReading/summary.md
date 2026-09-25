# Chapter 15 — Targeted reading: reading for positioning

Reading here is not for learning an algorithm but for *placing the thesis*: for every source, the
question is "where does my contribution sit relative to this?". The plan's list (raw step 15,
Phase 3) is corrected where the September 2026 check found errors (see the frontier map, § 10).
Verification: Ganzfried & Sandholm (2015) was read in full for this chapter (authors' PDF,
2026-09-25). The other entries rely on `deliverables/finalReview/lit_gaps.md` and
`lit_evaluation.md` (verified 2026-09-24) and were not re-read; each says so.

---

## 1. Ganzfried & Sandholm (2015) — "Safe Opponent Exploitation"

*ACM Transactions on Economics and Computation 3(2), Article 8, 28 pp., DOI 10.1145/2716322
(EC'12 conference version). Read in full.* **Role:** the two-player safety definition that C2
generalises, and the baseline Chapter 8 lacked.

- **Key idea.** Safety is defined over the repeated game (Def. 4.1: at least v* per period in
  expectation, against any opponent). Deviating from a stage-game equilibrium can be safe exactly
  when the opponent plays "gift" strategies (a strategy that is not a best response to some
  equilibrium strategy of ours); then one can risk what the gifts have won.
- **Algorithms (§ 6).** RWYW (risk realised winnings) — not safe (Prop. 6.1; a counter-example in
  rock–paper–scissors, where luck is mistaken for gifts). RWYWE (Alg. 2): play the k_t-safe best
  response to the model; k_{t+1} = k_t + u(π_t, a_t) − v* with the expectation over *our*
  randomisation — safe (Prop. 6.4, via E[k_{T+1}] = Σ u(π_t, τ_t) − Tv* and k ≥ 0). Best
  equilibrium (§ 6.3) — safe, but "can only exploit the opponent as much as the best equilibrium
  can". BEFFE (Alg. 3) and BEFEWP (Alg. 4) — safe hybrids that switch to a full best response when
  the bank covers its exploitability.
- **Extensive form (§ 8).** The update needs the opponent's play off the path: assume a nemesis
  there, constrained to the observed actions (Alg. 5); with private information observed at the
  end, constrained to the observed card (Alg. 6, Prop. 8.7); unobserved, constrained to "some"
  card (§ 8.2.2). Gifts can also be detected within a hand (§ 8.3).
- **Generality (§ 2.3).** "For general-sum and multiplayer games, our methodology applies
  straightforwardly if we replace the minimax value with the maximin value." Stated, not tested.
- **Headline result (§ 9, Table I).** Kuhn, 40,000 opponents per class, 1,000 hands, card
  observed: against random opponents RWYWE 0.3636, BEFEWP 0.3553, BEFFE 0.1995, best equilibrium
  0.1450, best response 0.4700 $/hand; against dynamic opponents (random, then a nemesis) the safe
  algorithms stay above v* = −0.0556 (RWYWE −0.0204) while the best response falls to −0.1209.
- **Positioning.** C2's two-player baseline (Experiment 2.0, pilots P0–P1) and the source of the
  maximin-floor construction tested in pilot P2.
- **Verify when you read it.** The numbering of the gift definition (Def. 5.2 in the TEAC version,
  per the step-08 review); the proof of Prop. 8.7 ("identical reasoning" to Prop. 8.3).

## 2. Ge, Wang, Li & Jin (2025) — "Securing Equal Share"

*ICML 2025; arXiv:2406.04201. From lit_gaps (arXiv HTML, Props. 4.1–4.2 checked there).* **Role:**
the N-player objective the plan wanted as C2's guarantee. **Key point:** equal share C/n is
achievable with no-regret learning only if all opponents play the same strategy and do not adapt
arbitrarily fast; it cannot be secured against opponents playing different fixed strategies (Prop.
4.1) or adapting arbitrarily (Prop. 4.2). Experiments on three-player Majority Vote and a
30-player game; no exploitation, no imperfect-information testbed. **Positioning:** a reference
line in C2's figures, not a guarantee (a colluding pair is exactly the heterogeneous case).

## 3. Ge, Xu, Ding, Meng, An, Li & Gao (2024) — OX-Search

*ICML 2024, PMLR 235, 15255–15270. From lit_gaps and the step-08 extract.* **Role:** adaptation
safety (no more exploitable than the blueprint) and the "taught and exploited" motivation for
teaching attacks. **Positioning:** two-player; its blueprint-relative idea is what C2's
baseline-relative cap generalises (relative to a blueprint, against coordinated opponents). The
plan's attribution to "Ge, Kovařík & Lisý" and its arXiv link are wrong.

## 4. Team-maxmin: Celli & Gatti (2018); Zhang, An & Černý (2021); Zhang, Farina & Sandholm (2023)

*AAAI 2018; AAAI 2021; ICML 2023. From lit_gaps.* **Role:** the only worst-case notion against a
coordinated coalition. **Positioning:** in pilot P2 the team-maxmin value of each three-player
Kuhn seat is computed exactly (constraint generation with an enumeration oracle) and used as the
floor of G&S's construction.

## 5. Jacob et al. (2022) piKL; Bakhtin et al. (2023) DiL-piKL

*ICML 2022; ICLR 2023. From lit_gaps.* **Role:** the plan's proposed C2 mechanism.
**Correction:** the anchor is an imitation-learned human policy, for human compatibility, with no
exploitability or loss bound. **Positioning:** KL anchoring *to an equilibrium blueprint* is the
thesis's own proposal; its two-player relatives are RNR's mixture, magnetic mirror descent and
StratFormer's schedule. In pilot P2 it is a measured rule (KL(β)), not a bounded one.

## 6. Müller et al. (2025) — "Best of Both Worlds"

*ICML 2025; arXiv:2502.11673. From lit_gaps.* **Role:** baseline-relative safety: O(1) regret
against a given comparator while gaining Ω(T) from exploitable opponents, in two-player zero-sum
games with bandit feedback. **Positioning:** the conceptual source of C2's baseline-relative loss
criterion; the thesis checks such a criterion exactly against coordinated opponents in a
three-player game.

## 7. Babyak et al. (2024) — synchronous vs asynchronous coalitions

*arXiv:2412.19855 (the arXiv title misspells "Sychronous"). From lit_gaps.* **Role:** coalition
values depend on communication. **Positioning:** the colluder types of Experiment 2.2 (a fixed
coalition best response = full ex-ante coordination; soft play and dumping = weaker forms).

## 8. Lanctot et al. (2023a) — VasE; Lanctot et al. (2023b) — RRPS

*arXiv:2312.03121 (no venue confirmed); TMLR 2023. From lit_evaluation.* **Role:** how an
evaluation paper is made publishable (axioms, comparison with alternatives, surprising failures of
existing methods) and the nearest precedent for C3. **Positioning:** Paper 1 follows the same
pattern with failure modes in place of axioms.

## 9. Not done

The plan's calibration reading of recent PhD dissertations (Bowling, Sandholm, Tuyls groups) was
not carried out: no dissertation was read and none is cited. It remains useful for scoping the
number and depth of contributions and is left to the candidate.

## Synthesis

Two-player safe exploitation has three ingredients: a *reference value* (v*), a *bank* of what
the opponent's mistakes have provably given (gifts), and a *solver* for the best response within
the bank (the safe-best-response LP). With more than two players the reference value is the
problem: equal share cannot be secured, and equilibria guarantee nothing. The two replacements
available are the team-maxmin value (absolute, conservative, needs a coalition oracle) and a
baseline (relative, only as safe as the baseline). The G&S bank and the LP carry over to both.
That is the design space of C2, and the pilots test a first cut of each.

## Key takeaways for the final summary

- RWYWE's safety is a match-level property: banked gifts may be spent after a switch.
- G&S already suggest the maximin value for multiplayer games (§ 2.3); what the thesis can add
  there is the coordinated-coalition floor, exact checks and a test against colluders — not the
  idea itself.
- Equal share is a reference line; piKL is behavioural anchoring to a human policy; the plan's
  other statements are corrected in the frontier map.
