import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select table_name from all_tab_columns where column_name in ('CODE','NAME')
               and table_name like 'OV_%LOCATION%' group by table_name having count(distinct column_name)=2
               order by table_name""")
print(a([r[0] for r in cur.fetchall()]))
cur.close(); con.close()
