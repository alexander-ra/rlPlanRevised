# Hi-fi slide directions: brief

## Context

A 24 October talk, "Multi-Agent AI for Complex Problem Solving: Opportunities and Risks", given in Bulgarian with English slides to a non-technical audience. The lofi storyboard (`deliverables/agentic_ai_study/lofi/storyboard.html`) defines every slide as a list of elements on a 1600×900 canvas and morphs between consecutive slides; read its `render`, `drawBox`, `drawArrow` and `lerpEls` code to see how elements are drawn and morphed.

We are exploring hi-fi directions on two showcase slides:

- **F5a "Tools and a check"**: a five-step chain answers "Which is cheaper from Ruse to Sofia — driving or taking the train?". The calculator step becomes exact (100%); a check with four tests (sources agree ✓, sensible range ✓, date & currency ✗, recompute ✓) catches that the train fare came from a 2025 page priced in leva; a back arrow ("✗ fare from a 2025 page, in leva") returns to that step; the answer is on hold at 92%.
- **N2 "Acting in the world, through two doors"**: a conference system (~127 agents) brings 100 attendees from 15 countries to Ruse by the 23rd, under €30,000. A lead, three groups (Transport, Accommodation, Correspondence), five teams, three checks and a shared "living plan". It touches the outside world through only two doors: Correspondence writes to people (attendees, hotels, carriers by email); Payments (×2) is the only group that can pay (booking systems, payment card), after the budget guard, and anything over €500 needs the organiser's approval.

Their predecessors **F4** ("Thinking before each step") and **N1** ("A real-scale job: 100 people to this conference") are included so each variant can show its transition *into* the showcase slides. The sequence is F4 → F5a → N1 → N2.

## Data

`hifi/frames.json` holds the four frames exactly as in the storyboard: title, speaker note and every element (ids, kinds, positions, labels, states, percentages, arrows). It is the source of truth for content. `script_bg.md` is the Bulgarian spoken script, for context.

All text and numbers of the four frames must appear. You may restyle, re-layout and regroup freely; shorten a label only if you say so in your report.

## Deliverable

One self-contained HTML file, `deliverables/agentic_ai_study/hifi/vN-<slug>.html`:

- **No external scripts.** Script CDNs are unreachable from this machine, and the page should stand alone. Google Fonts stylesheets do load; give every face a fallback stack.
- **Stage:** a logical 1600×900 canvas, scaled uniformly to fit the window, centred and letterboxed with the page background. It must look right at 1920×1080, 1600×900, 1280×720 and about 800×450.
- **Navigation:** F4 → F5a → N1 → N2. → / Space / Page Down / click go forward, ← / Page Up back, using your transition. A slim control bar (frame buttons, "Replay transition") that never covers the stage.
- **Review hooks** (no UI shown in these modes):
  - `?frame=F5a` renders the final state of a frame;
  - `?frame=F5a&from=F4&t=0.5` renders the transition frozen at linear progress t ∈ [0, 1], with your easing applied inside. The same for `frame=N2&from=N1`.
  - Seed any randomness, so these renders are deterministic.
- **Reduced motion:** under `prefers-reduced-motion`, replace movement with a short crossfade.
- Do not modify other files and do not use git.

## Quality bar

We check every variant in screenshots against this:

1. **Fill the stage.** Size and centre the diagram to use the space between title and caption, with consistent outer margins and no large empty bands. The lofi frames leave big empty areas (F5a's top third, for one); fix that.
2. **Hierarchy.** The slide's news is the focus. F5a: the exact calculator, the check and what it catches (the failing fare step, the back arrow), the answer on hold. N2: the two doors to the outside world, and the budget guard with the organiser's approval above €500.
3. **No overlaps or clipping.** Text sits inside its box with padding; labels never collide; arrows attach to box edges with visible arrowheads and avoid crossing text.
4. **Transitions.** Elements that persist keep their identity and move or resize smoothly; new ones enter with intent (staggered, from a sensible origin); removed ones leave cleanly; changing labels crossfade rather than overlap. About 600–1200 ms with a deliberate easing. Frames at t = 0.25, 0.5 and 0.75 must not look broken.
5. **Legibility on a projector:** primary labels at least 20 px, secondary at least 15 px on the 1600×900 canvas, with strong contrast.
6. **Consistent semantics:** good / warning / bad / check keep one colour each, and an element type looks the same on every slide.
7. **No stock "AI-generated" look:** no cream + serif + terracotta, no neon green on black, no purple-to-blue gradients, no Inter or Space Grotesk, no emoji as icons.

## Self-review before reporting

Render your page with Playwright (`node`, `require('playwright')`; Chromium is preinstalled) at the review URLs: both showcase frames and both transitions at t = 0.25, 0.5 and 0.75, and the live page at 1280×720 and 800×450. Look at every screenshot, fix what is off, and repeat until it holds up. Keep your scripts and screenshots in your scratch folder (given in your task).

## Report (at most 200 words)

The file path; the idea in two sentences; what is worth reusing even if the whole variant is not chosen; the transition timing and easing; anything not done or known issues; the paths of your final screenshots.

## The five directions

Three keep the storyboard's structure and refine it; two are deliberately experimental, meant as inspiration rather than to land as is.

### V1: Refined light (conservative)

Keep the storyboard's layout logic and its morph model (same element identities, interpolated geometry), brought to presentation quality: a considered type pairing, a calm light palette with deliberate neutrals, depth used sparingly and only where it means something, refined badges, pills and chips, cleanly routed arrows, and the layout re-fitted to fill the stage. Transitions: geometry morph with a well-chosen ease (expo or cubic in-out, or a spring), staggered entry of new elements, crossfading text, and a brief highlight on what changed. The safe, polished option.

### V2: Projector dark (conservative)

The same diagrams designed for a dark room and a projector: a dark ground, high-contrast light text, semantic accents that stay readable when projected (not neon), bigger type, fewer hairlines. Motion as craft: arrows draw on, percentages count to their new values, persistent elements glide, and the news gets one subtle pulse.

### V3: Icons and the change (conservative, with build steps)

Each box gets a simple, consistent line icon (search, fuel, ticket, calculator, compare, checklist, people, hotel, plate, envelope, card, shield and so on), drawn as inline SVG with no icon library. The slide emphasises what changed since the previous one: unchanged parts recede, new or changed parts carry full colour. Add presenter build steps, so a slide reveals its news in two or three clicks. F5a: (1) the calculator becomes exact, (2) the check appears, (3) it catches the fare: back arrow, answer on hold. N2: (1) the outside-world band and the two doors, (2) the budget guard and the organiser's approval, (3) payments. → advances build steps before slides; `?frame=N2` shows the last step and `?frame=N2&beat=1` a given one.

### V4: A hundred attempts (experimental)

Make probability visible. Instead of percentage badges, 100 small dots (attempts) travel through the pipeline. Each step loses dots at its error rate; exact steps lose none; the check catches bad dots and sends them back along the redo arrow; the answer counts arrivals ("92 of 100, on hold"). On N2 the dots are actions and messages: they can leave the system only through the two doors, and payments queue at the guard, those over €500 passing only after the organiser approves. Keep the diagram minimal so the flow is the hero. The state must be a pure function of time and seed, so `t` freezes it deterministically.

### V5: Transit map (experimental)

The running example is a journey (Ruse → Sofia), so draw the AI system as a transit map. Steps are stations on a line from the question (origin) to the answer (terminus); a tool is an express segment; the check is an inspection interchange; the failing fare is a red signal with a return loop. On N2 the conference system is a network map: groups are coloured lines, the living plan is the central interchange, the two doors are the only exits to an "outside world" zone, the budget guard is a toll gate and the organiser a control point. Transitions: lines draw in, stations appear, a train runs the route. Transit-sign typography and 45°/90° line geometry. It does not need to follow the storyboard's layout.
