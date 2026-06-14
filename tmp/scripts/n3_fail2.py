import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:6]: print("  "+" | ".join("" if v is None else str(v)[:600] for v in r))
    except Exception as e: print("  ERR",str(e)[:150])
show("recent ACTION_INSTANCE_HISTORY (FAIL message)",
    "SELECT ACTION_INSTANCE_NO, TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI') dt, RUN_STATUS, RUN_ID, DBMS_LOB.SUBSTR(MESSAGE_DETAIL,500,1) msg "
    "FROM ACTION_INSTANCE_HISTORY ORDER BY DAYTIME DESC FETCH FIRST 4 ROWS ONLY")
show("recent SCHEDULE_HISTORY (DETAILED_LOG)",
    "SELECT SCHEDULE_NO, TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI') d, RUN_STATUS, DBMS_LOB.SUBSTR(DETAILED_LOG,1200,1) lg "
    "FROM SCHEDULE_HISTORY ORDER BY DAYTIME DESC FETCH FIRST 2 ROWS ONLY")
cur.close();c.close();print("\nDONE")
