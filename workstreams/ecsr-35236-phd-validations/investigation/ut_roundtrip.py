"""
ECSR-35236 Stage-1 UT: apply -> rollback ROUND-TRIP proof on plutodev.
Snapshot S0 (original) -> run apply SQL -> verify S1 (all 8 SCOPED) -> run rollback SQL
-> verify S2 -> assert S2 == S0. Ends in the original/rolled-back state (clean).
plutodev is the sanctioned write-with-rollback env. Idempotent; safe to re-run.
Connection: db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev  ECKERNEL_EC/energy
"""
import oracledb, sys, os

DSN = "db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev"
USER, PWD = "ECKERNEL_EC", "energy"
SQLDIR = os.path.join(os.path.dirname(__file__), "..", "sql")
APPLY = os.path.join(SQLDIR, "V1.1.8.0030.0001__ECSR-35236__PHD_check_rule_method_scope.sql")
ROLLBACK = os.path.join(SQLDIR, "ROLLBACK__ECSR-35236__PHD_check_rule_method_scope.sql")

RULES = {
    "PHD_TANK_DIP_GRS_MASS_VAL1": ("(${GrsMass} IS NULL OR ${GrsMass} < 0)",
        "(${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED}"),
    "PHD_TANK_DIP_STD_DENSITY_VAL1": ("(${StdDensity} IS NULL OR ${StdDensity} < 0)",
        "(${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensMethod} = ${ConstMEASURED}"),
    "PHD_STRM_ANALYSIS_DENSITY_VAL1": ("(${Density} IS NULL OR ${Density} < 0)",
        "(${Density} IS NULL OR ${Density} < 0) and ${DensityMethod} = ${ConstCOMP}"),
    "PHD_STRM_ANALYSIS_GCV_VAL1": ("(${Gcv} IS NULL OR ${Gcv} < 0)",
        "(${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP}"),
    "PHD_PWEL_STATUS_NODATA_BHTEMP": ("(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0)",
        "(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_WHTEMP": ("(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0)",
        "(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_BHPRESS": ("(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0)",
        "(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_WHPRESS": ("(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0)",
        "(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0) and ${OnStrmHrs} > 0"),
}
NEW_VARS = {"GrsMassMethod", "StdDensMethod", "DensityMethod", "GcvMethod",
            "ConstMEASURED", "ConstCOMP", "OnStrmHrs"}


def snapshot(cur):
    """Return {rule: (state, sorted_method_vars)} where state in ORIGINAL/SCOPED/OTHER."""
    snap = {}
    for name, (orig, scoped) in RULES.items():
        cur.execute("SELECT check_id, where_formula FROM tv_ctrl_check_rules WHERE check_name=:n", [name])
        row = cur.fetchone()
        if not row:
            snap[name] = ("MISSING", []); continue
        cid, wf = row[0], (row[1] or "").strip()
        state = "ORIGINAL" if wf == orig else ("SCOPED" if wf == scoped else "OTHER")
        cur.execute("SELECT variable_name FROM tv_ctrl_check_rule_variable WHERE check_id=:c", [cid])
        mv = sorted(v[0] for v in cur if v[0] in NEW_VARS)
        snap[name] = (state, mv)
    return snap


def run_sql_file(con, path):
    with open(path, encoding="utf-8") as f:
        block = f.read()
    # strip a trailing standalone '/' terminator (SQL*Plus syntax, not valid via the driver)
    lines = [ln for ln in block.splitlines() if ln.strip() != "/"]
    con.cursor().execute("\n".join(lines))
    con.commit()


def show(tag, snap):
    print(f"\n--- {tag} ---")
    for name, (state, mv) in snap.items():
        print(f"  {state:9} | method-vars={mv if mv else 'none'} | {name}")


con = oracledb.connect(user=USER, password=PWD, dsn=DSN)
cur = con.cursor()
print(f"Connected: {DSN}")

s0 = snapshot(cur); show("S0 (before apply)", s0)
print("\n>>> running APPLY ..."); run_sql_file(con, APPLY)
s1 = snapshot(cur); show("S1 (after apply)", s1)
print("\n>>> running ROLLBACK ..."); run_sql_file(con, ROLLBACK)
s2 = snapshot(cur); show("S2 (after rollback)", s2)

print("\n" + "=" * 64)
apply_ok = all(st == "SCOPED" and set(mv) for st, mv in s1.values())
rt_ok = (s0 == s2)
orig0 = all(st == "ORIGINAL" and not mv for st, mv in s0.values())
print(f"S0 all ORIGINAL + no method-vars : {orig0}")
print(f"S1 all SCOPED + method-vars added: {apply_ok}")
print(f"ROUND-TRIP  S2 == S0            : {rt_ok}")
print("VERDICT:", "PASS - apply scopes all 8, rollback restores original exactly"
      if (orig0 and apply_ok and rt_ok) else "FAIL - investigate")
con.close()
sys.exit(0 if (orig0 and apply_ok and rt_ok) else 1)
