"""Re-run just Service (with the apply_navigator levels fix) and Remote Endpoint Configuration
(with the insert-check retry fix) to clean up the two residual rows left by the first round-5
attempt and confirm both now pass full I-U-D + self-clean."""
import json
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import DbVerify as db

sys.path.insert(0, str(_HERE))
import importlib
r5 = importlib.import_module("stability_test_round5")

overall = {}
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    # Service: existing residual row AUTOTEST_R5_SV must be cleaned up as part of the pre-existing
    # check inside run_standard_ov (row_exists via select_row -> End=Start), now correctly
    # visible with levels=1.
    svc_cfg = next(c for c in r5.SCREENS if c["name"] == "Service")
    r = r5.run_standard_ov(page, svc_cfg)
    overall["Service"] = r
    print(f"[Service] insert={r['insert']} update={r['update']} delete={r['delete']} "
          f"self_clean={r['self_clean']} elapsed={r['elapsed_s']}s error={r['error']}")

    r2 = r5.run_remote_endpoint_config(page)
    overall["Remote Endpoint Configuration"] = r2
    print(f"[Remote Endpoint Configuration] insert={r2['insert']} update={r2['update']} "
          f"delete={r2['delete']} self_clean={r2['self_clean']} elapsed={r2['elapsed_s']}s error={r2['error']}")

    b.close()

with open(str(_HERE / "stability_test_round5_rerun_results.json"), "w", encoding="utf-8") as f:
    json.dump(overall, f, indent=2)
