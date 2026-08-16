"""Diagnose the sub-daily TC02 fail: UI cell showed 1 but ON_STREAM_HRS@00:00 stayed None. Find where
(if anywhere) the value committed — scan ALL numeric measured cols for FRMW Well 1 @2024-10-01 for any
non-null (= Save committed to some column/row). Distinguishes 'Save didn't commit' from 'C3 != ON_STREAM_HRS'.
Also clean any stray non-null residue back to NULL (zero-residue discipline)."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
OID = "AEBC774296C611E6E053020011ACFDF3"; D = "2024-10-01"

# all numeric measured cols
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' "
            "AND data_type='NUMBER' AND column_name<>'OBJECT_ID' ORDER BY column_id")
cols = [r[0] for r in cur.fetchall()]
print(f"{len(cols)} numeric cols")

# for each hour row, find non-null numeric cols
print("\n=== non-null numeric cells for FRMW Well 1 @", D, "(any committed value) ===")
sel = ", ".join(cols)
cur.execute(f"SELECT TO_CHAR(DAYTIME,'HH24:MI') hhmi, {sel} FROM PWEL_SUB_DAY_STATUS "
            f"WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY DAYTIME", o=OID, d=D)
rows = cur.fetchall()
colnames = [d[0] for d in cur.description]
found = []
for r in rows:
    hhmi = r[0]
    for i, v in enumerate(r[1:], start=1):
        if v is not None:
            found.append((hhmi, colnames[i], v))
if found:
    for f in found:
        print("  ", f)
else:
    print("  (NO non-null numeric cells anywhere — Save did NOT commit)")

# clean any stray residue back to null
if found:
    print("\n=== cleaning stray residue -> NULL ===")
    for hhmi, col, v in found:
        cur.execute(f"UPDATE PWEL_SUB_DAY_STATUS SET {col}=NULL WHERE OBJECT_ID=:o "
                    f"AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h",
                    o=OID, d=D, h=hhmi)
        print(f"  cleared {col}@{hhmi}: {cur.rowcount} row")
    c.commit()
cur.close(); c.close(); print("\nDONE")
