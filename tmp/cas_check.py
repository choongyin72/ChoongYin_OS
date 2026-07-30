import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur=c.cursor()
try:
    cur.execute("select count(*) from OV_CONTRACT_AREA_SETUP where code like 'AUTOTEST_CAS%'")
    print("AUTOTEST_CAS rows:", cur.fetchone()[0])
except Exception as e: print("ERR", str(e)[:100])
c.close()
