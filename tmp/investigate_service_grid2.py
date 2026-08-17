"""Contract's own BU_CODE = TS3_BU1 (confirmed via ov_contract -> ov_contract_area join) - matches
the nav scope exactly. So the invisibility is NOT a BU-scope mismatch. Retest with a fresh page load
+ longer settle time to rule out a caching/timing lag (Production Day Table precedent: some EC
screens have a real multi-second DB-commit-visibility delay)."""
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

CODE = "AUTOTEST_R5_SV"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    open_screen(page, "Service")
    eng = Engine(page, "Service")
    eng.apply_navigator(values=["TS3 BU1"])
    page.wait_for_timeout(3000)

    for i in range(3):
        info = page.evaluate(
            """(gid) => { const tb = document.getElementById(gid); if (!tb) return null;
                const rows = Array.from(tb.querySelectorAll('tr[data-ri]'));
                return { count: rows.length, texts: rows.map(r => r.textContent.trim().slice(0, 80)) }; }""",
            "manageObject:form:T_data",
        )
        print(f"attempt {i}: rows={info['count'] if info else None}")
        if info:
            for t in info["texts"]:
                print("   ", repr(t))
        if info and any("AUTOTEST_R5_SV" in t for t in info["texts"]):
            print("FOUND on attempt", i)
            break
        # re-query via GO again
        eng._click_go()
        page.wait_for_timeout(2500)

    b.close()
