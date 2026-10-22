"""Build presentation_bg.html: the deck as one self-contained, minified file for presenting.

- Fonts: the Google Fonts faces the deck links to, cut down to the characters the deck
  uses (variable axes and OpenType features kept) and embedded, so it needs no network.
  Renders match index.html pixel for pixel.
- PROD on: notes read-only, no rehearsal recording, nothing stored.
- CSS and JS minified with esbuild (fetched by npx).

Usage: python3 build_html.py ../index.html ../presentation_bg.html
"""
import base64
import hashlib
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

from fontTools import subset

SRC, DST = Path(sys.argv[1]), Path(sys.argv[2])
CACHE = Path("/tmp/deck_font_cache")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
ESBUILD = ["npx", "--yes", "esbuild@0.24.0", "--minify", "--log-level=warning"]
# Faces never reached: Roboto Flex has every character the deck uses, so its fallback is left out
# (renders stay pixel-identical). Narrowing Roboto Flex's axes would save ~60 KB but shifts outlines.
SKIP = {"Golos Text"}


def fetch(url):
    CACHE.mkdir(exist_ok=True)
    path = CACHE / hashlib.sha1(url.encode()).hexdigest()
    if not path.exists():
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        path.write_bytes(urllib.request.urlopen(req, timeout=60).read())
    return path


def codepoints(ranges):
    out = set()
    for part in ranges.split(","):
        part = part.strip()[2:]                      # drop "U+"
        lo, _, hi = part.partition("-")
        if "?" in lo:
            lo, hi = lo.replace("?", "0"), lo.replace("?", "F")
        out.update(range(int(lo, 16), int(hi or lo, 16) + 1))
    return out


def embedded_fonts(css_url, chars):
    """@font-face rules with each face that covers a character of the deck, subset and inlined."""
    css = fetch(css_url).read_text()
    rules, total = [], 0
    for block in re.findall(r"@font-face\s*\{([^}]*)\}", css):
        decl = dict(re.findall(r"([\w-]+):\s*([^;]+);", block))
        family = decl["font-family"].strip("'\"")
        need = chars & codepoints(decl["unicode-range"])
        if not need or family in SKIP:
            continue
        url = re.search(r"url\(([^)]+)\)", decl["src"]).group(1)
        opts = subset.Options()
        opts.flavor, opts.layout_features, opts.name_IDs, opts.notdef_outline = "woff2", ["*"], ["*"], True
        font = subset.load_font(str(fetch(url)), opts)
        sub = subset.Subsetter(opts)
        sub.populate(unicodes=need)
        sub.subset(font)
        out = CACHE / "subset.woff2"
        subset.save_font(font, str(out), opts)
        data = out.read_bytes()
        total += len(data)
        desc = "".join(f"{k}:{decl[k]};" for k in ("font-family", "font-style", "font-weight", "font-stretch") if k in decl)
        rules.append(f"@font-face{{{desc}font-display:block;"
                     f"src:url(data:font/woff2;base64,{base64.b64encode(data).decode()}) format('woff2');"
                     f"unicode-range:{decl['unicode-range']};}}")
    return "".join(rules), total


def esbuild(code, loader):
    r = subprocess.run(ESBUILD + [f"--loader={loader}"], input=code, capture_output=True, text=True, check=True)
    if r.stderr.strip():
        print(r.stderr, file=sys.stderr)
    return r.stdout.strip()


def main():
    html = SRC.read_text(encoding="utf-8")
    link = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/css2\?[^"]+)">', html)
    chars = {ord(c) for c in html if ord(c) >= 32} | set(range(32, 127))
    fonts, font_bytes = embedded_fonts(link.group(1).replace("&amp;", "&"), chars)
    html = re.sub(r'<link rel="preconnect"[^>]*>\n', "", html)
    html = html.replace(link.group(0), "<style>" + fonts + "</style>")
    assert html.count("const PROD = false;") == 1
    html = html.replace("const PROD = false;", "const PROD = true;")
    # minify: each <style> and <script>, then the whitespace between tags of the markup
    html = re.sub(r"<style>(.*?)</style>", lambda m: "<style>" + esbuild(m.group(1), "css") + "</style>", html, flags=re.S)
    html = re.sub(r"<script>(.*?)</script>", lambda m: "<script>" + esbuild(m.group(1), "js") + "</script>", html, flags=re.S)
    parts = re.split(r"(<script>.*?</script>|<style>.*?</style>)", html, flags=re.S)
    html = "".join(p if p.startswith(("<script>", "<style>")) else re.sub(r">\s+<", "><", p) for p in parts)
    DST.write_text(html, encoding="utf-8")
    print(f"{SRC.name} {SRC.stat().st_size / 1e3:.0f} KB -> {DST.name} {DST.stat().st_size / 1e3:.0f} KB "
          f"(embedded fonts {font_bytes / 1e3:.0f} KB before base64)")


if __name__ == "__main__":
    main()
