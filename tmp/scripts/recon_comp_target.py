"""RECON (read-only sandbox DB): lock a clean Stream Gas Component Analysis target.
For P1 streams, list each analysis (OBJECT_CODE, NAME, DAYTIME, ANALYSIS_TYPE, SAMPLING_METHOD,
RECORD_STATUS, component count) so we can pick one with a full component set + a clear status, and
know exactly what to set G:5 (Stream) / G:6 (Analysis Status) / G:7 (Sampling Method) to before GO.
Also dumps the distinct RECORD_STATUS values + the components of the best candidate. SELECT only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a)
    return cur.fetchall()


print("=== DV_STRM_COMP_ANALYSIS columns ===")
cols = [c[0] for c in q("""SELECT column_name FROM all_tab_columns
        WHERE owner='ECKERNEL_EC' AND table_name='DV_STRM_COMP_ANALYSIS' ORDER BY column_id""")]
print("  ", ", ".join(cols))

print("\n=== distinct RECORD_STATUS in DV_STRM_COMP_ANALYSIS ===")
for r in q("SELECT DISTINCT RECORD_STATUS FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS ORDER BY 1"):
    print("  ", r)

print("\n=== distinct SAMPLING_METHOD ===")
for r in q("SELECT DISTINCT SAMPLING_METHOD FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS ORDER BY 1"):
    print("  ", r)

print("\n=== P1 gas-comp analyses (grouped) — most components first ===")
rows = q("""SELECT OBJECT_CODE, TRUNC(DAYTIME) D,
                   MAX(ANALYSIS_TYPE) ATYPE, MAX(SAMPLING_METHOD) SMETHOD,
                   MAX(RECORD_STATUS) RSTAT, COUNT(*) NCOMP
            FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
            WHERE OBJECT_CODE LIKE 'P1%'
            GROUP BY OBJECT_CODE, TRUNC(DAYTIME)
            HAVING COUNT(*) >= 5
            ORDER BY COUNT(*) DESC, OBJECT_CODE, D
            FETCH FIRST 25 ROWS ONLY""")
for r in rows:
    print("  ", r)

if rows:
    code, d = rows[0][0], rows[0][1]
    has_ccode = "COMPONENT_CODE" in cols
    sel = "COMPONENT_NO, " + ("COMPONENT_CODE, " if has_ccode else "") + "MOL_PCT, WT_PCT, RECORD_STATUS"
    print(f"\n=== BEST CANDIDATE {code} @ {d} components ({sel}) ===")
    for r in q(f"""SELECT {sel}
                  FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                  WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=:d
                  ORDER BY COMPONENT_NO""", code, d):
        print("  ", r)
    print("\n  stream NAME (OV_STREAM):",
          q("SELECT NAME FROM ECKERNEL_EC.OV_STREAM WHERE CODE=:c FETCH FIRST 1 ROWS ONLY", code))

cur.close()
conn.close()
print("\nDONE (read-only)")
