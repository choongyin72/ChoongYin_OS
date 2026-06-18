"""RECON (read-only): find the Well Gas Component Analysis (WR.0010.01) data model and compare it to the
stream comp model (DV_STRM_COMP_ANALYSIS). Look for a well-comp view/table, its ANALYSIS_TYPE values,
MOL_PCT/WT_PCT population, and a data-bearing P1 well target. SELECT only."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


print("=== views/tables matching WELL + COMP/ANALYSIS ===")
for r in q("""SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
              AND object_type IN ('TABLE','VIEW')
              AND (object_name LIKE '%WELL%COMP%' OR object_name LIKE 'DV_WELL%COMP%'
                   OR object_name LIKE '%WELL_GAS_COMP%' OR object_name LIKE '%WCOMP%')
              AND object_name NOT LIKE '%JN' ORDER BY 2,1"""):
    try:
        cur.execute(f"SELECT COUNT(*) FROM ECKERNEL_EC.{r[0]}"); n = cur.fetchone()[0]
    except Exception:
        n = "?"
    print(f"  {r[1][0]} {r[0]:38s} rows={n}")

# the most likely analogue view
for cand in ("DV_WELL_COMP_ANALYSIS", "DV_WEL_COMP_ANALYSIS", "DV_WELL_GAS_COMP_ANALYSIS"):
    cols = [c[0] for c in q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id", cand)]
    if cols:
        print(f"\n=== {cand} cols ===\n  {', '.join(cols[:30])}")
        print("  distinct ANALYSIS_TYPE:", q(f"SELECT DISTINCT ANALYSIS_TYPE FROM ECKERNEL_EC.{cand}") if 'ANALYSIS_TYPE' in cols else 'n/a')
        print("\n  P1 WELL_GAS_COMP targets (code,date,status,ncomp,nmol,nwt):")
        try:
            for r in q(f"""SELECT OBJECT_CODE, TRUNC(DAYTIME) D, MAX(RECORD_STATUS), MAX(SAMPLING_METHOD),
                                  COUNT(*), COUNT(MOL_PCT), COUNT(WT_PCT)
                           FROM ECKERNEL_EC.{cand} WHERE OBJECT_CODE LIKE 'P1%'
                           AND ANALYSIS_TYPE LIKE '%GAS%'
                           GROUP BY OBJECT_CODE, TRUNC(DAYTIME) HAVING COUNT(*)>=5
                           ORDER BY COUNT(MOL_PCT) DESC FETCH FIRST 12 ROWS ONLY"""):
                print("   ", r)
        except Exception as e:
            print("   target query err:", str(e)[:60])
        break
cur.close()
print("\nDONE")
