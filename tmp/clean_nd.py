import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
cur.execute("update OV_NODE set OBJECT_END_DATE=OBJECT_START_DATE where CODE like 'AUTOTEST_ND%' and OBJECT_END_DATE is null")
print("cleaned rows:",cur.rowcount); c.commit()
cur.execute("select count(*) from OV_NODE where code like 'AUTOTEST_ND%'"); print("AUTOTEST_ND still visible:",cur.fetchone()[0])
c.close()
