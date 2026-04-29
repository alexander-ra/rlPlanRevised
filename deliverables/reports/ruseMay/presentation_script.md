# Presentation Script — May 2026 Ruse University Session

**Topic:** Adaptive Strategy Learning in Multi-Agent Imperfect-Information Games
**Target length:** 12–14 minutes
**Speaking pace assumption:** ~140 words per minute
**Slide count:** 13 (12 content + title)

Design philosophy: minimal text on each slide so the audience looks at the
speaker, not the screen. Slide content is 1–4 short phrases; the spoken
version carries the substance and gives room to pause and emphasise.

## Visual Style Guide

- **Format:** 16:9 PowerPoint deck generated from a project-local script,
  saved under `deliverables/reports/ruseMay/presentation/`.
- **Branding:** use the official Ruse University logo from
  `presentation/assets/ru-logo-125x140.png` on the title slide and in a
  subtle footer on all content slides.
- **Footer:** thin divider line, small university logo on the left,
  `Ruse University Academic Session · May 2026` near the logo, and slide
  number on the right. No footer on the title slide.
- **Tone:** clean scientific deck, light background, dark charcoal text,
  restrained accents. Avoid stock-photo-heavy or marketing-style visuals.
- **Visual system:** use simple PowerPoint shapes, line icons, timelines,
  diagrams, and small symbolic elements. Prefer consistent vector-like
  visuals over mixed web images.
- **Accent colors:** blue for adaptation/inference, red-orange for risk or
  exploitation, teal/green for evaluation/safety. Use accents sparingly.
- **Typography:** one clean sans-serif family; large slide titles, short
  bullets, no dense paragraphs on slides.
- **Media policy:** use existing assets only when they are official or
  clearly appropriate. Prefer custom diagrams over generated images. Use
  generated images only if a specific visual cannot be created cleanly with
  shapes/icons.
- **Small playful elements:** acceptable when subtle and relevant: tiny
  card glyphs, a bot icon, a rock-paper-scissors mark, or a KL label on a
  safety dial.

## Build Plan

- Create `deliverables/reports/ruseMay/presentation/build_presentation.py`.
- Use `python-pptx` to generate an editable `.pptx` file directly.
- Keep slide content in a structured list inside the script or in a small
  adjacent data file.
- Implement reusable layouts: title slide, two-column text+diagram slide,
  timeline slide, contribution slide, and closing slide.
- Generate diagrams using PowerPoint shapes and text boxes rather than
  static screenshots where practical.
- Output:
  `deliverables/reports/ruseMay/presentation/adaptive_strategy_ruse_may.pptx`.
- Optional fallback: export each slide as a full-slide PNG later and import
  into PowerPoint manually if needed.

---

## Slide 1 — Title (≈ 30s)

**On screen:**
- Adaptive Strategy Learning in Multi-Agent Imperfect-Information Games
- *From Equilibrium Computation to Safe Opponent Exploitation*
- Alexander Andreev · PhD session report · May 2026 · Ruse University

**Visual notes:**
- Use the Ruse University logo prominently but not oversized.
- Clean title layout, likely left-aligned with a subtle multi-agent network
  diagram or faint node-link pattern on the right.
- No footer on this slide.

**Say:**
Good day. I'm Alexander Andreev. Over the next ten to twelve minutes I'll
walk you through the state of AI research in multi-agent strategic decision-
making, the specific gap my doctoral work addresses, and what I aim to
contribute by the end of this programme.

---

## Slide 2 — Why this matters now (≈ 1 min 30s)

**On screen:**
- Strong single agents → well understood in constrained benchmarks
- Agents interacting with *other agents* → open problem
- Hidden information · adversarial intent · real-time decisions

**Visual notes:**
- Show a simple transition diagram: one isolated agent on the left,
  multiple interacting agents on the right.
- Use blue for the isolated agent and red-orange accents for uncertainty or
  adversarial interaction.

**Say:**
In 2026, AI agents are everywhere. They trade billions of dollars on stock
exchanges. They navigate intersections next to human drivers. They compete
for attention on social platforms. And increasingly, they interact with
*other* AI agents they've never seen before.

Here's what's changed. Training strong single agents in constrained
benchmarks is now well understood. The open question is what happens when
your agent meets another agent whose behaviour is hidden, and possibly
adversarial.

*[Pause.]*

How does your AI know if the other player is cooperating, competing, or
trying to deceive it? And what should it do when its guess is wrong?

That's the research challenge I'm addressing.

---

## Slide 3 — Where this shows up (use cases) (≈ 2 min)

**On screen:**
- Financial markets — hidden positions, microsecond reactions
- Cybersecurity — adaptive attackers, hidden intent
- Social platforms — bot networks, coordinated disinformation
- Security — patrol randomisation *(deployed today)*
- Gaming platforms — collusion, fraud detection

**Visual notes:**
- Use five small icon tiles, one per domain: market chart, attacker/network,
  social graph/bot, shield/patrol, cards/collusion.
- Keep icons monochrome with a single accent color; avoid photos.
- This slide can be slightly more visual than the rest because it is the
  hook.

**Say:**
Let me make this concrete.

*Financial markets.* High-frequency trading firms run algorithms that
compete on exchanges with hidden positions, private signals, and
microsecond-level reactions. No one knows anyone else's strategy. Each
algorithm makes sequential decisions under uncertainty against opponents
whose intent is hidden.

*Cybersecurity.* Defensive systems face attackers who adapt once they see
how the defense behaves. The defender has to infer intent from partial
signals, while the attacker tries to remain hidden.

*Social platforms.* During recent election cycles we saw coordinated bot
networks interacting with real users whose intent — cooperative,
competitive, deceptive — was not declared. Detecting and classifying that
is a strategic-inference problem.

*Security.* Game-theoretic solvers are already in operational use —
randomising patrol and screening schedules in civil aviation and maritime
security. This isn't hypothetical. Real systems. Today.

*Gaming platforms.* Online poker and casino operators deal with collusion:
players working together against the rest of the table. Detecting it is
the same kind of strategic-inference problem — inferring hidden intent
from observed actions.

*[Pause. Slow down.]*

What's common to every one of these examples? Hidden information.
Multiple self-interested decision-makers. Sequential choices.
And the need to decide quickly.

Mathematically, they share the same abstraction: imperfect-information
extensive-form games.

---

## Slide 4 — Why study games? (≈ 1 min)

**On screen:**
- Poker and Belot-like games — hidden cards and inference
- Auction-style games — hidden valuations and bidding
- Pursuit-evasion grid worlds — partial observability
- Coalition games — alliances, betrayal, multi-player incentives

**Visual notes:**
- Use four equal mini-panels: cards, auction bid/gavel, grid with pursuer
  and evader dots, coalition graph.
- Small playful element: card corner symbols for the poker/Belot tile.
- Keep the point clear: these are controlled validation environments, not
  the final application domains.

**Say:**
You might reasonably ask: why study these problems through games?

Because games give us controlled environments where strategic behaviour
can be tested rigorously. Poker variants such as Kuhn Poker and Leduc
Hold'em are the first testbeds because they combine hidden information,
sequential actions, stochastic outcomes, and self-interested players while
still being small enough to verify analytically.

But the thesis is not only about poker. Belot-like trick-taking games
make the hidden-card intuition familiar. Auction-style games test bidding
with hidden valuations. Pursuit-evasion grid worlds test partial
observability, movement, and adversarial search. Games such as So Long
Sucker or simplified Diplomacy variants test multi-player incentives and
coalition behaviour.

The point is not the domain surface. The point is that these environments
let us check whether adaptation, safety, and evaluation methods transfer
across different strategic structures.

---

## Slide 5 — State of the art (≈ 1 min 30s)

**On screen:**
- CFR (2007) · Libratus (2017) · Pluribus (2019) · ReBeL (2020)
- Diplomacy and Stratego at large scale
- *"Superhuman" in progressively larger games*

**Visual notes:**
- Use a horizontal timeline: 2007 CFR, 2017 Libratus, 2019 Pluribus, 2020
  ReBeL, 2022 Diplomacy/Stratego.
- Avoid screenshots of games unless licensing is clear; timeline is enough.

**Say:**
The field has made remarkable progress over the past decade.

Counterfactual Regret Minimization — CFR — came out in 2007 and made it
practical to compute equilibrium strategies in imperfect-information
games.

Libratus beat top professional players in two-player poker in 2017.
Pluribus did the same in six-player poker in 2019. ReBeL, in 2020,
brought AlphaZero-style search into imperfect-information games.

More recently, DeepNash reached expert-level play in Stratego — a game
with a state space ten to the power of one hundred and seventy-five times
larger than Go.
Meta's CICERO reached human-level play in Diplomacy — a seven-player
game with coalitions and betrayal.

*[Pause for the "but".]*

These are genuine milestones. But they all share a critical limitation.

---

## Slide 6 — The limitation (≈ 1 min)

**On screen:**
- **Fixed strategies. No adaptation.**
- The same policy against every opponent.

**Visual notes:**
- Show one central policy box sending identical arrows to three opponent
  types: cautious, aggressive, coordinated.
- This slide should be stark and minimal; the limitation should visually
  feel obvious.

**Say:**
Every one of these systems computes a *fixed* equilibrium strategy.
They play *identically* against every opponent.

Imagine a strategic agent that behaves the same way against a cautious
beginner, an aggressive bluffer, and a coordinated group of opponents. It
throws away easy gains against the weak opponent, and exposes itself when
the environment changes.

Equilibrium strategies are safe, but they're blind. They systematically
fail to exploit weaknesses they could detect.

And in games with more than two players, even "safe" becomes a problem.
The mathematical guarantees that underpin two-player safety — the minimax
property of Nash equilibrium — *provably* fail when you add a third
player.

---

## Slide 7 — Three open problems (≈ 1 min)

**On screen:**
1. **Adaptation** — infer opponents in real time
2. **Safety** — exploit without exposing yourself
3. **Evaluation** — measure if an agent adapts well

**Visual notes:**
- Use a triangle or three-node loop: Adaptation, Safety, Evaluation.
- Each node should map visually to the next three contribution slides.
- Color-code nodes consistently with later slides.

**Say:**
This exposes three interrelated research problems.

*First — adaptation.* How can an agent infer an opponent's tendencies from
observed actions and update its own strategy in real time?

*Second — safety under adaptation.* Once you start exploiting, you open
yourself up. How do you bound your worst-case losses? And critically, can
you do it in games with more than two players, where the classical safety
theorem fails?

*Third — evaluation.* How do you reliably measure whether an agent adapts
well? If I claim my agent is adaptive, you should be able to check.

These three problems — *inference, action, measurement* — map directly
onto my three thesis contributions.

---

## Slide 8 — Contribution 1: Behavioral Adaptation (≈ 1 min 30s)

**On screen:**
- Infer opponent *type*, not just hidden state
- Adapt only when evidence is strong enough
- Detect anomalies: bots, collusion, adversarial users

**Visual notes:**
- Use a belief-state diagram: observed actions feed into two belief boxes,
  hidden state and behavioral type, then into decision-making.
- Add a small fallback arrow to "equilibrium play" when evidence is weak.
- Small playful element: tiny bot icon near anomaly detection.

**Say:**
The first contribution is the Behavioral Adaptation Framework.

Existing systems already track a belief about hidden state: what cards an
opponent might hold, what private valuation they might have, or where an
agent might be in a partially observed grid. I extend that idea to also
track behavioural type. Not just "what information might you have", but
"what kind of strategic actor are you?"

The agent updates this belief from observed actions and feeds it into its
decision-making. With one critical design rule: if we haven't observed
enough yet, fall back to equilibrium play. No acting on unreliable guesses.

This is also where the practical applications enter. An agent that can
classify opponent behaviour can also detect anomalous behaviour: a bot, a
colluding pair, or an adversarial actor disguised as a normal participant.
That maps directly to fraud detection, bot identification, and platform
integrity.

---

## Slide 9 — Contribution 2: Safe Exploitation (≈ 1 min 30s)

**On screen:**
- Exploit detected weaknesses
- Stay close to a reference policy
- Target: useful safety heuristics beyond two players

**Visual notes:**
- Use a slider/dial from "exploit" to "reference policy".
- Show the exploitative policy constrained by a band around the reference
  policy.
- Small technical easter egg: label the constraint `πKL` or `KL`.

**Say:**
The second contribution is Multi-Agent Safe Exploitation.

The 2015 Safety Theorem gives formal guarantees for two-player games.
Those guarantees *provably fail* at three players and above.

My approach adapts an idea from Meta's Diplomacy system: πKL regularisation.
The agent is *allowed* to exploit, but it cannot drift too far from a safe
reference policy. The method gives us a dial — more exploitative on one
end, closer to the reference policy on the other.

The reference policy doesn't need to be a perfect equilibrium. It can be
a population average, a human-behaviour prior learned from data, or an
approximate equilibrium. That makes the approach usable in N-player games
where exact equilibrium is intractable.

The aim is not to claim a general theorem immediately. The realistic goal
is to validate practical heuristics on small but structurally different
multi-player games, and to characterise where they fail.

---

## Slide 10 — Contribution 3: Evaluation (≈ 1 min 30s)

**On screen:**
- Safety — worst-case vulnerability
- Population ranking — non-transitive dynamics
- Statistical reliability — variance reduction

**Visual notes:**
- Use a three-layer evaluation stack: safety, population ranking,
  statistical reliability.
- Small playful element: rock-paper-scissors glyphs beside non-transitive
  dynamics.
- Mention method names in speech; keep on-screen text conceptual.

**Say:**
The third contribution is the Evaluation Methodology.

Right now, there's no standard way to measure adaptive agents across
different games.

Exploitability measures worst-case vulnerability but ignores adaptation.
Elo ranks players but misses cyclic dominance — the rock-paper-scissors
structures that appear in real populations.
Raw win rates have too much variance in hidden-information games.

My framework combines three: an N-player version of exploitability,
α-Rank for non-transitive structures, and AIVAT for variance reduction.
Validated across structurally different game types, so the evaluations
transfer.

---

## Slide 11 — What I study deeply first (≈ 1 min 30s)

**On screen:**
- Phase A — Foundation — Steps 1–2 — RL · CFR (Done)
- Phase B — Scaling the toolbox — Steps 3–4 — CFR variants · Game abstraction
- Phase C — Neural methods — Steps 5–6 — Deep CFR · Pluribus → ReBeL → SoG
- Phase D — Opponent modelling — Steps 7–8 — Behavioural inference · Safe exploitation
- Phase E — Multi-agent dynamics — Steps 9–11 — MARL · PBT · Coalitions
- Phase F — Data-driven approaches — Steps 12–13 — Sequence models · Behavioural pipelines
- Phase G — Integration — Steps 14–15 — Evaluation · Frontier mapping

**Visual notes:**
- Use a 4 + 3 card grid: top row holds Phases A–D, bottom row holds Phases
  E–G. Each card carries a phase letter badge, name, step range, and a
  one-line keyword list.
- Colour the badges to match contribution alignment: blue for the early
  toolbox (B–D), red for multi-agent dynamics (E), teal for data-driven
  work (F), amber for integration (G). Phase A reads as completed.
- Keep type small but legible. The point is the shape of the path, not the
  individual words.

**Say:**
Before attacking the contributions, I commit to studying seven phases
deeply. The first two are already done — reinforcement learning and the
CFR foundation, including a Vanilla CFR implementation on Kuhn poker.

Phase B scales that toolbox: CFR variants, game abstraction, the
machinery for imperfect-information games at non-trivial size.

Phase C moves to neural methods — Deep CFR, DREAM, and the end-to-end
architectures that culminate in Pluribus, ReBeL, and Student of Games.
That is where modern game AI actually lives.

Phases D and E are the heart of the preparation. Phase D goes deep into
opponent modelling and safe exploitation theory — directly underneath
the first two contributions. Phase E covers multi-agent dynamics:
multi-agent RL, population-based training, and coalition formation.
That is where the safety problem becomes genuinely multi-player.

Phase F brings in data-driven methods and sequence models — including
LLM agents in strategic settings. Phase G is integration: evaluation
frameworks and a research-frontier mapping that feeds directly into the
contribution design.

The order is not arbitrary. Each phase unlocks the next, and the three
contributions sit on top of all seven. The thesis is the visible part;
this slide is the iceberg under it.

---

## Slide 12 — Expected outcomes (≈ 1 min)

**On screen:**
- **Realistic target:** validated adaptation · characterised safety heuristics · working evaluation framework
- **Stretch direction:** theoretical extensions · novel combinations

**Visual notes:**
- Use a two-column layout: realistic target on the left, stretch direction
  on the right.
- Keep the left column visually grounded and the right column lighter or
  more aspirational.
- Avoid making the stretch side look like a promise.

**Say:**
A word on scope.

The realistic target for each contribution is: a validated method on
structurally diverse games, characterised failure modes, and a framework
that produces actionable insights on real data.

Stretch outcomes exist — extending the Safety Theorem beyond two players,
or surprising empirical results in evaluation. But I'm deliberately not
over-promising.

The grounded outcomes, taken together, already constitute a coherent
thesis. Any further depth that emerges from the later study steps builds
on that foundation. No pivot required.

---

## Slide 13 — Close (≈ 30s)

**On screen:**
- The gap between *today's deployed systems* and *the next generation.*

**Visual notes:**
- Use a clean transformation graphic: fixed strategy systems on the left,
  adaptive safety-aware agents on the right.
- Include the Ruse University logo in the footer as usual.
- End visually quiet, not dramatic.

**Say:**
To close.

The gap I'm addressing is not merely academic. It's the gap that separates
today's deployed systems — fixed-strategy solvers in security, auctions,
and gaming platforms — from the next generation of AI. Agents that will
need to adapt, safely, to opponents they've never seen, while remaining
accountable to systematic evaluation.

That's what the thesis aims to contribute.

Thank you. I'd be happy to take questions.

---

## Timing summary

| Slide | Topic | Time |
|-------|------------------------|--------|
| 1 | Title | 0:30 |
| 2 | Why this matters now | 1:30 |
| 3 | Use cases | 2:00 |
| 4 | Why study games? | 1:00 |
| 5 | State of the art | 1:30 |
| 6 | The limitation | 1:00 |
| 7 | Three open problems | 1:00 |
| 8 | Contribution 1: Behavioral Adaptation | 1:30 |
| 9 | Contribution 2: Safe Exploitation | 1:30 |
| 10 | Contribution 3: Evaluation | 1:30 |
| 11 | What I study deeply first | 1:30 |
| 12 | Expected outcomes | 1:00 |
| 13 | Close | 0:30 |
| **Total** | | **~15:00** |

This is ~15:00 of planned timing, but the scripted text is closer to
12--13 minutes at normal speaking pace. The remaining time is for pauses,
transitions, and short clarifications if the committee needs them.

If you need to tighten: shorten Slide 3 use cases and Slide 4 testbeds,
or compress Slide 11 by reading only Phases B–E aloud. Together those
edits save two to three minutes without weakening the thesis
contribution.

## Notes for delivery

- **Slide 3 is the hook.** Slow down. Let the audience feel the range of
  domains. Don't rush through the list — each example should land.
- **Slides 6, 8, 9, and 10 carry the argument.** Pauses matter more than
  words.
- **Slide 8** contains the practical value angle. Emphasise anomaly and
  collusion detection there.
- **Don't read the slides.** The bullet points are memory anchors, not a
  script. You speak the substance; the slide just marks where you are.
- **Prepare three numbers to quote from memory:** $10^{175}$ (Stratego's
  state space), the year 2007 (CFR), and the number 7 (Diplomacy's
  players). Audiences remember concrete numbers.
