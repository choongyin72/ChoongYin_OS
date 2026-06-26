"""
ECSR-35333 READ-ONLY recon on ECAASDEV (QDB) - validate the report's source views vs the
3 ticket issues. Creds come from ENV (EC_DB_DSN/EC_DB_USER/EC_DB_PWD) so this file carries
no secrets. SELECT-only; ECAASDEV is read-only for us.
Run: EC_DB_DSN=... EC_DB_USER=... EC_DB_PWD=... py ecaasdev_rau_recon.py
"""
import os, oracledb

con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"],
                       dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()

VIEWS = ["ZWP_V_DEF_RAU_SUB_004", "ZWP_V_REP_RAU_PERF_MTH", "ZWP_V_REP_RAU_DEF_SUMMARY",
         "ZWP_V_REP_RAU_DEF_DETAIL", "ZWP_V_DEF_RAU_SUB_003"]
print("=== view existence + row counts ===")
for v in VIEWS:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {v}")
        print(f"  {v:28} rows={cur.fetchone()[0]}")
    except Exception as e:
        print(f"  {v:28} ERR {str(e)[:60]}")

print("\n=== ZWP_V_DEF_RAU_SUB_004 (Issue 1: Period/YTD Actual; Issue 3: YEO) ===")
try:
    cur.execute("SELECT TO_CHAR(MAX(daytime),'YYYY-MM-DD'), COUNT(*), "
                "SUM(CASE WHEN period_actual IS NULL THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN ytd_actual IS NULL THEN 1 ELSE 0 END), "
                "SUM(CASE WHEN yeo IS NULL THEN 1 ELSE 0 END) FROM ZWP_V_DEF_RAU_SUB_004")
    mx, n, pa_null, ytd_null, yeo_null = cur.fetchone()
    print(f"  max(daytime)={mx}  rows={n}  PERIOD_ACTUAL null={pa_null}  YTD_ACTUAL null={ytd_null}  YEO null={yeo_null}")
    cur.execute("SELECT TO_CHAR(daytime,'YYYY-MM-DD'), metric_category, production_unit_code, "
                "period_target, period_actual, ytd_target, ytd_actual, yeo, year_end_target "
                "FROM ZWP_V_DEF_RAU_SUB_004 WHERE daytime=(SELECT MAX(daytime) FROM ZWP_V_DEF_RAU_SUB_004) "
                "AND ROWNUM<=10")
    print("  sample latest-month rows (daytime, metric, PU, P_tgt, P_act, YTD_tgt, YTD_act, YEO, YE_tgt):")
    for r in cur:
        print("   ", r)
except Exception as e:
    print("  ERR", str(e)[:120])

print("\n=== ZWP_V_REP_RAU_PERF_MTH (YEO_TTD for Issue 3) ===")
try:
    cur.execute("SELECT TO_CHAR(daytime,'YYYY-MM-DD'), facility, metric_category, loss_type, yeo_ttd "
                "FROM ZWP_V_REP_RAU_PERF_MTH WHERE daytime=(SELECT MAX(daytime) FROM ZWP_V_REP_RAU_PERF_MTH) "
                "AND ROWNUM<=10")
    print("  sample latest rows (daytime, facility, metric, loss_type, YEO_TTD):")
    for r in cur:
        print("   ", r)
except Exception as e:
    print("  ERR", str(e)[:120])
con.close()
