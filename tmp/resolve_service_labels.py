#!/usr/bin/env python3
"""READ-ONLY: turn the CODES an existing SERVICE row uses into the LABELS the form dropdowns show.
Mirroring a real row (feedback_scan_existing_row_first) beats guessing valid combinations, and the
label/code distinction already tripped me once today."""
import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()

def one(sql, **kw):
    try:
        cur.execute(sql, kw); r = cur.fetchall(); return r
    except Exception as e:
        return [("ERR", repr(e)[:80])]

print(a("BU whose code is TS3_BU1:            %s" % one("select code, name from ov_businessunit where code='TS3_BU1'")))
print(a("contract TS3_GTA_SHP_A:              %s" % one("select code, name from ov_contract where code='TS3_GTA_SHP_A'")))
print(a("transport system TS3_SYSTEM:         %s" % one("select code, name from ov_transportsystem where code='TS3_SYSTEM'")))
print(a("service template TS3_STD_SERVICE_TEMP: %s" % one("select code, name from ov_service_template where code='TS3_STD_SERVICE_TEMP'")))
print(a("\nthe existing row I am mirroring:"))
print(a("   %s" % one("""select code, template_code, service_type, service_type_type, status_code,
                                contract_code, transport_system_code
                         from ov_service where code='TS3_SHIPPER_A_P2P'""")))
cur.close(); con.close()
