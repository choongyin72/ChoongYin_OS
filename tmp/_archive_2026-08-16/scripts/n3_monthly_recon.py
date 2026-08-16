"""READ-ONLY: decide build-vs-park for the N3 Monthly approve suite. Check (1) ec-worker scheduler node
state (async dependency), (2) the monthly approve process P1_FwdUpdPar1 + its target scope, (3) current
status-process log. NO writes."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql);cols=[d[0] for d in cur.description]
        print(" | ".join(cols))
        for r in cur.fetchall()[:25]: print(" | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e: print("ERR:",str(e)[:160])
# 1) scheduler/worker node state
show("scheduler nodes (look for RUNNING worker)", """
 SELECT NODE_NAME, SERVER_STATE, LAST_ACTIVE_TIME FROM SCHEDULER_NODE_STATE
 ORDER BY LAST_ACTIVE_TIME DESC""")
# fallback table name guesses if above errs
show("SERVER state-ish tables", """
 SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
  AND (table_name LIKE '%SCHEDULER%NODE%' OR table_name LIKE '%SERVER_STATE%' OR table_name LIKE '%NODE_STATE%')""")
# 2) the monthly approve process + scope
show("P1_FwdUpdPar1 + related approve processes in STATUS_PROCESS", """
 SELECT PROCESS_ID, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, REVERSE_FLAG
 FROM STATUS_PROCESS WHERE PROCESS_ID LIKE 'P1_FwdUpd%' OR PROCESS_ID LIKE '%MTH%' OR PROCESS_ID LIKE '%APPR%'""")
show("STAT_PROCESS_TASK target for P1_FwdUpd / P1_FwdUpdPar1", """
 SELECT PROCESS_ID, TABLE_ID, WHERE_FORMULA FROM STAT_PROCESS_TASK
 WHERE PROCESS_ID LIKE 'P1_FwdUpd%'""")
# 3) current status-process log (recent)
show("recent STAT_PROCESS_STATUS", """
 SELECT PROCESS_ID, RECORD_STATUS_LEVEL, DAYTIME, ROWS_UPDATED
 FROM (SELECT s.*, ROW_NUMBER() OVER (ORDER BY DAYTIME DESC) rn FROM STAT_PROCESS_STATUS s) WHERE rn<=10""")
con.close();print("\nDONE")
