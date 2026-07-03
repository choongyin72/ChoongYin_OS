import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
cur.execute("""select min(line) from all_source where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
               and lower(text) like '%function getgroupforecastid%'""")
st=cur.fetchone()[0]
print("=== getGroupForecastId body (from line", st, ") ===")
if st:
    cur.execute("""select line,text from all_source where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
                   and line between :a and :b order by line""",[st, st+55])
    for ln,tx in cur.fetchall(): print("%4d| %s"%(ln,(tx or '').rstrip()))
c.close()
