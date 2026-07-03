import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
def run(t, sql, args=None):
    print("\n=== "+t+" ===")
    try:
        cur.execute(sql, args or {}); print(" | ".join(d[0] for d in cur.description))
        n=0
        for r in cur.fetchall(): print(" | ".join('' if v is None else str(v) for v in r)); n+=1
        if n==0: print("(none)")
    except Exception as e: print("ERR:", str(e)[:180])

run("Package object status / last DDL (deployed on ECAASDEV)",
  """select object_name, object_type, status, to_char(last_ddl_time,'YYYY-MM-DD HH24:MI') last_ddl, to_char(created,'YYYY-MM-DD') created
     from all_objects where object_name='ZWP_P_DEF_RAU_CALC' order by object_type""")

run("Package header revision/mod comments (deployed source, first 25 lines of body)",
  """select line, text from all_source
     where name='ZWP_P_DEF_RAU_CALC' and type='PACKAGE BODY' and line <= 24 order by line""")

# Confirm the negative-deferment handling: is it only a warning, and does the defer SUM include negatives?
run("Deployed source around NEGATIVE auto-def handling (lines 146-162)",
  """select line, text from all_source
     where name='ZWP_P_DEF_RAU_CALC' and type='PACKAGE BODY' and line between 146 and 162 order by line""")

run("Deployed source: total-deferment SUM + Utilisation actual formula (lines 241-248, 485-487)",
  """select line, text from all_source
     where name='ZWP_P_DEF_RAU_CALC' and type='PACKAGE BODY'
       and (line between 241 and 248 or line between 485 and 487) order by line""")
c.close(); print("\nDONE")
