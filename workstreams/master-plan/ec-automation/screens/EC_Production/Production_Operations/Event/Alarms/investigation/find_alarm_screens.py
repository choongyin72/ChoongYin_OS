"""Identify candidate EC 'alarm' screens: class labels containing 'alarm' + their type/time-scope + view.
READ-ONLY. Helps match the screenshot (Date+PU+Area+Facility Class 1 nav, columns Time/Area/Type of Alarm/
Reason/Report)."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()

print("=== class labels containing 'ALARM' ===")
cur.execute("""SELECT p.class_name, p.property_value AS label, c.class_type, c.time_scope_code,
                      c.db_object_name, c.app_space_cntx
               FROM class_property_cnfg p
               JOIN class_cnfg c ON c.class_name = p.class_name
               WHERE p.property_code='LABEL' AND UPPER(p.property_value) LIKE '%ALARM%'
                 AND p.class_name NOT LIKE '%\\_ROWSORT' ESCAPE '\\'
                 AND p.class_name NOT LIKE '%\\_TEST' ESCAPE '\\'
               ORDER BY c.class_type, p.class_name""")
rows = cur.fetchall()
for r in rows:
    print(f"  [{r[2]:>6}/{(r[3] or '-'):>9}] {r[0]:32s} label='{r[1]}'  base={r[4]}  ctx={r[5]}")
print(f"\n({len(rows)} candidates)")

print("\n=== any tables/views with ALARM (for grain hints) ===")
cur.execute("""SELECT object_name, object_type FROM all_objects WHERE owner='ECKERNEL_EC'
               AND object_type IN ('TABLE','VIEW') AND object_name LIKE '%ALARM%'
               AND object_name NOT LIKE '%JN' ORDER BY 2,1 FETCH FIRST 25 ROWS ONLY""")
for r in cur.fetchall():
    print(f"  {r[1][0]} {r[0]}")
cur.close()
print("\nDONE")
