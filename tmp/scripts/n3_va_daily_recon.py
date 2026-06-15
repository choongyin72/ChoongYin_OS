"""N3 V->A DAILY recon (read-only). The daily V->A processes on HA.0001 are the matched pairs:
Analysis Data Mgmt (P1_AnalysisDataManagement_Ver ->V / _App V->A) and Stream Item (VER_STIM_DAY ->V
/ APPRV_STIM_DAY ->A). Goal: (1) find how a status process maps to its TARGET data (which table/class
+ scope) — STATUS_PROCESS alone didn't show it, so scan for STATUS_PROCESS* / STAT_PROCESS* config
tables; (2) resolve the Analysis facility scope; (3) check STAT_PROCESS_STATUS history for prior runs
of these processes (what level/rows they lifted). Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, binds=None, n=30):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql, binds or {})
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:40] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


# (1) config tables that might link a status process to its target class/table
show("tables matching STATUS_PROCESS / STAT_PROCESS",
     "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' "
     "AND (table_name LIKE '%STATUS_PROCESS%' OR table_name LIKE '%STAT_PROCESS%') ORDER BY table_name")

# (2) ALL columns of STATUS_PROCESS (is there a CLASS_NAME / TABLE_ID / OBJECT_CLASS col I missed?)
show("STATUS_PROCESS columns",
     "SELECT column_name, data_type FROM all_tab_columns WHERE table_name='STATUS_PROCESS' ORDER BY column_id", n=60)

# (3) the daily V->A pair configs (full rows)
show("daily V->A pair configs",
     "SELECT PROCESS_ID, PROCESS_TEXT, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, PARENT_PROCESS_ID, PROD_FCTY_ID "
     "FROM STATUS_PROCESS WHERE PROCESS_ID IN "
     "('P1_AnalysisDataManagement_Ver','P1_AnalysisDataManagement_App','VER_STIM_DAY','APPRV_STIM_DAY')")

# (4) resolve the Analysis facility scope name
show("Analysis facility (PROD_FCTY_ID 96D7FD4EFDE60217E053020011AC1940)",
     "SELECT OBJECT_ID, NAME, CLASS_NAME FROM OBJECT_VERSION WHERE OBJECT_ID='96D7FD4EFDE60217E053020011AC1940' FETCH FIRST 3 ROWS ONLY")

# (5) STAT_PROCESS_STATUS history for these processes (what they lifted before, if ever)
show("STAT_PROCESS_STATUS history for the daily V->A processes",
     "SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, ROWS_UPDATED "
     "FROM STAT_PROCESS_STATUS WHERE PROCESS_ID IN "
     "('P1_AnalysisDataManagement_Ver','P1_AnalysisDataManagement_App','VER_STIM_DAY','APPRV_STIM_DAY') "
     "ORDER BY PROCESS_ID")

cur.close(); c.close(); print("\nDONE")
