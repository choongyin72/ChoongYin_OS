"""ECSR-35333 read-only: EQPM_TYPE (+ product) per deferment equipment facility. Creds from env."""
import os, oracledb
c = oracledb.connect(user=os.environ['QDB_USER'], password=os.environ['QDB_PW'], dsn=os.environ['QDB_DSN'], tcp_connect_timeout=25)
cur = c.cursor()
cur.execute("""select DEF_FCTY_1_CODE,
                      EQPM_TYPE,
                      NAME,
                      ecdp_objects.getobjcode(ZWP_DEFER_PRODUCT) prod
               from ov_eqpm
               where eqpm_type='DEFERMENT'
                 and daytime <= DATE '2026-06-01'
                 and nvl(end_date, DATE '2026-07-01') > DATE '2026-06-01'
                 and DEF_FCTY_1_CODE in
                     ('PLU_LNG_TRAIN1','PLU_PNI','PLU_COND','PLU_DG','PLA_OFFSHORE','PLU_LNG_TRAIN2','SCA_OFFSHORE')
               order by DEF_FCTY_1_CODE""")
print("DEF_FCTY_1_CODE | EQPM_TYPE | EQPM_NAME | PRODUCT")
for r in cur.fetchall():
    print(" | ".join('' if v is None else str(v) for v in r))
c.close(); print("DONE")
