import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
# real error
try:
    cur.execute("select count(*) from OV_PROD_SUB_UNIT"); print("OV_PROD_SUB_UNIT:", cur.fetchone())
except Exception as e: print("OV_PROD_SUB_UNIT ERR:", str(e)[:80])
# candidate views
cur.execute("""select view_name from all_views where owner='ECKERNEL_EC'
   and (view_name like '%SUB_UNIT%' or view_name like '%PSU%' or view_name like 'OV_PROD%') order by view_name""")
print("candidates:", [r[0] for r in cur.fetchall()])
c.close()
