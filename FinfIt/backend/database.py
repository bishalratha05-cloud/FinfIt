import sqlite3
from pathlib import Path
from datetime import datetime

def connect(db_path):
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(path)

def init_db(db_path):
    with connect(db_path) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                method TEXT NOT NULL,
                result_count INTEGER NOT NULL,
                searched_at TEXT NOT NULL
            )
        """)

def save_search(db_path, query, method, result_count):
    with connect(db_path) as con:
        con.execute(
            "INSERT INTO searches(query, method, result_count, searched_at) VALUES (?, ?, ?, ?)",
            (query, method, result_count, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )

def get_history(db_path):
    with connect(db_path) as con:
        rows = con.execute(
            "SELECT query, method, result_count, searched_at FROM searches ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return rows

def clear_history(db_path):
    with connect(db_path) as con:
        con.execute("DELETE FROM searches")
