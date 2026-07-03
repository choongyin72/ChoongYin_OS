"""ECSR-35333 RE-OPENED RCA - read-only, aligned to ZWP_P_DEF_RAU_CALC logic. Creds from env.
Tests the source hypothesis: blank = p_capacity NULL/0 (line 409 skips write); invalid = negative auto-deferments."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
def q(title, sql):
    print("\n=== " + title + " ===")
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]; print(" | ".join(cols))
        n=0
        for r in cur.fetchall():
            print(" | ".join('' if v is None else str(v) for v in r)); n+=1
            if n>=50: print("...(more)"); break
        if n==0: print("(no rows)")
    except Exception as e:
        print("ERR:", str(e)[:150])

# A) DEFERMENT eqpm: facility -> asset(object_id) -> contract (effective June 2026)
q("A) DEFERMENT eqpm records (facility/asset/contract)",
  """select DEF_FCTY_1_CODE, OBJECT_ID, ZWP_CONTRACT_CODE
     from ov_eqpm where eqpm_type='DEFERMENT'
       and daytime <= DATE '2026-06-01'
       and nvl(end_date, DATE '2026-07-01') > DATE '2026-06-01'
     order by DEF_FCTY_1_CODE""")

# B) Per asset for June: unverified days, NEGATIVE auto-def (the calc's exact predicate), total deferment
q("B) June per-facility: unverified / NEGATIVE-auto-def / total deferment (TV_ZWP_DEF_DAY_DETAIL)",
  """select e.DEF_FCTY_1_CODE fcty,
          sum(case when nvl(d.APPROVAL_STATUS,'P')!='V' then 1 else 0 end) unverified_days,
          sum(case when d.DEF_QTY_DER < 0 and d.VARIATION='Y' then 1 else 0 end) neg_autodef_days,
          round(sum(nvl(d.DEF_QTY, d.DEF_QTY_DER)),2) total_def
     from TV_ZWP_DEF_DAY_DETAIL d
     join ov_eqpm e on e.OBJECT_ID = d.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime <= DATE '2026-06-01' and nvl(e.end_date, DATE '2026-07-01') > DATE '2026-06-01'
    where d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')
    group by e.DEF_FCTY_1_CODE order by fcty""")

# C) CAPACITY per asset for June from TV_ZWP_DEF_DAY_SUMMARY (Cond/DG/PNI path). NULL/0 => blank actuals.
q("C) June capacity from TV_ZWP_DEF_DAY_SUMMARY per facility (is it NULL/0?)",
  """select e.DEF_FCTY_1_CODE fcty, round(sum(s.CAPACITY),2) capacity_sum, count(*) day_rows
     from TV_ZWP_DEF_DAY_SUMMARY s
     join ov_eqpm e on e.OBJECT_ID = s.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime <= DATE '2026-06-01' and nvl(e.end_date, DATE '2026-07-01') > DATE '2026-06-01'
    where s.DAYTIME >= DATE '2026-06-01' and s.DAYTIME <= LAST_DAY(DATE '2026-06-01')
    group by e.DEF_FCTY_1_CODE order by fcty""")

# D) Do RAU actual events exist now (post 06-30 re-run) per contract + their values
q("D) RAU_*_ACT/_ACT_YTD events June 2026 (DV_SCTR_ACC_MTH_EVENT)",
  """select OBJECT_CODE contract, ACCOUNT_CODE, round(QTY,2) qty
     from DV_SCTR_ACC_MTH_EVENT
     where DAYTIME = DATE '2026-06-01' and ACCOUNT_CODE like 'RAU_%_ACT%'
     order by OBJECT_CODE, ACCOUNT_CODE""")

# E) Report view current state per facility
q("E) ZWP_V_DEF_RAU_SUB_004 June per facility (Period/YTD Actual NULL? YEO?)",
  """select DEF_FCTY_1_CODE, METRIC_CATEGORY, round(PERIOD_TARGET,3) p_tgt, round(PERIOD_ACTUAL,3) p_act,
          round(YTD_ACTUAL,3) ytd_act, round(YEO,3) yeo
     from ZWP_V_DEF_RAU_SUB_004 where DAYTIME = DATE '2026-06-01' order by DEF_FCTY_1_CODE, SORT_ORDER""")
c.close(); print("\nDONE")
