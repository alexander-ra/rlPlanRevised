# Interactive Study Viewer — UI/UX Improvement Plan

**Date:** 2026-04-07
**Scope:** Design inconsistencies, UI/UX improvements, and content-structure suggestions for the interactive study viewer (`interactiveStudy/src/` + `planning/rawSteps/`)

---

## 1. Visual Hierarchy & Typography

### 1.1 Step metadata header is unstyled plain text
**Problem:** Every step opens with a block of bold-text metadata (Duration, Dependencies, Phase, Freshness Note) that looks like regular body text. There's no visual containment, making it easy to skip past or confuse with content.

**Suggestion:** Render the metadata as a styled "info card" at the top of each step. This can be done in CSS by targeting the specific pattern, or in JS post-processing (similar to how YouTube links are converted to cards). A bordered card with the phase color as the left accent, showing duration/tier/dependencies in a compact grid, would make each step feel "scoped" immediately.

**Markdown change:** Wrap the metadata in a fenced div or use a consistent HTML comment marker that the JS can detect and restyle:
```markdown
<!-- step-meta -->
| Field | Value |
|---|---|
| Duration | 14 days (Tier 2) |
| Dependencies | Step 1, Step 3 |
| Phase | C — Neural Methods |
<!-- /step-meta -->
```

### 1.2 Phase Overview / Contribution Alignment blockquotes are visually identical to regular blockquotes
**Problem:** These two blockquotes at the top of each step carry critical context (why this step exists and how it connects to the thesis), but they look the same as any other `>` block in the content. A reader skimming will skip them.

**Suggestion:** Give them distinct styling — e.g., a colored background tint matching the step's phase, a left icon (compass for Phase Overview, target for Contribution Alignment), and slightly larger font. The JS already has the phase color available. Detection can use the `**Phase Overview:**` / `**Contribution Alignment:**` bold markers that are consistent across all 15 steps.

### 1.3 Too much emojis
**Problem:** Too many emojis are used all across the website — phase headings had emojis programmatically injected, status indicators used emoji, the theme toggle used emoji, and the homepage title used 📚.

**Suggestion:** Remove emojis from headers. The ones in the `.md` source keep — they are fine. Status indicators (done/active/upcoming) replace with CSS-styled dots. Theme toggle replaces with SVG sun/moon icons. Phase headings get a numbered CSS badge instead of emoji.


### 1.4 No visual differentiation between the 5 learning phases within a step
**Problem:** Each step has Phase 1 (Intuition) through Phase 5 (Consolidation). These are just H2 headings — there's no visual signal that you've moved from "reading" to "implementation". The 5-phase cycle is the pedagogical backbone of the entire plan, but it's invisible in the UI.

**Suggestion:** Add a subtle background tint or left-border color to each phase section. For example:
- Phase 1 (Intuition): light blue tint
- Phase 2 (Exploration): light green tint
- Phase 3 (Reading): light amber tint
- Phase 4 (Implementation): light red/rose tint
- Phase 5 (Consolidation): light violet tint

The JS can detect `## Phase N:` headings (consistent pattern across all steps) and wrap the content until the next H2 in a div with the appropriate class. Alternatively, a small colored pill/badge next to each Phase heading.

### 1.5 Heading hierarchy could use more contrast
**Problem:** H1, H2, H3 all use similar font sizes (1.6, 1.3, 1.1rem) with subtle differences. In long steps (step 14 is 64KB), it's hard to visually parse the structure at a glance.

**Suggestion:** Increase H1 to ~1.8rem. Give H2s a more distinct treatment — perhaps a phase-colored left bar instead of the current top border. Make H3s slightly more visually distinct from body text (currently 1.1rem vs body 0.88rem — the gap is small).

---

## 2. Navigation & Wayfinding

### 2.1 No reading progress indicator
**Problem:** On long steps (many are 30-50KB of markdown), there's no sense of "how far through this step am I?" beyond scrolling. The checkbox progress in the sidebar tracks task completion, not reading position.

**Suggestion:** Add a thin reading progress bar at the very top of the viewport (above the topbar, or integrated into it) that fills as the user scrolls through the content. This is a common pattern (Medium, dev.to, etc.) and is cheap to implement with a scroll event listener.

### 2.2 The section jump FAB icon is confusable with the sidebar hamburger
**Problem:** The FAB uses `☰` (trigram / hamburger icon) which is the same icon concept as the mobile sidebar hamburger. Two "hamburger" buttons in the same viewport is confusing.

**Suggestion:** Replace with an SVG "structured list / TOC outline" icon — horizontal lines of different indentation levels, clearly meaning "outline" not "menu". Distinct from the hamburger and relevant to "jump to section" semantics.

### 2.3 No breadcrumb or location context beyond topbar title
**Problem:** When reading a step, the topbar shows "Step 5: Neural Equilibrium" but doesn't show which phase of the plan you're in (Phase C — Neural Methods) or where in the 5-phase learning cycle you are within the step. The intersection observer updates the title with the current section, but it's a single line of text.

**Suggestion:** Add a dedicated subtitle row inside the topbar (below the main title). It shows: `Phase C — Neural Methods · §current-section` — combining plan phase context with the live section tracker. Clicking it scrolls to top. This replaces the hacked inline span approach from 2.5.

### 2.4 No step transition animation
**Problem:** Switching between steps is an instant content swap — the old content disappears, the new content appears. This feels abrupt, especially when navigating with arrow keys.

**Suggestion:** Add a CSS fade + subtle upward-translate exit animation (150ms), then a fade + downward-translate enter animation (200ms). Uses `@keyframes` classes added/removed by JS — avoids transition reversal issues on class removal.

### 2.5 The topbar section tracker (IntersectionObserver) has rough UX
**Problem:** The current section indicator in the topbar (e.g., "Step 5: Neural Equilibrium > Phase 3: Reading") uses inline styles, hardcoded emoji (❯), and a small "▲" click-to-top button embedded in the title text. It's functional but feels hacky — the clickable area is small, and mixing interaction into a title string is fragile.

**Suggestion:** Replaced by the 2.3 implementation: a proper `#topbar-section` element as a second line inside the topbar, updated by the IntersectionObserver. The whole subtitle row is a clickable scroll-to-top target. Clean separation from the title string.

---

## 3. Content Components

### 3.1 YouTube cards could show duration and instructor
**Problem:** YouTube links are converted to nice thumbnail cards, but they only show the link text as a title. The markdown already contains duration and instructor info on the line after each URL (`Duration: ~19m | Channel: DeepMind`), but it's not extracted.

**Suggestion:** After `embedYouTubeThumbnails()` replaces an `<a>` with a card, scan next sibling text nodes for a `Duration:` line. Parse out duration and `Channel:` / `Instructor:` fields. Render duration as a small dark badge bottom-right on the thumbnail; channel/instructor as a small subtitle line below the card title.

### 3.2 Paper reading guides (tree syntax) look raw
**Problem:** Steps use a tree syntax for structured reading guides (READ/SKIM/SKIP/MATH/KEY INSIGHT). These render as plain monospace code blocks.

**Suggestion:** Post-process any `<pre><code>` block whose content contains `├──` or `└──`. Parse each tree-prefix line into action type + content. Multi-line items continued with `│` or 4-space indent are joined. Render as a `.reading-guide` div: each item is a row with a color-coded badge (READ=green, SKIM=amber, SKIP=gray, MATH=blue, KEY INSIGHT=violet). Run BEFORE hljs so the original code block is replaced before syntax highlighting.

### 3.3 No code block copy button
**Problem:** Code blocks had no copy-to-clipboard button.

**Done:** Copy button now appears on hover in the top-right corner of every `<pre>` block.

### 3.4 No admonition/callout boxes
**Problem:** The markdown uses blockquotes with bold labels for planning notes, context, and cross-references. They all look the same visually.

**Suggestion:** Extend `styleSpecialBlockquotes()` to detect the real patterns in the rawSteps:
- `Know-How First compression` → amber/planning callout (planning artifact)
- `[Pn] ...` (plan decision labels) → neutral/dim, smaller font (cross-reference note)
- `Why this section exists`, `Before the papers` → teal/context (prereq/rationale)
- `Phase Overview` → already done

### 3.5 Tables lack interactivity
**Problem:** Tables are static — no visual feedback when hovering rows.

**Suggestion:** CSS-only `tbody tr:hover` with `surface-variant` background.

### 3.6 Image/figure support
**Problem:** Steps are text-only with no inline diagrams.

**Deferred:** Requires content-level edits to rawSteps markdown (adding image refs or mermaid diagrams). Not a pure UI task — deferred to a future content pass.

---

## 4. Homepage & Overview

### 4.1 Homepage header is minimal
**Problem:** The homepage shows a centered title, subtitle, and meta line. There's no visual impact — it looks like a plain list.

**Suggestion:** Add a hero section with:
- A gradient or phase-colored background strip
- A visual summary (e.g., "2/15 steps completed", progress ring/donut chart)
- Quick stats (days elapsed, days remaining, current step)
- The three thesis contributions as cards

### 4.2 Step cards on homepage are dense
**Problem:** Each step card shows: step number + status icon, phase badge, title, date range + days + tier, progress bar, description, and (optionally) download links. This is a lot of information in a small card with tiny text (0.72-0.78rem for most of it).

**Suggestion:**
- Increase base font size in cards slightly (0.8-0.85rem)
- Add more vertical spacing between elements
- Consider showing less by default and revealing details on hover/click (progressive disclosure)
- Group cards by phase with phase headers (currently they're just in a flat list with phase badges)

### 4.3 Calendar could show more at a glance
**Problem:** The calendar shows one month at a time with tiny color-coded cells. To see the full plan (Mar-Oct 2026), you need to click through 8 months.

**Suggestion:** Add a "full view" toggle that shows all 8 months in a compact grid (2x4 or 4x2). Each month shrinks but shows the phase color bands, giving a bird's-eye view of the whole plan. This makes the timeline tangible.

### 4.4 No overall progress visualization
**Problem:** There's checkbox progress per step, but no aggregate progress view. How far through the overall plan am I? How many steps are done vs active vs upcoming?

**Suggestion:** Add a plan-level progress section to the homepage:
- A horizontal progress bar showing steps 1-15 as segments (colored by phase, filled/unfilled by status)
- Aggregate stats: "2/15 completed, 28/232 days elapsed, 78 checkboxes checked"
- A Gantt-like horizontal bar chart (each step = a bar, positioned by date)

---

## 5. Sidebar

### 5.1 Schedule adjustment is cryptic
**Problem:** The sidebar footer shows "Delay (days)" with +/- buttons and "0/14". A first-time user won't understand what this does or why it exists.

**Suggestion:** Add a tooltip or one-line explanation: "Shift all step dates forward". When the value is non-zero, show the impact: "Plan ends: Oct 17 → Oct 31". Consider renaming to "Schedule Offset" or "Plan Shift".

### 5.2 Theme toggle is buried in the sidebar footer
**Problem:** On mobile, you have to open the sidebar and scroll to the bottom to access the theme toggle. On desktop, it's visible but in a low-priority position.

**Suggestion:** Add a theme toggle icon to the topbar (sun/moon icon button). Keep the sidebar one too for consistency.

### 5.3 Sidebar nav items could show more state
**Problem:** Nav items show step number + title + progress bar + optional report badge. There's no indication of completion status (done/active/upcoming) or dates.

**Suggestion:** Add a small status indicator (colored dot or icon) to each nav item:
- Green dot = completed
- Blue dot/pulse = active (current date range)
- Gray = upcoming

This mirrors the homepage step cards' status icons but in the sidebar context.

### 5.4 Phase groups in sidebar are collapsible?
**Problem:** Phase labels (e.g., "A — Foundation") are just static text. In a 15-item list, the sidebar is scrollable but not compactable.

**Suggestion:** Make phase groups collapsible (click phase label to show/hide its steps). Default to all expanded, but allow the user to collapse phases they've completed. Saves scroll distance and reduces cognitive load.

---

## 6. Mobile Experience

### 6.1 Bottom bar is underutilized
**Problem:** The mobile bottom bar has only two buttons (Previous / Next). This prime screen real estate could do more.

**Suggestion:** Add a center button for quick actions — e.g., a "sections" button (replaces the FAB which is harder to reach on tall phones), or a progress indicator showing current section position.

---

## 7. Content Structure (Markdown-Level Changes)

### 7.1 YouTube links should use markdown link syntax consistently
**Problem:** Some YouTube links are bare URLs on their own line:
```markdown
https://www.youtube.com/watch?v=nIgIv4IfJ6s
```
Others are in markdown link syntax. The bare URL format works (the JS detects and converts them to cards), but the link text becomes the URL itself, making the card title ugly.

**Suggestion:** Ensure all YouTube links use markdown link syntax with a descriptive title:
```markdown
[Reinforcement Learning: Crash Course AI #9](https://www.youtube.com/watch?v=nIgIv4IfJ6s)
```
This gives the card a proper human-readable title. Audit all 15 steps for consistency.

### 7.2 Exit Checklist structure varies across steps
**Problem:** Some steps have flat checklists, others have categorized sub-sections (Knowledge Gates, Deliverable Gates, etc.). The Exit Checklist is the key "am I done?" validator but its structure isn't consistent.

**Suggestion:** Standardize the Exit Checklist format across all steps:
```markdown
## Exit Checklist

### Knowledge Gates
- [ ] Can explain X to a non-expert
- [ ] Can derive Y from first principles

### Implementation Gates
- [ ] Code runs and produces expected output
- [ ] Tests pass

### Deliverable Gates
- [ ] One-pager written
- [ ] Learning log updated
```

### 7.3 The "Know-How First compression" notes are scattered
**Problem:** Some steps (e.g., Step 5) have a blockquote at the top explaining that the implementation phase has been compressed. This is a planning artifact that clutters the learning content.

**Suggestion:** 
- Style them as a collapsible "Planning Note" admonition so they don't dominate the top of the step

**Done:** Rendered as a collapsed `Planning Note` toggle with a chevron. Body hidden by default; click to expand. Uses the amber bq-planning color.

### 7.4 Math equation formatting inconsistency
**Problem:** Some steps use `$$...$$` for display math, others use `\[...\]`. Some inline math uses `$...$` (skipped by KaTeX config to avoid false positives), requiring `\(...\)` instead.

**Suggestion:** Standardize on `$$...$$` for display and `\(...\)` for inline. Audit all steps. Consider enabling single `$` delimiters in KaTeX if false positive rate is low.

### 7.5 No per-phase checkpoint milestones
**Problem:** All existing checkboxes are end-of-step deliverables (knowledge gates, implementation gates). During a step that takes 10–21 days, there's nothing to check off day-to-day. The 5 learning phases (Intuition, Exploration, Reading, Implementation, Consolidation) each have their own natural completion signal, but it's currently invisible in the UI.

**Suggestion:** Inject 2–3 lightweight checkpoints at the bottom of each phase section (auto-generated, not stored in the markdown). Examples:
- Phase 1 (Intuition): "Watched / read all Intuition resources" / "Can explain the core concept in one sentence"
- Phase 2 (Exploration): "Explored all listed tools and references" / "Identified 2–3 focus areas for Phase 3"
- Phase 3 (Reading): "Completed all READ items" / "Can recall the key algorithm without notes"
- Phase 4 (Implementation): "Code runs and produces expected output" / "Results pass sanity checks"
- Phase 5 (Consolidation): "Summary / learning-log entry written" / "Can connect this step to the thesis"

Stored in cloud with the `pchk_{stepId}_{phaseNum}_{idx}` key prefix. Count badge turns green when all done.

**Done:** Checkpoint cards injected at bottom of each `.phase-section` div. Phase-tinted header strip, cloud-persisted, all-done state turns the header green.

---

## 8. Polish & Delight

### 8.1 Loading screen could show which step is loading
**Problem:** The loading spinner says "Loading study plan..." but doesn't show progress or what's happening (downloading cloud data, parsing markdown, etc.).

**Suggestion:** Show step count or a deterministic progress bar: "Loading 15 steps... (cloud sync)". Since the build is a single file, loading is fast — but on slow connections or with cloud sync delays, feedback helps.

**Done:** Text updates to "Loading 15 steps…" immediately on DOMContentLoaded (before cloud call), then to "Building navigation…" after cloud sync completes.

### 8.2 No favicon feedback for active step
**Problem:** The brain emoji (🧠) favicon is static.

**Suggestion:** Could dynamically update the favicon to show the current phase color or step number. Minor polish.

### 8.3 Print stylesheet could be richer
**Problem:** The print CSS just hides navigation elements. Printed output loses all phase color coding and structure.

**Suggestion:** Enhance the print stylesheet to:
- Add phase color bands to headings
- Include step metadata in a header
- Add page breaks between major sections
- Include a mini TOC at the top

---

## 9. Technical / Performance

### 9.1 Consider lazy rendering
**Problem:** Currently, `renderStep()` calls `marked.parse()` on every navigation. For 15 steps, this is fine, but the parsing is repeated on every visit to the same step.

**Suggestion:** Cache the parsed HTML for each step after first render. Store in a Map: `parsedCache.set(stepId, html)`. Invalidation is unnecessary since content doesn't change at runtime.

**Done:** `_parsedCache` Map added; `marked.parse()` is now called only on first visit. Subsequent visits reuse cached HTML.

---

## Priority Matrix

| # | Improvement | Impact | Effort | Quick Win? | Status |
|---|---|---|---|---|---|
| 3.3 | Code block copy button | High | Low | Yes | ✅ Done |
| 1.3 | Emojis — remove from headers, CSS badges for phases, SVG icons for theme toggle | High | Low | Yes | ✅ Done |
| 2.1 | Reading progress bar | High | Low | Yes | ✅ Done |
| 5.2 | Theme toggle in topbar | Medium | Low | Yes | ✅ Done |
| 1.1 | Step metadata info card | High | Medium | | ✅ Done |
| 1.2 | Distinct Phase Overview blockquote | Medium | Low | Yes | ✅ Done |
| 1.4 | Phase section tinting | Medium | Medium | | ✅ Done |
| 1.5 | Heading hierarchy contrast (H1/H2/H3) | Medium | Low | Yes | ✅ Done |
| 2.4 | Step transition animation | Medium | Low | Yes | ✅ Done |
| 2.2 | Better FAB icon | Low | Low | Yes | ✅ Done |
| 2.3 | Breadcrumb navigation | Low | Medium | | ✅ Done |
| 2.6 | Clean up topbar section tracker | Low | Medium | | ✅ Done |
| 3.4 | Admonition/callout boxes | Medium | Medium | | ✅ Done |
| 3.2 | Styled reading guides (READ/SKIM/SKIP) | Medium | Medium | | ✅ Done |
| 3.5 | Table row hover | Low | Low | Yes | ✅ Done |
| 3.1 | YouTube card metadata (duration/instructor) | Low | Medium | | ✅ Done |
| 4.4 | Overall progress visualization | Medium | Medium | | ✅ Done |
| 5.3 | Nav item status indicators | Low | Low | Yes | |
| 5.4 | Collapsible phase groups | Low | Medium | | |
| 4.3 | Full calendar view | Low | Medium | | ✅ Done |
| 7.1 | YouTube link syntax audit | Low | Low | Yes (MD edit) | |
| 7.2 | Standardize exit checklists | Medium | Medium | MD edit | |
| 7.3 | Collapsible planning notes | Medium | Low | Yes | ✅ Done |
| 7.4 | Math formatting audit | Low | Medium | MD edit | |
| 7.5 | Per-phase checkpoint cards | High | Low | Yes | ✅ Done |
| 9.1 | Lazy rendering / cache | Low | Low | Yes | ✅ Done |
| 9.2 | Service worker | Low | Medium | | |
| 3.6 | Inline figures/diagrams | High | High | | Deferred |
| 6.1 | Richer mobile bottom bar | Low | Low | | ✅ Done |
| 6.2 | Simplified mobile timeline | Low | Medium | | |
| 8.1 | Enhanced loading screen | Low | Low | | ✅ Done |
| 8.3 | Richer print stylesheet | Low | Medium | | ✅ Done |
| 4.2 | Less dense homepage step cards | Medium | Low | Yes | ✅ Done |
| 9.3 | Inline critical CDN resources | Low | Medium | | |
