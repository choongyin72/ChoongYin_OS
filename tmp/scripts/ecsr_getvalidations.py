import os
"""Validate ZWP_P_TOOLTIP.getValidations - the custom screen-validation routine. Read-only: pull the
package-body source from ECAASDEV and print the getValidations function (esp. how it selects check rules
from CTRL_CHECK_* and any RECORD_STATUS / APPROVAL_STATE / ZWP_SCREEN_VAL filters). SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    cur.execute(sql, a or []); return cur.fetchall()


# locate the package + the getValidations function line range
print("=== ZWP_P_TOOLTIP objects ===")
for r in q("""SELECT object_type, status FROM all_objects WHERE owner='ECKERNEL_EC'
              AND object_name='ZWP_P_TOOLTIP'"""):
    print("  ", r)

src = q("""SELECT line, text FROM all_source WHERE owner='ECKERNEL_EC' AND name='ZWP_P_TOOLTIP'
           AND type='PACKAGE BODY' ORDER BY line""")
print(f"  package body lines: {len(src)}")

# find getValidations boundaries (case-insensitive)
lines = [(ln, t) for ln, t in src]
start = None
for i, (ln, t) in enumerate(lines):
    low = (t or "").lower()
    if ("function" in low or "procedure" in low) and "getvalidations" in low:
        start = i; break

if start is None:
    print("\n  getValidations not found by name; searching any 'getval' decls:")
    for ln, t in lines:
        if "getval" in (t or "").lower() and ("function" in (t or "").lower() or "procedure" in (t or "").lower()):
            print(f"   {ln}: {t.strip()[:120]}")
else:
    # print from start until the next top-level FUNCTION/PROCEDURE decl (heuristic) or +200 lines
    print(f"\n=== getValidations source (from line {lines[start][0]}) ===")
    depth_end = start + 1
    for j in range(start + 1, min(start + 260, len(lines))):
        low = (lines[j][1] or "").lower().strip()
        if (low.startswith("function ") or low.startswith("procedure ")) and "getvalidations" not in low:
            depth_end = j; break
        depth_end = j
    for j in range(start, depth_end):
        print(f"  {lines[j][0]:5d} {lines[j][1].rstrip() if lines[j][1] else ''}")

# also: any lines in the whole body referencing status/approval filters near CTRL_CHECK
print("\n=== body lines mentioning RECORD_STATUS / APPROVAL / SCREEN_VAL / CTRL_CHECK ===")
for ln, t in lines:
    low = (t or "").upper()
    if any(k in low for k in ("RECORD_STATUS", "APPROVAL_STATE", "ZWP_SCREEN_VAL", "SCREEN_VAL", "CTRL_CHECK")):
        print(f"  {ln:5d} {t.strip()[:140]}")

con.close()
print("\nDONE (read-only).")
