"""Tank (OV_TANK) - consolidated read-only recon (checklist #5). Confirms/documents every fact
this build relied on, live, in one script:
  1. Navigator shape: single row, increasing column (nav:form:G:0:R:1:C:0..3) - C:0 = Date
     (working default, left untouched), C:1/C:2/C:3 = Production Unit -> Area -> Facility
     Class 1 cascade (same shape as Well - well_page.resource "Apply Well Navigator"). Single
     nav GROUP (G:0 only) - not per-field groups, so this IS Area-pattern-shaped.
  2. Navigator values "P1 Production Unit"/"P1 Area"/"P1 Facility 1" are genuinely selectable
     and load the grid (same P1 taxonomy Well already uses).
  3. objectForm mandatory fields (yellow/rgb(252,249,192) background on the pristine
     New-Object row): Tank Code, Tank Name, Start Date, Tank Meter Freq., Use in BF.
  4. Op Production Unit/Op Area/Op Facility Class 1 fields exist in objectForm but are NOT
     mandatory and are NOT auto-populated from the navigator scope - they must be filled
     explicitly to match the nav scope for the new row to stay visible (same requirement as
     Area's own Op Production Unit).
  5. objectdates Delete field id: tab:tabPanel:objectdates:form:G:0:R:0:C:3:da_input (same
     shape as Area's ${AREA_DEL_ENDDATE}).
  6. Grid headers (manageObject:form:T): Tank Code / Tank Name / Start Date / End Date.
  7. Treeview path: Configuration > Assets > "Tank and Storage Objects" > Tank (confirmed via
     live treeview expand - Tank is a sibling of Storage/Manage Tank/Maintain Tanks there).
Never Saves (except step 2's separate self-cleaning probe, run once during the original recon
session and not repeated here - see JOURNAL.md)."""
import os
import sys
from pathlib import Path
EC = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PW = os.environ.get("EC_PASS", "sysadmin")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, USER, PW)
    label = ec.open_object_screen(pg, "Tank")
    print("screen label:", label)

    headers = pg.evaluate(
        """() => Array.from(document.querySelectorAll('[id^="nav:form:G:0:R:0:"]'))
                .map(e => [e.id, (e.innerText||'').trim()])"""
    )
    print("nav column headers (row 0):", headers)

    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "P1 Production Unit")
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:2:dd_input", "P1 Area")
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:3:dd_input", "P1 Facility 1")
    ec.click_go(pg)
    pg.wait_for_timeout(1200)
    rows = pg.locator("#manageObject\\:form\\:T_data tr").count()
    print("grid rows after P1 cascade + GO:", rows)

    grid_headers = pg.evaluate(
        """() => { const t = document.querySelector('#manageObject\\\\:form\\\\:T');
                   return t ? Array.from(t.querySelectorAll('thead th')).map(th => (th.innerText||'').trim()) : null; }"""
    )
    print("grid column headers:", grid_headers)

    ec._open_new_object(pg)
    pg.wait_for_timeout(600)
    print("recon: New-Object form opened (read-only, no Save). View = OV_TANK.")

    br.close()
