#!/usr/bin/env python3
"""Force the terminology decisions from the summaries review into the glossary DB.

The review (bundlereview/, 89 comments) settled a handful of terms that the
automatic pipeline had chosen differently. Terminology has to be bound where the
Bulgarian is *generated*, not patched afterwards, so these land in `picks` -
which wins over `proposals.chosen` in translate_doc.load_glossary().

Idempotent: re-running is a no-op. Run before re-translating anything.

    python llmPipeline/apply_review_terms.py --dry-run
    python llmPipeline/apply_review_terms.py
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
DB = HERE / "out" / "glossary.db"
NOTE = "summaries review 2026-08"

# key -> (bulgarian, keep_latin)
# Keys are the normalised lookup keys already present in `terms`; the few that
# are new are created below.
OVERRIDES: dict[str, tuple[str, int]] = {
    # --- Earth Mover's Distance: one quantity, four spellings in the corpus ---
    # "Земьов-Мъри"/"Земьов-Музер" calque the English idiom into what reads as a
    # surname. Wasserstein-1 is the same distance and is what a Bulgarian
    # specialist writes.
    "emd":                              ("разстояние на Васерщайн", 0),
    "emd proxy":                        ("прокси на разстоянието на Васерщайн", 0),
    "emd-style distance":               ("разстояния от тип Васерщайн", 0),
    "earth mover's distance":           ("разстояние на Васерщайн", 0),
    "earth mover's distance (emd":      ("разстояние на Васерщайн", 0),

    # --- action translation -------------------------------------------------
    # Deliberate anglicism: "превод" collides with translation of *text*, which
    # this corpus also discusses at length.
    "action translation":               ("транслация на действия", 0),
    "action translation problem":       ("проблем с транслацията на действия", 0),
    "action-translation method":        ("метод за транслация на действия", 0),
    "action-translation step":          ("стъпка на транслация на действия", 0),
    "static translation":               ("статична транслация", 0),
    "translation problem":              ("проблем с транслацията", 0),
    "translation boundary":             ("граници на транслацията", 0),
    "deployment translation":           ("транслация при внедряване", 0),
    "static action translator":         ("статични транслатори на действия", 0),
    "nearest-action translator":        ("транслатор към най-близкото действие", 0),
    "probability-split translator":     ("вероятностно разделяне", 0),
    "pseudo-harmonic translator":       ("псевдохармоничен транслатор", 0),

    # --- bottleneck ---------------------------------------------------------
    "bottleneck":                       ("стеснение", 0),
    "computational bottleneck":         ("изчислително стеснение", 0),
    "information bottleneck lagrangian": ("лагранжиан на информационното стеснение", 0),
    "information bottleneck (ib":       ("информационно стеснение", 0),
    "network size bottleneck":          ("стеснение в размера на мрежата", 0),

    # --- misc ---------------------------------------------------------------
    "state-of-the-art":                 ("водещ стандарт", 0),
    "state of the art":                 ("водещ стандарт", 0),
    "libratus":                         ("Libratus", 1),
    "king-flop":                        ("флоп с Поп", 0),
}

# Terms the extractor never saw as terms, but which the review settled.
# (key, surface form, bulgarian, category)
NEW_TERMS = [
    ("jack",  "Jack",  "Вале", "Poker & Games"),
    ("queen", "Queen", "Дама", "Poker & Games"),
    ("king",  "King",  "Поп",  "Poker & Games"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    if not DB.exists():
        print(f"FATAL: {DB} not found", file=sys.stderr)
        return 1

    con = sqlite3.connect(str(DB))
    now = time.time()
    changed = missing = 0

    for key, surface, bg, cat in NEW_TERMS:
        if con.execute("SELECT 1 FROM terms WHERE key=?", (key,)).fetchone():
            continue
        print(f"  + new term {key!r} -> {bg!r}")
        if not a.dry_run:
            con.execute(
                "INSERT INTO terms(key,term,kind,freq,contexts_json,sources_json,"
                "category,existing_bg) VALUES(?,?,?,?,?,?,?,?)",
                (key, surface, "term", 0, "[]", json.dumps(["review"]), cat, bg))
            con.execute(
                "INSERT INTO proposals(key,samples_json,candidates_json,decision,"
                "chosen,reason,ts) VALUES(?,?,?,?,?,?,?)",
                (key, "[]", "[]", "auto", bg, NOTE, now))
        changed += 1

    for key, (bg, latin) in OVERRIDES.items():
        row = con.execute("SELECT term FROM terms WHERE key=?", (key,)).fetchone()
        if not row:
            print(f"  ! no such term: {key!r}")
            missing += 1
            continue
        cur = con.execute("SELECT bg FROM picks WHERE key=?", (key,)).fetchone()
        if cur and cur[0] == bg:
            continue
        was = cur[0] if cur else "(no pick)"
        print(f"  ~ {row[0]!r}: {was!r} -> {bg!r}")
        if not a.dry_run:
            con.execute(
                "INSERT INTO picks(key,bg,status,keep_latin,first_use,note,stage,ts) "
                "VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(key) DO UPDATE SET "
                "bg=excluded.bg, status=excluded.status, keep_latin=excluded.keep_latin, "
                "note=excluded.note, stage=excluded.stage, ts=excluded.ts",
                (key, bg, "picked", latin, 1, NOTE, "review", now))
        changed += 1

    if not a.dry_run:
        con.commit()
    con.close()
    print(f"\n{changed} change(s){' (dry run)' if a.dry_run else ''}"
          f"{f', {missing} key(s) not in the DB' if missing else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
