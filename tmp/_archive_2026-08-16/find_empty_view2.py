import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
cur.execute("select view_name from all_views where view_name like 'OV_%' and view_name not like '%_JN' order by dbms_random.value fetch first 40 rows only")
cands = [r[0] for r in cur.fetchall()]
for v in cands:
    try:
        cur.execute("select count(*) from %s" % v)
        n = cur.fetchone()[0]
        if n == 0:
            print(a("EMPTY: %s" % v)); break
    except Exception:
        pass
else:
    print(a("none of the %d sampled views were empty" % len(cands)))
cur.close(); con.close()
