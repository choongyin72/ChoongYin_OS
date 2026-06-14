import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:10]: print("  "+" | ".join("" if v is None else str(v)[:46] for v in r))
    except Exception as e: print("  ERR",str(e)[:150])
show("STAT_PROCESS_STATUS row (the run result)",
    "SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, TO_CHAR(RUN_DAYTIME,'YYYY-MM-DD HH24:MI') run, ROWS_UPDATED FROM STAT_PROCESS_STATUS ORDER BY RUN_DAYTIME DESC")
# which day-status tables now have V rows on 2024-02-06 (the lift)?
for tbl in ["EQPM_DAY_STATUS","PWEL_DAY_STATUS","STRM_DAY_STREAM","PFLW_DAY_STATUS","PSEP_DAY_STATUS","IWEL_DAY_STATUS"]:
    try:
        cur.execute(f"SELECT '{tbl}' t, RECORD_STATUS, COUNT(*) n FROM {tbl} WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') GROUP BY RECORD_STATUS ORDER BY 2")
        rows=cur.fetchall()
        if rows: print(f"  {tbl} @2024-02-06:", [(r[1],r[2]) for r in rows])
    except Exception as e: print(f"  {tbl} ERR",str(e)[:50])
cur.close();c.close();print("\nDONE")
