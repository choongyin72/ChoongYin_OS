import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
cur.execute("select code, to_char(object_start_date,'YYYY-MM-DD'), to_char(object_end_date,'YYYY-MM-DD') from OV_CHEM_PRODUCT where code like 'AUTOTEST_CHP%'")
print("OV_CHEM_PRODUCT AUTOTEST rows (visible):", cur.fetchall())
# usage report conf child - any AUTOTEST-linked?
for t in ("CHEM_USAGE_REPORT_CONF",):
    try:
        cur.execute(f"select count(*) from {t} where created_date > sysdate-1")
        print(f"{t}: rows created in last 24h = {cur.fetchone()[0]}")
    except Exception as e: print(t,"ERR",str(e)[:60])
c.close()
