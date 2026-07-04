"""RC.0057 final pre-flight (READ-ONLY): confirm test member baseline + the existing rows
under TRACT_U3_T01 (which I must NOT touch)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
M = "108_WB1-1_PF1"; T = "TRACT_U3_T01"

cur.execute("SELECT COUNT(*) FROM dv_tract_well_setup WHERE perf_interval_code=:m", m=M)
print(f"{M} membership rows in ANY tract (baseline, expect 0):", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM dv_tract_well_setup WHERE object_code=:t AND perf_interval_code=:m", t=T, m=M)
print(f"{T} x {M} (expect 0 = safe pair):", cur.fetchone()[0])
cur.execute("SELECT perf_interval_code, sort_order FROM dv_tract_well_setup WHERE object_code=:t ORDER BY sort_order", t=T)
print(f"EXISTING rows under {T} (must NOT touch):", cur.fetchall())
cur.execute("SELECT TO_CHAR(object_start_date,'YYYY-MM-DD') FROM ov_perf_interval WHERE code=:m", m=M)
print(f"{M} effective start:", cur.fetchall())
c.close()
