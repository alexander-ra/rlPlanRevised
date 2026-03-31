# Interactive Study Viewer — Build Plan

> **Goal:** A mobile-friendly, responsive HTML viewer for the 15 rawSteps markdown files.  
> **Output:** 1 standalone HTML file (`dist/index.html`) — open on any device.  
> **Source folder:** `interactiveStudy/`  
> **Build tool:** Python 3 script (no npm, no bundler, zero external deps).

---

## 0. Content Inventory (reference)

| # | File | Lines | Phase | Short Title |
|---|------|------:|-------|-------------|
| 1 | `step_01_rl_basics.md` | 286 | A — Foundation | RL Basics |
| 2 | `step_02_game_theory_cfr.md` | 384 | A — Foundation | Game Theory + CFR |
| 3 | `step_03_cfr_variants_mc.md` | 331 | B — Scaling | CFR Variants + MC |
| 4 | `step_04_game_abstraction_scaling.md` | 373 | B — Scaling | Game Abstraction |
| 5 | `step_05_neural_equilibrium.md` | 390 | C — Neural Methods | Neural Equilibrium |
| 6 | `step_06_end_to_end_game_ai.md` | 587 | C — Neural Methods | End-to-End Game AI |
| 7 | `step_07_opponent_modeling.md` | 538 | D — Opponent Modeling | Opponent Modeling |
| 8 | `step_08_safe_exploitation.md` | 631 | D — Opponent Modeling | Safe Exploitation |
| 9 | `step_09_multi_agent_rl.md` | 495 | E — Multi-Agent | Multi-Agent RL |
| 10 | `step_10_population_training_evo_gt.md` | 530 | E — Multi-Agent | Population Training |
| 11 | `step_11_coalition_formation_ffa.md` | 621 | E — Multi-Agent | Coalition Formation |
| 12 | `step_12_sequence_models_llm_agents.md` | 517 | F — Data-Driven | Sequence Models + LLM |
| 13 | `step_13_behavioral_analysis.md` | 814 | F — Data-Driven | Behavioral Analysis |
| 14 | `step_14_evaluation_frameworks.md` | 855 | G — Integration | Evaluation Frameworks |
| 15 | `step_15_research_frontier_mapping.md` | 729 | G — Integration | Research Frontier |

**Total:** 8,081 lines, 592 KB of Markdown.

### Markdown features detected across files
- Headers: H1 (`#`), H2 (`##`), H3 (`###`)
- Code blocks: ` ```python `, ` ```bash `, ` ```yaml `, plain ` ``` ` (all 15 files)
- Tables: pipe-delimited GFM tables (all 15 files)
- Lists: ordered, unordered, deeply nested (3–4 levels)
- Inline formatting: `**bold**`, `*italic*`, `` `inline code` ``
- Links: external URLs (YouTube, ArXiv, GitHub) — must open in new tab on mobile
- Emoji markers: 🔴 🟡 🟢 (used for HAND-CODE / AI-ASSISTED / AI-GENERATED tags)
- Horizontal rules: `---`
- ASCII box diagrams: `├──`, `└──`, `│` inside code blocks
- LaTeX math: inline `$...$` and display `$$...$$` — present in steps 11, 13, 14
- Checkboxes: `- [ ]` task lists in several files

---

## 1. Folder Structure

```
interactiveStudy/
├── src/
│   ├── shell.html          # HTML template (skeleton + CDN refs)
│   ├── styles.css           # All CSS (layout, typography, responsive)
│   ├── app.js               # Navigation, rendering, state, event handlers
│   └── icons.svg            # Inline SVG icons (hamburger, arrows, etc.)
├── build.py                 # Build script — reads sources, inlines everything → dist/
├── dist/                    # OUTPUT (gitignored or committed — your call)
│   └── index.html           # The single standalone file to share
└── README.md                # Quick usage instructions
```

### Why separate source files?
- Easier to edit/debug CSS and JS independently
- Syntax highlighting and linting in VS Code
- Build script handles the "merge into one file" step automatically
- Re-running `python3 build.py` regenerates `dist/index.html` instantly

---

## 2. Step-by-Step Execution Plan

### Step 1 — Create folder structure and skeleton files

Create the directory tree:

```bash
mkdir -p interactiveStudy/src interactiveStudy/dist
touch interactiveStudy/src/shell.html
touch interactiveStudy/src/styles.css
touch interactiveStudy/src/app.js
touch interactiveStudy/build.py
```

---

### Step 2 — Write `shell.html` (HTML template)

This is the core HTML structure with placeholder markers that `build.py` will replace.

**Requirements:**
- `<!DOCTYPE html>` with `<html lang="en">`
- `<meta charset="UTF-8">`
- `<meta name="viewport" content="width=device-width, initial-scale=1.0">` (critical for mobile)
- `<title>RL Study — Raw Steps</title>`
- CDN `<link>` and `<script>` tags for external libraries (see Step 3)
- Placeholder comments for inlining:
  - `<!-- INLINE_CSS -->` — replaced with `<style>` contents of `styles.css`
  - `<!-- INLINE_JS -->` — replaced with `<script>` contents of `app.js`
  - `<!-- INLINE_CONTENT -->` — replaced with `<script>` containing embedded step markdown

**HTML body structure:**

```html
<body>
  <!-- OVERLAY BACKDROP (mobile nav) -->
  <div id="overlay" class="overlay"></div>

  <!-- SIDEBAR NAVIGATION -->
  <nav id="sidebar" class="sidebar">
    <div class="sidebar-header">
      <h2>Study Steps</h2>
      <button id="close-sidebar" class="icon-btn" aria-label="Close menu">✕</button>
    </div>
    <div id="nav-list" class="nav-list">
      <!-- Populated by JS: grouped by phase -->
    </div>
  </nav>

  <!-- MAIN LAYOUT -->
  <div id="main" class="main">
    <!-- TOP BAR -->
    <header class="topbar">
      <button id="hamburger" class="icon-btn" aria-label="Open menu">☰</button>
      <span id="topbar-title" class="topbar-title">Step 1</span>
      <div class="topbar-nav">
        <button id="prev-btn" class="nav-btn" aria-label="Previous step">← Prev</button>
        <button id="next-btn" class="nav-btn" aria-label="Next step">Next →</button>
      </div>
    </header>

    <!-- CONTENT AREA -->
    <article id="content" class="content">
      <!-- Rendered markdown goes here -->
    </article>

    <!-- BOTTOM NAV (visible on mobile) -->
    <footer class="bottombar">
      <button id="prev-btn-bottom" class="nav-btn full-width">← Previous Step</button>
      <button id="next-btn-bottom" class="nav-btn full-width">Next Step →</button>
    </footer>
  </div>
</body>
```

---

### Step 3 — CDN Library References

Add these to `<head>` in `shell.html`. They stay as CDN links in the built file (keeps it small; requires internet on first load, then cached).

```html
<!-- marked.js — Markdown parser -->
<script src="https://cdn.jsdelivr.net/npm/marked@15.0.7/marked.min.js"></script>

<!-- highlight.js — Code syntax highlighting -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/styles/github.min.css">
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/highlight.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/languages/python.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/languages/bash.min.js"></script>
<script src="https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@11.11.1/build/languages/yaml.min.js"></script>

<!-- KaTeX — Math rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.21/dist/contrib/auto-render.min.js"></script>
```

**Note on versions:** Pin to specific versions (not `@latest`) so the viewer never breaks from a library update.

---

### Step 4 — Write `styles.css`

All CSS for the viewer. Major sections:

#### 4.1 — CSS Reset & Base Typography

```
* { margin: 0; padding: 0; box-sizing: border-box; }
html { font-size: 16px; scroll-behavior: smooth; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
       color: #1a1a2e; background: #fafbfc; line-height: 1.65; }
```

#### 4.2 — Sidebar

- Fixed left, full height, width 280px
- Background: `#1a1a2e` (dark navy) — contrasts with white content
- Nav items: grouped by phase with phase labels as small uppercase headers
- Active item: left border accent + highlighted background
- Phase group: collapsible or always-open (decide: always-open is simpler, recommended for 15 items)
- Scrollable if content overflows (unlikely with 15 items + 7 phase headers)
- Mobile: `transform: translateX(-100%)` by default, slides in with `transform: translateX(0)` when `.open` class is added
- Transition: `transform 0.25s ease`

#### 4.3 — Overlay

- Mobile only: semi-transparent black backdrop behind open sidebar
- `position: fixed; inset: 0; background: rgba(0,0,0,0.4); z-index: 90;`
- Hidden by default, shown when sidebar is open

#### 4.4 — Topbar

- Sticky top, height ~52px
- Background: white, subtle bottom border/shadow
- Hamburger button: left side (hidden on desktop ≥768px)
- Step title: center
- Prev/Next: right side (hidden on mobile — they appear at bottom instead)

#### 4.5 — Content Area

- `max-width: 800px; margin: 0 auto; padding: 1rem 1.25rem 6rem;`
- Bottom padding: 6rem to clear mobile bottom bar
- Heading styles: H1 larger, H2 with subtle top border, H3 slightly smaller
- Code blocks: `overflow-x: auto; background: #f6f8fa; border-radius: 6px; padding: 1rem; font-size: 0.9rem;`
- Tables: full-width, horizontal scroll wrapper, striped rows
- Links: colored, underlined
- Blockquotes: left border accent
- Task list checkboxes (`- [ ]` / `- [x]`): styled as real checkboxes (read-only)
- Emoji: rendered natively (no special handling needed)

#### 4.6 — Bottom Bar (mobile)

- `position: fixed; bottom: 0; left: 0; right: 0; height: 52px;`
- Two buttons side by side: ← Previous | Next →
- Background: white, top border/shadow
- Hidden on desktop (≥768px)

#### 4.7 — Responsive Breakpoints

```css
/* Mobile-first (default): sidebar hidden, bottombar visible, hamburger visible */

@media (min-width: 768px) {
  /* Sidebar: always visible, not overlaid */
  .sidebar { transform: translateX(0); position: fixed; }
  .main { margin-left: 280px; }
  #hamburger { display: none; }
  #close-sidebar { display: none; }
  .overlay { display: none !important; }
  .bottombar { display: none; }
  .topbar .topbar-nav { display: flex; }
}
```

#### 4.8 — Landscape Mobile Consideration

- Landscape phone: typically 667×375 (iPhone SE) or 812×375 (iPhone X)
- Sidebar should still be hamburger-triggered (under 768px height doesn't help)
- Content area: reduce vertical padding
- Bottom bar: slightly shorter (44px)

```css
@media (max-width: 767px) and (orientation: landscape) {
  .topbar { height: 44px; }
  .bottombar { height: 44px; }
  .content { padding-bottom: 4rem; }
}
```

#### 4.9 — Print Styles (optional, low priority)

```css
@media print {
  .sidebar, .topbar, .bottombar, .overlay { display: none; }
  .main { margin-left: 0; }
  .content { max-width: 100%; }
}
```

---

### Step 5 — Write `app.js` — Step Metadata & Content Registry

Define the metadata array that maps step IDs to titles, phases, and short labels:

```javascript
const STEP_META = [
  { id: "step_01", num: 1,  title: "RL Basics",                    phase: "A", phaseLabel: "A — Foundation" },
  { id: "step_02", num: 2,  title: "Game Theory + CFR",            phase: "A", phaseLabel: "A — Foundation" },
  { id: "step_03", num: 3,  title: "CFR Variants + MC",            phase: "B", phaseLabel: "B — Scaling" },
  { id: "step_04", num: 4,  title: "Game Abstraction",             phase: "B", phaseLabel: "B — Scaling" },
  { id: "step_05", num: 5,  title: "Neural Equilibrium",           phase: "C", phaseLabel: "C — Neural Methods" },
  { id: "step_06", num: 6,  title: "End-to-End Game AI",           phase: "C", phaseLabel: "C — Neural Methods" },
  { id: "step_07", num: 7,  title: "Opponent Modeling",             phase: "D", phaseLabel: "D — Opponent Modeling" },
  { id: "step_08", num: 8,  title: "Safe Exploitation",            phase: "D", phaseLabel: "D — Opponent Modeling" },
  { id: "step_09", num: 9,  title: "Multi-Agent RL",               phase: "E", phaseLabel: "E — Multi-Agent" },
  { id: "step_10", num: 10, title: "Population Training",          phase: "E", phaseLabel: "E — Multi-Agent" },
  { id: "step_11", num: 11, title: "Coalition Formation",          phase: "E", phaseLabel: "E — Multi-Agent" },
  { id: "step_12", num: 12, title: "Sequence Models + LLM",        phase: "F", phaseLabel: "F — Data-Driven" },
  { id: "step_13", num: 13, title: "Behavioral Analysis",          phase: "F", phaseLabel: "F — Data-Driven" },
  { id: "step_14", num: 14, title: "Evaluation Frameworks",        phase: "G", phaseLabel: "G — Integration" },
  { id: "step_15", num: 15, title: "Research Frontier",            phase: "G", phaseLabel: "G — Integration" },
];
```

The `STEPS_CONTENT` object (mapping `step_01` → raw markdown string) will be generated by `build.py` and injected at the `<!-- INLINE_CONTENT -->` placeholder as a separate `<script>` block.

---

### Step 6 — Write `app.js` — Sidebar Navigation Builder

Function `buildNav()`:

1. Group `STEP_META` entries by `phase` (preserving order).
2. For each phase group, create:
   - A phase header: `<div class="phase-label">A — Foundation</div>`
   - Step items: `<button class="nav-item" data-step="step_01">1. RL Basics</button>`
3. Insert into `#nav-list`.
4. Attach click handlers: each button calls `navigateTo(stepId)`.

**Active state management:**
- `currentStepIndex` variable (0-based into `STEP_META`)
- `updateActiveNav()` — removes `.active` from all nav items, adds to current

---

### Step 7 — Write `app.js` — Markdown Rendering Pipeline

Function `renderStep(stepId)`:

```javascript
function renderStep(stepId) {
  const md = STEPS_CONTENT[stepId];
  if (!md) return;

  // 1. Parse markdown → HTML
  const html = marked.parse(md);

  // 2. Insert into DOM
  const contentEl = document.getElementById('content');
  contentEl.innerHTML = html;

  // 3. Syntax-highlight code blocks
  contentEl.querySelectorAll('pre code').forEach(block => {
    hljs.highlightElement(block);
  });

  // 4. Render LaTeX math (KaTeX auto-render)
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(contentEl, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "$",  right: "$",  display: false },
      ],
      throwOnError: false
    });
  }

  // 5. Make external links open in new tab
  contentEl.querySelectorAll('a[href^="http"]').forEach(a => {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });

  // 6. Wrap tables in scrollable container
  contentEl.querySelectorAll('table').forEach(table => {
    if (!table.parentElement.classList.contains('table-wrap')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrap';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // 7. Scroll to top
  contentEl.scrollTo(0, 0);
  window.scrollTo(0, 0);
}
```

**marked.js configuration** (run once at startup):

```javascript
marked.setOptions({
  gfm: true,            // GitHub-Flavored Markdown (tables, task lists)
  breaks: false,         // Don't convert \n to <br> (files use proper spacing)
  headerIds: true,       // Generate IDs on headings for in-page anchoring
  mangle: false,         // Don't mangle header IDs
});
```

---

### Step 8 — Write `app.js` — Navigation Logic

```javascript
let currentStepIndex = 0;

function navigateTo(stepId) {
  const idx = STEP_META.findIndex(s => s.id === stepId);
  if (idx === -1) return;
  currentStepIndex = idx;

  // Render content
  renderStep(stepId);

  // Update nav active state
  updateActiveNav();

  // Update topbar title
  const meta = STEP_META[idx];
  document.getElementById('topbar-title').textContent =
    `Step ${meta.num}: ${meta.title}`;

  // Update URL hash (for bookmarking / sharing)
  history.replaceState(null, '', `#${stepId}`);

  // Update prev/next button states
  updateNavButtons();

  // Close sidebar if open (mobile)
  closeSidebar();
}

function goNext() {
  if (currentStepIndex < STEP_META.length - 1) {
    navigateTo(STEP_META[currentStepIndex + 1].id);
  }
}

function goPrev() {
  if (currentStepIndex > 0) {
    navigateTo(STEP_META[currentStepIndex - 1].id);
  }
}

function updateNavButtons() {
  const atStart = currentStepIndex === 0;
  const atEnd = currentStepIndex === STEP_META.length - 1;
  // Disable/enable all prev/next buttons (topbar + bottombar)
  document.querySelectorAll('[id^="prev-btn"]').forEach(b => b.disabled = atStart);
  document.querySelectorAll('[id^="next-btn"]').forEach(b => b.disabled = atEnd);
}
```

---

### Step 9 — Write `app.js` — Sidebar Toggle (Mobile)

```javascript
function openSidebar() {
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('overlay').classList.add('visible');
  document.body.style.overflow = 'hidden'; // prevent background scroll
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('visible');
  document.body.style.overflow = '';
}
```

Wire up:
- `#hamburger` → `openSidebar()`
- `#close-sidebar` → `closeSidebar()`
- `#overlay` click → `closeSidebar()`

---

### Step 10 — Write `app.js` — Initialization

```javascript
document.addEventListener('DOMContentLoaded', () => {
  // Build sidebar navigation
  buildNav();

  // Wire up event listeners
  document.getElementById('hamburger').addEventListener('click', openSidebar);
  document.getElementById('close-sidebar').addEventListener('click', closeSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  document.getElementById('prev-btn').addEventListener('click', goPrev);
  document.getElementById('next-btn').addEventListener('click', goNext);
  document.getElementById('prev-btn-bottom').addEventListener('click', goPrev);
  document.getElementById('next-btn-bottom').addEventListener('click', goNext);

  // Check URL hash for initial step
  const hash = window.location.hash.replace('#', '');
  const initialStep = STEP_META.find(s => s.id === hash) ? hash : STEP_META[0].id;
  navigateTo(initialStep);

  // Handle browser back/forward
  window.addEventListener('hashchange', () => {
    const h = window.location.hash.replace('#', '');
    if (STEP_META.find(s => s.id === h)) {
      navigateTo(h);
    }
  });
});
```

**Keyboard navigation** (nice UX for desktop):

```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { goPrev(); e.preventDefault(); }
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { goNext(); e.preventDefault(); }
  if (e.key === 'Escape') { closeSidebar(); }
});
```

**Swipe navigation** (mobile gesture):

```javascript
let touchStartX = 0;
let touchStartY = 0;
document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
  touchStartY = e.changedTouches[0].screenY;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].screenX - touchStartX;
  const dy = e.changedTouches[0].screenY - touchStartY;
  // Only trigger on horizontal swipes (dx > dy, minimum 80px)
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 80) {
    if (dx > 0 && currentStepIndex > 0) {
      // Swipe right → previous step (or open sidebar if at step 1)
      if (touchStartX < 30) { openSidebar(); } // edge swipe → open nav
      else { goPrev(); }
    } else if (dx < 0) {
      goNext();
    }
  }
}, { passive: true });
```

---

### Step 11 — Write `build.py` — The Build Script

This is the central piece that reads all source files and produces `dist/index.html`.

**High-level flow:**

```python
#!/usr/bin/env python3
"""Build script for Interactive Study Viewer.

Reads source files from src/ and rawSteps content,
produces a single standalone dist/index.html.

Usage: python3 build.py
"""

import os
import json
from pathlib import Path

# Paths
SCRIPT_DIR   = Path(__file__).parent.resolve()
SRC_DIR      = SCRIPT_DIR / "src"
DIST_DIR     = SCRIPT_DIR / "dist"
RAW_STEPS_DIR = SCRIPT_DIR.parent / "planning" / "rawSteps"

# Step file list (order matters)
STEP_FILES = [
    "step_01_rl_basics.md",
    "step_02_game_theory_cfr.md",
    "step_03_cfr_variants_mc.md",
    "step_04_game_abstraction_scaling.md",
    "step_05_neural_equilibrium.md",
    "step_06_end_to_end_game_ai.md",
    "step_07_opponent_modeling.md",
    "step_08_safe_exploitation.md",
    "step_09_multi_agent_rl.md",
    "step_10_population_training_evo_gt.md",
    "step_11_coalition_formation_ffa.md",
    "step_12_sequence_models_llm_agents.md",
    "step_13_behavioral_analysis.md",
    "step_14_evaluation_frameworks.md",
    "step_15_research_frontier_mapping.md",
]
```

**Step 11.1 — Read all markdown content:**

```python
def read_steps():
    """Read all rawSteps markdown files into a dict."""
    steps = {}
    for filename in STEP_FILES:
        step_id = filename.replace(".md", "")  # e.g. "step_01_rl_basics"
        # Normalize to short ID: "step_01"
        short_id = "_".join(step_id.split("_")[:2])  # "step_01"
        filepath = RAW_STEPS_DIR / filename
        content = filepath.read_text(encoding="utf-8")
        steps[short_id] = content
    return steps
```

**Step 11.2 — Generate the content script block:**

```python
def generate_content_script(steps: dict) -> str:
    """Generate a <script> block with STEPS_CONTENT object."""
    # JSON-encode each value to safely embed in JS
    # (handles backticks, quotes, newlines, $-signs)
    pairs = []
    for step_id, content in steps.items():
        escaped = json.dumps(content)  # JSON string with proper escaping
        pairs.append(f'  "{step_id}": {escaped}')

    js = "const STEPS_CONTENT = {\n" + ",\n".join(pairs) + "\n};"
    return f"<script>\n{js}\n</script>"
```

> **Why json.dumps?** Template literals (backticks) would break on any backtick in the markdown content (code blocks use them constantly). JSON.dumps safely escapes all special characters including `\n`, `"`, `\`, and `$`.

**Step 11.3 — Inline CSS and JS into HTML:**

```python
def build():
    """Main build function."""
    # Read source files
    shell_html = (SRC_DIR / "shell.html").read_text(encoding="utf-8")
    styles_css = (SRC_DIR / "styles.css").read_text(encoding="utf-8")
    app_js     = (SRC_DIR / "app.js").read_text(encoding="utf-8")

    # Read and generate content
    steps = read_steps()
    content_script = generate_content_script(steps)

    # Replace placeholders
    output = shell_html
    output = output.replace("<!-- INLINE_CSS -->", f"<style>\n{styles_css}\n</style>")
    output = output.replace("<!-- INLINE_JS -->", f"<script>\n{app_js}\n</script>")
    output = output.replace("<!-- INLINE_CONTENT -->", content_script)

    # Write output
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DIST_DIR / "index.html"
    out_path.write_text(output, encoding="utf-8")

    # Report
    size_kb = out_path.stat().st_size / 1024
    print(f"✅ Built {out_path} ({size_kb:.0f} KB)")
    print(f"   Embedded {len(steps)} steps")

if __name__ == "__main__":
    build()
```

**Step 11.4 — Edge cases the build script must handle:**

- **Backticks in markdown:** Handled by `json.dumps` (not template literals).
- **Dollar signs in markdown:** Handled by `json.dumps` (no template literal interpolation).
- **Backslashes in code blocks:** Handled by `json.dumps` double-escaping.
- **Unicode (emoji 🔴🟡🟢, UTF-8):** Handled by Python 3 default UTF-8 encoding.
- **Empty files:** Guard with `if not content: continue`.
- **Missing rawSteps dir:** Fail fast with clear error message.

---

### Step 12 — Wire Up Event Handlers and Test Locally

After all source files are written:

```bash
cd interactiveStudy
python3 build.py
```

Open `dist/index.html` in a browser:

```bash
# Option A: direct file
xdg-open dist/index.html

# Option B: local server (some browsers block file:// for CORS)
python3 -m http.server 8080 -d dist
# then open http://localhost:8080
```

**Manual testing checklist:**

| # | Test | How to verify |
|---|------|--------------|
| 1 | All 15 steps load | Click each one in sidebar |
| 2 | Code blocks highlighted | Python/bash blocks should have syntax colors |
| 3 | Tables render properly | Should have borders, be horizontally scrollable |
| 4 | Math renders (steps 11, 13, 14) | Check for rendered LaTeX, not raw `$...$` |
| 5 | External links open in new tab | Click a YouTube/ArXiv link |
| 6 | Prev/Next navigation works | Both topbar and bottombar buttons |
| 7 | Hash navigation works | Manually go to `index.html#step_07`, refresh |
| 8 | Keyboard arrows work | Left/Right arrows change steps |
| 9 | Mobile hamburger menu | Chrome DevTools → Toggle Device Toolbar → iPhone SE |
| 10 | Sidebar closes on item click | Click a step in mobile sidebar |
| 11 | Sidebar closes on overlay click | Click dark backdrop area |
| 12 | Landscape mobile layout | DevTools → rotate device |
| 13 | Swipe gestures | DevTools → touch simulation, swipe left/right |
| 14 | Long content scrolls properly | Scroll through step 13 (814 lines, longest) |
| 15 | Task checkboxes render | Check steps with `- [ ]` items |
| 16 | Emoji markers visible | 🔴🟡🟢 should display as colored circles |
| 17 | ASCII box diagrams preserved | `├──` trees inside code blocks |
| 18 | File size reasonable | Should be ~600-800KB total |

---

### Step 13 — Polish & Edge Case Fixes

Common issues to anticipate and fix:

#### 13.1 — Table overflow on mobile
Tables wider than viewport need horizontal scrolling.

```css
.table-wrap {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  margin: 1rem 0;
}
```
The JS `renderStep()` already wraps tables in `.table-wrap` divs.

#### 13.2 — Code block overflow
Long lines in code blocks (especially ASCII diagrams) need horizontal scroll.

```css
pre {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}
```

#### 13.3 — KaTeX dollar-sign false positives
The rawSteps use `$` in non-math contexts (e.g., `$1`, `W$SD` in step 13). The KaTeX auto-render delimiters need to be configured to avoid false matches:

```javascript
renderMathInElement(contentEl, {
  delimiters: [
    { left: "$$", right: "$$", display: true },
    { left: "\\(", right: "\\)", display: false },
    // Deliberately SKIP single $ delimiter to avoid false positives
    // with "$1", "W$SD", etc. Only use $$ for display math.
    // If inline math is needed, switch to \(...\) syntax in source.
  ],
  throwOnError: false,
  ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
});
```

> **Decision:** Skip single-`$` inline math delimiters. The few inline math usages in step 14 (`$M$`, `$\alpha$`, `$V(h)$`) are readable as raw text. If proper rendering is desired later, switch those specific usages to `\(...\)` in the markdown source and re-build.

#### 13.4 — Link safety
All external links get `rel="noopener noreferrer"` (already in renderStep). No user-generated content, but good practice.

#### 13.5 — Content security
The embedded markdown is from local trusted files only. The build script uses `json.dumps` for escaping, preventing any injection through content. No `eval()` is used.

---

### Step 14 — Add Progress Tracking (Optional Enhancement)

Use `localStorage` to remember which step was last viewed:

```javascript
// Save on navigate
localStorage.setItem('lastStep', stepId);

// Restore on load (in init, before navigateTo)
const savedStep = localStorage.getItem('lastStep');
const initialStep = savedStep && STEP_META.find(s => s.id === savedStep)
  ? savedStep
  : STEP_META[0].id;
```

This way, reopening the file on your phone resumes where you left off.

---

### Step 15 — Add Section Jump (In-Step Navigation)

For long steps (600+ lines), add a floating "sections" button that shows H2/H3 headings within the current step:

- Parse the rendered HTML for `<h2>` and `<h3>` elements
- Build a mini table-of-contents dropdown
- Each item scrolls to that heading (`element.scrollIntoView()`)
- Position: fixed button in bottom-right corner (above bottom nav on mobile)

**Implementation:**

```javascript
function buildSectionNav() {
  const headings = document.querySelectorAll('#content h2, #content h3');
  const dropdown = document.getElementById('section-dropdown');
  dropdown.innerHTML = '';
  headings.forEach((h, i) => {
    h.id = h.id || `section-${i}`;
    const item = document.createElement('button');
    item.className = `section-item ${h.tagName === 'H3' ? 'indent' : ''}`;
    item.textContent = h.textContent;
    item.addEventListener('click', () => {
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      toggleSectionNav();
    });
    dropdown.appendChild(item);
  });
}
```

Add corresponding HTML and CSS for the floating button + dropdown.

---

### Step 16 — Final Build & Size Check

```bash
cd interactiveStudy
python3 build.py
ls -lh dist/index.html
```

Expected: ~600–800 KB (592 KB content + ~5–10 KB HTML/CSS/JS scaffold).

If the file size is a concern for sharing:
- **Option A:** gzip before sending (`gzip -k dist/index.html` → ~150 KB)
- **Option B:** Split into 2 files (`index.html` at ~15 KB + `content.js` at ~600 KB) — build.py can have a `--split` flag for this

---

### Step 17 — Sharing Workflow

**To send to another phone/device:**

1. Run `python3 build.py` (regenerates `dist/index.html`)
2. Send `dist/index.html` via:
   - AirDrop / Nearby Share / Bluetooth
   - Messaging app (Telegram, WhatsApp → send as file)
   - USB transfer
   - Email attachment
   - Upload to a private GitHub Gist → open URL on phone
3. Open in any mobile browser (Chrome, Safari, Firefox)
4. **First load requires internet** (for CDN libraries). After that, browser caches them.

**If offline-first is needed:**
- Add `--offline` flag to `build.py` that downloads CDN files and inlines them
- This adds ~400 KB to the file (marked ~40KB, highlight.js ~130KB + theme, KaTeX ~230KB + fonts)
- Total: ~1.0–1.2 MB — still perfectly shareable

---

## 3. File Dependency Graph

```
planning/rawSteps/*.md (15 files)
        │
        ▼
interactiveStudy/build.py  ←── reads ──→  interactiveStudy/src/shell.html
        │                                  interactiveStudy/src/styles.css
        │                                  interactiveStudy/src/app.js
        ▼
interactiveStudy/dist/index.html  (single standalone output)
```

---

## 4. Summary of Commands

```bash
# One-time setup
mkdir -p interactiveStudy/src interactiveStudy/dist

# Development (edit src/ files, then rebuild)
cd interactiveStudy
python3 build.py

# Local preview
python3 -m http.server 8080 -d dist

# After editing rawSteps content, rebuild to pick up changes
python3 build.py

# Share
# → send dist/index.html to target device
```

---

## 5. Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Build tool | Python 3 script | Already installed (3.13.12), zero deps, cross-platform |
| Library loading | CDN (pinned versions) | Keeps dist file small (~700KB vs ~1.1MB). First load needs internet. |
| Markdown parser | marked.js (v15) | Mature, fast, GFM support, small footprint |
| Code highlighting | highlight.js (v11.11) | Universal standard, language auto-detect + explicit |
| Math rendering | KaTeX (v0.16) | Faster than MathJax, smaller, auto-render extension |
| Single `$` math delimiter | Disabled | Too many false positives (`$1`, `W$SD`). Use `$$` only. |
| Sidebar on mobile | Hamburger drawer | Standard mobile pattern, thumb-friendly |
| Sidebar on desktop | Persistent left panel | Steps are always visible, no extra clicks |
| Navigation | Prev/Next + sidebar + hash + keyboard + swipe | Multiple input methods for different contexts |
| Content embedding | JSON.dumps in build script | Safe escaping of backticks, quotes, dollar signs, backslashes |
| Light/dark mode | Light only (initially) | Better for outdoor phone reading; dark toggle can be added later |
| Progress tracking | localStorage last-step | Auto-resumes on reopen — no server needed |
| Offline mode | Optional `--offline` flag | CDN is preferred default; offline available when needed |

---

## 6. Future Enhancements (Not in Initial Scope)

- **Dark mode toggle** — CSS class swap + localStorage preference
- **Search across steps** — JS text search with highlighted results
- **Reading progress bar** — scroll position indicator per step
- **Step completion checkboxes** — localStorage-based "done" tracking per phase
- **cleanSteps viewer** — same viewer, different content source (build.py flag)
- **PDF export** — print styles already handle this partially
- **Offline PWA** — service worker + manifest for install-to-homescreen
