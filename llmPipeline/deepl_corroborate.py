#!/usr/bin/env python3
"""DeepL corroboration for terms where BgGPT could not reach consensus.

Why DeepL and not more BgGPT samples: the remaining terms are queued precisely
because BgGPT has no stable opinion about them, so more samples from the same
model only resample the same uncertainty. DeepL is an INDEPENDENT system, so its
agreement is real evidence rather than self-agreement.

It is a voter, never an override. Verified on the first test call: DeepL matched
the human glossary exactly on "counterfactual regret minimization" but produced
"набор от информация" for "information set", where the established term is
"информационно множество". It has no domain knowledge, so:

  DeepL agrees with the existing glossary entry -> accept (two independent sources)
  DeepL agrees with the top-voted BgGPT candidate -> accept
  DeepL agrees with a lower-voted candidate      -> promote it, still your call
  DeepL matches nothing                          -> add as a candidate, your call

    python llmPipeline/deepl_corroborate.py --dry-run --limit 40
    python llmPipeline/deepl_corroborate.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from core import store as store_mod                                  # noqa: E402
from core.compose_graph import fold, has_cyrillic, stem              # noqa: E402

OUT = HERE / "out"
KEY_FILE = OUT / ".deepl_key"
API = "https://api-free.deepl.com/v2/translate"
USAGE = "https://api-free.deepl.com/v2/usage"

# DeepL's `context` field is not translated and not billed; it exists to
# disambiguate. Untargeted, DeepL renders these as everyday vocabulary -
# "information set" came back as "набор от информация" rather than the
# game-theory term - so the framing is explicitly computer-science/ML, and each
# batch additionally carries its category and real sentences from the corpus.
DOMAIN = (
    "This is specialist terminology from a computer science PhD dissertation on "
    "artificial intelligence in computer games. The subject areas are machine "
    "learning and theoretical computer science: reinforcement learning, deep "
    "neural networks, game theory, imperfect-information games such as poker, "
    "multi-agent systems, search algorithms and algorithm analysis. "
    "Render each item as established Bulgarian scientific terminology used in "
    "academic computer-science writing, not as everyday vocabulary. "
    "For example 'policy' is the reinforcement-learning sense (a decision rule), "
    "'value' means an expected numeric return, 'agent' is an autonomous decision "
    "maker, 'state' is a configuration of an environment, and 'information set' "
    "is the game-theoretic concept."
)


def batch_context(category: str | None, sentences: list[str]) -> str:
    """Category plus a little real usage, so DeepL sees the sense of the terms.

    Kept deliberately short: with four full sentences DeepL began emitting
    fragments OF the context instead of translating the term ("observation
    function" came back as "на DeepStack"). Two clipped sentences give the sense
    without inviting the model to copy from them.
    """
    parts = []
    if category and category != "UNCLEAR":
        parts.append(f"All of these terms belong to the subject area: {category}.")
    clean = [s.strip()[:110] for s in sentences if len(s.strip()) > 25][:2]
    if clean:
        parts.append("Example usage: " + " ".join(clean))
    return " ".join(parts)


LATIN_WORD = re.compile(r"[A-Za-z]{3,}")


def context_bleed(term: str, out: str) -> bool:
    """DeepL sometimes returns text copied from the context rather than a
    translation. Symptom: Latin-script words in the output that do not occur in
    the source term (e.g. "observation function" -> "на DeepStack")."""
    src = {w.lower() for w in LATIN_WORD.findall(term)}
    return any(w.lower() not in src for w in LATIN_WORD.findall(out))


def key() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"no DeepL key at {KEY_FILE}")
    return KEY_FILE.read_text(encoding="utf-8").strip()


def call(texts: list[str], k: str, context: str = "", attempts: int = 4) -> list[str]:
    body = json.dumps({
        "text": texts, "target_lang": "BG", "source_lang": "EN",
        "context": (DOMAIN + " " + context).strip()[:900],
    }).encode()
    for i in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                API, data=body,
                headers={"Authorization": f"DeepL-Auth-Key {k}",
                         "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return [t["text"] for t in json.loads(r.read())["translations"]]
        except urllib.error.HTTPError as e:
            if e.code == 456:
                raise SystemExit("DeepL quota exhausted")
            if e.code == 429:
                time.sleep(min(30, 5 * i))
                continue
            if 400 <= e.code < 500:
                raise SystemExit(f"DeepL rejected request: {e.code} {e.read()[:200]!r}")
            time.sleep(3 * i)
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(3 * i)
    return []


def matches(deepl: str, cand: str) -> bool:
    """Stem match, tolerant of Bulgarian inflection and definite articles."""
    a, b = fold(deepl), fold(cand)
    if not a or not b:
        return False
    if a == b:
        return True
    aw = [w for w in a.split() if len(w) > 3]
    bw = [w for w in b.split() if len(w) > 3]
    if not aw or not bw or abs(len(a.split()) - len(b.split())) > 1:
        return False
    return all(any(stem(x) == stem(y) for y in bw) for x in aw)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--batch", type=int, default=40)
    a = ap.parse_args()

    k = key()
    st = store_mod.Store(OUT / "glossary.db")
    rows = st.db.execute("""
        SELECT t.key, t.term, t.existing_bg, t.contexts_json, p.candidates_json,
               t.category
        FROM proposals p JOIN terms t ON t.key = p.key
        LEFT JOIN picks pk ON pk.key = p.key
        WHERE p.decision IN ('queue','stage2') AND pk.key IS NULL
        ORDER BY t.category, t.freq DESC, t.term""").fetchall()
    if a.limit:
        rows = rows[:a.limit]
    print(f"{len(rows)} unresolved terms to corroborate")

    # batch within a single category so every request carries a coherent context
    by_cat: dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r[5] or "UNCLEAR", []).append(r)
    batches = [(cat, group[i:i + a.batch])
               for cat, group in by_cat.items()
               for i in range(0, len(group), a.batch)]
    print(f"{len(batches)} batches across {len(by_cat)} categories")

    stats: Counter = Counter()
    t0 = time.perf_counter()
    processed = 0

    for bi, (cat, grp) in enumerate(batches):
        sents: list[str] = []
        for r in grp:
            try:
                sents.extend(json.loads(r[3] or "[]")[:1])
            except Exception:  # noqa: BLE001
                pass
        out = call([r[1] for r in grp], k, batch_context(cat, sents))
        if not out or len(out) != len(grp):
            print(f"   batch {bi} ({cat}) returned {len(out)}/{len(grp)}; skipping")
            continue

        for (key_, term, ex_bg, ctx_json, cj, _cat), dl in zip(grp, out):
            cands = json.loads(cj or "[]")
            dl = (dl or "").strip()
            if not dl or not has_cyrillic(dl):
                stats["no usable DeepL output"] += 1
                continue
            if context_bleed(term, dl):
                stats["rejected: context bleed"] += 1
                continue

            decision = chosen = None
            reason = ""

            if ex_bg and has_cyrillic(ex_bg) and matches(dl, ex_bg):
                decision, chosen = "auto", ex_bg
                reason = "deepl: agrees with your existing glossary entry"
            elif cands and matches(dl, cands[0].get("bg", "")):
                decision, chosen = "auto", cands[0]["bg"]
                reason = "deepl: agrees with the top-voted candidate"
            else:
                hit = next((c for c in cands[1:] if matches(dl, c.get("bg", ""))), None)
                if hit:
                    cands = [hit] + [c for c in cands if c is not hit]
                    reason = "deepl: agrees with a lower-voted candidate - promoted"
                    stats["promoted"] += 1
                else:
                    cands = cands + [{"bg": dl, "votes": 0, "deepl": True}]
                    reason = "deepl: independent suggestion added"
                    stats["added candidate"] += 1

            if a.dry_run:
                mark = {"auto": "ACCEPT", None: "queue"}.get(decision, "queue")
                print(f"   {mark:<6} {term[:34]:<36} deepl={dl[:34]:<36} {reason[:44]}")
                if decision:
                    stats["auto-accepted"] += 1
                continue

            if decision == "auto":
                st.db.execute(
                    "UPDATE proposals SET decision='auto', chosen=?, reason=? WHERE key=?",
                    (chosen, reason, key_))
                st.db.execute(
                    """INSERT OR REPLACE INTO picks(key,bg,status,keep_latin,first_use,note,stage,ts)
                       VALUES (?,?,?,0,1,?,?,?)""",
                    (key_, chosen, "auto", reason, "deepl", time.time()))
                stats["auto-accepted"] += 1
            else:
                st.db.execute(
                    "UPDATE proposals SET candidates_json=?, reason=? WHERE key=?",
                    (json.dumps(cands, ensure_ascii=False), reason, key_))
        if not a.dry_run:
            st.db.commit()

        processed += len(grp)
        if bi % 5 == 0 or processed >= len(rows):
            el = time.perf_counter() - t0
            print(f"   {processed}/{len(rows)}  {el/60:5.1f}m  "
                  f"accepted={stats['auto-accepted']}", flush=True)

    print("\n" + "\n".join(f"  {k2:<26} {v}" for k2, v in stats.most_common()))
    try:
        req = urllib.request.Request(USAGE, headers={"Authorization": f"DeepL-Auth-Key {k}"})
        u = json.loads(urllib.request.urlopen(req, timeout=30).read())
        print(f"\nDeepL usage: {u['character_count']:,} / {u['character_limit']:,} chars")
    except Exception:  # noqa: BLE001
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
