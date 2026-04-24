# Presentation Script — May 2026 Ruse University Session

**Topic:** Adaptive Strategy Learning in Multi-Agent Imperfect-Information Games
**Target length:** 10–12 minutes
**Speaking pace assumption:** ~140 words per minute
**Slide count:** 11 (10 content + title)

Design philosophy: minimal text on each slide so the audience looks at the
speaker, not the screen. Slide content is 1–4 short phrases; the spoken
version carries the substance and gives room to pause and emphasise.

---

## Slide 1 — Title (≈ 30s)

**On screen:**
- Adaptive Strategy Learning in Multi-Agent Imperfect-Information Games
- *From Equilibrium Computation to Safe Opponent Exploitation*
- Alexander Andreev · PhD session report · May 2026 · Ruse University

**Say:**
Good day. I'm Alexander Andreev. Over the next ten to twelve minutes I'll
walk you through the state of AI research in multi-agent strategic decision-
making, the specific gap my doctoral work addresses, and what I aim to
contribute by the end of this programme.

---

## Slide 2 — Why this matters now (≈ 1 min 30s)

**On screen:**
- Training a single smart agent → mostly solved
- Agents interacting with *other agents* → open problem
- Hidden information · adversarial intent · real-time decisions

**Say:**
In 2026, AI agents are everywhere. They trade billions of dollars on stock
exchanges. They navigate intersections next to human drivers. They compete
for attention on social platforms. And increasingly, they interact with
*other* AI agents they've never seen before.

Here's what's changed. Training a single smart agent in isolation is mostly
a solved problem. The open question now is what happens when your agent
meets another agent whose behaviour is hidden, and possibly adversarial.

*[Pause.]*

How does your AI know if the other player is cooperating, competing, or
trying to deceive it? And what should it do when its guess is wrong?

That's the research challenge I'm addressing.

---

## Slide 3 — Where this shows up (use cases) (≈ 2 min)

**On screen:**
- Financial markets — hidden positions, microsecond reactions
- Autonomous vehicles — unsignaled intersections
- Social platforms — bot networks, coordinated disinformation
- Security — patrol randomisation *(deployed today)*
- Gaming platforms — collusion, fraud detection

**Say:**
Let me make this concrete.

*Financial markets.* High-frequency trading firms run algorithms that
compete on exchanges with hidden positions, private signals, and
microsecond-level reactions. No one knows anyone else's strategy. Each
algorithm makes sequential decisions under uncertainty against opponents
whose intent is hidden.

*Autonomous vehicles.* Two self-driving cars arriving at an unsignaled
intersection — that's a game-theoretic problem. Each has to predict what
the other will do, without access to the other's internal model.

*Social platforms.* During recent election cycles we saw coordinated bot
networks interacting with real users whose intent — cooperative,
competitive, deceptive — was not declared. Detecting and classifying that
is a strategic-inference problem.

*Security.* Game-theoretic solvers are already in operational use —
randomising patrol and screening schedules in civil aviation and maritime
security. This isn't hypothetical. Real systems. Today.

*Gaming platforms.* Online poker and casino operators deal with collusion:
players working together against the rest of the table. Detecting it is
the same mathematical problem — inferring hidden intent from observed
actions.

*[Pause. Slow down.]*

What's common to every one of these examples? Hidden information.
Multiple self-interested decision-makers. Sequential choices.
And the need to decide quickly.

Mathematically, they are all the same object: imperfect-information
extensive-form games.

---

## Slide 4 — Why poker? (≈ 1 min)

**On screen:**
- Smallest clean testbed with all four real-world features:
  - Hidden info · sequential actions · stochastic outcomes · multiple players
- Algorithms are *domain-agnostic*

**Say:**
You might reasonably ask: why has the research community focused on poker?

Because poker is the smallest game family that has all four structural
features of the real-world problems I just listed. Hidden private
information — your hole cards. Sequential actions — bet, call, fold.
Stochastic outcomes — the next card is random. Multiple self-interested
players.

And unlike, say, autonomous driving, poker has an unambiguous winner.
So you can actually tell whether your algorithm is working.

But the algorithms themselves don't care about cards. They apply to any
imperfect-information game.

---

## Slide 5 — State of the art (≈ 1 min 30s)

**On screen:**
- CFR (2007) · Libratus (2017) · Pluribus (2019) · ReBeL (2020)
- DeepNash on Stratego · CICERO on Diplomacy
- *"Superhuman" in progressively larger games*

**Say:**
The field has made remarkable progress over the past decade.

Counterfactual Regret Minimization — CFR — came out in 2007 and made it
practical to compute equilibrium strategies in imperfect-information
games.

Libratus beat top professional players in two-player poker in 2017.
Pluribus did the same in six-player poker in 2019. ReBeL, in 2020,
brought AlphaZero-style search into imperfect-information games.

More recently, DeepNash solved Stratego — a game with a state space ten
to the power of one hundred and seventy-five times larger than Go.
Meta's CICERO reached human-level play in Diplomacy — a seven-player
game with coalitions and betrayal.

*[Pause for the "but".]*

These are genuine milestones. But they all share a critical limitation.

---

## Slide 6 — The limitation (≈ 1 min)

**On screen:**
- **Fixed strategies. No adaptation.**
- The same moves against a novice and a world champion.

**Say:**
Every one of these systems computes a *fixed* equilibrium strategy.
They play *identically* against every opponent.

Imagine a chess program that plays the same opening against a club player
and against Magnus Carlsen. Against the club player it throws away easy
wins. Against Carlsen, it just hopes the math holds up.

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

## Slide 8 — The three contributions (≈ 3 min)

**On screen:**
1. **Behavioral Adaptation Framework** — infer opponent *type*, not just cards
2. **Multi-Agent Safe Exploitation** — πKL regularisation beyond two players
3. **Evaluation Methodology** — domain-agnostic, variance-aware

**Say:**
Let me walk through each.

*Contribution 1 — the Behavioral Adaptation Framework.*

The idea: existing systems already track a belief about what private
information the opponent holds. I extend that to also track who the
opponent *is* as a player. Not just "what cards might you have", but
"what type of player are you — aggressive, conservative, bluff-heavy?".

The agent updates this belief from observed actions and feeds it into
decision-making. With a critical design rule: if we haven't observed
enough yet, fall back to equilibrium play. No acting on unreliable
guesses.

*[Small pause.]*

*Contribution 2 — Multi-Agent Safe Exploitation.*

The 2015 Safety Theorem gives us formal guarantees for two-player games.
Those guarantees *provably fail* at three players and above.

My approach adapts an idea from Meta's Diplomacy system: πKL regularisation.
The agent is *allowed* to exploit, but it cannot drift too far from a safe
reference policy. The math gives us a dial — fully exploitative on one end,
fully safe on the other.

The reference policy doesn't need to be a perfect equilibrium. It can be
a population average, a human-behaviour prior learned from data, or an
approximate equilibrium. That makes the approach usable in N-player games
where exact equilibrium is intractable.

*[Small pause.]*

*Contribution 3 — the Evaluation Methodology.*

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

## Slide 9 — Real-world applications (≈ 1 min)

**On screen:**
- Fraud detection
- Bot identification
- Collusion detection
- Platform integrity

**Say:**
One point I want to emphasise about Contribution 1.

An agent that can infer "what *type* of player is my opponent" is also an
agent that can *detect* anomalous behaviour. An unauthorised bot. A
colluding pair of players. An adversarial actor disguised as a normal user.

That has immediate applications in fraud detection, bot identification,
and platform integrity — especially in online gaming and financial
platforms.

So the thesis isn't purely theoretical. The techniques I'm developing map
directly onto products that companies already deploy. I mention this
because my career trajectory includes potential collaboration with gaming
platforms that have exactly this problem — detecting collusion in
multiplayer card games.

---

## Slide 10 — Expected outcomes (≈ 1 min)

**On screen:**
- **Grounded floor:** validated adaptation · characterised safety heuristics · working evaluation framework
- **Open direction:** theoretical extensions · novel combinations

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

## Slide 11 — Close (≈ 30s)

**On screen:**
- The gap between *today's deployed systems* and *the next generation.*

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
| 4 | Why poker? | 1:00 |
| 5 | State of the art | 1:30 |
| 6 | The limitation | 1:00 |
| 7 | Three open problems | 1:00 |
| 8 | Three contributions | 3:00 |
| 9 | Real-world applications | 1:00 |
| 10 | Expected outcomes | 1:00 |
| 11 | Close | 0:30 |
| **Total** | | **~14:00** |

This is ~14 minutes of pure talking — perfect, because you'll naturally go
faster in places and slower for emphasis in others. The actual delivered
time usually lands 10–20% under the scripted time. Expect 11–12 minutes
live.

If you need to tighten: cut Slide 4 ("why poker?") — it's the most
skippable. That saves a full minute.

## Notes for delivery

- **Slide 3 is the hook.** Slow down. Let the audience feel the range of
  domains. Don't rush through the list — each example should land.
- **Slides 6 and 8 carry the argument.** Pauses matter more than words.
- **Slide 9** is your career-narrative slide. Emphasise the industry
  angle; this is where the committee sees practical value.
- **Don't read the slides.** The bullet points are memory anchors, not a
  script. You speak the substance; the slide just marks where you are.
- **Prepare three numbers to quote from memory:** $10^{175}$ (Stratego's
  state space), the year 2007 (CFR), and the number 7 (Diplomacy's
  players). Audiences remember concrete numbers.
