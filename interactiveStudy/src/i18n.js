/* ===== Internationalisation ===== */
// TRANSLATIONS is injected by build.py before this script runs

let currentLang = (() => {
  try { return localStorage.getItem('rl_lang') || 'bg'; } catch(e) { return 'bg'; }
})();

function t(key, vars) {
  const lang = (TRANSLATIONS && TRANSLATIONS[currentLang]) ? currentLang : 'en';
  const str = (TRANSLATIONS[lang] || {})[key] || (TRANSLATIONS.en || {})[key] || key;
  if (!vars) return str;
  return str.replace(/\{(\w+)\}/g, (_, k) => (vars[k] !== undefined ? vars[k] : _));
}

function getStepsContent() {
  if (currentLang === 'bg' && typeof STEPS_CONTENT_BG !== 'undefined') return STEPS_CONTENT_BG;
  return typeof STEPS_CONTENT_EN !== 'undefined' ? STEPS_CONTENT_EN : {};
}

function getStepTitle(step) {
  return t('step_' + step.id.split('_')[1] + '_title') || step.title;
}

function getPhaseLabel(phase) {
  return t('phase_' + phase.toLowerCase() + '_label');
}

function applyI18nToShell() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll('[data-i18n-aria]').forEach(el => {
    el.setAttribute('aria-label', t(el.dataset.i18nAria));
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el => {
    el.setAttribute('title', t(el.dataset.i18nTitle));
  });
  document.title = t('page_title');
  // Update lang button active states
  const enBtn = document.getElementById('lang-en');
  const bgBtn = document.getElementById('lang-bg');
  if (enBtn) enBtn.classList.toggle('active', currentLang === 'en');
  if (bgBtn) bgBtn.classList.toggle('active', currentLang === 'bg');
}

function setLang(lang) {
  currentLang = lang;
  try { localStorage.setItem('rl_lang', lang); } catch(e) {}
  // Clear render cache so steps re-parse with new content
  if (typeof _parsedCache !== 'undefined') _parsedCache.clear();
  applyI18nToShell();
  // Rebuild nav with updated titles
  const navList = document.getElementById('nav-list');
  if (navList) { navList.innerHTML = ''; buildNav(); }
  // Re-render current view
  if (isCalendarPage) {
    navigateCalendar();
  } else if (isHomepage) {
    navigateHome();
  } else if (currentStepIndex >= 0) {
    navigateTo(STEP_META[currentStepIndex].id);
  }
}

// DAY_NAMES and MONTH_NAMES as functions (locale-aware)
function DAY_NAMES() {
  return ['day_sun','day_mon','day_tue','day_wed','day_thu','day_fri','day_sat'].map(k => t(k));
}
function MONTH_NAMES() {
  return ['month_jan','month_feb','month_mar','month_apr','month_may','month_jun',
          'month_jul','month_aug','month_sep','month_oct','month_nov','month_dec'].map(k => t(k));
}
