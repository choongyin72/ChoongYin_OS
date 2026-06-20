"""
Read-only query: SELECT * FROM ov_bank
Target: LOCAL SANDBOX DB (localhost:1521/ORCL) - where AUTOTEST_BNK_* were created.
oracledb thin mode (no client needed).
"""
import oracledb

HOST    = 'localhost'
PORT    = 1521
SERVICE = 'ORCL'
USER    = 'ECKERNEL_EC'
PWD     = 'energy'

dsn = oracledb.makedsn(HOST, PORT, service_name=SERVICE)
print(f'Connecting to {HOST}:{PORT}/{SERVICE} as {USER} ...')

try:
    conn = oracledb.connect(user=USER, password=PWD, dsn=dsn, tcp_connect_timeout=15)
    print('CONNECTED\n')
except Exception as e:
    print(f'CONNECTION FAILED: {type(e).__name__}: {e}')
    raise SystemExit(1)

cur = conn.cursor()

# How many rows?
try:
    cur.execute('SELECT COUNT(*) FROM ov_bank')
    total = cur.fetchone()[0]
    print(f'ov_bank total rows: {total}\n')
except Exception as e:
    print(f'COUNT failed: {type(e).__name__}: {e}')
    total = None

# Column names
cur.execute('SELECT * FROM ov_bank WHERE ROWNUM <= 50')
cols = [d[0] for d in cur.description]
print(f'Columns ({len(cols)}):')
print('  ' + ', '.join(cols))
print()

rows = cur.fetchall()
print(f'Fetched {len(rows)} row(s) (capped at 50):\n')

# Print compactly - show first ~6 columns per row for readability
show_cols = min(len(cols), 6)
header = ' | '.join(f'{cols[i][:18]:<18}' for i in range(show_cols))
print(header)
print('-' * len(header))
for r in rows:
    line = ' | '.join(f'{str(r[i])[:18]:<18}' for i in range(show_cols))
    print(line)

cur.close()
conn.close()
print('\nDone.')
