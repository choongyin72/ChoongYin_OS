"""
ECSR-35236 READ-ONLY verification: does the live state of the 8 PHD rules match the
ROLLBACK 'original' formulas (and are the 7 method/const vars net-new = absent)?
Run against plutodev (rolled-back/original per the register). Proves the rollback
endpoint = the pristine value-only checks with NO leftover ECSR-35236 variables.
Connection: db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev  ECKERNEL_EC/energy
"""
import oracledb

DSN = "db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev"
USER, PWD = "ECKERNEL_EC", "energy"

# rule -> (rollback ORIGINAL formula, apply SCOPED formula)
RULES = {
    "PHD_TANK_DIP_GRS_MASS_VAL1": (
        "(${GrsMass} IS NULL OR ${GrsMass} < 0)",
        "(${GrsMass} IS NULL OR ${GrsMass} < 0) and ${GrsMassMethod} = ${ConstMEASURED}"),
    "PHD_TANK_DIP_STD_DENSITY_VAL1": (
        "(${StdDensity} IS NULL OR ${StdDensity} < 0)",
        "(${StdDensity} IS NULL OR ${StdDensity} < 0) and ${StdDensMethod} = ${ConstMEASURED}"),
    "PHD_STRM_ANALYSIS_DENSITY_VAL1": (
        "(${Density} IS NULL OR ${Density} < 0)",
        "(${Density} IS NULL OR ${Density} < 0) and ${DensityMethod} = ${ConstCOMP}"),
    "PHD_STRM_ANALYSIS_GCV_VAL1": (
        "(${Gcv} IS NULL OR ${Gcv} < 0)",
        "(${Gcv} IS NULL OR ${Gcv} < 0) and ${GcvMethod} = ${ConstCOMP}"),
    "PHD_PWEL_STATUS_NODATA_BHTEMP": (
        "(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0)",
        "(${AvgBHTemp} IS NULL OR ${AvgBHTemp} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_WHTEMP": (
        "(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0)",
        "(${AvgWHTemp} IS NULL OR ${AvgWHTemp} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_BHPRESS": (
        "(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0)",
        "(${AvgBHPress} IS NULL OR ${AvgBHPress} < 0) and ${OnStrmHrs} > 0"),
    "PHD_PWEL_STATUS_NODATA_WHPRESS": (
        "(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0)",
        "(${AvgWHPress} IS NULL OR ${AvgWHPress} < 0) and ${OnStrmHrs} > 0"),
}
NEW_VARS = {"GrsMassMethod", "StdDensMethod", "DensityMethod", "GcvMethod",
            "ConstMEASURED", "ConstCOMP", "OnStrmHrs"}

c = oracledb.connect(user=USER, password=PWD, dsn=DSN)
cur = c.cursor()
print(f"Connected to {DSN}\n")
for name, (orig, scoped) in RULES.items():
    cur.execute("SELECT check_id, where_formula, rev_text FROM tv_ctrl_check_rules WHERE check_name=:n", [name])
    row = cur.fetchone()
    if not row:
        print(f"[{name}]  *** NOT FOUND ***"); continue
    cid, wf, rt = row
    wf = (wf or "").strip()
    state = "ORIGINAL (rolled-back)" if wf == orig else ("SCOPED (applied)" if wf == scoped else "OTHER/UNKNOWN")
    print(f"[{name}]  check_id={cid}  rev_text={rt}")
    print(f"   formula = {wf}")
    print(f"   -> {state}")
    cur.execute("""SELECT variable_name, variable_type, variable_value, rev_text
                   FROM tv_ctrl_check_rule_variable WHERE check_id=:c ORDER BY variable_name""", [cid])
    vars_ = cur.fetchall()
    leftover = [v[0] for v in vars_ if v[0] in NEW_VARS]
    print(f"   variables ({len(vars_)}): " + ", ".join(f"{v[0]}[{v[1]}={v[2]};rev={v[3]}]" for v in vars_))
    print(f"   ECSR-35236 method/const vars present: {leftover if leftover else 'NONE (clean)'}")
    print()
c.close()
