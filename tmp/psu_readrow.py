import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
cur.execute("""select code, name, to_char(object_start_date,'YYYY-MM-DD'), to_char(object_end_date,'YYYY-MM-DD'),
   record_status from OV_PROD_SUB_UNIT where code='AUTOTEST_PSU_001'""")
for r in cur.fetchall(): print("row:", r)
c.close()
