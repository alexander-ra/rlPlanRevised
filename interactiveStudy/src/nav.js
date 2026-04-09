/* ===== Sidebar Navigation Builder ===== */
function buildNav() {
  const navList = document.getElementById('nav-list');
  navList.innerHTML = '';

  const homeBtn = document.createElement('button');
  homeBtn.className = 'nav-item nav-home';
  homeBtn.dataset.step = 'home';
  homeBtn.textContent = t('home_btn');
  homeBtn.addEventListener('click', () => navigateHome());
  navList.appendChild(homeBtn);

  let currentPhase = null;

  STEP_META.forEach((step) => {
    if (step.phase !== currentPhase) {
      currentPhase = step.phase;
      const label = document.createElement('div');
      label.className = 'phase-label';
      label.textContent = getPhaseLabel(step.phase);
      navList.appendChild(label);
    }

    const wrapper = document.createElement('div');
    wrapper.className = 'nav-item-wrap';

    const btn = document.createElement('button');
    btn.className = 'nav-item';
    btn.dataset.step = step.id;
    const hasReport = !!STEP_REPORTS[step.id];
    btn.innerHTML = step.num + '. ' + getStepTitle(step) +
      (hasReport ? ` <span class="report-badge" title="${t('report_badge_title')}">\uD83D\uDCD6</span>` : '');
    btn.addEventListener('click', () => navigateTo(step.id));
    wrapper.appendChild(btn);

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

/* ===== Step Navigation ===== */
function navigateTo(stepId) {
  if (stepId === 'home') { navigateHome(); return; }

  const contentEl = document.getElementById('content');

  const doRender = () => {
    isHomepage = false;
    document.getElementById('timeline-bar').style.display = '';
    document.getElementById('section-nav').style.display = '';
    updateFab();

    const idx = STEP_META.findIndex(s => s.id === stepId);
    if (idx === -1) return;
    currentStepIndex = idx;

    renderStep(stepId);
    updateActiveNav();

    const meta = STEP_META[idx];
    document.getElementById('topbar-title').textContent =
      t('step_prefix') + ' ' + meta.num + ': ' + getStepTitle(meta);
    const sectionEl = document.getElementById('topbar-section');
    if (sectionEl) sectionEl.textContent = getPhaseLabel(meta.phase);

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
  if (isHomepage) { navigateTo(STEP_META[0].id); return; }
  if (currentStepIndex < STEP_META.length - 1) {
    navigateTo(STEP_META[currentStepIndex + 1].id);
  }
}

function goPrev() {
  if (currentStepIndex === 0) { navigateHome(); return; }
  if (currentStepIndex > 0) {
    navigateTo(STEP_META[currentStepIndex - 1].id);
  }
}

function updateNavButtons() {
  const atEnd = !isHomepage && currentStepIndex === STEP_META.length - 1;
  document.querySelectorAll('[id^="prev-btn"]').forEach(b => b.disabled = isHomepage);
  document.querySelectorAll('[id^="next-btn"]').forEach(b => b.disabled = atEnd);
}

/* ===== Section Jump Nav ===== */
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
