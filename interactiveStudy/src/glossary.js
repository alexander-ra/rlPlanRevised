/* ===== Glossary Module ===== */
// GLOSSARY_DATA is injected by build.py as a const before this script.
// isGlossaryPage state is declared in config.js

/* ── Domain colour map (mirrors CSS phase vars) ── */
const GL_DOMAIN_COLORS = {
  rl:           'var(--phase-a-border)',
  game_theory:  'var(--phase-c-border)',
  algorithms:   'var(--phase-g-border)',
  evaluation:   'var(--phase-e-border)',
};

const GL_DOMAIN_ORDER = ['rl', 'game_theory', 'algorithms', 'evaluation'];

function glDomainLabel(domain) {
  const keys = {
    rl:          'gl_domain_rl',
    game_theory: 'gl_domain_gt',
    algorithms:  'gl_domain_alg',
    evaluation:  'gl_domain_eval',
  };
  return t(keys[domain] || domain);
}

/* ──────────────────────────────────────────────────────────────────────────
   GLOSSARY PAGE
   ────────────────────────────────────────────────────────────────────────── */

function navigateGlossary(highlightId) {
  const contentEl = document.getElementById('content');

  const doRender = () => {
    isHomepage    = false;
    isCalendarPage = false;
    isGlossaryPage = true;
    currentStepIndex = -1;

    document.getElementById('topbar-title').textContent = t('glossary_btn');
    const sectionEl = document.getElementById('topbar-section');
    if (sectionEl) sectionEl.textContent = '';
    document.getElementById('timeline-bar').style.display = 'none';
    document.getElementById('section-nav').style.display  = 'none';
    updateNavButtons();
    updateFab();
    updateActiveNav();
    history.replaceState(null, '', '#glossary');

    contentEl.innerHTML = buildGlossaryHTML();
    window.scrollTo(0, 0);
    setupGlossaryInteraction();
    updateReadingProgress();
    closeSidebar();

    if (highlightId) {
      setTimeout(() => {
        const entry = document.querySelector(`.gl-entry[data-id="${highlightId}"]`);
        if (entry) {
          entry.scrollIntoView({ behavior: 'smooth', block: 'center' });
          entry.classList.add('gl-entry--highlight');
          setTimeout(() => entry.classList.remove('gl-entry--highlight'), 2000);
        }
      }, 200);
    }

    contentEl.classList.add('content-enter');
    contentEl.addEventListener('animationend',
      () => contentEl.classList.remove('content-enter'), { once: true });
  };

  contentEl.classList.add('content-exit');
  setTimeout(() => { contentEl.classList.remove('content-exit'); doRender(); }, 150);
}

/* ── Build the full glossary page HTML ── */
function buildGlossaryHTML() {
  if (typeof GLOSSARY_DATA === 'undefined') {
    return `<div class="glossary-page"><p>${t('gl_unavailable')}</p></div>`;
  }

  const lang     = currentLang;
  const altLang  = lang === 'bg' ? 'en' : 'bg';

  /* Group & sort entries by domain */
  const grouped = {};
  GL_DOMAIN_ORDER.forEach(d => (grouped[d] = []));

  for (const [id, entry] of Object.entries(GLOSSARY_DATA)) {
    const domain = entry.domain || 'evaluation';
    if (!grouped[domain]) grouped[domain] = [];
    grouped[domain].push({ id, ...entry });
  }
  GL_DOMAIN_ORDER.forEach(d => {
    grouped[d].sort((a, b) => {
      const at = ((a[lang] || a.en)?.term || '').toLowerCase();
      const bt = ((b[lang] || b.en)?.term || '').toLowerCase();
      return at.localeCompare(bt, lang === 'bg' ? 'bg' : 'en');
    });
  });

  const totalCount = Object.values(grouped).reduce((s, a) => s + a.length, 0);

  /* Domain filter pills */
  const filterPills = GL_DOMAIN_ORDER.map(d => {
    const color = GL_DOMAIN_COLORS[d];
    return `<button class="gl-filter-btn" data-domain="${d}"
              style="--gl-dc:${color}">${glDomainLabel(d)}</button>`;
  }).join('');

  /* Domain sections */
  let sectionsHtml = '';
  for (const domain of GL_DOMAIN_ORDER) {
    const entries = grouped[domain];
    if (!entries.length) continue;
    const color = GL_DOMAIN_COLORS[domain];

    const entriesHtml = entries.map(entry => {
      const primary   = entry[lang]   || entry.en  || {};
      const secondary = entry[altLang] || entry.en  || {};
      const abbr      = entry.en?.abbr || '';

      return `<div class="gl-entry" data-id="${entry.id}" data-domain="${domain}">
        <div class="gl-entry-head">
          <span class="gl-entry-term">${escHtml(primary.term || '')}</span>
          ${abbr ? `<code class="gl-entry-abbr">${escHtml(abbr)}</code>` : ''}
          <span class="gl-entry-badge" style="--gl-dc:${color}">${glDomainLabel(domain)}</span>
        </div>
        ${lang !== 'en' && secondary.term && secondary.term !== primary.term
          ? `<div class="gl-entry-alt">${escHtml(secondary.term)}</div>` : ''}
        <p class="gl-entry-def">${escHtml(primary.def || '')}</p>
      </div>`;
    }).join('');

    sectionsHtml += `
      <section class="gl-domain-section" data-domain="${domain}">
        <h2 class="gl-domain-title" style="--gl-dc:${color}">
          <span class="gl-domain-dot" aria-hidden="true"></span>
          ${glDomainLabel(domain)}
          <span class="gl-domain-count">${entries.length}</span>
        </h2>
        <div class="gl-entries">${entriesHtml}</div>
      </section>`;
  }

  return `
    <div class="glossary-page">
      <div class="glossary-hdr">
        <h1 class="glossary-title">📖 ${t('glossary_btn')}</h1>
        <p class="glossary-meta">${totalCount} ${t('gl_terms_count')}</p>
      </div>

      <div class="glossary-controls">
        <div class="glossary-search-wrap">
          <svg class="glossary-search-icon" viewBox="0 0 20 20" fill="currentColor"
               width="16" height="16" aria-hidden="true">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89
              3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z"
              clip-rule="evenodd"/>
          </svg>
          <input id="gl-search" class="glossary-search" type="search" autocomplete="off"
                 placeholder="${t('gl_search_placeholder')}">
        </div>
        <div class="gl-filters" role="group" aria-label="${t('gl_filter_label')}">
          <button class="gl-filter-btn active" data-domain="all">${t('gl_filter_all')}</button>
          ${filterPills}
        </div>
      </div>

      <div id="gl-body" class="glossary-body">
        ${sectionsHtml}
      </div>
      <p id="gl-empty" class="gl-empty" style="display:none">${t('gl_no_results')}</p>
    </div>`;
}

/* ── Search + filter interaction ── */
function setupGlossaryInteraction() {
  const searchEl = document.getElementById('gl-search');
  if (!searchEl) return;
  searchEl.addEventListener('input', applyGlossaryFilter);
  document.querySelectorAll('.gl-filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.gl-filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyGlossaryFilter();
    });
  });
}

function applyGlossaryFilter() {
  if (typeof GLOSSARY_DATA === 'undefined') return;
  const query      = (document.getElementById('gl-search')?.value || '').toLowerCase().trim();
  const activeDomain = document.querySelector('.gl-filter-btn.active')?.dataset.domain || 'all';
  const lang       = currentLang;
  const altLang    = lang === 'bg' ? 'en' : 'bg';

  let totalVisible = 0;

  document.querySelectorAll('.gl-entry').forEach(el => {
    const id     = el.dataset.id;
    const domain = el.dataset.domain;
    const g      = GLOSSARY_DATA[id];
    if (!g) { el.style.display = 'none'; return; }

    const matchDomain = activeDomain === 'all' || domain === activeDomain;

    let matchQuery = !query;
    if (!matchQuery) {
      const primary   = g[lang]    || g.en  || {};
      const secondary = g[altLang] || g.en  || {};
      const abbr      = (g.en?.abbr || '').toLowerCase();
      matchQuery =
        (primary.term   || '').toLowerCase().includes(query) ||
        (primary.def    || '').toLowerCase().includes(query) ||
        (secondary.term || '').toLowerCase().includes(query) ||
        abbr.includes(query) ||
        id.replace(/_/g, ' ').includes(query);
    }

    const show = matchDomain && matchQuery;
    el.style.display = show ? '' : 'none';
    if (show) totalVisible++;
  });

  /* Show/hide domain sections */
  document.querySelectorAll('.gl-domain-section').forEach(sec => {
    const anyVisible = Array.from(sec.querySelectorAll('.gl-entry'))
      .some(e => e.style.display !== 'none');
    sec.style.display = anyVisible ? '' : 'none';
  });

  const emptyEl = document.getElementById('gl-empty');
  if (emptyEl) emptyEl.style.display = totalVisible === 0 ? '' : 'none';
}

/* ──────────────────────────────────────────────────────────────────────────
   INLINE TOOLTIPS (replacing <sup class="gl"> in step content)
   ────────────────────────────────────────────────────────────────────────── */

function setupGlossaryTooltips() {
  const contentEl = document.getElementById('content');
  if (!contentEl || typeof GLOSSARY_DATA === 'undefined') return;

  contentEl.querySelectorAll('sup.gl[data-gl]').forEach(sup => {
    const tid   = sup.dataset.gl;
    const gData = GLOSSARY_DATA[tid];
    if (!gData) { sup.remove(); return; }

    const lang     = currentLang;
    const altLang  = lang === 'bg' ? 'en' : 'bg';
    const primary  = gData[lang]    || gData.en || {};
    const secondary= gData[altLang] || gData.en || {};
    const color    = GL_DOMAIN_COLORS[gData.domain] || 'var(--primary)';

    /* Wrapper trigger */
    const trigger = document.createElement('span');
    trigger.className   = 'gl-trigger';
    trigger.dataset.gl  = tid;
    trigger.tabIndex    = 0;
    trigger.setAttribute('role', 'button');
    trigger.setAttribute('aria-label',
      `${t('gl_tooltip_aria')}: ${primary.term || tid}`);

    /* Visual icon replaces the raw <sup> */
    const icon = document.createElement('sup');
    icon.className = 'gl-sup-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.innerHTML = '<svg viewBox="0 0 12 12" width="10" height="10" fill="currentColor"' +
      ' aria-hidden="true"><path d="M6 0a6 6 0 100 12A6 6 0 006 0zm.75 9h-1.5V5.25h1.5V9z' +
      'M6 4.5a.75.75 0 110-1.5.75.75 0 010 1.5z"/></svg>';

    /* Popup card */
    const popup = document.createElement('div');
    popup.className = 'gl-popup';
    popup.setAttribute('role', 'tooltip');

    const abbrHtml = gData.en?.abbr
      ? `<code class="gl-popup-abbr">${escHtml(gData.en.abbr)}</code>` : '';
    const altHtml = (secondary.term && secondary.term !== primary.term)
      ? `<div class="gl-popup-alt">${escHtml(secondary.term)}</div>` : '';

    popup.innerHTML = `
      <div class="gl-popup-head" style="border-left-color:${color}">
        <span class="gl-popup-term">${escHtml(primary.term || tid)}</span>
        ${abbrHtml}
        <span class="gl-popup-domain" style="color:${color}">${glDomainLabel(gData.domain)}</span>
      </div>
      ${altHtml}
      <p class="gl-popup-def">${escHtml(primary.def || '')}</p>
      <button class="gl-popup-more" data-gl="${escHtml(tid)}">
        ${t('gl_view_in_glossary')} →
      </button>`;

    trigger.appendChild(icon);
    trigger.appendChild(popup);
    sup.replaceWith(trigger);

    /* Events */
    trigger.addEventListener('touchstart', () => { _glLastTouch = Date.now(); }, { passive: true });
    trigger.addEventListener('mouseenter', () => {
      if (Date.now() - _glLastTouch < 500) return;
      glCancelHide(); glShowPopup(trigger);
    });
    trigger.addEventListener('mouseleave', e => {
      if (Date.now() - _glLastTouch < 500) return;
      if (!trigger.contains(e.relatedTarget)) glScheduleHide(trigger, 250);
    });
    trigger.addEventListener('focus', () => glShowPopup(trigger));
    trigger.addEventListener('blur',  e => {
      if (Date.now() - _glLastTouch < 500) return;
      if (!trigger.contains(e.relatedTarget)) glScheduleHide(trigger, 250);
    });
    trigger.addEventListener('click', e => {
      e.stopPropagation();
      trigger.classList.contains('gl-open') ? glHidePopup(trigger) : glShowPopup(trigger);
    });
    trigger.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        trigger.classList.contains('gl-open') ? glHidePopup(trigger) : glShowPopup(trigger);
      }
      if (e.key === 'Escape') glHidePopup(trigger);
    });

    /* "View in glossary" */
    popup.querySelector('.gl-popup-more').addEventListener('click', e => {
      e.stopPropagation();
      glHidePopup(trigger);
      navigateGlossary(tid);
    });
  });

  /* Global click-away */
  document.addEventListener('click', glCloseAll);
}

let _glHideTimer  = null;
let _glLastTouch  = 0;

function glCancelHide() {
  if (_glHideTimer) { clearTimeout(_glHideTimer); _glHideTimer = null; }
}

function glScheduleHide(trigger, delay) {
  glCancelHide();
  _glHideTimer = setTimeout(() => glHidePopup(trigger), delay ?? 250);
}

function glShowPopup(trigger) {
  glCancelHide();
  glCloseAll();
  trigger.classList.add('gl-open');
  const popup = trigger.querySelector('.gl-popup');
  if (!popup) return;
  glPositionPopup(trigger, popup);
  popup.classList.add('gl-popup--on');
}

function glHidePopup(trigger) {
  trigger.classList.remove('gl-open');
  trigger.querySelector('.gl-popup')?.classList.remove('gl-popup--on');
}

function glCloseAll() {
  glCancelHide();
  document.querySelectorAll('.gl-trigger.gl-open').forEach(t => glHidePopup(t));
}

function glPositionPopup(trigger, popup) {
  // Remove old overrides so getBoundingClientRect reflects natural position
  popup.style.left = '';
  popup.style.top  = '';
  popup.style.bottom = '';
  popup.classList.remove('gl-popup--above', 'gl-popup--below');

  const tr   = trigger.getBoundingClientRect();
  const pw   = 300; // matches CSS max-width
  const spaceAbove = tr.top;
  const spaceBelow = window.innerHeight - tr.bottom;
  const above      = spaceAbove >= 180 || spaceAbove > spaceBelow;

  /* Horizontal: centre on trigger, clamp to viewport */
  let left = tr.left + tr.width / 2 - pw / 2 - tr.left;
  const absLeft = tr.left + left;
  if (absLeft < 8) left += 8 - absLeft;
  if (absLeft + pw > window.innerWidth - 8) left -= (absLeft + pw) - (window.innerWidth - 8);

  popup.style.left = left + 'px';
  if (above) {
    popup.style.bottom = (tr.height + 6) + 'px';
    popup.style.top    = 'auto';
    popup.classList.add('gl-popup--above');
  } else {
    popup.style.top    = (tr.height + 6) + 'px';
    popup.style.bottom = 'auto';
    popup.classList.add('gl-popup--below');
  }
}

/* ── Utility ── */
function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}
