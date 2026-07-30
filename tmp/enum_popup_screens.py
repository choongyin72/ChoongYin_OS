import oracledb
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL");cur=c.cursor()
cur.execute("""select table_name, listagg(column_name, ', ') within group (order by column_name) pops
   from all_tab_columns where owner='ECKERNEL_EC'
     and table_name like 'OV\_%' escape '~' and table_name not like '%\_JN' escape '~'
     and column_name like '%POPUP'
   group by table_name order by table_name""".replace("~","\\"))
rows=cur.fetchall()
print("OV views with popup-picker field(s): %d" % len(rows))
for t,p in rows: print("  %-36s %s" % (t, p))
c.close()
