"""Canonical Universal Screen Engine regression canary - Bank (OV) + Language (TV) full I-U-D.

MANDATORY pre-push gate for any change to engine.py or universal_classifier.py (same role R12
gives the shared T1/T2 canary for RF changes - see docs/lessons-learned.md). Bank and Language are
the two proven, simplest exemplars of each screen family the engine supports (OV manage-object,
TV inline-editable grid) - if a change to the engine breaks either of these, it is very likely to
break every other screen built on the same primitives.

Run before pushing any engine.py/universal_classifier.py change:
    EC_HEADED=0 py -X utf8 workstreams/master-plan/ec-automation/py/engine_canary.py
Exits 0 only if BOTH screens' full Insert->Update->Delete pass AND DB-verify 0 residual.
"""
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "libraries"))
from engine import Engine, open_screen, SaveFailed, css  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright
import DbVerify as db  # noqa: E402

HEADED = os.environ.get("EC_HEADED", "0") == "1"
results = {}


def canary_bank(page):
    """OV manage-object exemplar: New Object form, label-driven fill, row-select, End=Start delete."""
    code = "AUTOTEST_CANARY_BANK"
    name = "AUTOTEST Canary Bank"
    name_upd = name + " UPDATED"
    start_date = "2000-01-01"

    open_screen(page, "Bank")
    eng = Engine(page, "Bank")

    eng.toolbar("New Object")
    page.wait_for_timeout(1000)
    eng.fill("Code", code)
    eng.fill("Name", name)
    eng.fill("Start Date", start_date)
    eng.click("Save")

    page.wait_for_timeout(1200)
    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    eng.select_row(grid_id, code)
    eng.fill("Name", name_upd)
    eng.click("Save")

    page.wait_for_timeout(1200)
    eng.select_row(grid_id, code)
    sd = eng._field("Start Date")
    sd_val = page.locator(css(sd["id"])).first.input_value()
    eng.fill("End Date", sd_val)
    eng.click("Save")

    page.wait_for_timeout(1200)
    present = db.code_present("ov_bank", code)
    return not present  # True = self-cleaned (deleted), as expected


def canary_language(page):
    """TV inline-grid exemplar: Insert flyout, blank-row resolution by both key cells empty,
    cell edit, physical delete."""
    code = "ZZ"
    name = "AUTOTEST Canary Language"
    name_upd = name + " UPDATED"

    open_screen(page, "Language")
    eng = Engine(page, "Language")

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]

    eng.toolbar("Language", icon="insert")
    page.wait_for_timeout(1000)
    rows = page.evaluate(
        """(gid) => { const tb = document.getElementById(gid);
        return Array.from(tb.querySelectorAll('tr[data-ri]')).map(tr => ({
            ri: parseInt(tr.getAttribute('data-ri'), 10),
            cells: Array.from(tr.querySelectorAll('td')).map(td => {
                const inp = td.querySelector('input'); return inp ? inp.value : td.textContent.trim();
            }),
        })); }""",
        grid_id,
    )
    row_idx = next(r["ri"] for r in rows if r["cells"][0] == "" and r["cells"][1] == "")
    eng.grid_cell(grid_id, row_idx, "Id").set("999")
    eng.grid_cell(grid_id, row_idx, "Language").set(code)
    eng.grid_cell(grid_id, row_idx, "Name").set(name)
    eng.click("Save")

    page.wait_for_timeout(1200)
    row_idx = eng.find_grid_row(grid_id, code)
    eng.grid_cell(grid_id, row_idx, "Name").set(name_upd)
    eng.click("Save")

    page.wait_for_timeout(1200)
    row_idx = eng.find_grid_row(grid_id, code)
    eng.select_grid_row(grid_id, code)
    eng.toolbar("Language", icon="delete")
    page.wait_for_timeout(1000)
    eng.click("Save")

    page.wait_for_timeout(1200)
    present = db.code_present("t_basis_language", code)
    return not present  # True = physically deleted, as expected


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, slow_mo=200 if HEADED else 0,
                           args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=HEADED).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    print("=== CANARY: Bank (OV) ===")
    try:
        results["bank"] = "PASS" if canary_bank(page) else "FAIL: not self-cleaned"
    except (SaveFailed, Exception) as e:
        results["bank"] = "FAIL: %s" % str(e)[:150]
    print(" ", results["bank"])

    print("=== CANARY: Language (TV) ===")
    try:
        results["language"] = "PASS" if canary_language(page) else "FAIL: not self-cleaned"
    except (SaveFailed, Exception) as e:
        results["language"] = "FAIL: %s" % str(e)[:150]
    print(" ", results["language"])

    if HEADED:
        page.wait_for_timeout(3000)
    b.close()

print("\n" + "=" * 40 + "\nRESULTS")
ok = all(v == "PASS" for v in results.values())
for k, v in results.items():
    print("  %s %-10s: %s" % ("OK" if v == "PASS" else "X", k, v))
print("Overall:", "ALL PASS" if ok else "FAILURES")
sys.exit(0 if ok else 1)
