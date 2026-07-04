"""READ-ONLY: resolve the target data table + check-group for the PHD rules (plutodev)."""
import oracledb
con = oracledb.connect(user="ECKERNEL_EC", password="energy",
                       dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev")
cur = con.cursor()
for name in ["PHD_TANK_DIP_GRS_MASS_VAL1", "PHD_STRM_ANALYSIS_DENSITY_VAL1", "PHD_PWEL_STATUS_NODATA_BHTEMP"]:
    cur.execute("""SELECT check_id, table_id, select_clause, sql, check_message, severity_level
                   FROM tv_ctrl_check_rules WHERE check_name=:n""", [name])
    r = cur.fetchone()
    cid, tid, sel, sql, msg, sev = r
    print(f"[{name}] check_id={cid} table_id={tid} severity={sev}")
    print(f"   SELECT_CLAUSE = {sel}")
    print(f"   SQL = {(sql or '')[:200]}")
    print(f"   MESSAGE = {msg}")
    # resolve table_id -> table/class name if there is a class/table registry
    if tid is not None:
        for tbl, col in [("CTRL_TABLE_CLASS", "TABLE_CLASS_NAME"), ("CLASS_CNFG", "CLASS_NAME")]:
            try:
                cur.execute(f"SELECT {col} FROM {tbl} WHERE table_id=:t", [tid])
                got = cur.fetchall()
                if got:
                    print(f"   table_id {tid} -> {tbl}.{col} = {[g[0] for g in got]}")
            except Exception:
                pass
    # check-group membership via ctrl_check_combination (inspect its columns first)
    print()
# what columns does ctrl_check_combination have + a sample for one check_id
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CTRL_CHECK_COMBINATION' ORDER BY column_id")
print("CTRL_CHECK_COMBINATION cols:", [r[0] for r in cur])
cur.execute("SELECT * FROM ctrl_check_combination WHERE check_id=1147")
cols = [d[0] for d in cur.description]
rows = cur.fetchall()
print("combination rows for check_id 1147:", len(rows))
for row in rows[:5]:
    print("  ", dict(zip(cols, row)))
con.close()
