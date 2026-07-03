import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
f={'SCA':'45A9A31E0AA14198E0630100007F1329','PNI':'45A9A31E0AF14198E0630100007F1329'}
for code,fid in f.items():
    print(f"\n=== {code} facility_class_1 {fid} ===")
    try:
        cur.execute("select prod_plan_method from fcty_version where object_id=:1 and daytime<=DATE '2026-06-01' order by daytime desc fetch first 1 rows only",[fid])
        r=cur.fetchone(); print("  prod_plan_method:", r[0] if r else "(none)")
    except Exception as e: print("  prod_plan_method ERR:", str(e)[:90])
    try:
        cur.execute("select zwp_p_defer_custom.getGroupForecastId(:1, DATE '2026-06-01','CAPACITY') from dual",[fid])
        gid=cur.fetchone()[0]; print("  getGroupForecastId(CAPACITY):", gid)
        if gid:
            cur.execute("""select round(sum(nvl(ZWP_LNG_CAPACITY,0)),2) sum_lng_cap, count(*) rows_jun
                           from DV_FCST_FCTY1_DAY_STATUS
                           where FORECAST_ID=:1 and DAYTIME between DATE '2026-06-01' and LAST_DAY(DATE '2026-06-01')""",[gid])
            r=cur.fetchone(); print(f"  forecast ZWP_LNG_CAPACITY June: sum={r[0]} over {r[1]} rows")
    except Exception as e: print("  forecast ERR:", str(e)[:110])
c.close(); print("\nDONE")
