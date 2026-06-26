"""
READ-ONLY recon: for the 8 PHD check rules, find (a) the target table-class the check runs
against, (b) the check group(s) they belong to (CTRL_CHECK_COMBINATION), so Stage-2 can
either run the real Validation/check-group OR evaluate the predicate against the data table.
plutodev, read-only SELECTs.
"""
import oracledb

con = oracledb.connect(user="ECKERNEL_EC", password="energy",
                       dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
cur = con.cursor()
RULES = ["PHD_TANK_DIP_GRS_MASS_VAL1", "PHD_STRM_ANALYSIS_DENSITY_VAL1", "PHD_PWEL_STATUS_NODATA_BHTEMP"]

# columns available on the check-rules table (to see what target/class info it carries)
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='TV_CTRL_CHECK_RULES' ORDER BY column_id")
print("TV_CTRL_CHECK_RULES columns:", [r[0] for r in cur])
print()

for name in RULES:
    cur.execute("SELECT * FROM tv_ctrl_check_rules WHERE check_name=:n", [name])
    cols = [d[0] for d in cur.description]
    row = cur.fetchone()
    d = dict(zip(cols, row)) if row else {}
    print(f"[{name}]")
    for k in ("CHECK_ID", "CHECK_NAME", "TABLE_CLASS_NAME", "CLASS_NAME", "CHECK_TABLE",
              "TARGET_CLASS", "SEVERITY", "MESSAGE", "WHERE_FORMULA"):
        if k in d:
            print(f"    {k} = {d[k]}")
    # which check groups reference this rule
    try:
        cur.execute("""SELECT cc.check_group_name FROM ctrl_check_combination cc
                       WHERE cc.check_name=:n""", [name])
        grps = [r[0] for r in cur]
        print(f"    check group(s): {grps if grps else 'none found via ctrl_check_combination.check_name'}")
    except Exception as e:
        print(f"    (group lookup err: {str(e)[:60]})")
    print()
con.close()
