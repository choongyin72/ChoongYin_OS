"""Self-test the new N3 DbVerify helpers against the live DB (read-only + a no-op restore since
baseline is already clean). Confirms they return the expected baseline values before Robot wiring."""
import sys
sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\libraries")
import DbVerify as dv

DATE = "2024-02-06"
PID = "P1_FwdUpd"

print("record_status_family_count(P):", dv.record_status_family_count(DATE, "P"))
print("record_status_family_count(V):", dv.record_status_family_count(DATE, "V"), "(expect 0 = clean baseline)")
print("status_process_run_count(P1_FwdUpd):", dv.status_process_run_count(PID, DATE), "(expect >=1, append-only log)")
print("latest_status_process_rows_updated:", dv.latest_status_process_rows_updated(PID, DATE), "(expect 15 from proven run)")
print("restore_record_status_family (no-op, baseline clean):", dv.restore_record_status_family(DATE, "V", "P"), "(expect 0)")
print("DONE")
