"""Read-only recon: open Financial Item Definition and Financial Item Template, capture their
real treeview menu path (breadcrumb / tv-link tooltip) and re-confirm field_inventory() output,
before building their missing screen bundles. No Save, no data entered."""
import sys
import json

sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
from engine import Engine, open_screen  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

SCREENS = ["Financial Item Definition", "Financial Item Template"]

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=150, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    for screen in SCREENS:
        print(f"\n=== {screen} ===")
        open_screen(page, screen)
        eng = Engine(page, screen)

        # Breadcrumb / path: check the treeview panel for the currently-highlighted/expanded path
        path = page.evaluate("""() => {
            const active = document.querySelector('.ui-treenode-selected, .tv-link.active, [aria-selected="true"]');
            if (active) {
                let parts = [];
                let node = active.closest('li');
                while (node) {
                    const label = node.querySelector(':scope > .ui-treenode-content .ui-treenode-label, :scope > .ui-treenode-content');
                    if (label) parts.unshift(label.textContent.trim());
                    node = node.parentElement ? node.parentElement.closest('li') : null;
                }
                return parts.join(' > ');
            }
            return null;
        }""")
        print("Breadcrumb attempt:", path)

        # Title shown top-right of the screen (often the real screen name)
        title = page.evaluate("""() => {
            const el = document.querySelector('[id$="screenTitle"], .screen-title, h1, h2');
            return el ? el.textContent.trim() : null;
        }""")
        print("Screen title element:", title)

        grids = page.evaluate("""() => Array.from(document.querySelectorAll('[id$=":T_data"]')).map(e => e.id)""")
        print("Grid ids found:", grids)

        inv = eng.field_inventory(grid_id=grids[0] if grids else None)
        print(json.dumps(inv, indent=2))

    page.wait_for_timeout(3000)
    b.close()
