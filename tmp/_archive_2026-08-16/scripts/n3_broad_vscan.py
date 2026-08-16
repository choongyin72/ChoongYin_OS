"""Cleanliness check: scan ALL tables that have BOTH RECORD_STATUS and DAYTIME columns for V rows on
2024-02-06 (to find any residue from my P1_FwdUpd test lift). 2024-02-06 was all-P before my run, so
any V there = my lift. Report only; restore in a second pass after I see what's there."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
# tables having both RECORD_STATUS and a DAYTIME column
cur.execute("""SELECT t.table_name FROM all_tab_columns t
  WHERE t.owner='ECKERNEL_EC' AND t.column_name='RECORD_STATUS'
  AND EXISTS (SELECT 1 FROM all_tab_columns d WHERE d.owner='ECKERNEL_EC' AND d.table_name=t.table_name AND d.column_name='DAYTIME')
  AND t.table_name NOT LIKE '%JN' ORDER BY t.table_name""")
tables=[r[0] for r in cur.fetchall()]
print(f"scanning {len(tables)} tables with RECORD_STATUS+DAYTIME for V on 2024-02-06...")
hits=[]
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t} WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND RECORD_STATUS='V'")
        n=cur.fetchone()[0]
        if n: hits.append((t,n)); print(f"  V FOUND: {t} = {n}")
    except Exception:
        pass
print("tables with V on 2024-02-06:", len(hits), "| total V rows:", sum(n for _,n in hits))
cur.close(); c.close(); print("DONE")
