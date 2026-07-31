import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db
def a(s): return str(s).encode("ascii","replace").decode("ascii")
con = db._connect(); cur = con.cursor()
cur.execute("select * from ov_service where code like 'AUTOTEST%' and object_end_date is null")
cols = [d[0] for d in cur.description]
for r in cur.fetchall():
    print(a("FULL ROW logged before write:"))
    for k, v in zip(cols, r):
        if v is not None: print(a("   %-26s %r" % (k, v)))
cur.execute("""update ov_service set object_end_date = object_start_date
               where code like 'AUTOTEST%' and object_end_date is null""")
print(a("rows closed: %d" % cur.rowcount))
con.commit()
cur.execute("select count(*) from ov_service where code like 'AUTOTEST%' and object_end_date is null")
print(a("open AUTOTEST rows left: %d" % cur.fetchone()[0]))
cur.close(); con.close()
