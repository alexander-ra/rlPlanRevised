/* ===== Phase Number Badges ===== */
// Matches both EN "Phase N:" and BG "Фаза N:"
const PHASE_H2_RE = /^(?:Phase|Фаза) (\d+)[:\s]/;

function addPhaseLabels() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('h2').forEach(h => {
    if (h.dataset.phaseLabelAdded) return;
    const m = h.textContent.trim().match(PHASE_H2_RE);
    if (m) {
      h.dataset.sectionTitle = h.textContent.trim();
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

/* ===== Special Blockquote Styling ===== */
const PHASE_OVERVIEW_LABELS = new Set(['Phase Overview', 'Общ преглед на фазата']);
const PLANNING_LABELS = new Set(['Know-How First compression', 'Компресия "Know-How First"', 'Практическо свиване']);
const CONTEXT_LABELS = new Set(['Why this section exists', 'Before the papers', 'Преди статиите', 'Защо тази секция съществува']);

function styleSpecialBlockquotes() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  contentEl.querySelectorAll('blockquote').forEach(bq => {
    const strong = bq.querySelector('strong');
    if (!strong) return;
    const label = strong.textContent.trim().replace(/:$/, '');
    if (PHASE_OVERVIEW_LABELS.has(label)) {
      bq.classList.add('bq-phase-overview');
    } else if (PLANNING_LABELS.has(label)) {
      bq.classList.add('bq-planning');
      if (!bq.querySelector('.bq-planning-toggle')) {
        const body = document.createElement('div');
        body.className = 'bq-planning-body';
        while (bq.firstChild) body.appendChild(bq.firstChild);
        const toggle = document.createElement('button');
        toggle.className = 'bq-planning-toggle';
        toggle.setAttribute('aria-expanded', 'false');
        toggle.innerHTML = `<span class="bq-planning-chevron" aria-hidden="true">\u203A</span> ${t('bq_planning_note')}`;
        toggle.addEventListener('click', () => {
          const open = bq.classList.toggle('bq-planning--open');
          toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        bq.appendChild(toggle);
        bq.appendChild(body);
      }
    } else if (/^\[P\d/.test(label)) {
      bq.classList.add('bq-plan-decision');
    } else if (CONTEXT_LABELS.has(label)) {
      bq.classList.add('bq-context');
    }
  });
}

/* ===== Phase Section Tinting ===== */
function wrapPhaseSections() {
  const contentEl = document.getElementById('content');
  if (!contentEl) return;
  const phaseH2s = Array.from(contentEl.querySelectorAll('h2')).filter(h => {
    const txt = h.dataset.sectionTitle || h.textContent.trim();
    return PHASE_H2_RE.test(txt);
  });
  phaseH2s.forEach(h2 => {
    if (h2.closest('.phase-section')) return;
    const raw = h2.dataset.sectionTitle || h2.textContent;
    const m = raw.trim().match(PHASE_H2_RE);
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

/* ===== Phase Checkpoint Injection ===== */
function injectPhaseCheckpoints() {
  const contentEl = document.getElementById('content');
  if (!contentEl || currentStepIndex < 0) return;
  const stepId = STEP_META[currentStepIndex].id;

  contentEl.querySelectorAll('.phase-section').forEach(section => {
    const m = section.className.match(/phase-section--(\d)/);
    if (!m) return;
    const n = +m[1];
    const count = PHASE_CHECKPOINT_COUNTS[n] || 0;
    if (!count) return;
    if (section.querySelector('.phase-checkpoint')) return;

    const card = document.createElement('div');
    card.className = 'phase-checkpoint';

    const hdr = document.createElement('div');
    hdr.className = 'phase-checkpoint-hdr';
    const titleSpan = document.createElement('span');
    titleSpan.className = 'phase-checkpoint-title';
    titleSpan.textContent = t('phase_checkpoint_title', { n });
    const countSpan = document.createElement('span');
    countSpan.className = 'phase-checkpoint-count';
    countSpan.id = 'pchk-count-' + stepId + '-' + n;
    countSpan.textContent = '0/' + count;
    hdr.appendChild(titleSpan);
    hdr.appendChild(countSpan);
    card.appendChild(hdr);

    for (let idx = 0; idx < count; idx++) {
      const key = 'pchk_' + stepId + '_' + n + '_' + idx;
      const labelEl = document.createElement('label');
      labelEl.className = 'phase-checkpoint-item';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.setAttribute('data-pchk', key);
      cb.removeAttribute('disabled');
      const span = document.createElement('span');
      span.textContent = t(`phase_${n}_check_${idx}`);
      labelEl.appendChild(cb);
      labelEl.appendChild(span);
      card.appendChild(labelEl);
    }

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
  updateNavProgress(stepId);
}

/* ===== Step Metadata Card ===== */
const META_KEY_ALIASES = {
  '\u041f\u0440\u043e\u0434\u044a\u043b\u0436\u0438\u0442\u0435\u043b\u043d\u043e\u0441\u0442': 'Duration',
  '\u0417\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0438': 'Dependencies',
  '\u0424\u0430\u0437\u0430': 'Phase',
};
const META_ALLOWED = new Set(['Duration', 'Dependencies', 'Phase', ...Object.keys(META_KEY_ALIASES)]);

function extractAndStripMeta(md) {
  const lines = md.split('\n');
  let h1Seen = false, foundAny = false;
  const toStrip = new Set();
  const metaFields = {};

  for (let i = 0; i < lines.length; i++) {
    const l = lines[i];
    if (!h1Seen) { if (l.startsWith('# ')) h1Seen = true; continue; }
    if (l.trim() === '---') break;
    const m = l.match(/^\*\*([^*:]+):\*\*\s*(.*)/);
    if (m) {
      const rawKey = m[1].trim();
      const normKey = META_KEY_ALIASES[rawKey] || rawKey;
      const val = m[2].replace(/\s{2,}$/, '').trim();
      if (META_ALLOWED.has(rawKey)) {
        metaFields[normKey] = val; toStrip.add(i); foundAny = true;
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
    k.textContent = t('meta_' + key.toLowerCase()) + ':';
    card.appendChild(k);
    const v = document.createElement('span');
    v.className = 'step-meta-val';
    v.textContent = val;
    card.appendChild(v);
  }
  return card;
}
