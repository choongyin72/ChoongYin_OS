"""RECON (read-only): which P1 GAS-comp analyses have populated MOL_PCT (the cell we want to edit),
and in what RECORD_STATUS. Prefer a Preliminary (P) gas analysis with non-null mol% as the edit
target (Approved 'A' is likely locked). SELECT only."""
import os
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()


def q(sql, *a):
    cur.execute(sql, a)
    return cur.fetchall()


print("=== P1 STRM_GAS_COMP analyses: mol%/wt% population by (code,date,status) ===")
for r in q("""SELECT OBJECT_CODE, TRUNC(DAYTIME) D, RECORD_STATUS, SAMPLING_METHOD,
                     COUNT(*) NCOMP,
                     COUNT(MOL_PCT) N_MOL, COUNT(WT_PCT) N_WT,
                     ROUND(SUM(MOL_PCT),4) SUM_MOL
              FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
              WHERE OBJECT_CODE LIKE 'P1%' AND ANALYSIS_TYPE='STRM_GAS_COMP'
              GROUP BY OBJECT_CODE, TRUNC(DAYTIME), RECORD_STATUS, SAMPLING_METHOD
              HAVING COUNT(MOL_PCT) > 0
              ORDER BY COUNT(MOL_PCT) DESC, OBJECT_CODE, D
              FETCH FIRST 30 ROWS ONLY"""):
    print("  ", r)

print("\n=== components of P1_S0163_M_GAS_COMP @ 2025-04-01 (P) ===")
for r in q("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT, RECORD_STATUS, OBJECT_ID
              FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
              WHERE OBJECT_CODE='P1_S0163_M_GAS_COMP' AND TRUNC(DAYTIME)=TO_DATE('2025-04-01','YYYY-MM-DD')
              ORDER BY COMPONENT_NO"""):
    print("  ", r)

print("\n=== components of P1 S038_AGA3_1985_AGA8_Y_1 @ 2011-11-01 (P) ===")
for r in q("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT, RECORD_STATUS, OBJECT_ID
              FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
              WHERE OBJECT_CODE='P1 S038_AGA3_1985_AGA8_Y_1' AND TRUNC(DAYTIME)=TO_DATE('2011-11-01','YYYY-MM-DD')
              ORDER BY COMPONENT_NO"""):
    print("  ", r)

cur.close()
conn.close()
print("\nDONE (read-only)")
