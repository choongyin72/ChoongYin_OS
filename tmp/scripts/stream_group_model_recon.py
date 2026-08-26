"""Read-only DB recon for Stream - by Group Model (CO.0027, class STREAM, view OV_STREAM).
Confirms: OV_STREAM columns, AUTOTEST_STREAM_GROUP_MODEL code freedom, sample real nav values."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()


def q(sql, *a):
    cur.execute(sql, a)
    return cur.fetchall()


print("=== OV_STREAM columns ===")
for r in q("SELECT column_name, data_type FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='OV_STREAM' ORDER BY column_id"):
    print(" ", r)

print("\n=== CODE freedom check: AUTOTEST_STREAM_GROUP_MODEL ===")
print(q("SELECT COUNT(*) FROM ov_stream WHERE code = 'AUTOTEST_STREAM_GROUP_MODEL'"))

print("\n=== sample real nav values (from task's known facts, confirm still selectable) ===")
for r in q("SELECT DISTINCT op_productionunit_code FROM ov_stream WHERE op_productionunit_code IS NOT NULL"):
    print(" PU used by existing streams:", r)
for r in q("SELECT DISTINCT op_area_code FROM ov_stream WHERE op_area_code IS NOT NULL"):
    print(" Area used by existing streams:", r)
for r in q("SELECT DISTINCT op_fcty_1_code FROM ov_stream WHERE op_fcty_1_code IS NOT NULL"):
    print(" Facility Class 1 used by existing streams:", r)

cur.close()
