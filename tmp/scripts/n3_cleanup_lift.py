"""Cleanup: restore V rows on 2024-02-06 (from my P1_FwdUpd test lift) back to P across day-status
tables. Before my run everything was P, so all V@2024-02-06 = my lift. Show -> restore -> verify."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' "
            "AND (table_name LIKE '%DAY_STATUS' OR table_name='STRM_DAY_STREAM') "
            "AND table_name NOT LIKE '%JN' ORDER BY table_name")
tables=[r[0] for r in cur.fetchall()]
affected=[]; total=0
print("=== V rows on 2024-02-06 BEFORE cleanup ===")
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t} WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND RECORD_STATUS='V'")
        n=cur.fetchone()[0]
        if n: print(f"  {t}: {n} V"); total+=n; affected.append(t)
    except Exception:
        pass
print("total V to restore:", total)
for t in affected:
    cur.execute(f"UPDATE {t} SET RECORD_STATUS='P' WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND RECORD_STATUS='V'")
    print(f"  restored {t}: {cur.rowcount}")
c.commit()
print("=== AFTER cleanup (V should be 0) ===")
chk=0
for t in affected:
    cur.execute(f"SELECT COUNT(*) FROM {t} WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND RECORD_STATUS='V'")
    v=cur.fetchone()[0]; chk+=v; print(f"  {t} V now: {v}")
print("residual V:", chk)
cur.close(); c.close(); print("DONE")
