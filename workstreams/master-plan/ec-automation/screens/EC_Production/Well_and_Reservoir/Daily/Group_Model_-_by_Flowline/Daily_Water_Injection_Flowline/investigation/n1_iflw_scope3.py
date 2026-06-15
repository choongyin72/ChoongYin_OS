import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
print("=== WI flowlines on 2019-12-20 (CODE/NAME + current target cells) ===")
cur.execute("""SELECT s.OBJECT_ID, f.CODE, f.NAME, s.ON_STREAM_HRS, s.INJ_VOL, s.INJ_RATE,
  f.OP_PRODUCTIONUNIT_CODE, f.OP_AREA_CODE, f.OP_FCTY_1_CODE
 FROM IFLW_DAY_STATUS s LEFT JOIN OV_FLOWLINE f ON f.OBJECT_ID=s.OBJECT_ID
 WHERE s.RECORD_STATUS='P' AND s.INJ_TYPE='WI' AND TRUNC(s.DAYTIME)=DATE '2019-12-20'
 ORDER BY f.CODE""")
cols=[d[0] for d in cur.description]
for r in cur.fetchall():
    print("  "+" | ".join(f"{cols[i]}={'' if v is None else str(v)[:22]}" for i,v in enumerate(r)))
con.close();print("DONE")
