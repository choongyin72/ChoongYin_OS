"""ECSR-35333 read-only: resolve DEF_FCTY_1 code -> name for the June verify table. Creds from env."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
codes = ['PLU_LNG_TRAIN1','PLU_PNI','PLU_COND','PLU_DG','PLA_OFFSHORE','PLU_LNG_TRAIN2','SCA_OFFSHORE']
# distinct DEF_FCTY_1_ID per code from the DEFERMENT eqpm
cur.execute("""select distinct DEF_FCTY_1_CODE, DEF_FCTY_1_ID from ov_eqpm
               where eqpm_type='DEFERMENT' and DEF_FCTY_1_CODE in
               ('PLU_LNG_TRAIN1','PLU_PNI','PLU_COND','PLU_DG','PLA_OFFSHORE','PLU_LNG_TRAIN2','SCA_OFFSHORE')""")
rows = cur.fetchall()
print("code | id | name(getobjname) | name(fcty_class_1)")
for code, oid in rows:
    n1=n2=None
    try:
        cur.execute("select ecdp_objects.getobjname(:1) from dual",[oid]); n1=cur.fetchone()[0]
    except Exception as e: n1='ERR:'+str(e)[:40]
    try:
        cur.execute("select name from ov_fcty_class_1 where object_id=:1 and rownum=1",[oid]); r=cur.fetchone(); n2=r[0] if r else None
    except Exception as e: n2='ERR:'+str(e)[:40]
    print(f"{code} | {oid} | {n1} | {n2}")
c.close(); print("DONE")
