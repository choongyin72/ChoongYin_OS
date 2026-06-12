"""READ-ONLY: query COPSDEV for existing Advanced File Import configuration -
interfaces, source mappings, target mappings, plus ECIS-related schedules.
These are the real-world examples to model the PHD-backup Excel upload after."""
import oracledb

conn = oracledb.connect(user="ECKERNEL_EC", password="energy",
                        dsn="db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev",
                        tcp_connect_timeout=20)
cur = conn.cursor()

print("=== IMP_SOURCE_INTERFACE (interfaces) ===")
try:
    cur.execute("""SELECT INTERFACE_CODE, NAME, TYPE, TRANSACTION_TYPE, FORMAT,
                          SOURCE_TYPE, EC_DATA_LEVEL, STAGING_VALIDATION_IND
                   FROM IMP_SOURCE_INTERFACE ORDER BY INTERFACE_CODE""")
    for r in cur.fetchall():
        print("  ", r)
except Exception as e:
    print("  ERR", str(e)[:120])

print("\n=== IMP_SOURCE_MAPPING counts per interface ===")
try:
    cur.execute("""SELECT INTERFACE_CODE, COUNT(*) FROM IMP_SOURCE_MAPPING
                   GROUP BY INTERFACE_CODE ORDER BY 1""")
    for r in cur.fetchall():
        print("  ", r)
except Exception as e:
    print("  ERR", str(e)[:120])

print("\n=== sample source mappings (first interface) ===")
try:
    cur.execute("""SELECT INTERFACE_CODE, CODE, TYPE, VALUE_TYPE, PATH_ORIGIN, EC_KEY
                   FROM IMP_SOURCE_MAPPING FETCH FIRST 15 ROWS ONLY""")
    for r in cur.fetchall():
        print("  ", r)
except Exception as e:
    print("  ERR", str(e)[:120])

print("\n=== IMP_TARGET_MAPPING sample ===")
try:
    cur.execute("""SELECT EC_KEY, CLASS, ATTRIBUTE, CLASS_KEY_1, CLASS_KEY_2,
                          CONSTANT_STRING_VALUE
                   FROM IMP_TARGET_MAPPING FETCH FIRST 15 ROWS ONLY""")
    for r in cur.fetchall():
        print("  ", r)
except Exception as e:
    print("  ERR", str(e)[:120])

print("\n=== ECIS-ish schedules (CTRL_JOB / scheduler tables) ===")
for q, lbl in [
    ("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'CTRL_JOB%'", "job tables"),
    ("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' AND table_name LIKE 'IMP_%'", "IMP_ tables"),
]:
    try:
        cur.execute(q)
        print(f"  {lbl}:", [r[0] for r in cur.fetchall()][:20])
    except Exception as e:
        print(f"  {lbl}: ERR {str(e)[:80]}")

cur.close()
conn.close()
print("done (READ-ONLY)")
