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

/* ===== Per-Phase Checkpoint Texts (7.5) ===== */
const PHASE_CHECKPOINTS = {
  1: [
    'Watched / read all Intuition resources',
    'Can explain the core concept in one sentence',
  ],
  2: [
    'Explored all listed tools and references for this phase',
    'Identified 2–3 focus areas to dig deeper in Phase 3',
  ],
  3: [
    'Completed all READ items in the reading guide',
    'Can recall the key algorithm or result without notes',
  ],
  4: [
    'Implementation runs and produces expected output',
    'Results match the expected range or pass sanity checks',
  ],
  5: [
    'Summary / learning-log entry written',
    'Can explain how this step connects to the thesis',
  ],
};

/* ===== Report Availability (stepId → reports folder name) ===== */
const STEP_REPORTS = { step_01: 'step01', step_02: 'step02' };
const REPORT_BASE_URL = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/reports';
const SUMMARY_BASE_URL = 'https://github.com/alexander-ra/rlPlanRevised/raw/master/deliverables/summaries';

/* ===== Tertiary step colors for calendar (cycle within phase) ===== */
const STEP_BG_PALETTE = [
  ['#dbeafe','#bfdbfe','#93c5fd'],  // A — blue
  ['#fae8ff','#f5d0fe','#f0abfc'],  // B — fuchsia (swap from indigo)
  ['#fef3c7','#fde68a','#fcd34d'],  // C — amber  (swap from purple)
  ['#ffe4e6','#fecdd3','#fda4af'],  // D — rose
  ['#dcfce7','#bbf7d0','#86efac'],  // E — emerald
  ['#cffafe','#a5f3fc','#67e8f9'],  // F — cyan   (swap from teal)
  ['#ede9fe','#ddd6fe','#c4b5fd'],  // G — violet (swap from amber)
];
const STEP_BG_PALETTE_DARK = [
  ['#1e3a5f','#1a3050','#162845'],  // A — blue
  ['#4a1248','#3d1040','#330e38'],  // B — fuchsia
  ['#44310a','#3a2808','#302006'],  // C — amber
  ['#4a1a2e','#401528','#361022'],  // D — rose
  ['#14432a','#103824','#0c2d1e'],  // E — emerald
  ['#0a3040','#08283a','#062033'],  // F — cyan
  ['#2a1555','#23114a','#1c0d3e'],  // G — violet
];
const PHASE_ORDER = ['A','B','C','D','E','F','G'];
function getStepBg(stepIndex) {
  const step = STEP_META[stepIndex];
  const phaseIdx = PHASE_ORDER.indexOf(step.phase);
  const palette = document.documentElement.getAttribute('data-theme') === 'dark' ? STEP_BG_PALETTE_DARK : STEP_BG_PALETTE;
  const colors = palette[phaseIdx] || palette[0];
  // Find position within this phase
  let posInPhase = 0;
  for (let i = 0; i < stepIndex; i++) {
    if (STEP_META[i].phase === step.phase) posInPhase++;
  }
  return colors[posInPhase % colors.length];
}

// STEPS_CONTENT is injected by build.py via the content placeholder

/* ===== State ===== */
let currentStepIndex = 0;
let scheduleAdjust = 0; // days to delay plan start (shifts all dates forward)
let isHomepage = false;
let calendarMonth = new Date().getMonth();
let calendarYear = new Date().getFullYear();
let calendarFull = false;

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
  updateTopbarThemeIcon();
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

    // Extract metadata from next sibling text node
    // Handles both new format "⏱ ~12m · Channel: Name" and legacy "Duration: ~12m | Channel: Name"
    let node = card.nextSibling;
    for (let i = 0; i < 6 && node; i++, node = node.nextSibling) {
      if (node.nodeType === 3) {
        const text = node.textContent.replace(/\s+/g, ' ').trim();
        let durText = null, chanText = null;

        if (text.startsWith('⏱')) {
          // New format: "⏱ ~12m · Channel: CrashCourse" or "⏱ ~12m · Instructor: Name"
          const parts = text.replace(/^⏱\s*/, '').split(/\s*·\s*/);
          durText = parts[0] ? parts[0].trim() : null;
          // First part that contains a role keyword is the channel
          for (let p = 1; p < parts.length; p++) {
            if (/^(?:Channel|Instructor|Creator):/i.test(parts[p])) {
              chanText = parts[p].replace(/^(?:Channel|Instructor|Creator):\s*/i, '').trim();
              break;
            }
          }
        } else if (text.startsWith('Duration:')) {
          // Legacy format: "Duration: ~12m | Channel: Name"
          const durM = text.match(/Duration:\s*([^|]+)/);
          const chanM = text.match(/(?:Channel|Instructor|Creator):\s*(.+)/);
          durText  = durM  ? durM[1].trim()  : null;
          chanText = chanM ? chanM[1].trim() : null;
        }

        if (durText || chanText) {
          if (durText) {
            const dur = document.createElement('span');
            dur.className = 'yt-duration';
            dur.textContent = durText;
            thumbWrap.appendChild(dur);
          }
          if (chanText) {
            const chan = document.createElement('div');
            chan.className = 'yt-channel';
            chan.textContent = chanText;
            card.appendChild(chan);
          }
          break;
        }
      }
    }
  });
}

/* ===== Checkpoint Progress Counting ===== */
function getStepCheckboxCounts(stepId) {
  const md = typeof STEPS_CONTENT !== 'undefined' ? STEPS_CONTENT[stepId] : null;
  if (!md) return { total: 0, checked: 0 };

  // Count markdown checkboxes
  const allMatches = md.match(/- \[[ x]\]/g);
  const mdTotal = allMatches ? allMatches.length : 0;
  let mdChecked = 0;
  for (let i = 0; i < mdTotal; i++) {
    if (cloudData.checkboxes[`cb_${stepId}_${i}`] === '1') mdChecked++;
  }

  // Count per-phase checkpoints
  let pchkTotal = 0, pchkChecked = 0;
  for (let phase = 1; phase <= 5; phase++) {
    const texts = PHASE_CHECKPOINTS[phase];
    if (!texts) continue;
    pchkTotal += texts.length;
    texts.forEach((_, idx) => {
      if (cloudData.checkboxes[`pchk_${stepId}_${phase}_${idx}`] === '1') pchkChecked++;
    });
  }

  return { total: mdTotal + pchkTotal, checked: mdChecked + pchkChecked };
}

/* ===== Checkbox Persistence (Cloud) ===== */
function setupCheckboxes() {
  const contentEl = document.getElementById('content');
  const stepId = STEP_META[currentStepIndex].id;
  const checkboxes = contentEl.querySelectorAll('input[type="checkbox"]:not([data-pchk])');
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

/* Returns 'done' | 'active' | 'upcoming' for a step's nav dot (5.3) */
function getNavDotStatus(stepId) {
  const progress = getStepCheckboxCounts(stepId);
  if (progress.total > 0 && progress.checked >= progress.total) return 'done';
  if (!isHomepage && STEP_META[currentStepIndex] && STEP_META[currentStepIndex].id === stepId) return 'active';
  return 'upcoming';
}

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
  let currentGroup = null;

  STEP_META.forEach((step) => {
    if (step.phase !== currentPhase) {
      currentPhase = step.phase;

      // Collapsible phase label (5.4)
      const label = document.createElement('button');
      label.className = 'phase-label';
      label.dataset.phase = currentPhase;
      let phaseCollapsed = false;
      try { phaseCollapsed = localStorage.getItem('navPhaseCollapsed_' + currentPhase) === '1'; } catch(e) {}
      const chevron = document.createElement('span');
      chevron.className = 'phase-label-chevron';
      chevron.textContent = phaseCollapsed ? '\u25B6' : '\u25BC';
      label.appendChild(chevron);
      label.appendChild(document.createTextNode('\u00A0' + step.phaseLabel));

      const groupItems = document.createElement('div');
      groupItems.className = 'nav-phase-items';
      if (phaseCollapsed) groupItems.classList.add('nav-phase-items--collapsed');

      label.addEventListener('click', () => {
        const nowCollapsed = groupItems.classList.toggle('nav-phase-items--collapsed');
        try { localStorage.setItem('navPhaseCollapsed_' + currentPhase, nowCollapsed ? '1' : '0'); } catch(e) {}
        chevron.textContent = nowCollapsed ? '\u25B6' : '\u25BC';
      });

      navList.appendChild(label);
      navList.appendChild(groupItems);
      currentGroup = groupItems;
    }

    const wrapper = document.createElement('div');
    wrapper.className = 'nav-item-wrap';

    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.step = step.id;
    const hasReport = !!STEP_REPORTS[step.id];
    btn.innerHTML = step.num + '. ' + step.title + (hasReport ? ' <span class="report-badge" title="Report & summary available">\uD83D\uDCD6</span>' : '');

    // Status dot (5.3)
    const dot = document.createElement('span');
    dot.className = 'nav-status-dot nav-status-dot--' + getNavDotStatus(step.id);
    dot.id = 'nav-dot-' + step.id;
    btn.insertBefore(dot, btn.firstChild);

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

    currentGroup.appendChild(wrapper);
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
  // Update status dot (5.3)
  const dot = document.getElementById('nav-dot-' + stepId);
  if (dot) dot.className = 'nav-status-dot nav-status-dot--' + getNavDotStatus(stepId);
}

function updateActiveNav() {
  const activeId = isHomepage ? 'home' : STEP_META[currentStepIndex].id;
  document.querySelectorAll('.nav-item').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.step === activeId);
  });
  // Update status dots (5.3)
  STEP_META.forEach(step => {
    const dot = document.getElementById('nav-dot-' + step.id);
    if (dot) dot.className = 'nav-status-dot nav-status-dot--' + getNavDotStatus(step.id);
  });
}

/* ===== Markdown Rendering ===== */
/* ===== Lazy Render Cache (9.1) ===== */
const _parsedCache = new Map();

function renderStep(stepId) {
  const md = STEPS_CONTENT[stepId];
  if (!md) return;

  // Configure marked
  marked.setOptions({
    gfm: true,
    breaks: false,
  });

  // Pre-process: extract and strip metadata block before parsing
  const stepMeta = STEP_META[currentStepIndex];
  const { cleanMd, metaFields, freshnessLines: metaFreshLines } = extractAndStripMeta(md);

  // Parse markdown to HTML — use cache to avoid re-parsing on revisit
  let html;
  if (_parsedCache.has(stepId)) {
    html = _parsedCache.get(stepId);
  } else {
    html = marked.parse(cleanMd);
    _parsedCache.set(stepId, html);
  }

  // Insert into DOM
  const contentEl = document.getElementById('content');
  contentEl.innerHTML = html;

  // Download cards (summary + report)
  const reportFolder = STEP_REPORTS[stepId];
  if (reportFolder) {
    const wrap = document.createElement('div');
    wrap.className = 'dl-cards';
    wrap.innerHTML = `
      <div class="dl-card dl-card--summary">
        <div class="dl-card-title">Study Summary</div>
        <div class="dl-card-desc">Detailed theoretical narrative covering key concepts and learning notes for the step</div>
        <div class="dl-btns">
          <a href="${SUMMARY_BASE_URL}/${reportFolder}_en.pdf" target="_blank" rel="noopener noreferrer" class="dl-btn"><span class="dl-flag">🇬🇧</span> EN ↓</a>
          <a href="${SUMMARY_BASE_URL}/${reportFolder}_bg.pdf" target="_blank" rel="noopener noreferrer" class="dl-btn"><span class="dl-flag">🇧🇬</span> BG ↓</a>
        </div>
      </div>
      <div class="dl-card dl-card--report">
        <div class="dl-card-title">Implementation Report</div>
        <div class="dl-card-desc">Implementation results, experiment graphs, metrics, and minimal commentary</div>
        <div class="dl-btns">
          <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_en.pdf" target="_blank" rel="noopener noreferrer" class="dl-btn"><span class="dl-flag">🇬🇧</span> EN ↓</a>
          <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_bg.pdf" target="_blank" rel="noopener noreferrer" class="dl-btn"><span class="dl-flag">🇧🇬</span> BG ↓</a>
        </div>
      </div>`;
    contentEl.insertBefore(wrap, contentEl.firstChild);
  }

  // Step metadata info card
  if (metaFields && Object.keys(metaFields).length > 0) {
    const metaCard = buildMetaCard(metaFields, metaFreshLines, stepMeta);
    const h1 = contentEl.querySelector('h1');
    if (h1) h1.insertAdjacentElement('afterend', metaCard);
    else contentEl.insertBefore(metaCard, contentEl.firstChild);
  }

  // Transform reading guide code blocks BEFORE hljs so they aren't syntax-highlighted
  transformReadingGuides();

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

  // Phase number badges + blockquote styling + section tinting (run after IDs are set)
  addPhaseLabels();
  styleSpecialBlockquotes();
  wrapPhaseSections();
  injectPhaseCheckpoints();

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
    
    const sectionEl = document.getElementById('topbar-section');
    const stepMeta = window.STEP_META[window.currentStepIndex];
    if (!stepMeta || !sectionEl) return;
    if (visibleHeaders.length > 0) {
      const h = visibleHeaders[visibleHeaders.length - 1];
      const txt = (h.dataset.sectionTitle || h.textContent)
        .replace('▶', '').replace('▼', '').replace('Table of Contents', 'Overview').trim();
      sectionEl.textContent = `${stepMeta.phaseLabel} · ${txt}`;
    } else if (window.scrollY < 100) {
      sectionEl.textContent = stepMeta.phaseLabel;
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

  // Copy buttons for code blocks
  addCopyButtons();

  // Reset reading progress to top
  updateReadingProgress();

  // Checkbox persistence
  setupCheckboxes();

  // Phase checkpoint persistence
  setupPhaseCheckpoints();
}

/* ===== Navigation Logic ===== */
function navigateTo(stepId) {
  if (stepId === 'home') { navigateHome(); return; }

  const contentEl = document.getElementById('content');

  const doRender = () => {
    isHomepage = false;
    document.getElementById('timeline-bar').style.display = '';
    document.getElementById('section-nav').style.display = '';

    const idx = STEP_META.findIndex(s => s.id === stepId);
    if (idx === -1) return;
    currentStepIndex = idx;

    renderStep(stepId);
    updateActiveNav();

    const meta = STEP_META[idx];
    document.getElementById('topbar-title').textContent = 'Step ' + meta.num + ': ' + meta.title;
    const sectionEl = document.getElementById('topbar-section');
    if (sectionEl) sectionEl.textContent = meta.phaseLabel;
    updateFavicon(meta.phase);

    history.replaceState(null, '', '#' + stepId);
    updateNavButtons();
    renderTimeline();
    closeSidebar();

    contentEl.classList.add('content-enter');
    contentEl.addEventListener('animationend', () => contentEl.classList.remove('content-enter'), { once: true });
  };

  contentEl.classList.add('content-exit');
  setTimeout(() => { contentEl.classList.remove('content-exit'); doRender(); }, 150);
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
    item.textContent = h.dataset.sectionTitle || h.textContent;
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
  // Update loading text with step count before the cloud call
  const loadingTextEl = document.getElementById('loading-text');
  if (loadingTextEl) {
    loadingTextEl.textContent = `Loading ${STEP_META.length} steps…`;
  }
  await initCloudStorage();
  if (loadingTextEl) loadingTextEl.textContent = 'Building navigation…';
  buildNav();

  // Dismiss loading overlay
  const loadingEl = document.getElementById('loading-overlay');
  if (loadingEl) { loadingEl.classList.add('hidden'); setTimeout(() => loadingEl.remove(), 500); }

  document.getElementById('hamburger').addEventListener('click', openSidebar);
  document.getElementById('close-sidebar').addEventListener('click', closeSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  document.getElementById('prev-btn').addEventListener('click', goPrev);
  document.getElementById('next-btn').addEventListener('click', goNext);
  document.getElementById('prev-btn-bottom').addEventListener('click', goPrev);
  document.getElementById('next-btn-bottom').addEventListener('click', goNext);

  document.getElementById('section-fab').addEventListener('click', toggleSectionNav);
  document.getElementById('sections-btn-bottom').addEventListener('click', (e) => {
    e.stopPropagation();
    toggleSectionNav();
  });
  document.addEventListener('click', (e) => {
    const nav = document.getElementById('section-nav');
    if (!nav.contains(e.target)) closeSectionNav();
  });

  initScheduleAdjust();
  document.getElementById('sched-minus').addEventListener('click', () => adjustSchedule(-1));
  document.getElementById('sched-plus').addEventListener('click', () => adjustSchedule(1));
  document.getElementById('theme-toggle-top').addEventListener('click', toggleTheme);

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

window.toggleCalendarFull = function() {
  calendarFull = !calendarFull;
  if (isHomepage) navigateHome();
};

function buildCalendar() {
  if (calendarFull) {
    return `<div class="cal-wrap cal-wrap--full">
      <div class="cal-header">
        <span class="cal-month-label">Mar &ndash; Oct 2026</span>
        <button class="cal-view-toggle" onclick="window.toggleCalendarFull()">Month View</button>
      </div>
      ${buildAllMonthsView()}
      ${buildCalendarLegend()}
    </div>`;
  }

  const planStart = addDays(PLAN_START, scheduleAdjust);
  const minM = planStart.getMonth(), minY = planStart.getFullYear();
  const atMin = calendarYear === minY && calendarMonth === minM;
  const atMax = calendarYear === 2026 && calendarMonth === 9;

  const header = `<div class="cal-header">
    <button class="cal-nav-btn${atMin ? ' disabled' : ''}" onclick="changeCalMonth(-1)" aria-label="Previous month" ${atMin ? 'disabled' : ''}>\u2039</button>
    <span class="cal-month-label">${MONTH_NAMES[calendarMonth]} ${calendarYear}</span>
    <button class="cal-nav-btn${atMax ? ' disabled' : ''}" onclick="changeCalMonth(1)" aria-label="Next month" ${atMax ? 'disabled' : ''}>\u203A</button>
    <button class="cal-view-toggle" onclick="window.toggleCalendarFull()">Full View</button>
  </div>`;

  const grid = buildCalendarMonth(calendarYear, calendarMonth);
  const legend = buildCalendarLegend();
  return `<div class="cal-wrap">${header}${grid}${legend}</div>`;
}

function buildAllMonthsView() {
  const FULL_MONTHS = [[2026,2],[2026,3],[2026,4],[2026,5],[2026,6],[2026,7],[2026,8],[2026,9]];
  return `<div class="cal-full-grid">${FULL_MONTHS.map(([y,m]) =>
    `<div class="cal-full-month">
      <div class="cal-full-month-hdr">${MONTH_NAMES[m]}</div>
      ${buildCalendarMonth(y, m)}
    </div>`
  ).join('')}</div>`;
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
      const bg = getStepBg(si);
      style = `background:${bg};border-color:${c.border};`;
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
  let currentPhase = null;

  STEP_META.forEach((step, i) => {
    const rng = getStepDateRange(i);
    const st = getStepStatus(i);
    const c = getPhaseColors(step.phase);
    const tier = getStepTier(step.num);
    const summary = extractStepSummary(step.id);
    const icon = st === 'done'
      ? '<span class="step-status step-status--done" title="Completed"></span>'
      : st === 'active'
      ? '<span class="step-status step-status--active" title="Active"></span>'
      : '<span class="step-status step-status--upcoming" title="Upcoming"></span>';
    const hasReport = !!STEP_REPORTS[step.id];
    const reportFolder = STEP_REPORTS[step.id];
    const reportBadge = hasReport ? '<span class="sc-report-badge" title="Report &amp; summary available">PDF</span>' : '';
    const progress = getStepCheckboxCounts(step.id);
    const progressPct = progress.total > 0 ? Math.round((progress.checked / progress.total) * 100) : 0;
    const progressHtml = progress.total > 0
      ? `<div class="sc-progress"><div class="sc-progress-bar"><div class="sc-progress-fill" style="width:${progressPct}%;background:${c.border}"></div></div><span class="sc-progress-text">${progress.checked}/${progress.total}</span></div>`
      : '';
    const dlHtml = reportFolder ? `
      <div class="sc-dl-row" onclick="event.stopPropagation()">
        <span class="sc-dl-label">Summary:</span>
        <a href="${SUMMARY_BASE_URL}/${reportFolder}_en.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDEC\uD83C\uDDE7 EN</a>
        <a href="${SUMMARY_BASE_URL}/${reportFolder}_bg.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDE7\uD83C\uDDEC BG</a>
        <span class="sc-dl-sep">|</span>
        <span class="sc-dl-label">Report:</span>
        <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_en.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDEC\uD83C\uDDE7 EN</a>
        <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_bg.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDE7\uD83C\uDDEC BG</a>
      </div>` : '';

    // Phase group header
    if (step.phase !== currentPhase) {
      if (currentPhase !== null) html += '</div>';
      currentPhase = step.phase;
      html += `<div class="sc-phase-group"><div class="sc-phase-header" style="border-bottom-color:${c.border}"><span class="sc-phase-badge" style="background:${c.bg};color:${c.text};border-color:${c.border}">${step.phase}</span><span class="sc-phase-name">${step.phaseLabel}</span></div>`;
    }

    html += `<div class="sc" onclick="navigateTo('${step.id}')" style="border-left:4px solid ${c.border}">
      <div class="sc-top"><span class="sc-num">${icon} Step ${step.num}</span><span class="sc-badges">${reportBadge}</span></div>
      <div class="sc-title">${step.title}</div>
      <div class="sc-meta"><span>${formatDayShort(rng.start)} \u2013 ${formatDayShort(rng.end)}</span><span>${step.days}d \u00b7 ${tier}</span></div>
      ${progressHtml}
      ${summary ? `<div class="sc-desc">${summary}</div>` : ''}
      ${dlHtml}
    </div>`;
  });

  if (currentPhase !== null) html += '</div>';
  return html;
}

/* ===== Phase Checkpoint Injection (7.5) ===== */
function injectPhaseCheckpoints() {
  const contentEl = document.getElementById('content');
  if (!contentEl || currentStepIndex < 0) return;
  const stepId = STEP_META[currentStepIndex].id;

  contentEl.querySelectorAll('.phase-section').forEach(section => {
    const m = section.className.match(/phase-section--(\d)/);
    if (!m) return;
    const n = +m[1];
    const texts = PHASE_CHECKPOINTS[n];
    if (!texts || !texts.length) return;
    if (section.querySelector('.phase-checkpoint')) return; // guard against double-inject

    const card = document.createElement('div');
    card.className = 'phase-checkpoint';

    const hdr = document.createElement('div');
    hdr.className = 'phase-checkpoint-hdr';
    const titleSpan = document.createElement('span');
    titleSpan.className = 'phase-checkpoint-title';
    titleSpan.textContent = 'Phase ' + n + ' checkpoints';
    const countSpan = document.createElement('span');
    countSpan.className = 'phase-checkpoint-count';
    countSpan.id = 'pchk-count-' + stepId + '-' + n;
    countSpan.textContent = '0/' + texts.length;
    hdr.appendChild(titleSpan);
    hdr.appendChild(countSpan);
    card.appendChild(hdr);

    texts.forEach((text, idx) => {
      const key = 'pchk_' + stepId + '_' + n + '_' + idx;
      const labelEl = document.createElement('label');
      labelEl.className = 'phase-checkpoint-item';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.setAttribute('data-pchk', key);
      cb.removeAttribute('disabled');
      const span = document.createElement('span');
      span.textContent = text;
      labelEl.appendChild(cb);
      labelEl.appendChild(span);
      card.appendChild(labelEl);
    });

    section.appendChild(card);
  });
}

function setupPhaseCheckpoints() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;

  contentEl.querySelectorAll('input[data-pchk]').forEach(cb => {
    const key = cb.getAttribute('data-pchk');
    if (cloudData.checkboxes[key] === '1') cb.checked = true;
    _updatePchkCount(cb);
    cb.addEventListener('change', () => {
      cloudData.checkboxes[key] = cb.checked ? '1' : '0';
      syncToCloud();
      _updatePchkCount(cb);
    });
  });
}

function _updatePchkCount(cb) {
  const key = cb.getAttribute('data-pchk');
  // key: pchk_{stepId}_{phaseNum}_{idx}
  const m = key.match(/^pchk_(.+)_(\d+)_\d+$/);
  if (!m) return;
  const stepId = m[1];
  const countEl = document.getElementById('pchk-count-' + stepId + '-' + m[2]);
  if (!countEl) return;
  const card = cb.closest('.phase-checkpoint');
  if (!card) return;
  const all = card.querySelectorAll('input[data-pchk]');
  const done = Array.from(all).filter(c => c.checked).length;
  countEl.textContent = done + '/' + all.length;
  card.classList.toggle('phase-checkpoint--done', done === all.length && all.length > 0);
  // Propagate to sidebar nav and homepage step card progress
  updateNavProgress(stepId);
}

/* ===== Homepage Hero Section (4.1) ===== */
function buildHeroSection() {
  const today = new Date(); today.setHours(0,0,0,0);
  const planStart = addDays(PLAN_START, scheduleAdjust);
  const planEnd = addDays(planStart, BASE_TOTAL_DAYS - 1);
  const daysElapsed = Math.max(0, Math.min(BASE_TOTAL_DAYS, Math.round((today - planStart) / 86400000) + 1));
  const daysLeft = Math.max(0, Math.round((planEnd - today) / 86400000));

  let stepsCompleted = 0;
  let activeStepMeta = null;
  STEP_META.forEach((step, i) => {
    const st = getStepStatus(i);
    if (st === 'done') stepsCompleted++;
    if (st === 'active' && !activeStepMeta) activeStepMeta = step;
  });

  // SVG donut ring — r=38, circumference = 2*PI*38 ≈ 238.76
  const circum = 238.76;
  const ringDash = ((stepsCompleted / 15) * circum).toFixed(1);
  const activeText = activeStepMeta
    ? `Step ${activeStepMeta.num}: ${activeStepMeta.title}`
    : (stepsCompleted === 15 ? 'All complete' : 'Not started');

  const contributions = [
    { id: 'C1', title: 'Behavioral Adaptation', desc: 'Real-time opponent strategy inference' },
    { id: 'C2', title: 'Safe Exploitation', desc: 'KL-regularized multi-agent exploitation' },
    { id: 'C3', title: 'Evaluation Methodology', desc: 'Domain-agnostic adaptability framework' },
  ];
  const contribHtml = contributions.map(c =>
    `<div class="hp-contribution">
      <span class="hp-contrib-id">${c.id}</span>
      <div><div class="hp-contrib-title">${c.title}</div><div class="hp-contrib-desc">${c.desc}</div></div>
    </div>`
  ).join('');

  return `<div class="hp-hero">
    <div class="hp-hero-main">
      <div class="hp-hero-copy">
        <h1 class="hp-hero-title">PhD Research Plan</h1>
        <p class="hp-hero-sub">AI in Computer Games &mdash; Adaptive Strategy in Multi-Agent Imperfect-Information Environments</p>
        <div class="hp-stats-row">
          <div class="hp-stat"><span class="hp-stat-val">${stepsCompleted}/15</span><span class="hp-stat-label">Steps done</span></div>
          <div class="hp-stat"><span class="hp-stat-val">${daysElapsed}</span><span class="hp-stat-label">Days in</span></div>
          <div class="hp-stat"><span class="hp-stat-val">${daysLeft}</span><span class="hp-stat-label">Days left</span></div>
          <div class="hp-stat hp-stat--current"><span class="hp-stat-val hp-stat-val--sm">${activeText}</span><span class="hp-stat-label">Current step</span></div>
        </div>
      </div>
      <div class="hp-hero-ring" aria-label="${stepsCompleted} of 15 steps completed">
        <svg viewBox="0 0 100 100" width="110" height="110" overflow="visible">
          <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="9"/>
          <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="9"
            stroke-dasharray="${ringDash} ${circum}" stroke-linecap="round"
            transform="rotate(-90 50 50)"/>
          <text x="50" y="48" text-anchor="middle" font-size="21" font-weight="700" fill="white">${stepsCompleted}</text>
          <text x="50" y="62" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.65)">of 15</text>
        </svg>
      </div>
    </div>
    <div class="hp-contributions">${contribHtml}</div>
  </div>`;
}

/* ===== Overall Progress Visualization (4.4) ===== */
function buildProgressViz() {
  const today = new Date(); today.setHours(0,0,0,0);
  const planStart = addDays(PLAN_START, scheduleAdjust);
  const daysElapsed = Math.max(0, Math.min(BASE_TOTAL_DAYS, Math.round((today - planStart) / 86400000) + 1));

  let stepsCompleted = 0, totalChecked = 0, totalCB = 0;
  STEP_META.forEach((step, i) => {
    if (getStepStatus(i) === 'done') stepsCompleted++;
    const cnt = getStepCheckboxCounts(step.id);
    totalChecked += cnt.checked;
    totalCB += cnt.total;
  });

  let segments = '';
  STEP_META.forEach((step, i) => {
    const c = getPhaseColors(step.phase);
    const st = getStepStatus(i);
    const widthPct = (step.days / BASE_TOTAL_DAYS * 100).toFixed(3);
    segments += `<div class="hp-seg hp-seg--${st}" style="width:${widthPct}%;background:${c.border}" onclick="navigateTo('${step.id}')" title="Step ${step.num}: ${step.title} (${step.days}d)"></div>`;
  });

  const todayPct = Math.min(100, (daysElapsed / BASE_TOTAL_DAYS) * 100).toFixed(3);

  let labels = '';
  STEP_META.forEach(step => {
    const widthPct = (step.days / BASE_TOTAL_DAYS * 100).toFixed(3);
    labels += `<div class="hp-gantt-label" style="width:${widthPct}%">${step.num}</div>`;
  });

  const cbText = totalCB > 0 ? `${totalChecked}/${totalCB} checkboxes` : '';
  const parts = [`${stepsCompleted}/15 steps completed`, `${daysElapsed}/${BASE_TOTAL_DAYS} days elapsed`, cbText].filter(Boolean);

  return `<div class="hp-progress-viz">
    <div class="hp-progress-stats">${parts.join(' &middot; ')}</div>
    <div class="hp-step-bar-wrap">
      <div class="hp-step-bar">${segments}<div class="hp-today-line" style="left:${todayPct}%" title="Today"></div></div>
      <div class="hp-gantt-labels">${labels}</div>
    </div>
  </div>`;
}

function navigateHome() {
  const contentEl = document.getElementById('content');

  const doRender = () => {
    isHomepage = true;
    currentStepIndex = -1;
    document.getElementById('topbar-title').textContent = 'RL Study Plan';
    const sectionEl = document.getElementById('topbar-section');
    if (sectionEl) sectionEl.textContent = '';
    updateFavicon(null);
    document.getElementById('timeline-bar').style.display = 'none';
    document.getElementById('section-nav').style.display = 'none';
    updateNavButtons();
    updateActiveNav();
    history.replaceState(null, '', '#home');

    contentEl.innerHTML =
      `<div class="hp">
        ${buildHeroSection()}
        <h2 class="hp-sec">Overall Progress</h2>
        ${buildProgressViz()}
        <h2 class="hp-sec">Timeline</h2>
        ${buildGanttCalendar()}
        <h2 class="hp-sec">Steps</h2>
        <div class="sc-list">${buildStepSummaries()}</div>
      </div>`;
    window.scrollTo(0, 0);
    updateReadingProgress();
    closeSidebar();

    contentEl.classList.add('content-enter');
    contentEl.addEventListener('animationend', () => contentEl.classList.remove('content-enter'), { once: true });
  };

  contentEl.classList.add('content-exit');
  setTimeout(() => { contentEl.classList.remove('content-exit'); doRender(); }, 150);
}

/* ===== Dynamic Favicon (8.2) ===== */
function updateFavicon(phase) {
  const link = document.querySelector('link[rel="icon"]');
  if (!link) return;
  if (!phase) {
    link.href = 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>\uD83E\uDDE0</text></svg>';
    return;
  }
  const c = getPhaseColors(phase);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="15" fill="${c.border}"/><text x="16" y="21" text-anchor="middle" font-family="system-ui,sans-serif" font-size="16" font-weight="700" fill="white">${phase}</text></svg>`;
  link.href = 'data:image/svg+xml,' + encodeURIComponent(svg);
}

/* ===== Reading Progress Bar ===== */
function updateReadingProgress() {
  const fill = document.getElementById('reading-progress-fill');
  if (!fill) return;
  if (isHomepage) { fill.style.width = '0'; return; }
  const scrollTop = window.scrollY;
  const docHeight = document.documentElement.scrollHeight - window.innerHeight;
  fill.style.width = (docHeight > 0 ? Math.min(100, (scrollTop / docHeight) * 100) : 0) + '%';
}
window.addEventListener('scroll', updateReadingProgress, { passive: true });

/* ===== Topbar Theme Icon (SVG sun/moon) ===== */
const SUN_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
const MOON_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

function updateTopbarThemeIcon() {
  const btn = document.getElementById('theme-toggle-top');
  if (!btn) return;
  btn.innerHTML = document.documentElement.getAttribute('data-theme') === 'dark' ? MOON_SVG : SUN_SVG;
}

/* ===== Code Block Copy Buttons ===== */
function addCopyButtons() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = 'Copy';
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = pre.querySelector('code');
      const text = code ? code.textContent : pre.textContent;
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = 'Copied!';
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
      }).catch(() => {
        btn.textContent = 'Failed';
        setTimeout(() => { btn.textContent = 'Copy'; }, 1500);
      });
    });
    pre.style.position = 'relative';
    pre.appendChild(btn);
  });
}

/* ===== Reading Guide Transformer (3.2 — styled READ/SKIM/SKIP/MATH/KEY INSIGHT) ===== */
const RG_BADGE_CLASS = {
  'READ': 'rg-read', 'SKIM': 'rg-skim', 'SKIP': 'rg-skip',
  'MATH': 'rg-math', 'KEY INSIGHT': 'rg-insight',
};
const RG_BADGE_LABEL = {
  'READ': 'READ', 'SKIM': 'SKIM', 'SKIP': 'SKIP',
  'MATH': 'MATH', 'KEY INSIGHT': '★ KEY',
};

function transformReadingGuides() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('pre > code').forEach(code => {
    if (!/[├└]──/.test(code.textContent)) return;

    const lines = code.textContent.split('\n');
    const items = [];
    let cur = null;

    for (const line of lines) {
      if (/^[├└]──/.test(line)) {
        if (cur) items.push(cur);
        const rest = line.replace(/^[├└]──\s*/, '');
        const m = rest.match(/^(KEY INSIGHT|READ|SKIM|SKIP|MATH):\s*([\s\S]*)/);
        cur = m
          ? { action: m[1], content: m[2].replace(/^["']/, '').trim() }
          : { action: null, content: rest };
      } else if (cur && (line.startsWith('│') || /^\s{3,}\S/.test(line))) {
        const cont = line.replace(/^[│\s]+/, '').replace(/["']$/, '').trim();
        if (cont) cur.content += ' ' + cont;
      }
    }
    if (cur) items.push(cur);
    if (items.length === 0) return;

    const guide = document.createElement('div');
    guide.className = 'reading-guide';

    items.forEach(item => {
      const row = document.createElement('div');
      row.className = 'rg-row';

      const badge = document.createElement('span');
      badge.className = 'rg-badge ' + (RG_BADGE_CLASS[item.action] || 'rg-skip');
      badge.textContent = RG_BADGE_LABEL[item.action] || (item.action || '—');

      const content = document.createElement('span');
      content.className = 'rg-content';
      content.textContent = item.content.replace(/["']\s*$/, '').trim();

      row.appendChild(badge);
      row.appendChild(content);
      guide.appendChild(row);
    });

    code.closest('pre').replaceWith(guide);
  });
}

/* ===== Phase Number Badges (replaces emoji icons — academic style) ===== */
function addPhaseLabels() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('h2').forEach(h => {
    if (h.dataset.phaseLabelAdded) return;
    const m = h.textContent.trim().match(/^Phase (\d+)[:\s]/);
    if (m) {
      h.dataset.sectionTitle = h.textContent.trim(); // save clean title before DOM modification
      const n = +m[1];
      const badge = document.createElement('span');
      badge.className = `phase-badge phase-badge--${n}`;
      badge.setAttribute('aria-hidden', 'true');
      badge.textContent = n;
      h.insertBefore(badge, h.firstChild);
      h.dataset.phaseLabelAdded = '1';
    }
  });
}

/* ===== Special Blockquote Styling (callouts — 3.4) ===== */
function styleSpecialBlockquotes() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('blockquote').forEach(bq => {
    const strong = bq.querySelector('strong');
    if (!strong) return;
    const label = strong.textContent.trim().replace(/:$/, '');
    if (label === 'Phase Overview') {
      bq.classList.add('bq-phase-overview');
    } else if (label === 'Know-How First compression') {
      bq.classList.add('bq-planning');
      if (!bq.querySelector('.bq-planning-toggle')) {
        const body = document.createElement('div');
        body.className = 'bq-planning-body';
        while (bq.firstChild) body.appendChild(bq.firstChild);
        const toggle = document.createElement('button');
        toggle.className = 'bq-planning-toggle';
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = '<span class="bq-planning-chevron" aria-hidden="true">›</span> Planning Note';
        toggle.addEventListener('click', () => {
          const open = bq.classList.toggle('bq-planning--open');
          toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        bq.appendChild(toggle);
        bq.appendChild(body);
      }
    } else if (/^\[P\d/.test(label)) {
      bq.classList.add('bq-plan-decision');
    } else if (label === 'Why this section exists' || label === 'Before the papers') {
      bq.classList.add('bq-context');
    }
  });
}

/* ===== Phase Section Tinting (wraps Phase 1–5 content blocks) ===== */
function wrapPhaseSections() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  const phaseH2s = Array.from(contentEl.querySelectorAll('h2')).filter(h =>
    /^Phase \d+[:\s]/.test(h.textContent.trim()) || h.dataset.sectionTitle && /^Phase \d+[:\s]/.test(h.dataset.sectionTitle)
  );
  phaseH2s.forEach(h2 => {
    if (h2.closest('.phase-section')) return;
    const raw = h2.dataset.sectionTitle || h2.textContent;
    const m = raw.trim().match(/^Phase (\d+)[:\s]/);
    if (!m) return;
    const n = +m[1];
    const toMove = [h2];
    let el = h2.nextSibling;
    while (el) {
      if (el.nodeType === 1 && /^H[12]$/.test(el.tagName)) break;
      toMove.push(el);
      el = el.nextSibling;
    }
    const wrapper = document.createElement('div');
    wrapper.className = `phase-section phase-section--${n}`;
    h2.parentNode.insertBefore(wrapper, h2);
    toMove.forEach(node => wrapper.appendChild(node));
  });
}

/* ===== Step Metadata Card ===== */
function extractAndStripMeta(md) {
  const lines = md.split('\n');
  let h1Seen = false, foundAny = false;
  const toStrip = new Set();
  const metaFields = {};

  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (!h1Seen) { if (l.startsWith('# ')) h1Seen = true; continue; }
    if (l.trim() === '---') break; // stop at first content separator
    const m = l.match(/^\*\*([^*:]+):\*\*\s*(.*)/);
    if (m) {
      const key = m[1].trim();
      const val = m[2].replace(/\s{2,}$/, '').trim();
      if (['Duration', 'Dependencies', 'Phase'].includes(key)) {
        metaFields[key] = val; toStrip.add(i); foundAny = true;
      }
    }
  }

  if (!foundAny) return { cleanMd: md, metaFields: null, freshnessLines: [] };
  const cleanMd = lines.filter((_, i) => !toStrip.has(i)).join('\n');
  return { cleanMd, metaFields, freshnessLines: [] };
}

function buildMetaCard(metaFields, _freshnessLines, stepMeta) {
  const c = getPhaseColors(stepMeta.phase);
  const card = document.createElement('div');
  card.className = 'step-meta-card';
  card.style.borderLeftColor = c.border;

  for (const [key, val] of Object.entries(metaFields)) {
    const k = document.createElement('span');
    k.className = 'step-meta-key';
    k.textContent = key + ':';
    card.appendChild(k);
    const v = document.createElement('span');
    v.className = 'step-meta-val';
    v.textContent = val;
    card.appendChild(v);
  }
  return card;
}
