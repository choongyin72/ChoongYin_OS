"""Baseline ALL numeric columns of FRMW Well 1 @ 2024-10-01 00:00 BEFORE a manual save test, so I can
(a) detect exactly which DB column the user's grid edit lands in, and (b) revert precisely to original
(no assumptions). Writes the baseline to tmp/n1_subdaily_baseline.json. Read-only."""
import os, json
import oracledb
OID = "AEBC774296C611E6E053020011ACFDF3"; D = "2024-10-01"; HH = "00:00"
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' "
            "AND data_type='NUMBER' AND column_name<>'OBJECT_ID' ORDER BY column_id")
cols = [r[0] for r in cur.fetchall()]
sel = ", ".join(cols)
cur.execute(f"SELECT {sel} FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') "
            f"AND TO_CHAR(DAYTIME,'HH24:MI')=:h", o=OID, d=D, h=HH)
row = cur.fetchone()
baseline = {cols[i]: (None if row[i] is None else float(row[i])) for i in range(len(cols))}
nonnull = {k: v for k, v in baseline.items() if v is not None}
print("=== FRMW Well 1 @", D, HH, " — NON-NULL numeric cols (baseline) ===")
for k, v in nonnull.items():
    print(f"  {k} = {v}")
print(f"\n({len(nonnull)} non-null of {len(cols)} numeric cols)")
with open(r"c:/Projects/ChoongYin_OS/tmp/n1_subdaily_baseline.json", "w") as f:
    json.dump({"oid": OID, "date": D, "hhmi": HH, "baseline": baseline}, f, indent=1)
print("baseline saved -> tmp/n1_subdaily_baseline.json")
cur.close(); c.close(); print("DONE")
