# DRY RUN on LOCAL sandbox with ROLLBACK (nothing persists). Validates parse + upsert mechanics.
import oracledb
from pathlib import Path
sql = Path("workstreams/ecsr-35236-phd-validations/backport-ec14151-4rules/create_ECSR-35236_4rules.sql").read_text(encoding="utf-8")
block = sql.rsplit("/",1)[0]  # strip trailing slash for oracledb
NAMES=('PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
       'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS')
try:
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn="localhost:1521/ORCL")
except Exception as e:
    print("LOCAL CONNECT FAILED:",str(e)[:150]); raise SystemExit
cur=c.cursor()
# pre-existence of the required tables/classes locally
for t in ("CTRL_CHECK_RULES","TV_CTRL_CHECK_RULES","TV_CTRL_CHECK_RULE_VARIABLE","TV_CTRL_CHECK_COMBINATION"):
    cur.execute("select count(*) from all_objects where owner='ECKERNEL_EC' and object_name=:n",{"n":t})
    print(f"  local has {t}: {cur.fetchone()[0]>0}")
inlist=",".join("'%s'"%n for n in NAMES)
cur.execute(f"select count(*) from ctrl_check_rules where check_name in ({inlist})")
print("rules present BEFORE:",cur.fetchone()[0])
try:
    cur.execute(block)
    cur.execute(f"select check_name from ctrl_check_rules where check_name in ({inlist}) order by check_name")
    got=[r[0] for r in cur.fetchall()]
    print("rules present AFTER block (uncommitted):",len(got),got)
    c.rollback()
    cur.execute(f"select count(*) from ctrl_check_rules where check_name in ({inlist})")
    print("rules present AFTER ROLLBACK:",cur.fetchone()[0],"(expect 0 if none pre-existed)")
    print("DRY RUN: block executed + rolled back OK")
except Exception as e:
    c.rollback()
    print("BLOCK ERROR (rolled back):", str(e)[:250])
c.close()
