import sys; sys.path.insert(0, r'workstreams/master-plan/ec-automation/libraries')
import DbVerify as db
import oracledb
c=oracledb.connect(user='ECKERNEL_EC',password='energy',dsn='localhost:1521/ORCL');cur=c.cursor()
cur.execute("select object_id from ov_chem_product where code='AUTOTEST_CP_001'")
row=cur.fetchone()
if not row:
    print("already absent"); print("residual:", db.count_like('ov_chem_product','AUTOTEST')); c.close(); sys.exit()
oid=row[0]; print("object_id:", oid)
cur.execute("delete from CHEM_USAGE_REPORT_CONF where OBJECT_ID=:1",[oid]); print("child rows deleted:", cur.rowcount)
cur.execute("update OV_CHEM_PRODUCT set OBJECT_END_DATE=OBJECT_START_DATE where CODE='AUTOTEST_CP_001'"); print("end=start rowcount:", cur.rowcount)
c.commit(); c.close()
print("residual now:", db.count_like('ov_chem_product','AUTOTEST'))
