import oracledb
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = con.cursor()
for sql, lbl in (
  ("select code, name, object_start_date, object_end_date from ov_contract where code='TS3_GTA_SHP_A'", "contract TS3_GTA_SHP_A"),
  ("select code, name, object_start_date, object_end_date from ov_transport_system where code in ('TS3_SYSTEM','TS5_TS')", "transport systems"),
  ("select code, name, object_start_date from ov_business_unit where code='TS3_BU1'", "BU TS3_BU1"),
  ("select min(object_start_date), max(object_start_date) from ov_service", "existing SERVICE start dates")):
    try:
        cur.execute(sql); print(a("%-28s %s" % (lbl, cur.fetchall())))
    except Exception as e:
        print(a("%-28s ERR %s" % (lbl, repr(e)[:70])))
cur.close(); con.close()
