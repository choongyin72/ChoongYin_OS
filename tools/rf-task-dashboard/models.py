"""SQLite task store for the RF EC-screen conversion task board.

Statuses (in normal flow order): unclaimed -> in_progress -> pr_raised ->
changes_requested (loops back to in_progress) -> merged. `blocked` is an
exception state reachable from in_progress or pr_raised.
"""
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent / "tasks.db"

VALID_STATUSES = (
    "unclaimed",
    "in_progress",
    "pr_raised",
    "changes_requested",
    "merged",
    "blocked",
)


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            screen_name TEXT NOT NULL UNIQUE,
            pattern TEXT NOT NULL DEFAULT 'UNKNOWN',
            status TEXT NOT NULL DEFAULT 'unclaimed',
            claimed_by TEXT,
            pr_number INTEGER,
            blocker_note TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
            from_status TEXT,
            to_status TEXT NOT NULL,
            note TEXT,
            timestamp TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()


def list_tasks(status=None):
    conn = get_conn()
    if status:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE status = ? ORDER BY updated_at DESC", (status,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tasks ORDER BY updated_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_task(task_id):
    conn = get_conn()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_history(task_id):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM task_history WHERE task_id = ? ORDER BY timestamp ASC", (task_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_task(screen_name, pattern="UNKNOWN"):
    conn = get_conn()
    now = _now()
    cur = conn.execute(
        "INSERT INTO tasks (screen_name, pattern, status, created_at, updated_at) "
        "VALUES (?, ?, 'unclaimed', ?, ?)",
        (screen_name.strip(), pattern, now, now),
    )
    task_id = cur.lastrowid
    conn.execute(
        "INSERT INTO task_history (task_id, from_status, to_status, note, timestamp) "
        "VALUES (?, NULL, 'unclaimed', 'task added', ?)",
        (task_id, now),
    )
    conn.commit()
    conn.close()
    return task_id


def claim_task(task_id, claimed_by):
    conn = get_conn()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        return None, "task not found"
    if task["status"] != "unclaimed":
        conn.close()
        return None, f"task is not unclaimed (current status: {task['status']})"
    now = _now()
    conn.execute(
        "UPDATE tasks SET status = 'in_progress', claimed_by = ?, updated_at = ? WHERE id = ?",
        (claimed_by, now, task_id),
    )
    conn.execute(
        "INSERT INTO task_history (task_id, from_status, to_status, note, timestamp) "
        "VALUES (?, 'unclaimed', 'in_progress', ?, ?)",
        (task_id, f"claimed by {claimed_by}", now),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(updated), None


def update_status(task_id, new_status, note=None, pr_number=None):
    if new_status not in VALID_STATUSES:
        return None, f"invalid status: {new_status}"
    conn = get_conn()
    task = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if not task:
        conn.close()
        return None, "task not found"
    now = _now()
    fields = ["status = ?", "updated_at = ?"]
    params = [new_status, now]
    if pr_number is not None:
        fields.append("pr_number = ?")
        params.append(pr_number)
    if new_status == "blocked":
        fields.append("blocker_note = ?")
        params.append(note or "")
    elif new_status in ("unclaimed", "merged"):
        fields.append("claimed_by = NULL")
    params.append(task_id)
    conn.execute(f"UPDATE tasks SET {', '.join(fields)} WHERE id = ?", params)
    conn.execute(
        "INSERT INTO task_history (task_id, from_status, to_status, note, timestamp) "
        "VALUES (?, ?, ?, ?, ?)",
        (task_id, task["status"], new_status, note, now),
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(updated), None


def summary():
    conn = get_conn()
    rows = conn.execute("SELECT status, COUNT(*) as n FROM tasks GROUP BY status").fetchall()
    conn.close()
    counts = {s: 0 for s in VALID_STATUSES}
    for r in rows:
        counts[r["status"]] = r["n"]
    counts["total"] = sum(counts[s] for s in VALID_STATUSES)
    return counts
