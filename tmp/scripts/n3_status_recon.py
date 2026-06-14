"""N3 brief recon: the reality of RECORD_STATUS on day-status tables — values present, and whether
there's data in a non-approved state to lift (P->V->A). Read-only. Picks the WR.0001/PO.0002 tables
I already automate so the N3 build can reuse the N1 nav cascade."""
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
        for row in cur.fetchall():
            print("  " + " | ".join("" if v is None else str(v) for v in row))
    except Exception as e:
        print("  ERR:", str(e)[:200])

# RECORD_STATUS distribution on PWEL_DAY_STATUS (N1 well status — has a nav cascade I own)
run("PWEL_DAY_STATUS record_status distribution",
    "SELECT RECORD_STATUS, COUNT(*) n, TO_CHAR(MIN(TRUNC(DAYTIME)),'YYYY-MM-DD') min_day, "
    "TO_CHAR(MAX(TRUNC(DAYTIME)),'YYYY-MM-DD') max_day FROM PWEL_DAY_STATUS GROUP BY RECORD_STATUS ORDER BY n DESC")

# Same for the gas stream status table (PO.0002)
run("STRM_DAY_STREAM record_status distribution",
    "SELECT RECORD_STATUS, COUNT(*) n FROM STRM_DAY_STREAM GROUP BY RECORD_STATUS ORDER BY n DESC")

# Is there a status-process / status-history / approval table?
run("Candidate status-process / approval tables",
    "SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND "
    "(table_name LIKE '%STATUS_PROC%' OR table_name LIKE '%STAT_PROC%' OR table_name LIKE '%APPROVAL%' "
    "OR table_name LIKE '%STATUS_LOG%' OR table_name LIKE '%STATUS_HIST%') ORDER BY table_name")

# What distinct RECORD_STATUS codes exist system-wide on day tables (the P/V/A ladder)?
run("Distinct RECORD_STATUS codes on PWEL_DAY_STATUS",
    "SELECT DISTINCT RECORD_STATUS FROM PWEL_DAY_STATUS")

# WR.0001 working scope day (2003-01-01) status — the data I can drive a lift on
run("PWEL_DAY_STATUS @ 2003-01-01 by status (the N1 scope day)",
    "SELECT RECORD_STATUS, COUNT(*) n FROM PWEL_DAY_STATUS "
    "WHERE TRUNC(DAYTIME)=TO_DATE('2003-01-01','YYYY-MM-DD') GROUP BY RECORD_STATUS")

cur.close(); conn.close()
print("\nDONE")
