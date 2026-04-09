/* ===== JSONBin.io Cloud Storage ===== */
const JSONBIN_API_KEY = '$2a$10$k1FLc/sztnYxUeK/9hzPROI8cAJxmQJHZX1CDs.YZbIJL.l2Wi6d6';
const JSONBIN_API_URL = 'https://api.jsonbin.io/v3/b';
const JSONBIN_BIN_ID = '69d2c3e1aaba882197c967a7';
const JSONBIN_BIN_KEY = 'rlstudy_bin_id';
let cloudData = { checkboxes: {}, scheduleAdjust: 0 };
let binId = null;
let syncTimeout = null;

async function initCloudStorage() {
  const targetId = JSONBIN_BIN_ID || (() => {
    try { return localStorage.getItem(JSONBIN_BIN_KEY); } catch(e) { return null; }
  })();

  if (targetId) {
    try {
      const res = await fetch(`${JSONBIN_API_URL}/${targetId}/latest`, {
        headers: { 'X-Master-Key': JSONBIN_API_KEY }
      });
      if (res.ok) {
        const json = await res.json();
        cloudData = json.record || cloudData;
        binId = targetId;
        try { localStorage.setItem(JSONBIN_BIN_KEY, binId); } catch(e) {}
        return cloudData;
      }
    } catch(e) { console.warn('Cloud load failed:', e); }
    if (JSONBIN_BIN_ID) {
      console.error('Hardcoded JSONBIN_BIN_ID is invalid:', JSONBIN_BIN_ID);
      return cloudData;
    }
    try { localStorage.removeItem(JSONBIN_BIN_KEY); } catch(e) {}
  }

  try {
    const res = await fetch(JSONBIN_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Master-Key': JSONBIN_API_KEY,
        'X-Bin-Name': 'rl-study-progress'
      },
      body: JSON.stringify(cloudData)
    });
    if (res.ok) {
      const json = await res.json();
      binId = json.metadata.id;
      try { localStorage.setItem(JSONBIN_BIN_KEY, binId); } catch(e) {}
      console.info('%c[RL Study] New bin created. Set JSONBIN_BIN_ID to: ' + binId,
        'color: #f97316; font-weight: bold; font-size: 14px;');
      showBinIdBanner(binId);
    }
  } catch(e) { console.warn('Cloud create failed:', e); }

  return cloudData;
}

function showBinIdBanner(id) {
  const banner = document.createElement('div');
  banner.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:9999;background:#f97316;color:#fff;padding:10px 16px;font-size:13px;font-family:monospace;text-align:center;cursor:pointer;';
  banner.innerHTML = `New cloud bin created. To sync across devices, set <b>JSONBIN_BIN_ID = '${id}'</b> in cloud.js then rebuild. <span style="text-decoration:underline">Click to copy &amp; dismiss.</span>`;
  banner.addEventListener('click', () => {
    navigator.clipboard.writeText(id).catch(() => {});
    banner.remove();
  });
  document.body.prepend(banner);
}

function syncToCloud() {
  if (!binId) return;
  clearTimeout(syncTimeout);
  syncTimeout = setTimeout(async () => {
    try {
      await fetch(`${JSONBIN_API_URL}/${binId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json', 'X-Master-Key': JSONBIN_API_KEY },
        body: JSON.stringify(cloudData)
      });
    } catch(e) { console.warn('Cloud sync failed:', e); }
  }, 1000);
}
