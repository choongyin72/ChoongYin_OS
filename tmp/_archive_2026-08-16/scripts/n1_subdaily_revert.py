"""Revert the manual save test: restore FRMW Well 1 @ 2024-10-01 00:00 to the exact baseline
(tmp/n1_subdaily_baseline.json). Diff current vs baseline across all numeric cols, UPDATE each
changed col back to its original value, commit, verify 0 mismatches. Leaves the row as found."""
import os, json
import oracledb
B = json.load(open(r"c:/Projects/ChoongYin_OS/tmp/n1_subdaily_baseline.json"))
OID, D, HH, BASE = B["oid"], B["date"], B["hhmi"], B["baseline"]
cols = list(BASE.keys()); sel = ", ".join(cols)
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()


def read():
    cur.execute(f"SELECT {sel} FROM PWEL_SUB_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h", o=OID, d=D, h=HH)
    r = cur.fetchone()
    return {cols[i]: (None if r[i] is None else float(r[i])) for i in range(len(cols))}


curr = read()
changed = [(k, curr[k], BASE[k]) for k in cols if (curr[k] is None) != (BASE[k] is None) or (curr[k] is not None and BASE[k] is not None and curr[k] != BASE[k])]
print("=== changes to revert (current -> original) ===")
for k, cv, ov in changed:
    print(f"  {k}: {cv} -> {ov}")
    cur.execute(f"UPDATE PWEL_SUB_DAY_STATUS SET {k}=:v WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND TO_CHAR(DAYTIME,'HH24:MI')=:h", v=ov, o=OID, d=D, h=HH)
c.commit()
after = read()
mism = [k for k in cols if (after[k] is None) != (BASE[k] is None) or (after[k] is not None and BASE[k] is not None and after[k] != BASE[k])]
print(f"\nreverted {len(changed)} col(s); post-revert mismatches vs baseline: {len(mism)} (expect 0)")
print("AVG_WH_PRESS now:", after["AVG_WH_PRESS"], "(expect 210.0)")
cur.close(); c.close(); print("DONE")
