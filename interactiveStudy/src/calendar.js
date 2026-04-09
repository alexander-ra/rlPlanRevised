/* ===== Step Status ===== */
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
  const stepsContent = getStepsContent();
  const md = stepsContent[stepId];
  if (!md) return '';
  const lines = md.split('\n');
  const targets = [t('extract_target_phase_overview'), t('extract_target_contribution')];
  for (const target of targets) {
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

/* ===== Calendar Helpers ===== */
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
        <button class="cal-view-toggle" onclick="window.toggleCalendarFull()">${t('month_view')}</button>
      </div>
      ${buildAllMonthsView()}
      ${buildCalendarLegend()}
    </div>`;
  }

  const planStart = addDays(PLAN_START, scheduleAdjust);
  const minM = planStart.getMonth(), minY = planStart.getFullYear();
  const atMin = calendarYear === minY && calendarMonth === minM;
  const atMax = calendarYear === 2026 && calendarMonth === 9;
  const monthNames = MONTH_NAMES();

  const header = `<div class="cal-header">
    <button class="cal-nav-btn${atMin ? ' disabled' : ''}" onclick="changeCalMonth(-1)" aria-label="${t('prev_month')}" ${atMin ? 'disabled' : ''}>\u2039</button>
    <span class="cal-month-label">${monthNames[calendarMonth]} ${calendarYear}</span>
    <button class="cal-nav-btn${atMax ? ' disabled' : ''}" onclick="changeCalMonth(1)" aria-label="${t('next_month')}" ${atMax ? 'disabled' : ''}>\u203A</button>
    <button class="cal-view-toggle" onclick="window.toggleCalendarFull()">${t('full_view')}</button>
  </div>`;

  const grid = buildCalendarMonth(calendarYear, calendarMonth);
  const legend = buildCalendarLegend();
  return `<div class="cal-wrap">${header}${grid}${legend}</div>`;
}

function buildAllMonthsView() {
  const FULL_MONTHS = [[2026,2],[2026,3],[2026,4],[2026,5],[2026,6],[2026,7],[2026,8],[2026,9]];
  const monthNames = MONTH_NAMES();
  return `<div class="cal-full-grid">${FULL_MONTHS.map(([y,m]) =>
    `<div class="cal-full-month">
      <div class="cal-full-month-hdr">${monthNames[m]}</div>
      ${buildCalendarMonth(y, m)}
    </div>`
  ).join('')}</div>`;
}

function buildCalendarMonth(year, month) {
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  let startDow = new Date(year, month, 1).getDay() - 1;
  if (startDow < 0) startDow = 6;

  const today = new Date(); today.setHours(0,0,0,0);

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

  // Mon–Sun order
  const dayHeaders = ['day_mon','day_tue','day_wed','day_thu','day_fri','day_sat','day_sun']
    .map(k => `<div class="cal-dh">${t(k)}</div>`).join('');

  let cells = '';
  for (let i = 0; i < startDow; i++) cells += `<div class="cal-cell empty"></div>`;

  for (let d = 1; d <= daysInMonth; d++) {
    const date = new Date(year, month, d);
    const isToday = date.toDateString() === today.toDateString();
    const dow = date.getDay();
    const isWeekend = dow === 0 || dow === 6;
    const si = stepForDay[d - 1];

    let cls = 'cal-cell';
    let style = '', onclick = '', title = '';

    if (isToday) cls += ' today';
    if (isWeekend) cls += ' weekend';

    if (si >= 0) {
      cls += ' has-step';
      const c = getPhaseColors(STEP_META[si].phase);
      const bg = getStepBg(si);
      style = `background:${bg};border-color:${c.border};`;
      onclick = `onclick="navigateTo('${STEP_META[si].id}')"`;
      title = `title="${t('step_prefix')} ${STEP_META[si].num}: ${getStepTitle(STEP_META[si])}"`;

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
    items += `<span class="cal-legend-item"><span class="cal-legend-dot" style="background:${c.bg};border:2px solid ${c.border}"></span>${getPhaseLabel(s.phase)}</span>`;
  });
  return `<div class="cal-legend">${items}</div>`;
}

/* ===== Step Summary Cards ===== */
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
      ? `<span class="step-status step-status--done" title="${t('status_completed')}"></span>`
      : st === 'active'
      ? `<span class="step-status step-status--active" title="${t('status_active')}"></span>`
      : `<span class="step-status step-status--upcoming" title="${t('status_upcoming')}"></span>`;
    const hasReport = !!STEP_REPORTS[step.id];
    const reportFolder = STEP_REPORTS[step.id];
    const reportBadge = hasReport ? `<span class="sc-report-badge" title="${t('report_badge_title')}">PDF</span>` : '';
    const progress = getStepCheckboxCounts(step.id);
    const progressPct = progress.total > 0 ? Math.round((progress.checked / progress.total) * 100) : 0;
    const progressHtml = progress.total > 0
      ? `<div class="sc-progress"><div class="sc-progress-bar"><div class="sc-progress-fill" style="width:${progressPct}%;background:${c.border}"></div></div><span class="sc-progress-text">${progress.checked}/${progress.total}</span></div>`
      : '';
    const dlHtml = reportFolder ? `
      <div class="sc-dl-row" onclick="event.stopPropagation()">
        <span class="sc-dl-label">${t('sc_summary_label')}</span>
        <a href="${SUMMARY_BASE_URL}/${reportFolder}_en.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDEC\uD83C\uDDE7 EN</a>
        <a href="${SUMMARY_BASE_URL}/${reportFolder}_bg.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDE7\uD83C\uDDEC BG</a>
        <span class="sc-dl-sep">|</span>
        <span class="sc-dl-label">${t('sc_report_label')}</span>
        <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_en.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDEC\uD83C\uDDE7 EN</a>
        <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_bg.pdf" target="_blank" rel="noopener noreferrer" class="sc-dl-btn">\uD83C\uDDE7\uD83C\uDDEC BG</a>
      </div>` : '';

    if (step.phase !== currentPhase) {
      if (currentPhase !== null) html += '</div>';
      currentPhase = step.phase;
      html += `<div class="sc-phase-group"><div class="sc-phase-header" style="border-bottom-color:${c.border}"><span class="sc-phase-badge" style="background:${c.bg};color:${c.text};border-color:${c.border}">${step.phase}</span><span class="sc-phase-name">${getPhaseLabel(step.phase)}</span></div>`;
    }

    html += `<div class="sc" onclick="navigateTo('${step.id}')" style="border-left:4px solid ${c.border}">
      <div class="sc-top"><span class="sc-num">${icon} ${t('step_prefix')} ${step.num}</span><span class="sc-badges">${reportBadge}</span></div>
      <div class="sc-title">${getStepTitle(step)}</div>
      <div class="sc-meta"><span>${formatDayShort(rng.start)} \u2013 ${formatDayShort(rng.end)}</span><span>${step.days}${t('days_suffix')} \u00b7 ${tier}</span></div>
      ${progressHtml}
      ${summary ? `<div class="sc-desc">${summary}</div>` : ''}
      ${dlHtml}
    </div>`;
  });

  if (currentPhase !== null) html += '</div>';
  return html;
}

/* ===== Hero Section ===== */
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

  const circum = 238.76;
  const ringDash = ((stepsCompleted / 15) * circum).toFixed(1);
  const activeText = activeStepMeta
    ? `${t('step_prefix')} ${activeStepMeta.num}: ${getStepTitle(activeStepMeta)}`
    : (stepsCompleted === 15 ? t('all_complete') : t('not_started'));

  const contributions = [
    { id: 'C1', title: t('c1_title'), desc: t('c1_desc') },
    { id: 'C2', title: t('c2_title'), desc: t('c2_desc') },
    { id: 'C3', title: t('c3_title'), desc: t('c3_desc') },
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
        <h1 class="hp-hero-title">${t('hero_title')}</h1>
        <p class="hp-hero-sub">${t('hero_sub')}</p>
        <div class="hp-stats-row">
          <div class="hp-stat"><span class="hp-stat-val">${stepsCompleted}/15</span><span class="hp-stat-label">${t('steps_done')}</span></div>
          <div class="hp-stat"><span class="hp-stat-val">${daysElapsed}</span><span class="hp-stat-label">${t('days_in')}</span></div>
          <div class="hp-stat"><span class="hp-stat-val">${daysLeft}</span><span class="hp-stat-label">${t('days_left')}</span></div>
          <div class="hp-stat hp-stat--current"><span class="hp-stat-val hp-stat-val--sm">${activeText}</span><span class="hp-stat-label">${t('current_step')}</span></div>
        </div>
      </div>
      <div class="hp-hero-ring" aria-label="${stepsCompleted} ${t('of_15')} ${t('steps_completed_stat')}">
        <svg viewBox="0 0 100 100" width="110" height="110" overflow="visible">
          <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="9"/>
          <circle cx="50" cy="50" r="38" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="9"
            stroke-dasharray="${ringDash} ${circum}" stroke-linecap="round"
            transform="rotate(-90 50 50)"/>
          <text x="50" y="48" text-anchor="middle" font-size="21" font-weight="700" fill="white">${stepsCompleted}</text>
          <text x="50" y="62" text-anchor="middle" font-size="9" fill="rgba(255,255,255,0.65)">${t('of_15')}</text>
        </svg>
      </div>
    </div>
    <div class="hp-contributions">${contribHtml}</div>
  </div>`;
}

/* ===== Overall Progress Bar ===== */
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
    segments += `<div class="hp-seg hp-seg--${st}" style="width:${widthPct}%;background:${c.border}" onclick="navigateTo('${step.id}')" title="${t('step_prefix')} ${step.num}: ${getStepTitle(step)} (${step.days}${t('days_suffix')})"></div>`;
  });

  const todayPct = Math.min(100, (daysElapsed / BASE_TOTAL_DAYS) * 100).toFixed(3);

  let labels = '';
  STEP_META.forEach(step => {
    const widthPct = (step.days / BASE_TOTAL_DAYS * 100).toFixed(3);
    labels += `<div class="hp-gantt-label" style="width:${widthPct}%">${step.num}</div>`;
  });

  const cbText = totalCB > 0 ? `${totalChecked}/${totalCB} ${t('checkboxes_stat')}` : '';
  const parts = [
    `${stepsCompleted}/15 ${t('steps_completed_stat')}`,
    `${daysElapsed}/${BASE_TOTAL_DAYS} ${t('days_elapsed_stat')}`,
    cbText
  ].filter(Boolean);

  return `<div class="hp-progress-viz">
    <div class="hp-progress-stats">${parts.join(' &middot; ')}</div>
    <div class="hp-step-bar-wrap">
      <div class="hp-step-bar">${segments}<div class="hp-today-line" style="left:${todayPct}%" title="${t('today_label')}"></div></div>
      <div class="hp-gantt-labels">${labels}</div>
    </div>
  </div>`;
}

/* ===== Homepage ===== */
function navigateHome() {
  const contentEl = document.getElementById('content');

  const doRender = () => {
    isHomepage = true;
    currentStepIndex = -1;
    document.getElementById('topbar-title').textContent = t('hero_title');
    const sectionEl = document.getElementById('topbar-section');
    if (sectionEl) sectionEl.textContent = '';
    document.getElementById('timeline-bar').style.display = 'none';
    updateNavButtons();
    updateFab();
    updateActiveNav();
    history.replaceState(null, '', '#home');

    contentEl.innerHTML =
      `<div class="hp">
        ${buildHeroSection()}
        <h2 class="hp-sec">${t('overall_progress')}</h2>
        ${buildProgressViz()}
        <h2 class="hp-sec">${t('timeline_label')}</h2>
        ${buildCalendar()}
        <h2 class="hp-sec">${t('steps_label')}</h2>
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
