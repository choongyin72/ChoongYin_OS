"""N3 ground-truth: after the forward run went WAITING, did the DB actually change?
Check STAT_PROCESS_STATUS for a new row, RECORD_STATUS on day-status tables for 2003-01-01 (any V?),
and the P1_FwdUpd facility's data. Read-only."""
import os
import oracledb
conn = oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS","energy"), dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),
    tcp_connect_timeout=15)
cur=conn.cursor()
def run(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql); cols=[c[0] for c in cur.description]; print(" | ".join(cols))
        for r in cur.fetchall(): print("  "+" | ".join("" if v is None else str(v) for v in r))
    except Exception as e: print("  ERR:", str(e)[:200])

run("STAT_PROCESS_STATUS rows now (any run logged?)",
    "SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, "
    "TO_CHAR(RUN_DAYTIME,'YYYY-MM-DD HH24:MI') run_at, ROWS_UPDATED FROM STAT_PROCESS_STATUS "
    "ORDER BY RUN_DAYTIME DESC NULLS LAST FETCH FIRST 10 ROWS ONLY")

run("PWEL_DAY_STATUS RECORD_STATUS distribution NOW (was all P)",
    "SELECT RECORD_STATUS, COUNT(*) n FROM PWEL_DAY_STATUS GROUP BY RECORD_STATUS")

run("Any day-status-ish table with a V on 2003-01-01? (sample PWEL/STRM/IWEL)",
    "SELECT 'PWEL' t, RECORD_STATUS, COUNT(*) n FROM PWEL_DAY_STATUS "
    "WHERE TRUNC(DAYTIME)=TO_DATE('2003-01-01','YYYY-MM-DD') GROUP BY RECORD_STATUS")

# Quartz / job queue: is there a WAITING/queued job? (EC scheduler tables)
run("Candidate job-queue tables",
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND "
    "(table_name LIKE '%QRTZ%' OR table_name LIKE '%JOB_QUEUE%' OR table_name LIKE '%RUNNING%' "
    "OR table_name LIKE '%JOB_EXEC%' OR table_name LIKE 'BPM%') ORDER BY table_name FETCH FIRST 20 ROWS ONLY")

cur.close(); conn.close(); print("\nDONE")
