"""N2: test per-row physical invariants checkable on existing PWEL_DAY_ALLOC data alone (no co-present
stream totals needed). Candidates: NET<=GROSS gas; energy ~= vol*GCV; mass>0 where vol>0. Read-only."""
import os
import oracledb

conn = oracledb.connect(
    user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
    password=os.environ.get("EC_DB_PASS", "energy"),
    dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"),
    tcp_connect_timeout=15,
)
cur = conn.cursor()
DAY = "2021-10-01"

def run(title, sql):
    print(f"\n=== {title} ===")
    try:
        cur.execute(sql, {"d": DAY})
        cols = [c[0] for c in cur.description]
        print(" | ".join(cols))
        for row in cur.fetchall():
            print("  " + " | ".join("" if v is None else str(v) for v in row))
    except Exception as e:
        print("  ERR:", str(e)[:200])

# 0. Confirm the exact ALLOC_* + NET/GCV/ENERGY columns
run("PWEL_DAY_ALLOC ALLOC_* numeric columns",
    "SELECT column_name FROM all_tab_columns WHERE table_name='PWEL_DAY_ALLOC' "
    "AND column_name LIKE 'ALLOC\\_%' ESCAPE '\\' AND data_type='NUMBER' ORDER BY column_id")

# 1. NET <= GROSS gas: rows where ALLOC_NET_GAS_VOL > ALLOC_GAS_VOL (should be 0)
run("Violations NET_GAS_VOL > GAS_VOL (expect 0)",
    "SELECT COUNT(*) violations, "
    "SUM(CASE WHEN ALLOC_NET_GAS_VOL IS NOT NULL AND ALLOC_GAS_VOL IS NOT NULL THEN 1 ELSE 0 END) comparable_rows "
    "FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') "
    "AND ALLOC_NET_GAS_VOL > ALLOC_GAS_VOL")

# 1b. show the gross/net gas values to eyeball
run("Sample GAS_VOL vs NET_GAS_VOL (first rows)",
    "SELECT OBJECT_ID, ROUND(ALLOC_GAS_VOL,3) GROSS, ROUND(ALLOC_NET_GAS_VOL,3) NET, "
    "ROUND(ALLOC_GAS_MASS,3) GAS_MASS, ROUND(ALLOC_GAS_ENERGY,3) ENERGY, ROUND(ALLOC_GAS_GCV,5) GCV "
    "FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') "
    "AND ALLOC_GAS_VOL IS NOT NULL ORDER BY ALLOC_GAS_VOL DESC FETCH FIRST 8 ROWS ONLY")

# 2. energy ~= vol * GCV : relative error where all three present and vol>0
run("energy vs vol*GCV rel-error (where GCV present, vol>0)",
    "SELECT COUNT(*) rows_checked, "
    "ROUND(MAX(ABS(ALLOC_GAS_ENERGY - ALLOC_GAS_VOL*ALLOC_GAS_GCV) "
    "  / NULLIF(ABS(ALLOC_GAS_ENERGY),0)),5) max_rel_err "
    "FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') "
    "AND ALLOC_GAS_ENERGY IS NOT NULL AND ALLOC_GAS_GCV IS NOT NULL AND ALLOC_GAS_VOL>0")

# 3. mass present where vol>0 (gas): orphan vol-without-mass (informational)
run("Gas vol>0 but mass NULL/0 (informational)",
    "SELECT COUNT(*) vol_pos, "
    "SUM(CASE WHEN NVL(ALLOC_GAS_MASS,0)=0 THEN 1 ELSE 0 END) mass_missing "
    "FROM PWEL_DAY_ALLOC WHERE TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND ALLOC_GAS_VOL>0")

cur.close(); conn.close()
print("\nDONE")
