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

const PLAN_START = new Date(2026, 2, 9); // March 8, 2026 (0-based month)
const BASE_TOTAL_DAYS = STEP_META.reduce((s, m) => s + m.days, 0); // 232

/* ===== Report Availability (stepId → reports folder name) ===== */
const STEP_REPORTS = { step_01: 'step01', step_02: 'step02' };
const REPORT_BASE_URL = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/reports';

// STEPS_CONTENT is injected by build.py via the content placeholder

/* ===== State ===== */
let currentStepIndex = 0;
let scheduleAdjust = 0; // days to delay plan start (shifts all dates forward)
let isHomepage = false;
let calendarMonth = new Date().getMonth();
let calendarYear = new Date().getFullYear();

/* ===== JSONBin.io Cloud Storage ===== */
const JSONBIN_API_KEY = '$2a$10$k1FLc/sztnYxUeK/9hzPROI8cAJxmQJHZX1CDs.YZbIJL.l2Wi6d6';
const JSONBIN_API_URL = 'https://api.jsonbin.io/v3/b';
// Set this once after the first bin is created — all devices share this ID
const JSONBIN_BIN_ID = '69d2c3e1aaba882197c967a7';
const JSONBIN_BIN_KEY = 'rlstudy_bin_id';
let cloudData = { checkboxes: {}, scheduleAdjust: 0 };
let binId = null;
let syncTimeout = null;

async function initCloudStorage() {
  // 1) Use hardcoded bin ID if available (cross-device)
  const targetId = JSONBIN_BIN_ID || (() => {
    try { return localStorage.getItem(JSONBIN_BIN_KEY); } catch(e) { return null; }
  })();

  if (targetId) {
    try {
      const res = await fetch(`${JSONBIN_API_URL}/${targetId}/latest`, {
        headers: { 'X-Master-Key': JSONBIN_API_KEY }
      });
      if (res.ok) {
        const json = await res.json();
        cloudData = json.record || cloudData;
        binId = targetId;
        try { localStorage.setItem(JSONBIN_BIN_KEY, binId); } catch(e) {}
        return cloudData;
      }
    } catch(e) { console.warn('Cloud load failed:', e); }
    // If hardcoded ID failed, don't fall through — it's a config error
    if (JSONBIN_BIN_ID) {
      console.error('Hardcoded JSONBIN_BIN_ID is invalid:', JSONBIN_BIN_ID);
      return cloudData;
    }
    // Cached localStorage ID invalid — clear and create new
    try { localStorage.removeItem(JSONBIN_BIN_KEY); } catch(e) {}
  }

  // 2) No bin ID known — create a new bin
  try {
    const res = await fetch(JSONBIN_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Master-Key': JSONBIN_API_KEY,
        'X-Bin-Name': 'rl-study-progress'
      },
      body: JSON.stringify(cloudData)
    });
    if (res.ok) {
      const json = await res.json();
      binId = json.metadata.id;
      try { localStorage.setItem(JSONBIN_BIN_KEY, binId); } catch(e) {}
      // Show the bin ID so the user can hardcode it for cross-device sync
      console.info('%c[RL Study] New bin created. Set JSONBIN_BIN_ID to: ' + binId,
        'color: #f97316; font-weight: bold; font-size: 14px;');
      showBinIdBanner(binId);
    }
  } catch(e) { console.warn('Cloud create failed:', e); }

  return cloudData;
}

function showBinIdBanner(id) {
  const banner = document.createElement('div');
  banner.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:9999;background:#f97316;color:#fff;padding:10px 16px;font-size:13px;font-family:monospace;text-align:center;cursor:pointer;';
  banner.innerHTML = `New cloud bin created. To sync across devices, set <b>JSONBIN_BIN_ID = '${id}'</b> in app.js then rebuild. <span style="text-decoration:underline">Click to copy & dismiss.</span>`;
  banner.addEventListener('click', () => {
    navigator.clipboard.writeText(id).catch(() => {});
    banner.remove();
  });
  document.body.prepend(banner);
}

function syncToCloud() {
  if (!binId) return;
  clearTimeout(syncTimeout);
  syncTimeout = setTimeout(async () => {
    try {
      await fetch(`${JSONBIN_API_URL}/${binId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-Master-Key': JSONBIN_API_KEY },
        body: JSON.stringify(cloudData)
      });
    } catch(e) { console.warn('Cloud sync failed:', e); }
  }, 1000);
}

/* ===== Phase Colors (read from CSS vars for theme support) ===== */
function getPhaseColors(phase) {
  const s = getComputedStyle(document.documentElement);
  const p = phase.toLowerCase();
  return {
    bg: s.getPropertyValue(`--phase-${p}-bg`).trim(),
    border: s.getPropertyValue(`--phase-${p}-border`).trim(),
    text: s.getPropertyValue(`--phase-${p}-text`).trim(),
  };
}

/* ===== Theme Toggle ===== */
function initTheme() {
  let theme;
  try { theme = localStorage.getItem('theme'); } catch(e) {}
  if (!theme) {
    theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  applyTheme(theme);
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  try { localStorage.setItem('theme', theme); } catch(e) {}
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  if (isHomepage) navigateHome(); // re-render to pick up new CSS vars
}

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
  if (!bar || isHomepage) return;

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

    // Don't rewrap if already a card
    if (a.classList.contains('yt-card')) return;

    const title = a.textContent.trim();

    // Build card — the whole card is the link
    const card = document.createElement('a');
    card.href = href;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.className = 'yt-card';
    card.setAttribute('aria-label', title);

    const thumbWrap = document.createElement('div');
    thumbWrap.className = 'yt-thumb-wrap';

    const img = document.createElement('img');
    img.src = `https://img.youtube.com/vi/${encodeURIComponent(videoId)}/mqdefault.jpg`;
    img.alt = title;
    img.className = 'yt-thumb';
    img.loading = 'lazy';

    const play = document.createElement('span');
    play.className = 'yt-play';
    play.setAttribute('aria-hidden', 'true');
    play.textContent = '\u25B6';

    thumbWrap.appendChild(img);
    thumbWrap.appendChild(play);

    const label = document.createElement('div');
    label.className = 'yt-title';
    label.textContent = title;

    card.appendChild(thumbWrap);
    card.appendChild(label);

    // Replace the original anchor entirely
    a.parentNode.replaceChild(card, a);
  });
}

/* ===== Checkpoint Progress Counting ===== */
function getStepCheckboxCounts(stepId) {
  const md = typeof STEPS_CONTENT !== 'undefined' ? STEPS_CONTENT[stepId] : null;
  if (!md) return { total: 0, checked: 0 };
  const allMatches = md.match(/- \[[ x]\]/g);
  const total = allMatches ? allMatches.length : 0;
  let checked = 0;
  for (let i = 0; i < total; i++) {
    if (cloudData.checkboxes[`cb_${stepId}_${i}`] === '1') checked++;
  }
  return { total, checked };
}

/* ===== Checkbox Persistence (Cloud) ===== */
function setupCheckboxes() {
  const contentEl = document.getElementById('content');
  const stepId = STEP_META[currentStepIndex].id;
  const checkboxes = contentEl.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach((cb, idx) => {
    cb.disabled = false;
    cb.removeAttribute('disabled');
    const key = `cb_${stepId}_${idx}`;
    const saved = cloudData.checkboxes[key];
    if (saved === '1') cb.checked = true;
    else if (saved === '0') cb.checked = false;
    cb.addEventListener('change', () => {
      cloudData.checkboxes[key] = cb.checked ? '1' : '0';
      syncToCloud();
      updateNavProgress(stepId);
    });
  });
}

/* ===== Schedule Adjustment ===== */
function initScheduleAdjust() {
  scheduleAdjust = cloudData.scheduleAdjust || 0;
  updateScheduleUI();
}

function adjustSchedule(delta) {
  const maxAdj = getMaxAdjust();
  const newVal = scheduleAdjust + delta;
  if (newVal < 0 || newVal > maxAdj) return;
  scheduleAdjust = newVal;
  cloudData.scheduleAdjust = scheduleAdjust;
  syncToCloud();
  updateScheduleUI();
  if (isHomepage) navigateHome();
  else renderTimeline();
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

  // Home button
  const homeBtn = document.createElement('button');
  homeBtn.className = 'nav-item nav-home';
  homeBtn.dataset.step = 'home';
  homeBtn.textContent = '\u2302 Overview';
  homeBtn.addEventListener('click', () => navigateHome());
  navList.appendChild(homeBtn);

  let currentPhase = null;

  STEP_META.forEach((step) => {
    if (step.phase !== currentPhase) {
      currentPhase = step.phase;
      const label = document.createElement('div');
      label.className = 'phase-label';
      label.textContent = step.phaseLabel;
      navList.appendChild(label);
    }

    const wrapper = document.createElement('div');
    wrapper.className = 'nav-item-wrap';

    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.step = step.id;
    const hasReport = !!STEP_REPORTS[step.id];
    btn.innerHTML = step.num + '. ' + step.title + (hasReport ? ' <span class="report-badge" title="Report available">\uD83D\uDCC4</span>' : '');
    btn.addEventListener('click', () => navigateTo(step.id));
    wrapper.appendChild(btn);

    // Thin progress bar
    const progress = getStepCheckboxCounts(step.id);
    const pct = progress.total > 0 ? Math.round((progress.checked / progress.total) * 100) : 0;
    const c = getPhaseColors(step.phase);
    const bar = document.createElement('div');
    bar.className = 'nav-progress';
    bar.id = `nav-progress-${step.id}`;
    if (progress.total > 0) {
      bar.innerHTML = `<div class="nav-progress-fill" style="width:${pct}%;background:${c.border}"></div>`;
    }
    wrapper.appendChild(bar);

    navList.appendChild(wrapper);
  });
}

function updateNavProgress(stepId) {
  const bar = document.getElementById(`nav-progress-${stepId}`);
  if (!bar) return;
  const progress = getStepCheckboxCounts(stepId);
  if (progress.total > 0) {
    const pct = Math.round((progress.checked / progress.total) * 100);
    const step = STEP_META.find(s => s.id === stepId);
    const c = getPhaseColors(step.phase);
    bar.innerHTML = `<div class="nav-progress-fill" style="width:${pct}%;background:${c.border}"></div>`;
  }
}

function updateActiveNav() {
  const activeId = isHomepage ? 'home' : STEP_META[currentStepIndex].id;
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

  // Report download bar
  const reportFolder = STEP_REPORTS[stepId];
  if (reportFolder) {
    const bar = document.createElement('div');
    bar.className = 'report-bar';
    bar.innerHTML = `<span class="report-bar-label">\uD83D\uDCC4 Report available</span>
      <a href="${REPORT_BASE_URL}/${reportFolder}/report_en.pdf" target="_blank" rel="noopener noreferrer" class="report-btn">EN \u2193</a>
      <a href="${REPORT_BASE_URL}/${reportFolder}/report_bg.pdf" target="_blank" rel="noopener noreferrer" class="report-btn">BG \u2193</a>`;
    contentEl.insertBefore(bar, contentEl.firstChild);
  }

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

  // Add intersection observer to track which section we're in
  if (window.__sectionObserver) {
    window.__sectionObserver.disconnect();
  }
  
  // Skip observer setup if on homepage (currentStepIndex is -1)
  if (isHomepage || currentStepIndex < 0) {
    return;
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
      if (!stepMeta) return;
      titleEl.innerHTML = `Step ${stepMeta.num}: ${stepMeta.title} <span class="sub-header" style="opacity:0.6;font-size:0.8em;margin-left:10px;cursor:pointer;" onclick="window.scrollTo({top:0,behavior:'smooth'})">❯ ${txt} <span style="font-size:0.8em;">▲</span></span>`;
    } else if (window.scrollY < 100) {
      let titleEl = document.getElementById('topbar-title');
      let stepMeta = window.STEP_META[window.currentStepIndex];
      if (!stepMeta) return;
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
  if (stepId === 'home') { navigateHome(); return; }

  isHomepage = false;
  document.getElementById('timeline-bar').style.display = '';
  document.getElementById('section-nav').style.display = '';

  const idx = STEP_META.findIndex(s => s.id === stepId);
  if (idx === -1) return;
  currentStepIndex = idx;

  renderStep(stepId);
  updateActiveNav();

  const meta = STEP_META[idx];
  document.getElementById('topbar-title').innerHTML = 'Step ' + meta.num + ': ' + meta.title;

  history.replaceState(null, '', '#' + stepId);
  updateNavButtons();
  renderTimeline();
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
  const atStart = isHomepage || currentStepIndex <= 0;
  const atEnd = isHomepage || currentStepIndex === STEP_META.length - 1;
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
document.addEventListener('DOMContentLoaded', async () => {
  initTheme();
  await initCloudStorage();
  buildNav();

  document.getElementById('hamburger').addEventListener('click', openSidebar);
  document.getElementById('close-sidebar').addEventListener('click', closeSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  document.getElementById('prev-btn').addEventListener('click', goPrev);
  document.getElementById('next-btn').addEventListener('click', goNext);
  document.getElementById('prev-btn-bottom').addEventListener('click', goPrev);
  document.getElementById('next-btn-bottom').addEventListener('click', goNext);

  document.getElementById('section-fab').addEventListener('click', toggleSectionNav);
  document.addEventListener('click', (e) => {
    const nav = document.getElementById('section-nav');
    if (!nav.contains(e.target)) closeSectionNav();
  });

  initScheduleAdjust();
  document.getElementById('sched-minus').addEventListener('click', () => adjustSchedule(-1));
  document.getElementById('sched-plus').addEventListener('click', () => adjustSchedule(1));
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);

  // Determine initial view: hash > homepage
  const hash = window.location.hash.replace('#', '');
  if (hash && hash !== 'home' && STEP_META.find(s => s.id === hash)) {
    navigateTo(hash);
  } else {
    navigateHome();
  }

  window.addEventListener('hashchange', () => {
    const h = window.location.hash.replace('#', '');
    if (h === 'home' || h === '') { navigateHome(); }
    else if (STEP_META.find(s => s.id === h)) { navigateTo(h); }
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

/* ===== Homepage ===== */
function getStepStatus(stepIndex) {
  const today = new Date(); today.setHours(0,0,0,0);
  const range = getStepDateRange(stepIndex);
  if (today > range.end) return 'done';
  if (today >= range.start) return 'active';
  return 'upcoming';
}

function getStepTier(num) {
  if ([6,7,8].includes(num)) return 'T1';
  if ([12,15].includes(num)) return 'T3';
  return 'T2';
}

function extractStepSummary(stepId) {
  const md = typeof STEPS_CONTENT !== 'undefined' ? STEPS_CONTENT[stepId] : null;
  if (!md) return '';
  const lines = md.split('\n');
  for (const target of ['Contribution Alignment:', 'Phase Overview:']) {
    let result = '', capturing = false;
    for (const line of lines) {
      if (line.includes(`**${target}**`) || line.includes(`**${target}`)) {
        result = line.replace(/^>\s*/, '').replace(/\*\*/g, '');
        capturing = true; continue;
      }
      if (capturing) {
        if (line.startsWith('>')) { result += ' ' + line.replace(/^>\s*/, '').replace(/\*\*/g, ''); }
        else break;
      }
    }
    if (result.trim()) return result.trim();
  }
  return '';
}

function buildGanttCalendar() {
  return buildCalendar();
}

function changeCalMonth(delta) {
  calendarMonth += delta;
  if (calendarMonth > 11) { calendarMonth = 0; calendarYear++; }
  if (calendarMonth < 0) { calendarMonth = 11; calendarYear--; }
  const planStart = addDays(PLAN_START, scheduleAdjust);
  const minM = planStart.getMonth(), minY = planStart.getFullYear();
  if (calendarYear < minY || (calendarYear === minY && calendarMonth < minM)) { calendarYear = minY; calendarMonth = minM; }
  if (calendarYear > 2026 || (calendarYear === 2026 && calendarMonth > 9)) { calendarYear = 2026; calendarMonth = 9; }
  if (isHomepage) navigateHome();
}
window.changeCalMonth = changeCalMonth;

function buildCalendar() {
  const planStart = addDays(PLAN_START, scheduleAdjust);
  const minM = planStart.getMonth(), minY = planStart.getFullYear();
  const atMin = calendarYear === minY && calendarMonth === minM;
  const atMax = calendarYear === 2026 && calendarMonth === 9;

  const header = `<div class="cal-header">
    <button class="cal-nav-btn${atMin ? ' disabled' : ''}" onclick="changeCalMonth(-1)" aria-label="Previous month" ${atMin ? 'disabled' : ''}>\u2039</button>
    <span class="cal-month-label">${MONTH_NAMES[calendarMonth]} ${calendarYear}</span>
    <button class="cal-nav-btn${atMax ? ' disabled' : ''}" onclick="changeCalMonth(1)" aria-label="Next month" ${atMax ? 'disabled' : ''}>\u203A</button>
  </div>`;

  const grid = buildCalendarMonth(calendarYear, calendarMonth);
  const legend = buildCalendarLegend();
  return `<div class="cal-wrap">${header}${grid}${legend}</div>`;
}

function buildCalendarMonth(year, month) {
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  let startDow = new Date(year, month, 1).getDay() - 1; // Mon=0..Sun=6
  if (startDow < 0) startDow = 6;

  const today = new Date(); today.setHours(0,0,0,0);

  // Precompute step index for each day
  const stepForDay = [];
  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    let found = -1;
    for (let i = 0; i < STEP_META.length; i++) {
      const r = getStepDateRange(i);
      if (date >= r.start && date <= r.end) { found = i; break; }
    }
    stepForDay.push(found);
  }

  const dayHeaders = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    .map(d => `<div class="cal-dh">${d}</div>`).join('');

  let cells = '';
  for (let i = 0; i < startDow; i++) cells += `<div class="cal-cell empty"></div>`;

  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    const isToday = date.toDateString() === today.toDateString();
    const dow = date.getDay();
    const isWeekend = dow === 0 || dow === 6;
    const si = stepForDay[d - 1];

    let cls = 'cal-cell';
    let style = '';
    let onclick = '';
    let title = '';

    if (isToday) cls += ' today';
    if (isWeekend) cls += ' weekend';

    if (si >= 0) {
      cls += ' has-step';
      const c = getPhaseColors(STEP_META[si].phase);
      style = `background:${c.bg};border-color:${c.border};`;
      onclick = `onclick="navigateTo('${STEP_META[si].id}')"`;
      title = `title="Step ${STEP_META[si].num}: ${STEP_META[si].title}"`;

      // Continuity classes for multi-day bar effect within a row
      const gridPos = startDow + d - 1;
      const isFirstCol = gridPos % 7 === 0;
      const isLastCol = gridPos % 7 === 6;
      if (!isFirstCol && d > 1 && stepForDay[d - 2] === si) cls += ' cont-l';
      if (!isLastCol && d < daysInMonth && stepForDay[d] === si) cls += ' cont-r';
    }

    cells += `<div class="${cls}" style="${style}" ${onclick} ${title}><span class="cal-date">${d}</span></div>`;
  }

  return `<div class="cal-grid"><div class="cal-hdr-row">${dayHeaders}</div><div class="cal-body">${cells}</div></div>`;
}

function buildCalendarLegend() {
  const seen = new Set();
  let items = '';
  STEP_META.forEach(s => {
    if (seen.has(s.phase)) return;
    seen.add(s.phase);
    const c = getPhaseColors(s.phase);
    items += `<span class="cal-legend-item"><span class="cal-legend-dot" style="background:${c.bg};border:2px solid ${c.border}"></span>${s.phaseLabel}</span>`;
  });
  return `<div class="cal-legend">${items}</div>`;
}

function buildStepSummaries() {
  let html = '';
  STEP_META.forEach((step, i) => {
    const rng = getStepDateRange(i);
    const st = getStepStatus(i);
    const c = getPhaseColors(step.phase);
    const tier = getStepTier(step.num);
    const summary = extractStepSummary(step.id);
    const icon = st === 'done' ? '&#x2705;' : st === 'active' ? '&#x1F535;' : '&#x2B1C;';
    const hasReport = !!STEP_REPORTS[step.id];
    const reportBadge = hasReport ? '<span class="sc-report-badge" title="Report available">\uD83D\uDCC4</span>' : '';
    const progress = getStepCheckboxCounts(step.id);
    const progressPct = progress.total > 0 ? Math.round((progress.checked / progress.total) * 100) : 0;
    const progressHtml = progress.total > 0
      ? `<div class="sc-progress"><div class="sc-progress-bar"><div class="sc-progress-fill" style="width:${progressPct}%;background:${c.border}"></div></div><span class="sc-progress-text">${progress.checked}/${progress.total}</span></div>`
      : '';
    html += `<div class="sc" onclick="navigateTo('${step.id}')" style="border-left:4px solid ${c.border}">
      <div class="sc-top"><span class="sc-num">${icon} Step ${step.num}</span><span class="sc-badges">${reportBadge}<span class="sc-phase" style="background:${c.bg};color:${c.text}">${step.phaseLabel}</span></span></div>
      <div class="sc-title">${step.title}</div>
      <div class="sc-meta"><span>${formatDayShort(rng.start)} \u2013 ${formatDayShort(rng.end)}</span><span>${step.days}d \u00b7 ${tier}</span></div>
      ${progressHtml}
      ${summary ? `<div class="sc-desc">${summary}</div>` : ''}
    </div>`;
  });
  return html;
}

function navigateHome() {
  isHomepage = true;
  currentStepIndex = -1;
  document.getElementById('topbar-title').textContent = 'RL Study Plan';
  document.getElementById('timeline-bar').style.display = 'none';
  document.getElementById('section-nav').style.display = 'none';
  updateNavButtons();
  updateActiveNav();
  history.replaceState(null, '', '#home');

  document.getElementById('content').innerHTML =
    `<div class="hp">
      <div class="hp-hdr"><h1>PhD Research Plan</h1>
        <p>AI in Computer Games &mdash; Adaptive Strategy in Multi-Agent Imperfect-Information Environments</p>
        <p class="hp-meta">15 steps &middot; 7 phases &middot; ${BASE_TOTAL_DAYS} days &middot; Mar&ndash;Oct 2026</p>
      </div>
      <h2 class="hp-sec">Timeline</h2>
      ${buildGanttCalendar()}
      <h2 class="hp-sec">Steps</h2>
      <div class="sc-list">${buildStepSummaries()}</div>
    </div>`;
  window.scrollTo(0, 0);
  closeSidebar();
}
