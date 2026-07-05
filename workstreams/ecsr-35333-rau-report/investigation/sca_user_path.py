"""Name the exact screens/objects a user needs: deferment screens, forecast screens, the PNI working forecast group."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
def q(t,sql,binds=None):
    print("\n=== "+t+" ===")
    try:
        cur.execute(sql,binds or {}); 
        for r in cur.fetchall(): print("  "," | ".join('' if v is None else str(v) for v in r))
    except Exception as e: print("  ERR:",str(e)[:140])

q("PNI's WORKING forecast group (the pattern to copy)",
  """select fg.object_code, fgv.name, to_char(fgv.daytime,'YYYY-MM-DD'), to_char(fgv.end_date,'YYYY-MM-DD')
     from forecast_group fg join forecast_group_version fgv on fgv.object_id=fg.object_id
     where fg.object_id='45A9A31E15CD4198E0630100007F1329'""")

q("Does SCA have ANY forecast group rows in FCST_FCTY_DAY (June)?",
  """select f.FORECAST_ID, fg.object_code, count(*) 
     from FCST_FCTY_DAY f left join forecast_group fg on fg.object_id=f.forecast_id
     where f.object_id='45A9A31E0AA14198E0630100007F1329'
       and f.daytime between DATE '2026-06-01' and DATE '2026-06-30'
     group by f.FORECAST_ID, fg.object_code""")

q("Screens: deferment + forecast + equipment (BUSINESS_FUNCTION)",
  """select bf_code, name from business_function
     where lower(name) like '%defer%' or lower(name) like '%forecast group%' 
        or lower(name) like '%facility day forecast%' or lower(name) like '%120%'
     order by bf_code""")

q("SCA equipment: Stream Reference Capacity attribute set?",
  """select ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id('45A9A31E13C84198E0630100007F1329',DATE '2026-06-01','<=')),
            ec_zwp_equipment.zwp_strm_ref_capacity(ec_eqpm_version.rec_id('45A9A31E13A04198E0630100007F1329',DATE '2026-06-01','<='))
     from dual""")
c.close()
