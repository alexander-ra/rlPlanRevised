# Exports of the BG deck

## Single HTML file for presenting

`../presentation_bg.html` (about 550 KB) is `../index.html` built for the talk:

- **Self-contained.** The fonts are embedded and cut down to the characters the deck uses. It makes no network requests, so it works offline on any machine with a current browser. Every slide renders pixel for pixel as in `index.html`.
- **Presenting.** F or "Цял екран" opens fullscreen: the slide alone on black, filling a 16:9 screen, with the screen kept awake and the pointer hidden when idle. B or . blanks the screen (what clickers send), and any key brings it back. Esc leaves fullscreen.
- **Read-only notes.** N shows the notes beside the slide outside fullscreen. Rehearsal recording and note editing stay in `index.html`.
- **Minified** with esbuild.

Rebuild after any change to `index.html` (needs fonttools with brotli, and npx; about 10 s):

```bash
python3 build_html.py ../index.html ../presentation_bg.html
```

## PowerPoint

`../presentation_bg.pptx` is `../index.html` as PowerPoint: one full-screen 1920×1080 video per slide, speaker notes from the deck.

### How a slide plays

- The video starts on the previous slide's last frame, plays the transition and the slide's own animation, and rests on its last frame. So moving forward looks like the HTML deck.
- Slides that keep moving (F5a, F7a–F9, N1–N3, R0–R6, R5a/b, END) then hand over to a second, looping video underneath. Most loops repeat exactly. The network slides (N1–N3, R0–R4) carry randomised message streams, and R6's dots drift at unrelated speeds, so these never repeat; their 29–34 s loops crossfade over the last 0.6 s.
- Videos start on their own. The play bar is switched off for the whole file. A transparent shape on top takes the clicks, so a click advances the slide instead of pausing the video.
- Each slide's title sits just above the slide, outside the shown area, so the outline and "go to slide" name every slide.

Known limits:

- Thumbnails and the editor show each slide's first frame, which is the previous slide's ending.
- Going back (←) replays the transition into the slide forwards, not in reverse.

### Rebuilding

Needs Node with Playwright (Chromium), ffmpeg, and Python with python-pptx, lxml and Pillow. Takes about 30 minutes, mostly rendering.

```bash
OUT=/tmp/deck_export
node render_videos.js "$PWD/../index.html" $OUT 3     # frames → lossless intermediates, posters, plan.json
python3 encode_videos.py $OUT 22                      # H.264 MP4s (CRF 22)
python3 build_pptx.py ../index.html $OUT ../presentation_bg.pptx
```

Keep the .pptx under 100 MB (GitHub's file limit). A higher CRF makes it smaller.
