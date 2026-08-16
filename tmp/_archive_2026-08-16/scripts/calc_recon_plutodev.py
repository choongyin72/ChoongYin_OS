"""EC Calculation framework live recon on plutodev (read-only).
Inventories: CALC% tables, calculations, versions, variables, mappings,
allocation network job wiring, recent calc activity.
"""
import oracledb

conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud', 1521,
                         service_name='plutodev'),
    tcp_connect_timeout=25)
cur = conn.cursor()

def section(t):
    print('\n' + '=' * 70 + '\n' + t + '\n' + '=' * 70)

def run(sql, binds=None):
    cur.execute(sql, binds or {})
    return cur.fetchall()

section('1. CALC% TABLE INVENTORY (row counts)')
tabs = run("""SELECT table_name FROM all_tables
              WHERE owner='ECKERNEL_EC' AND table_name LIKE 'CALC%'
              ORDER BY table_name""")
for (t,) in tabs:
    try:
        n = run(f'SELECT COUNT(*) FROM {t}')[0][0]
        if n:
            print(f'  {t:<38} {n}')
    except Exception:
        pass

section('2. CALCULATIONS (CALCULATION joined to version names)')
try:
    rows = run("""
        SELECT c.object_id, c.calc_period, c.calc_type, c.calc_scope,
               (SELECT MAX(v.name) FROM calculation_version v
                 WHERE v.object_id = c.object_id) AS name
        FROM calculation c ORDER BY 5""")
    print(f'  total: {len(rows)}')
    for oid, per, typ, scope, name in rows:
        print(f'  {str(name):<46} period={str(per):<4} type={str(typ):<10} scope={str(scope)}')
except Exception as e:
    print('  ERROR:', e)

section('3. VARIABLES (DV_CALC_VARIABLE) by prefix')
try:
    rows = run("""
        SELECT CASE WHEN name LIKE 'ZWP%' THEN 'ZWP_* (Woodside)'
                    WHEN name LIKE 'XEM%' THEN 'XEM_* (emissions)'
                    ELSE 'other/product' END grp,
               COUNT(*)
        FROM dv_calc_variable GROUP BY CASE WHEN name LIKE 'ZWP%' THEN 'ZWP_* (Woodside)'
                    WHEN name LIKE 'XEM%' THEN 'XEM_* (emissions)'
                    ELSE 'other/product' END""")
    for g, n in rows:
        print(f'  {g:<22} {n}')
    tot = run('SELECT COUNT(*) FROM dv_calc_variable')[0][0]
    print(f'  TOTAL: {tot}')
except Exception as e:
    print('  ERROR:', e)

section('4. READ MAPPINGS — top 15 source classes')
try:
    for cls, n in run("""SELECT cls_name_mapping, COUNT(*) FROM dv_calc_var_read_mapping
                         GROUP BY cls_name_mapping ORDER BY 2 DESC FETCH FIRST 15 ROWS ONLY"""):
        print(f'  {cls:<40} {n}')
except Exception as e:
    print('  ERROR:', e)

section('5. WRITE MAPPINGS — top 15 target classes')
try:
    for cls, n in run("""SELECT cls_name_mapping, COUNT(*) FROM dv_calc_var_write_mapping
                         GROUP BY cls_name_mapping ORDER BY 2 DESC FETCH FIRST 15 ROWS ONLY"""):
        print(f'  {cls:<40} {n}')
except Exception as e:
    print('  ERROR:', e)

section('6. ALLOC NETWORK JOB CONNECTIONS')
try:
    rows = run("""
        SELECT n.object_code, j.object_code
        FROM tv_alloc_network_job_conn c
        JOIN (SELECT object_id, object_code FROM alloc_network) n ON n.object_id = c.alloc_network_id
        JOIN (SELECT object_id, object_code FROM calculation) j ON j.object_id = c.job_id
        ORDER BY 1, 2""")
    for net, job in rows:
        print(f'  {net:<24} -> {job}')
except Exception as e:
    print('  ERROR (trying simpler):', e)
    try:
        for net, job in run("""SELECT alloc_network_id, job_id FROM tv_alloc_network_job_conn"""):
            print(f'  {net} -> {job}')
    except Exception as e2:
        print('  ERROR:', e2)

section('7. RECENT CALC ACTIVITY (log/run tables)')
for t in ('CALC_JOB_LOG', 'CALC_LOG', 'CALC_RUN_LOG', 'CALC_JOB_EXECUTION'):
    try:
        n = run(f'SELECT COUNT(*) FROM {t}')[0][0]
        last = run(f'SELECT MAX(created_date) FROM {t}')[0][0]
        print(f'  {t:<22} rows={n:<8} last={last}')
    except Exception:
        pass
# generic: any CALC% table with recent created_date
try:
    for (t,) in tabs:
        cols = {r[0] for r in run("""SELECT column_name FROM all_tab_columns
                                     WHERE owner='ECKERNEL_EC' AND table_name=:t""", {'t': t})}
        if 'CREATED_DATE' in cols:
            r = run(f"SELECT MAX(created_date) FROM {t}")[0][0]
            if r and str(r) >= '2026-06-01':
                print(f'  active-in-June: {t:<34} last={r}')
except Exception as e:
    print('  scan error:', e)

cur.close()
conn.close()
print('\nDone (read-only).')
