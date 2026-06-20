"""READ-ONLY: pick Water vs Gas injection + a data-bearing scope for the IFLW N1 build.
INJ_TYPE distribution overall + on the best dates, and the flowlinexdate with ON_STREAM_HRS already set
(so an edit->diff has a clean target). NO writes."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
print("=== INJ_TYPE distribution (all P rows) ===")
cur.execute("SELECT INJ_TYPE, COUNT(*), COUNT(DISTINCT OBJECT_ID) flowlines FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P' GROUP BY INJ_TYPE ORDER BY 2 DESC")
for r in cur.fetchall(): print("  ", r)
print("\n=== best (date x INJ_TYPE) by distinct flowlines ===")
cur.execute("""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, INJ_TYPE, COUNT(DISTINCT OBJECT_ID) fl, COUNT(*) rows_
 FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P' GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD'), INJ_TYPE
 ORDER BY fl DESC, d DESC FETCH FIRST 10 ROWS ONLY""")
for r in cur.fetchall(): print("  ", r)
print("\n=== sample flowlines with ON_STREAM_HRS already SET (clean edit->diff target) ===")
cur.execute("""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, INJ_TYPE, OBJECT_ID, ON_STREAM_HRS, INJ_VOL
 FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P' AND ON_STREAM_HRS IS NOT NULL
 ORDER BY DAYTIME DESC FETCH FIRST 8 ROWS ONLY""")
for r in cur.fetchall(): print("  ", r)
con.close();print("DONE")
