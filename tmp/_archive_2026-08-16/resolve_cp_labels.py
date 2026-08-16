import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
def q(label, sql, **kw):
    try:
        cur.execute(sql, kw); print(a("%-30s %s" % (label, cur.fetchall())))
    except Exception as e:
        print(a("%-30s ERR %s" % (label, repr(e)[:80])))
q("PU P3_PU ->", "select code, name from ov_productionunit where code='P3_PU'")
q("Area P3_AREA ->", "select code, name from ov_area where code='P3_AREA'")
q("Route P3_ROUTE_1 ->", "select code, name from ov_operator_route where code='P3_ROUTE_1'")
cur.close(); con.close()
