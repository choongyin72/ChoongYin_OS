import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
def run(t,sql):
    print("\n=== "+t+" ===")
    try:
        cur.execute(sql); print(" | ".join(d[0] for d in cur.description)); n=0
        for r in cur.fetchall(): print(" | ".join('' if v is None else str(v) for v in r)); n+=1
        if n==0: print("(none)")
    except Exception as e: print("ERR:",str(e)[:180])

# 1) columns of TV_ZWP_DEF_DAY_SUMMARY
run("columns TV_ZWP_DEF_DAY_SUMMARY",
    "select column_name from all_tab_columns where table_name='TV_ZWP_DEF_DAY_SUMMARY' order by column_id")

# 2) SCA vs a working facility (PNI) - summary rows June, key cols
run("SCA June summary rows (first 5)",
    """select s.DAYTIME, round(s.CAPACITY,2) capacity, s.* 
       from TV_ZWP_DEF_DAY_SUMMARY s
       join ov_eqpm e on e.OBJECT_ID=s.ASSET_ID and e.eqpm_type='DEFERMENT'
          and e.daytime<=DATE '2026-06-01' and nvl(e.end_date,DATE '2026-07-01')>DATE '2026-06-01'
       where e.DEF_FCTY_1_CODE='SCA_OFFSHORE' and s.DAYTIME>=DATE '2026-06-01' and s.DAYTIME<=LAST_DAY(DATE '2026-06-01')
       order by s.DAYTIME fetch first 5 rows only""")

run("PNI June summary rows (first 5, working ref)",
    """select s.DAYTIME, round(s.CAPACITY,2) capacity, s.*
       from TV_ZWP_DEF_DAY_SUMMARY s
       join ov_eqpm e on e.OBJECT_ID=s.ASSET_ID and e.eqpm_type='DEFERMENT'
          and e.daytime<=DATE '2026-06-01' and nvl(e.end_date,DATE '2026-07-01')>DATE '2026-06-01'
       where e.DEF_FCTY_1_CODE='PLU_PNI' and s.DAYTIME>=DATE '2026-06-01' and s.DAYTIME<=LAST_DAY(DATE '2026-06-01')
       order by s.DAYTIME fetch first 5 rows only""")
c.close(); print("\nDONE")
