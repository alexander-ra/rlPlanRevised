/* ===== YouTube Thumbnails ===== */
function embedYouTubeThumbnails() {
  const contentEl = document.getElementById('content');
  contentEl.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href');
    let videoId = null;
    try {
      const url = new URL(href);
      if (url.hostname.includes('youtube.com') && url.searchParams.get('v')) {
        videoId = url.searchParams.get('v');
      } else if (url.hostname === 'youtu.be') {
        videoId = url.pathname.slice(1);
      }
    } catch(e) {}
    if (!videoId) return;
    if (a.classList.contains('yt-card')) return;

    const title = a.textContent.trim();

    const card = document.createElement('a');
    card.href = href;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.className = 'yt-card';
    card.setAttribute('aria-label', title);

    const thumbWrap = document.createElement('div');
    thumbWrap.className = 'yt-thumb-wrap';

    const img = document.createElement('img');
    img.src = `https://img.youtube.com/vi/${encodeURIComponent(videoId)}/mqdefault.jpg`;
    img.alt = title;
    img.className = 'yt-thumb';
    img.loading = 'lazy';

    const play = document.createElement('span');
    play.className = 'yt-play';
    play.setAttribute('aria-hidden', 'true');
    play.textContent = '\u25B6';

    thumbWrap.appendChild(img);
    thumbWrap.appendChild(play);

    const label = document.createElement('div');
    label.className = 'yt-title';
    label.textContent = title;

    card.appendChild(thumbWrap);
    card.appendChild(label);

    a.parentNode.replaceChild(card, a);

    // Extract Duration / Channel / Instructor from next sibling text node
    let node = card.nextSibling;
    for (let i = 0; i < 6 && node; i++, node = node.nextSibling) {
      if (node.nodeType === 3) {
        const text = node.textContent.replace(/\s+/g, ' ').trim();
        if (text.startsWith('Duration:') || text.startsWith('\u23F1')) {
          let duration = null, channel = null;
          if (text.startsWith('\u23F1')) {
            // Format: ⏱ ~12m · Channel: CrashCourse  (middle dot U+00B7)
            const parts = text.split(' \u00B7 ');
            duration = parts[0].replace('\u23F1', '').trim();
            const chanPart = parts[1] || '';
            const chanM = chanPart.match(/(?:Channel|Канал|Instructor):\s*(.+)/);
            if (chanM) channel = chanM[1].trim();
          } else {
            // Legacy format: Duration: 12m | Channel: X
            const durM = text.match(/Duration:\s*([^|]+)/);
            const chanM = text.match(/(?:Channel|Instructor):\s*(.+)/);
            if (durM) duration = durM[1].trim();
            if (chanM) channel = chanM[1].trim();
          }
          if (duration) {
            const dur = document.createElement('span');
            dur.className = 'yt-duration';
            dur.textContent = duration;
            thumbWrap.appendChild(dur);
          }
          if (channel) {
            const chan = document.createElement('div');
            chan.className = 'yt-channel';
            chan.textContent = channel;
            card.appendChild(chan);
          }
          break;
        }
      }
    }
  });
}
