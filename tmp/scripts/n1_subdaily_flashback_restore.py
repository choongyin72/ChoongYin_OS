"""URGENT restore: my diagnostic NULLed columns on FRMW Well 1 / 2024-10-01 that were likely
pre-existing real data. Use Oracle Flashback (AS OF TIMESTAMP, ~20 min ago = before today's test +
diagnostic writes) to read the ORIGINAL values of every numeric column for these 24 interval rows,
and restore any column whose current value differs from the original. Scoped strictly to
OID=FRMW Well 1, 2024-10-01. Prints a full diff before/after."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
OID = "AEBC774296C611E6E053020011ACFDF3"; D = "2024-10-01"
MINS = 25  # flashback window: before today's live test + diagnostic

cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_SUB_DAY_STATUS' "
            "AND data_type='NUMBER' AND column_name<>'OBJECT_ID' ORDER BY column_id")
cols = [r[0] for r in cur.fetchall()]
sel = ", ".join(cols)

# ORIGINAL (flashback) keyed by DAYTIME
try:
    cur.execute(
        f"SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') k, {sel} "
        f"FROM PWEL_SUB_DAY_STATUS AS OF TIMESTAMP (SYSTIMESTAMP - INTERVAL '{MINS}' MINUTE) "
        f"WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", o=OID, d=D)
    orig = {r[0]: r[1:] for r in cur.fetchall()}
    print(f"flashback rows (AS OF -{MINS}min): {len(orig)}")
except Exception as e:
    print("FLASHBACK ERR:", str(e)[:200]); cur.close(); c.close(); raise SystemExit(1)

# CURRENT
cur.execute(f"SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') k, {sel} FROM PWEL_SUB_DAY_STATUS "
            f"WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", o=OID, d=D)
curr = {r[0]: r[1:] for r in cur.fetchall()}

# diff + restore
restored = 0
print("\n=== diffs (current -> original) ===")
for k, ovals in orig.items():
    cvals = curr.get(k)
    if cvals is None:
        print(f"  {k}: row missing in current?!"); continue
    for i, col in enumerate(cols):
        ov, cv = ovals[i], cvals[i]
        if (ov is None) != (cv is None) or (ov is not None and cv is not None and float(ov) != float(cv)):
            print(f"  {k} {col}: current={cv} -> original={ov}")
            cur.execute(f"UPDATE PWEL_SUB_DAY_STATUS SET {col}=:v WHERE OBJECT_ID=:o "
                        f"AND DAYTIME=TO_DATE(:k,'YYYY-MM-DD HH24:MI:SS')", v=ov, o=OID, k=k)
            restored += cur.rowcount
c.commit()
print(f"\nrestored {restored} column-cell(s)")

# verify: current == original now
cur.execute(f"SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD HH24:MI:SS') k, {sel} FROM PWEL_SUB_DAY_STATUS "
            f"WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", o=OID, d=D)
curr2 = {r[0]: r[1:] for r in cur.fetchall()}
mismatch = 0
for k, ovals in orig.items():
    for i in range(len(cols)):
        ov = ovals[i]; cv = curr2[k][i]
        if (ov is None) != (cv is None) or (ov is not None and cv is not None and float(ov) != float(cv)):
            mismatch += 1
print("post-restore mismatches vs original:", mismatch, "(expect 0)")
cur.close(); c.close(); print("DONE")
