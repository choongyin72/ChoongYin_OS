"""Self-clean: revert the AVG_BH_TEMP demo values I wrote into PWEL_DAY_STATUS back to NULL (as-found).
Reads the current rows first (proof), NULLs ONLY avg_bh_temp for the 3 demo wells on the demo dates, verifies
via the view. Non-destructive beyond undoing my own writes. py -X utf8 this.
"""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"))
cur = conn.cursor()
WELLS = ("AS1_Well_001", "AS1_Well_002", "AS1_Well_003")
DATES = ("2003-01-05", "2003-01-07", "2003-01-09", "2003-01-10")
inlist = ",".join(f"'{w}'" for w in WELLS)
dlist = ",".join(f"TO_DATE('{d}','YYYY-MM-DD')" for d in DATES)

print("BEFORE revert (dv_pwel_day_status avg_bh_temp):")
cur.execute(f"""SELECT object_code, TO_CHAR(daytime,'YYYY-MM-DD') d, avg_bh_temp FROM dv_pwel_day_status
                WHERE object_code IN ({inlist}) AND daytime IN ({dlist}) AND avg_bh_temp IS NOT NULL
                ORDER BY d, object_code""")
rows = cur.fetchall()
for r in rows:
    print("  ", r)
print(f"  ({len(rows)} non-null rows to revert)")

# resolve object ids
cur.execute(f"SELECT code, object_id FROM ov_well WHERE code IN ({inlist})")
oid = {c: o for c, o in cur.fetchall()}
print("object ids:", oid)

# NULL only avg_bh_temp on the base table for those object_ids + dates
upd = cur.execute(f"""UPDATE pwel_day_status SET avg_bh_temp = NULL
                      WHERE object_id IN ({",".join(f"'{o}'" for o in oid.values())})
                      AND daytime IN ({dlist}) AND avg_bh_temp IS NOT NULL""")
print("rows updated:", cur.rowcount)
conn.commit()

print("\nAFTER revert:")
cur.execute(f"""SELECT object_code, TO_CHAR(daytime,'YYYY-MM-DD') d, avg_bh_temp FROM dv_pwel_day_status
                WHERE object_code IN ({inlist}) AND daytime IN ({dlist}) ORDER BY d, object_code""")
for r in cur.fetchall():
    print("  ", r)
conn.close()
print("DONE")
