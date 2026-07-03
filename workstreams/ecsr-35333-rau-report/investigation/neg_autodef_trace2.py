import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
def run(t, sql):
    print("\n=== "+t+" ===")
    try:
        cur.execute(sql); print(" | ".join(d[0] for d in cur.description))
        n=0
        for r in cur.fetchall(): print(" | ".join('' if v is None else str(v) for v in r)); n+=1
        if n==0: print("(none)")
    except Exception as e: print("ERR:", str(e)[:180])

# negative auto-def rows per facility + what kind (title/cause/loss)
run("Negative auto-def rows June 2026 (VARIATION='Y', DEF_QTY_DER<0) - sample",
  """select e.DEF_FCTY_1_CODE fcty, d.DAYTIME, d.LOSS_CATEGORY, d.LOSS_TYPE, d.VARIATION,
          round(d.DEF_QTY,2) def_qty, round(d.DEF_QTY_DER,2) def_qty_der,
          d.DEFERMENT_EVENT_TITLE, d.CAUSE, d.KEEP_FLAG
     from TV_ZWP_DEF_DAY_DETAIL d
     join ov_eqpm e on e.OBJECT_ID=d.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime<=DATE '2026-06-01' and nvl(e.end_date,DATE '2026-07-01')>DATE '2026-06-01'
    where d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')
      and d.DEF_QTY_DER < 0 and d.VARIATION='Y'
    order by e.DEF_FCTY_1_CODE, d.DAYTIME fetch first 20 rows only""")

# distinct titles/causes of the negative auto-defs (what are they?)
run("Distinct title/cause/loss of negative auto-defs June",
  """select e.DEF_FCTY_1_CODE fcty, d.DEFERMENT_EVENT_TITLE, d.LOSS_CATEGORY, d.CAUSE, count(*) n,
          round(min(d.DEF_QTY_DER),2) min_der, round(max(d.DEF_QTY_DER),2) max_der
     from TV_ZWP_DEF_DAY_DETAIL d
     join ov_eqpm e on e.OBJECT_ID=d.ASSET_ID and e.eqpm_type='DEFERMENT'
        and e.daytime<=DATE '2026-06-01' and nvl(e.end_date,DATE '2026-07-01')>DATE '2026-06-01'
    where d.DAYTIME >= DATE '2026-06-01' and d.DAYTIME <= LAST_DAY(DATE '2026-06-01')
      and d.DEF_QTY_DER < 0 and d.VARIATION='Y'
    group by e.DEF_FCTY_1_CODE, d.DEFERMENT_EVENT_TITLE, d.LOSS_CATEGORY, d.CAUSE
    order by n desc""")
c.close(); print("\nDONE")
