/* ===== Step Metadata ===== */
const STEP_META = [
  { id: "step_01", num: 1,  title: "RL Basics",             phase: "A", phaseLabel: "A \u2014 Foundation",         days: 14 },
  { id: "step_02", num: 2,  title: "Game Theory + CFR",     phase: "A", phaseLabel: "A \u2014 Foundation",         days: 14 },
  { id: "step_03", num: 3,  title: "CFR Variants + MC",     phase: "B", phaseLabel: "B \u2014 Scaling",            days: 10 },
  { id: "step_04", num: 4,  title: "Game Abstraction",      phase: "B", phaseLabel: "B \u2014 Scaling",            days: 10 },
  { id: "step_05", num: 5,  title: "Neural Equilibrium",    phase: "C", phaseLabel: "C \u2014 Neural Methods",     days: 11 },
  { id: "step_06", num: 6,  title: "End-to-End Game AI",    phase: "C", phaseLabel: "C \u2014 Neural Methods",     days: 21 },
  { id: "step_07", num: 7,  title: "Opponent Modeling",      phase: "D", phaseLabel: "D \u2014 Opponent Modeling", days: 21 },
  { id: "step_08", num: 8,  title: "Safe Exploitation",     phase: "D", phaseLabel: "D \u2014 Opponent Modeling", days: 21 },
  { id: "step_09", num: 9,  title: "Multi-Agent RL",        phase: "E", phaseLabel: "E \u2014 Multi-Agent",       days: 14 },
  { id: "step_10", num: 10, title: "Population Training",   phase: "E", phaseLabel: "E \u2014 Multi-Agent",       days: 14 },
  { id: "step_11", num: 11, title: "Coalition Formation",   phase: "E", phaseLabel: "E \u2014 Multi-Agent",       days: 14 },
  { id: "step_12", num: 12, title: "Sequence Models + LLM", phase: "F", phaseLabel: "F \u2014 Data-Driven",       days: 10 },
  { id: "step_13", num: 13, title: "Behavioral Analysis",   phase: "F", phaseLabel: "F \u2014 Data-Driven",       days: 14 },
  { id: "step_14", num: 14, title: "Evaluation Frameworks", phase: "G", phaseLabel: "G \u2014 Integration",       days: 14 },
  { id: "step_15", num: 15, title: "Research Frontier",     phase: "G", phaseLabel: "G \u2014 Integration",       days: 10 },
];

const PLAN_START = new Date(2026, 1, 16); // Feb 16 2026
const BASE_TOTAL_DAYS = STEP_META.reduce((s, m) => s + m.days, 0); // 211

// STEPS_CONTENT is injected by build.py via the content placeholder

/* ===== State ===== */
let currentStepIndex = 0;
let scheduleAdjust = 0; // days to delay plan start (shifts all dates forward)

/* ===== Schedule Computation ===== */
const DAY_NAMES = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

function addDays(d, n) {
  const r = new Date(d);
  r.setDate(r.getDate() + n);
  return r;
}

function getStepDateRange(stepIndex) {
  const planStart = addDays(PLAN_START, scheduleAdjust);
  let offset = 0;
  for (let i = 0; i < stepIndex; i++) offset += STEP_META[i].days;
  const start = addDays(planStart, offset);
  const end = addDays(planStart, offset + STEP_META[stepIndex].days - 1);
  return { start, end, days: STEP_META[stepIndex].days };
}

function formatDayShort(d) {
  return d.getDate() + ' ' + MONTH_NAMES[d.getMonth()];
}

function getMaxAdjust() {
  // Plan must end by Oct 31 2026
  const deadline = new Date(2026, 9, 31); // Oct 31
  const planEndBase = addDays(PLAN_START, BASE_TOTAL_DAYS - 1);
  return Math.floor((deadline - planEndBase) / 86400000);
}

/* ===== Timeline Bar ===== */
function renderTimeline() {
  const bar = document.getElementById('timeline-bar');
  if (!bar) return;

  const range = getStepDateRange(currentStepIndex);
  const windowBefore = 7;
  const windowAfter = 7;
  const windowStart = addDays(range.start, -windowBefore);
  const windowEnd = addDays(range.end, windowAfter);
  const totalWindowDays = Math.round((windowEnd - windowStart) / 86400000) + 1;

  const today = new Date();
  today.setHours(0,0,0,0);

  const stepStartStr = range.start.toDateString();
  const stepEndStr = range.end.toDateString();

  // Build day cells — one per day in the window
  let cells = '';
  for (let i = 0; i < totalWindowDays; i++) {
    const d = addDays(windowStart, i);
    const ds = d.toDateString();
    const dow = d.getDay(); // 0=Sun, 6=Sat
    const isWeekend = dow === 0 || dow === 6;
    const isInStep = d >= range.start && d <= range.end;
    const isToday = ds === today.toDateString();
    const isStepBound = ds === stepStartStr || ds === stepEndStr;
    const isMonday = dow === 1;
    const is1st = d.getDate() === 1;

let cls = 'tl-cell';
    if (isInStep) cls += ' in-step';
    if (isWeekend && isInStep) cls += ' wknd-active';
    if (isWeekend && !isInStep) cls += ' wknd';
    if (isToday) cls += ' today';
    if (isStepBound) cls += ' bound';

    // Show label on: step boundaries, every Monday, 1st of month, and Today
    const showLabel = isStepBound || isMonday || is1st || isToday;
    const label = showLabel
      ? (isToday 
          ? `<span class="tl-label" style="color: #ea580c; font-weight: bold; font-size: 0.65rem; z-index: 10;">Today<br>${d.getDate()}</span>`
          : `<span class="tl-label">${d.getDate()}<br>${DAY_NAMES[dow]}</span>`)
      : '';
    // Thin tick for every day; taller for labelled days
    const tickCls = showLabel ? 'tl-tick tall' : 'tl-tick';

    cells += `<div class="${cls}"><div class="${tickCls}"></div>${label}</div>`;
  }

  bar.innerHTML =
    `<div class="tl-row">${cells}</div>` +
    `<div class="timeline-label">${formatDayShort(range.start)} \u2013 ${formatDayShort(range.end)} \u00b7 ${range.days}d</div>`;
}

/* ===== YouTube Thumbnails ===== */
function embedYouTubeThumbnails() {
  const contentEl = document.getElementById('content');
  // Match YouTube links: youtube.com/watch?v=ID or youtu.be/ID
  contentEl.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    let videoId = null;
    try {
      const url = new URL(href);
      if (url.hostname.includes('youtube.com') && url.searchParams.get('v')) {
        videoId = url.searchParams.get('v');
      } else if (url.hostname === 'youtu.be') {
        videoId = url.pathname.slice(1);
      }
    } catch(e) {}
    if (!videoId) return;

    // Don't wrap if already wrapped
    if (a.parentElement.classList.contains('yt-thumb-wrap')) return;

    // Create thumbnail block
    const wrapper = document.createElement('div');
    wrapper.className = 'yt-thumb-wrap';
    const img = document.createElement('img');
    img.src = `https://img.youtube.com/vi/${encodeURIComponent(videoId)}/mqdefault.jpg`;
    img.alt = a.textContent;
    img.className = 'yt-thumb';
    img.loading = 'lazy';
    const overlay = document.createElement('span');
    overlay.className = 'yt-play';
    overlay.textContent = '\u25B6';

    const link = document.createElement('a');
    link.href = href;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'yt-thumb-link';
    link.appendChild(img);
    link.appendChild(overlay);

    wrapper.appendChild(link);
    // Keep the original text link below
    const textLink = a.cloneNode(true);
    textLink.target = '_blank';
    textLink.rel = 'noopener noreferrer';

    a.parentNode.insertBefore(wrapper, a);
    // Original link stays as-is
  });
}

/* ===== Checkbox Persistence ===== */
function setupCheckboxes() {
  const contentEl = document.getElementById('content');
  const stepId = STEP_META[currentStepIndex].id;
  const checkboxes = contentEl.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((cb, idx) => {
    cb.disabled = false;          // marked.js adds disabled by default
    cb.removeAttribute('disabled');
    const key = `cb_${stepId}_${idx}`;
    // Restore state
    try {
      const saved = localStorage.getItem(key);
      if (saved === '1') cb.checked = true;
      else if (saved === '0') cb.checked = false;
    } catch(e) {}
    // Save on change
    cb.addEventListener('change', () => {
      try { localStorage.setItem(key, cb.checked ? '1' : '0'); } catch(e) {}
    });
  });
}

/* ===== Schedule Adjustment ===== */
function initScheduleAdjust() {
  try {
    const saved = localStorage.getItem('scheduleAdjust');
    if (saved !== null) scheduleAdjust = parseInt(saved, 10) || 0;
  } catch(e) {}
  updateScheduleUI();
}

function adjustSchedule(delta) {
  const maxAdj = getMaxAdjust();
  const newVal = scheduleAdjust + delta;
  if (newVal < 0 || newVal > maxAdj) return;
  scheduleAdjust = newVal;
  try { localStorage.setItem('scheduleAdjust', String(scheduleAdjust)); } catch(e) {}
  updateScheduleUI();
  renderTimeline();
}

function updateScheduleUI() {
  const maxAdj = getMaxAdjust();
  const el = document.getElementById('sched-value');
  if (el) el.textContent = `${scheduleAdjust}/${maxAdj}`;
  const minusBtn = document.getElementById('sched-minus');
  const plusBtn = document.getElementById('sched-plus');
  if (minusBtn) minusBtn.disabled = scheduleAdjust <= 0;
  if (plusBtn) plusBtn.disabled = scheduleAdjust >= maxAdj;
}

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

  
  // Set IDs for headers so anchors work
  contentEl.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
    if (!h.id) {
      let anchor = h.textContent.toLowerCase()
                    .replace(/[^\w\s-]/g, '')
                    .replace(/\s+/g, '-')
                    .replace(/-+/g, '-');
      h.id = anchor;
    }
  });

  // Smooth scroll for internal links
  contentEl.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const targetEl = document.getElementById(targetId);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Make Table of Contents collapsable
  const tocHeader = Array.from(contentEl.querySelectorAll('h2')).find(h => h.textContent.trim() === 'Table of Contents');
  if (tocHeader) {
    tocHeader.style.cursor = 'pointer';
    tocHeader.style.userSelect = 'none';
    tocHeader.innerHTML = '&#9654; Table of Contents'; // Right pointing triangle
    
    // The ul is exactly the next element sibling
    const tocList = tocHeader.nextElementSibling;
    if (tocList && tocList.tagName.toLowerCase() === 'ul') {
      tocList.style.display = 'none'; // Collapsed by default
      
      tocHeader.addEventListener('click', () => {
        if (tocList.style.display === 'none') {
          tocList.style.display = 'block';
          tocHeader.innerHTML = '&#9660; Table of Contents'; // Down pointing triangle
        } else {
          tocList.style.display = 'none';
          tocHeader.innerHTML = '&#9654; Table of Contents';
        }
      });
    }
  }

  // Make external links open in new tab
  contentEl.querySelectorAll('a[href^="http"]').forEach(a => {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });

  
  // Replace missing interactive checkboxes setup since we removed it by accident earlier maybe? We'll put it later.
  // Add intersection observer to track which section we're in
  if (window.__sectionObserver) {
    window.__sectionObserver.disconnect();
  }
  
  const headers = Array.from(document.querySelectorAll('#content h1, #content h2'));
  const observer = new IntersectionObserver((entries) => {
    // Determine current active header based on scroll position
    const visibleHeaders = headers.filter(h => {
       const rect = h.getBoundingClientRect();
       return rect.top <= window.innerHeight * 0.4 && rect.bottom >= -window.innerHeight;
    });
    
    if(visibleHeaders.length > 0) {
      // get the last one that passed the threshold
      const h = visibleHeaders[visibleHeaders.length - 1];
      let txt = h.textContent.replace('▶', '').replace('▼', '').replace('Table of Contents', 'Overview').trim();
      
      let titleEl = document.getElementById('topbar-title');
      let stepMeta = window.STEP_META[window.currentStepIndex];
      titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title} <span class="sub-header" style="opacity:0.6;font-size:0.8em;margin-left:10px;cursor:pointer;" onclick="window.scrollTo({top:0,behavior:'smooth'})">❯ ${txt} <span style="font-size:0.8em;">▲</span></span>`;
    } else if (window.scrollY < 100) {
      let titleEl = document.getElementById('topbar-title');
      let stepMeta = window.STEP_META[window.currentStepIndex];
      titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title}`;
    }
  }, { rootMargin: '-10px 0px -80% 0px', threshold: [0, 1] });

  headers.forEach(h => observer.observe(h));
  window.__sectionObserver = observer;


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

  // YouTube thumbnails
  embedYouTubeThumbnails();

  // Checkbox persistence
  setupCheckboxes();
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
  document.getElementById('topbar-title').innerHTML = 'Step ' + meta.num + ': ' + meta.title;

  // Update URL hash
  history.replaceState(null, '', '#' + stepId);

  // Update prev/next button states
  updateNavButtons();

  // Update timeline
  renderTimeline();

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

  // Schedule adjustment
  initScheduleAdjust();
  document.getElementById('sched-minus').addEventListener('click', () => adjustSchedule(-1));
  document.getElementById('sched-plus').addEventListener('click', () => adjustSchedule(1));

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
