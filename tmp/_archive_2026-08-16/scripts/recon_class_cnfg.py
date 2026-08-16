"""Verify the user's metadata-from-screen-name queries (class_property_cnfg + class_cnfg) so the spec
template can reduce its inputs to ONLY the screen name. Run for 'contract area'. SELECT only."""
import os
import oracledb

cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()
SCREEN = os.environ.get("SCREEN", "contract area").lower()


def q(sql, *a):
    cur.execute(sql, a); return cur.fetchall()


print(f"=== [1] class_name from LABEL = '{SCREEN}' ===")
cn = q("""SELECT t.class_name FROM class_property_cnfg t
          WHERE t.property_code='LABEL' AND lower(t.property_value)=:s""", SCREEN)
print("  class_name(s):", cn)

print(f"\n=== [2] class_cnfg columns ===")
cols = [c[0] for c in q("SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC' AND table_name='CLASS_CNFG' ORDER BY column_id")]
print("  ", ", ".join(cols))

print(f"\n=== [3] class_cnfg row(s) for the screen's class (the t.* the user cited) ===")
rows = q("""SELECT * FROM class_cnfg t WHERE t.class_name IN (
              SELECT class_name FROM class_property_cnfg
              WHERE property_code='LABEL' AND lower(property_value)=:s)""", SCREEN)
for r in rows:
    d = dict(zip(cols, r))
    # print the fields most likely to carry type / view / base table / date-effective
    keep = {k: v for k, v in d.items() if any(t in k for t in
            ("CLASS_NAME", "TYPE", "VIEW", "TABLE", "OBJECT", "DATE", "DELETE", "EFFECTIV", "SCREEN", "OV_", "MANAGE"))}
    print("  ", keep)
    print("   FULL:", d)
cur.close()
print("\nDONE")
