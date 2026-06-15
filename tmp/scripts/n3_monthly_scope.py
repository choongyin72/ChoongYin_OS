"""READ-ONLY: does the monthly approve (P1_FwdUpdPar1 -> IWEL_DAY_STATUS_AIR/_CO2) have liftable rows?
Check row counts + RECORD_STATUS distribution + dates. Decides build-vs-park. NO writes."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
for tbl in ("IWEL_DAY_STATUS_AIR","IWEL_DAY_STATUS_CO2"):
    print(f"\n=== {tbl} ===")
    try:
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        print("total rows:", cur.fetchone()[0])
        cur.execute(f"SELECT RECORD_STATUS, COUNT(*) FROM {tbl} GROUP BY RECORD_STATUS ORDER BY 1")
        print("by RECORD_STATUS:", cur.fetchall())
        cur.execute(f"SELECT TO_CHAR(DAYTIME,'YYYY-MM') ym, RECORD_STATUS, COUNT(*) FROM {tbl} GROUP BY TO_CHAR(DAYTIME,'YYYY-MM'), RECORD_STATUS ORDER BY 1 DESC")
        rows=cur.fetchall()
        print("by month x status (top 12):")
        for r in rows[:12]: print("  ", r)
    except Exception as e: print("ERR:",str(e)[:160])
# also: P1_FwdUpdPar1 FROM level (what it approves from) + its variables
print("\n=== P1_FwdUpdPar1 detail ===")
cur.execute("SELECT PROCESS_ID, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, REVERSE_FLAG FROM STATUS_PROCESS WHERE PROCESS_ID='P1_FwdUpdPar1'")
print(cur.fetchall())
con.close();print("\nDONE")
