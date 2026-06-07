"""DB verify for MIME Type Mapping. Read-only. Checks test row + existing-data integrity."""
import oracledb, sys
TEST = sys.argv[1] if len(sys.argv) > 1 else 'application/x-ec-autotest'
c = oracledb.connect(user='ECKERNEL_EC', password='energy',
                     dsn=oracledb.makedsn('localhost', 1521, service_name='ORCL'), tcp_connect_timeout=15)
cur = c.cursor()

# columns of the base table
cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name='CTRL_MIME_TYPE_MAPPING' ORDER BY column_id")
print('CTRL_MIME_TYPE_MAPPING cols:', [r[0] for r in cur.fetchall()])

for obj in ['CTRL_MIME_TYPE_MAPPING', 'TV_CTRL_MIME_TYPE_MAPPING']:
    cur.execute(f'SELECT COUNT(*) FROM {obj}')
    print(f'\n{obj}: total rows = {cur.fetchone()[0]}')

print('\n=== All MIME types in base table (CTRL_MIME_TYPE_MAPPING) ===')
cur.execute("SELECT mime_type, file_extensions FROM ctrl_mime_type_mapping ORDER BY mime_type")
for r in cur.fetchall():
    flag = '  <== TEST ROW' if r[0] == TEST else ''
    print(f'  {r[0]:<70} {r[1] or ""}{flag}')

cur.execute("SELECT COUNT(*) FROM ctrl_mime_type_mapping WHERE mime_type = :m", m=TEST)
print(f'\nTest row "{TEST}" present in base table: {cur.fetchone()[0]} row(s)')
cur.close(); c.close()
