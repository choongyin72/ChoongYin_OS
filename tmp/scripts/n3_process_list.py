"""N3: list the actual defined status processes (text, from->to level, facility, interval, reverse),
decode RS levels, and show any run history in STAT_PROCESS_STATUS. Read-only."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()

def run(title, sql):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        print(" | ".join(cols))
        n = 0
        for row in cur.fetchall():
            print("  " + " | ".join("" if v is None else str(v) for v in row)); n += 1
            if n >= 40:
                print("  ...(truncated)"); break
    except Exception as e:
        print("  ERR:", str(e)[:200])

# Decode RS levels (numeric -> P/V/A) if a code table exists
run("RECORD_STATUS level codes (CTRL/code table guess)",
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE '%RECORD_STATUS%' ORDER BY table_name")

# The processes: text, from->to level, facility name, interval, reverse
run("Defined status processes",
    "SELECT sp.PROCESS_ID, sp.PROCESS_TEXT, sp.FROM_RS_LEVEL, sp.TO_RS_LEVEL, "
    "sp.PROCESS_INTERVAL, sp.REVERSE_FLAG, sp.PROD_FCTY_ID, sp.PARENT_PROCESS_ID "
    "FROM STATUS_PROCESS sp ORDER BY sp.PROCESS_INTERVAL, sp.PROCESS_TEXT FETCH FIRST 40 ROWS ONLY")

run("Count of status processes by interval + from->to level",
    "SELECT PROCESS_INTERVAL, FROM_RS_LEVEL, TO_RS_LEVEL, REVERSE_FLAG, COUNT(*) n "
    "FROM STATUS_PROCESS GROUP BY PROCESS_INTERVAL, FROM_RS_LEVEL, TO_RS_LEVEL, REVERSE_FLAG "
    "ORDER BY n DESC")

# Any run history (proves runnable + ROWS_UPDATED oracle)
run("STAT_PROCESS_STATUS run history (recent)",
    "SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD') day, "
    "TO_CHAR(RUN_DAYTIME,'YYYY-MM-DD HH24:MI') run_at, ROWS_UPDATED "
    "FROM STAT_PROCESS_STATUS WHERE RUN_DAYTIME IS NOT NULL ORDER BY RUN_DAYTIME DESC FETCH FIRST 15 ROWS ONLY")

# Map a facility id to name for the AS2 scope I drive in N1
run("PROD_FCTY_ID -> facility name sample (join FACILITY_VERSION if present)",
    "SELECT sp.PROD_FCTY_ID, fv.NAME FROM STATUS_PROCESS sp "
    "LEFT JOIN FACILITY_VERSION fv ON fv.OBJECT_ID=sp.PROD_FCTY_ID "
    "WHERE sp.PROD_FCTY_ID IS NOT NULL FETCH FIRST 15 ROWS ONLY")

cur.close(); conn.close()
print("\nDONE")
