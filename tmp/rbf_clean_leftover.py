import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
for v,code in [("OV_RESV_BLOCK","AUTOTEST_RFB_001"),("OV_RESV_FORMATION","AUTOTEST_RFF_001")]:
    try:
        cur.execute(f"update {v} set OBJECT_END_DATE = OBJECT_START_DATE where CODE='{code}' and OBJECT_END_DATE is null")
        print(f"{v} {code}: rows updated={cur.rowcount}")
    except Exception as e: print(v,"ERR",str(e)[:120])
c.commit()
# verify absent from views
for v,code in [("OV_RESV_BLOCK","AUTOTEST_RFB_001"),("OV_RESV_FORMATION","AUTOTEST_RFF_001")]:
    cur.execute(f"select count(*) from {v} where CODE='{code}'"); print(f"  {v} {code} still visible: {cur.fetchone()[0]}")
c.close()
