"""ECPR-31011 recon v2 — data-class level (read-only).

v1 showed PWEL_DAY_STATUS_2 is a DATA CLASS over the single PWEL_DAY_STATUS table
(DATA_CLASS_NAME discriminator), not a separate table. So:
  1. Diff DV_PWEL_DAY_STATUS vs DV_PWEL_DAY_STATUS_2 view columns (the real class diff).
  2. Where do Cato's 5 ZWP_* attrs live (DV views map class attrs -> VALUE_n/TEXT_n)?
  3. Row activity per DATA_CLASS_NAME (is class 2 still landing data?).
  4. Wells per data class, with names.
  5. Dependencies of the Woodside report views *_ZWP_R_PWEL_DAY_STATUS_2.
"""
import oracledb

conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
    dsn=oracledb.makedsn('db.plutodev.woodside-pluto.tieto-og.cloud', 1521,
                         service_name='plutodev'),
    tcp_connect_timeout=25)
cur = conn.cursor()

def section(title):
    print('\n' + '=' * 70)
    print(title)
    print('=' * 70)

def run(sql, binds=None):
    cur.execute(sql, binds or {})
    return cur.fetchall()

# 1. DV view column diff
section('1. DV VIEW COLUMN DIFF (class-level attribute sets)')
cols = {}
for v in ('DV_PWEL_DAY_STATUS', 'DV_PWEL_DAY_STATUS_2'):
    cols[v] = {r[0] for r in run("""
        SELECT column_name FROM all_tab_columns
        WHERE table_name = :t AND owner = 'ECKERNEL_EC'""", {'t': v})}
    print(f'  {v}: {len(cols[v])} columns')
only2 = sorted(cols['DV_PWEL_DAY_STATUS_2'] - cols['DV_PWEL_DAY_STATUS'])
only1 = sorted(cols['DV_PWEL_DAY_STATUS'] - cols['DV_PWEL_DAY_STATUS_2'])
print(f'\n  ONLY in DV_PWEL_DAY_STATUS_2 ({len(only2)}):')
for c in only2:
    print('    ', c)
print(f'\n  ONLY in DV_PWEL_DAY_STATUS ({len(only1)}):')
for c in only1:
    print('    ', c)

# 2. where do the ZWP_* attrs live?
section('2. ZWP_* ATTRIBUTE LOCATIONS (any view/table with these columns)')
for attr in ('ZWP_ALLOC_GAS_ENERGY', 'ZWP_MEAS_EV_RATIO', 'ZWP_MEAS_GAS_ENERGY',
             'ZWP_MEAS_MV_RATIO', 'ZWP_THEOR_GAS_ENERGY', 'ZWP_THEOR_GAS_VOL'):
    rows = run("""
        SELECT table_name FROM all_tab_columns
        WHERE column_name = :c AND owner = 'ECKERNEL_EC'
          AND table_name LIKE '%PWEL%' ORDER BY table_name""", {'c': attr})
    where = ', '.join(r[0] for r in rows) if rows else '-- nowhere in *PWEL* objects'
    print(f'  {attr:<24} {where}')

# 3. activity per data class
section('3. ROW ACTIVITY PER DATA_CLASS_NAME (PWEL_DAY_STATUS base table)')
for cls, n, wells, dmin, dmax, recent in run("""
    SELECT data_class_name, COUNT(*), COUNT(DISTINCT object_id),
           MIN(daytime), MAX(daytime),
           SUM(CASE WHEN daytime >= TRUNC(SYSDATE) - 30 THEN 1 ELSE 0 END)
    FROM pwel_day_status
    GROUP BY data_class_name ORDER BY 2 DESC"""):
    print(f'  {str(cls):<24} rows={n:<7} wells={wells:<4} '
          f'{str(dmin)[:10]} .. {str(dmax)[:10]}  last30d={recent}')

# 4. wells per class
section('4. WELLS PER DATA CLASS (name via WELL table if possible)')
namesrc = None
for src in ('WELL', 'WELL_VERSION', 'OV_WELL'):
    try:
        cur.execute(f"SELECT object_code FROM {src} WHERE ROWNUM = 1")
        namesrc = src
        break
    except Exception:
        pass
print(f'  (well-name source: {namesrc})')
rows = run("""
    SELECT data_class_name, object_id, MAX(daytime), COUNT(*)
    FROM pwel_day_status
    GROUP BY data_class_name, object_id
    ORDER BY data_class_name, 2""")
for cls, oid, dmax, n in rows:
    name = ''
    if namesrc:
        try:
            r = run(f"SELECT object_code FROM {namesrc} WHERE object_id = :i AND ROWNUM = 1",
                    {'i': oid})
            name = r[0][0] if r else ''
        except Exception:
            pass
    print(f'  {str(cls):<24} {oid}  {name:<22} last={str(dmax)[:10]} rows={n}')

# 5. report-view dependencies
section('5. DEPENDENTS OF WOODSIDE REPORT VIEWS (ZWP_R_PWEL_DAY_STATUS_2)')
for ref in ('RV_ZWP_R_PWEL_DAY_STATUS_2', 'TV_ZWP_R_PWEL_DAY_STATUS_2',
            'ZWP_V_REP_PWEL_DAY_STATUS_2', 'RV_PWEL_DAY_STATUS_2',
            'RV_DT_PWEL_DAY_STATUS_2', 'TV_DT_PWEL_DAY_STATUS_2'):
    rows = run("""
        SELECT owner, name, type FROM all_dependencies
        WHERE referenced_name = :r ORDER BY type, name""", {'r': ref})
    print(f'  {ref}: {len(rows)} dependents')
    for owner, name, typ in rows:
        print(f'    {typ:<14} {owner}.{name}')

cur.close()
conn.close()
print('\nDone (read-only).')
