"""Read-only post-run check: existing TRACT_U3_T01 rows intact + test member gone + sentinel gone."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
cur.execute("SELECT perf_interval_code, sort_order FROM dv_tract_well_setup WHERE object_code='TRACT_U3_T01' ORDER BY sort_order")
print("TRACT_U3_T01 rows (expect P1 PI-5/PI-6 only):", cur.fetchall())
cur.execute("SELECT COUNT(*) FROM dv_tract_well_setup WHERE perf_interval_code='108_WB1-1_PF1'")
print("108_WB1-1_PF1 rows (expect 0):", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM dv_tract_well_setup WHERE comments='AUTOTEST_TWS_UPD'")
print("AUTOTEST_TWS_UPD sentinel rows (expect 0):", cur.fetchone()[0])
c.close()
