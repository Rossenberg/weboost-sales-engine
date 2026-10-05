"""Small helper module for connecting to the SQLite database and logging events."""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "weboost.db"
SCHEMA_PATH = Path(__file__).resolve().parent / "schema.sql"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    migrate(conn)
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    migrate(conn)
    conn.commit()
    conn.close()


def migrate(conn: sqlite3.Connection) -> None:
    """Add columns introduced after the first schema version."""
    cols = {r["name"] for r in conn.execute("PRAGMA table_info(leads)")}
    if not cols:  # table not created yet (fresh database)
        return
    for name, ddl in [
        ("last_message_id", "TEXT"),
        ("mc_number", "TEXT"),
        ("phone", "TEXT"),
        ("lead_probability", "INTEGER"),  # AI estimate 0-100 that this becomes a customer
        ("next_action", "TEXT"),          # AI-suggested next step after a reply
        ("reply_reasoning", "TEXT"),
    ]:
        if name not in cols:
            conn.execute(f"ALTER TABLE leads ADD COLUMN {name} {ddl}")
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id TEXT NOT NULL,
            kind TEXT NOT NULL,          -- initial / followup_1..3 / reply_in
            subject TEXT,
            body TEXT,
            created_at TEXT NOT NULL,
            message_id TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_messages_lead ON messages(lead_id);
        CREATE TABLE IF NOT EXISTS api_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            step TEXT NOT NULL,          -- analysis / email / followup / reply_classification
            model TEXT,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cost_usd REAL
        );
    """)


def log_message(conn: sqlite3.Connection, lead_id: str, kind: str, subject: str, body: str, message_id: str = "") -> None:
    conn.execute(
        "INSERT INTO messages (lead_id, kind, subject, body, created_at, message_id) VALUES (?, ?, ?, ?, ?, ?)",
        (lead_id, kind, subject, body, now_iso(), message_id),
    )
    conn.commit()


def log_event(conn: sqlite3.Connection, lead_id: str, action: str, status: str, detail: str = "") -> None:
    conn.execute(
        "INSERT INTO lead_events (lead_id, timestamp, action, status, detail) VALUES (?, ?, ?, ?, ?)",
        (lead_id, now_iso(), action, status, detail),
    )
    conn.commit()
