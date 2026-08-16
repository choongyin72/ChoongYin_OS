"""N2 DB recon: confirm PWEL_DAY_ALLOC ALLOC_* numeric columns, the richest data day,
and the no-negatives invariant. Read-only. Local sandbox DB."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

# 1. ALLOC_* numeric columns of PWEL_DAY_ALLOC
cur.execute(
    "SELECT column_name, data_type FROM all_tab_columns "
    "WHERE table_name = 'PWEL_DAY_ALLOC' AND column_name LIKE 'ALLOC\\_%' ESCAPE '\\' "
    "AND data_type IN ('NUMBER','FLOAT','BINARY_DOUBLE','BINARY_FLOAT') ORDER BY column_id"
)
alloc_cols = cur.fetchall()
print("ALLOC_* numeric columns (%d):" % len(alloc_cols))
for c, t in alloc_cols:
    print("  ", c, t)

# 2. Days with the most rows
cur.execute(
    "SELECT TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') d, COUNT(*) n "
    "FROM PWEL_DAY_ALLOC GROUP BY TRUNC(DAYTIME) ORDER BY n DESC FETCH FIRST 8 ROWS ONLY"
)
print("\nTop days by row count:")
for d, n in cur.fetchall():
    print("  ", d, n)

# 3. no-negatives on 2021-10-01 across all ALLOC_* numeric cols
day = "2021-10-01"
preds = " OR ".join(f"{c} < 0" for c, _ in alloc_cols)
cur.execute(
    f"SELECT COUNT(*) FROM PWEL_DAY_ALLOC "
    f"WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND ({preds})", d=day,
)
neg = cur.fetchone()[0]
cur.execute(
    "SELECT COUNT(*) FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", d=day,
)
total = cur.fetchone()[0]
print(f"\n{day}: total rows={total}, rows with ANY negative ALLOC_*={neg}")

cur.close()
conn.close()
print("DONE")
