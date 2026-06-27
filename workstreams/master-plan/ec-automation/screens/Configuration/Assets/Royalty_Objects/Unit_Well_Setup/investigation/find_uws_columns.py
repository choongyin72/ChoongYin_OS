"""RC.0050 columns + sample (local sandbox, read-only)."""
import oracledb
c = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = c.cursor()
for t in ("DV_UNIT_WELL_SETUP", "WELL_SETUP"):
    print(f"\n=== {t} columns ===")
    cur.execute("SELECT column_name, data_type FROM all_tab_columns WHERE table_name=:t AND owner='ECKERNEL_EC' ORDER BY column_id", [t])
    for r in cur: print(f"   {r[0]:32} {r[1]}")
print("\n=== DV_UNIT_WELL_SETUP row count + 5 sample rows ===")
cur.execute("SELECT COUNT(*) FROM dv_unit_well_setup"); print("   rows:", cur.fetchone()[0])
cur.execute("SELECT * FROM dv_unit_well_setup WHERE ROWNUM<=5")
cols = [d[0] for d in cur.description]
print("   cols:", cols)
for r in cur: print("   ", r)
c.close()
