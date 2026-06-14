"""Find the well daily-status table + a data-bearing PU/date (READ-ONLY DB).
Answers N1 unknown #5 and locates a scope that will populate the WR.0001 grid."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

def q(sql, label, n=25):
    print(f"\n=== {label} ===")
    try:
        cur.execute(sql)
        rows = cur.fetchall()
        for r in rows[:n]:
            print("  ", r)
        if not rows:
            print("   (none)")
        return rows
    except Exception as e:
        print("   ERR:", str(e)[:140])
        return []

# 1) candidate well day-status tables/views
q("""SELECT table_name FROM all_tables
     WHERE owner='ECKERNEL_EC' AND (
       table_name LIKE '%WEL%DAY%STAT%' OR table_name LIKE '%WELL%STAT%'
       OR table_name LIKE 'PWEL%STAT%' OR table_name LIKE '%DAY_STATUS%')
     ORDER BY table_name""", "candidate day-status TABLES")

q("""SELECT view_name FROM all_views
     WHERE owner='ECKERNEL_EC' AND (
       view_name LIKE '%WEL%DAY%STAT%' OR view_name LIKE 'OV_%WELL%'
       OR view_name LIKE '%WELL%STATUS%')
     AND ROWNUM<=30 ORDER BY view_name""", "candidate day-status VIEWS")

# 2) well hookup objects (the nav G4 scope) — do any exist + under which PU?
q("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC'
     AND (table_name LIKE '%WELL_HOOKUP%' OR table_name LIKE '%WEL_HUP%'
          OR table_name LIKE 'OV_WELL%') ORDER BY table_name""", "well-hookup tables/views")

conn.close()
print("\nDONE")
