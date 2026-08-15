"""Read-only: open Financial Item Definition, click New Object, capture the INSERT-context
field_inventory (mandatory flags only render correctly on an empty/pristine form). No Save."""
import sys
import json

sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
from engine import Engine, open_screen  # noqa: E402
from universal_classifier import EC_URL  # noqa: E402
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=150, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    open_screen(page, "Financial Item Definition")
    eng = Engine(page, "Financial Item Definition")

    eng.toolbar("New Object")
    page.wait_for_timeout(1000)
    print(json.dumps(eng.field_inventory(), indent=2))

    page.wait_for_timeout(2000)
    b.close()
