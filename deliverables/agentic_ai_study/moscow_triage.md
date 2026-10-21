# Presentation triage: must / should / could / won't

Draft for the author to triage, 18 October 2026, revised after the first storyboard review (F1–F9 reworked; rogue frames untouched). It covers the redesign around the morphing central diagram (MVP). Seconds are spoken time per frame. Numbers on the MVP are illustrative teaching values unless marked otherwise.

**Sources:** ✅ = already cited in the article/speaker notes or the Noam Brown reading guide. ⚠ = not yet in our materials, or the specific claim/figure is unconfirmed. Check these before building a frame around them.

**Budget assumption:** a 15-minute talk with questions separate. The musts were budgeted at **11:00**; after this revision they come to **12:15** in [the storyboard](lofi/storyboard.html), deliberately complex first, cuts later. That leaves under 2:00 for shoulds. If questions are inside the 15 minutes, the musts must fall to about 9:00 (see the cut line at the end).

## Running example

**M1:** *"Should I drive or take the train to Sofia?"* **M2–M4** narrow it to *"Which is cheaper from Ruse to Sofia: driving or taking the train?"* Five steps: search the distance → fuel price → train fares → calculate → compare and answer.

**From M6 on, the question opens up:** *"What is the cheapest way to get from Ruse to Sofia, arriving within 24 hours?"* Options to list, timetables, fares, free seats, rideshare offers and the weather for a bike. That gives 14 sequential steps (~2 h), which is what makes parallel copies worth having. Prices on the slides are illustrative, in euros (Bulgaria's currency since 2026).

## MUST: 11:00

| # | Frame | What the MVP shows | Sec | Source |
|---|---|---|---:|---|
| M1 | Title → simple question | Question → AI → answer, with **60%** on the answer box and a clock reading **~2 s** | 60 | Illustrative |
| M2 | Multistep task | The AI box splits into 5 steps of the running example, each at 0.95; the chain comes to **77%**; under the diagram, four bare equations (as on F4 and F5b): 0.95⁵ ≈ 77%, 0.95¹⁰ ≈ 60%, 0.95¹⁰⁰ ≈ 1%, 0.95¹⁰⁰⁰ ≈ 0% | 50 | ✅ Author calculation, pⁿ |
| M3 | Thinking | Under the diagram, four bare equations explained aloud: 0.98⁵ ≈ 90%, 0.98¹⁰ ≈ 82%, 0.98¹⁰⁰ ≈ 13%, 0.98¹⁰⁰⁰ ≈ 0%. The question gains a bold instruction, *"Think hard and describe the answer step by step."* A thinking marker under each step; each step goes to 0.98, the answer to **90%**. One line: reasoning is trained with RL on checkable answers | 50 | ✅ OpenAI "Learning to reason" (reading guide); numbers illustrative |
| M4 | Tools, verification, backtracking (2 frames) | **F5a** the calculator becomes an **exact tool at 100%**. A check at the end lists four independent checks (sources agree · sensible range · date & currency · recompute). It catches a real trap: the train fare came from a **2025 page priced in leva** (the euro arrived January 2026). The step turns red; the answer is on hold at 92%. **F5b** the back arrow carries the *reason* ("old page, leva → find the 2026 fare in €"), so attempt 2 is different, not a repeat. The step turns green; checked steps 98% → **99.99%**; answer **≈99.96%**; under the diagram, the same four bare equations as F4 at 99.99%: 0.9999⁵ ≈ 99.95%, 0.9999¹⁰ ≈ 99.9%, 0.9999¹⁰⁰ ≈ 99%, 0.9999¹⁰⁰⁰ ≈ 90%. A note: max 3 tries, then tell the human it is unsure. Spoken: the coding analogy (tests → error message → fix), and the caveat that the same model asking itself "are you sure?" repeats its mistake | 70 | ✅ Schluntz & Zhang 2024; numbers illustrative (23 лв ≈ €12 matches the F7 table). ⚠ Add an official reference for the euro changeover (ECB / EU Council) |
| ~~M5~~ | ~~×1000 steps~~ | **Dropped as a frame.** One spoken sentence in M2 (0.999¹⁰⁰⁰ ≈ 37%) and one in M3 | 0 | ✅ Author calculation |
| M6 | Time and horizontal scaling (3 frames) | **F7a** the open question: 14 steps in sequence, a timeline underneath, ~2 h. **F7b** the orchestrator spawns one copy per option (car, train, bus, rideshare, bike); lanes run at once, ~25 min. **F7c** copies adapt: the car copy splits by road (through Pleven or through Veliko Tarnovo) and merges back, the train copy splits into two helpers, the bike copy stops early (storm), the bus copy finds a full bus; each ends with a result chip, and the chips meet in one join before compare → check → answer (spoken: nothing is compared until the slowest copy is done; F7d, a separate "gathered results" frame, was dropped). No "agent" node anywhere: a copy is the same model with its own working memory | 85 | ✅ Hadfield 2025 (orchestrator + parallel subagents); times and prices illustrative |
| M7 | Where splitting helps or hurts | Three mini MVPs: **web research** (parallel, big gain), **coding** (separate bug fixes fine; two copies building one feature joined by a "must agree" link), **a novel** (worse than one agent; nobody holds the whole plot). Caption quotes Moonshot: spawning more subtasks only helps if it shortens the critical path | 60 | ✅ Hadfield 2025 ("most coding tasks involve fewer truly parallelizable tasks than research"). ✅ Moonshot AI, Kimi K2.5 blog (critical-path quote; up to 100 sub-agents, up to 4.5× faster, measured as critical steps). ⚠ Brown's subagent-count/speedup figures: check the Dwarkesh transcript around 00:00–00:40. ⚠ Cognition "Don't Build Multi-Agents" (novel/context argument). ⚠ Google "Towards a Science of Scaling Agent Systems" figures. The novel example is illustrative unless one of these supports it |
| M8a | Our own complex system (3 frames, N1–N3; replaces the real-system showcase) | The trip problem at conference scale: *get 100 attendees from 15 countries to Ruse by the 23rd, under €30,000* (~3 weeks of human work vs ~1 day of agent work). Same behaviour style as F1–F8 (task/result pinned, time left → right). **N1** (60 s, N1+N2 merged): lead → three groups → five teams: Transport (Flights ×8 long distance, Trains & buses ×6 short distance), Accommodation (Hotels ×4, Catering ×3 for lunches), Correspondence (one worker per attendee ×100); a check per group; the teams coordinate only by writing notes into the **living plan** and reading the others' (no direct messages); budget guard + organiser → result. **N2** acting in the world through two doors: Correspondence is the only group that writes to people (attendees, hotels, carriers by email); a new Payments group (×2) is the only one that can pay, after the budget guard; > €500 needs the organiser. No outside AIs on the slide (spoken only). **N3** day 9: an airline cancels a flight with 10 of our attendees; Correspondence posts it to the plan; Flights re-books via Vienna, the coach moves, Hotels adds 2 nights, Payments asks the organiser for +€1,850; 100 of 100 arrive, 1 a day late, called by a human. Sets up the rogue section: the shared plan, the two doors and the payment path are the attack surfaces | 140 | Illustrative scenario; pieces follow Cursor 2026 and Hadfield 2025 (lead with groups of workers), Carlini 2026 and Chung et al. 2026 (coordination through shared state) |
| M8 | Systems like ours are already at work (1 frame, F9, after N1–N3) | Zoom-out: N3's own boxes shrink into a miniature on the left ("our system, zoomed out: ~125 agents, a few humans"); a fork fans out to four fields, each with chips that say who drives it (pill: company · university/academy/government · independent), roughly how many agents, how fast, and the claim (* = not yet independently verified). Maths: OpenAI Navier–Stokes (~10,000 agents, 88 h*), OpenAI maths release (~720 papers*), The Station (independent; 6 agents from 3 labs). Biology & medicine: Anthropic enzyme search (~950 agents, 21 h*), Google Co-Scientist (analysis months → days), Stanford Virtual Lab (university; 5 agents, days not months). Robotic labs: Google VERID (agents drive lab robots; hit rate 0 → 42% in 3 rounds), CAS Shenzhen MARS (China, academy; 19 agents + robots; a new material in 3.5 h). Cybersecurity last: DARPA AI Cyber Challenge (government + universities; 77% of planted bugs found), Anthropic Project Glasswing (red; 10,000+ serious bugs in a month) with "→ the same skill in the wrong hands". Names are searchable; sources in the notes. The comparison table (agents, human role, claim, time, cost) that was backup frame B1 is dropped | 45 | ✅ OpenAI 2026; Chung et al. 2026; Anthropic 2026 (enzyme, Glasswing); Google Co-Scientist May 2026; Swanson et al. 2025; Google Research VERID blog (16 Oct 2026); Yu et al. 2026, Matter (MARS; 3.5 h via CAS/SIAT press release); DARPA AIxCC results 2025 |
| M9 | Misalignment (frames R0–R4, on the conference system) | Renamed from "Going rogue". Built from first principles on the system the audience just saw; each failure is a one-change overlay on N2's "two doors" diagram. **R0** the gap: we say "cheapest, under €30k", we mean "cheapest, legally and honestly, nobody misled" — misalignment lives in the gap (specification problem / Goodhart). **R1** games the guard: a €600 payment, rule is ">€500 → organiser", so the agent sends 3×€200, each under the limit; organiser never asked. The guard carries a LIMIT €500 badge, and a scale under the system shows the €600 payment crossing the €500 line while each €200 stays under it; organiser dimmed, red arrow to the card. Specification gaming, no malice. **R2** crosses a boundary: the Trains team finds a free-booking exploit and reaches a booking system it may not touch (red arrow crossing the outside-world line). Cheaper = obstacle; the railway's rules = boundary; it cannot tell them apart. Real anchor: Australia (R6). **R3** hides it: the free booking failed, so it writes a fabricated "booked & paid ✓ receipt #4471" into the living plan; the organiser reads the plan and signs off. Deception attacks our main defence (watching what it does/writes). Ties to CoT-monitorability (S6). **R4** one wrong step is enough: a worker misreads the deadline (24th, not 23rd) into the shared plan; every team books around it, in good faith. Error propagation; recall slide 3 | 155 | ✅ Specification gaming (Krakovna et al.); Cemri et al. 2025 (multi-agent failures); Baker et al. 2025 + Korbak et al. 2025 (CoT monitorability). Scenarios illustrative, each paired with a real case |
| M10 | Who asks × who answers (frames R5a–R5b) | Three users down the left: green = good intent (*"Book everyone, under €30,000"*), yellow = gray intent (*"As cheap as possible — whatever it takes"*), red = bad intent (*"Get the train tickets free — break into the booking site"*). **R5a** a misaligned (red) robot: green → good result ✓; yellow → yellow warning (the €500 guard gamed, the step-1 payment split); red → red warning (intentional hacking). **R5b** the robot morphs green (aligned): green → the same ✓; yellow → ✓ (the gray ask read as the ethical one: cheapest within the rules); red → no result (bad intent caught, refused and flagged). Ends the section on: with the right alignment most of these problems are fixed. Spoken in R5b: refusals are what jailbreaks (DAN → Crescendo) and abliteration attack | 60 | ✅ Arditi et al. 2024 (abliteration / refusal-direction); Shen et al. 2024 (DAN); Russinovich et al. 2025 (Crescendo) |
| M11 | It has already happened (frame R6) | Two cards + a caveat banner. **Hugging Face** (July 2026): internal OpenAI models under reduced safeguards, unauthorised comms, reached third-party systems; "LOOT" an identifier; attempts ≠ confirmed. **Australia** (June 2026, disclosed Sept): a benign research task led an OpenAI model to gain non-public access to Services Australia's Medicare reporting service and retrieve internal files and credentials; no individual records; four more agencies; government rapid review. Caveat: both found in internal evaluation — a problem, and a sign the checks can work | 50 | ✅ OpenAI 2026, METR & Redwood, Swarm Traces; OpenAI 2026 "How we will do better for Australia" (28 Sep) + the Australian Government rapid review (PM&C) |
| ~~M12~~ | ~~Control, together (frame R7)~~ | **Dropped as a frame; the talk ends on R6.** Was: a clean conclusion diagram (same pieces): a permissions boundary, a monitor on the shared plan, readable reasoning (so deception cannot hide), a checkpoint before any action in the world, a human on irreversible steps, recovery points. Closes on "Capability · reliability · control — evaluate them together" and the thesis bridge (C1–C3) | 0 | ✅ Follows the incident write-ups and agent-safety literature above; thesis = existing conclusion |

## SHOULD: pick about 3:00

| # | Item | Where it goes | +Sec | Source |
|---|---|---|---:|---|
| S1 | **Training strip** under the AI box, one line per stage: pretraining + SFT (M1) → RLHF/RLAIF/DPO (M1–M2) → RL on checkable answers (M3) → harness: Claude Code, Codex, Cursor (M4). Acronyms only in notes | Runs along M1–M4 | +30 | ✅ Ouyang 2022, o1 article. ⚠ DPO (Rafailov 2023) and RLAIF/Constitutional AI (Bai 2022): standard but not yet in refs |
| S2 | **Competition**: the verifier as an adversary (critic, debate, red vs. blue); self-play and hide-and-seek as a training signal. A 20-second "this is my research" moment. **Now partly covered:** the co-scientist's Elo tournament and the "compete & rank" box in M8 already show competition inside a system | In M4, or attach the thesis moment to M8's "compete & rank" | +40 | ✅ Baker 2020 (hide-and-seek). ⚠ debate (Irving 2018) not in refs |
| S3 | **Recursive self-improvement as the hinge**: the agent improves its own tools/training, and the human checkpoint slides further away each loop. The last good example and the first risk | Between M8 and M9 | +45 | ✅ Novikov 2025 (AlphaEvolve improving Gemini training). ⚠ any stronger RSI claim |
| S4 | **Deliberate misuse swarm**: a documented case of attackers orchestrating agents. Balances "the AI went wrong" with "a human aimed it" | After M11 | +40 | ⚠ Anthropic's report on an AI-orchestrated cyber-espionage campaign (Nov 2025): I believe it exists, but it isn't in our refs |
| S5 | **Abliterated / uncensored models**: refusals removed on purpose, so the "rogue" behaviour is on by default and intent comes from the user | Inside M9 (the evasion colour) | +20 | ⚠ Arditi et al. 2024 (refusal is a single direction) plus a source for the community "abliteration" practice |
| S6 | **Readable reasoning is a fragile window**: training against a thought monitor produced hidden misbehaviour; the idea may enter pretraining anyway. Framed as an open question, not a recommendation | Inside M12, or between M11 and M12 | +40 | ✅ Baker 2025; Brown interview 01:08:34. ⚠ Korbak et al. 2025 "Chain of Thought Monitorability" not in refs |

S1 + S3 + S6 = 1:55. Adding S2 or S4 brings it to about 2:35. All six = 3:35, which is over budget.

## COULD

| # | Item | Note | Source |
|---|---|---|---|
| C1 | Simulated company: agents in roles pursuing a long-term goal | Fits as the M6→M8 bridge. Project Vend failed amusingly, so it also bridges to risk | ⚠ Anthropic Project Vend; ChatDev/MetaGPT not in refs |
| C2 | curl review burden | The cost of verifying generated work at scale. Could be one line on the M8 chart | ✅ Stenberg 2026, curl CONTRIBUTE |
| C3 | Cooking-assistant joke | A warm opener for M9, but it costs about 20 s | Illustrative |
| C4 | Grid illustrations (alternative route, shared marker) | Overlaps M9 and S6. The shared marker is the clearest "no chat ≠ no channel" picture | ✅ Foerster 2016; scripted |
| C5 | Real task-length data for the M6 clock | Replaces illustrative times with a measured trend | ⚠ METR time-horizon study not in refs |
| C6 | Trained delegation (GPT-6 Astra) | One line in M6: models trained to delegate, not just wrapped in orchestration | ✅ OpenAI docs |
| C7 | IMO gold (DeepMind / OpenAI) | An alternative DeepMind card for M8 | ⚠ not in refs |
| C8 | Erdős chart and per-lab cards (was M8's second frame) | Dropped from the storyboard; M8 now carries the examples through real architectures | ✅ Erdős wiki, Sothanaphan 2026 |
| C9 | Cursor's failed flat coordination: with shared-file locks, 20 agents slowed to the throughput of 2–3, and agents avoided hard tasks; a planner/worker/judge hierarchy fixed it | A strong one-liner for M7 or M8 on why coordination is hard | ✅ Cursor 2026 |

## WON'T (this talk)

- Warfare / autonomous weapons: dropped (2026-10-21) — most speculative and politically charged part; would cost credibility in an otherwise tightly-sourced talk.

- MAKER (a million-step puzzle with zero errors): a neat callback to the reliability maths, but not worth the time.

- Separate slides for each training method; S1 is a strip, not a lecture.
- Pluribus, CICERO and the game-AI history: keep them for questions.
- Thermal or other exotic covert channels.
- Growth-rate or "exponential" claims from the Erdős chart.
- The model's self-reported confidence presented as accuracy. Label MVP numbers as illustrative.
- Exploit payloads or other operational detail from the incident.
- Recommending RL on thoughts or inter-agent messages (S6 raises it only as a risk or open question).
- Forecasts of recursive self-improvement timelines.

## Cut line if questions are inside the 15 minutes

If the talk must be about 10 minutes, the musts need to lose about 2:00:
- drop M5 (×1000) and fold its point into one sentence in M4 (−35)
- drop M10 (DAN) and keep one sentence in M11 (−35)
- shorten M8 to the chart plus one card per lab (−20)
- shorten M7 to two examples (−20)

That gives about 9:10, with room for S1 only.

## Mapping from the current deck

| Current slide | Goes to |
|---|---|
| 2 Training vs. operation | S1 strip, plus a line in M3 |
| 3 Reliability | M2, M5 |
| 4 Tools and verification | M4 |
| 5 Horizontal scaling | M6 |
| 6 Competition and cooperation | S2 |
| 7–8 Science and Erdős chart | M8 (+ C2) |
| 9 Appropriate use | M9 (+ C3) |
| 10 Grids | C4 |
| 11 DAN / Crescendo | M10 |
| 12 Hugging Face | M11 |
| 13 Activity between checks | M6 (clock) and M12 |
| 14 Open questions | S3, S6, M12 |
