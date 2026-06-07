"""Find the Language backing table/view + code column + length. Read-only."""
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
                        dsn=oracledb.makedsn('localhost', 1521, service_name='ORCL'),
                        tcp_connect_timeout=15)
cur = conn.cursor()
print('=== tables/views matching LANG ===')
cur.execute("""SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE '%LANG%' ORDER BY table_name""")
tabs = [r[0] for r in cur.fetchall()]
print(' tables:', tabs)
cur.execute("""SELECT view_name FROM all_views WHERE owner='ECKERNEL_EC' AND view_name LIKE '%LANG%' ORDER BY view_name""")
print(' views :', [r[0] for r in cur.fetchall()])

# inspect the most likely base table candidates
for t in tabs:
    if t.endswith('_JN'):
        continue
    try:
        cur.execute(f'SELECT COUNT(*) FROM {t}')
        n = cur.fetchone()[0]
    except Exception as e:
        n = f'err {e}'
    print(f'\n--- {t}: {n} rows ---')
    cur.execute("""SELECT column_name, data_type, data_length FROM all_tab_columns
                   WHERE table_name=:t AND data_type LIKE '%CHAR%' ORDER BY column_id""", t=t)
    for name, dtype, dlen in cur.fetchall():
        print(f'    {name:<22} {dtype}({dlen})')
cur.close(); conn.close()
