"""Database helpers: SQLite connection and table creation."""
import sqlite3
from contextlib import closing
from pathlib import Path

# The database file lives next to this script. It is listed in .gitignore,
# so test accounts never get uploaded to GitHub.
DB_PATH = Path(__file__).with_name("app.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # lets us read columns by name
    return conn


def init_db():
    """Create the tables if they don't exist yet (safe to call every start)."""
    with closing(get_connection()) as conn, conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT    NOT NULL UNIQUE,
                salt          BLOB    NOT NULL,
                password_hash BLOB    NOT NULL,
                iterations    INTEGER NOT NULL,
                created_at    TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )