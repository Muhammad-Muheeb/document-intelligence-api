import sqlite3
import json

DB_PATH = "documents.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            name TEXT,
            role TEXT,
            experience_years INTEGER,
            skills TEXT,
            summary TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_analysis(filename, result):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO analyses (filename, name, role, experience_years, skills, summary) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            filename,
            result.get("name"),
            result.get("role"),
            result.get("experience_years"),
            json.dumps(result.get("skills", [])),
            result.get("summary"),
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def list_analyses():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM analyses ORDER BY id DESC").fetchall()
    conn.close()
    results = []
    for row in rows:
        item = dict(row)
        item["skills"] = json.loads(item["skills"])
        results.append(item)
    return results