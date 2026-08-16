"""Discover the nav scope for an injection-well daily-status row (IWEL_DAY_STATUS) so the UI recon
lands on data. Find a day + well + its facility hierarchy (PU/Area/FacilityClass1/WellHookup).
Read-only."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
def show(t,sql):
    print(f"\n=== {t} ===")
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; print(" | ".join(cols))
        for r in cur.fetchall()[:15]: print("  "+" | ".join("" if v is None else str(v)[:38] for v in r))
    except Exception as e: print("  ERR",str(e)[:140])

# Which wells have IWEL data on the top day, + their names
show("IWEL_DAY_STATUS wells on 2026-02-13 (name)",
    "SELECT a.OBJECT_ID, w.NAME FROM IWEL_DAY_STATUS a LEFT JOIN WELL_VERSION w "
    "ON w.OBJECT_ID=a.OBJECT_ID AND TRUNC(a.DAYTIME) BETWEEN TRUNC(w.DAYTIME) AND NVL(w.END_DATE,DATE'9999-01-01') "
    "WHERE TRUNC(a.DAYTIME)=TO_DATE('2026-02-13','YYYY-MM-DD') ORDER BY w.NAME FETCH FIRST 12 ROWS ONLY")

# numeric measured columns on IWEL_DAY_STATUS (candidate editable cells)
show("IWEL_DAY_STATUS numeric columns (candidate measured cells)",
    "SELECT column_name FROM all_tab_columns WHERE table_name='IWEL_DAY_STATUS' AND data_type='NUMBER' "
    "AND column_name NOT IN ('OBJECT_ID') ORDER BY column_id FETCH FIRST 25 ROWS ONLY")

# a sample row's key measured values (to know what's populated/editable)
show("Sample IWEL_DAY_STATUS row values on 2026-02-13",
    "SELECT OBJECT_ID, RECORD_STATUS, ON_STREAM_HRS, AVG_WH_PRESS, AVG_WH_TEMP "
    "FROM IWEL_DAY_STATUS WHERE TRUNC(DAYTIME)=TO_DATE('2026-02-13','YYYY-MM-DD') FETCH FIRST 5 ROWS ONLY")
cur.close(); c.close(); print("\nDONE")
