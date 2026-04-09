/* ===== Lock Mode ===== */
const LOCK_KEY      = 'rl_unlocked';
const LOCK_PASSWORD = 'rlStudy';

let isLocked = !localStorage.getItem(LOCK_KEY);

const LOCK_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`;
const UNLOCK_SVG = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>`;
const TOC_SVG_FAB   = `<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" width="16" height="16" aria-hidden="true"><line x1="2" y1="4" x2="16" y2="4"/><line x1="5" y1="8" x2="16" y2="8"/><line x1="5" y1="12" x2="16" y2="12"/><line x1="2" y1="16" x2="16" y2="16"/></svg>`;
const TOC_SVG_BTM   = `<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" width="18" height="18" aria-hidden="true"><line x1="2" y1="4" x2="16" y2="4"/><line x1="5" y1="8" x2="16" y2="8"/><line x1="5" y1="12" x2="16" y2="12"/><line x1="2" y1="16" x2="16" y2="16"/></svg>`;

function initLock() {
  isLocked = !localStorage.getItem(LOCK_KEY);
  applyLockState();
}

function toggleLock() {
  if (isLocked) {
    const lockPrompt = currentLang === 'bg' 
      ? "Въведете парола, за да отключите редактирането.\n\n(Това засяга редактиране на график и отчет. Съдържанието остава същото.)"
      : "Enter password to unlock editing.\n\n(This only affects your personal schedule and completion marks — the study content itself is never modified.)";
    const pw = prompt(lockPrompt);
    if (pw === null) return;
    if (pw === LOCK_PASSWORD) {
      isLocked = false;
      localStorage.setItem(LOCK_KEY, '1');
      applyLockState();
      updateFab();
    } else {
      const incorrectMsg = currentLang === 'bg' ? "Неправилна парола." : "Incorrect password.";
      alert(incorrectMsg);
    }
  } else {
    isLocked = true;
    localStorage.removeItem(LOCK_KEY);
    applyLockState();
    updateFab();
  }
}

function applyLockState() {
  const minus = document.getElementById('sched-minus');
  const plus  = document.getElementById('sched-plus');
  if (minus) minus.disabled = isLocked;
  if (plus)  plus.disabled  = isLocked;

  document.querySelectorAll('#content input[type="checkbox"]').forEach(cb => {
    cb.disabled = isLocked;
  });
}

function updateFab() {
  const fab    = document.getElementById('section-fab');
  const btnBtm = document.getElementById('sections-btn-bottom');
  if (!fab) return;

  if (isHomepage || isCalendarPage) {
    const icon  = isLocked ? LOCK_SVG : UNLOCK_SVG;
    const label = isLocked 
      ? (currentLang === 'bg' ? 'Заключи' : 'Lock')
      : (currentLang === 'bg' ? 'Отключи' : 'Unlock');
    fab.innerHTML = icon;
    fab.setAttribute('aria-label', label);
    fab.title = label;
    fab.classList.toggle('fab-unlocked', !isLocked);
    if (btnBtm) {
      btnBtm.innerHTML = isLocked ? LOCK_SVG : UNLOCK_SVG;
      btnBtm.setAttribute('aria-label', label);
    }
  } else {
    fab.innerHTML = TOC_SVG_FAB;
    fab.setAttribute('aria-label', 'Jump to section');
    fab.removeAttribute('title');
    fab.classList.remove('fab-unlocked');
    if (btnBtm) {
      btnBtm.innerHTML = TOC_SVG_BTM;
      btnBtm.setAttribute('aria-label', 'Jump to section');
    }
  }
}
