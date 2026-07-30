import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
cur.execute("""select column_name from all_tab_columns where owner='ECKERNEL_EC'
   and table_name='OV_PROD_SUB_UNIT' order by column_id""")
cols = [r[0] for r in cur.fetchall()]
print("cols:", cols)
codecol = "CODE" if "CODE" in cols else next((x for x in cols if x.endswith("CODE")), cols[0])
cur.execute("select %s from OV_PROD_SUB_UNIT" % codecol)
print("all", codecol, "vals:", [r[0] for r in cur.fetchall()])
c.close()
