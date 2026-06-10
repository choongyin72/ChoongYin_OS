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


def check_log_count(check_id, daytime):
    """Count CTRL_CHECK_LOG rows for a check rule (CHECK_ID) on a DAYTIME (YYYY-MM-DD).

    This is EC's validation OUTPUT table — a row per rule violation produced when a
    check group is run. Used to assert a UI-triggered validation matches DB ground truth.
    """
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT COUNT(*) FROM CTRL_CHECK_LOG "
            "WHERE CHECK_ID = :id AND DAYTIME = TO_DATE(:d, 'YYYY-MM-DD')",
            id=int(check_id), d=str(daytime),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def check_log_count_should_be(check_id, daytime, expected):
    """Fail unless CTRL_CHECK_LOG has exactly ``expected`` rows for CHECK_ID on DAYTIME."""
    actual = check_log_count(check_id, daytime)
    if int(actual) != int(expected):
        raise AssertionError(
            f"DB check FAILED: CTRL_CHECK_LOG CHECK_ID={check_id} on {daytime} "
            f"= {actual} rows, expected {expected}"
        )


def distinct_violation_objects_for_rule(check_id, daytime):
    """Independent oracle, computed from SOURCE data using the rule's OWN deployed logic.

    Reads the check rule's TABLE_ID + WHERE_FORMULA from CTRL_CHECK_RULES (and its
    ${variable} -> column mapping from CTRL_CHECK_RULE_VARIABLE), substitutes the real
    columns, and returns COUNT(DISTINCT OBJECT_ID) of violating objects on ``daytime``.

    EC logs ONE row per violating object (e.g. a stream is flagged once even if many of
    its component rows are bad), so this distinct-object count is the correct yardstick to
    compare against CTRL_CHECK_LOG and the UI Summary. Using the rule's own WHERE_FORMULA
    keeps the oracle faithful to what was deployed (it can't drift from the rule).
    """
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT TABLE_ID, WHERE_FORMULA FROM CTRL_CHECK_RULES WHERE CHECK_ID = :i",
            i=int(check_id),
        )
        row = cur.fetchone()
        if not row:
            raise AssertionError(f"Check rule CHECK_ID={check_id} not found")
        table_id, where_formula = row
        _safe(table_id)
        cur.execute(
            "SELECT VARIABLE_NAME, VARIABLE_VALUE FROM CTRL_CHECK_RULE_VARIABLE WHERE CHECK_ID = :i",
            i=int(check_id),
        )
        pred = where_formula
        for var_name, var_col in cur.fetchall():
            pred = pred.replace("${" + var_name + "}", var_col)
        cur.execute(
            f"SELECT COUNT(DISTINCT OBJECT_ID) FROM {table_id} "
            f"WHERE DAYTIME = TO_DATE(:d,'YYYY-MM-DD') AND ({pred})",
            d=str(daytime),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def frozen_distinct_violation_objects(check_id, daytime):
    """Faithful oracle for a FROZEN function-rule (ZWP_P_TOOLTIP.getValFrozenValue).

    distinct_violation_objects_for_rule() can't handle these — their WHERE_FORMULA vars are
    a package name + 'FROZEN' const, not columns. So derive the oracle from the rule's OWN
    func-params: read TABLE_ID + the P_VALUE column + P_ATTRIBUTE const, then COUNT(DISTINCT
    OBJECT_ID) where getValFrozenValue(...) = 'FROZEN' on ``daytime``. Stays faithful to the
    deployed rule (can't drift). EC logs one row per frozen object -> compare to CTRL_CHECK_LOG.
    """
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT TABLE_ID FROM CTRL_CHECK_RULES WHERE CHECK_ID = :i", i=int(check_id))
        row = cur.fetchone()
        if not row:
            raise AssertionError(f"Check rule CHECK_ID={check_id} not found")
        table_id = _safe(row[0])
        cur.execute(
            "SELECT PARAMETER_NAME, PARAMETER_VALUE FROM CTRL_CHECK_RULE_FUNC_PARAM "
            "WHERE CHECK_ID = :i AND PARAMETER_NAME IN ('P_VALUE','P_ATTRIBUTE')",
            i=int(check_id),
        )
        params = {n: v for n, v in cur.fetchall()}
        valcol = _safe(params["P_VALUE"])
        attr = params["P_ATTRIBUTE"]
        cur.execute(
            f"SELECT COUNT(DISTINCT OBJECT_ID) FROM {table_id} "
            f"WHERE DAYTIME = TO_DATE(:d,'YYYY-MM-DD') AND {valcol} IS NOT NULL "
            f"AND ZWP_P_TOOLTIP.getValFrozenValue(DATA_CLASS_NAME,OBJECT_ID,DAYTIME,{valcol},:a)='FROZEN'",
            d=str(daytime), a=attr,
        )
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
