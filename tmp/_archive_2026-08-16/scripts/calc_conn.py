"""Which Allocation Network runs which Calculation Job (READ-ONLY) — gives valid (network, job,
date) combos to trigger an allocation directly. Joins ALLOC_NETWORK_JOB_CONN -> OV_ALLOC_NETWORK
(name) + CALCULATION (job code)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL", tcp_connect_timeout=15).cursor()

# network name columns
print("=== OV_ALLOC_NETWORK columns ===")
c.execute("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_ALLOC_NETWORK' ORDER BY column_id")
print("  ", [r[0] for r in c.fetchall()])

print("\n=== network <-> calc-job connections (name resolved) ===")
try:
    c.execute("""SELECT n.NAME net, j.OBJECT_CODE job, j.CALC_PERIOD, j.CALC_TYPE, j.CALC_SCOPE,
                        TO_CHAR(conn.DAYTIME,'YYYY-MM-DD') frm, TO_CHAR(conn.END_DATE,'YYYY-MM-DD') too
                 FROM ECKERNEL_EC.ALLOC_NETWORK_JOB_CONN conn
                 JOIN ECKERNEL_EC.OV_ALLOC_NETWORK n ON n.OBJECT_ID = conn.ALLOC_NETWORK_ID
                 JOIN ECKERNEL_EC.CALCULATION j ON j.OBJECT_ID = conn.JOB_ID
                 ORDER BY n.NAME""")
    rows=c.fetchall()
    for r in rows[:40]: print("  ", tuple(str(v)[:26] for v in r))
    print("  total connections:", len(rows))
except Exception as e:
    print("  ERR:", str(e)[:160])

# which MAIN jobs exist (the runnable ones)
print("\n=== MAIN-scope (runnable) calc jobs ===")
c.execute("""SELECT OBJECT_CODE, CALC_PERIOD, CALC_TYPE FROM ECKERNEL_EC.CALCULATION
             WHERE CALC_SCOPE='MAIN' AND (END_DATE IS NULL OR END_DATE > SYSDATE) ORDER BY OBJECT_CODE""")
for r in c.fetchall(): print("  ", r)
print("\nDONE")
