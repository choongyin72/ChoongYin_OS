"""ECSR-35333 - read-only: is ALL June-2026 deferment data verified? Per facility + status breakdown. Creds from env."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
def q(title, sql):
    print("\n=== " + title + " ===")
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; print(" | ".join(cols))
        n=0
        for r in cur.fetchall():
            print(" | ".join('' if v is None else str(v) for v in r)); n+=1
        if n==0: print("(no rows)")
    except Exception as e:
        print("ERR:", str(e)[:150])

# Per facility: status breakdown for June 2026 (V vs not)
q("June 2026 deferment APPROVAL_STATUS per facility (TV_ZWP_DEF_DAY_DETAIL)",
  """select e.DEF_FCTY_1_CODE fcty,
          count(*) total_rows,
          sum(case when d.APPROVAL_STATUS='V' then 1 else 0 end) verified,
          sum(case when nvl(d.APPROVAL_STATUS,'P')!='V' then 1 else 0 end) not_verified,
          listagg(distinct nvl(d.APPROVAL_STATUS,'(null)'),',') within group (order by nvl(d.APPROVAL_STATUS,'(null)')) statuses
     from TV_ZWP_DEF_DAY_DETAIL d
     join ov_eqpm e on e.OBJECT_ID = d.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime <= DATE '2026-06-01' and nvl(e.end_date, DATE '2026-07-01') > DATE '2026-06-01'
    where d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')
    group by e.DEF_FCTY_1_CODE order by not_verified desc, fcty""")

# Overall grand total
q("June 2026 overall verified vs not-verified (all facilities)",
  """select count(*) total_rows,
          sum(case when d.APPROVAL_STATUS='V' then 1 else 0 end) verified,
          sum(case when nvl(d.APPROVAL_STATUS,'P')!='V' then 1 else 0 end) not_verified
     from TV_ZWP_DEF_DAY_DETAIL d
     join ov_eqpm e on e.OBJECT_ID = d.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime <= DATE '2026-06-01' and nvl(e.end_date, DATE '2026-07-01') > DATE '2026-06-01'
    where d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')""")
c.close(); print("\nDONE")
