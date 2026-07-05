"""ECSR-35333 follow-up (read-only): compare uploaded RAU TARGET events across contracts - are they identical?"""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
print("=== RAU monthly contract-account events per contract, June 2026 (all account codes) ===")
cur.execute("""select OBJECT_CODE, ACCOUNT_CODE, round(QTY,6)
   from DV_SCTR_ACC_MTH_EVENT
   where DAYTIME = DATE '2026-06-01' and ACCOUNT_CODE like 'RAU_%'
     and OBJECT_CODE in ('C_PLU_LNG_1','C_PLU_LNG_2','C_PLU_COND','C_PLU_PG','C_PLU_PNI')
   order by ACCOUNT_CODE, OBJECT_CODE""")
rows=cur.fetchall()
from collections import defaultdict
by=defaultdict(dict)
for oc,ac,q in rows: by[ac][oc]=q
hdr=['C_PLU_LNG_1','C_PLU_LNG_2','C_PLU_COND','C_PLU_PG','C_PLU_PNI']
print(f"{'ACCOUNT_CODE':28} | " + " | ".join(f"{h:12}" for h in hdr))
for ac in sorted(by):
    print(f"{ac:28} | " + " | ".join(f"{str(by[ac].get(h,'-')):12}" for h in hdr))
print("\n=== count of TRGT events full-year 2026 per contract ===")
cur.execute("""select OBJECT_CODE, count(*) 
   from DV_SCTR_ACC_MTH_EVENT
   where DAYTIME >= DATE '2026-01-01' and DAYTIME < DATE '2027-01-01'
     and ACCOUNT_CODE like 'RAU%TRGT' and OBJECT_CODE in ('C_PLU_LNG_1','C_PLU_LNG_2','C_PLU_COND','C_PLU_PG','C_PLU_PNI')
   group by OBJECT_CODE order by OBJECT_CODE""")
for r in cur.fetchall(): print("  ", r)
c.close(); print("DONE")
