"""Robot Framework keyword library — verify EC data at the DATABASE (ground truth).

The web UI can lie (optimistic client state, silent rejects, pagination); the DB
is the source of truth. These keywords let a suite assert presence/absence of a
record directly in an EC view/table, so a PASS means the data really persisted
(or was really deleted), not just that the screen looked right.

Generic across screens: pass the view name (e.g. ov_bank, OV_EQPM,
CTRL_MIME_TYPE_MAPPING) and the code. The code is matched against any VARCHAR
column of the view, so callers need not know which column holds it.

Connection resolves from OS env vars with local-sandbox fallbacks:
  EC_DB_USER (ECKERNEL_EC) / EC_DB_PASS (energy) / EC_DB_DSN (localhost:1521/ORCL)
Uses oracledb thin mode (no Oracle client needed). Read-only.
"""
import os
import re

import oracledb

_IDENT = re.compile(r"[A-Za-z0-9_]+")


def _connect():
    return oracledb.connect(
        user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
        password=os.environ.get("EC_DB_PASS", "energy"),
        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
        tcp_connect_timeout=15,
    )


def _safe(identifier):
    if not _IDENT.fullmatch(identifier or ""):
        raise ValueError(f"Unsafe SQL identifier: {identifier!r}")
    return identifier


def _string_columns(cur, view):
    cur.execute(
        "SELECT column_name FROM all_tab_columns "
        "WHERE table_name = :v AND data_type LIKE '%CHAR%' ORDER BY column_id",
        v=view.upper(),
    )
    return [r[0] for r in cur.fetchall()]


def _code_present(view, code):
    _safe(view)
    conn = _connect()
    cur = conn.cursor()
    try:
        for col in _string_columns(cur, view):
            cur.execute(f'SELECT COUNT(*) FROM {view} WHERE "{col}" = :c', c=code)
            if cur.fetchone()[0]:
                return True
        return False
    finally:
        cur.close()
        conn.close()


def view_row_count(view):
    """Return the total row count of an EC view/table (e.g. ov_bank)."""
    _safe(view)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {view}")
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def code_should_be_present_in_view(view, code):
    """Fail unless ``code`` appears in any string column of ``view`` (DB ground truth)."""
    if not _code_present(view, code):
        raise AssertionError(f"DB check FAILED: {code} not found in {view} (expected present)")


def code_should_be_absent_in_view(view, code):
    """Fail if ``code`` appears in any string column of ``view`` (DB ground truth)."""
    if _code_present(view, code):
        raise AssertionError(f"DB check FAILED: {code} still present in {view} (expected absent)")
