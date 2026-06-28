"""ECSR-35333 READ-ONLY: ZWP_V_DEF_RAU_SUB_004 view definition + the 2026-06-01 report-period
row, to confirm how PERIOD_ACTUAL/YTD_ACTUAL are derived (and that June is NULL).
Creds from ENV (no secrets in file). SELECT-only on ECAASDEV."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()

print("=== ZWP_V_DEF_RAU_SUB_004 view definition ===")
try:
    cur.execute("SELECT text FROM all_views WHERE view_name='ZWP_V_DEF_RAU_SUB_004'")
    row = cur.fetchone()
    print(row[0] if row else "(view not found in all_views)")
except Exception as e:
    print("DDL ERR", str(e)[:120])

print("\n=== SUB_004 rows for the report period DAYTIME=2026-06-01 (LNG Train 1 / PLU_SCA) ===")
try:
    cur.execute("""SELECT TO_CHAR(daytime,'YYYY-MM-DD'), metric_category, production_unit_code, def_fcty_1_code,
                          period_target, period_actual, ytd_target, ytd_actual, yeo, year_end_target
                   FROM ZWP_V_DEF_RAU_SUB_004
                   WHERE daytime = DATE '2026-06-01' AND ROWNUM <= 25""")
    cols = "daytime, metric, PU, fcty, P_tgt, P_act, YTD_tgt, YTD_act, YEO, YE_tgt"
    print("  (", cols, ")")
    for r in cur:
        print("   ", r)
except Exception as e:
    print("ROW ERR", str(e)[:120])
con.close()
