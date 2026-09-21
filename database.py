import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "smartnet.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS monitoring_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monitor_type TEXT NOT NULL,
            target TEXT NOT NULL,
            port INTEGER,
            status TEXT NOT NULL,
            response_time_ms REAL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    connection.commit()
    connection.close()


def save_result(monitor_type, target, status, response_time_ms=None, port=None, details=None):
    connection = get_connection()
    connection.execute(
        """
        INSERT INTO monitoring_results
        (monitor_type, target, port, status, response_time_ms, details)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (monitor_type, target, port, status, response_time_ms, details),
    )
    connection.commit()
    connection.close()


def get_results(limit=100):
    connection = get_connection()
    rows = connection.execute(
        """
        SELECT id, monitor_type, target, port, status,
               response_time_ms, details, created_at
        FROM monitoring_results
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()
    connection.close()
    return [dict(row) for row in rows]
