"""Patient ~3.5min poll: do the queued status-process jobs execute now (jBPM warming up)?
Watch STAT_PROCESS_STATUS (a row = a run completed), JBPM_PROCESSINSTANCEINFO / JBPM_REQUESTINFO
(jBPM picked it up), and PWEL V count. Read-only."""
import os, time
import oracledb
def snap(cur):
    out = {}
    for label, sql in [
        ("STAT_PROC", "SELECT COUNT(*) FROM STAT_PROCESS_STATUS"),
        ("STAT_PROC_run", "SELECT COUNT(*) FROM STAT_PROCESS_STATUS WHERE RUN_DAYTIME IS NOT NULL"),
        ("jbpm_procinst", "SELECT COUNT(*) FROM JBPM_PROCESSINSTANCEINFO"),
        ("jbpm_request", "SELECT COUNT(*) FROM JBPM_REQUESTINFO"),
        ("pwel_V", "SELECT COUNT(*) FROM PWEL_DAY_STATUS WHERE RECORD_STATUS='V'"),
    ]:
        cur.execute(sql); out[label] = cur.fetchone()[0]
    return out

c = oracledb.connect(user="ECKERNEL_EC", password="energy",
                     dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = c.cursor()
for i in range(15):
    s = snap(cur)
    print(f"t+{i*15:>3}s  STAT_PROCESS_STATUS={s['STAT_PROC']}(run={s['STAT_PROC_run']})  "
          f"jbpm_procinst={s['jbpm_procinst']}  jbpm_request={s['jbpm_request']}  PWEL_V={s['pwel_V']}")
    if s["STAT_PROC_run"] or s["jbpm_procinst"] or s["pwel_V"]:
        print(">>> EXECUTION DETECTED"); break
    time.sleep(15)
cur.close(); c.close()
print("DONE")
