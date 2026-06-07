"""Find the Equipment object view/table in EC. Read-only."""
import oracledb
conn = oracledb.connect(user='ECKERNEL_EC', password='energy',
                        dsn=oracledb.makedsn('localhost', 1521, service_name='ORCL'), tcp_connect_timeout=15)
cur = conn.cursor()

print('=== VIEWS containing EQUIP ===')
cur.execute("SELECT view_name FROM all_views WHERE view_name LIKE '%EQUIP%' ORDER BY view_name")
for r in cur.fetchall(): print('  ', r[0])

print('\n=== TABLES containing EQUIP ===')
cur.execute("SELECT table_name FROM all_tables WHERE table_name LIKE '%EQUIP%' ORDER BY table_name")
for r in cur.fetchall(): print('  ', r[0])

print('\n=== any OV_ object that has a row with code OFF_FLASH_GAS_COMP ===')
# check a few likely OV_ views for the known equipment code
cur.execute("SELECT view_name FROM all_views WHERE view_name LIKE 'OV\\_%' ESCAPE '\\'")
views = [r[0] for r in cur.fetchall()]
print(f'  ({len(views)} OV_ views total) probing for OFF_FLASH_GAS_COMP...')
found = []
for v in views:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {v} WHERE code = 'OFF_FLASH_GAS_COMP'")
        if cur.fetchone()[0] > 0:
            found.append(v)
    except Exception:
        pass
print(f'  views containing OFF_FLASH_GAS_COMP: {found}')

cur.close(); conn.close()
