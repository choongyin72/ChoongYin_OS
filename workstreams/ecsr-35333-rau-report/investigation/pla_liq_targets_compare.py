import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
print("=== RAU TRGT-family events, full year 2026, PLA contracts ===")
cur.execute("""select OBJECT_CODE, ACCOUNT_CODE, count(*) n, min(QTY), max(QTY)
   from DV_SCTR_ACC_MTH_EVENT
   where DAYTIME >= DATE '2026-01-01' and DAYTIME < DATE '2027-01-01'
     and OBJECT_CODE in ('C_PLA_GAS_EXP','C_PLA_LIQ_EXP')
     and (ACCOUNT_CODE like '%TRGT%' or ACCOUNT_CODE like '%TARGET%')
   group by OBJECT_CODE, ACCOUNT_CODE order by OBJECT_CODE, ACCOUNT_CODE""")
rows=cur.fetchall()
if not rows: print("  (none)")
for r in rows: print("  "," | ".join(str(v) for v in r))
print("\n=== June SUB_004 rows for the two PLA contracts (targets vs actuals) ===")
cur.execute("""select CODE, METRIC_CATEGORY, round(PERIOD_TARGET,4), round(PERIOD_ACTUAL,4), round(YTD_TARGET,4), round(YTD_ACTUAL,4), round(YEO,4), round(YEAR_END_TARGET,4)
   from ZWP_V_DEF_RAU_SUB_004 where DAYTIME=DATE '2026-06-01' and CODE in ('PLA_GAS_EXP','PLA_LIQ_EXP') order by CODE, SORT_ORDER""")
print("  CODE | METRIC | P_TGT | P_ACT | YTD_TGT | YTD_ACT | YEO | YE_TGT")
for r in cur.fetchall(): print("  "," | ".join('' if v is None else str(v) for v in r))
c.close()
