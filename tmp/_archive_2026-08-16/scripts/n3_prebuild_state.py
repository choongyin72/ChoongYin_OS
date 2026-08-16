"""Pre-build state check for the N3 suite build (2026-06-14).
Confirms: (1) DB reachable; (2) STATUS_PROCESS config row for P1 Forward Status Update;
(3) data on 2024-02-06 is clean baseline (all target rows P, ZERO residual V);
(4) which day-status tables hold P rows on 2024-02-06 (the run's target set);
(5) any existing STAT_PROCESS_STATUS log rows for P1_FwdUpd/2024-02-06 (append-only)."""
import os, oracledb
DATE = "2024-02-06"
c = oracledb.connect(user='ECKERNEL_EC', password='energy',
                     dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'),
                     tcp_connect_timeout=15)
cur = c.cursor()

print("=== (2) STATUS_PROCESS config: P1 Forward Status Update ===")
cur.execute("SELECT PROCESS_ID, PROCESS_TEXT, FROM_RS_LEVEL, TO_RS_LEVEL, PROCESS_INTERVAL, "
            "REVERSE_FLAG FROM STATUS_PROCESS WHERE UPPER(PROCESS_TEXT) LIKE '%FORWARD STATUS%' "
            "OR PROCESS_ID='P1_FwdUpd'")
for r in cur.fetchall():
    print("  ", r)

print("\n=== (3)/(4) RECORD_STATUS breakdown on", DATE, "across day-status tables ===")
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' "
            "AND (table_name LIKE '%DAY_STATUS' OR table_name='STRM_DAY_STREAM' "
            "OR table_name='OBJECT_DAY_WEATHER') AND table_name NOT LIKE '%JN' ORDER BY table_name")
tables = [r[0] for r in cur.fetchall()]
target_tables = []
residual_v = 0
for t in tables:
    try:
        cur.execute(f"SELECT RECORD_STATUS, COUNT(*) FROM {t} "
                    f"WHERE TRUNC(DAYTIME)=TO_DATE('{DATE}','YYYY-MM-DD') GROUP BY RECORD_STATUS ORDER BY 1")
        rows = cur.fetchall()
        if rows:
            d = {rs: n for rs, n in rows}
            print(f"  {t}: {d}")
            if d.get('P'):
                target_tables.append(t)
            residual_v += d.get('V', 0)
    except Exception as e:
        pass
print("\n  TARGET TABLES (have P rows on", DATE, "):", target_tables)
print("  RESIDUAL V on", DATE, "(should be 0 for clean baseline):", residual_v)

print("\n=== (5) existing STAT_PROCESS_STATUS log rows for P1_FwdUpd /", DATE, "===")
cur.execute("SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, "
            "TO_CHAR(RUN_DAYTIME,'YYYY-MM-DD HH24:MI:SS') run, ROWS_UPDATED "
            "FROM STAT_PROCESS_STATUS WHERE PROCESS_ID='P1_FwdUpd' "
            "AND TRUNC(DAYTIME)=TO_DATE('"+DATE+"','YYYY-MM-DD') ORDER BY RUN_DAYTIME DESC")
spc = cur.fetchall()
for r in spc:
    print("  ", r)
print("  (count =", len(spc), "— append-only log; suite uses a delta, not absence)")

cur.close(); c.close(); print("\nDONE")
