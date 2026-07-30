import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
for v in ("OV_FORECAST_GROUP","OV_FORECAST"):
    try:
        cur.execute(f"select code, to_char(object_start_date,'YYYY-MM-DD'), to_char(object_end_date,'YYYY-MM-DD') from {v} where code like 'AUTOTEST_FC%'")
        r=cur.fetchall(); print(f"{v}: {len(r)} AUTOTEST rows {r}")
    except Exception as e: print(v,"ERR",str(e)[:70])
c.close()
