"""Production domain DB recon: which daily-flow tables exist + hold seed data on the
local sandbox (the learnable flows)."""
import os

import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()

CANDIDATES = [
    # core daily statuses
    "PWEL_DAY_STATUS", "PWEL_SUB_DAY_STATUS", "PWEL_DAY_ALLOC",
    "FCTY1_DAY_STATUS", "FCTY2_DAY_STATUS", "STRM_DAY_STATUS",
    "TANK_DAY_STATUS", "EQPM_DAY_STATUS", "WELL_HOOKUP",
    # testing
    "PWEL_RESULT", "PWEL_PERF_CURVE",
    # deferment
    "DEFERMENT_EVENT", "DEFER_WELL_DAY_ALLOC",
    # allocation / HCA
    "STRM_DAY_ALLOC", "TANK_DAY_ALLOC", "OBJECT_STATUS",
    "PROD_DAY", "SYSTEM_DAYS",
]
for t in CANDIDATES:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        n = cur.fetchone()[0]
        print(f"{t:28s} {n}")
    except Exception:
        print(f"{t:28s} (not found)")

# discover actual table families by prefix
print("\n== families by prefix (tables with rows, top by count) ==")
for pre in ("PWEL", "FCTY", "STRM", "DEFER", "PROD", "TANK", "WELL"):
    cur.execute("""SELECT table_name, num_rows FROM all_tables
                   WHERE owner='ECKERNEL_EC' AND table_name LIKE :p || '%'
                   AND num_rows > 0 ORDER BY num_rows DESC FETCH FIRST 6 ROWS ONLY""", p=pre)
    rows = cur.fetchall()
    print(f"{pre}*: " + ", ".join(f"{t}({n})" for t, n in rows))
conn.close()
