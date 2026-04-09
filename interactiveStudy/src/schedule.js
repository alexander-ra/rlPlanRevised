/* ===== Schedule Computation ===== */

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
  return d.getDate() + ' ' + MONTH_NAMES()[d.getMonth()];
}

function getMaxAdjust() {
  const deadline = new Date(2026, 9, 31);
  const planEndBase = addDays(PLAN_START, BASE_TOTAL_DAYS - 1);
  return Math.floor((deadline - planEndBase) / 86400000);
}

/* ===== Timeline Bar ===== */
function renderTimeline() {
  const bar = document.getElementById('timeline-bar');
  if (!bar || isHomepage || isCalendarPage) return;

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
  const dayNames = DAY_NAMES();

  let cells = '';
  for (let i = 0; i < totalWindowDays; i++) {
    const d = addDays(windowStart, i);
    const ds = d.toDateString();
    const dow = d.getDay();
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

    const showLabel = isStepBound || isMonday || is1st || isToday;
    const label = showLabel
      ? (isToday
          ? `<span class="tl-label" style="color: #ea580c; font-weight: bold; font-size: 0.65rem; z-index: 10;">${t('today_label')}<br>${d.getDate()}</span>`
          : `<span class="tl-label">${d.getDate()}<br>${dayNames[dow]}</span>`)
      : '';
    const tickCls = showLabel ? 'tl-tick tall' : 'tl-tick';

    cells += `<div class="${cls}"><div class="${tickCls}"></div>${label}</div>`;
  }

  bar.innerHTML =
    `<div class="tl-row">${cells}</div>` +
    `<div class="timeline-label">${formatDayShort(range.start)} \u2013 ${formatDayShort(range.end)} \u00b7 ${range.days}${t('days_suffix')}</div>`;
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
  if (isCalendarPage) navigateCalendar();
  else if (isHomepage) navigateHome();
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
