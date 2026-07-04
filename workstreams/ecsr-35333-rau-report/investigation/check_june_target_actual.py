"""ECSR-35333 READ-ONLY: for June 2026, is SUB_004.PERIOD_TARGET also NULL (not just ACTUAL)?
Decompose vs the underlying RAU contract-account monthly events. Creds from ENV."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()

print("=== (1) ZWP_V_DEF_RAU_SUB_004 rows for DAYTIME=2026-06-01 ===")
cur.execute("""SELECT metric_category, production_unit_code, def_fcty_1_code,
                      period_target, period_actual, ytd_target, ytd_actual, yeo, year_end_target
               FROM zwp_v_def_rau_sub_004 WHERE daytime = DATE '2026-06-01'
               ORDER BY def_fcty_1_code, metric_category""")
print("  (metric, PU, fcty, P_tgt, P_act, YTD_tgt, YTD_act, YEO, YE_tgt)")
for r in cur: print("   ", r)

print("\n=== (1b) null-counts for June ===")
cur.execute("""SELECT COUNT(*) rows_,
       SUM(CASE WHEN period_target IS NULL THEN 1 ELSE 0 END) ptgt_null,
       SUM(CASE WHEN period_actual IS NULL THEN 1 ELSE 0 END) pact_null,
       SUM(CASE WHEN ytd_target    IS NULL THEN 1 ELSE 0 END) ytdtgt_null,
       SUM(CASE WHEN ytd_actual    IS NULL THEN 1 ELSE 0 END) ytdact_null
       FROM zwp_v_def_rau_sub_004 WHERE daytime = DATE '2026-06-01'""")
print("   rows, P_tgt_null, P_act_null, YTD_tgt_null, YTD_act_null =", cur.fetchone())

print("\n=== (2) RAU contract-account monthly events feeding the view, June 2026 ===")
try:
    cur.execute("""SELECT object_code, account_code, qty, TO_CHAR(daytime,'YYYY-MM-DD') dt
                   FROM dv_sctr_acc_mth_event
                   WHERE account_code LIKE 'RAU\\_%' ESCAPE '\\' AND daytime = DATE '2026-06-01'
                   ORDER BY object_code, account_code""")
    rows = cur.fetchall()
    print(f"   {len(rows)} RAU events on 2026-06-01:")
    for r in rows: print("   ", r)
except Exception as e:
    print("   ERR", str(e)[:120])

print("\n=== (2b) RAU event suffixes present per month (TRGT/ACT/YTD...) ===")
try:
    cur.execute("""SELECT TO_CHAR(daytime,'YYYY-MM') ym,
                          SUBSTR(account_code, INSTR(account_code,'_',-1)+1) suffix, COUNT(*) n
                   FROM dv_sctr_acc_mth_event
                   WHERE account_code LIKE 'RAU\\_%' ESCAPE '\\'
                     AND daytime BETWEEN DATE '2026-01-01' AND DATE '2026-08-01'
                   GROUP BY TO_CHAR(daytime,'YYYY-MM'), SUBSTR(account_code, INSTR(account_code,'_',-1)+1)
                   ORDER BY 1,2""")
    for r in cur: print("   ", r)
except Exception as e:
    print("   ERR", str(e)[:120])
con.close()
