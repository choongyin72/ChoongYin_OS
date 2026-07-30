# FULL local dry-run w/ ROLLBACK: synthesize the 2 Woodside groups, run create block, verify, rollback.
import oracledb
from pathlib import Path
sql=Path("workstreams/ecsr-35236-phd-validations/backport-ec14151-4rules/create_ECSR-35236_4rules.sql").read_text(encoding="utf-8")
block=sql.rsplit("/",1)[0]
NAMES=('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
       'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS')
inlist=",".join("'%s'"%n for n in NAMES)
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL"); cur=c.cursor()
try:
    # 1) synthesize the 2 groups the combination FK needs (rolled back later)
    for g,d in [("V_PHD_STREAM_GAS","Daily Stream Gas Status - PHD Validations"),
                ("V_MD_TANK_DAY_INV_OIL","Daily Tank Status - Missing Data Validation")]:
        cur.execute("insert into tv_ctrl_check_group (table_class_name, check_group, description, rev_text) "
                    "values ('CTRL_CHECK_GROUP', :g, :d, 'ECSR-35236')", {"g":g,"d":d})
    # 2) run the create block
    cur.execute(block)
    # 3) verify (uncommitted)
    cur.execute(f"select count(*) from ctrl_check_rules where check_name in ({inlist})"); r=cur.fetchone()[0]
    cur.execute(f"select count(*) from tv_ctrl_check_rule_variable where check_id in (select check_id from ctrl_check_rules where check_name in ({inlist}))"); v=cur.fetchone()[0]
    cur.execute(f"select count(*) from tv_ctrl_check_combination where check_id in (select check_id from ctrl_check_rules where check_name in ({inlist}))"); k=cur.fetchone()[0]
    print(f"AFTER create (uncommitted): rules={r}/4  variables={v}/12  combinations={k}/4")
    # 4) idempotency: run again, counts must not grow
    cur.execute(block)
    cur.execute(f"select count(*) from ctrl_check_rules where check_name in ({inlist})"); r2=cur.fetchone()[0]
    cur.execute(f"select count(*) from tv_ctrl_check_rule_variable where check_id in (select check_id from ctrl_check_rules where check_name in ({inlist}))"); v2=cur.fetchone()[0]
    print(f"AFTER 2nd run (idempotency): rules={r2}/4  variables={v2}/12  (must equal first run)")
    ok = (r==4 and v==12 and k==4 and r2==4 and v2==12)
    print("RESULT:", "PASS - full create valid + idempotent" if ok else "CHECK COUNTS")
finally:
    c.rollback()
    cur.execute(f"select count(*) from ctrl_check_rules where check_name in ({inlist})")
    print("AFTER ROLLBACK: rules =", cur.fetchone()[0], "(expect 0 - nothing persisted)")
    c.close()
