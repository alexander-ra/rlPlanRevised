"""SQLite checkpoint. The run's source of truth.

Every unit of work is committed the moment it completes, so a kill at any point
resumes exactly where it stopped and never repeats or loses work.
"""
from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS chunks (
    id          TEXT PRIMARY KEY,
    path        TEXT,
    granularity TEXT,
    text        TEXT,
    status      TEXT DEFAULT 'pending',   -- pending | done | failed
    terms_json  TEXT,
    err         TEXT,
    ts          REAL
);
CREATE TABLE IF NOT EXISTS terms (
    key           TEXT PRIMARY KEY,        -- normalised lookup key
    term          TEXT,                    -- canonical surface form
    kind          TEXT,
    freq          INTEGER DEFAULT 0,
    contexts_json TEXT,
    sources_json  TEXT,                    -- extracted | glossary | term_map
    category      TEXT,
    existing_bg   TEXT                     -- from terminology_EN_BG.md / TERM_MAP
);
CREATE TABLE IF NOT EXISTS proposals (
    key          TEXT PRIMARY KEY,
    samples_json TEXT,
    candidates_json TEXT,
    decision     TEXT,                     -- auto | queue | deferred
    chosen       TEXT,
    reason       TEXT,
    ts           REAL
);
CREATE TABLE IF NOT EXISTS meta (k TEXT PRIMARY KEY, v TEXT);
CREATE INDEX IF NOT EXISTS ix_chunks_status ON chunks(status);
"""


class Store:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path), timeout=60)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(SCHEMA)
        self.db.commit()

    # ── meta ──
    def get(self, k: str, default=None):
        r = self.db.execute("SELECT v FROM meta WHERE k=?", (k,)).fetchone()
        return r[0] if r else default

    def set(self, k: str, v) -> None:
        self.db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (k, str(v)))
        self.db.commit()

    # ── chunks ──
    def add_chunks(self, rows) -> None:
        self.db.executemany(
            "INSERT OR IGNORE INTO chunks(id,path,granularity,text) VALUES (?,?,?,?)", rows)
        self.db.commit()

    def pending_chunks(self):
        return self.db.execute(
            "SELECT id,path,text FROM chunks WHERE status='pending' ORDER BY id").fetchall()

    def finish_chunk(self, cid: str, terms, err: str | None = None) -> None:
        self.db.execute(
            "UPDATE chunks SET status=?, terms_json=?, err=?, ts=? WHERE id=?",
            ("failed" if err else "done", json.dumps(terms, ensure_ascii=False),
             err, time.time(), cid))
        self.db.commit()

    def chunk_counts(self):
        rows = dict(self.db.execute(
            "SELECT status, COUNT(*) FROM chunks GROUP BY status").fetchall())
        return rows.get("pending", 0), rows.get("done", 0), rows.get("failed", 0)

    def all_chunk_terms(self):
        for (j,) in self.db.execute(
                "SELECT terms_json FROM chunks WHERE status='done' AND terms_json IS NOT NULL"):
            try:
                yield from json.loads(j)
            except Exception:
                continue

    # ── terms ──
    def upsert_terms(self, rows) -> None:
        self.db.executemany(
            """INSERT INTO terms(key,term,kind,freq,contexts_json,sources_json,existing_bg)
               VALUES (:key,:term,:kind,:freq,:contexts,:sources,:existing_bg)
               ON CONFLICT(key) DO UPDATE SET
                 freq=excluded.freq, contexts_json=excluded.contexts_json,
                 sources_json=excluded.sources_json,
                 existing_bg=COALESCE(excluded.existing_bg, terms.existing_bg)""", rows)
        self.db.commit()

    def set_category(self, key: str, cat: str) -> None:
        self.db.execute("UPDATE terms SET category=? WHERE key=?", (cat, key))

    def commit(self) -> None:
        self.db.commit()

    def terms(self, only_uncategorised: bool = False):
        q = "SELECT key,term,kind,freq,contexts_json,sources_json,category,existing_bg FROM terms"
        if only_uncategorised:
            q += " WHERE category IS NULL"
        return self.db.execute(q + " ORDER BY freq DESC, term").fetchall()

    def term_count(self) -> int:
        return self.db.execute("SELECT COUNT(*) FROM terms").fetchone()[0]

    # ── proposals ──
    def done_proposals(self) -> set[str]:
        return {r[0] for r in self.db.execute("SELECT key FROM proposals")}

    def save_proposal(self, key, samples, candidates, decision, chosen, reason) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO proposals VALUES (?,?,?,?,?,?,?)",
            (key, json.dumps(samples, ensure_ascii=False),
             json.dumps(candidates, ensure_ascii=False),
             decision, chosen, reason, time.time()))
        self.db.commit()

    def proposals(self):
        return self.db.execute(
            """SELECT p.key, t.term, t.category, t.freq, t.contexts_json, t.existing_bg,
                      p.samples_json, p.candidates_json, p.decision, p.chosen, p.reason
               FROM proposals p JOIN terms t ON t.key = p.key
               ORDER BY t.freq DESC, t.term""").fetchall()

    def decision_counts(self):
        return dict(self.db.execute(
            "SELECT decision, COUNT(*) FROM proposals GROUP BY decision").fetchall())
