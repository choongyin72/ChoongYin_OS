import os, oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'),tcp_connect_timeout=15)
cur=c.cursor()
cur.execute("SELECT COUNT(*) FROM STAT_PROCESS_STATUS"); print('STAT_PROCESS_STATUS rows =', cur.fetchone()[0])
cur.execute("SELECT RECORD_STATUS,COUNT(*) FROM PWEL_DAY_STATUS GROUP BY RECORD_STATUS ORDER BY 1"); print('PWEL_DAY_STATUS by status =', cur.fetchall())
cur.execute("SELECT RECORD_STATUS,COUNT(*) FROM STRM_DAY_STREAM GROUP BY RECORD_STATUS ORDER BY 1"); print('STRM_DAY_STREAM by status =', cur.fetchall())
cur.close(); c.close()
