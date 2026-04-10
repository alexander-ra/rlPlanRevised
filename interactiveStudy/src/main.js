/* ===== Initialization ===== */
document.addEventListener('DOMContentLoaded', async () => {
  initTheme();

  // Apply saved language immediately
  applyI18nToShell();

  const loadingTextEl = document.getElementById('loading-text');
  if (loadingTextEl) {
    loadingTextEl.textContent = t('loading_text');
  }

  await initCloudStorage();
  initLock();

  if (loadingTextEl) loadingTextEl.textContent = t('loading_text');

  buildNav();

  const loadingEl = document.getElementById('loading-overlay');
  if (loadingEl) { loadingEl.classList.add('hidden'); setTimeout(() => loadingEl.remove(), 500); }

  // Sidebar controls
  document.getElementById('hamburger').addEventListener('click', openSidebar);
  document.getElementById('close-sidebar').addEventListener('click', closeSidebar);
  document.getElementById('overlay').addEventListener('click', closeSidebar);

  // Nav buttons
  document.getElementById('prev-btn').addEventListener('click', goPrev);
  document.getElementById('next-btn').addEventListener('click', goNext);
  document.getElementById('prev-btn-bottom').addEventListener('click', goPrev);
  document.getElementById('next-btn-bottom').addEventListener('click', goNext);

  // Section jump / lock toggle (context-dependent)
  document.getElementById('section-fab').addEventListener('click', () => {
    if (isHomepage || isCalendarPage || isGlossaryPage) toggleLock();
    else toggleSectionNav();
  });
  document.getElementById('sections-btn-bottom').addEventListener('click', (e) => {
    e.stopPropagation();
    if (isHomepage || isCalendarPage || isGlossaryPage) toggleLock();
    else toggleSectionNav();
  });
  document.addEventListener('click', (e) => {
    const nav = document.getElementById('section-nav');
    if (!nav.contains(e.target)) closeSectionNav();
  });

  // Schedule controls
  initScheduleAdjust();
  document.getElementById('sched-minus').addEventListener('click', () => adjustSchedule(-1));
  document.getElementById('sched-plus').addEventListener('click', () => adjustSchedule(1));

  // Theme toggle
  document.getElementById('theme-toggle-top').addEventListener('click', toggleTheme);

  // Language switcher
  document.getElementById('lang-en').addEventListener('click', () => setLang('en'));
  document.getElementById('lang-bg').addEventListener('click', () => setLang('bg'));

  // Initial view from URL hash
  const hash = window.location.hash.replace('#', '');
  if (hash === 'calendar') {
    navigateCalendar();
  } else if (hash === 'glossary') {
    navigateGlossary();
  } else if (hash && hash !== 'home' && STEP_META.find(s => s.id === hash)) {
    navigateTo(hash);
  } else {
    navigateHome();
  }

  window.addEventListener('hashchange', () => {
    const h = window.location.hash.replace('#', '');
    if (h === 'home' || h === '') { navigateHome(); }
    else if (h === 'calendar') { navigateCalendar(); }
    else if (h === 'glossary') { navigateGlossary(); }
    else if (STEP_META.find(s => s.id === h)) { navigateTo(h); }
  });
});

/* ===== Keyboard Navigation ===== */
document.addEventListener('keydown', (e) => {
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
  if (e.key === 'ArrowLeft') { goPrev(); e.preventDefault(); }
  if (e.key === 'ArrowRight') { goNext(); e.preventDefault(); }
  if (e.key === 'Escape') { closeSidebar(); glCloseAll(); }
});
