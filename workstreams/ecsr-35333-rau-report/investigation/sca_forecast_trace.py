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

# The calc gets the CAPACITY forecast group per facility. Compare SCA vs PNI.
run("getGroupForecastId CAPACITY: SCA vs PNI (facility class1 ids)",
  """select 'SCA' who, zwp_p_defer_custom.getGroupForecastId('45A9A31E0AA14198E0630100007F1329', DATE '2026-06-01','CAPACITY') grp from dual
     union all
     select 'PNI', zwp_p_defer_custom.getGroupForecastId('45A9A31E0AAB4198E0630100007F1329', DATE '2026-06-01','CAPACITY') from dual""")

# Where does the summary CAPACITY come from - is there ANY capacity forecast/target for SCA in June?
run("Forecast facility-day-status rows June by facility (DV_FCST_FCTY1_DAY_STATUS)",
  """select FORECAST_ID, count(*) rows_jun, round(sum(nvl(CAPACITY,0)),0) sum_capacity
     from DV_FCST_FCTY1_DAY_STATUS
     where DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')
     group by FORECAST_ID order by FORECAST_ID""")
c.close(); print("\nDONE")
