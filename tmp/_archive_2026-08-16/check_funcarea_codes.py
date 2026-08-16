import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select view_name from all_views where view_name like '%FUNCTIONAL_AREA%' order by 1")
views = [r[0] for r in cur.fetchall()]
print(a("views: %s" % views[:6]))
for v in views[:3]:
    try:
        cur.execute("select code, name from %s order by name" % v)
        rows = cur.fetchall()
        print(a("\n%s (%d rows):" % (v, len(rows))))
        for r in rows[:12]:
            print(a("   code=%-16s name=%s" % r))
    except Exception as e:
        print(a("%s ERR %s" % (v, repr(e)[:70])))
cur.close(); con.close()
