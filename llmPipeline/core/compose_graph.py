"""Containment graph + constraint pool for compositional resolution.

A term is "ready" when every constituent it contains already has a settled
Bulgarian rendering, so those renderings can be injected as constraints and the
compound re-sampled for consistency.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

CYR = re.compile(r"[Ѐ-ӿ]")


def fold(s: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s or "").lower()).strip()


def has_cyrillic(s: str) -> bool:
    return bool(CYR.search(s or ""))


def stem(s: str, cut: int = 3) -> str:
    """Loose stem for inflection-tolerant matching.

    Bulgarian marks definiteness and number with suffixes ("равновесие" ->
    "равновесието", "стратегия" -> "стратегии"), so a constrained rendering
    rarely appears verbatim inside the compound. Trimming the tail lets us check
    the constraint was USED without demanding an exact substring.
    """
    s = fold(s)
    return s[:-cut] if len(s) > cut + 2 else s


@dataclass
class Term:
    key: str
    term: str
    freq: int
    existing_bg: str | None
    settled_bg: str | None            # picks.bg, else proposals.chosen when auto
    status: str | None                # picked | auto | flagged | skipped | None
    decision: str | None              # queue | stage2 | auto | deferred
    candidates: list = field(default_factory=list)

    @property
    def words(self) -> list[str]:
        return fold(self.term).split()


# ── constraint pool ──────────────────────────────────────────────────────────

def classify_conflict(t: Term) -> str:
    """'' | 'benign' | 'real'

    terminology_EN_BG.md stores the ENGLISH EXPANSION in the Bulgarian column for
    abbreviation rows (PBT -> "Population-Based Training"), so a raw string
    comparison against a Latin settled value reports a conflict that isn't one.
    A genuine conflict is the glossary holding Cyrillic while we settled on Latin
    - that means a keep-Latin classification overrode a real translation.
    """
    if not t.existing_bg or not t.settled_bg:
        return ""
    if fold(t.existing_bg) == fold(t.settled_bg):
        return ""
    if t.status == "picked":
        return ""                      # a human overrode it deliberately
    ex_cyr, set_cyr = has_cyrillic(t.existing_bg), has_cyrillic(t.settled_bg)
    if not ex_cyr and not set_cyr:
        return "benign"                # expansion vs abbreviation, both Latin
    if ex_cyr and not set_cyr:
        return "real"                  # translation overridden by keep-Latin
    return "real"


def find_leaky(pool: dict[str, str]) -> dict[str, str]:
    """Single-word terms whose rendering absorbed a larger compound's meaning.

    Extraction produced bare fragments like "nash", and sampling settled it as
    "Наш равновесие" - the translation of *Nash equilibrium*, not of "Nash".
    Composing on that yields "Наш равновесие базова линия".

    Deliberately narrow: only ONE-word English terms whose Bulgarian is
    MULTI-word and contains another one-word term's rendering. Restricting to
    one-word English avoids the obvious false positive, where a legitimate
    multi-word rendering shares vocabulary with another term
    ("policy gradient" -> "градиент на стратегията" contains "стратегия").
    """
    # hyphens separate words: "cross-validation" and "best-response" are
    # semantically two words, and their naturally two-word Bulgarian
    # ("кръстосана проверка") is not evidence of a leak.
    def en_words(s: str) -> int:
        return len([p for p in re.split(r"[\s\-–—]+", s) if p])

    singles = {k: v for k, v in pool.items() if en_words(k) == 1}
    leaky: dict[str, str] = {}
    for k, v in singles.items():
        if len(fold(v).split()) < 2:
            continue
        for other_k, other_v in singles.items():
            if other_k == k or not has_cyrillic(other_v):
                continue
            if len(fold(other_v).split()) != 1:
                continue
            if stem(other_v) and stem(other_v) in fold(v):
                leaky[k] = v
                break
    return leaky


def build_pool(terms: list[Term]):
    """-> (constraints by folded term, quarantined, benign, leaky)"""
    pool: dict[str, str] = {}
    quarantined: list[Term] = []
    benign: list[Term] = []
    for t in terms:
        if not t.settled_bg:
            continue
        c = classify_conflict(t)
        if c == "real":
            quarantined.append(t)
            continue
        if c == "benign":
            benign.append(t)
        pool[fold(t.term)] = t.settled_bg

    leaky = find_leaky(pool)
    for k in leaky:
        pool.pop(k, None)
    return pool, quarantined, benign, leaky


# ── containment ──────────────────────────────────────────────────────────────

def constituents(t: Term, known: set[str]) -> list[str]:
    """Longest-first, non-overlapping whole-word spans of `t` that are known terms.

    Longest-first matters: for "counterfactual value decomposition" we want
    "counterfactual value" as one constraint, not "value" on its own.
    """
    w = t.words
    n = len(w)
    taken = [False] * n
    out: list[str] = []
    for size in range(n - 1, 0, -1):
        for i in range(n - size + 1):
            if any(taken[i:i + size]):
                continue
            span = " ".join(w[i:i + size])
            if span in known and span != fold(t.term):
                out.append(span)
                for j in range(i, i + size):
                    taken[j] = True
    return out


def ready_terms(pending: list[Term], pool: dict[str, str],
                known: set[str]) -> list[tuple[Term, dict[str, str]]]:
    """Pending terms whose every constituent has a usable constraint.

    Shortest first so shallow compounds settle before deeper ones that contain them.
    """
    out = []
    for t in sorted(pending, key=lambda x: (len(x.words), -x.freq)):
        cons = constituents(t, known)
        if not cons:
            continue
        if all(c in pool for c in cons):
            out.append((t, {c: pool[c] for c in cons}))
    return out


def load_terms(store) -> list[Term]:
    rows = store.db.execute("""
        SELECT t.key, t.term, t.freq, t.existing_bg,
               p.decision, p.chosen, p.candidates_json,
               pk.bg, pk.status
        FROM terms t
        JOIN proposals p ON p.key = t.key
        LEFT JOIN picks pk ON pk.key = t.key""").fetchall()
    import json
    out = []
    for key, term, freq, ex, dec, chosen, cj, pbg, pstat in rows:
        settled = pbg if (pbg and pstat in ("picked", "auto")) else (
            chosen if dec == "auto" else None)
        try:
            cands = json.loads(cj or "[]")
        except Exception:  # noqa: BLE001
            cands = []
        out.append(Term(key, term, freq or 0, ex, settled, pstat, dec, cands))
    return out
