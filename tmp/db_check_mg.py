import sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "libraries"))
import DbVerify as db
for q in ("select code, name, object_start_date, object_end_date from ov_message_group where code like 'AUTOTEST%'",
          "select count(*) from ov_message_group"):
    try:
        print(q[:70], "->", db.query(q) if hasattr(db, "query") else "(no query helper)")
    except Exception as e:
        print("ERR", repr(e)[:120])
print("code_present:", db.code_present("ov_message_group", "AUTOTEST_MG001"))
