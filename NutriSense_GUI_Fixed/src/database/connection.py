"""
SQLite connection and query helpers for NutriSense AI.
All SQL uses parameterized queries to prevent SQL injection.

HF Spaces Fix: Database stored in /tmp/ (ephemeral but functional).
Data resets on Space restart — acceptable for demo/academic use.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

# ── Database path ─────────────────────────────────────────────────────────────
# HF Spaces has a read-only filesystem except /tmp/
# Local dev: uses project root /database/nutrisense.db
# HF Spaces:  uses /tmp/nutrisense.db

def _resolve_db_path() -> Path:
    """
    Resolve database path based on environment.
    - HF Spaces / any read-only FS → /tmp/nutrisense.db
    - Local dev                    → PROJECT_ROOT/database/nutrisense.db
    """
    # Allow explicit override via env var
    env_path = os.environ.get("DB_PATH")
    if env_path:
        return Path(env_path)

    # HF Spaces detection
    if os.environ.get("SPACE_ID") or os.environ.get("HF_SPACE_ID"):
        return Path("/tmp/nutrisense.db")

    # Local dev — original path
    project_root = Path(__file__).resolve().parents[2]
    return project_root / "database" / "nutrisense.db"


DATABASE_PATH = _resolve_db_path()
DATABASE_DIR  = DATABASE_PATH.parent

# Schema is always read from project root (read-only is fine for reading)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH  = PROJECT_ROOT / "database" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    """Open a SQLite connection with row factory and foreign keys enabled."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database() -> None:
    """Create database file and tables from schema.sql if they do not exist."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file not found: {SCHEMA_PATH}")

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.commit()

        # Migration: add auth columns if upgrading an existing database
        existing_cols = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(users)").fetchall()
        }
        if "email" not in existing_cols:
            conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
        if "password_hash" not in existing_cols:
            conn.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
        conn.commit()


def execute_query(query: str, params: tuple | list | None = None) -> int:
    """
    Run INSERT/UPDATE/DELETE and return lastrowid (or rowcount for non-insert).
    Uses parameterized queries for safe execution.
    """
    with get_connection() as conn:
        cursor = conn.execute(query, params or ())
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount


def fetch_one(query: str, params: tuple | list | None = None) -> dict[str, Any] | None:
    """Fetch a single row as a dictionary, or None if not found."""
    with get_connection() as conn:
        row = conn.execute(query, params or ()).fetchone()
        return dict(row) if row else None


def fetch_all(query: str, params: tuple | list | None = None) -> list[dict[str, Any]]:
    """Fetch all matching rows as a list of dictionaries."""
    with get_connection() as conn:
        rows = conn.execute(query, params or ()).fetchall()
        return [dict(row) for row in rows]