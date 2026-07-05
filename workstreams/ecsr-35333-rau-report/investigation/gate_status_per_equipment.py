"""Stage-A verification-gate status per DEFERMENT equipment, June 2026 (read-only, exact calc predicate)."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur=c.cursor()
cur.execute("""
  select e.DEF_FCTY_1_CODE, f.NAME, e.ZWP_CONTRACT_CODE,
         count(*) total_rows,
         sum(case when d.APPROVAL_STATUS='V' then 1 else 0 end) verified,
         sum(case when nvl(d.APPROVAL_STATUS,'P')!='V' then 1 else 0 end) not_verified
  from ov_eqpm e
  join ov_fcty_class_1 f on f.object_id = e.DEF_FCTY_1_ID
  left join TV_ZWP_DEF_DAY_DETAIL d
    on d.ASSET_ID = e.OBJECT_ID
   and d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')
  where e.eqpm_type='DEFERMENT'
    and e.daytime <= DATE '2026-06-01' and nvl(e.end_date, DATE '2026-07-01') > DATE '2026-06-01'
  group by e.DEF_FCTY_1_CODE, f.NAME, e.ZWP_CONTRACT_CODE
  order by not_verified desc, e.DEF_FCTY_1_CODE""")
print(f"{'EQUIPMENT FACILITY':16} {'NAME':16} {'CONTRACT':16} {'ROWS':>5} {'VERIF':>6} {'PENDING':>8}  GATE RESULT")
for code,name,ctr,tot,v,nv in cur.fetchall():
    gate = "BLOCKED (skip - no actuals)" if (nv or 0)>=1 else "PASS (calc proceeds)"
    print(f"{code:16} {name:16} {ctr:16} {tot or 0:>5} {v or 0:>6} {nv or 0:>8}  {gate}")
c.close()
