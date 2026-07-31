import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db
con = db._connect(); cur = con.cursor()
cur.execute("select code, object_start_date, object_end_date, functional_area_code "
            "from ov_message_group where code like 'AUTOTEST%'")
for r in cur.fetchall(): print("residual:", r)
cur.execute("select functional_area_code, count(*) from ov_message_group group by functional_area_code "
            "order by 2 desc")
print("existing rows per functional area:", cur.fetchall()[:8])
cur.close(); con.close()
