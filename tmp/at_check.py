import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
try:
  cur.execute("select count(*) from OV_CONTROL_POINT where code like 'AUTOTEST_AT%'");print("AUTOTEST_AT rows:",cur.fetchone()[0])
except Exception as e:print("ERR",str(e)[:100])
c.close()
