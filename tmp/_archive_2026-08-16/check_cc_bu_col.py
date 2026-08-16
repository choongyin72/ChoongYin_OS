import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select column_name from all_tab_columns where table_name='OV_CONTRACT_CAPACITY' order by column_id")
print(a([r[0] for r in cur.fetchall()]))
cur.close(); con.close()
