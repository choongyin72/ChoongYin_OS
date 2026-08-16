import sys
sys.path.insert(0, r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries")
import DbVerify as db
result = db.code_present("ov_bank", "AUTOTEST_DOES_NOT_EXIST_XYZ")
print("code_present() returned:", result, "(should be False)")
count = db.view_row_count("ov_bank")
print("view_row_count() returned:", count, "(should be a positive integer)")
