"""
Detail probe for AUTOTEST_BNK_003 (which the UI UPDATE changed to '...UPDATED').
ov_bank showed the base name - investigate why (date-effective versioning).
Read-only.
"""
import oracledb

dsn = oracledb.makedsn('localhost', 1521, service_name='ORCL')
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=dsn, tcp_connect_timeout=15)
cur = conn.cursor()

print('=== Full ov_bank row for AUTOTEST_BNK_003 ===')
cur.execute("SELECT * FROM ov_bank WHERE code = 'AUTOTEST_BNK_003'")
cols = [d[0] for d in cur.description]
row = cur.fetchone()
for c, v in zip(cols, row):
    print(f'  {c:<22}: {v}')

# Is NAME a date-effective attribute? Check how many name versions / revisions exist.
print('\n=== Row count per AUTOTEST code in ov_bank (versions visible) ===')
cur.execute("""SELECT code, COUNT(*) FROM ov_bank
               WHERE code LIKE 'AUTOTEST_BNK_%' GROUP BY code ORDER BY code""")
for r in cur.fetchall():
    print(f'  {r[0]:<20}: {r[1]} row(s)')

# Look for the updated name anywhere in ov_bank
print("\n=== Any ov_bank row whose NAME contains 'UPDATED' ===")
cur.execute("SELECT code, name, object_start_date, object_end_date FROM ov_bank WHERE name LIKE '%UPDATED%'")
hits = cur.fetchall()
if hits:
    for r in hits:
        print(f'  {r[0]:<20} | {r[1]:<28} | {r[2]} | {r[3]}')
else:
    print('  (none - updated name not present in ov_bank)')

cur.close()
conn.close()
print('\nDone.')
