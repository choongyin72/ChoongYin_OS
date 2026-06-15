"""READ-ONLY: lock the IFLW (injection flowline) N1 scope — a data-bearing flowline×date in
IFLW_DAY_STATUS, its OV_FLOWLINE name + cascade (facility/area/PU), and the non-null target columns
(persisting cell candidates). Mirrors the PFLW build. NO writes."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
# columns of IFLW_DAY_STATUS (measured value columns = target candidates)
cur.execute("SELECT column_name,data_type FROM all_tab_columns WHERE table_name='IFLW_DAY_STATUS' ORDER BY column_id")
cols=cur.fetchall()
print("IFLW_DAY_STATUS cols:", ", ".join(f"{c}" for c,_ in cols))
# a date with the most flowlines having rows (good scope day)
print("\n=== top dates by distinct flowlines (P rows) ===")
cur.execute("""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, COUNT(DISTINCT OBJECT_ID) flowlines, COUNT(*) rows_
  FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P'
  GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD') ORDER BY flowlines DESC, d DESC FETCH FIRST 8 ROWS ONLY""")
for r in cur.fetchall(): print("  ", r)
# pick one flowline+date and show its row's non-null measured columns
print("\n=== sample IFLW row (non-null measured cols = persisting target candidates) ===")
cur.execute("""SELECT * FROM (SELECT * FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P' ORDER BY DAYTIME DESC) WHERE ROWNUM=1""")
crow=[d[0] for d in cur.description]; row=cur.fetchone()
samp={crow[i]:row[i] for i in range(len(crow))}
oid=samp.get('OBJECT_ID'); dt=samp.get('DAYTIME')
nonnull=[(k,v) for k,v in samp.items() if v is not None and k not in ('OBJECT_ID','DAYTIME','REC_ID','RECORD_STATUS','CREATED_BY','CREATED_DATE','REV_NO','APPROVAL_STATE')]
print("  OBJECT_ID:",oid," DAYTIME:",dt)
print("  non-null measured:", [(k,str(v)[:14]) for k,v in nonnull][:18])
# resolve flowline name + its facility/area/PU via OV_FLOWLINE version
print("\n=== flowline name ===")
try:
    cur.execute("SELECT OBJECT_CODE FROM OV_FLOWLINE WHERE OBJECT_ID=:i",{"i":oid}); print("  OV_FLOWLINE:",cur.fetchone())
except Exception as e: print("  ERR:",str(e)[:80])
con.close();print("DONE")
