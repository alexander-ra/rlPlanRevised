// Render every slide of the deck as the presenter sees it when stepping forward, at 1920x1080:
// the transition from the previous slide, the slide's own run, and for slides that keep moving one loop.
// Writes lossless RGB intermediates (raw/<id>.mkv), poster PNGs and plan.json; encode_videos.py makes the MP4s.
// Usage: node render_videos.js <deck.html> <outdir> [workers] [ids,...]
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const [DECK, OUT, WORKERS = '3', ONLY = ''] = process.argv.slice(2);
const FPS = 30, XF = 0.6;                     // crossfade at the loop seam, seconds
// Loop lengths (s). Exact where the slide repeats; elsewhere a length that keeps the main tokens in step,
// and the crossfade hides the rest (network streams are randomised per message and never repeat).
const LOOP = { F5a: 2.6, F7a: 32.671, F7b: 30.7, F7c: 14.387, F8: 11.962, F9: 35.933, R5a: 41.892, R5b: 47.292, END: 8.6,
  N1: 30, N2: 30, R0: 30, N3: 32.542, R4: 30.762, R1: 33.75, R2: 33.078, R3: 29.86, R6: 29.4 };
const log = (...a) => { const s = a.join(' '); console.log(s); fs.appendFileSync(path.join(OUT, 'render.log'), s + '\n'); };
async function openPage(b) {
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  p.on('pageerror', e => log('PAGEERROR', String(e)));
  await p.goto('file://' + DECK + '?frame=F1'); await p.waitForFunction(() => window.__ready, null, { timeout: 30000 });
  await p.evaluate(() => document.fonts.ready);
  return p;
}
(async () => {
  fs.mkdirSync(path.join(OUT, 'raw'), { recursive: true }); fs.mkdirSync(path.join(OUT, 'poster'), { recursive: true });
  const b = await chromium.launch();
  const p0 = await openPage(b);
  // which slides keep moving once their run has finished
  const info = await p0.evaluate(() => ORDER.map(id => {
    const F = FRAMES[id], rl = runLen(F);
    let moves = !F.still;
    if (moves) { const B = rl + 1, v = c => { AMB = 50 + c; const w = stillView(id, c, true); return JSON.stringify([w.dots.map(d => [Math.round(d.x), Math.round(d.y), +(d.a || 0).toFixed(2)]), w.els.map(e => JSON.stringify(e, (k, x) => typeof x === 'function' ? undefined : x))]); };
      const base = v(B); moves = [0.1, 0.3, 0.5, 0.9, 1.3, 1.7, 2.3].some(x => v(B + x) !== base); }
    return { id, title: (NOTES[id] || {}).t || id, runLen: rl, moves, D };
  }));
  let Abase = 50, prev = null;
  const plan = info.map((s, i) => {
    const Dd = i === 0 ? 0 : s.D, loop = s.moves;
    if (loop && !LOOP[s.id]) throw new Error('no loop length for ' + s.id);
    const endClock = loop ? s.runLen + 1 : s.runLen + 0.3;
    const nEnd = Math.round((Dd + endClock) * FPS);                 // V1 is frames 0..nEnd; its last frame is the loop's first
    const nP = loop ? Math.round(LOOP[s.id] * FPS) : 0, nX = loop ? Math.round(XF * FPS) : 0;
    const r = { i, id: s.id, title: s.title, prev: prev && prev.id, Dd, loop, nEnd, nP, nX, Abase,
      cA: prev ? prev.endClockQ : 0, endClockQ: nEnd / FPS - Dd, frames: nEnd + 1 + (loop ? nP : 0), fps: FPS };
    Abase += nEnd / FPS; prev = r; return r;
  });
  fs.writeFileSync(path.join(OUT, 'plan.json'), JSON.stringify(plan, null, 1));
  log('plan', plan.map(r => `${r.id}:${r.loop ? 'loop' : 'still'}:${r.frames}`).join(' '), 'total frames', plan.reduce((a, r) => a + r.frames, 0));
  await p0.close();
  const queue = plan.filter(r => !ONLY || ONLY.split(',').includes(r.id)).sort((a, b) => b.frames - a.frames);
  const worker = async w => {
    const p = await openPage(b), cdp = await p.context().newCDPSession(p);
    while (queue.length) {
      const r = queue.shift(), t0 = Date.now();
      const raw = path.join(OUT, 'raw', r.id + '.mkv');
      const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'png', '-framerate', String(FPS), '-i', '-',
        '-c:v', 'libx264rgb', '-qp', '0', '-preset', 'ultrafast', raw]);
      let ffErr = ''; ff.stderr.on('data', d => { ffErr += d; });
      for (let k = 0; k < r.frames; k++) {
        await p.evaluate(({ r, tau }) => new Promise(res => {
          AMB = r.Abase + tau;
          draw(tau < r.Dd ? transView(r.prev, r.id, tau / r.Dd, r.cA, true) : stillView(r.id, tau - r.Dd, true));
          requestAnimationFrame(() => res());
        }), { r, tau: k / FPS });
        const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true });
        const buf = Buffer.from(data, 'base64');
        if (k === 0) fs.writeFileSync(path.join(OUT, 'poster', r.id + '_a.png'), buf);
        if (k === r.nEnd) fs.writeFileSync(path.join(OUT, 'poster', r.id + '_end.png'), buf);
        if (!ff.stdin.write(buf)) await new Promise(res => ff.stdin.once('drain', res));
      }
      ff.stdin.end(); const code = await new Promise(res => ff.on('close', res));
      log(`w${w} ${r.id} ${r.frames} frames ${((Date.now() - t0) / 1000).toFixed(0)} s ffmpeg=${code} ${ffErr.trim()}`);
    }
    await p.close();
  };
  await Promise.all(Array.from({ length: +WORKERS }, (_, w) => worker(w)));
  log('done');
  await b.close();
})().catch(e => { log('FATAL', e.stack || e); process.exit(1); });
