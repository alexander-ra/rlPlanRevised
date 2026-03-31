# Interactive Study Viewer

A standalone, mobile-friendly HTML viewer for the 15 RL study plan raw steps.

## Build

```bash
python3 build.py
```

Produces `dist/index.html` (~638 KB) — a single self-contained file with all CSS, JS, and markdown content inlined. No server required; works via `file://` on desktop or mobile.

## Source Structure

```
src/
  shell.html   — HTML skeleton with CDN links (marked.js, highlight.js, KaTeX)
  styles.css   — All styles (responsive, mobile-first)
  app.js       — Navigation, rendering, timeline, all interactive features
build.py       — Build script that inlines everything into one HTML file
inject_intros.py — One-shot script that added study plan intro text to rawSteps
```

## Features

- **Step navigation**: sidebar (collapsible on mobile), prev/next buttons, keyboard arrows, swipe gestures
- **Timeline bar**: per-day cells below the header showing the current step's date window with weekend highlighting
- **Section jump**: floating button to jump to any heading within the current step
- **YouTube thumbnails**: YouTube links are replaced with clickable thumbnail previews
- **Checkbox persistence**: checkbox state saved to localStorage per step
- **Schedule delay**: sidebar control to shift the plan start date forward by N days (reflected in timeline)
- **Math & code**: KaTeX for LaTeX equations, highlight.js for code blocks

## Content Source

The viewer reads markdown from `planning/rawSteps/step_01_*.md` through `step_15_*.md`. Each file has a blockquote intro injected by `inject_intros.py` with phase overview and contribution alignment text from `deliverables/studyPlan/en/`.
