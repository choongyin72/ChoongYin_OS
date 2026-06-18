import os
"""ECSR-35331 item 1 - WHY does rule 1040 (negative gross mass) not fire? Read-only on ECAASDEV.
Checks (a) rule/group/combination activation status, (b) the actual Train 1 LNG Rundown data's
GRS_MASS_GAS_TONNES + GRS_MASS_METHOD (is method = MEASURED?). SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:150]); return []


print("=== (a) rule 1040 activation (TV_CTRL_CHECK_RULES) ===")
for r in q("""SELECT CHECK_ID, CHECK_NAME, ZWP_SCREEN_VAL, SEVERITY_LEVEL, RECORD_STATUS, APPROVAL_STATE
              FROM TV_CTRL_CHECK_RULES WHERE CHECK_ID=1040"""):
    print("  rule:", r)
print("  combination 1040/V_PHD_STREAM_GAS:")
for r in q("""SELECT CHECK_ID, CHECK_GROUP, RECORD_STATUS, APPROVAL_STATE FROM CTRL_CHECK_COMBINATION
              WHERE CHECK_ID=1040"""):
    print("   ", r)
print("  group V_PHD_STREAM_GAS:")
for r in q("""SELECT CHECK_GROUP, RECORD_STATUS, APPROVAL_STATE, EC_USER_OBJECT FROM CTRL_CHECK_GROUP
              WHERE CHECK_GROUP='V_PHD_STREAM_GAS'"""):
    print("   ", r[:3], "\n     EC_USER_OBJECT:", r[3])

print("\n=== (b) RV_STRM_DAY_STREAM_MEAS_GAS columns containing MASS or METHOD ===")
mcols = [c[0] for c in q("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
         AND table_name='RV_STRM_DAY_STREAM_MEAS_GAS'
         AND (column_name LIKE '%MASS%' OR column_name LIKE '%METHOD%' OR column_name LIKE '%STREAM%NAME%'
              OR column_name LIKE '%DAYTIME%' OR column_name LIKE '%DAY%')""")]
print("  ", mcols)

# find the stream-name + daytime + gross-mass + method columns
def pick(*subs):
    for c in mcols:
        if all(s in c for s in subs):
            return c
    return None
nm = next((c for c in mcols if 'STREAM' in c and 'NAME' in c), None) or 'STREAM_NAME'
dt = next((c for c in mcols if 'DAYTIME' in c or c == 'DAY' or 'DAY' in c), None)
gm = next((c for c in mcols if 'GRS_MASS_GAS_TONNES' in c), None) or next((c for c in mcols if 'MASS' in c and 'TONNE' in c), None)
mth = next((c for c in mcols if c == 'GRS_MASS_METHOD'), None) or next((c for c in mcols if 'MASS' in c and 'METHOD' in c), None)
print(f"\n  using: name={nm} daytime={dt} grsMass={gm} method={mth}")

print("\n=== (b) Train 1 LNG Rundown measured-gas records (recent) ===")
if nm and gm:
    sel = ", ".join([c for c in (nm, dt, gm, mth) if c])
    rows = q(f"""SELECT {sel} FROM RV_STRM_DAY_STREAM_MEAS_GAS
                 WHERE UPPER({nm}) LIKE '%LNG RUNDOWN%'
                 ORDER BY {dt or nm} DESC FETCH FIRST 15 ROWS ONLY""")
    for r in rows:
        print("   ", r)
    print("\n  distinct method values for LNG Rundown:")
    if mth:
        for r in q(f"""SELECT {mth}, COUNT(*) FROM RV_STRM_DAY_STREAM_MEAS_GAS
                       WHERE UPPER({nm}) LIKE '%LNG RUNDOWN%' GROUP BY {mth}"""):
            print("   ", r)

con.close()
print("\nDONE (read-only).")
