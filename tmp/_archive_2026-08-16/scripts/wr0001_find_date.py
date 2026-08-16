"""Find data-bearing dates + trace a well-hookup to its PU/Area/Facility (READ-ONLY DB)."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

def q(sql, label, n=15, **kw):
    print(f"\n=== {label} ===")
    try:
        cur.execute(sql, **kw)
        names = [d[0] for d in cur.description]
        rows = cur.fetchall()
        print("  cols:", names)
        for r in rows[:n]:
            print("  ", tuple(str(v)[:30] for v in r))
        if not rows: print("   (none)")
        return rows
    except Exception as e:
        print("   ERR:", str(e)[:160]); return []

# top dates by row count (where measured values actually exist, ON_STREAM_HRS not null)
q("""SELECT TO_CHAR(DAYTIME,'YYYY-MM-DD') d, COUNT(*) n,
            COUNT(ON_STREAM_HRS) filled
     FROM ECKERNEL_EC.PWEL_DAY_STATUS
     GROUP BY TO_CHAR(DAYTIME,'YYYY-MM-DD')
     ORDER BY filled DESC, n DESC FETCH FIRST 15 ROWS ONLY""",
  "PWEL_DAY_STATUS top dates (by filled measured values)")

# a specific well with filled data + its object name
q("""SELECT s.OBJECT_ID, TO_CHAR(s.DAYTIME,'YYYY-MM-DD') d, s.ON_STREAM_HRS, s.AVG_WH_PRESS
     FROM ECKERNEL_EC.PWEL_DAY_STATUS s
     WHERE s.ON_STREAM_HRS IS NOT NULL
     ORDER BY s.DAYTIME DESC FETCH FIRST 10 ROWS ONLY""",
  "PWEL rows WITH measured data (recent)")

# resolve well object name + its production unit / facility class via the object/version tables
# discover the well object table columns first
q("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
     AND table_name IN ('WELL','WELL_VERSION','OV_WELL','PWEL','PRODUCTION_WELL') ORDER BY table_name""",
  "well object tables present")

conn.close(); print("\nDONE")
