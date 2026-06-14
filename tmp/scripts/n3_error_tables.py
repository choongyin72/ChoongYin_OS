import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; print(" | ".join(cols))
        rows=cur.fetchall()
        if not rows: print("  (no rows)")
        for r in rows[:8]: print("  "+" | ".join("" if v is None else str(v)[:70] for v in r))
    except Exception as e: print("  ERR", str(e)[:140])

# jBPM async executor requests carry error message/retries if a job was created+failed
show("JBPM_REQUESTINFO (async job errors)",
    "SELECT ID, STATUS, RETRIES, TO_CHAR(TIME,'YYYY-MM-DD HH24:MI') t, MESSAGE FROM JBPM_REQUESTINFO ORDER BY ID DESC FETCH FIRST 8 ROWS ONLY")
show("JBPM_EXECERRORINFO (executor error info, if present)",
    "SELECT ID, TYPE, TO_CHAR(ERROR_DATE,'YYYY-MM-DD HH24:MI') d, DBMS_LOB.SUBSTR(ERROR_INFO,200,1) info FROM JBPM_EXECERRORINFO ORDER BY ERROR_DATE DESC FETCH FIRST 5 ROWS ONLY")
show("BPM_EC_EVENT_HANDLE_LOG (event handling)",
    "SELECT * FROM BPM_EC_EVENT_HANDLE_LOG ORDER BY 1 DESC FETCH FIRST 5 ROWS ONLY")
show("BPM_PROC_MONITOR (process monitor)",
    "SELECT * FROM BPM_PROC_MONITOR FETCH FIRST 5 ROWS ONLY")
# EC scheduler job log table?
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND (table_name LIKE '%SCHEDUL%LOG%' OR table_name LIKE '%JOB%LOG%' OR table_name LIKE '%RUNNING_JOB%' OR table_name LIKE '%SCHEDULED_JOB%') ORDER BY 1")
print("\n=== candidate scheduler/job-log tables ===")
for r in cur.fetchall(): print("  ",r[0])
cur.close(); c.close()
