import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
for v,code in [("OV_RESV_BLOCK","AUTOTEST_RFB%"),("OV_RESV_FORMATION","AUTOTEST_RFF%"),("OV_RESV_BLOCK_FORMATION","AUTOTEST_RFR%")]:
    try:
        cur.execute(f"select code from {v} where code like '{code}'")
        r=[x[0] for x in cur.fetchall()]; print(f"{v}: {len(r)} leftover {r}")
    except Exception as e: print(v,"ERR",str(e)[:80])
c.close()
