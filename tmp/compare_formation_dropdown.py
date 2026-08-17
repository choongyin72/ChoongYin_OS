"""Compare the two tools directly on the SAME page state: after correctly selecting Reservoir
Block, does the proven ec_object_iud.select_dropdown() find any options in the dependent
Reservoir Formation dropdown where engine.py's select() found zero? Isolates whether this is an
engine-specific gap or a genuine EC/sandbox cascade limitation."""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "py"))
sys.path.insert(0, str(_HERE.parent / "workstreams" / "master-plan" / "ec-automation" / "libraries"))
from engine import Engine, open_screen, css
from universal_classifier import EC_URL
from playwright.sync_api import sync_playwright
import ec_object_iud as ec

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    open_screen(page, "Reservoir Block Formation")
    eng = Engine(page, "Reservoir Block Formation")
    eng.toolbar("New Object")
    page.wait_for_timeout(1000)

    print("Selecting Reservoir Block via engine.select() ...")
    eng.select("Reservoir Block", "AUTOTEST R6 RBF Block")
    print("  Block selected OK")
    page.wait_for_timeout(1000)

    ff = eng._field("Reservoir Formation")
    print("Reservoir Formation field id:", ff["id"])

    print("\nAttempting ec_object_iud.select_dropdown() on Reservoir Formation (value='__FIRST__')...")
    try:
        ec.select_dropdown(page, ff["id"], "__FIRST__")
        print("  SUCCESS - select_dropdown() found and picked an option")
        val = page.eval_on_selector(f"[id='{ff['id']}']", "e => e.value")
        print("  resulting value:", val)
    except Exception as e:
        print("  FAILED:", str(e)[:300])

    b.close()
