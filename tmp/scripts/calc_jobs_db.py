"""What allocation calcs exist + which networks have runnable jobs (READ-ONLY DB) — answers
'what type of allocation calc can I run?'. Inspects CALCULATION (+VERSION), ALLOC_NETWORK_JOB_CONN,
and joins network names."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()

def cols(t):
    print(f"\n=== {t} columns ===")
    c.execute("SELECT column_name,data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id", t=t)
    for n,dt in c.fetchall(): print(f"   {n:26} {dt}")

def q(label,sql,n=25):
    print(f"\n=== {label} ===")
    try:
        c.execute(sql); rows=c.fetchall()
        for r in rows[:n]: print("  ", tuple(str(v)[:32] for v in r))
        if not rows: print("   (none)")
    except Exception as e: print("   ERR:", str(e)[:130])

cols("CALCULATION")
cols("ALLOC_NETWORK_JOB_CONN")
# calc jobs: name + type
q("CALCULATION rows (name/type/code)",
  """SELECT * FROM (SELECT * FROM ECKERNEL_EC.CALCULATION) WHERE ROWNUM<=30""")
# network -> calc job connections (which network runs which calc)
q("ALLOC_NETWORK_JOB_CONN (network <-> calc job)",
  """SELECT * FROM (SELECT * FROM ECKERNEL_EC.ALLOC_NETWORK_JOB_CONN) WHERE ROWNUM<=30""")
# resolve network names from OV_ALLOC_NETWORK
q("OV_ALLOC_NETWORK columns",
  """SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_ALLOC_NETWORK' ORDER BY column_id""", 40)
print("\nDONE")
