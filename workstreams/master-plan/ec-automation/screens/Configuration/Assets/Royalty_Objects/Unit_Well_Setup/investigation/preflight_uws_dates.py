"""RC.0050 final pre-flight (READ-ONLY): effective windows + clean-target + delta baseline,
so the live run picks a date inside both the Unit Agreement and Perf Interval windows."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()

print("=== OV_UNIT_AGR: UNIT_3 effective window ===")
cur.execute("""SELECT code, TO_CHAR(object_start_date,'YYYY-MM-DD'),
       TO_CHAR(object_end_date,'YYYY-MM-DD') FROM ov_unit_agr WHERE code='UNIT_3'""")
for r in cur: print("   ", r)

print("\n=== OV_PERF_INTERVAL: 108_WB1-1_PF1 effective window ===")
try:
    cur.execute("""SELECT code, TO_CHAR(object_start_date,'YYYY-MM-DD'),
           TO_CHAR(object_end_date,'YYYY-MM-DD') FROM ov_perf_interval WHERE code='108_WB1-1_PF1'""")
    for r in cur: print("   ", r)
except Exception as e:
    print("   err", str(e)[:90])

print("\n=== clean target: DV_UNIT_WELL_SETUP rows for OBJECT_CODE='UNIT_3' (expect 0) ===")
cur.execute("SELECT COUNT(*) FROM dv_unit_well_setup WHERE object_code='UNIT_3'")
print("   UNIT_3 well-setup rows:", cur.fetchone()[0])

print("\n=== delta baseline: DV_UNIT_WELL_SETUP rows for PERF_INTERVAL_CODE='108_WB1-1_PF1' ===")
cur.execute("SELECT COUNT(*) FROM dv_unit_well_setup WHERE perf_interval_code='108_WB1-1_PF1'")
print("   108_WB1-1_PF1 membership rows (any agreement):", cur.fetchone()[0])

print("\n=== combined scope check: UNIT_3 + 108_WB1-1_PF1 (expect 0 = safe test pair) ===")
cur.execute("SELECT COUNT(*) FROM dv_unit_well_setup WHERE object_code='UNIT_3' AND perf_interval_code='108_WB1-1_PF1'")
print("   UNIT_3 x 108_WB1-1_PF1:", cur.fetchone()[0])
c.close()
