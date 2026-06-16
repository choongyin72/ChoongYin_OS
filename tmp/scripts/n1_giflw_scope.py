"""READ-ONLY: lock the Gas Injection (GI) flowline scope for the next screen — GI flowlines on a
data-bearing date with names + facility cascade + current ON_STREAM_HRS. Mirrors the IFLW recon."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
print("=== GI: top dates by distinct flowlines ===")
cur.execute("""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, COUNT(DISTINCT OBJECT_ID) fl, COUNT(*) rows_
 FROM IFLW_DAY_STATUS WHERE RECORD_STATUS='P' AND INJ_TYPE='GI'
 GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD') ORDER BY fl DESC, d DESC FETCH FIRST 6 ROWS ONLY""")
for r in cur.fetchall(): print("  ",r)
print("\n=== GI flowlines on 2019-12-20 (name + facility + current cells) ===")
cur.execute("""SELECT s.OBJECT_ID, f.CODE, f.NAME, f.OP_PRODUCTIONUNIT_CODE, f.OP_AREA_CODE, f.OP_FCTY_1_CODE, s.ON_STREAM_HRS
 FROM IFLW_DAY_STATUS s JOIN OV_FLOWLINE f ON f.OBJECT_ID=s.OBJECT_ID
 WHERE s.RECORD_STATUS='P' AND s.INJ_TYPE='GI' AND TRUNC(s.DAYTIME)=DATE '2019-12-20' ORDER BY f.CODE""")
cols=[d[0] for d in cur.description]
for r in cur.fetchall(): print("  "+" | ".join(f"{cols[i]}={'' if v is None else str(v)[:22]}" for i,v in enumerate(r)))
con.close();print("DONE")
