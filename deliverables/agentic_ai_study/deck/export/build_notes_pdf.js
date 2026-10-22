// Build the printable speaker notes (A4): one block per slide, never split across pages, with the
// slide as it looks when settled, 2-3 cue words, the notes, and the time the slide took in the
// last rehearsal and where in the talk it starts. Notes come from the deck's NOTES; cue words and
// times from notes_cues_bg.json.
// Usage: node build_notes_pdf.js ../index.html notes_cues_bg.json ../notes_bg.pdf
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const [DECK, CUES, OUT] = process.argv.slice(2).map(p => path.resolve(p));

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const mmss = s => { s = Math.round(s); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };

const CSS = `
  @page { size: A4; margin: 12mm 14mm 15mm; }
  :root { --ink: #14202b; --ink2: #4a5866; --line: #b9c3cc; --soft: #eef1f4; }
  * { box-sizing: border-box; }
  body { margin: 0; color: var(--ink); font: 12.5pt/1.45 "Roboto Flex", Arial, sans-serif; }
  .doc { display: flex; justify-content: space-between; align-items: flex-end; gap: 8mm;
         border-bottom: 0.6mm solid var(--ink); padding-bottom: 3mm; margin-bottom: 5mm; }
  .doc h1 { margin: 0; font: 800 17pt/1.2 "Roboto Flex", Arial, sans-serif; text-wrap: balance; }
  .doc .meta { font-size: 9.5pt; color: var(--ink2); text-align: right; white-space: nowrap; }
  .slide { break-inside: avoid; border-top: 1mm solid var(--ink); padding-top: 2.2mm; margin-bottom: 6mm; }
  .head { display: flex; align-items: baseline; gap: 3mm; }
  .num { font: 800 21pt/1 "Roboto Flex", Arial, sans-serif; font-variant-numeric: tabular-nums; min-width: 9mm; }
  .id { font: 700 10.5pt/1 "Roboto Flex", Arial, sans-serif; color: var(--ink2); letter-spacing: .03em; }
  .title { flex: 1; font: 800 14pt/1.2 "Roboto Flex", Arial, sans-serif; }
  .time { font-size: 9.5pt; color: var(--ink2); text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums; }
  .time b { color: var(--ink); }
  .body { display: grid; grid-template-columns: 56mm minmax(0, 1fr); gap: 5mm; margin-top: 2.5mm; }
  .side img { width: 56mm; display: block; border: 0.25mm solid var(--line); }
  .cues { display: flex; flex-direction: column; gap: 1.6mm; margin-top: 2.6mm; }
  .cue { font: 750 12.5pt/1.2 "Roboto Flex", Arial, sans-serif; background: var(--soft); border: 0.25mm solid var(--line);
         border-radius: 1.2mm; padding: 1.1mm 2.2mm; }
  .text p { margin: 0 0 2.2mm; }
  .text p:last-child { margin-bottom: 0; }
`;

(async () => {
  const html = fs.readFileSync(DECK, 'utf8');
  const NOTES = JSON.parse(html.match(/const NOTES = (\{.*?\});\n/)[1]);
  const ORDER = JSON.parse(html.match(/const ORDER = (\[.*?\]);/)[1].replace(/'/g, '"'));
  const title = html.match(/<title>(.*?)<\/title>/)[1];
  const { run, slides } = JSON.parse(fs.readFileSync(CUES, 'utf8'));
  const b = await chromium.launch();

  // each slide as it looks once settled, from the deck's own ?frame= hook
  const shooter = await b.newPage({ viewport: { width: 960, height: 540 } });
  const thumbs = {};
  for (const id of ORDER) {
    await shooter.goto('file://' + DECK + '?frame=' + id);
    await shooter.waitForFunction(() => window.__ready, null, { timeout: 30000 });
    thumbs[id] = (await shooter.screenshot({ type: 'jpeg', quality: 90 })).toString('base64');
  }

  let at = 0;
  const blocks = ORDER.map((id, i) => {
    const s = slides[id] || { cues: [], secs: 0 }, n = NOTES[id] || { t: id, p: [] };
    const time = s.secs ? `начало <b>${mmss(at)}</b><br>≈ ${mmss(s.secs)}` : `начало <b>${mmss(at)}</b>`;
    at += s.secs;
    return `<section class="slide">
      <div class="head"><span class="num">${i + 1}</span><span class="id">${esc(id)}</span>
        <span class="title">${esc(n.t)}</span><span class="time">${time}</span></div>
      <div class="body">
        <div class="side"><img src="data:image/jpeg;base64,${thumbs[id]}" alt="">
          <div class="cues">${s.cues.map(c => `<div class="cue">${esc(c)}</div>`).join('')}</div></div>
        <div class="text">${n.p.map(p => `<p>${esc(p)}</p>`).join('')}</div>
      </div></section>`;
  }).join('');
  const page = `<!doctype html><html lang="bg"><head><meta charset="utf-8">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto+Flex:opsz,wdth,wght@8..144,25..151,100..1000&display=swap">
    <style>${CSS}</style></head><body>
    <header class="doc"><h1>${esc(title)}<br>Бележки на говорещия</h1>
      <div class="meta">24 октомври 2026<br>${ORDER.length} слайда · времена: ${esc(run)}</div></header>
    ${blocks}</body></html>`;

  const p = await b.newPage();
  await p.setContent(page, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: OUT, format: 'A4', printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="width:100%;font:8pt Arial,sans-serif;color:#4a5866;padding:0 14mm;display:flex;justify-content:space-between">
      <span>Бележки · ${esc(title)}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>` });
  console.log(`${OUT}: ${(fs.statSync(OUT).size / 1e6).toFixed(1)} MB`);
  await b.close();
})();
