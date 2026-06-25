"""Business-Unit distribution of Contract Areas + the BU object's display name (for the nav dropdown label)
and whether OV_CONTRACT_AREA has any AUTOTEST_ residue. READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()

print("=== contract-area count per Business Unit (code) ===")
cur.execute("""SELECT business_unit_code, COUNT(*) FROM ECKERNEL_EC.OV_CONTRACT_AREA
               GROUP BY business_unit_code ORDER BY 2 DESC""")
for r in cur.fetchall():
    print(f"  {r[0]:18s} {r[1]}")

print("\n=== Business Unit names (for nav dropdown data-item-label) ===")
try:
    cur.execute("""SELECT code, name FROM ECKERNEL_EC.OV_BUSINESS_UNIT ORDER BY code""")
    for r in cur.fetchall()[:30]:
        print(f"  {r[0]:18s} {r[1]}")
except Exception as e:
    print("  OV_BUSINESS_UNIT:", str(e)[:70])

print("\n=== any AUTOTEST_ residue already present? ===")
cur.execute("""SELECT code, name, business_unit_code, object_start_date, end_date
               FROM ECKERNEL_EC.OV_CONTRACT_AREA WHERE code LIKE 'AUTOTEST%' OR name LIKE 'AUTOTEST%'""")
rows = cur.fetchall()
print("  residue rows:", len(rows))
for r in rows:
    print("   ", r)
cur.close()
print("\nDONE")
