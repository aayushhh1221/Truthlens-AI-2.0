"""
TruthLens AI 2.0 — Database Layer (SQLite)
Schema: analyses, claims, evidence, feedback, documents, model_versions, analytics_events
"""
import sqlite3
import json
from datetime import datetime
from utils.config import DATABASE_PATH
from utils.helpers import ts_now


# ─── Connection ───────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# ─── Init ─────────────────────────────────────────────────────

def init_database():
    """Create all tables if they do not exist."""
    ddl = """
    CREATE TABLE IF NOT EXISTS users (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id  TEXT    UNIQUE NOT NULL,
        created_at  TEXT    DEFAULT (datetime('now','utc')),
        last_seen   TEXT    DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS analyses (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id TEXT    UNIQUE NOT NULL,
        type        TEXT    NOT NULL,          -- 'text' | 'image' | 'document'
        input_hash  TEXT    NOT NULL,
        verdict     TEXT,
        fake_score  REAL,
        confidence  REAL,
        result_json TEXT,
        created_at  TEXT    DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS claims (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id TEXT    NOT NULL,
        claim_text  TEXT    NOT NULL,
        verdict     TEXT,
        confidence  REAL,
        sources     TEXT,                      -- JSON list
        created_at  TEXT    DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS evidence (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        claim_id    INTEGER NOT NULL,
        source_url  TEXT,
        source_title TEXT,
        snippet     TEXT,
        relevance   REAL,
        supports    INTEGER,                   -- 1=supports, 0=contradicts, -1=unknown
        created_at  TEXT    DEFAULT (datetime('now','utc')),
        FOREIGN KEY (claim_id) REFERENCES claims(id)
    );

    CREATE TABLE IF NOT EXISTS feedback (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        analysis_id TEXT    NOT NULL,
        is_correct  INTEGER NOT NULL,          -- 1=correct, 0=incorrect
        user_note   TEXT,
        created_at  TEXT    DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS documents (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_id         TEXT UNIQUE NOT NULL,
        doc_type       TEXT,
        authenticity   REAL,
        forgery_score  REAL,
        ocr_text       TEXT,
        result_json    TEXT,
        created_at     TEXT DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS model_versions (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        version     TEXT NOT NULL,
        accuracy    REAL,
        samples     INTEGER,
        notes       TEXT,
        created_at  TEXT DEFAULT (datetime('now','utc'))
    );

    CREATE TABLE IF NOT EXISTS analytics_events (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        event       TEXT NOT NULL,
        payload     TEXT,
        created_at  TEXT DEFAULT (datetime('now','utc'))
    );

    CREATE INDEX IF NOT EXISTS idx_analyses_type ON analyses(type);
    CREATE INDEX IF NOT EXISTS idx_analyses_verdict ON analyses(verdict);
    CREATE INDEX IF NOT EXISTS idx_feedback_aid ON feedback(analysis_id);
    CREATE INDEX IF NOT EXISTS idx_evidence_claim ON evidence(claim_id);
    CREATE INDEX IF NOT EXISTS idx_claims_analysis ON claims(analysis_id);
    """
    with get_conn() as conn:
        conn.executescript(ddl)


# ─── User Tracking ────────────────────────────────────────────

def get_or_create_user(session_id: str) -> None:
    """Register a session as a 'user' row, updating last_seen on repeat visits."""
    with get_conn() as conn:
        existing = conn.execute(
            "SELECT id FROM users WHERE session_id=?", (session_id,)
        ).fetchone()
        if existing:
            conn.execute(
                "UPDATE users SET last_seen=datetime('now','utc') WHERE session_id=?",
                (session_id,),
            )
        else:
            conn.execute(
                "INSERT INTO users (session_id) VALUES (?)", (session_id,)
            )


def get_user_count() -> int:
    with get_conn() as conn:
        return conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]


# ─── Analysis CRUD ────────────────────────────────────────────

def save_analysis(analysis_id: str, analysis_type: str, input_hash: str, result: dict) -> None:
    sql = """
        INSERT OR REPLACE INTO analyses
            (analysis_id, type, input_hash, verdict, fake_score, confidence, result_json)
        VALUES (?,?,?,?,?,?,?)
    """
    with get_conn() as conn:
        conn.execute(sql, (
            analysis_id,
            analysis_type,
            input_hash,
            result.get("verdict", ""),
            result.get("fake_score", result.get("ai_generated_score", 0)),
            result.get("confidence", 0),
            json.dumps(result),
        ))


def get_analyses_stats() -> dict:
    with get_conn() as conn:
        total   = conn.execute("SELECT COUNT(*) FROM analyses").fetchone()[0]
        fake    = conn.execute("SELECT COUNT(*) FROM analyses WHERE fake_score >= 70").fetchone()[0]
        docs    = conn.execute("SELECT COUNT(*) FROM analyses WHERE type='document'").fetchone()[0]
        images  = conn.execute("SELECT COUNT(*) FROM analyses WHERE type='image'").fetchone()[0]
        texts   = conn.execute("SELECT COUNT(*) FROM analyses WHERE type='text'").fetchone()[0]
        fb_total= conn.execute("SELECT COUNT(*) FROM feedback").fetchone()[0]
        fb_ok   = conn.execute("SELECT COUNT(*) FROM feedback WHERE is_correct=1").fetchone()[0]
        accuracy = round((fb_ok / fb_total * 100), 1) if fb_total else 0
        recent  = conn.execute(
            "SELECT verdict, fake_score, type, created_at FROM analyses ORDER BY id DESC LIMIT 20"
        ).fetchall()
        return {
            "total": total, "fake": fake, "docs": docs,
            "images": images, "texts": texts,
            "fb_total": fb_total, "fb_ok": fb_ok, "accuracy": accuracy,
            "recent": [dict(r) for r in recent],
        }


# ─── Claims & Evidence CRUD ──────────────────────────────────

def save_claims(analysis_id: str, claims: list, evidence_map: dict = None) -> None:
    """
    Persist claims and, if provided, link retrieved evidence to each claim.

    evidence_map keys are expected as 'claim_0', 'claim_1', ... matching
    the order of `claims` (as produced by agents/multi_agent.py).
    """
    sql = """
        INSERT INTO claims (analysis_id, claim_text, verdict, confidence, sources)
        VALUES (?,?,?,?,?)
    """
    evidence_sql = """
        INSERT INTO evidence (claim_id, source_url, source_title, snippet, relevance, supports)
        VALUES (?,?,?,?,?,?)
    """
    with get_conn() as conn:
        for i, c in enumerate(claims):
            cur = conn.execute(sql, (
                analysis_id,
                c.get("claim", ""),
                c.get("verdict", ""),
                c.get("confidence", 0),
                json.dumps(c.get("sources", [])),
            ))
            claim_id = cur.lastrowid

            if evidence_map:
                entry = evidence_map.get(f"claim_{i}", {})
                verdict = (c.get("verdict") or "").upper()
                supports = 1 if verdict == "SUPPORTED" else (0 if verdict == "CONTRADICTED" else -1)
                for ev in entry.get("evidence", [])[:5]:
                    conn.execute(evidence_sql, (
                        claim_id,
                        ev.get("url", ""),
                        ev.get("title", ""),
                        ev.get("snippet", "")[:500],
                        ev.get("relevance", 0),
                        supports,
                    ))


def get_evidence_for_analysis(analysis_id: str) -> list:
    """Fetch all evidence rows linked to claims for a given analysis."""
    sql = """
        SELECT e.source_url, e.source_title, e.snippet, e.relevance, e.supports, c.claim_text
        FROM evidence e
        JOIN claims c ON c.id = e.claim_id
        WHERE c.analysis_id = ?
        ORDER BY e.relevance DESC
    """
    with get_conn() as conn:
        rows = conn.execute(sql, (analysis_id,)).fetchall()
    return [dict(r) for r in rows]


# ─── Feedback CRUD ────────────────────────────────────────────

def save_feedback(analysis_id: str, is_correct: bool, user_note: str = "") -> None:
    sql = "INSERT INTO feedback (analysis_id, is_correct, user_note) VALUES (?,?,?)"
    with get_conn() as conn:
        conn.execute(sql, (analysis_id, 1 if is_correct else 0, user_note))
    # Log analytics event
    log_event("feedback_submitted", {"analysis_id": analysis_id, "correct": is_correct})


# ─── Document CRUD ───────────────────────────────────────────

def save_document(doc_id: str, doc_type: str, result: dict) -> None:
    sql = """
        INSERT OR REPLACE INTO documents
            (doc_id, doc_type, authenticity, forgery_score, ocr_text, result_json)
        VALUES (?,?,?,?,?,?)
    """
    with get_conn() as conn:
        conn.execute(sql, (
            doc_id,
            doc_type,
            result.get("authenticity_score", 0),
            result.get("forgery_score", 0),
            result.get("ocr_text", ""),
            json.dumps(result),
        ))


# ─── Analytics ───────────────────────────────────────────────

def log_event(event: str, payload: dict = None) -> None:
    sql = "INSERT INTO analytics_events (event, payload) VALUES (?,?)"
    with get_conn() as conn:
        conn.execute(sql, (event, json.dumps(payload or {})))


def get_daily_counts(days: int = 30) -> list:
    sql = """
        SELECT date(created_at) as day, COUNT(*) as cnt
        FROM analyses
        WHERE created_at >= date('now', ?)
        GROUP BY day ORDER BY day
    """
    with get_conn() as conn:
        rows = conn.execute(sql, (f"-{days} days",)).fetchall()
        return [{"day": r["day"], "count": r["cnt"]} for r in rows]
