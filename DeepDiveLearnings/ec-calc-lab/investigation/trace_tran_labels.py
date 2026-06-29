"""Business names (LABEL) for the key Transport I/O classes."""
import os, oracledb
def say(m): print(m, flush=True)
def rd(v):
    try: return v.read() if hasattr(v,'read') else v
    except: return v
classes=['SERVICE_DAY_TRANSACTION','SERVICE_DAY_TRANSACTION_LOCATION','DELSTRM_DAY_TRANSACTION',
'NOMPNT_DAY_NOM_ALLOC','DELSTRM_DAY_CAPACITY','TRNP_NP_DAY_NOM_PATH','DELPNT_DAY_INVENTORY_TRANSACTION',
'STOR_MTH_FCST_BAL','FCST_STOR_LIFT_NOM_ALLOC','STORAGE_LIFT_NOM_ALLOC','LIFT_ACC_DAY_FORECAST','STOR_DAY_FORECAST',
'FCST_CNTR_DAY_STATUS','FCST_DP_DAY_STATUS','FCST_NOMPNT_DAY_STATUS','CONTRACT_PARTIES',
'FCST_DP_DAY_ALLOC','FCST_NOMPNT_DAY_ALLOC','FCST_CNTR_DAY_ALLOC',
'STOR_DAY_LIFTING_ALLOC','STOR_DAY_ANALYSIS_ALLOC']
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
for cl in classes:
    cur.execute("select property_value from class_property_cnfg where class_name=:c and property_code='LABEL' and rownum=1",{'c':cl})
    r=cur.fetchone()
    say("   %-34s %s" % (cl, rd(r[0]) if r else '(no label)'))
c.close()
