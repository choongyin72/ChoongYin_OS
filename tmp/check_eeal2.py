import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("""select view_name from all_views where view_name like 'OV_PROD%'
               or view_name like '%PRODUCTION_UNIT%' order by view_name""")
print(a("candidate views: %s" % [r[0] for r in cur.fetchall()][:10]))
for v in ("OV_PROD_UNIT", "OV_PRODUCTIONUNIT"):
    try:
        cur.execute("select code, name from %s where code = 'EEAL' or name = 'Production Unit'" % v)
        print(a("%s -> %s" % (v, cur.fetchall())))
    except Exception as e:
        print(a("%s ERR %s" % (v, repr(e)[:60])))
cur.close(); con.close()
