"""Columns + data-bearing scope for the WR.0001 day-status tables (READ-ONLY DB)."""
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
        print(f"   {c:32} {dt}")

def count(tbl):
    try:
        cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{tbl}")
        print(f"\n{tbl} row count:", cur.fetchone()[0])
    except Exception as e:
        print(f"\n{tbl} count ERR:", str(e)[:120])

for t in ("PWEL_DAY_STATUS", "WELL_HOOKUP_DAY_STATUS"):
    cols(t); count(t)

# sample distinct (object, day) so we know a scope that populates the grid
for t, key in (("PWEL_DAY_STATUS", "PWEL"), ("WELL_HOOKUP_DAY_STATUS", "WELL_HOOKUP")):
    print(f"\n=== {t} sample distinct day + obj ===")
    try:
        cur.execute(f"""SELECT * FROM (
                          SELECT t.* FROM ECKERNEL_EC.{t} t ORDER BY 1
                        ) WHERE ROWNUM<=3""")
        names = [d[0] for d in cur.description]
        print("   cols:", names)
        for r in cur.fetchall():
            print("   row:", dict(zip(names, [str(v)[:25] for v in r])))
    except Exception as e:
        print("   ERR:", str(e)[:140])

conn.close()
print("\nDONE")
