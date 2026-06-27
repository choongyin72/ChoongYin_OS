"""RC.0057 Tract - Well Setup pre-flight (READ-ONLY, local sandbox localhost:1521/ORCL).
Understand DV_TRACT_WELL_SETUP model, find an EMPTY Tract (clean target), the member pool +
a free member (baseline 0), and effective windows - so the live run picks a valid date."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()

print("=== DV_TRACT_WELL_SETUP columns ===")
cur.execute("SELECT column_name, data_type FROM all_tab_columns WHERE table_name='DV_TRACT_WELL_SETUP' AND owner='ECKERNEL_EC' ORDER BY column_id")
cols = [r[0] for r in cur.fetchall()]
for r in cols: print("   ", r)

print("\n=== distinct OBJECT_CODE (Tract parent) + #rows ===")
cur.execute("""SELECT object_code, COUNT(*) n FROM dv_tract_well_setup GROUP BY object_code ORDER BY object_code""")
for r in cur: print("   ", r)

print("\n=== sample rows (first 8) ===")
cur.execute("SELECT * FROM dv_tract_well_setup WHERE ROWNUM<=8")
scols = [d[0] for d in cur.description]
print("   cols:", scols)
for r in cur: print("   ", r)

print("\n=== OV_TRACT: all tracts + effective start (find an EMPTY one) ===")
cur.execute("SELECT code, TO_CHAR(object_start_date,'YYYY-MM-DD'), TO_CHAR(object_end_date,'YYYY-MM-DD') FROM ov_tract ORDER BY code")
tracts = cur.fetchall()
for r in tracts: print("   TRACT:", r)

print("\n=== which tracts are EMPTY in well-setup (clean targets) ===")
cur.execute("""SELECT t.code, TO_CHAR(t.object_start_date,'YYYY-MM-DD')
   FROM ov_tract t WHERE NOT EXISTS (SELECT 1 FROM dv_tract_well_setup w WHERE w.object_code=t.code)
   ORDER BY t.code""")
for r in cur: print("   EMPTY tract:", r)

print("\n=== member pool: OV_PERF_INTERVAL count + a few codes ===")
try:
    cur.execute("SELECT code, TO_CHAR(object_start_date,'YYYY-MM-DD') FROM ov_perf_interval WHERE ROWNUM<=6 ORDER BY code")
    for r in cur: print("   PERF_INTERVAL:", r)
except Exception as e:
    print("   err", str(e)[:80])
c.close()
