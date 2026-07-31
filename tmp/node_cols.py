import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select column_name from all_tab_columns where table_name='OV_NODE'
               and (column_name like '%PROD%' or column_name like '%UNIT%' or column_name like '%OP_%')
               order by column_id""")
print(a("candidate parent columns: %s" % [r[0] for r in cur.fetchall()]))
cur.execute("select code, op_prod_unit_code from ov_node where rownum <= 4")
print(a("sample rows (code, op_prod_unit_code):"))
for r in cur.fetchall(): print(a("   %s" % (r,)))
cur.execute("select count(*) from ov_node where code like 'AUTOTEST%' and object_end_date is null")
print(a("open AUTOTEST rows in ov_node before run: %d" % cur.fetchone()[0]))
cur.close(); con.close()
