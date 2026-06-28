"""
PRE-FLIGHT GRID-LOCATOR GUARD (read-only) -- run BEFORE the live RF run.

Purpose: make the "assumed the grid id from a sibling screen" mistake IMPOSSIBLE to ship
silently. (Root cause of the CD.0024 Calendar miss: the term screens use
`manage_object_nav_nav:form:T_data` + a GO button; Calendar is a custom-URL OV with grid
`nav:form:T_data` and NO GO. The insert persisted but the UI row-check failed confusingly.)

This opens the screen and asserts the T3's declared grid id actually exists in the live DOM,
and reports whether a navigator GO button is present. On mismatch it FAILS LOUD (exit 1) and
prints the ACTUAL grid id(s) on the screen so the fix is obvious -- no guessing, no sibling copy.

Usage (env-driven, matches scan_ec_screen.py):
    SCREEN="Calendar" GRID_ID="nav:form:T_data" py tmp/scripts/preflight_grid_locator.py
Optional:
    EXPECT_GO=true|false   # assert GO presence too (default: just report it)

Credentials from env (EC_USER/EC_PASS, default sysadmin/sysadmin) -- never hardcoded (R16).
ASCII-only (R20).
"""
from playwright.sync_api import sync_playwright
import os, sys

EC_URL  = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER = os.environ.get('EC_USER', 'sysadmin')
EC_PASS = os.environ.get('EC_PASS', 'sysadmin')
SCREEN  = os.environ.get('SCREEN')
GRID_ID = os.environ.get('GRID_ID')
EXPECT_GO = os.environ.get('EXPECT_GO')  # 'true' / 'false' / None

if not SCREEN or not GRID_ID:
    print("USAGE: SCREEN=\"<name>\" GRID_ID=\"<tbody id>\" py tmp/scripts/preflight_grid_locator.py")
    sys.exit(2)


def wait_ajax(pg, t=15000):
    pg.wait_for_load_state('networkidle', timeout=t)
    pg.wait_for_timeout(1000)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    pg = b.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080}).new_page()
    pg.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username', EC_USER); pg.fill('#password', EC_PASS); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wait_ajax(pg)
    si = pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible', timeout=10000)
    si.clear(); si.type(SCREEN, delay=60); pg.wait_for_load_state('networkidle', timeout=8000); pg.wait_for_timeout(400)
    pg.locator(
        f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']"
    ).first.click()
    wait_ajax(pg)

    found = pg.evaluate("(gid) => !!document.getElementById(gid)", GRID_ID)
    all_grids = pg.evaluate("""() => Array.from(document.querySelectorAll("tbody[id$='_data']")).map(e => e.id)""")
    go_present = pg.evaluate("""() => { const g = document.getElementById('button:form:B'); return !!(g && g.offsetParent !== null); }""")
    b.close()

print(f"SCREEN     : {SCREEN}")
print(f"GRID_ID    : {GRID_ID}")
print(f"GO button  : {'present' if go_present else 'ABSENT (custom-URL OV -> reload via toolbar Refresh)'}")
print(f"grids live : {all_grids}")

ok = True
if not found:
    print("\nX FAIL -- declared GRID_ID NOT found in the live DOM.")
    print("  You likely carried a grid id from a SIBLING screen. Use the real one from the list above")
    print("  (an OV list grid is the `...:T_data` that is NOT a sub-tab like daytimes/versions).")
    ok = False
else:
    print("\nOK -- declared GRID_ID resolves on the live screen.")

if EXPECT_GO is not None:
    want = EXPECT_GO.strip().lower() == 'true'
    if want != go_present:
        print(f"X FAIL -- GO expectation mismatch: EXPECT_GO={EXPECT_GO} but live GO {'present' if go_present else 'absent'}.")
        print("  manage-object OV has a GO button; custom-URL OV does not (T2 Save And Refresh List handles both).")
        ok = False
    else:
        print(f"OK -- GO presence matches EXPECT_GO={EXPECT_GO}.")

print("\nRESULT:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
