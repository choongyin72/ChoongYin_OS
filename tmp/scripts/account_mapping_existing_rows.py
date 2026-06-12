"""READ-ONLY: full-row dump of the existing Account Mapping rows on the local
sandbox (OV_FIN_ACCOUNT_MAPPING) - the proven-valid reference combinations to
model the test insert after (clone-by-full-row rule)."""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
cur.execute("SELECT * FROM OV_FIN_ACCOUNT_MAPPING")
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
print(f"{len(rows)} rows, {len(cols)} columns\n")
for r in rows[:3]:
    print("=" * 60)
    for c, v in zip(cols, r):
        if v is not None:
            print(f"  {c:28s} = {v}")
cur.close()
conn.close()
