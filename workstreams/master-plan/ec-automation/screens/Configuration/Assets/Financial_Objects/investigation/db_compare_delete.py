"""
Compare delete semantics in ov_bank:
  BNK_001-008: End Date = Start +1 day (2000-01-02)
  BNK_009    : End Date = Start Date  (2000-01-01)  <- the corrected EC delete
Read-only.
"""
import oracledb

dsn = oracledb.makedsn('localhost', 1521, service_name='ORCL')
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=dsn, tcp_connect_timeout=15)
cur = conn.cursor()

print('=== ov_bank total rows ===')
cur.execute('SELECT COUNT(*) FROM ov_bank')
print(f'  {cur.fetchone()[0]}\n')

print('=== All AUTOTEST banks: code, start, end, rev ===')
cur.execute("""SELECT code, object_start_date, object_end_date, rev_no, record_status
               FROM ov_bank WHERE code LIKE 'AUTOTEST_BNK_%' ORDER BY code""")
print(f'  {"CODE":<20} {"START":<12} {"END":<12} {"REV":<6} {"STATUS"}')
print('  ' + '-'*60)
for r in cur.fetchall():
    start = r[1].strftime('%Y-%m-%d') if r[1] else 'None'
    end   = r[2].strftime('%Y-%m-%d') if r[2] else 'None'
    print(f'  {r[0]:<20} {start:<12} {end:<12} {str(r[3]):<6} {r[4]}')

print('\n=== Is BNK_009 present in ov_bank at all? ===')
cur.execute("SELECT COUNT(*) FROM ov_bank WHERE code = 'AUTOTEST_BNK_009'")
n9 = cur.fetchone()[0]
print(f'  AUTOTEST_BNK_009 rows in ov_bank: {n9}')

# ov_bank is an object VIEW. Check the underlying base table too (likely OBJECTS / O_BANK).
# Try common EC base tables to see if the physical record still exists.
print('\n=== Underlying base-table check (does the physical row survive?) ===')
for tbl, col in [('o_bank', 'code'), ('objects', 'code')]:
    try:
        cur.execute(f"SELECT code, object_start_date, object_end_date FROM {tbl} "
                    f"WHERE code = 'AUTOTEST_BNK_009'")
        rows = cur.fetchall()
        print(f'  {tbl}: {len(rows)} row(s) for BNK_009 -> {rows}')
    except Exception as e:
        print(f'  {tbl}: (n/a) {type(e).__name__}')

# Compare: how many AUTOTEST rows still visible vs total created (009)
print('\n=== Summary ===')
cur.execute("SELECT COUNT(*) FROM ov_bank WHERE code LIKE 'AUTOTEST_BNK_%'")
print(f'  AUTOTEST banks visible in ov_bank now: {cur.fetchone()[0]}')

cur.close()
conn.close()
print('\nDone.')
