"""READ-ONLY: find the best UNCOVERED N1 daily-status grid target — list %DAY_STATUS tables with row
counts + RECORD_STATUS spread. Already covered: PWEL, IWEL, STRM(_DAY_STREAM), EQPM, PFLW(flowline)."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
 AND table_name LIKE '%DAY_STATUS' AND table_name NOT LIKE '%_JN' ORDER BY table_name""")
tabs=[r[0] for r in cur.fetchall()]
print(f"{len(tabs)} %DAY_STATUS tables\n")
covered={'PWEL_DAY_STATUS','IWEL_DAY_STATUS','STRM_DAY_STATUS','EQPM_DAY_STATUS'}
rows=[]
for t in tabs:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        n=cur.fetchone()[0]
        cur.execute(f"SELECT RECORD_STATUS, COUNT(*) FROM {t} GROUP BY RECORD_STATUS ORDER BY 2 DESC")
        st=cur.fetchall()
        rows.append((n,t,st))
    except Exception as e: rows.append((-1,t,str(e)[:40]))
rows.sort(reverse=True)
for n,t,st in rows:
    mark="  [COVERED]" if t in covered else ""
    print(f"{n:>8}  {t}{mark}  {st}")
con.close();print("\nDONE")
