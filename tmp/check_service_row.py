import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = db._connect(); cur = con.cursor()
cur.execute("""select code, name, contract_code, transport_system_code, template_code, service_type,
                      status_code, object_start_date, object_end_date
               from ov_service where code like 'AUTOTEST%'""")
rows = cur.fetchall()
print(a("AUTOTEST rows in ov_service: %d" % len(rows)))
for r in rows: print(a("   %s" % (r,)))
cur.execute("select count(*) from ov_service where contract_code = 'TS3_GTA_SHP_A'")
print(a("rows under contract TS3_GTA_SHP_A (the nav scope): %d" % cur.fetchone()[0]))
cur.close(); con.close()
