import os
"""ECSR-35331 item 1 - confirm why rule 1040 didn't fire after user set Grs Mass = -8.5 on Train 1 LNG
Rundown. Read-only. Shows the current record's GRS_MASS_GAS_TONNES/KG + GRS_MASS_METHOD, and runs the
rule's exact WHERE condition to see if it WOULD match. SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:160]); return []


print("=== current Train 1 LNG Rundown records (negative or recent) ===")
rows = q("""SELECT STREAM_NAME, DAYTIME, GRS_MASS_GAS_TONNES, GRS_MASS_GAS_KG, GRS_MASS_METHOD
            FROM RV_STRM_DAY_STREAM_MEAS_GAS
            WHERE UPPER(STREAM_NAME) LIKE '%TRAIN 1 LNG RUNDOWN%'
              AND (GRS_MASS_GAS_TONNES < 0 OR GRS_MASS_GAS_TONNES IS NULL
                   OR DAYTIME >= TO_DATE('2026-05-10','YYYY-MM-DD'))
            ORDER BY DAYTIME DESC FETCH FIRST 12 ROWS ONLY""")
print("  STREAM_NAME | DAYTIME | GRS_MASS_GAS_TONNES | GRS_MASS_GAS_KG | GRS_MASS_METHOD")
for r in rows:
    print("  ", r)

print("\n=== run rule 1040's exact condition against LNG Rundown ===")
# rule: (GrsMassGasTonnes IS NULL OR GrsMassGasTonnes < 0) AND GrsMassMethod = 'MEASURED'
hit = q("""SELECT STREAM_NAME, DAYTIME, GRS_MASS_GAS_TONNES, GRS_MASS_METHOD
           FROM RV_STRM_DAY_STREAM_MEAS_GAS
           WHERE UPPER(STREAM_NAME) LIKE '%TRAIN 1 LNG RUNDOWN%'
             AND (GRS_MASS_GAS_TONNES IS NULL OR GRS_MASS_GAS_TONNES < 0)
             AND GRS_MASS_METHOD = 'MEASURED'""")
print(f"  rows matching rule 1040 (negative/null mass AND method=MEASURED): {len(hit)}")
for r in hit:
    print("  ", r)

print("\n=== same but IGNORING the method gate (negative/null regardless of method) ===")
hit2 = q("""SELECT STREAM_NAME, DAYTIME, GRS_MASS_GAS_TONNES, GRS_MASS_METHOD
            FROM RV_STRM_DAY_STREAM_MEAS_GAS
            WHERE UPPER(STREAM_NAME) LIKE '%TRAIN 1 LNG RUNDOWN%'
              AND (GRS_MASS_GAS_TONNES IS NULL OR GRS_MASS_GAS_TONNES < 0)""")
print(f"  rows with negative/null mass (any method): {len(hit2)}")
for r in hit2:
    print("  ", r)

con.close()
print("\nDONE (read-only).")
