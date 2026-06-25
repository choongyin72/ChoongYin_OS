"""MHM SME recon step 3 (read-only): is the live notification configured + what's the journal domain
+ where's the Todo/task half. Checks: MESSAGE_DEFINITION codes (8), DISTRIBUTION_SET codes/names (4),
MHM_MSG distinct MSG_TYPE/DIRECTION/STATUS, search for N_R_D_VALIDATION_REVIEW anywhere, and find the
Todo/task table."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password=os.environ.get('EC_DB_PWD', 'energy'),
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, n=20):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql)
        d = [x[0] for x in cur.description]
        print("  " + " | ".join(d))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:46] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:150])


show("MESSAGE_DEFINITION codes (the 8 message types)",
     "SELECT OBJECT_CODE, TO_CHAR(START_DATE,'YYYY-MM-DD') sd, RECORD_STATUS FROM MESSAGE_DEFINITION ORDER BY OBJECT_CODE")
show("DISTRIBUTION_SET (the 4 dist lists)",
     "SELECT DISTRIBUTION_SET_CODE, NAME, RECORD_STATUS FROM DISTRIBUTION_SET ORDER BY 1")
show("MHM_MSG journal domain (distinct MSG_TYPE / DIRECTION / STATUS counts)",
     "SELECT MSG_TYPE, DIRECTION, STATUS, COUNT(*) n FROM MHM_MSG GROUP BY MSG_TYPE, DIRECTION, STATUS ORDER BY n DESC")
# search for the live notification code anywhere it might be configured
for t, col in (("MESSAGE_DEFINITION", "OBJECT_CODE"), ("MESSAGE_DISTRIBUTION", None)):
    try:
        if col:
            cur.execute(f"SELECT COUNT(*) FROM {t} WHERE UPPER({col}) LIKE '%VALID%' OR UPPER({col}) LIKE 'N_R%'")
            print(f"\n  {t}.{col} matching VALID/N_R: {cur.fetchone()[0]}")
    except Exception as e:
        print(f"  {t} ERR", str(e)[:80])
# find the Todo/task table (the in-app notification half)
show("candidate TODO/TASK tables",
     "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name NOT LIKE '%JN' "
     "AND (table_name LIKE '%TODO%' OR table_name LIKE '%TASK%' OR table_name LIKE '%WORK_ITEM%' "
     "OR table_name LIKE '%WORKITEM%' OR table_name LIKE '%REVIEW%') ORDER BY table_name", n=30)
cur.close(); c.close(); print("\nDONE")
