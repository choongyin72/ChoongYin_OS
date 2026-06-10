"""ECPR-31011 — snapshot current access rows for the SCA screen (pre-change evidence).
Read-only. Writes access_backup_PWEL_DAY_STATUS_2.csv next to this script.
"""
import csv
import os
import oracledb

HERE = os.path.dirname(os.path.abspath(__file__))
NAME = ('/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/'
        'CLASS_NAME/PWEL_DAY_STATUS_2')

conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud', 1521,
                         service_name='plutodev'),
    tcp_connect_timeout=25)
cur = conn.cursor()
cur.execute("""
    SELECT a.t_basis_access_id, a.role_id, a.app_id, a.level_id, a.level_name,
           a.object_id, a.created_by, TO_CHAR(a.created_date,'YYYY-MM-DD HH24:MI:SS')
    FROM tv_t_basis_access a
    WHERE a.object_id = (SELECT object_id FROM t_basis_object WHERE object_name = :n)
    ORDER BY a.role_id""", {'n': NAME})
rows = cur.fetchall()
hdr = ['T_BASIS_ACCESS_ID', 'ROLE_ID', 'APP_ID', 'LEVEL_ID', 'LEVEL_NAME',
       'OBJECT_ID', 'CREATED_BY', 'CREATED_DATE']
out = os.path.join(HERE, 'access_backup_PWEL_DAY_STATUS_2.csv')
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['object_name', NAME])
    w.writerow(hdr)
    w.writerows(rows)
print(f'{len(rows)} rows backed up to {out}')
for r in rows:
    print(f'  {r[1]:<18} level={r[3]:<3} ({r[4]})')
cur.close()
conn.close()
