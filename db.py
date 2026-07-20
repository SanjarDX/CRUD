import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "tasks.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def _row_to_task(row: sqlite3.Row) -> dict:
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                done BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )
        count = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            conn.executemany(
                "INSERT INTO tasks (title, done) VALUES (?, ?)",
                [
                    ("Buy milk", False),
                    ("Write README", False),
                    ("Learn FastAPI", True),
                ],
            )


def list_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT id, title, done FROM tasks ORDER BY id").fetchall()
        return [_row_to_task(row) for row in rows]


def get_task(task_id: int) -> Optional[dict]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return _row_to_task(row) if row else None


def create_task(title: str) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, done) VALUES (?, 0)", (title,)
        )
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
        return _row_to_task(row)


def update_task(
    task_id: int, title: Optional[str], done: Optional[bool]
) -> Optional[dict]:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE tasks
            SET title = COALESCE(?, title),
                done = COALESCE(?, done)
            WHERE id = ?
            """,
            (title, done, task_id),
        )
        row = conn.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        return _row_to_task(row) if row else None


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0
