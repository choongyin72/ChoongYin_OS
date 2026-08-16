import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db
con = db._connect(); cur = con.cursor()
cur.execute("select code from ov_message_group where code like 'AUTOTEST%' and object_end_date is null")
codes = [r[0] for r in cur.fetchall()]
print("open AUTOTEST rows:", codes)
for c in codes:
    cur.execute("update ov_message_group set object_end_date = object_start_date where code = :c", c=c)
    print("  closed", c, "rows=", cur.rowcount)
con.commit()
cur.execute("select count(*) from ov_message_group where code like 'AUTOTEST%' and object_end_date is null")
print("remaining OPEN AUTOTEST rows:", cur.fetchone()[0])
cur.close(); con.close()
