import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
for v in ("OV_CALC_PROCESS_DETAIL_LOG", "OV_ALLOC_JOB_LOG", "CALC_BATCH_LOG", "CALC_PROCESS_LOG"):
    cur.execute("select count(*) from all_views where view_name=:v", v=v)
    if cur.fetchone()[0] == 0:
        print(a("%s: not a view" % v)); continue
    cur.execute("select count(*) from %s" % v)
    print(a("%s: %d rows" % (v, cur.fetchone()[0])))
cur.close(); con.close()
