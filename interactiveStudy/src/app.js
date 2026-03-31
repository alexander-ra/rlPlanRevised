/* ===== Step Metadata ===== */
const STEP_META = [
  { id: "step_01", num: 1,  title: "RL Basics",             phase: "A", phaseLabel: "A \u2014 Foundation" },
  { id: "step_02", num: 2,  title: "Game Theory + CFR",     phase: "A", phaseLabel: "A \u2014 Foundation" },
  { id: "step_03", num: 3,  title: "CFR Variants + MC",     phase: "B", phaseLabel: "B \u2014 Scaling" },
  { id: "step_04", num: 4,  title: "Game Abstraction",      phase: "B", phaseLabel: "B \u2014 Scaling" },
  { id: "step_05", num: 5,  title: "Neural Equilibrium",    phase: "C", phaseLabel: "C \u2014 Neural Methods" },
  { id: "step_06", num: 6,  title: "End-to-End Game AI",    phase: "C", phaseLabel: "C \u2014 Neural Methods" },
  { id: "step_07", num: 7,  title: "Opponent Modeling",      phase: "D", phaseLabel: "D \u2014 Opponent Modeling" },
  { id: "step_08", num: 8,  title: "Safe Exploitation",     phase: "D", phaseLabel: "D \u2014 Opponent Modeling" },
  { id: "step_09", num: 9,  title: "Multi-Agent RL",        phase: "E", phaseLabel: "E \u2014 Multi-Agent" },
  { id: "step_10", num: 10, title: "Population Training",   phase: "E", phaseLabel: "E \u2014 Multi-Agent" },
  { id: "step_11", num: 11, title: "Coalition Formation",   phase: "E", phaseLabel: "E \u2014 Multi-Agent" },
  { id: "step_12", num: 12, title: "Sequence Models + LLM", phase: "F", phaseLabel: "F \u2014 Data-Driven" },
  { id: "step_13", num: 13, title: "Behavioral Analysis",   phase: "F", phaseLabel: "F \u2014 Data-Driven" },
  { id: "step_14", num: 14, title: "Evaluation Frameworks", phase: "G", phaseLabel: "G \u2014 Integration" },
  { id: "step_15", num: 15, title: "Research Frontier",     phase: "G", phaseLabel: "G \u2014 Integration" },
];

// STEPS_CONTENT is injected by build.py at <!-- INLINE_CONTENT -->

/* ===== State ===== */
let currentStepIndex = 0;

/* ===== Sidebar Navigation Builder ===== */
function buildNav() {
  const navList = document.getElementById('nav-list');
  let currentPhase = null;

  STEP_META.forEach((step) => {
    if (step.phase !== currentPhase) {
      currentPhase = step.phase;
      const label = document.createElement('div');
      label.className = 'phase-label';
      label.textContent = step.phaseLabel;
      navList.appendChild(label);
    }
    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.step = step.id;
    btn.textContent = step.num + '. ' + step.title;
    btn.addEventListener('click', () => navigateTo(step.id));
    navList.appendChild(btn);
  });
}

function updateActiveNav() {
  const activeId = STEP_META[currentStepIndex].id;
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.step === activeId);
  });
}

/* ===== Markdown Rendering ===== */
function renderStep(stepId) {
  const md = STEPS_CONTENT[stepId];
  if (!md) return;

  // Configure marked
  marked.setOptions({
    gfm: true,
    breaks: false,
  });

  // Parse markdown to HTML
  const html = marked.parse(md);

  // Insert into DOM
  const contentEl = document.getElementById('content');
  contentEl.innerHTML = html;

  // Syntax-highlight code blocks
  contentEl.querySelectorAll('pre code').forEach(block => {
    hljs.highlightElement(block);
  });

  // Render LaTeX math (KaTeX auto-render) — skip single $ to avoid false positives
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(contentEl, {
      delimiters: [
        { left: "$$", right: "$$", display: true },
        { left: "\\(", right: "\\)", display: false },
        { left: "\\[", right: "\\]", display: true },
      ],
      throwOnError: false,
      ignoredTags: ["script", "noscript", "style", "textarea", "pre", "code"]
    });
  }

  // Make external links open in new tab
  contentEl.querySelectorAll('a[href^="http"]').forEach(a => {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });

  // Wrap tables in scrollable container
  contentEl.querySelectorAll('table').forEach(table => {
    if (!table.parentElement.classList.contains('table-wrap')) {
      const wrapper = document.createElement('div');
      wrapper.className = 'table-wrap';
      table.parentNode.insertBefore(wrapper, table);
      wrapper.appendChild(table);
    }
  });

  // Scroll to top
  window.scrollTo(0, 0);

  // Build section jump navigation
  buildSectionNav();
}

/* ===== Navigation Logic ===== */
function navigateTo(stepId) {
  const idx = STEP_META.findIndex(s => s.id === stepId);
  if (idx === -1) return;
  currentStepIndex = idx;

  renderStep(stepId);
  updateActiveNav();

  // Update topbar title
  const meta = STEP_META[idx];
  document.getElementById('topbar-title').textContent =
    'Step ' + meta.num + ': ' + meta.title;

  // Update URL hash
  history.replaceState(null, '', '#' + stepId);

  // Update prev/next button states
  updateNavButtons();

  // Close sidebar if open (mobile)
  closeSidebar();

  // Save to localStorage
  try { localStorage.setItem('lastStep', stepId); } catch(e) {}
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
  document.querySelectorAll('[id^="prev-btn"]').forEach(b => b.disabled = atStart);
  document.querySelectorAll('[id^="next-btn"]').forEach(b => b.disabled = atEnd);
}

/* ===== Section Jump Navigation ===== */
function buildSectionNav() {
  const headings = document.querySelectorAll('#content h2, #content h3');
  const dropdown = document.getElementById('section-dropdown');
  const fab = document.getElementById('section-fab');
  dropdown.innerHTML = '';

  if (headings.length === 0) {
    fab.style.display = 'none';
    return;
  }
  fab.style.display = '';

  headings.forEach((h, i) => {
    if (!h.id) h.id = 'section-' + i;
    const item = document.createElement('button');
    item.className = 'section-item' + (h.tagName === 'H3' ? ' indent' : '');
    item.textContent = h.textContent;
    item.addEventListener('click', () => {
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      closeSectionNav();
    });
    dropdown.appendChild(item);
  });
}

function toggleSectionNav() {
  document.getElementById('section-dropdown').classList.toggle('open');
}

function closeSectionNav() {
  document.getElementById('section-dropdown').classList.remove('open');
}

/* ===== Sidebar Toggle (Mobile) ===== */
function openSidebar() {
  document.getElementById('sidebar').classList.add('open');
  document.getElementById('overlay').classList.add('visible');
  document.body.style.overflow = 'hidden';
}

function closeSidebar() {
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('visible');
  document.body.style.overflow = '';
}

/* ===== Initialization ===== */
document.addEventListener('DOMContentLoaded', () => {
  buildNav();

  // Wire up event listeners
  document.getElementById('hamburger').addEventListener('click', openSidebar);
  document.getElementById('close-sidebar').addEventListener('click', closeSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  document.getElementById('prev-btn').addEventListener('click', goPrev);
  document.getElementById('next-btn').addEventListener('click', goNext);
  document.getElementById('prev-btn-bottom').addEventListener('click', goPrev);
  document.getElementById('next-btn-bottom').addEventListener('click', goNext);

  // Section jump FAB
  document.getElementById('section-fab').addEventListener('click', toggleSectionNav);
  document.addEventListener('click', (e) => {
    const nav = document.getElementById('section-nav');
    if (!nav.contains(e.target)) closeSectionNav();
  });

  // Determine initial step: hash > localStorage > first
  const hash = window.location.hash.replace('#', '');
  let initialStep = STEP_META[0].id;
  if (STEP_META.find(s => s.id === hash)) {
    initialStep = hash;
  } else {
    try {
      const saved = localStorage.getItem('lastStep');
      if (saved && STEP_META.find(s => s.id === saved)) {
        initialStep = saved;
      }
    } catch(e) {}
  }
  navigateTo(initialStep);

  // Browser back/forward
  window.addEventListener('hashchange', () => {
    const h = window.location.hash.replace('#', '');
    if (STEP_META.find(s => s.id === h)) {
      navigateTo(h);
    }
  });
});

/* ===== Keyboard Navigation ===== */
document.addEventListener('keydown', (e) => {
  // Don't intercept if user is typing in an input
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft') { goPrev(); e.preventDefault(); }
  if (e.key === 'ArrowRight') { goNext(); e.preventDefault(); }
  if (e.key === 'Escape') { closeSidebar(); }
});

/* ===== Touch Swipe Navigation ===== */
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
  touchStartY = e.changedTouches[0].screenY;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].screenX - touchStartX;
  const dy = e.changedTouches[0].screenY - touchStartY;
  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 80) {
    if (dx > 0) {
      // Swipe right — edge swipe opens nav, otherwise prev step
      if (touchStartX < 30) { openSidebar(); }
      else { goPrev(); }
    } else {
      goNext();
    }
  }
}, { passive: true });
