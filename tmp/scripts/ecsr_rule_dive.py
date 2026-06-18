import os
"""ECSR-35331 root-cause DB dive (read-only) on ECAASDEV. For the screen-bound check groups (gas/oil/elec/
water/tank + missing-data), list the linked rules (via CTRL_CHECK_COMBINATION) with full WHERE_FORMULA /
SELECT / TABLE / ZWP_SCREEN_VAL / SEVERITY / RECORD_STATUS, plus their variable->attribute mappings. Reveals
exactly which negative/null checks apply to which stream-status screen and what they test. SELECT only."""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD",""),
                       dsn="dev.db.non-prod.plp.wde.ecaas.cloud:1521/QDB", tcp_connect_timeout=20)
cur = con.cursor()


def q(sql, a=None):
    try:
        cur.execute(sql, a or []); return cur.fetchall()
    except Exception as e:
        print("  ERR:", str(e)[:140]); return []


def cols(t):
    return [c[0] for c in q("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
            AND table_name=:t ORDER BY column_id""", [t])]


print("=== CTRL_CHECK_COMBINATION cols ===")
cc = cols("CTRL_CHECK_COMBINATION"); print("  ", cc)
print("=== CTRL_CHECK_RULE_VARIABLE cols ===")
print("  ", cols("CTRL_CHECK_RULE_VARIABLE"))

# groups of interest (screen-bound daily stream-status + tank + missing-data)
GROUPS = ['D_GAS', 'V_PHD_STREAM_GAS', 'V_MD_STRM_DAY_STREAM_MEAS_GAS',
          'D_LIQUID', 'V_PHD_STREAM_LIQUID', 'V_PHD_STREAM_ELEC', 'V_MD_STRM_DAY_STREAM_MEAS_ELE',
          'TANK_INVENTORY', 'V_MD_TANK_DAY_INV_OIL']

print("\n=== group -> linked rules (CTRL_CHECK_COMBINATION) ===")
# discover the linking columns dynamically
grp_col = next((c for c in cc if 'GROUP' in c), None)
rule_col = next((c for c in cc if c in ('CHECK_ID', 'CHECK_NAME', 'CHECK_RULE', 'RULE_ID')), None)
print(f"  (group col={grp_col}, rule col={rule_col})")
linked = {}
for g in GROUPS:
    rows = q(f"SELECT {rule_col} FROM CTRL_CHECK_COMBINATION WHERE {grp_col}=:g", [g])
    linked[g] = [r[0] for r in rows]
    print(f"  {g}: {linked[g]}")

# dump rule detail for all linked rules
all_rules = sorted({r for v in linked.values() for r in v})
print(f"\n=== rule detail for {len(all_rules)} linked rules (from TV_CTRL_CHECK_RULES) ===")
if all_rules:
    binds = ",".join(f":{i}" for i in range(len(all_rules)))
    rd = q(f"""SELECT CHECK_ID, CHECK_NAME, TABLE_ID, SEVERITY_LEVEL, ZWP_SCREEN_VAL, RECORD_STATUS,
              WHERE_FORMULA FROM TV_CTRL_CHECK_RULES WHERE CHECK_ID IN ({binds})""", all_rules)
    for r in rd:
        cid, cn, tbl, sev, sv, rs, wf = r
        print(f"\n  [{cid}] {cn}  table={tbl}  sev={sev}  screenVal={sv}  status={rs}")
        print(f"     WHERE: {str(wf)[:260]}")
    # variable -> attribute mappings for the gas + missing-data rules
    print("\n=== rule variables (CHECK_ID, VAR, TYPE, VALUE) for gas/elec/md rules ===")
    for cid in (1039, 1040, 1041, 1042, 1043, 1044, 1058, 1057, 1073, 1074):
        vs = q("""SELECT VARIABLE_NAME, VARIABLE_TYPE, VARIABLE_VALUE FROM CTRL_CHECK_RULE_VARIABLE
                  WHERE CHECK_ID=:c ORDER BY VARIABLE_NAME""", [cid])
        if vs:
            print(f"  [{cid}] " + "; ".join(f"{v[0]}={v[2]}({v[1]})" for v in vs))

con.close()
print("\nDONE (read-only).")
