"""Persistent storage for Net-OS metric history and engine events."""

import sqlite3
import time

DB_PATH = "netos.db"


def get_conn(db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH):
    """Create the metrics and events tables if they don't already exist."""
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            cpu_percent REAL NOT NULL,
            memory_percent REAL NOT NULL,
            net_sent INTEGER NOT NULL,
            net_recv INTEGER NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            event TEXT NOT NULL,
            detail TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def log_metrics(
    cpu_percent: float,
    memory_percent: float,
    net_sent: int,
    net_recv: int,
    db_path: str = DB_PATH,
):
    """Store one metrics snapshot with the current timestamp."""
    conn = get_conn(db_path)
    conn.execute(
        """
        INSERT INTO metrics
            (timestamp, cpu_percent, memory_percent, net_sent, net_recv)
        VALUES (?, ?, ?, ?, ?)
        """,
        (time.time(), cpu_percent, memory_percent, net_sent, net_recv),
    )
    conn.commit()
    conn.close()


def log_event(event: str, detail: str = "", db_path: str = DB_PATH):
    """Record a discrete engine/strategy/router event for later review."""
    conn = get_conn(db_path)
    conn.execute(
        "INSERT INTO events (timestamp, event, detail) VALUES (?, ?, ?)",
        (time.time(), event, detail),
    )
    conn.commit()
    conn.close()


def fetch_recent_metrics(limit: int = 20, db_path: str = DB_PATH):
    """Return the most recent metric snapshots, newest first."""
    conn = get_conn(db_path)
    rows = conn.execute(
        "SELECT * FROM metrics ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def fetch_recent_events(limit: int = 20, db_path: str = DB_PATH):
    """Return the most recent logged events, newest first."""
    conn = get_conn(db_path)
    rows = conn.execute(
        "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
