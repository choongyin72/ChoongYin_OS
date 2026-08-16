"""Last feasibility check for a READ-ONLY sum-to-total on 2021-10-01 (the 22-well day). Look across the
WHOLE *_DAY_ALLOC family + measured STRM_DAY_STREAM for a co-present TOTAL that the 22 well allocations
should sum to. If a conserving (members -> total) pair exists on one date, the oracle is buildable
read-only (no live run). Else: fall back to a daily N1 clone. Read-only."""
import os, oracledb
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)
cur = c.cursor()
DAY = "2021-10-01"


def q(sql, binds=None):
    cur.execute(sql, binds or {}); return cur.fetchall()


# all *_DAY_ALLOC tables + their row count on 2021-10-01
print("=== *_DAY_ALLOC family row counts on", DAY, "===")
cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE '%DAY_ALLOC' "
            "AND table_name NOT LIKE '%JN' ORDER BY table_name")
tabs = [r[0] for r in cur.fetchall()]
for t in tabs:
    try:
        n = q(f"SELECT COUNT(*) FROM {t} WHERE TRUNC(DAYTIME)=TO_DATE('{DAY}','YYYY-MM-DD')")[0][0]
        if n:
            print(f"  {t}: {n}")
    except Exception:
        pass

# sum of the 22 wells' gas/oil alloc on the day
print("\n=== PWEL_DAY_ALLOC member sums on", DAY, "===")
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_ALLOC' "
            r"AND column_name LIKE 'ALLOC\_%' ESCAPE '\' AND data_type='NUMBER' ORDER BY column_id")
acols = [r[0] for r in cur.fetchall()]
nonnull = []
for col in acols:
    s = q(f"SELECT ROUND(SUM({col}),3), COUNT({col}) FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE('{DAY}','YYYY-MM-DD')")[0]
    if s[1]:
        nonnull.append((col, s[0], s[1])); print(f"  SUM {col} = {s[0]} (over {s[1]} non-null wells)")
if not nonnull:
    print("  (no non-null ALLOC_* — only one col populated previously)")

# measured stream gas on the day (a candidate 'total')
print("\n=== measured STRM_DAY_STREAM on", DAY, "(candidate total source) ===")
try:
    rows = q("SELECT COUNT(*), ROUND(SUM(GRS_VOL),3) FROM STRM_DAY_STREAM WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", {"d": DAY})
    print("  STRM_DAY_STREAM rows / SUM(GRS_VOL):", rows[0])
except Exception as e:
    print("  ERR", str(e)[:120])

cur.close(); c.close(); print("\nDONE")
