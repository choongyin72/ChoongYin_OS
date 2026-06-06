"""Verify BNK_010 (RF run, End=Start) is gone from ov_bank. Read-only."""
import oracledb
dsn = oracledb.makedsn('localhost', 1521, service_name='ORCL')
conn = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=dsn, tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM ov_bank WHERE code = 'AUTOTEST_BNK_010'")
print(f'BNK_010 rows in ov_bank: {cur.fetchone()[0]}  (expect 0 = true delete)')
cur.execute("SELECT code, object_start_date, object_end_date FROM ov_bank WHERE code LIKE 'AUTOTEST_BNK_%' ORDER BY code")
print('\nAUTOTEST banks still in ov_bank:')
for r in cur.fetchall():
    s = r[1].strftime('%Y-%m-%d') if r[1] else 'None'
    e = r[2].strftime('%Y-%m-%d') if r[2] else 'None'
    print(f'  {r[0]:<20} start={s} end={e}')
cur.close(); conn.close()
