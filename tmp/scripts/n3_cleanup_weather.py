"""Restore the 13 OBJECT_DAY_WEATHER rows my P1_FwdUpd test lifted to V on 2024-02-06 back to P.
(DV_WEATHER/RV_WEATHER are views over OBJECT_DAY_WEATHER.) Then confirm total residual V = 0."""
import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
cur.execute("SELECT RECORD_STATUS, COUNT(*) FROM OBJECT_DAY_WEATHER WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') GROUP BY RECORD_STATUS ORDER BY 1")
print("OBJECT_DAY_WEATHER @2024-02-06 before:", cur.fetchall())
cur.execute("UPDATE OBJECT_DAY_WEATHER SET RECORD_STATUS='P' WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') AND RECORD_STATUS='V'")
print("restored:", cur.rowcount)
c.commit()
cur.execute("SELECT RECORD_STATUS, COUNT(*) FROM OBJECT_DAY_WEATHER WHERE TRUNC(DAYTIME)=TO_DATE('2024-02-06','YYYY-MM-DD') GROUP BY RECORD_STATUS ORDER BY 1")
print("OBJECT_DAY_WEATHER @2024-02-06 after:", cur.fetchall())
cur.close(); c.close(); print("DONE")
