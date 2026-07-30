# READ-ONLY trace on COPS SANDBOX (ec14151). SELECT only - no DML, no commit.
import oracledb
DSN="db.ec14151.woodside-pluto.tieto-og.cloud:1521/ec14151"
NAMES=['PHD_STREAM_GAS_MEAS_VAL_STD_DENSITY','PHD_STREAM_GAS_MEAS_VAL_GCV',
       'MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_GRS_MASS','MISSING_DATA_TANK_DAY_DIP_STATUS_VAL_STD_DENS']
try:
    c=oracledb.connect(user="ECKERNEL_EC",password="energy",dsn=DSN)
except Exception as e:
    print("CONNECT FAILED:",str(e)[:220]); raise SystemExit
cur=c.cursor()
cur.execute("""select column_name from all_tab_columns where owner='ECKERNEL_EC'
   and table_name='CTRL_CHECK_RULES' and column_name in
   ('CHECK_ID','CHECK_NAME','CREATED_BY','CREATED_DATE','LAST_UPDATED_BY','LAST_UPDATED_DATE','REV_NO','REV_TEXT')""")
cols=[r[0] for r in cur.fetchall()]
print("audit cols present:",cols)
sel=", ".join(c if 'DATE' not in c else f"TO_CHAR({c},'YYYY-MM-DD HH24:MI') {c}" for c in cols)
q=f"""select {sel} from ctrl_check_rules
      where check_name in ({','.join(':n%d'%i for i in range(len(NAMES)))})
         or check_id in (1147,1148,1149,1150) order by check_id"""
cur.execute(q, {f"n{i}":v for i,v in enumerate(NAMES)})
rows=cur.fetchall()
print(f"\n=== {len(rows)} row(s) ===")
print(" | ".join(cols))
for r in rows: print(" | ".join(str(x) for x in r))
c.close()
