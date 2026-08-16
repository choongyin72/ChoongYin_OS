"""N3: recon the STATUS_PROCESS config — which processes are defined, their from->to status + target,
so the N3 build can pick a P->V process to run + verify. Read-only."""
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

run("STATUS_PROCESS columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='STATUS_PROCESS' ORDER BY column_id")

run("STAT_PROCESS_STATUS columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='STAT_PROCESS_STATUS' ORDER BY column_id")

# Defined status processes (names) - look for P->V daily ones, esp Woodside SP_IN_*_P_V
run("Defined status processes (first 40 by name)",
    "SELECT NAME FROM STATUS_PROCESS ORDER BY NAME FETCH FIRST 40 ROWS ONLY")

run("Status processes mentioning P_V / VERIF / DAILY (name filter)",
    "SELECT NAME FROM STATUS_PROCESS WHERE UPPER(NAME) LIKE '%P_V%' OR UPPER(NAME) LIKE '%VERIF%' "
    "OR UPPER(NAME) LIKE '%DAILY%' OR UPPER(NAME) LIKE '%P-V%' ORDER BY NAME FETCH FIRST 40 ROWS ONLY")

cur.close(); conn.close()
print("\nDONE")
