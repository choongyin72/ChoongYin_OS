import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
for pat in ("%BUSINESS%UNIT%", "%TRANSPORT%SYS%", "%SERVICE%TEMPLATE%", "%SERVICE%TEMPL%"):
    cur.execute("""select view_name from all_views where view_name like :p and view_name like 'OV%'
                   and view_name not like '%_JN' order by view_name""", p=pat)
    print(a("%-22s -> %s" % (pat, [r[0] for r in cur.fetchall()][:6])))
cur.close(); con.close()
