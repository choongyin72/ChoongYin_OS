"""EC DB ground-truth verify (reusable across OV object screens).

The UI can lie (optimistic state, silent rejects). A pass counts only when the DB agrees.
Queries the object view (ov_<screen>) by CODE. After an EC 'delete' (End Date = Start Date)
the row is removed from the ov_* view entirely, so presence == exists-in-view.

Env: EC_DB_DSN (localhost:1521/ORCL), EC_DB_USER (ECKERNEL_EC), EC_DB_PASS (energy).
"""
import os
import oracledb


def _connect():
    return oracledb.connect(
        user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
        password=os.environ.get("EC_DB_PASS", "energy"),
        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    )


def fetch_object(view, code):
    """Return the row for CODE from the object view as {COLNAME: value}, or None if absent."""
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute(f"select * from {view} where code = :c", c=code)
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        con.close()


def is_present(view, code):
    return fetch_object(view, code) is not None


def field_equals(view, code, column, expected):
    """True if the view row's column == expected (string compare, trimmed)."""
    row = fetch_object(view, code)
    if row is None:
        return False, None
    actual = row.get(column.upper())
    actual_s = "" if actual is None else str(actual).strip()
    return actual_s == str(expected).strip(), actual_s


def verify_row(view, code, expected):
    """Test-case helper. expected = {COLUMN: value}. Returns (all_ok, checks) where checks is a
    list of (column, expected, actual, ok). Missing row => all checks fail."""
    row = fetch_object(view, code)
    checks = []
    all_ok = row is not None
    for col, exp in expected.items():
        if row is None:
            checks.append((col, exp, None, False))
            continue
        actual = row.get(col.upper())
        actual_s = "" if actual is None else str(actual).strip()
        ok = actual_s == str(exp).strip()
        all_ok = all_ok and ok
        checks.append((col, exp, actual_s, ok))
    return all_ok, checks


def count_like(view, code_prefix):
    """Count rows whose CODE starts with prefix (residual self-clean check)."""
    con = _connect()
    try:
        cur = con.cursor()
        cur.execute(f"select count(*) from {view} where code like :p", p=code_prefix + "%")
        return cur.fetchone()[0]
    finally:
        con.close()
