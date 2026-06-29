import os, oracledb
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
say("=== calc-config tables (CALC_CONTEXT / OBJECT_TYPE / VARIABLE / GLOBAL) ===")
cur.execute("""select table_name from all_tables where owner='ECKERNEL_EC'
   and (table_name like 'CALC_CONTEXT%' or table_name like 'CALC_OBJECT%' or table_name like '%OBJECT_TYPE%'
        or table_name like 'CALC_VARIABLE%' or table_name like 'CALC_GLOBAL%' or table_name like 'CALC_ATTR%')
   order by table_name""")
for (t,) in cur.fetchall(): say("   "+t)
say("\n=== CALC_CONTEXT columns ===")
cur.execute("select column_name from all_tab_columns where owner='ECKERNEL_EC' and table_name='CALC_CONTEXT' order by column_id")
say("   "+", ".join(x[0] for x in cur.fetchall()))
say("\n=== CALC_CONTEXT rows (code + desc) ===")
try:
    cur.execute("select object_code, description from calc_context order by object_code")
    for r in cur.fetchall(): say("   %-14s %s" % (r[0], rd(r[1])))
except Exception as e: say("   (need different cols: "+str(e)[:60]+")")
c.close()
