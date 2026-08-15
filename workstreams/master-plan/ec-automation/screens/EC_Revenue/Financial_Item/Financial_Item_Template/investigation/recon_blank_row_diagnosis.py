"""Read-only-ish recon: click Insert on Financial Item Template, dump every row's cells to see
where the new blank row actually lands, before fixing the driver's row-resolution logic."""
import sys

sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
from engine import Engine, open_screen  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=150, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    open_screen(page, "Financial Item Template")
    eng = Engine(page, "Financial Item Template")

    grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
    grid_id = grids[0]
    print("grid_id:", grid_id)

    eng.toolbar("Template", icon="insert")
    page.wait_for_timeout(1500)

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
    for r in rows:
        print(r)

    page.wait_for_timeout(3000)
    b.close()
