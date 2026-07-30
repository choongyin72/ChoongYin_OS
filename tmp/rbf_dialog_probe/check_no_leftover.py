import sys
sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\libraries")
from DbVerify import _code_present

present = _code_present("OV_RESV_FORMATION", "AUTOTEST_PROBE_001")
print("AUTOTEST_PROBE_001 present in OV_RESV_FORMATION:", present)
