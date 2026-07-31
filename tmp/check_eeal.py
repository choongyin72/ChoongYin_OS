import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select code, name, object_start_date from ov_production_unit where code = 'EEAL'")
print(a("PU with code EEAL: %s" % (cur.fetchall(),)))
cur.execute("select code, name from ov_production_unit where name = 'Production Unit'")
print(a("PU(s) named 'Production Unit': %s" % (cur.fetchall(),)))
cur.close(); con.close()
