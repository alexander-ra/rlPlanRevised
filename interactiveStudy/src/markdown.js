/* ===== Lazy Render Cache ===== */
const _parsedCache = new Map();

/* ===== Checkbox Progress Counting ===== */
function getStepCheckboxCounts(stepId) {
  const stepsContent = getStepsContent();
  const md = stepsContent[stepId];
  if (!md) return { total: 0, checked: 0 };

  const allMatches = md.match(/- \[[ x]\]/g);
  const mdTotal = allMatches ? allMatches.length : 0;
  let mdChecked = 0;
  for (let i = 0; i < mdTotal; i++) {
    if (cloudData.checkboxes[`cb_${stepId}_${i}`] === '1') mdChecked++;
  }

  let pchkTotal = 0, pchkChecked = 0;
  for (const [phase, count] of Object.entries(PHASE_CHECKPOINT_COUNTS)) {
    pchkTotal += count;
    for (let idx = 0; idx < count; idx++) {
      if (cloudData.checkboxes[`pchk_${stepId}_${phase}_${idx}`] === '1') pchkChecked++;
    }
  }

  return { total: mdTotal + pchkTotal, checked: mdChecked + pchkChecked };
}

/* ===== Checkbox Persistence ===== */
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

/* ===== Code Block Copy Buttons ===== */
function addCopyButtons() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.copy-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.textContent = t('copy_btn');
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const code = pre.querySelector('code');
      const text = code ? code.textContent : pre.textContent;
      navigator.clipboard.writeText(text).then(() => {
        btn.textContent = t('copied_btn');
        btn.classList.add('copied');
        setTimeout(() => { btn.textContent = t('copy_btn'); btn.classList.remove('copied'); }, 2000);
      }).catch(() => {
        btn.textContent = t('failed_btn');
        setTimeout(() => { btn.textContent = t('copy_btn'); }, 1500);
      });
    });
    pre.style.position = 'relative';
    pre.appendChild(btn);
  });
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

  // Phase names for the label shown beside the colored bar
  const phaseNames = {
    1: currentLang === 'bg' ? 'Интуиция'        : 'Intuition',
    2: currentLang === 'bg' ? 'Изследване'      : 'Exploration',
    3: currentLang === 'bg' ? 'Четене'          : 'Targeted Reading',
    4: currentLang === 'bg' ? 'Имплементация'   : 'Implementation',
    5: currentLang === 'bg' ? 'Консолидация'    : 'Consolidation',
  };

  let currentPhase = 0;

  headings.forEach((h, i) => {
    if (!h.id) h.id = 'section-' + i;

    // Detect phase number from H2 headings like "Phase 1: …" / "Фаза 1: …"
    if (h.tagName === 'H2') {
      const txt = (h.dataset.sectionTitle || h.textContent).trim();
      const m = txt.match(/^(?:Phase|Фаза) (\d+)[:\s]/);
      if (m) currentPhase = +m[1];
    }

    const isH3 = h.tagName === 'H3';
    const item = document.createElement('button');
    item.className = 'section-item' + (isH3 ? ' indent' : '');
    if (currentPhase > 0) item.dataset.phase = currentPhase;

    const label = h.dataset.sectionTitle || h.textContent;
    if (!isH3 && currentPhase > 0 && phaseNames[currentPhase]) {
      item.innerHTML =
        `<span class="section-item-phase" aria-hidden="true">${phaseNames[currentPhase]}</span>` +
        `<span class="section-item-title">${label}</span>`;
    } else {
      item.textContent = label;
    }

    item.addEventListener('click', () => {
      h.scrollIntoView({ behavior: 'smooth', block: 'start' });
      closeSectionNav();
    });
    dropdown.appendChild(item);
  });
}

/* ===== Markdown Rendering ===== */
function renderStep(stepId) {
  const stepsContent = getStepsContent();
  const md = stepsContent[stepId];
  if (!md) return;

  marked.setOptions({ gfm: true, breaks: false });

  const stepMeta = STEP_META[currentStepIndex];
  const { cleanMd, metaFields, freshnessLines: metaFreshLines } = extractAndStripMeta(md);

  // Cache parsed HTML per step+lang to avoid re-parsing on revisit
  const cacheKey = stepId + ':' + currentLang;
  let html;
  if (_parsedCache.has(cacheKey)) {
    html = _parsedCache.get(cacheKey);
  } else {
    html = marked.parse(cleanMd);
    _parsedCache.set(cacheKey, html);
  }

  const contentEl = document.getElementById('content');
  contentEl.innerHTML = html;

  // Download widget
  const reportFolder = STEP_REPORTS[stepId];
  if (reportFolder) {
    const stepMeta = STEP_META[currentStepIndex];
    const c = getPhaseColors(stepMeta.phase);
    const wrap = document.createElement('div');
    wrap.className = 'dl-widget';
    wrap.innerHTML = `
      <div class="dl-widget-hdr" style="background:linear-gradient(135deg,${c.border} 0%,${c.border}99 100%)">
        <span class="dl-widget-hdr-icon">📥</span>
        <span>${t('deliverables_label')}</span>
      </div>
      <div class="dl-widget-body">
        <div class="dl-widget-col">
          <div class="dl-widget-col-title">${t('study_summary')}</div>
          <div class="dl-widget-col-desc">${t('summary_desc')}</div>
          <div class="dl-widget-btns">
            <a href="${SUMMARY_BASE_URL}/${reportFolder}_en.pdf" target="_blank" rel="noopener noreferrer" class="dl-widget-btn" style="--btn-color:${c.border}">\uD83C\uDDEC\uD83C\uDDE7 EN \u2193</a>
            <a href="${SUMMARY_BASE_URL}/${reportFolder}_bg.pdf" target="_blank" rel="noopener noreferrer" class="dl-widget-btn" style="--btn-color:${c.border}">\uD83C\uDDE7\uD83C\uDDEC BG \u2193</a>
          </div>
        </div>
        <div class="dl-widget-col">
          <div class="dl-widget-col-title">${t('impl_report')}</div>
          <div class="dl-widget-col-desc">${t('report_desc')}</div>
          <div class="dl-widget-btns">
            <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_en.pdf" target="_blank" rel="noopener noreferrer" class="dl-widget-btn" style="--btn-color:${c.border}">\uD83C\uDDEC\uD83C\uDDE7 EN \u2193</a>
            <a href="${REPORT_BASE_URL}/${reportFolder}/${reportFolder}_report_bg.pdf" target="_blank" rel="noopener noreferrer" class="dl-widget-btn" style="--btn-color:${c.border}">\uD83C\uDDE7\uD83C\uDDEC BG \u2193</a>
          </div>
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

  // Transform reading guides BEFORE hljs highlighting
  transformReadingGuides();

  // Syntax highlight code blocks
  contentEl.querySelectorAll('pre code').forEach(block => {
    hljs.highlightElement(block);
  });

  // Render LaTeX math
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

  // Set IDs for headers (for anchor links)
  contentEl.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(h => {
    if (!h.id) {
      h.id = h.textContent.toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-');
    }
  });

  // Content transformations
  addPhaseLabels();
  styleSpecialBlockquotes();
  wrapPhaseSections();
  injectPhaseCheckpoints();

  // Smooth scroll for internal anchor links
  contentEl.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      const targetEl = document.getElementById(this.getAttribute('href').substring(1));
      if (targetEl) targetEl.scrollIntoView({ behavior: 'smooth' });
    });
  });

  // Table of Contents collapsible (matches current language TOC header)
  const tocText = t('toc_header');
  const tocHeader = Array.from(contentEl.querySelectorAll('h2')).find(h =>
    h.textContent.trim() === tocText || h.textContent.trim() === 'Table of Contents' || h.textContent.trim() === 'Съдържание'
  );
  if (tocHeader) {
    tocHeader.style.cursor = 'pointer';
    tocHeader.style.userSelect = 'none';
    tocHeader.innerHTML = '\u25BA ' + tocText;
    const tocList = tocHeader.nextElementSibling;
    if (tocList && tocList.tagName.toLowerCase() === 'ul') {
      tocList.style.display = 'none';
      tocHeader.addEventListener('click', () => {
        if (tocList.style.display === 'none') {
          tocList.style.display = 'block';
          tocHeader.innerHTML = '\u25BC ' + tocText;
        } else {
          tocList.style.display = 'none';
          tocHeader.innerHTML = '\u25BA ' + tocText;
        }
      });
    }
  }

  // External links in new tab
  contentEl.querySelectorAll('a[href^="http"]').forEach(a => {
    a.setAttribute('target', '_blank');
    a.setAttribute('rel', 'noopener noreferrer');
  });

  // Section observer for topbar subtitle
  if (window.__sectionObserver) window.__sectionObserver.disconnect();
  if (isHomepage || isCalendarPage || currentStepIndex < 0) return;

  const headers = Array.from(document.querySelectorAll('#content h1, #content h2'));
  const observer = new IntersectionObserver((entries) => {
    const visibleHeaders = headers.filter(h => {
      const rect = h.getBoundingClientRect();
      return rect.top <= window.innerHeight * 0.4 && rect.bottom >= -window.innerHeight;
    });
    const sectionEl = document.getElementById('topbar-section');
    const sMeta = window.STEP_META[window.currentStepIndex];
    if (!sMeta || !sectionEl) return;
    if (visibleHeaders.length > 0) {
      const h = visibleHeaders[visibleHeaders.length - 1];
      const txt = (h.dataset.sectionTitle || h.textContent)
        .replace('\u25BA', '').replace('\u25BC', '').replace('Table of Contents', 'Overview').trim();
      sectionEl.textContent = `${getPhaseLabel(sMeta.phase)} \u00b7 ${txt}`;
    } else if (window.scrollY < 100) {
      sectionEl.textContent = getPhaseLabel(sMeta.phase);
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

  window.scrollTo(0, 0);
  buildSectionNav();
  embedYouTubeThumbnails();
  addCopyButtons();
  updateReadingProgress();
  setupCheckboxes();
  setupPhaseCheckpoints();
  applyLockState();
  setupGlossaryTooltips();
}
