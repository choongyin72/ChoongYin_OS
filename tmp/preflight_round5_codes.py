"""Pre-flight: confirm none of round 5's intended AUTOTEST codes already exist in their target
views before running the live batch (established convention from every prior round)."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
import DbVerify as db

CHECKS = [
    ("ov_orifice_plate", "AUTOTEST_R5_OP"),
    ("ov_pilot_boat", "AUTOTEST_R5_PB"),
    ("ov_process_train", "AUTOTEST_R5_PT"),
    ("ov_prodseparator", "AUTOTEST_R5_PSEP"),
    ("ov_resv_block", "AUTOTEST_R5_RESVB"),
    ("ov_resv_formation", "AUTOTEST_R5_RESVF"),
    ("ov_stream_category", "AUTOTEST_R5_RSC"),
    ("ov_service", "AUTOTEST_R5_SV"),
    ("ov_storage_flow", "AUTOTEST_R5_SF"),
    ("ov_stream_item_category", "AUTOTEST_R5_SIC"),
    ("ov_task_process", "AUTOTEST_R5_TP"),
    ("ov_shift", "AUTOTEST_R5_SH"),
    ("ov_report_group", "AUTOTEST_R5_RG"),
    ("ov_perf_interval", "AUTOTEST_R5_PI"),
]

ok = True
for view, code in CHECKS:
    present = db.code_present(view, code)
    print(f"  {'COLLISION' if present else 'clear    '}  {view:<28} {code}")
    if present:
        ok = False

rec_residual = db.count_like("OV_ENDPOINT_CONFIG", "autotest-r5-")
print(f"  {'COLLISION' if rec_residual else 'clear    '}  OV_ENDPOINT_CONFIG           autotest-r5-* ({rec_residual} residual)")
if rec_residual:
    ok = False

print("\nPre-flight:", "ALL CLEAR" if ok else "COLLISIONS FOUND - do not run live yet")
sys.exit(0 if ok else 1)
