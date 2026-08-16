import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select code, cp_productionunit_code, cp_area_code, cp_operator_route_code
               from ov_collection_point""")
for r in cur.fetchall(): print(a(str(r)))
cur.close(); con.close()
