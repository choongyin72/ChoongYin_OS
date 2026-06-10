"""ECPR-31011 read-only DB recon on plutodev (Woodside DEV).

Answers:
  1. Which PWEL_DAY_STATUS / PWEL_DAY_STATUS_2 objects exist (tables, DV_/OV_/TV_ views)?
  2. Column diff between the two classes (incl. the 5 ZWP_* attrs from Cato's comment).
  3. Is SCA data still actively landing in PWEL_DAY_STATUS_2 (row counts, last DAYTIME)?
  4. Which wells write to class 2?
  5. Who depends on PWEL_DAY_STATUS_2 / DV_PWEL_DAY_STATUS_2 (DB-side consumer list)?
  6. Do the two theoretical-rate packages exist (zwp_ vs ecbp_)?

No INSERT/UPDATE/DELETE/DDL anywhere.
"""
import oracledb

WANTED_ZWP = ['ZWP_ALLOC_GAS_ENERGY', 'ZWP_MEAS_EV_RATIO', 'ZWP_MEAS_GAS_ENERGY',
              'ZWP_MEAS_MV_RATIO', 'ZWP_THEOR_GAS_ENERGY']

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

# 1. object inventory
section('1. OBJECT INVENTORY (tables/views named *PWEL_DAY_STATUS*)')
try:
    for owner, name, otype in run("""
        SELECT owner, object_name, object_type FROM all_objects
        WHERE object_name LIKE '%PWEL_DAY_STATUS%'
        ORDER BY object_type, object_name"""):
        print(f'  {otype:<14} {owner}.{name}')
except Exception as e:
    print('  ERROR:', e)

# 2. column diff
section('2. COLUMN DIFF: PWEL_DAY_STATUS vs PWEL_DAY_STATUS_2 (base tables)')
try:
    cols = {}
    for tab in ('PWEL_DAY_STATUS', 'PWEL_DAY_STATUS_2'):
        cols[tab] = {r[0] for r in run("""
            SELECT column_name FROM all_tab_columns
            WHERE table_name = :t AND owner = 'ECKERNEL'""", {'t': tab})}
        if not cols[tab]:  # fallback: whoever owns it
            cols[tab] = {r[0] for r in run("""
                SELECT DISTINCT column_name FROM all_tab_columns
                WHERE table_name = :t""", {'t': tab})}
        print(f'  {tab}: {len(cols[tab])} columns')
    only2 = sorted(cols['PWEL_DAY_STATUS_2'] - cols['PWEL_DAY_STATUS'])
    only1 = sorted(cols['PWEL_DAY_STATUS'] - cols['PWEL_DAY_STATUS_2'])
    print(f'\n  Columns ONLY in PWEL_DAY_STATUS_2 ({len(only2)}):')
    for c in only2:
        print('    ', c)
    print(f'\n  Columns ONLY in PWEL_DAY_STATUS ({len(only1)}):')
    for c in only1:
        print('    ', c)
    print('\n  The 5 ZWP_* attrs Cato listed — present in PWEL_DAY_STATUS?')
    for c in WANTED_ZWP:
        print(f'    {c:<28} status1={"YES" if c in cols["PWEL_DAY_STATUS"] else "no "} '
              f'status2={"YES" if c in cols["PWEL_DAY_STATUS_2"] else "no "}')
except Exception as e:
    print('  ERROR:', e)

# 3. data activity
section('3. DATA ACTIVITY (row counts, daytime range, recent landings)')
for tab in ('PWEL_DAY_STATUS', 'PWEL_DAY_STATUS_2'):
    try:
        n, dmin, dmax, wells = run(f"""
            SELECT COUNT(*), MIN(daytime), MAX(daytime), COUNT(DISTINCT object_id)
            FROM {tab}""")[0]
        recent = run(f"""
            SELECT COUNT(*) FROM {tab} WHERE daytime >= TRUNC(SYSDATE) - 30""")[0][0]
        print(f'  {tab:<22} rows={n:<9} wells={wells:<5} '
              f'daytime {str(dmin)[:10]} .. {str(dmax)[:10]}  rows_last30d={recent}')
    except Exception as e:
        print(f'  {tab}: ERROR: {e}')

# 4. wells on class 2
section('4. WELLS WRITING TO PWEL_DAY_STATUS_2 (latest 30 days)')
try:
    rows = run("""
        SELECT s.object_id, MAX(s.daytime), COUNT(*)
        FROM pwel_day_status_2 s
        WHERE s.daytime >= TRUNC(SYSDATE) - 30
        GROUP BY s.object_id ORDER BY 1""")
    print(f'  {len(rows)} wells active in last 30 days')
    # try to resolve names via the well object table
    for src in ('WELL', 'WELL_VERSION', 'OV_WELL'):
        try:
            cur.execute(f"SELECT object_code FROM {src} WHERE ROWNUM = 1")
            namesrc = src
            break
        except Exception:
            namesrc = None
    for oid, dmax, n in rows[:40]:
        name = ''
        if namesrc:
            try:
                r = run(f"SELECT object_code FROM {namesrc} WHERE object_id = :i AND ROWNUM = 1",
                        {'i': oid})
                name = r[0][0] if r else ''
            except Exception:
                pass
        print(f'    {oid}  {name:<20} last={str(dmax)[:10]} rows={n}')
    if len(rows) > 40:
        print(f'    ... and {len(rows) - 40} more')
except Exception as e:
    print('  ERROR:', e)

# 5. DB-side consumers
section('5. DB DEPENDENCIES on PWEL_DAY_STATUS_2 / DV_PWEL_DAY_STATUS_2')
try:
    for ref in ('PWEL_DAY_STATUS_2', 'DV_PWEL_DAY_STATUS_2'):
        rows = run("""
            SELECT owner, name, type FROM all_dependencies
            WHERE referenced_name = :r
            ORDER BY type, name""", {'r': ref})
        print(f'  referenced_name={ref}: {len(rows)} dependents')
        for owner, name, typ in rows:
            print(f'    {typ:<14} {owner}.{name}')
except Exception as e:
    print('  ERROR:', e)

# 6. theoretical packages
section('6. THEORETICAL-RATE FUNCTIONS (zwp_ vs ecbp_)')
try:
    for pkg in ('ZWP_PROD_WELL_THEORETICAL', 'ECBP_WELL_THEORETICAL'):
        rows = run("""
            SELECT owner, object_type, status FROM all_objects
            WHERE object_name = :p""", {'p': pkg})
        if rows:
            for owner, otype, status in rows:
                print(f'  {pkg:<28} {otype:<14} {owner} status={status}')
        else:
            print(f'  {pkg:<28} NOT FOUND')
except Exception as e:
    print('  ERROR:', e)

cur.close()
conn.close()
print('\nDone (read-only).')
