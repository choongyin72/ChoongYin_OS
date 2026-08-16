"""The worker now executes DailyDataStatusProcess but it FAILS (code 2). Read the failure detail from
the DB (where the log was re-routed): recent SCHEDULE_HISTORY + ACTION_INSTANCE_HISTORY messages, and
STAT_PROCESS_STATUS. Also check if any RECORD_STATUS actually changed. Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15);cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description];print(" | ".join(cols))
        for r in cur.fetchall()[:12]: print("  "+" | ".join("" if v is None else str(v)[:90] for v in r))
    except Exception as e: print("  ERR",str(e)[:150])
# columns of the history tables
show("SCHEDULE_HISTORY columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='SCHEDULE_HISTORY' ORDER BY column_id")
show("ACTION_INSTANCE_HISTORY columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='ACTION_INSTANCE_HISTORY' ORDER BY column_id")
# recent action-instance-history (status + message) - the FAIL reason
show("recent ACTION_INSTANCE_HISTORY (status + message)",
    "SELECT ACTION_INSTANCE_NO, TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI') dt, STATUS, DBMS_LOB.SUBSTR(MESSAGE,300,1) msg "
    "FROM ACTION_INSTANCE_HISTORY ORDER BY DAYTIME DESC FETCH FIRST 5 ROWS ONLY")
# recent schedule_history with the rerouted log
show("recent SCHEDULE_HISTORY (log)",
    "SELECT SCHEDULE_NO, TO_CHAR(SCHED_DATE,'YYYY-MM-DD HH24:MI') d, STATUS, DBMS_LOB.SUBSTR(LOG,600,1) lg "
    "FROM SCHEDULE_HISTORY ORDER BY SCHED_DATE DESC FETCH FIRST 3 ROWS ONLY")
show("STAT_PROCESS_STATUS now",
    "SELECT COUNT(*) FROM STAT_PROCESS_STATUS")
show("PWEL_DAY_STATUS V count (did anything lift?)",
    "SELECT RECORD_STATUS, COUNT(*) FROM PWEL_DAY_STATUS GROUP BY RECORD_STATUS")
cur.close();c.close();print("\nDONE")
