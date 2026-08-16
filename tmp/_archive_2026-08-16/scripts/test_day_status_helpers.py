"""Self-test the new DbVerify N1 helpers against the live DB."""
import sys
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as d

# 1) resolve a known well name -> OBJECT_ID
wid = d.well_object_id_by_name("AS2_Onshore Well no 2")
print("well_object_id_by_name('AS2_Onshore Well no 2') =", wid)

# 2) read a measured value for that well on the seed date
v = d.day_status_value("PWEL_DAY_STATUS", wid, "2003-01-01", "ON_STREAM_HRS")
print("day_status_value ON_STREAM_HRS on 2003-01-01 =", v)

# 3) positive assertion (should pass if v matches)
if v is not None:
    d.day_status_value_should_be("PWEL_DAY_STATUS", wid, "2003-01-01", "ON_STREAM_HRS", v)
    print("day_status_value_should_be PASS (value matches)")

# 4) negative assertion (should raise)
try:
    d.day_status_value_should_be("PWEL_DAY_STATUS", wid, "2003-01-01", "ON_STREAM_HRS", -99999)
    print("ERROR: negative assertion did NOT raise")
except AssertionError as e:
    print("negative assertion correctly raised:", str(e)[:90])

print("\nALL HELPER TESTS DONE")
