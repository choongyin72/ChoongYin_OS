import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
# eqpm object ids from query A
ids = {'SCA_OFFSHORE':'45A9A31E13C84198E0630100007F1329',
       'PLU_PNI':'45A9A31E13B04198E0630100007F1329',
       'PLU_COND':'45A9A31E13A84198E0630100007F1329',
       'PLU_DG':'45A9A31E13904198E0630100007F1329'}
print("=== zwp_p_defer_custom.getCapacity('EQPM', <eqpm>, 2026-06-01) ===")
for code,oid in ids.items():
    try:
        cur.execute("select zwp_p_defer_custom.getCapacity('EQPM', :1, DATE '2026-06-01') from dual",[oid])
        print(f"{code:15} -> {cur.fetchone()[0]}")
    except Exception as e:
        print(f"{code:15} -> ERR {str(e)[:90]}")

print("\n=== locate getCapacity in ZWP_P_DEFER_CUSTOM body ===")
cur.execute("""select line, text from all_source
   where name='ZWP_P_DEFER_CUSTOM' and type='PACKAGE BODY'
     and lower(text) like '%function getcapacity%' order by line""")
for ln,tx in cur.fetchall(): print("start line", ln, ":", tx.strip())
c.close(); print("DONE-locate")
