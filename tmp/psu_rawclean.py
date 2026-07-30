import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
# EC true-delete semantics: END_DATE = OBJECT_START_DATE via the OV view (fires the IUD_ trigger)
try:
    cur.execute("""update OV_PROD_SUB_UNIT set END_DATE = OBJECT_START_DATE
                   where CODE='AUTOTEST_PSU_001'""")
    print("rows updated:", cur.rowcount); c.commit()
except Exception as e:
    print("view update ERR:", str(e)[:160])
cur.execute("select code, to_char(end_date,'YYYY-MM-DD') from OV_PROD_SUB_UNIT where code='AUTOTEST_PSU_001'")
r = cur.fetchall()
print("still visible in OV view:", r)
c.close()
