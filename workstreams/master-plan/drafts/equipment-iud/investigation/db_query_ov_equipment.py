"""
DB verification for Equipment IUD. Read-only.
Usage: py db_query_ov_equipment.py [CODE]
Finds the equipment object view, reports row(s) for CODE, and confirms existing untouched.
"""
import oracledb, sys

CODE = sys.argv[1] if len(sys.argv) > 1 else 'AUTOTEST_EQP_001'
dsn = oracledb.makedsn('localhost', 1521, service_name='ORCL')
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=dsn, tcp_connect_timeout=15)
cur = conn.cursor()

# find the view name
view = None
for cand in ['ov_eqpm', 'ov_equipment', 'ov_equip']:
    try:
        cur.execute(f'SELECT COUNT(*) FROM {cand}')
        view = cand; break
    except Exception:
        pass
if not view:
    cur.execute("SELECT view_name FROM all_views WHERE view_name LIKE 'OV_EQUIP%' ORDER BY view_name")
    rows = cur.fetchall()
    print('Candidate views:', [r[0] for r in rows])
    view = rows[0][0] if rows else None

print(f'Object view: {view}')
if not view:
    raise SystemExit('No equipment object view found')

cur.execute(f'SELECT COUNT(*) FROM {view}')
print(f'{view} total rows: {cur.fetchone()[0]}')

print(f'\n=== Rows for CODE = {CODE} ===')
cur.execute(f"SELECT code, name, object_start_date, object_end_date, rev_no FROM {view} WHERE code = :c", c=CODE)
hits = cur.fetchall()
if hits:
    for r in hits:
        s = r[2].strftime('%Y-%m-%d') if r[2] else 'None'
        e = r[3].strftime('%Y-%m-%d') if r[3] else 'None'
        print(f'  code={r[0]}  name="{r[1]}"  start={s}  end={e}  rev={r[4]}')
else:
    print(f'  (0 rows — {CODE} not present)')

print('\n=== Existing AUTOTEST_EQP_* still present ===')
cur.execute(f"SELECT code, object_end_date FROM {view} WHERE code LIKE 'AUTOTEST_EQP_%' ORDER BY code")
for r in cur.fetchall():
    e = r[1].strftime('%Y-%m-%d') if r[1] else 'None'
    print(f'  {r[0]}  end={e}')

print('\n=== Existing OFF_ equipment (must be untouched) ===')
cur.execute(f"SELECT code, name, object_end_date FROM {view} WHERE code LIKE 'OFF\\_%' ESCAPE '\\' ORDER BY code")
for r in cur.fetchall():
    e = r[2].strftime('%Y-%m-%d') if r[2] else 'None'
    print(f'  {r[0]:<20} end={e}  "{r[1]}"')

cur.close(); conn.close()
