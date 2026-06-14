"""Crack the daily-process TARGET mapping. Check: (1) full STATUS_PROCESS*/STAT_PROCESS* table list;
(2) STAT_PROCESS_TASK (cols + rows for the daily V->A pairs — likely the process->object-class config);
(3) the Analysis/Stream-Item processes' TEXT_1..10 + REF_OBJECT_ID_1..5 (may name the target class);
(4) resolve facility 96D7FD4E... by scanning likely facility views. Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def show(t, sql, binds=None, n=40):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql, binds or {})
        cols = [d[0] for d in cur.description]
        print("  " + " | ".join(cols))
        for r in cur.fetchall()[:n]:
            print("  " + " | ".join("" if v is None else str(v)[:42] for v in r))
    except Exception as e:
        print("  ERR", str(e)[:160])


show("(1) all STATUS_PROCESS*/STAT_PROCESS* tables",
     "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND (table_name LIKE 'STATUS_PROCESS%' "
     "OR table_name LIKE 'STAT_PROCESS%') AND table_name NOT LIKE '%JN' ORDER BY table_name")

show("(2a) STAT_PROCESS_TASK columns",
     "SELECT column_name, data_type FROM all_tab_columns WHERE table_name='STAT_PROCESS_TASK' ORDER BY column_id", n=40)
show("(2b) STAT_PROCESS_TASK rows for the daily V->A pairs",
     "SELECT * FROM STAT_PROCESS_TASK WHERE PROCESS_ID IN "
     "('P1_AnalysisDataManagement_Ver','P1_AnalysisDataManagement_App','VER_STIM_DAY','APPRV_STIM_DAY') FETCH FIRST 20 ROWS ONLY")

show("(3) Analysis/Stream-Item TEXT + REF_OBJECT_ID slots (target class encoded?)",
     "SELECT PROCESS_ID, TEXT_1, TEXT_2, TEXT_3, REF_OBJECT_ID_1, REF_OBJECT_ID_2, REF_OBJECT_ID_3 "
     "FROM STATUS_PROCESS WHERE PROCESS_ID IN "
     "('P1_AnalysisDataManagement_Ver','P1_AnalysisDataManagement_App','VER_STIM_DAY','APPRV_STIM_DAY')")

# (4) find which table/view holds OBJECT_ID 96D7FD4E... (the Analysis facility) — try common facility views
for v in ("OV_FACILITY_CLASS_1", "OV_FACILITY_CLASS_2", "OV_PRODUCTIONUNIT", "OV_PROD_FCTY", "OV_FACILITY"):
    try:
        cur.execute(f"SELECT NAME FROM {v} WHERE OBJECT_ID='96D7FD4EFDE60217E053020011AC1940' FETCH FIRST 1 ROWS ONLY")
        r = cur.fetchone()
        if r:
            print(f"\n  facility 96D7FD4E... = '{r[0]}' (in {v})")
    except Exception:
        pass

cur.close(); c.close(); print("\nDONE")
