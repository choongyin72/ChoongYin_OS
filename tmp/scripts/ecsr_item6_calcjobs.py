import os
"""ECSR-35331 item 6 - identify the 'Calculation Job' options on the Daily Allocation screen + which is
defunct. Read-only. Finds where the calc-job list ('02 Onshore Daily Allocation' etc.) is stored and lists
all entries (active vs defunct/end-dated). SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:150]); return []


# 1) find columns whose data holds the calc job names
print("=== search tables for a column containing 'Onshore Daily Allocation' ===")
cands = q("""SELECT owner, table_name, column_name FROM all_tab_columns
             WHERE owner='ECKERNEL_EC' AND data_type IN ('VARCHAR2','CHAR','NVARCHAR2')
               AND (column_name LIKE '%NAME%' OR column_name LIKE '%DESC%' OR column_name LIKE '%LABEL%'
                    OR column_name LIKE '%JOB%' OR column_name LIKE '%CODE%')
               AND (table_name LIKE '%CALC%' OR table_name LIKE '%ALLOC%' OR table_name LIKE '%JOB%'
                    OR table_name LIKE '%BATCH%' OR table_name LIKE '%TASK%')
             ORDER BY table_name, column_name""")
print(f"  candidate columns: {len(cands)}")
for o, t, c in cands[:40]:
    print(f"   {t}.{c}")

# 2) probe each candidate for the calc-job names
print("\n=== probe candidates for 'Onshore Daily' / 'Commercial Calculation' ===")
seen = set()
for o, t, c in cands:
    if (t, c) in seen:
        continue
    seen.add((t, c))
    hit = q(f"""SELECT DISTINCT {c} FROM {t}
                WHERE UPPER({c}) LIKE '%ONSHORE DAILY%' OR UPPER({c}) LIKE '%COMMERCIAL CALCULATION%'
                   OR UPPER({c}) LIKE '%DAILY ALLOCATION%' """)
    if hit:
        print(f"\n  >>> {t}.{c} matches:")
        for h in hit[:20]:
            print("       ", h[0])

con.close()
print("\nDONE (read-only).")
