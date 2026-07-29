#!/usr/bin/env python3
"""
Translate an English .srt into Bulgarian with a local Ollama model, once per
translator, and report wall-clock time for each full run.

Built as a head-to-head harness for the two translator candidates
(bggpt3-27b vs eurollm-22b) on natural dialogue -- a different register from
the academic prose in deliverables/, so it probes a different failure surface.

Why a Polish auxiliary track:
    English underspecifies grammatical gender, which Bulgarian must mark
    ("уморен" vs "уморена"). Polish marks gender on past-tense verbs AND
    adjectives, same as Bulgarian needs, so the aligned Polish line is passed
    as a disambiguation hint. Romance tracks were rejected: they mark adjective
    gender but not past-tense verb gender.

    Cue counts differ per language (EN 603 vs PL 560) and timestamps are offset
    by ~250ms, so alignment is by TIME OVERLAP, never by cue index.

Usage:
    python scripts/translate_srt.py --episode 1
    python scripts/translate_srt.py --episode 1 --limit 40      # smoke test
    python scripts/translate_srt.py --episode 1 --models bggpt3-27b
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUBS = REPO / "Subs"
OLLAMA = "http://127.0.0.1:11434/api/generate"

# newlines inside a cue are meaningful (subtitle line breaks) but would break a
# line-oriented response protocol, so they ride through as a sentinel
NL = "⏎"

DEFAULT_MODELS = ["bggpt3-27b", "eurollm-22b"]
BATCH = 12          # cues per request
CONTEXT = 3         # preceding source cues shown for continuity (not translated)

SYSTEM = """You are a professional subtitle translator. You translate English television dialogue into natural, idiomatic Bulgarian.

RULES:
1. Translate into fluent spoken Bulgarian as an experienced subtitler would - concise, natural, suitable for on-screen reading. Do NOT translate word-for-word.
2. Return EXACTLY one line per input cue, in the same order.
3. Each output line MUST start with the cue's number in square brackets: [1], [2], ...
4. Keep any HTML tags such as <i> and </i> exactly where they belong.
5. Keep the ⏎ symbol where it appears - it marks a line break inside the subtitle. Do not add or remove any.
6. Keep a leading "- " (dialogue dash) when the source has one.
7. Speaker labels in caps followed by a colon (e.g. "MAN:") stay as labels but are translated ("МЪЖ:").
8. Never merge, split, reorder, drop, or renumber cues. Never add commentary, notes, or explanations.
9. Output ONLY the numbered lines. No preamble, no closing remarks."""

GENDER_NOTE = """
A Polish translation of the same scene is provided as POLISH_REF for some cues.
Polish marks grammatical gender and formality the same way Bulgarian does.
Use it ONLY to decide grammatical gender (masculine/feminine verb and adjective
endings) and formal/informal address. Translate from the ENGLISH text - the
Polish is a hint about grammar, never the source of meaning."""


# ───────────────────────────── SRT parsing ─────────────────────────────

@dataclass
class Cue:
    idx: int
    start: str          # kept as raw text so timestamps round-trip byte-exact
    end: str
    text: str

    @property
    def start_ms(self) -> int:
        return ts_ms(self.start)

    @property
    def end_ms(self) -> int:
        return ts_ms(self.end)


def ts_ms(t: str) -> int:
    h, m, rest = t.split(":")
    s, ms = rest.split(",")
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms)


TIME_RE = re.compile(r"(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})")


def read_srt(path: Path) -> list[Cue]:
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp1251", "cp1250", "latin-1"):
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise SystemExit(f"cannot decode {path}")

    cues, blocks = [], re.split(r"\r?\n\r?\n+", text.strip())
    for b in blocks:
        lines = [l.rstrip("\r") for l in b.split("\n") if l.strip() != ""]
        if len(lines) < 2:
            continue
        m = TIME_RE.search(lines[1]) if TIME_RE.search(lines[1]) else TIME_RE.search(lines[0])
        if not m:
            continue
        body_start = 2 if TIME_RE.search(lines[1]) else 1
        try:
            idx = int(lines[0].strip())
        except ValueError:
            idx = len(cues) + 1
        body = "\n".join(lines[body_start:]).strip()
        cues.append(Cue(idx, m.group(1), m.group(2), body))
    return cues


def write_srt(path: Path, cues: list[Cue], texts: list[str]) -> None:
    out = []
    for c, t in zip(cues, texts):
        out.append(f"{c.idx}\r\n{c.start} --> {c.end}\r\n{t}\r\n")
    path.write_text("\r\n".join(out) + "\r\n", encoding="utf-8")


def align_by_time(src: list[Cue], aux: list[Cue]) -> dict[int, str]:
    """Map src cue index -> best time-overlapping aux text.

    Cue counts and timings differ between language tracks, so this is a
    two-pointer sweep on overlap duration rather than an index join.
    """
    out, j = {}, 0
    for c in src:
        best, best_ov = None, 0
        k = j
        while k < len(aux) and aux[k].start_ms < c.end_ms:
            ov = min(c.end_ms, aux[k].end_ms) - max(c.start_ms, aux[k].start_ms)
            if ov > best_ov:
                best, best_ov = aux[k], ov
            k += 1
        # only trust a match that covers a real share of the cue
        if best is not None and best_ov > 0.4 * max(1, c.end_ms - c.start_ms):
            out[c.idx] = best.text.replace("\n", " ")
        while j < len(aux) and aux[j].end_ms < c.start_ms:
            j += 1
    return out


# ───────────────────────────── model call ─────────────────────────────

def ollama(model: str, system: str, prompt: str, timeout: int = 600) -> str:
    body = json.dumps({
        "model": model, "system": system, "prompt": prompt, "stream": False,
        "keep_alive": "1h",          # keep weights resident between batches
        "options": {"temperature": 0.25, "top_p": 0.9, "num_predict": 2048},
    }).encode()
    req = urllib.request.Request(OLLAMA, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["response"]


LINE_RE = re.compile(r"^\s*\[(\d+)\]\s*(.*)$")


def parse_reply(reply: str, n: int) -> list[str] | None:
    """Strict: need every index 1..n exactly once, else caller re-splits."""
    got = {}
    for line in reply.splitlines():
        m = LINE_RE.match(line)
        if m:
            k = int(m.group(1))
            if 1 <= k <= n and k not in got:
                got[k] = m.group(2).strip()
    if len(got) != n:
        return None
    return [got[i] for i in range(1, n + 1)]


def translate_batch(model, cues, polish, prior, depth=0) -> list[str]:
    """Translate a batch; on malformed output, split and retry, then give up
    to the source text for that single cue so timing/cue-count never desync."""
    n = len(cues)
    src_lines = "\n".join(
        f"[{i}] {c.text.replace(chr(10), ' ' + NL + ' ')}" for i, c in enumerate(cues, 1))

    hints = [f"[{i}] {polish[c.idx]}" for i, c in enumerate(cues, 1) if c.idx in polish]
    parts = []
    if prior:
        parts.append("PRECEDING CONTEXT (already translated, do not repeat):\n" +
                     "\n".join(prior[-CONTEXT:]))
    if hints:
        parts.append(GENDER_NOTE.strip() + "\n\nPOLISH_REF:\n" + "\n".join(hints))
    parts.append(f"Translate these {n} cues into Bulgarian. "
                 f"Return exactly {n} lines, [1]..[{n}].\n\nENGLISH:\n{src_lines}")

    try:
        reply = ollama(model, SYSTEM, "\n\n".join(parts))
        out = parse_reply(reply, n)
    except (urllib.error.URLError, TimeoutError, OSError, KeyError) as e:
        print(f"      ! request failed: {e}", file=sys.stderr)
        out = None

    if out is not None:
        return [t.replace(NL, "\n").strip() for t in out]

    if n == 1:
        print(f"      ! cue {cues[0].idx}: kept source", file=sys.stderr)
        return [cues[0].text]

    mid = n // 2
    print(f"      ! malformed reply for {n} cues, splitting", file=sys.stderr)
    left = translate_batch(model, cues[:mid], polish, prior, depth + 1)
    right = translate_batch(model, cues[mid:], polish, prior + left, depth + 1)
    return left + right


# ───────────────────────────── driver ─────────────────────────────

def run(model: str, cues: list[Cue], polish: dict[int, str], out_path: Path) -> float:
    """Returns wall-clock seconds for the FULL run (load + all batches + write)."""
    t0 = time.perf_counter()
    done: list[str] = []
    total = len(cues)
    for i in range(0, total, BATCH):
        chunk = cues[i:i + BATCH]
        done.extend(translate_batch(model, chunk, polish, done))
        el = time.perf_counter() - t0
        pct = len(done) / total * 100
        eta = el / max(1, len(done)) * (total - len(done))
        print(f"   {model:<14} {len(done):>4}/{total} ({pct:5.1f}%)  "
              f"{el:6.1f}s elapsed  ~{eta:5.1f}s left", flush=True)
    write_srt(out_path, cues, done)
    return time.perf_counter() - t0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", type=int, default=1)
    ap.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    ap.add_argument("--limit", type=int, default=0, help="only first N cues (smoke test)")
    ap.add_argument("--no-polish", action="store_true", help="disable gender hints")
    a = ap.parse_args()

    eps = sorted(d for d in SUBS.iterdir()
                 if d.is_dir() and f"S01E{a.episode:02d}" in d.name)
    if not eps:
        raise SystemExit(f"no folder for S01E{a.episode:02d} under {SUBS}")
    ep = eps[0]

    # 2_English is the clean dialogue track; 3_English is SDH (sound descriptions)
    src_path = ep / "2_English.srt"
    if not src_path.exists():
        raise SystemExit(f"missing {src_path}")

    cues = read_srt(src_path)
    if a.limit:
        cues = cues[:a.limit]

    polish: dict[int, str] = {}
    pl_path = ep / "14_Polish.srt"
    if not a.no_polish and pl_path.exists():
        polish = align_by_time(cues, read_srt(pl_path))

    print(f"episode : {ep.name}")
    print(f"source  : {src_path.name}  ({len(cues)} cues)")
    print(f"gender  : Polish hints on {len(polish)}/{len(cues)} cues "
          f"({len(polish)/max(1,len(cues))*100:.0f}%)\n")

    timings = {}
    for m in a.models:
        out = ep / f"99_Bulgarian_{m}.srt"
        print(f"-> {m}")
        timings[m] = run(m, cues, polish, out)
        print(f"   wrote {out.name}   TOTAL {timings[m]:.1f}s\n")

    print("=" * 58)
    print(f"{'model':<16}{'total':>10}{'per cue':>12}{'cues/min':>12}")
    print("-" * 58)
    for m, s in timings.items():
        print(f"{m:<16}{s:>9.1f}s{s/len(cues):>11.2f}s{len(cues)/s*60:>12.1f}")
    print("=" * 58)


if __name__ == "__main__":
    main()
