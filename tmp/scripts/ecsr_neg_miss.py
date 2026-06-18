import os
"""ECSR-35331 - (1) negative-value rules: attribute/column + screen, to group neg items with item 1.
(2) missing-data rules: which attributes are actually mandatory-checked per stream class (validate items
7/9/10/11). Read-only / SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:150]); return []


def attr(check_id):
    """the ATTRIBUTE-type variable value(s) for a rule = the actual column checked."""
    rows = q("""SELECT VARIABLE_NAME, VARIABLE_VALUE FROM CTRL_CHECK_RULE_VARIABLE
                WHERE CHECK_ID=:c AND VARIABLE_TYPE='ATTRIBUTE' ORDER BY VARIABLE_NAME""", [check_id])
    return ", ".join(f"{v}" for _, v in rows)


print("=== (1) NEGATIVE-value check rules (WHERE has '< 0') ===")
negs = q("""SELECT CHECK_ID, CHECK_NAME, TABLE_ID, SEVERITY_LEVEL, ZWP_SCREEN_VAL
            FROM TV_CTRL_CHECK_RULES WHERE WHERE_FORMULA LIKE '%< 0%' ORDER BY TABLE_ID, CHECK_ID""")
for cid, cn, tbl, sev, sv in negs:
    print(f"  [{cid}] {cn:34s} tbl={tbl:30s} sev={sev:7s} screenVal={sv}  attr=({attr(cid)})")

print("\n=== (2) MISSING-data check rules (WHERE has 'IS NULL') ===")
miss = q("""SELECT CHECK_ID, CHECK_NAME, TABLE_ID, SEVERITY_LEVEL, ZWP_SCREEN_VAL
            FROM TV_CTRL_CHECK_RULES WHERE UPPER(WHERE_FORMULA) LIKE '%IS NULL%' ORDER BY TABLE_ID, CHECK_ID""")
for cid, cn, tbl, sev, sv in miss:
    print(f"  [{cid}] {cn:42s} tbl={tbl:30s} sev={sev:7s} screenVal={sv}  attr=({attr(cid)})")

print("\n=== gas-stream coverage summary (RV_STRM_DAY_STREAM_MEAS_GAS) ===")
print("  NEGATIVE rules on gas:", [r[0] for r in negs if 'MEAS_GAS' in (r[2] or '')])
print("  MISSING rules on gas :", [r[0] for r in miss if 'MEAS_GAS' in (r[2] or '')])

con.close()
print("\nDONE (read-only).")
