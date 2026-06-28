"""ECSR-35333 READ-ONLY diagnostic: why PLU_LNG_TRAIN1 -> NULL but PLU_LNG_TRAIN2 -> garbage.
Checks the SUB_004 eqpm INNER JOIN for fan-out / expired-version duplication and the
contract->ACT-event resolution. Creds from ENV. SELECT-only."""
import os, oracledb
con = oracledb.connect(user=os.environ["EC_DB_USER"], password=os.environ["EC_DB_PWD"], dsn=os.environ["EC_DB_DSN"])
cur = con.cursor()
FAC = "('PLU_LNG_TRAIN1','PLU_LNG_TRAIN2')"

print("=== (A) ALL DEFERMENT eqpm rows for the two trains (date-effectivity visible) ===")
cur.execute(f"""SELECT def_fcty_1_code, code, name, zwp_contract_code, zwp_contract_id,
       TO_CHAR(daytime,'YYYY-MM-DD') start_dt, TO_CHAR(end_date,'YYYY-MM-DD') end_dt,
       NVL(zwp_defer_summary,'N') defsum
   FROM ov_eqpm WHERE eqpm_type='DEFERMENT' AND def_fcty_1_code IN {FAC}
   ORDER BY def_fcty_1_code, code, daytime""")
for r in cur: print("   ", r)

print("\n=== (B) rows the VIEW's eqpm CTE actually selects (its exact filter) - fan-out check ===")
cur.execute(f"""SELECT def_fcty_1_code, COUNT(*) n_rows,
       LISTAGG(zwp_contract_code||'['||TO_CHAR(daytime,'YYYY-MM')||'..'||NVL(TO_CHAR(end_date,'YYYY-MM'),'open')||']',' ; ')
         WITHIN GROUP (ORDER BY daytime) AS contracts
   FROM ov_eqpm
   WHERE eqpm_type='DEFERMENT' AND NVL(zwp_defer_summary,'N')='Y'
     AND daytime <= SYSDATE AND (end_date IS NULL OR end_date <= SYSDATE)
     AND def_fcty_1_code IN {FAC}
   GROUP BY def_fcty_1_code""")
for r in cur: print("   ", r)

print("\n=== (C) contract -> object_code -> ACT / ACT_YTD event resolution per train ===")
cur.execute(f"""SELECT e.def_fcty_1_code, e.zwp_contract_code, ca.object_code,
   (SELECT COUNT(*) FROM dv_sctr_acc_mth_event m WHERE m.object_code=ca.object_code AND m.daytime=DATE '2026-06-01'
      AND m.account_code IN ('RAU_AVAILABILITY_ACT','RAU_RELIABILITY_ACT','RAU_UTILISATION_ACT')) period_act_evts,
   (SELECT COUNT(*) FROM dv_sctr_acc_mth_event m WHERE m.object_code=ca.object_code AND m.daytime=DATE '2026-06-01'
      AND m.account_code IN ('RAU_AVAILABILITY_ACT_YTD','RAU_RELIABILITY_ACT_YTD','RAU_UTILISATION_ACT_YTD')) ytd_act_evts
   FROM ov_eqpm e
   JOIN dv_contract_account ca ON ca.object_id = e.zwp_contract_id AND INSTR(ca.account_code,'RAU')>0
   WHERE e.eqpm_type='DEFERMENT' AND NVL(e.zwp_defer_summary,'N')='Y' AND e.def_fcty_1_code IN {FAC}
   GROUP BY e.def_fcty_1_code, e.zwp_contract_code, ca.object_code
   ORDER BY 1,2,3""")
print("   (facility, eqpm_contract, ca.object_code, period_ACT_evts, ACT_YTD_evts)")
for r in cur: print("   ", r)
con.close()
