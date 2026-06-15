import os, oracledb
con=oracledb.connect(user=os.environ.get("EC_DB_USER","ECKERNEL_EC"),password=os.environ.get("EC_DB_PASS","energy"),dsn=os.environ.get("EC_DB_DSN","localhost:1521/ORCL"),tcp_connect_timeout=15)
cur=con.cursor()
cur.execute("""SELECT OBJECT_ID, CODE, NAME FROM OV_FLOWLINE WHERE UPPER(NAME) LIKE '%0600 F003%' OR UPPER(CODE) LIKE '%0600%F003%' OR UPPER(NAME) LIKE '%F003 WI%'""")
print("OV_FLOWLINE matches:", cur.fetchall())
cur.execute("""SELECT s.OBJECT_ID, f.CODE, f.NAME, s.ON_STREAM_HRS, s.RECORD_STATUS
 FROM IFLW_DAY_STATUS s JOIN OV_FLOWLINE f ON f.OBJECT_ID=s.OBJECT_ID
 WHERE TRUNC(s.DAYTIME)=DATE '2019-12-20' AND (UPPER(f.NAME) LIKE '%F003%' OR UPPER(f.CODE) LIKE '%F003%')""")
print("IFLW row for F003 on 2019-12-20:", cur.fetchall())
con.close()
