import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
def run(t,sql,args=None):
    print("\n=== "+t+" ===")
    try:
        cur.execute(sql,args or {}); print(" | ".join(d[0] for d in cur.description)); n=0
        for r in cur.fetchall(): print(" | ".join('' if v is None else str(v) for v in r)); n+=1
        if n==0: print("(none)")
    except Exception as e: print("ERR:",str(e)[:160])

# 1) PNI's valid group - what object is it?
run("PNI's CAPACITY forecast group 45A9A31E15CD... (name/code)",
  """select object_id, code, name, to_char(daytime,'YYYY-MM-DD') start_dt, to_char(end_date,'YYYY-MM-DD') end_dt
     from ov_forecast_prod where object_id='45A9A31E15CD4198E0630100007F1329'
     union all
     select object_id, code, name, null, null from forecast_group where object_id='45A9A31E15CD4198E0630100007F1329' and rownum=1""")

# 2) Which facilities have CAPACITY forecast data loaded in June (ZWP_T_FCST_FCTY_DAY capacity present)
run("Facilities WITH June capacity forecast rows (ZWP_T_FCST_FCTY_DAY via FCST_FCTY_DAY)",
  """select ecdp_objects.getobjcode(f.object_id) fcty_code, count(*) rows_with_cap
     from FCST_FCTY_DAY f
     join ZWP_T_FCST_FCTY_DAY z on z.rec_id = f.rec_id
     where f.daytime between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')
       and (z.ZWP_GAS_CAPACITY is not null or z.ZWP_LNG_CAPACITY is not null or z.ZWP_COND_CAPACITY is not null or z.ZWP_NET_OIL_CAPACITY is not null)
     group by ecdp_objects.getobjcode(f.object_id) order by fcty_code""")

# 3) Does SCA facility appear in FCST_FCTY_DAY at all for June?
run("SCA facility rows in FCST_FCTY_DAY June (any forecast at all?)",
  """select f.FORECAST_ID, count(*) rows_jun
     from FCST_FCTY_DAY f
     where f.object_id='45A9A31E0AA14198E0630100007F1329'
       and f.daytime between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')
     group by f.FORECAST_ID""")
c.close(); print("\nDONE")
