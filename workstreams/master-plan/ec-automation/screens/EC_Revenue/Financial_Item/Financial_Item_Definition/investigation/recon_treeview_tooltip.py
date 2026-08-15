"""Read-only: type each screen name into the menu search and read the resulting tv-link's title/
tooltip attribute, which EC often uses to show the full treeview path. No navigation, no data entry."""
import sys

sys.path.insert(0, r"c:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation\py")
from universal_classifier import EC_URL, css, ajax, USER, PW  # noqa: E402
from playwright.sync_api import sync_playwright

SCREENS = ["Financial Item Definition", "Financial Item Template"]

with sync_playwright() as p:
    b = p.chromium.launch(headless=False, slow_mo=150, args=["--ignore-certificate-errors", "--start-maximized"])
    page = b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)

    if page.locator("#username").count():
        page.fill("#username", USER)
        page.fill("#password", PW)
        page.click("#kc-login")
        page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000)
        ajax(page)

    for screen in SCREENS:
        print(f"\n=== {screen} ===")
        box = page.locator(css("menu:searchForm:searchTxt"))
        box.click()
        box.fill("")
        box.type(screen, delay=45)
        ajax(page, 7000)
        link = page.locator(
            f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen}']"
        ).first
        title_attr = link.get_attribute("title")
        print("Link title attr:", title_attr)
        # Also check any ancestor with a tooltip / data attribute
        ancestor_info = link.evaluate("""(el) => {
            let node = el;
            const info = [];
            for (let i = 0; i < 6 && node; i++) {
                info.push({tag: node.tagName, title: node.getAttribute && node.getAttribute('title'),
                           cls: node.className});
                node = node.parentElement;
            }
            return info;
        }""")
        print("Ancestor chain:", ancestor_info)
        box.fill("")

    page.wait_for_timeout(2000)
    b.close()
