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


def view_count_where(view, column, value):
    """Count rows of ``view`` where ``column`` equals ``value`` (bind-safe).

    Built for delta-style assertions on shared/parent-child tables (e.g.
    OBJECT_LIST_SETUP): record the count before an insert, assert +1 after,
    assert back after the delete - pre-existing rows never matter.
    """
    _safe(view)
    _safe(column)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM {view} WHERE {column} = :v", v=value)
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def view_count_where_should_be(view, column, value, expected):
    """Fail unless ``view_count_where`` returns exactly ``expected``."""
    actual = view_count_where(view, column, value)
    if int(actual) != int(expected):
        raise AssertionError(
            f"DB check FAILED: {view}.{column} = {value!r} has {actual} rows, expected {expected}"
        )


def object_id_by_name(source, name):
    """Resolve an object's OBJECT_ID from its display NAME, via any name-bearing source.

    N1 day-status tables key on OBJECT_ID, but the grid shows the object NAME. ``source`` is the
    view/table that maps NAME->OBJECT_ID for that object type: WELL_VERSION for wells, OV_STREAM
    for streams, etc. (NAME is matched exactly.) Generic so every N1 screen reuses one helper.
    """
    _safe(source)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT OBJECT_ID FROM {source} WHERE NAME = :n FETCH FIRST 1 ROWS ONLY", n=name)
        row = cur.fetchone()
        if not row:
            raise AssertionError(f"Object named {name!r} not found in {source}")
        return row[0]
    finally:
        cur.close()
        conn.close()


def well_object_id_by_name(well_name):
    """Back-compat wrapper: resolve a well's OBJECT_ID from WELL_VERSION.NAME."""
    return object_id_by_name("WELL_VERSION", well_name)


def day_status_value(table, object_id, daytime, column):
    """Return a single measured value from an N1 day-status row (DB ground truth).

    ``table`` = e.g. PWEL_DAY_STATUS; key = (OBJECT_ID, DAYTIME date). ``column`` = a measured
    column (e.g. ON_STREAM_HRS, AVG_WH_PRESS). Returns None if the (object, day) row is absent.
    """
    _safe(table)
    _safe(column)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT {column} FROM {table} "
            f"WHERE OBJECT_ID = :o AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD')",
            o=object_id, d=str(daytime),
        )
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()


def day_status_value_should_be(table, object_id, daytime, column, expected):
    """Fail unless an N1 day-status measured value equals ``expected`` (numeric-tolerant).

    The trustworthy oracle for the N1 edit-in-place pattern: after the screen Save, assert the
    value really persisted to the (well x day) row — not that the grid optimistically showed it.
    """
    actual = day_status_value(table, object_id, daytime, column)
    expected_is_null = expected is None or (isinstance(expected, str) and expected.strip() == "")
    if expected_is_null:
        ok = actual is None
    else:
        try:
            ok = actual is not None and float(actual) == float(expected)
        except (TypeError, ValueError):
            ok = str(actual) == str(expected)
    if not ok:
        raise AssertionError(
            f"DB check FAILED: {table}.{column} for OBJECT_ID={object_id} on {daytime} "
            f"= {actual!r}, expected {expected!r}"
        )


def reset_day_status_value(table, object_id, daytime, column, value=None):
    """TEST-TEARDOWN ONLY: restore an N1 day-status measured cell to ``value`` (default NULL).

    NOT an oracle — the sole DB *write* in this library, used to leave the sandbox exactly as found
    after an edit-in-place test whose cell was NULL-original (so a faithful UI "revert to empty" is
    unreliable: clearing a cell can pop a save-confirmation modal). The assertion that proves coverage
    is still the UI->DB write verified read-only by ``day_status_value_should_be``; this only cleans up.
    """
    _safe(table)
    _safe(column)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE {table} SET {column} = :v "
            f"WHERE OBJECT_ID = :o AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD')",
            v=value, o=object_id, d=str(daytime),
        )
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()


# --- N1 sub-daily: intraday (datetime-keyed) day-status value ------------------------------------
# Sub-daily status tables (e.g. PWEL_SUB_DAY_STATUS) key on (OBJECT_ID, DAYTIME, SUMMER_TIME) where
# DAYTIME carries the TIME-OF-DAY — many intraday rows per object per day. So the daily helpers
# (which match TRUNC(DAYTIME)=date) would hit ALL the day's rows; these match the specific interval
# by date + hour-of-day (HH:MI). On a clean hourly day with a single SUMMER_TIME value, (object,
# date, HH:MI) uniquely identifies the row; ``summer_time`` can be passed to disambiguate a DST
# fall-back hour if ever needed.

def sub_day_status_value(table, object_id, date, hhmi, column, summer_time=None):
    """Return a measured value from a SUB-daily status row, keyed by (OBJECT_ID, date, HH:MI).

    ``date`` = 'YYYY-MM-DD', ``hhmi`` = 'HH:MI' (24h, e.g. '00:00'). Returns None if absent.
    """
    _safe(table)
    _safe(column)
    conn = _connect()
    cur = conn.cursor()
    try:
        sql = (
            f"SELECT {column} FROM {table} "
            f"WHERE OBJECT_ID = :o AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') "
            f"AND TO_CHAR(DAYTIME,'HH24:MI') = :h"
        )
        binds = {"o": object_id, "d": str(date), "h": str(hhmi)}
        if summer_time is not None:
            sql += " AND SUMMER_TIME = :s"
            binds["s"] = summer_time
        cur.execute(sql, binds)
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()


def sub_day_status_value_should_be(table, object_id, date, hhmi, column, expected, summer_time=None):
    """Fail unless a sub-daily measured value equals ``expected`` (numeric-tolerant; None = NULL).

    The trustworthy oracle for the sub-daily N1 edit-in-place pattern: after the screen Save, assert
    the value really persisted to the (object x interval) row — proving the cell maps to ``column``
    AND the datetime key resolves to exactly one intraday row.
    """
    actual = sub_day_status_value(table, object_id, date, hhmi, column, summer_time)
    expected_is_null = expected is None or (isinstance(expected, str) and expected.strip() == "")
    if expected_is_null:
        ok = actual is None
    else:
        try:
            ok = actual is not None and float(actual) == float(expected)
        except (TypeError, ValueError):
            ok = str(actual) == str(expected)
    if not ok:
        raise AssertionError(
            f"DB check FAILED: {table}.{column} for OBJECT_ID={object_id} on {date} {hhmi} "
            f"= {actual!r}, expected {expected!r}"
        )


def sub_day_status_value_should_be_approx(table, object_id, date, hhmi, column, expected, tolerance=0.05, summer_time=None):
    """Fail unless a sub-daily measured value is within ``tolerance`` of ``expected``.

    For UNIT-bearing columns (pressure/rate/temp) the EC grid shows configured units while the DB
    stores base/SI units (see reference_ec_ui_db_unit_conversion). A write-verify therefore checks
    DB_after ~= typed_display / factor, where the factor is derived live from UI_before / DB_before —
    so an exact equality would spuriously fail on the unit conversion + rounding. None = no row.
    """
    actual = sub_day_status_value(table, object_id, date, hhmi, column, summer_time)
    if actual is None:
        raise AssertionError(
            f"DB check FAILED: {table}.{column} for OBJECT_ID={object_id} on {date} {hhmi} is NULL, "
            f"expected ~{expected}"
        )
    if abs(float(actual) - float(expected)) > float(tolerance):
        raise AssertionError(
            f"DB check FAILED: {table}.{column} for OBJECT_ID={object_id} on {date} {hhmi} "
            f"= {actual}, expected ~{expected} (tolerance {tolerance})"
        )


def reset_sub_day_status_value(table, object_id, date, hhmi, column, value=None):
    """TEST-TEARDOWN ONLY: restore a sub-daily measured cell to ``value`` (default NULL) for the
    (OBJECT_ID, date, HH:MI) interval — leaves the sandbox as found after a null-original edit test.
    Same role as ``reset_day_status_value`` for the daily grid. Returns rows updated."""
    _safe(table)
    _safe(column)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE {table} SET {column} = :v "
            f"WHERE OBJECT_ID = :o AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') "
            f"AND TO_CHAR(DAYTIME,'HH24:MI') = :h",
            v=value, o=object_id, d=str(date), h=str(hhmi),
        )
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()


# --- N2: allocation conservation oracle ---------------------------------------------------------
# An allocation calc RUN distributes measured field/stream totals onto wells/streams, writing per-
# object quantities to the *_DAY_ALLOC tables (e.g. PWEL_DAY_ALLOC, key OBJECT_ID+DAYTIME). The
# calc-engine critique (DeepDiveLearnings/ecpedia-efk/calc-engine-insights.md) gives the invariants
# a correct allocation must satisfy — the "conservation oracle". The cheapest, always-true invariant
# is NO NEGATIVES: an allocated physical volume/mass/energy can never be < 0. (Sum-to-total and
# day->month roll-up need the network->members->measured-total mapping; staged as a later extension.)

def _alloc_numeric_columns(cur, table):
    """The ALLOC_* numeric columns of an allocation result table (the quantities to invariant-check)."""
    cur.execute(
        "SELECT column_name FROM all_tab_columns "
        r"WHERE table_name = :t AND column_name LIKE 'ALLOC\_%' ESCAPE '\' "
        "AND data_type IN ('NUMBER','FLOAT','BINARY_DOUBLE','BINARY_FLOAT') ORDER BY column_id",
        t=table.upper(),
    )
    return [r[0] for r in cur.fetchall()]


def allocation_row_count(table, daytime):
    """Count allocation result rows in ``table`` on ``daytime`` (YYYY-MM-DD).

    Guards the no-negatives check from being vacuously true on a day with no allocation data.
    """
    _safe(table)
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            f"SELECT COUNT(*) FROM {table} WHERE TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD')",
            d=str(daytime),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def allocation_negative_count(table, daytime):
    """Count rows on ``daytime`` where ANY ALLOC_* numeric quantity is negative (should be 0)."""
    _safe(table)
    conn = _connect()
    cur = conn.cursor()
    try:
        cols = _alloc_numeric_columns(cur, table)
        if not cols:
            raise AssertionError(f"No ALLOC_* numeric columns found on {table}")
        preds = " OR ".join(f"{_safe(c)} < 0" for c in cols)
        cur.execute(
            f"SELECT COUNT(*) FROM {table} "
            f"WHERE TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') AND ({preds})",
            d=str(daytime),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def allocation_conservation_should_hold(table, daytime):
    """Conservation oracle (no-negatives) on an allocation result table for ``daytime``.

    Fails if the day has no allocation rows (nothing to verify) or if any allocated ALLOC_*
    quantity is negative. The trustworthy ground-truth assertion for an allocation RUN: the calc
    may report "Success" in the UI log, but only the DB invariants prove the result is sane.
    """
    rows = allocation_row_count(table, daytime)
    if int(rows) == 0:
        raise AssertionError(
            f"Conservation check FAILED: {table} has NO allocation rows on {daytime} "
            f"(nothing to verify — wrong date or the run wrote nothing)"
        )
    neg = allocation_negative_count(table, daytime)
    if int(neg) != 0:
        raise AssertionError(
            f"Conservation check FAILED: {table} on {daytime} has {neg} row(s) with a negative "
            f"ALLOC_* quantity (allocated volumes/masses/energy must be >= 0)"
        )


# --- N3: status-process (P->V->A record-status engine) oracle -----------------------------------
# A "status process" run (HA.0001) lifts RECORD_STATUS on the scoped day-status rows
# (Provisional 'P' -> Verified 'V' -> Approved 'A') and appends a row to STAT_PROCESS_STATUS with
# ROWS_UPDATED = how many rows it lifted. The run is async (executed by the ec-worker scheduler
# node; see DeepDiveLearnings/ec-bpm/ec-worker-and-scheduler.md), so the suite polls the DB for the
# result. Ground-truth oracle = the engine's ROWS_UPDATED self-report AND the actual RECORD_STATUS
# transition count in the data must AGREE. Self-clean = DB-restore V->P (the EC reverse process
# lifts 0 rows here, so a scoped restore is the reliable teardown — like reset_day_status_value).

_STATUS_FAMILY_SQL = (
    "SELECT table_name FROM all_tables WHERE owner = :o "
    "AND (table_name LIKE '%DAY_STATUS' OR table_name = 'STRM_DAY_STREAM' "
    "OR table_name = 'OBJECT_DAY_WEATHER') AND table_name NOT LIKE '%JN'"
)


def _status_family_tables(cur):
    """The day-status family: every %DAY_STATUS table + STRM_DAY_STREAM + OBJECT_DAY_WEATHER
    (excluding journal %JN tables). The proven P1_FwdUpd lift writes only within this family, and a
    broad 6382-table scan confirmed nothing outside it changes — so scoping the V-count oracle and
    the restore to this family is both correct and fast (~10 tables)."""
    cur.execute(_STATUS_FAMILY_SQL, o=os.environ.get("EC_DB_USER", "ECKERNEL_EC"))
    return [r[0] for r in cur.fetchall()]


def record_status_family_count(daytime, status):
    """Total day-status rows on ``daytime`` (YYYY-MM-DD) with RECORD_STATUS = ``status`` across the
    whole day-status family. The data-side oracle for a status-process lift: the Verified ('V')
    count goes 0 -> ROWS_UPDATED after a P->V run, and back to 0 after the self-clean restore."""
    conn = _connect()
    cur = conn.cursor()
    try:
        total = 0
        for t in _status_family_tables(cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {t} "
                f"WHERE TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') AND RECORD_STATUS = :s",
                d=str(daytime), s=status,
            )
            total += cur.fetchone()[0]
        return total
    finally:
        cur.close()
        conn.close()


def status_process_run_count(process_id, daytime):
    """COUNT(*) of STAT_PROCESS_STATUS log rows for ``process_id`` on ``daytime``.

    STAT_PROCESS_STATUS is an append-only run log (one row per run), so absence of a run can't be
    asserted once a prior run has logged — the suite captures this baseline, fires the run, then
    polls for a +1 delta to prove a FRESH run landed.
    """
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT COUNT(*) FROM STAT_PROCESS_STATUS "
            "WHERE PROCESS_ID = :p AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD')",
            p=process_id, d=str(daytime),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def latest_status_process_rows_updated(process_id, daytime):
    """ROWS_UPDATED from the most-recent STAT_PROCESS_STATUS run row for ``process_id``/``daytime``
    (the engine's own self-report of how many rows it lifted). Returns None if no run row exists."""
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT ROWS_UPDATED FROM STAT_PROCESS_STATUS "
            "WHERE PROCESS_ID = :p AND TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') "
            "ORDER BY RUN_DAYTIME DESC FETCH FIRST 1 ROWS ONLY",
            p=process_id, d=str(daytime),
        )
        row = cur.fetchone()
        return row[0] if row else None
    finally:
        cur.close()
        conn.close()


def restore_record_status_family(daytime, from_status="V", to_status="P"):
    """TEST-TEARDOWN ONLY: restore RECORD_STATUS on ``daytime`` from ``from_status`` back to
    ``to_status`` across the whole day-status family — leaves the sandbox exactly as found after a
    status-process P->V lift. The EC reverse process lifts 0 rows here, so this scoped DB-restore is
    the reliable self-clean (the only RECORD_STATUS write in this library). Returns rows restored."""
    conn = _connect()
    cur = conn.cursor()
    try:
        total = 0
        for t in _status_family_tables(cur):
            cur.execute(
                f"UPDATE {t} SET RECORD_STATUS = :ts "
                f"WHERE TRUNC(DAYTIME) = TO_DATE(:d,'YYYY-MM-DD') AND RECORD_STATUS = :fs",
                ts=to_status, d=str(daytime), fs=from_status,
            )
            total += cur.rowcount
        conn.commit()
        return total
    finally:
        cur.close()
        conn.close()


def record_status_family_count_month(month_date, status):
    """MONTH-grain counterpart of record_status_family_count: total day-status rows whose DAYTIME
    falls in the WHOLE calendar month of ``month_date`` (YYYY-MM-DD) with RECORD_STATUS = ``status``
    across the day-status family. Use for MONTH-grain status processes whose lift has no WHERE filter
    and may span every day of the month (a single-day count would miss the rest of the month). Day-
    grain suites keep using record_status_family_count."""
    conn = _connect()
    cur = conn.cursor()
    try:
        total = 0
        for t in _status_family_tables(cur):
            cur.execute(
                f"SELECT COUNT(*) FROM {t} "
                f"WHERE TRUNC(DAYTIME,'MM') = TRUNC(TO_DATE(:d,'YYYY-MM-DD'),'MM') "
                f"AND RECORD_STATUS = :s",
                d=str(month_date), s=status,
            )
            total += cur.fetchone()[0]
        return total
    finally:
        cur.close()
        conn.close()


def restore_record_status_family_month(month_date, from_status="A", to_status="P"):
    """TEST-TEARDOWN ONLY (MONTH grain): restore RECORD_STATUS across EVERY day of the calendar month
    of ``month_date`` over the day-status family — the month-grain counterpart of
    restore_record_status_family, for a monthly status process whose lift may span the whole month
    (a single-day restore would leave residual 'A' on the other days). Returns rows restored."""
    conn = _connect()
    cur = conn.cursor()
    try:
        total = 0
        for t in _status_family_tables(cur):
            cur.execute(
                f"UPDATE {t} SET RECORD_STATUS = :ts "
                f"WHERE TRUNC(DAYTIME,'MM') = TRUNC(TO_DATE(:d,'YYYY-MM-DD'),'MM') "
                f"AND RECORD_STATUS = :fs",
                ts=to_status, d=str(month_date), fs=from_status,
            )
            total += cur.rowcount
        conn.commit()
        return total
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
