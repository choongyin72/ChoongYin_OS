import os
"""Validate: screen validation only shows AFTER the check rule is RUN (which populates CTRL_CHECK_LOG).
Read-only: find which PL/SQL writes CTRL_CHECK_LOG (the run engine), and confirm getValidations only reads.
SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:150]); return []


print("=== which PL/SQL objects INSERT/write CTRL_CHECK_LOG (the run engine) ===")
rows = q("""SELECT DISTINCT name, type FROM all_source
            WHERE owner='ECKERNEL_EC' AND UPPER(text) LIKE '%CTRL_CHECK_LOG%'
              AND (UPPER(text) LIKE '%INSERT%' OR UPPER(text) LIKE '%MERGE%')
            ORDER BY name""")
for r in rows:
    print("  ", r)

print("\n=== source lines that INSERT INTO CTRL_CHECK_LOG (engine + context) ===")
for r in q("""SELECT name, line, TRIM(text) FROM all_source
              WHERE owner='ECKERNEL_EC' AND UPPER(text) LIKE '%INSERT%CTRL_CHECK_LOG%'
              ORDER BY name, line""")[:15]:
    print(f"  {r[0]} :{r[1]}  {r[2][:110]}")

print("\n=== run-check procedures in pck_gen_check / check engine (names) ===")
for r in q("""SELECT DISTINCT name, TRIM(text) FROM all_source
              WHERE owner='ECKERNEL_EC' AND name LIKE 'PCK_GEN_CHECK%'
                AND (UPPER(text) LIKE '%PROCEDURE %' OR UPPER(text) LIKE '%FUNCTION %')
                AND (UPPER(text) LIKE '%RUN%' OR UPPER(text) LIKE '%CHECK%' OR UPPER(text) LIKE '%VALID%')
              ORDER BY name""")[:30]:
    print(f"  {r[0]}: {r[1][:110]}")

print("\n=== does getValidations (ZWP_P_TOOLTIP) only READ ctrl_check_log? (no insert) ===")
ins = q("""SELECT COUNT(*) FROM all_source WHERE owner='ECKERNEL_EC' AND name='ZWP_P_TOOLTIP'
           AND UPPER(text) LIKE '%INSERT%CTRL_CHECK_LOG%'""")
print("  ZWP_P_TOOLTIP inserts into CTRL_CHECK_LOG:", ins[0][0], "(0 = read-only/display)")

con.close()
print("\nDONE (read-only).")
