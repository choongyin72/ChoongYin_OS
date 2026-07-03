import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
cur.execute("""select s.DAYTIME, s.ASSET_CODE, round(s.CAPACITY,2) capacity, round(s.PRODUCTION,2) production, round(s.DEFERMENT,2) deferment
   from TV_ZWP_DEF_DAY_SUMMARY s
   join ov_eqpm e on e.OBJECT_ID=s.ASSET_ID and e.eqpm_type='DEFERMENT'
      and e.daytime<=DATE '2026-06-01' and nvl(e.end_date,DATE '2026-07-01')>DATE '2026-06-01'
   where e.DEF_FCTY_1_CODE='SCA_OFFSHORE'
     and s.DAYTIME>=DATE '2026-06-01' and s.DAYTIME<=LAST_DAY(DATE '2026-06-01')
   order by s.DAYTIME""")
rows=cur.fetchall()
print("DAY | ASSET_CODE | CAPACITY | PRODUCTION | DEFERMENT")
for r in rows: print(r[0].strftime('%Y-%m-%d'), "|", r[1], "|", r[2], "|", r[3], "|", r[4])
caps=[r[2] for r in rows]
print(f"\nrows={len(rows)}  |  CAPACITY: min={min(caps)} max={max(caps)}  |  #rows with CAPACITY<>0 = {sum(1 for x in caps if x not in (0,None))}")
c.close()
