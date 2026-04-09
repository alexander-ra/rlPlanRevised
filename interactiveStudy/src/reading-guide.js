/* ===== Reading Guide Transformer (READ/SKIM/SKIP/MATH/KEY INSIGHT) ===== */
const RG_BADGE_CLASS = {
  'READ': 'rg-read', 'SKIM': 'rg-skim', 'SKIP': 'rg-skip',
  'MATH': 'rg-math', 'KEY INSIGHT': 'rg-insight',
};

function getRgBadgeLabel(action) {
  const keyMap = {
    'READ': 'rg_read', 'SKIM': 'rg_skim', 'SKIP': 'rg_skip',
    'MATH': 'rg_math', 'KEY INSIGHT': 'rg_key',
  };
  return keyMap[action] ? t(keyMap[action]) : (action || '\u2014');
}

const BG_ACTION_MAP = {
  'ПРОЧЕТЕТЕ': 'READ',
  'ПРЕГЛЕДАЙТЕ': 'SKIM',
  'ПРОПУСНЕТЕ': 'SKIP',
  'МАТЕМАТИКА': 'MATH',
  'КЛЮЧОВО ПРОЗРЕНИЕ': 'KEY INSIGHT',
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
        const m = rest.match(/^(КЛЮЧОВО ПРОЗРЕНИЕ|ПРОЧЕТЕТЕ|ПРЕГЛЕДАЙТЕ|ПРОПУСНЕТЕ|МАТЕМАТИКА|KEY INSIGHT|READ|SKIM|SKIP|MATH):\s*([\s\S]*)/);
        let action = m ? m[1] : null;
        if (action && BG_ACTION_MAP[action]) action = BG_ACTION_MAP[action];
        cur = m
          ? { action, content: m[2].replace(/^["']/, '').trim() }
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
      badge.textContent = getRgBadgeLabel(item.action);

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
