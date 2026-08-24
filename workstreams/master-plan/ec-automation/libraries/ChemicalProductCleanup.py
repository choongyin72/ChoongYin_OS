"""Robot Framework keyword library - Chemical Product screen-scoped delete workaround.

SCREEN-SPECIFIC, deliberately NOT added to the shared libraries/DbVerify.py (which is
read-only by design) or resources/manage_object.resource (the shared T2 delete keyword's
contract - End Date = Start Date via the UI - is used unmodified by every OTHER OV screen).

Documented root cause (ec-ui-knowledge/EC_KNOWN_ISSUES.md, "OV_CHEM_PRODUCT (Chemical
Product, CO.0072) - End=Start delete blocked by a child-FK dependency", confirmed root cause,
2026-07-26/31): CHEM_PRODUCT is VERSIONED, but EC auto-creates a 1:1 CHEM_USAGE_REPORT_CONF
child row on every product insert. That child's OBJECT_ID FK to CHEM_PRODUCT.OBJECT_ID has
delete rule NO ACTION, so the standard zero-length-window (End Date = Start Date) close is
rejected by the DB (ORA-02292 -> the IUD_CHEM_PRODUCT trigger's ORA-20102). The web UI
swallows both errors, so End Date fills, Save clicks, no error shows, but
OV_CHEM_PRODUCT.OBJECT_END_DATE stays NULL - a genuine EC PRODUCT DEFECT, not an automation
gap. There is NO UI screen for CHEM_USAGE_REPORT_CONF (verified against DefaultScreenTreeview,
2026-07-31), so the fix documented by that same KNOWN_ISSUES entry - remove the child row at
DB level FIRST, then the normal UI End=Start action persists correctly - is applied here.

Connection resolves the same way as DbVerify.py: EC_DB_USER (ECKERNEL_EC) / EC_DB_PASS
(energy) / EC_DB_DSN (localhost:1521/ORCL), oracledb thin mode.
"""
import os

import oracledb


def _connect():
    return oracledb.connect(
        user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
        password=os.environ.get("EC_DB_PASS", "energy"),
        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
        tcp_connect_timeout=15,
    )


def remove_chem_usage_report_conf_child(code):
    """Delete the auto-created CHEM_USAGE_REPORT_CONF row for the Chemical Product identified
    by ``code`` (CHEM_PRODUCT.OBJECT_CODE), so the standard UI End=Start delete that follows
    this keyword no longer hits the NO-ACTION child-FK block. Returns the number of child rows
    removed (0 if the product code doesn't exist, or it never had a child row - both are
    treated as a no-op, not a failure, so this keyword is safe to call unconditionally before
    Delete Object Via End Date).
    """
    conn = _connect()
    try:
        cur = conn.cursor()
        cur.execute("SELECT OBJECT_ID FROM CHEM_PRODUCT WHERE OBJECT_CODE = :c", c=code)
        row = cur.fetchone()
        if not row:
            return 0
        object_id = row[0]
        cur.execute("DELETE FROM CHEM_USAGE_REPORT_CONF WHERE OBJECT_ID = :o", o=object_id)
        removed = cur.rowcount
        conn.commit()
        return removed
    finally:
        conn.close()
