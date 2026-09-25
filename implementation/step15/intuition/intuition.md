# Chapter 15 — Intuition: from a learning programme to a research programme

## The problem in one paragraph

Fourteen chapters built a toolbox: how to compute equilibria, how to model an opponent, how to
exploit one safely, how to handle more than two players, how to read real hand histories, and how
to evaluate agents that adapt. A PhD is not a toolbox. It is three claims that nobody has made
before, each backed by a method and by evidence, and each defensible against the question "hasn't
this been done?". Frontier mapping is the act of placing every tool against the published
literature and asking, for each intended contribution: what exists, what exactly is missing, what
the thesis will do about it, what already shows it can be done, and what could go wrong. Contribution
design turns the answer into experiments and papers *before* running them, so the contribution
shapes the experiment rather than the other way round.

## A mental picture

A map of a coastline being surveyed. The surveyed coast is the literature; the thesis wants to plant
three flags on unclaimed ground. The April 2026 plan drew the coast from memory and placed the flags
generously. The September 2026 survey (`lit_gaps.md`) found that other expeditions had landed near
two of them: real-time opponent modelling exists in two-player games, and evaluation that combines
return with exploitability exists for one game. The flags move inland — to N players, to shifts
within a match, to coalition-aware and match-level measures. The third flag, safe exploitation with
more than two players, still stands on open ground, but the survey also found fences around it:
equal share cannot be guaranteed, and the only worst-case notion for coalitions is the conservative
team-maxmin value.

## Approaches to "safe" with more than two players, compared

| Notion | What it promises | Weakness | Source |
|---|---|---|---|
| Nash equilibrium | nothing individually: equilibria are many, and a pair can shift utility inside the family | no guarantee at all | Szafron et al. 2013; Brown & Sandholm 2019 |
| Equal share C/n | a fair share of the total | provably not securable against heterogeneous opponents | Ge et al. 2025 |
| Team-maxmin (maximin against a coordinated pair) | a real worst-case guarantee, even against colluders | reputed very conservative; needs a coalition best-response oracle | Celli & Gatti 2018; Zhang et al. 2021, 2023 |
| Ganzfried–Sandholm gifts with the maximin floor | exploit, while the match stays above the maximin value | stated, not evaluated, in G&S 2015 § 2.3 | this chapter's pilot P2 |
| Baseline-relative regret / loss caps | never much worse than the baseline against the same opponents | relative, not absolute: the baseline itself can lose to colluders | Müller et al. 2025; pilot P2 |
| KL anchoring | stay behaviourally close to an anchor | no loss bound; piKL's anchor is a human policy | Jacob et al. 2022; Bakhtin et al. 2023 |

## How the field got here (the safe-exploitation thread)

- 2004 — ε-safe strategies (McCracken & Bowling): exploit within a risk budget.
- 2007 — restricted Nash response (Johanson, Zinkevich & Bowling): a tunable frontier between
  exploitation and exploitability.
- 2012/2015 — Ganzfried & Sandholm: safety over the *repeated* game; deviating beyond equilibrium is
  safe exactly when the opponent has given "gifts", and RWYWE risks only those.
- 2022 — safe subgame refinement (Liu et al.); 2024 — adaptation safety for nested search
  (OX-Search, Ge et al.).
- 2025 — equal share and its impossibility (Ge, Wang, Li & Jin); baseline-relative regret
  (Müller et al.).
- 2026 — per-deployment certificates (Li & Huang, preprint). Still two-player.

## Easy to get wrong

- "Equal share is guaranteed." It is a target; against opponents who play differently it is
  provably not securable.
- "piKL keeps the policy near Nash." It keeps it near a human-imitation policy.
- "Safe means every hand is safe." Ganzfried–Sandholm safety is per period *in expectation over
  the match*; a gift-banking agent may lose after an opponent switches and still be safe overall.
- "A tie in an LP is harmless." Among equally good equilibria the solver may return a degenerate
  one (never bluff, never bet the best hand), which a slightly different opponent punishes
  (`EXECUTION_NOTES.md`, surprise 1).
- "Nobody adapts." The landmark systems do not; plenty of two-player work does.

## You should be able to answer

1. Which of the three contributions is open at the core, and which two are narrowed — and by what?
2. Why is equal share a reference line and not a guarantee?
3. What does RWYWE risk, and why is its safety a property of the whole match?
4. What is the team-maxmin value, and why is it the natural N-player replacement for v*?
5. What is the first publication, and why that one?

## Key takeaways for the final summary

- The contributions are claimed at the level the September 2026 check allows: C1 = N-player,
  within-match, safety-coupled inference; C2 = N-player exploitation with a stated, checked loss
  criterion, tested against colluders, no general theorem; C3 = a joint protocol that catches the
  failures of existing measures across two- and three-player games.
- Safety with more than two players has to be relative (to a baseline) or conservative (the
  maximin value against a coordinated pair); the thesis uses both and reports equal share only as a
  reference line.
