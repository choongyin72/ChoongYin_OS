"""Smoke-test the new allocation conservation-oracle keywords in DbVerify.py."""
import sys
sys.path.insert(0, r"C:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d

print("row_count 2021-10-01 :", d.allocation_row_count("PWEL_DAY_ALLOC", "2021-10-01"))
print("neg_count 2021-10-01 :", d.allocation_negative_count("PWEL_DAY_ALLOC", "2021-10-01"))
d.allocation_conservation_should_hold("PWEL_DAY_ALLOC", "2021-10-01")
print("conservation_should_hold 2021-10-01 : PASS")

# Negative-path: an empty day must FAIL (guards vacuous pass)
try:
    d.allocation_conservation_should_hold("PWEL_DAY_ALLOC", "1999-01-01")
    print("EMPTY-DAY GUARD : FAIL (should have raised)")
except AssertionError as e:
    print("EMPTY-DAY GUARD : PASS ->", str(e)[:70])
print("DONE")
