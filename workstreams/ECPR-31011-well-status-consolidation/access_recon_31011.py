"""ECPR-31011 — current screen-access state for the 3 daily_well_status URL objects.
Read-only against plutodev. v2: discovers actual column names first.
"""
import oracledb

BASE = '/com.ec.prod.wr.screens/daily_well_status/GROUPMODEL/WELL/TARGET/WELL/CLASS_NAME/'
SCREENS = ['PWEL_DAY_STATUS', 'PWEL_DAY_STATUS_2', 'PWEL_DAY_STATUS_3']

conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud', 1521,
                         service_name='plutodev'),
    tcp_connect_timeout=25)
cur = conn.cursor()

def columns(tab):
    cur.execute("""SELECT column_name FROM all_tab_columns
                   WHERE owner='ECKERNEL_EC' AND table_name=:t ORDER BY column_id""",
                {'t': tab})
    return [r[0] for r in cur.fetchall()]

for t in ('T_BASIS_OBJECT', 'T_BASIS_ACCESS', 'T_BASIS_ACCESS_LEVEL', 'T_BASIS_ROLE'):
    print(f'{t}: {columns(t)}')

# objects
print()
for s in SCREENS:
    name = BASE + s
    cur.execute("SELECT object_id FROM t_basis_object WHERE object_name = :n", {'n': name})
    row = cur.fetchone()
    print('=' * 70)
    print(s, '-> object_id =', row[0] if row else 'NOT FOUND')
    if not row:
        continue
    cur.execute("SELECT * FROM tv_t_basis_access WHERE object_id = :o", {'o': row[0]})
    desc = [d[0] for d in cur.description]
    rows = cur.fetchall()
    print('  TV_T_BASIS_ACCESS cols:', desc)
    print(f'  access rows: {len(rows)}')
    for r in rows:
        print('   ', dict(zip(desc, [str(v)[:40] for v in r])))

cur.close()
conn.close()
print('\nDone (read-only).')
