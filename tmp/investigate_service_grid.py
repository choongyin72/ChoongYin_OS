"""Deeper investigation: select_row() reported False for AUTOTEST_R5_SV under TS3 BU1 scope even
though the DB confirms the row exists. Dump the grid's real state (row count, pager, exact row
texts) to find out whether it's a pagination-reach issue, a stale-grid issue, or something else -
no guessing."""
import sys
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

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]

    info = page.evaluate(
        """(gid) => { const tb = document.getElementById(gid); if (!tb) return null;
            const rows = Array.from(tb.querySelectorAll('tr[data-ri]'));
            return { count: rows.length, texts: rows.map(r => r.textContent.trim().slice(0, 80)) }; }""",
        grid_id,
    )
    print("grid_id:", grid_id)
    print("visible rows on page 1:", info["count"] if info else None)
    if info:
        for t in info["texts"]:
            print("  ROW:", repr(t))

    pager = page.evaluate(
        """(gid) => { const wrap = document.getElementById(gid).closest('.ui-datatable, .ui-paginator, table')?.parentElement;
            const next = document.querySelector('[id*="paginator"] .ui-paginator-next, .ui-paginator-next');
            return { hasNext: !!next, nextDisabled: next ? next.className.includes('ui-state-disabled') : null }; }""",
        grid_id,
    )
    print("pager:", pager)

    print("DB says present:", db.code_present("ov_service", CODE))
    b.close()
