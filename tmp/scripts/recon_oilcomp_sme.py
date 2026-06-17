"""RECON (read-only): Stream Oil Component Analysis (PO.0019) SME facts. Confirm the oil-comp data model
vs gas-comp: which column is populated (WT_PCT vs MOL_PCT), the component set (C8+?), density, statuses,
and data-bearing P1 targets. Oil comp shares the view DV_STRM_COMP_ANALYSIS with ANALYSIS_TYPE=STRM_OIL_COMP."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a)
    return cur.fetchall()


print("=== STRM_OIL_COMP analyses (P1): population of MOL_PCT vs WT_PCT, status, sampling ===")
for r in q("""SELECT OBJECT_CODE, TRUNC(DAYTIME) D, RECORD_STATUS, SAMPLING_METHOD,
                     COUNT(*) NCOMP, COUNT(MOL_PCT) N_MOL, COUNT(WT_PCT) N_WT,
                     ROUND(SUM(MOL_PCT),3) SUM_MOL, ROUND(SUM(WT_PCT),3) SUM_WT
              FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
              WHERE ANALYSIS_TYPE='STRM_OIL_COMP'
              GROUP BY OBJECT_CODE, TRUNC(DAYTIME), RECORD_STATUS, SAMPLING_METHOD
              ORDER BY COUNT(WT_PCT) DESC, OBJECT_CODE FETCH FIRST 20 ROWS ONLY"""):
    print("  ", r)

print("\n=== component set of the best WT_PCT-populated oil analysis ===")
best = q("""SELECT OBJECT_CODE, TRUNC(DAYTIME) FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
            WHERE ANALYSIS_TYPE='STRM_OIL_COMP' AND WT_PCT IS NOT NULL
            GROUP BY OBJECT_CODE, TRUNC(DAYTIME) ORDER BY COUNT(WT_PCT) DESC FETCH FIRST 1 ROWS ONLY""")
if best:
    code, d = best[0]
    print(f"  target: {code} @ {d}")
    for r in q("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT, MOL_WT, DENSITY, RECORD_STATUS
                  FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                  WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=:d ORDER BY COMPONENT_NO""", code, d):
        print("   ", r)

print("\n=== distinct STRM_OIL_COMP statuses / sampling methods ===")
print("  status:", q("SELECT DISTINCT RECORD_STATUS FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS WHERE ANALYSIS_TYPE='STRM_OIL_COMP'"))
print("  sampling:", q("SELECT DISTINCT SAMPLING_METHOD FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS WHERE ANALYSIS_TYPE='STRM_OIL_COMP'"))
cur.close()
conn.close()
print("\nDONE (read-only)")
