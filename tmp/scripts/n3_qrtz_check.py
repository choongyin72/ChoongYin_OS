import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
cur.execute("SELECT TO_CHAR(SYSDATE,'HH24:MI:SS') FROM dual"); print('DB SYSDATE(UTC?) =', cur.fetchone()[0])
cur.execute("""SELECT INSTANCE_NAME,
 TO_CHAR(TO_DATE('19700101','YYYYMMDD')+LAST_CHECKIN_TIME/86400000,'HH24:MI:SS') checkin,
 ROUND((CAST(SYS_EXTRACT_UTC(SYSTIMESTAMP) AS DATE)-(TO_DATE('19700101','YYYYMMDD')+LAST_CHECKIN_TIME/86400000))*86400) secs_ago
 FROM QRTZ_SCHEDULER_STATE ORDER BY INSTANCE_NAME""")
print('QRTZ scheduler instances:')
for r in cur.fetchall(): print('  ', r[0], '| checkin', r[1], '| secs_ago', r[2])
cur.execute("SELECT TRIGGER_NAME,TRIGGER_STATE FROM QRTZ_TRIGGERS ORDER BY 1")
print('QRTZ triggers:', cur.fetchall())
cur.execute("SELECT COUNT(*) FROM QRTZ_FIRED_TRIGGERS"); print('QRTZ fired now =', cur.fetchone()[0])
cur.close(); c.close()
