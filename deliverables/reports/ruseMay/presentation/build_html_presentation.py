"""Build the May 2026 Ruse University deck from HTML slide designs.

Pipeline:
1. Write one standalone 1920x1080 HTML file per slide.
2. Render each HTML slide to a 1920x1080 PNG with Playwright/Chromium.
3. Place each PNG full-bleed into a 16:9 PowerPoint deck.

This intentionally makes the PPTX non-editable at the element level. The
editable source of truth is the generated HTML/CSS in ``html_slides/``.
"""

from __future__ import annotations

import base64
import html
from pathlib import Path

from PIL import Image, ImageStat
from pptx import Presentation
from pptx.util import Inches


HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
LOGO = ASSETS / "ru-logo-125x140.png"

HTML_DIR = HERE / "html_slides"
PNG_DIR = HERE / "slide_images"
OUTPUT = HERE / "adaptive_strategy_ruse_may_html.pptx"

WIDTH = 1920
HEIGHT = 1080


def logo_data_uri() -> str:
    if not LOGO.exists():
        return ""
    data = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{data}"


LOGO_URI = logo_data_uri()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def footer(slide_no: int) -> str:
    return f"""
    <footer class="footer">
      <div class="footer-left">
        {'<img src="' + LOGO_URI + '" alt="Ruse University logo">' if LOGO_URI else ''}
        <span>Ruse University Academic Session &middot; May 2026</span>
      </div>
      <span class="slide-no">{slide_no:02d}</span>
    </footer>
    """


COMMON_CSS = """\
/* === 1. Design tokens === */
:root {
  --bg: #f7f8fb;
  --panel: #ffffff;
  --ink: #202832;
  --ink-soft: #56616e;
  --muted: #8b95a3;
  --rule: #d8dde5;
  --blue: #1f5f9f;
  --blue-soft: #dceaf7;
  --red: #c74432;
  --red-soft: #fae2dd;
  --teal: #178c7d;
  --teal-soft: #d9eee9;
  --amber: #bf821e;
  --shadow: 0 18px 44px rgba(31, 46, 64, 0.08);
}

/* === 2. Reset === */
* { box-sizing: border-box; }
html, body {
  margin: 0;
  width: 1920px;
  height: 1080px;
  overflow: hidden;
  background: var(--bg);
  color: var(--ink);
  font-family: Arial, Helvetica, sans-serif;
  letter-spacing: 0;
}
body { -webkit-font-smoothing: antialiased; }

/* === 3. Slide canvas === */
.slide {
  position: relative;
  width: 1920px;
  height: 1080px;
  padding: 82px 104px 104px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.86), rgba(247,248,251,0.98)),
    radial-gradient(circle at 91% 18%, rgba(31,95,159,0.08), transparent 25%),
    var(--bg);
}

/* === 4. Header & title rule === */
.slide-header { position: relative; height: 128px; }
h1 {
  margin: 0;
  font-size: 54px;
  line-height: 1.04;
  font-weight: 760;
  max-width: 1300px;
}
.title-rule {
  width: 92px;
  height: 8px;
  margin-top: 26px;
  border-radius: 999px;
  background: var(--ink);
}
.title-rule.blue  { background: var(--blue); }
.title-rule.red   { background: var(--red); }
.title-rule.teal  { background: var(--teal); }

/* === 5. Footer === */
.footer {
  position: absolute;
  left: 104px;
  right: 104px;
  bottom: 36px;
  height: 42px;
  border-top: 1.5px solid var(--rule);
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  color: var(--muted);
  font-size: 18px;
}
.footer-left { display: flex; align-items: center; gap: 14px; }
.footer img  { width: 30px; height: auto; display: block; }
.slide-no    { font-variant-numeric: tabular-nums; }

/* === 6. Typography === */
.eyebrow {
  margin-bottom: 16px;
  color: var(--muted);
  font-size: 18px;
  font-weight: 760;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.lead {
  color: var(--ink-soft);
  font-size: 29px;
  line-height: 1.35;
  margin: 0;
}
.caption {
  color: var(--muted);
  font-size: 22px;
  line-height: 1.35;
}
.big-statement {
  margin-top: 44px;
  font-size: 58px;
  line-height: 1.08;
  font-weight: 800;
  color: var(--red);
}

/* === 7. Layout grids === */
.grid-2 {
  display: grid;
  grid-template-columns: 0.98fr 1.02fr;
  gap: 72px;
  align-items: center;
  height: 760px;
}
.grid-2.narrow-left { grid-template-columns: 0.86fr 1.14fr; }
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 38px;
  margin-top: 44px;
}

/* === 8. Panel surface === */
.panel {
  background: rgba(255,255,255,0.76);
  border: 1.5px solid var(--rule);
  border-radius: 8px;
  box-shadow: var(--shadow);
}

/* === 9. Bullet list === */
.bullets {
  display: grid;
  gap: 34px;
  margin-top: 16px;
}
.bullet {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 22px;
  align-items: start;
}
.bullet i {
  width: 16px;
  height: 16px;
  margin-top: 13px;
  background: var(--blue);
  border-radius: 4px;
  display: block;
}
.bullet.red i  { background: var(--red); }
.bullet.teal i { background: var(--teal); }
.bullet strong {
  display: block;
  font-size: 35px;
  line-height: 1.12;
  margin-bottom: 8px;
}
.bullet span {
  display: block;
  color: var(--ink-soft);
  font-size: 24px;
  line-height: 1.24;
}

/* === 10. Tile grid & tiles === */
.tile-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  margin-top: 30px;
}
.tile-grid.two {
  grid-template-columns: repeat(2, 1fr);
  width: 1110px;
  margin-left: auto;
  margin-right: auto;
}
.tile {
  min-height: 240px;
  padding: 34px 34px 30px;
  display: grid;
  grid-template-columns: 108px 1fr;
  gap: 26px;
  align-items: center;
}
.icon {
  position: relative;
  width: 108px;
  height: 108px;
  border-radius: 8px;
  background: var(--blue-soft);
  color: var(--blue);
  display: grid;
  place-items: center;
  font-size: 48px;
  font-weight: 760;
}
.icon svg {
  width: 72px;
  height: 72px;
  stroke: currentColor;
  fill: none;
  stroke-width: 4;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.icon svg .fill   { fill: currentColor; stroke: none; }
.icon.red  { background: var(--red-soft);  color: var(--red); }
.icon.teal { background: var(--teal-soft); color: var(--teal); }
.tile h2 {
  margin: 0 0 10px;
  font-size: 31px;
  line-height: 1.1;
}
.tile p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 21px;
  line-height: 1.25;
}

/* === 11. Tag badge === */
.tag {
  display: inline-flex;
  align-items: center;
  min-height: 42px;
  padding: 0 20px;
  border-radius: 999px;
  background: white;
  border: 1.5px solid var(--rule);
  color: var(--ink-soft);
  font-size: 19px;
  font-weight: 700;
  white-space: nowrap;
}

/* === 12. Diagram primitives === */
.diagram {
  position: relative;
  min-height: 560px;
}
.node {
  position: absolute;
  width: 84px;
  height: 84px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: white;
  font-size: 30px;
  font-weight: 760;
  background: var(--blue);
  box-shadow: 0 10px 26px rgba(31, 95, 159, 0.22);
  z-index: 2;
}
.node.red  { background: var(--red);  box-shadow: 0 10px 26px rgba(199, 68, 50, 0.20); }
.node.teal { background: var(--teal); box-shadow: 0 10px 26px rgba(23, 140, 125, 0.18); }
.line {
  position: absolute;
  height: 4px;
  background: var(--rule);
  transform-origin: left center;
  border-radius: 999px;
  z-index: 1;
}
.line.blue { background: rgba(31,95,159,0.28); }
.line.red  { background: rgba(199,68,50,0.35); }
.arrow {
  position: absolute;
  height: 4px;
  background: var(--ink-soft);
  transform-origin: left center;
  border-radius: 999px;
}
.arrow::after {
  content: "";
  position: absolute;
  right: -3px;
  top: -8px;
  border-left: 18px solid var(--ink-soft);
  border-top: 10px solid transparent;
  border-bottom: 10px solid transparent;
}

/* === 13. Timeline === */
.timeline {
  position: relative;
  height: 590px;
  margin-top: 28px;
}
.timeline .axis {
  position: absolute;
  left: 60px;
  right: 60px;
  top: 292px;
  height: 5px;
  background: var(--ink-soft);
  border-radius: 999px;
}
.milestone {
  position: absolute;
  width: 250px;
  text-align: center;
}
.milestone .dot {
  position: absolute;
  left: 50%;
  width: 32px;
  height: 32px;
  margin-left: -16px;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: 0 0 0 10px rgba(31,95,159,0.10);
}
.milestone.top    .dot { top:  276px; }
.milestone.bottom .dot { top: -38px; }
.milestone h2 {
  margin: 0 0 8px;
  color: var(--blue);
  font-size: 24px;
}
.milestone strong {
  display: block;
  font-size: 31px;
  margin-bottom: 10px;
}
.milestone p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 19px;
  line-height: 1.25;
}

/* === 14. Policy box & opponents === */
.policy-box {
  position: absolute;
  background: white;
  border: 4px solid var(--ink);
  border-radius: 8px;
  padding: 28px;
  font-size: 33px;
  font-weight: 760;
  line-height: 1.14;
  text-align: center;
  box-shadow: var(--shadow);
}
.opponent {
  position: absolute;
  width: 450px;
  height: 116px;
  border-radius: 8px;
  border: 4px solid var(--blue);
  display: grid;
  place-items: center;
  color: var(--blue);
  background: white;
  font-size: 28px;
  font-weight: 760;
  box-shadow: var(--shadow);
}
.opponent.red   { border-color: var(--red);   color: var(--red); }
.opponent.amber { border-color: var(--amber); color: var(--amber); }

/* === 15. Numbered list === */
.numbered {
  display: grid;
  gap: 44px;
  margin-top: 44px;
}
.numbered .item {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 28px;
  align-items: center;
}
.num {
  width: 86px;
  height: 86px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: white;
  font-size: 38px;
  font-weight: 800;
  background: var(--blue);
}
.num.red  { background: var(--red); }
.num.teal { background: var(--teal); }
.numbered strong {
  display: block;
  font-size: 42px;
  line-height: 1.08;
}
.numbered span { color: var(--ink-soft); font-size: 25px; }

/* === 16. Process cards === */
.process {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
  align-items: stretch;
  margin-top: 52px;
}
.process-card {
  padding: 34px 32px;
  min-height: 210px;
  text-align: center;
}
.process-card h2 {
  margin: 0 0 12px;
  font-size: 31px;
}
.process-card p {
  margin: 0;
  color: var(--ink-soft);
  font-size: 21px;
  line-height: 1.28;
}

/* === 17. Slider === */
.slider {
  height: 360px;
  padding: 64px 54px;
}
.track {
  position: relative;
  height: 28px;
  margin: 90px 0 34px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--red-soft), var(--blue-soft));
}
.track::before {
  content: "";
  position: absolute;
  left: 35%;
  top: -26px;
  width: 42px;
  height: 80px;
  border-radius: 8px;
  background: var(--ink);
  box-shadow: 0 14px 28px rgba(32,40,50,0.22);
}
.track-labels {
  display: flex;
  justify-content: space-between;
  font-size: 29px;
  font-weight: 760;
}

/* === 18. Note === */
.note {
  padding: 34px 38px;
  font-size: 25px;
  line-height: 1.32;
  color: var(--ink-soft);
}

/* === 19. Stack / layer === */
.stack {
  width: 620px;
  margin: 46px auto 0;
  display: grid;
  gap: 16px;
}
.layer {
  min-height: 112px;
  padding: 22px 30px;
  border: 3px solid var(--teal);
  background: white;
}
.layer:nth-child(odd) { background: var(--teal-soft); }
.layer strong {
  display: block;
  font-size: 29px;
  margin-bottom: 8px;
}
.layer span { color: var(--teal); font-size: 22px; font-weight: 760; }

/* === 20. Outcome panels === */
.outcome {
  padding: 42px 44px;
  min-height: 548px;
}
.outcome h2 {
  margin: 0 0 8px;
  color: var(--blue);
  font-size: 22px;
  letter-spacing: 0.08em;
}
.outcome h3 {
  margin: 0 0 40px;
  font-size: 38px;
  line-height: 1.15;
}
.outcome ul {
  margin: 0;
  padding-left: 32px;
  color: var(--ink);
  font-size: 28px;
  line-height: 1.58;
}
.outcome.light h2           { color: var(--muted); }
.outcome.light h3,
.outcome.light ul           { color: var(--ink-soft); }
"""


def write_common_css() -> Path:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    path = HTML_DIR / "common.css"
    path.write_text(COMMON_CSS, encoding="utf-8")
    return path


def shell(title: str, body: str, *, slide_no: int | None, accent: str = "blue", title_slide: bool = False) -> str:
    cls = "slide title-slide" if title_slide else "slide"
    header = "" if title_slide else f"""
      <header class="slide-header">
        <h1>{esc(title)}</h1>
        <div class="title-rule {accent}"></div>
      </header>
    """
    foot = "" if slide_no is None else footer(slide_no)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width={WIDTH}, initial-scale=1">
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="common.css">
</head>
<body>
  <main class="{cls}">
    {header}
    {body}
    {foot}
  </main>
</body>
</html>
"""


def line(x1: int, y1: int, x2: int, y2: int, cls: str = "") -> str:
    import math

    length = math.hypot(x2 - x1, y2 - y1)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (
        f'<div class="line {cls}" style="left:{x1}px;top:{y1}px;'
        f'width:{length:.1f}px;transform:rotate({angle:.2f}deg)"></div>'
    )


def arrow(x1: int, y1: int, x2: int, y2: int) -> str:
    import math

    length = math.hypot(x2 - x1, y2 - y1)
    angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
    return (
        f'<div class="arrow" style="left:{x1}px;top:{y1}px;'
        f'width:{length:.1f}px;transform:rotate({angle:.2f}deg)"></div>'
    )


def svg_icon(kind: str) -> str:
    icons = {
        "market": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <path d="M14 64V18M14 64H68"/>
            <path d="M20 54L32 43L42 49L54 30L66 35"/>
            <path d="M58 30H68V40"/>
          </svg>
        """,
        "lock": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <rect x="18" y="34" width="44" height="32" rx="6"/>
            <path d="M28 34V25C28 15 35 9 40 9C45 9 52 15 52 25V34"/>
            <circle class="fill" cx="40" cy="50" r="4"/>
          </svg>
        """,
        "network": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <path d="M40 40L19 22M40 40L62 23M40 40L22 61M40 40L60 61"/>
            <circle cx="40" cy="40" r="8"/>
            <circle cx="19" cy="22" r="7"/>
            <circle cx="62" cy="23" r="7"/>
            <circle cx="22" cy="61" r="7"/>
            <circle cx="60" cy="61" r="7"/>
          </svg>
        """,
        "grid": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <path d="M16 16H64V64H16zM32 16V64M48 16V64M16 32H64M16 48H64"/>
            <circle class="fill" cx="24" cy="24" r="5"/>
            <circle class="fill" cx="56" cy="40" r="5"/>
          </svg>
        """,
        "cards": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <rect x="18" y="18" width="30" height="42" rx="5"/>
            <rect x="32" y="24" width="30" height="42" rx="5"/>
            <path d="M47 38C42 32 36 37 40 43C43 47 47 51 47 51C47 51 51 47 54 43C58 37 52 32 47 38Z"/>
          </svg>
        """,
        "gavel": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <path d="M18 58H54"/>
            <path d="M28 24L44 40M22 30L34 18M38 46L50 34"/>
            <path d="M46 42L64 60"/>
          </svg>
        """,
        "coalition": """
          <svg viewBox="0 0 80 80" aria-hidden="true">
            <path d="M22 24H58M22 24L18 58M58 24L62 58M18 58H62M22 24L62 58"/>
            <circle class="fill" cx="22" cy="24" r="6"/>
            <circle class="fill" cx="58" cy="24" r="6"/>
            <circle class="fill" cx="18" cy="58" r="6"/>
            <circle class="fill" cx="62" cy="58" r="6"/>
          </svg>
        """,
    }
    return icons[kind]


def slides() -> list[tuple[str, str]]:
    title_network = "\n".join(
        [
            line(1310, 210, 1440, 305, "blue"),
            line(1440, 305, 1580, 220, "blue"),
            line(1440, 305, 1400, 430, "blue"),
            line(1400, 430, 1540, 500, "blue"),
            line(1540, 500, 1370, 650, "blue"),
            line(1540, 500, 1660, 625, "blue"),
            line(1660, 625, 1740, 430, "blue"),
        ]
        + [
            f'<div class="node" style="left:{x}px;top:{y}px">{label}</div>'
            for x, y, label in [
                (1270, 170, "A"),
                (1400, 265, "?"),
                (1540, 180, "?"),
                (1360, 390, "?"),
                (1500, 460, "?"),
                (1330, 610, "?"),
                (1620, 585, "?"),
                (1700, 390, "?"),
            ]
        ]
    )
    s1 = shell(
        "Adaptive Strategy Learning",
        f"""
        <div style="position:absolute;left:104px;top:98px">
          {'<img src="' + LOGO_URI + '" alt="Ruse University logo" style="width:144px;height:auto">' if LOGO_URI else ''}
        </div>
        <section style="position:absolute;left:104px;top:330px;width:1050px">
          <h1 style="font-size:78px;line-height:1.02;margin:0 0 34px">
            Adaptive Strategy Learning<br>
            in Multi-Agent<br>
            Imperfect-Information Games
          </h1>
          <p style="margin:0;color:var(--blue);font-size:34px;font-style:italic">
            From Equilibrium Computation to Safe Opponent Exploitation
          </p>
          <div class="title-rule blue" style="margin-top:42px"></div>
          <p style="margin:54px 0 0;font-size:31px;font-weight:760">Alexander Andreev</p>
          <p style="margin:12px 0 0;color:var(--ink-soft);font-size:25px">
            PhD session report &middot; May 2026 &middot; Ruse University "Angel Kanchev"
          </p>
        </section>
        <div class="diagram" style="position:absolute;left:0;top:0;width:1920px;height:1080px">
          {title_network}
        </div>
        """,
        slide_no=None,
        title_slide=True,
    )

    # .diagram has position:relative, so all coordinates below are panel-relative.
    # Right panel is the .diagram.panel div, width ≈ 836px (1.02fr of 1640px), height = 620px.
    # Single-agent section: x 0–380. Divider at x=380. Multi-agent section: x 380–836.
    multi_lines = "\n".join(
        [
            line(472, 222, 632, 132, "red"),  # A → top-right
            line(472, 222, 352, 332, "red"),  # A → left
            line(472, 222, 682, 332, "red"),  # A → right
            line(632, 132, 682, 332, "red"),  # top-right → right
            line(352, 332, 502, 442, "red"),  # left → bottom
            line(682, 332, 502, 442, "red"),  # right → bottom
        ]
    )
    s2 = shell(
        "Why this matters now",
        f"""
        <section class="grid-2">
          <div class="bullets">
            <div class="bullet"><i></i><div><strong>Strong single agents</strong><span>well understood in constrained benchmarks</span></div></div>
            <div class="bullet"><i></i><div><strong>Agents interacting with other agents</strong><span>open problem</span></div></div>
            <div class="bullet red"><i></i><div><strong>Hidden information</strong><span>adversarial intent &middot; real-time decisions</span></div></div>
          </div>
          <div class="diagram panel" style="height:620px">
            <div class="tag" style="position:absolute;left:60px;top:50px">Single agent</div>
            <div class="node" style="left:148px;top:268px">A</div>
            <div style="position:absolute;left:380px;top:50px;width:2px;height:470px;background:var(--rule)"></div>
            <div class="tag" style="position:absolute;left:440px;top:50px">Multi-agent</div>
            {multi_lines}
            <div class="node" style="left:430px;top:180px">A</div>
            <div class="node red" style="left:590px;top:90px">?</div>
            <div class="node red" style="left:310px;top:290px">?</div>
            <div class="node" style="left:640px;top:290px">?</div>
            <div class="node red" style="left:460px;top:400px">?</div>
            <p class="caption" style="position:absolute;right:36px;bottom:36px;text-align:right">hidden &middot; possibly adversarial</p>
          </div>
        </section>
        """,
        slide_no=2,
        accent="blue",
    )

    use_tiles = [
        ("Financial markets", "hidden positions &middot; microsecond reactions", svg_icon("market"), ""),
        ("Cybersecurity", "adaptive attackers &middot; hidden intent", svg_icon("lock"), "red"),
        ("Social platforms", "bot networks &middot; coordinated disinformation", svg_icon("network"), ""),
        ("Security", "patrol and screening randomisation", svg_icon("grid"), "teal"),
        ("Gaming platforms", "collusion &middot; fraud detection", svg_icon("cards"), "red"),
    ]
    tile_html = "".join(
        f"""
        <article class="tile panel">
          <div class="icon {color}">{icon}</div>
          <div><h2>{title}</h2><p>{sub}</p></div>
        </article>
        """
        for title, sub, icon, color in use_tiles[:3]
    )
    tile_html_2 = "".join(
        f"""
        <article class="tile panel">
          <div class="icon {color}">{icon}</div>
          <div><h2>{title}</h2><p>{sub}</p></div>
        </article>
        """
        for title, sub, icon, color in use_tiles[3:]
    )
    s3 = shell(
        "Where this shows up",
        f"""
        <section class="tile-grid">{tile_html}</section>
        <section class="tile-grid two" style="margin-top:28px">{tile_html_2}</section>
        """,
        slide_no=3,
        accent="blue",
    )

    testbeds = [
        ("Poker / Belot-like", "hidden cards &middot; inference", svg_icon("cards")),
        ("Auction-style", "hidden valuations &middot; bidding", svg_icon("gavel")),
        ("Pursuit-evasion", "partial observability &middot; adversarial search", svg_icon("grid")),
        ("Coalition games", "alliances &middot; betrayal &middot; N-player incentives", svg_icon("coalition")),
    ]
    s4 = shell(
        "Why study games?",
        f"""
        <p class="lead" style="margin-top:12px">Controlled environments where strategic behaviour is testable.</p>
        <section class="tile-grid" style="grid-template-columns:repeat(4,1fr);gap:24px;margin-top:58px">
          {''.join(f'<article class="tile panel" style="grid-template-columns:1fr;min-height:530px;text-align:center"><div class="icon" style="margin:18px auto 42px">{icon}</div><h2>{title}</h2><p>{sub}</p></article>' for title, sub, icon in testbeds)}
        </section>
        <p class="caption" style="position:absolute;left:104px;right:104px;bottom:104px;text-align:center">
          Validation environments, not the final application domains.
        </p>
        """,
        slide_no=4,
        accent="blue",
    )

    milestones = [
        ("2007", "CFR", "regret minimisation<br>in imperfect-info games", 70, "top"),
        ("2017", "Libratus", "2-player poker<br>superhuman", 420, "bottom"),
        ("2019", "Pluribus", "6-player poker<br>superhuman", 770, "top"),
        ("2020", "ReBeL", "search + RL<br>in imperfect-info", 1120, "bottom"),
        ("2022", "DeepNash / CICERO", "Stratego &middot; Diplomacy<br>7 players, coalitions", 1470, "top"),
    ]
    m_html = "".join(
        f"""
        <div class="milestone {pos}" style="left:{x}px;top:{70 if pos == 'top' else 338}px">
          <div class="dot"></div><h2>{year}</h2><strong>{name}</strong><p>{sub}</p>
        </div>
        """
        for year, name, sub, x, pos in milestones
    )
    s5 = shell(
        "State of the art",
        f"""
        <p class="lead" style="margin-top:8px">"Superhuman" in progressively larger games.</p>
        <section class="timeline">
          <div class="axis"></div>
          {m_html}
        </section>
        """,
        slide_no=5,
        accent="blue",
    )

    s6 = shell(
        "The limitation",
        f"""
        <section class="diagram" style="height:700px">
          <div class="big-statement">Fixed strategies. No adaptation.</div>
          <p class="lead" style="margin-top:20px">The same policy against every opponent.</p>
          <div class="policy-box" style="left:160px;top:370px;width:360px;height:150px">Equilibrium<br>policy</div>
          <div class="opponent" style="left:1120px;top:300px">Cautious beginner</div>
          <div class="opponent red" style="left:1120px;top:466px">Aggressive bluffer</div>
          <div class="opponent amber" style="left:1120px;top:632px">Coordinated group</div>
          {arrow(520,445,1120,358)}
          {arrow(520,445,1120,524)}
          {arrow(520,445,1120,690)}
          <p class="caption" style="position:absolute;left:0;right:0;bottom:110px">Safe, but blind. Systematically misses exploitable weaknesses.</p>
        </section>
        """,
        slide_no=6,
        accent="red",
    )

    # .diagram has position:relative, so all coordinates are panel-relative.
    # Right panel width ≈ 935px (1.14fr of 1640px), height = 650px.
    # Nodes are 160×160; centres = left+80, top+80.
    tri = "\n".join(
        [
            arrow(519, 211, 678, 399),   # Adaptation edge → Safety edge
            arrow(650, 460, 270, 460),   # Safety edge → Evaluation edge
            arrow(242, 400, 415, 210),   # Evaluation edge → Adaptation edge
            '<div class="node" style="left:387px;top:70px;width:160px;height:160px;font-size:23px">Adaptation</div>',
            '<div class="node red" style="left:650px;top:380px;width:160px;height:160px;font-size:25px">Safety</div>',
            '<div class="node teal" style="left:110px;top:380px;width:160px;height:160px;font-size:22px">Evaluation</div>',
        ]
    )
    s7 = shell(
        "Three open problems",
        f"""
        <section class="grid-2 narrow-left">
          <div class="numbered">
            <div class="item"><div class="num">1</div><div><strong style="color:var(--blue)">Adaptation</strong><span>infer opponents in real time</span></div></div>
            <div class="item"><div class="num red">2</div><div><strong style="color:var(--red)">Safety</strong><span>exploit without exposing yourself</span></div></div>
            <div class="item"><div class="num teal">3</div><div><strong style="color:var(--teal)">Evaluation</strong><span>measure if an agent adapts well</span></div></div>
          </div>
          <div class="diagram panel" style="height:650px">{tri}<p class="caption" style="position:absolute;left:0;right:0;bottom:36px;text-align:center">inference &rarr; action &rarr; measurement</p></div>
        </section>
        """,
        slide_no=7,
        accent="",
    )

    s8 = shell(
        "Behavioral Adaptation Framework",
        f"""
        <div class="eyebrow" style="color:var(--blue)">Contribution 1</div>
        <section class="grid-2 narrow-left" style="margin-top:-30px">
          <div class="bullets">
            <div class="bullet"><i></i><div><strong>Infer opponent type</strong><span>not just hidden state</span></div></div>
            <div class="bullet"><i></i><div><strong>Adapt only when evidence is strong enough</strong><span>fallback to equilibrium</span></div></div>
            <div class="bullet"><i></i><div><strong>Detect anomalies</strong><span>bots &middot; collusion &middot; adversarial users</span></div></div>
          </div>
          <div>
            <section class="process">
              <article class="process-card panel"><h2>Observed actions</h2><p>sequence of strategic behaviour</p></article>
              <article class="process-card panel"><h2>Beliefs</h2><p>hidden state + behavioural type</p></article>
              <article class="process-card panel"><h2>Decision</h2><p>adaptive policy, or equilibrium fallback</p></article>
            </section>
            <div class="note panel" style="margin-top:44px;border-color:var(--blue)">
              Weak evidence keeps the agent near equilibrium play. Strong evidence opens the adaptation path.
            </div>
          </div>
        </section>
        """,
        slide_no=8,
        accent="blue",
    )

    s9 = shell(
        "Multi-Agent Safe Exploitation",
        """
        <div class="eyebrow" style="color:var(--red)">Contribution 2</div>
        <section class="grid-2 narrow-left" style="margin-top:-30px">
          <div class="bullets">
            <div class="bullet red"><i></i><div><strong>Exploit detected weaknesses</strong><span>act on the inferred type</span></div></div>
            <div class="bullet red"><i></i><div><strong>Stay close to a reference policy</strong><span>pi_KL regularisation</span></div></div>
            <div class="bullet red"><i></i><div><strong>Useful safety heuristics</strong><span>beyond two-player guarantees</span></div></div>
          </div>
          <div>
            <section class="slider panel">
              <div class="track-labels"><span style="color:var(--red)">Exploit</span><span style="color:var(--blue)">Reference policy</span></div>
              <div class="track"></div>
              <p class="caption" style="text-align:center">constrained by pi_KL band around reference</p>
            </section>
            <div class="note panel" style="margin-top:34px;border-color:var(--red)">
              Two-player safety guarantees provably fail at N >= 3. The target is practical, characterised safety behaviour in larger games.
            </div>
          </div>
        </section>
        """,
        slide_no=9,
        accent="red",
    )

    s10 = shell(
        "Evaluation Methodology",
        """
        <div class="eyebrow" style="color:var(--teal)">Contribution 3</div>
        <section class="grid-2 narrow-left" style="margin-top:-30px">
          <div class="bullets">
            <div class="bullet teal"><i></i><div><strong>Safety</strong><span>worst-case vulnerability</span></div></div>
            <div class="bullet teal"><i></i><div><strong>Population ranking</strong><span>non-transitive dynamics</span></div></div>
            <div class="bullet teal"><i></i><div><strong>Statistical reliability</strong><span>variance reduction</span></div></div>
          </div>
          <div>
            <section class="stack">
              <article class="layer panel"><strong>Safety</strong><span>N-player exploitability</span></article>
              <article class="layer panel"><strong>Population ranking</strong><span>alpha-Rank &middot; R/P/S cycles</span></article>
              <article class="layer panel"><strong>Statistical reliability</strong><span>AIVAT variance reduction</span></article>
            </section>
            <p class="caption" style="text-align:center;margin-top:36px">validated across structurally different game types</p>
          </div>
        </section>
        """,
        slide_no=10,
        accent="teal",
    )

    s11 = shell(
        "Expected outcomes",
        """
        <section class="columns">
          <article class="outcome panel" style="border-color:var(--blue);border-width:3px">
            <h2>REALISTIC TARGET</h2>
            <h3>What the thesis will deliver</h3>
            <ul>
              <li>Validated adaptation methods</li>
              <li>Characterised safety heuristics</li>
              <li>Working evaluation framework</li>
              <li>Failure modes documented</li>
            </ul>
          </article>
          <article class="outcome panel light">
            <h2>STRETCH DIRECTION</h2>
            <h3>If the work goes deeper</h3>
            <ul>
              <li>Theoretical extensions of the safety theorem</li>
              <li>Novel combinations across contributions</li>
              <li>Surprising empirical results</li>
            </ul>
          </article>
        </section>
        <p class="caption" style="position:absolute;left:104px;right:104px;bottom:110px;text-align:center">
          Grounded outcomes already constitute a coherent thesis. No pivot required.
        </p>
        """,
        slide_no=11,
        accent="",
    )

    s12 = shell(
        "Today to Tomorrow",
        f"""
        <p class="lead" style="margin-top:10px">The gap between today's deployed systems and the next generation.</p>
        <section class="columns" style="align-items:center;margin-top:78px">
          <article class="outcome panel light" style="min-height:390px">
            <h2>TODAY</h2>
            <h3>Fixed-strategy systems</h3>
            <ul>
              <li>Equilibrium solvers</li>
              <li>Identical play vs. every opponent</li>
              <li>Two-player safety guarantees</li>
            </ul>
          </article>
          <article class="outcome panel" style="min-height:390px;border-color:var(--blue);border-width:3px">
            <h2>NEXT GENERATION</h2>
            <h3>Adaptive, safe, accountable agents</h3>
            <ul>
              <li>Adaptation</li>
              <li>Safety beyond two players</li>
              <li>Systematic evaluation</li>
            </ul>
          </article>
        </section>
        <div style="position:absolute;left:895px;top:560px;width:130px;text-align:center;color:var(--muted);font-size:20px">thesis</div>
        {arrow(820,540,1100,540)}
        <p style="position:absolute;left:104px;right:104px;bottom:110px;text-align:center;font-size:36px;font-weight:760">Thank you. Questions welcome.</p>
        """,
        slide_no=12,
        accent="",
    )

    return [
        ("slide_01_title.html", s1),
        ("slide_02_why_now.html", s2),
        ("slide_03_use_cases.html", s3),
        ("slide_04_games.html", s4),
        ("slide_05_state_of_art.html", s5),
        ("slide_06_limitation.html", s6),
        ("slide_07_open_problems.html", s7),
        ("slide_08_contribution_1.html", s8),
        ("slide_09_contribution_2.html", s9),
        ("slide_10_contribution_3.html", s10),
        ("slide_11_outcomes.html", s11),
        ("slide_12_close.html", s12),
    ]


def write_html_files() -> list[Path]:
    write_common_css()
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    paths = []
    for filename, content in slides():
        path = HTML_DIR / filename
        path.write_text(content, encoding="utf-8")
        paths.append(path)
    return paths


def render_pngs(html_paths: list[Path]) -> list[Path]:
    from playwright.sync_api import sync_playwright

    PNG_DIR.mkdir(parents=True, exist_ok=True)
    png_paths: list[Path] = []
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": HEIGHT}, device_scale_factor=2)
        for index, html_path in enumerate(html_paths, start=1):
            png_path = PNG_DIR / f"slide_{index:02d}.png"
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle")
            page.screenshot(path=str(png_path), full_page=False)
            png_paths.append(png_path)
        browser.close()
    return png_paths


def verify_pngs(png_paths: list[Path]) -> None:
    expected = (WIDTH * 2, HEIGHT * 2)  # device_scale_factor=2 doubles pixel dimensions
    for path in png_paths:
        with Image.open(path) as image:
            if image.size != expected:
                raise RuntimeError(f"{path} has size {image.size}, expected {expected}")
            stat = ImageStat.Stat(image.convert("L"))
            if stat.stddev[0] < 2.0:
                raise RuntimeError(f"{path} appears blank or nearly blank")


def build_pptx(png_paths: list[Path]) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for path in png_paths:
        slide = prs.slides.add_slide(blank)
        slide.shapes.add_picture(str(path), 0, 0, width=prs.slide_width, height=prs.slide_height)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUTPUT)


def build() -> None:
    html_paths = write_html_files()
    png_paths = render_pngs(html_paths)
    verify_pngs(png_paths)
    build_pptx(png_paths)
    print(f"Wrote {len(html_paths)} HTML slides to {HTML_DIR}")
    print(f"Wrote {len(png_paths)} PNG slides to {PNG_DIR}")
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    build()
