"""Trace a data-bearing well to its PU/Area/Facility-Class/Well-Hookup names (READ-ONLY DB).
Gives exact navigator scope values to drive WR.0001 so the grid populates."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

def cols(tbl):
    print(f"\n=== {tbl} columns ===")
    cur.execute("""SELECT column_name, data_type FROM all_tab_columns
                   WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id""", t=tbl)
    for c, dt in cur.fetchall():
        print(f"   {c:34} {dt}")

cols("WELL")
cols("WELL_VERSION")

# one well that has FILLED status on 2003-01-01
print("\n=== a filled well on 2003-01-01 ===")
cur.execute("""SELECT OBJECT_ID FROM ECKERNEL_EC.PWEL_DAY_STATUS
               WHERE TRUNC(DAYTIME)=DATE '2003-01-01' AND ON_STREAM_HRS IS NOT NULL
               FETCH FIRST 1 ROWS ONLY""")
row = cur.fetchone()
wid = row[0] if row else None
print("  well OBJECT_ID:", wid)

if wid:
    print("\n=== WELL row ===")
    cur.execute("SELECT * FROM ECKERNEL_EC.WELL WHERE OBJECT_ID=:i", i=wid)
    names = [d[0] for d in cur.description]
    for r in cur.fetchall():
        print("  ", dict(zip(names, [str(v)[:40] for v in r])))
    print("\n=== WELL_VERSION row(s) ===")
    cur.execute("SELECT * FROM ECKERNEL_EC.WELL_VERSION WHERE OBJECT_ID=:i", i=wid)
    names = [d[0] for d in cur.description]
    for r in cur.fetchall():
        d = dict(zip(names, [str(v)[:40] for v in r]))
        # print only non-null fields for readability
        print("  ", {k: v for k, v in d.items() if v not in ("None", "")})

conn.close(); print("\nDONE")
