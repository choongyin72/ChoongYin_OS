import sys
sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\libraries")
from DbVerify import _code_present

for view, code in [
    ("OV_RESV_BLOCK", "AUTOTEST_PROBE_BLK"),
    ("OV_RESV_FORMATION", "AUTOTEST_PROBE_FRM"),
    ("OV_RESV_BLOCK_FORMATION", "AUTOTEST_PROBE_RBF"),
]:
    print(view, code, "present:", _code_present(view, code))
