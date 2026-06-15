"""READ-ONLY: lock the Water Injection (WI) scope on 2019-12-20 — flowlines + names + current
ON_STREAM_HRS/INJ_VOL (target-cell candidates) + OV_FLOWLINE name column. ASCII only. NO writes."""
import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),
 password=os.environ.get("EC_DB_PASS","energy"),
 dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='OV_FLOWLINE' ORDER BY column_id")
print("OV_FLOWLINE cols:", ", ".join(r[0] for r in cur.fetchall()))
print("\n=== WI flowlines on 2019-12-20 (name + current target cells) ===")
cur.execute("""SELECT s.OBJECT_ID, f.OBJECT_CODE, s.ON_STREAM_HRS, s.INJ_VOL, s.INJ_RATE
 FROM IFLW_DAY_STATUS s LEFT JOIN OV_FLOWLINE f ON f.OBJECT_ID=s.OBJECT_ID
 WHERE s.RECORD_STATUS='P' AND s.INJ_TYPE='WI' AND TRUNC(s.DAYTIME)=DATE '2019-12-20'
 ORDER BY f.OBJECT_CODE""")
for r in cur.fetchall(): print("  ", tuple(str(x)[:30] for x in r))
con.close();print("DONE")
