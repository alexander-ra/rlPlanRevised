"""Corpus discovery, markdown cleaning, and the three segmentation granularities.

Cleaning matters for extraction quality: code blocks and file trees are full of
identifier-shaped noise that would otherwise flood the queue with things like
`day07_cfrplus_panels.py`. Tables are KEPT - step04's abstraction vocabulary
lives largely inside them.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

SOURCES = [
    ("cleanStep", REPO / "planning" / "cleanSteps", "*.md"),
    ("summary", REPO / "deliverables" / "reports", "step*/summary/summaryEn.md"),
    ("onePager", REPO / "deliverables" / "reports", "step*/summary/onePager.md"),
    ("report", REPO / "deliverables" / "reports", "step*/report_en.md"),
]

FENCE_RE = re.compile(r"^```.*?^```", re.S | re.M)
TILDE_RE = re.compile(r"^~~~.*?^~~~", re.S | re.M)
YAML_RE = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
IMG_RE = re.compile(r"!\[[^\]]*\]\([^)]*\)(\{[^}]*\})?")
LINKURL_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
MATHBLOCK_RE = re.compile(r"\$\$.*?\$\$", re.S)
MATHINLINE_RE = re.compile(r"\$[^$\n]+\$")
HEADING_RE = re.compile(r"^#{1,6}\s+", re.M)
SUP_RE = re.compile(r"<sup[^>]*>.*?</sup>", re.S)


def discover() -> list[tuple[str, Path]]:
    out = []
    for kind, root, pat in SOURCES:
        if root.exists():
            for p in sorted(root.glob(pat)):
                out.append((kind, p))
    return out


def clean(md: str) -> str:
    md = YAML_RE.sub("", md)
    md = COMMENT_RE.sub(" ", md)
    md = FENCE_RE.sub(" ", md)
    md = TILDE_RE.sub(" ", md)
    md = MATHBLOCK_RE.sub(" ", md)
    md = MATHINLINE_RE.sub(" ", md)
    md = SUP_RE.sub("", md)
    md = IMG_RE.sub(" ", md)
    md = LINKURL_RE.sub(r"\1", md)      # keep link text, drop the URL
    md = INLINE_CODE_RE.sub(" ", md)
    md = HEADING_RE.sub("", md)
    md = re.sub(r"[*_>]{1,3}", "", md)  # emphasis marks
    md = re.sub(r"^\s*[-|:]{3,}\s*$", " ", md, flags=re.M)   # table rules
    md = re.sub(r"[ \t]+", " ", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\"'‘“])")


def segment(text: str, mode: str, window_words: int = 400) -> list[str]:
    """mode: 'sentence' | 'paragraph' | 'window'"""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    if mode == "paragraph":
        out, buf = [], ""
        for p in paras:
            # merge tiny fragments (table rows, one-line bullets) into usable context
            if len(buf.split()) + len(p.split()) < 120:
                buf = (buf + "\n" + p).strip()
            else:
                if buf:
                    out.append(buf)
                buf = p
        if buf:
            out.append(buf)
        return out

    if mode == "sentence":
        out = []
        for p in paras:
            out.extend(s.strip() for s in SENT_RE.split(p) if len(s.split()) >= 4)
        return out

    words, out, buf = text.split(), [], []
    for w in words:
        buf.append(w)
        if len(buf) >= window_words:
            out.append(" ".join(buf))
            buf = []
    if buf:
        out.append(" ".join(buf))
    return out


def chunk_id(path: Path, mode: str, i: int, text: str) -> str:
    h = hashlib.sha1(f"{path}|{mode}|{i}|{text[:200]}".encode()).hexdigest()[:16]
    return f"{mode}:{h}"


def build_chunks(mode: str, files: list[tuple[str, Path]] | None = None):
    files = files if files is not None else discover()
    rows = []
    for _kind, p in files:
        try:
            body = clean(p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for i, seg in enumerate(segment(body, mode)):
            if len(seg.split()) < 5:
                continue
            rows.append((chunk_id(p, mode, i, seg), str(p), mode, seg))
    return rows
