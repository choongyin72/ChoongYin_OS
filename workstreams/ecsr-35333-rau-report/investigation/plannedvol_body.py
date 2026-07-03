import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
cur.execute("""select line,text from all_source where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
               and line between 201 and 280 order by line""")
for ln,tx in cur.fetchall(): print("%4d| %s"%(ln,(tx or '').rstrip()))
c.close()
