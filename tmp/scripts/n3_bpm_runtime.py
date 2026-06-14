"""Find BPM/job runtime tables + inspect my WAITING status-process job's actual state. Read-only."""
import os
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy",
                     dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = c.cursor()

cur.execute(
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND ("
    "table_name LIKE 'ACT_RU%' OR table_name LIKE 'ACT_GE%' OR table_name LIKE '%JBPM%' "
    "OR table_name LIKE '%PROCESS_INST%' OR table_name LIKE '%RUNNING%' OR table_name LIKE '%JOB_EXEC%' "
    "OR table_name LIKE '%WORKFLOW%' OR table_name LIKE '%PROC_MONITOR%') ORDER BY table_name"
)
ts = [r[0] for r in cur.fetchall()]
print("candidate runtime tables (%d):" % len(ts))
for t in ts:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        print(f"  {t:40s} rows={cur.fetchone()[0]}")
    except Exception as e:
        print(f"  {t:40s} ERR {str(e)[:60]}")

# Flowable/Activiti runtime jobs (where async jobs live + exceptions)
for t in ["ACT_RU_JOB", "ACT_RU_TIMER_JOB", "ACT_RU_DEADLETTER_JOB", "ACT_RU_SUSPENDED_JOB",
          "ACT_RU_EXECUTION", "ACT_RU_TASK"]:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        n = cur.fetchone()[0]
        print(f"\n{t}: {n} rows")
        if n:
            cur.execute(f"SELECT * FROM {t} FETCH FIRST 3 ROWS ONLY")
            cols = [d[0] for d in cur.description]
            print("  cols:", ", ".join(cols[:14]))
    except Exception as e:
        print(f"\n{t}: ERR {str(e)[:70]}")

cur.close(); c.close()
print("\nDONE")
