"""Pre-flight: confirm none of round 6's intended AUTOTEST codes already exist in their target
views before running the live batch. Financial Item Definition/Template and Project Data Mapping
Setup have no confirmed view name from their drivers (self-clean there is grid-based, not
view-based) - skipped here; their own harness functions clean up any pre-existing row live."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
import DbVerify as db

CHECKS = [
    ("ov_dummy_tag_event", "AUTOTEST_R6_DTE"),
    ("ov_split_item_other", "AUTOTEST_R6_SIO"),
    ("ov_testseparator", "AUTOTEST_R6_TSEP"),
    ("ov_trans_inv_tmpl_set", "AUTOTEST_R6_TILS"),
    ("ov_trans_inventory", "AUTOTEST_R6_TIP"),
    ("ov_fin_uop_depr_key", "AUTOTEST_R6_UOP"),
    ("ov_well_hole", "AUTOTEST_R6_WHL"),
    ("ov_well_hookup", "AUTOTEST_R6_WH"),
    ("ov_resv_block_formation", "AUTOTEST_R6_RBF"),
    ("ov_resv_block", "AUTOTEST_R6_RBFB"),
    ("ov_resv_formation", "AUTOTEST_R6_RBFF"),
    ("OV_STREAM_ITEM", "AUTOTEST_R6_SI"),
    ("ov_well_bore", "AUTOTEST_R6_WB"),
    ("ov_well_bore_interval", "AUTOTEST_R6_WBI"),
    ("ov_calculation", "AUTOTEST_R6_CC"),
]

ok = True
for view, code in CHECKS:
    present = db.code_present(view, code)
    print(f"  {'COLLISION' if present else 'clear    '}  {view:<28} {code}")
    if present:
        ok = False

print("\nPre-flight:", "ALL CLEAR" if ok else "COLLISIONS FOUND - do not run live yet")
sys.exit(0 if ok else 1)
