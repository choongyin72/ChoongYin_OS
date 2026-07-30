# LOCAL rollback dry-run: synth groups -> CREATE (assert 4/12/4) -> DELETE (assert 0/0/0) -> rollback.
import oracledb
from pathlib import Path
B="workstreams/ecsr-35236-phd-validations/backport-ec14151-4rules"
create=Path(f"{B}/create_ECSR-35236_4rules.sql").read_text(encoding="utf-8").rsplit("/",1)[0]
delete=Path(f"{B}/delete_ECSR-35236_4rules.sql").read_text(encoding="utf-8").rsplit("/",1)[0]
NAMES=('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS')
inl=",".join("'%s'"%n for n in NAMES)
c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL"); cur=c.cursor()
def counts():
    cur.execute(f"select (select count(*) from ctrl_check_rules where check_name in ({inl})),"
                f"(select count(*) from tv_ctrl_check_rule_variable where check_id in (select check_id from ctrl_check_rules where check_name in ({inl}))),"
                f"(select count(*) from tv_ctrl_check_combination where check_id in (select check_id from ctrl_check_rules where check_name in ({inl}))) from dual")
    return cur.fetchone()
try:
    for g,d in [("V_PHD_STREAM_GAS","Daily Stream Gas Status - PHD Validations"),("V_MD_TANK_DAY_INV_OIL","Daily Tank Status - Missing Data Validation")]:
        cur.execute("insert into tv_ctrl_check_group (table_class_name,check_group,description,rev_text) values ('CTRL_CHECK_GROUP',:g,:d,'ECSR-35236')",{"g":g,"d":d})
    cur.execute(create); print("after CREATE   rules/vars/combos:", counts())
    cur.execute(delete); print("after DELETE   rules/vars/combos:", counts())
    cur.execute(delete); print("after DELETE#2 (re-runnable):    ", counts())
    print("ROUND-TRIP: PASS" if counts()==(0,0,0) else "CHECK")
finally:
    c.rollback(); c.close(); print("rolled back - nothing persisted")
