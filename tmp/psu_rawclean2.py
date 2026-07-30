import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
try:
    cur.execute("""update OV_PROD_SUB_UNIT set OBJECT_END_DATE = OBJECT_START_DATE
                   where CODE='AUTOTEST_PSU_001'""")
    print("rows updated:", cur.rowcount); c.commit()
except Exception as e:
    print("ERR:", str(e)[:200])
cur.execute("select code from OV_PROD_SUB_UNIT where code='AUTOTEST_PSU_001'")
print("still in OV view (should be empty):", cur.fetchall())
c.close()
