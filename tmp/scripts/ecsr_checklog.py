import os
"""ECSR-35331 item 1 - does CTRL_CHECK_LOG have a violation for the -8.5 Train 1 LNG Rundown record?
getValidations reads this log; if empty, no on-screen error shows. Read-only / SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:150]); return []


print("=== CTRL_CHECK_LOG overall freshness ===")
print("  total rows:", q("SELECT COUNT(*) FROM CTRL_CHECK_LOG")[0][0])
print("  max daytime:", q("SELECT MAX(daytime) FROM CTRL_CHECK_LOG")[0][0])
for c in ("CREATED_DATE", "LAST_UPDATED_DATE", "LOG_DATE", "RUN_DATE"):
    r = q(f"SELECT MAX({c}) FROM CTRL_CHECK_LOG")
    if r:
        print(f"  max {c}:", r[0][0])

print("\n=== any CTRL_CHECK_LOG rows for check 1040/1039/1041 (gas meas) ? ===")
print("  count by check_id:")
for r in q("""SELECT check_id, COUNT(*) FROM CTRL_CHECK_LOG WHERE check_id IN (1039,1040,1041)
              GROUP BY check_id ORDER BY check_id"""):
    print("   ", r)

print("\n=== log rows on 2026-05-12 (any check) ===")
print("  count:", q("SELECT COUNT(*) FROM CTRL_CHECK_LOG WHERE daytime=TO_DATE('2026-05-12','YYYY-MM-DD')")[0][0])

print("\n=== log rows mentioning LNG Rundown (any date) ===")
rows = q("""SELECT check_id, daytime, severity_level, status, SUBSTR(log_message,1,90)
            FROM CTRL_CHECK_LOG WHERE UPPER(log_message) LIKE '%LNG RUNDOWN%'
            ORDER BY daytime DESC FETCH FIRST 10 ROWS ONLY""")
print("  rows:", len(rows))
for r in rows:
    print("   ", r)

print("\n=== log rows mentioning 'negative or missing gross mass' (rule 1040 message) ===")
rows2 = q("""SELECT check_id, daytime, object_id, status, SUBSTR(log_message,1,90)
             FROM CTRL_CHECK_LOG WHERE UPPER(log_message) LIKE '%GROSS MASS%'
             ORDER BY daytime DESC FETCH FIRST 10 ROWS ONLY""")
print("  rows:", len(rows2))
for r in rows2:
    print("   ", r)

con.close()
print("\nDONE (read-only).")
