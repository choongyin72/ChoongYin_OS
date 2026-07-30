"""R12: confirm DbVerify.py still imports + has both new and existing keywords. tmp scratch."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path("C:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")))
import DbVerify
new = ["fetch_object", "field_equals", "verify_row", "field_should_equal_in_view", "code_present", "count_like"]
existing = ["code_should_be_present_in_view", "code_should_be_absent_in_view", "view_row_count",
            "day_status_value_should_be", "record_status_family_count", "message_journal_count"]
for f in new + existing:
    assert hasattr(DbVerify, f), "MISSING: " + f
print("DbVerify import OK -", len(new), "new +", len(existing), "existing keywords present")
# smoke the new ones read-only against a known bank
print("code_present(ov_bank, CITI):", DbVerify.code_present("ov_bank", "CITI"))
ok, act = DbVerify.field_equals("ov_bank", "CITI", "BANK_SWIFT_CODE", "SWCITILONGB")
print("field_equals swift:", ok, act)
