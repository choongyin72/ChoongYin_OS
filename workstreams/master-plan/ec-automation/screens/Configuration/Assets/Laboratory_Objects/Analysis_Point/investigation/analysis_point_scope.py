"""Find the exact Op PU/Area/Facility NAMES for the populated Analysis Point scope (for the nav cascade +
insert Op-parent), by joining the OP_*_CODE columns to the object views. READ-ONLY."""
import os, oracledb
cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15).cursor()

print("=== distinct Op scope of existing analysis points ===")
cur.execute("""SELECT DISTINCT OP_PRODUCTIONUNIT_CODE, OP_AREA_CODE, OP_FCTY_1_CODE, TYPE
               FROM ECKERNEL_EC.OV_ANALYSIS_POINT ORDER BY 1,2,3""")
for r in cur.fetchall():
    print("  PU=%-10s AREA=%-14s FCTY=%-16s TYPE=%s" % tuple(str(x) for x in r))


def name_for(view, code):
    if not code or code == 'None':
        return code
    try:
        cur.execute(f"SELECT name FROM ECKERNEL_EC.{view} WHERE code=:c FETCH FIRST 1 ROWS ONLY", [code])
        row = cur.fetchone()
        return row[0] if row else '(no name in %s)' % view
    except Exception as e:
        return 'ERR %s' % str(e)[:40]


print("\n=== resolve names for nav cascade ===")
cur.execute("SELECT OP_PRODUCTIONUNIT_CODE, OP_AREA_CODE, OP_FCTY_1_CODE FROM ECKERNEL_EC.OV_ANALYSIS_POINT FETCH FIRST 1 ROWS ONLY")
pu, area, fcty = cur.fetchone()
print("  PU  :", pu, "->", name_for("OV_PRODUCTIONUNIT", pu))
for av in ("OV_AREA",):
    print("  AREA:", area, "->", name_for(av, area))
for fv in ("OV_FACILITY", "OV_FACILITY_CLASS_1", "OV_FCTY", "OV_FACILITY_CLASS"):
    n = name_for(fv, fcty)
    if not n.startswith("ERR") and not n.startswith("(no name"):
        print("  FCTY:", fcty, "->", n, f"(from {fv})"); break
else:
    print("  FCTY:", fcty, "-> (name view not found; will read live nav options)")

print("\n=== Analysis Point TYPE values present ===")
cur.execute("SELECT DISTINCT TYPE, TYPE_TEXT FROM ECKERNEL_EC.OV_ANALYSIS_POINT")
for r in cur.fetchall():
    print("  ", r)
cur.close()
print("\nDONE")
