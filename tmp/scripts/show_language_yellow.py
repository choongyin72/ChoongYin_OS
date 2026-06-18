"""Read-only: show WHY the scanner missed Language's mandatory yellow cell. Captures the grid in two
states - (A) existing saved rows, (B) after Insert -> a fresh blank row - and prints each row's cell
background colour. Existing rows = white; the new insert row's mandatory PK cell = yellow. NOTHING saved
(browser closes without Save). Usage: EC_HEADED=1 py tmp/scripts/show_language_yellow.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
OUT = "tmp/lang_yellow"
os.makedirs(OUT, exist_ok=True)


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def cell_colours(page, tag):
    """bg colour of every grid input cell, grouped by row, so we can SEE white vs yellow."""
    return page.evaluate("""() => {
        const out=[];
        document.querySelectorAll("[id^='table:form:T:'][id$='_in']").forEach(e=>{
            const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return;
            out.push({row:+m[1], col:+m[2], val:e.value, bg:getComputedStyle(e).backgroundColor});
        });
        return out; }""")


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1700, "height": 950}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector("#menu\\:searchForm\\:searchTxt", timeout=60000); ajax(page)
    box = page.locator("#menu\\:searchForm\\:searchTxt"); box.click(); box.fill(""); box.type("Language", delay=45); ajax(page, 7000)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Language']").first.click()
    ajax(page)
    mm = page.locator("#screenToolbar\\:form\\:minmaxMenu")
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)

    # STATE A - existing saved rows
    page.screenshot(path=f"{OUT}/A_existing_rows.png")
    print("STATE A (existing saved rows) - cell background colours:")
    for c in cell_colours(page, "A")[:6]:
        print(f"   row{c['row']} col{c['col']}  val={c['val']!r:12s} bg={c['bg']}")

    # STATE B - click Insert submenu -> the screen-label item -> a fresh BLANK row
    try:
        page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
        page.wait_for_timeout(900)
        links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        clicked = False
        for i in range(links.count()):
            if links.nth(i).is_visible():
                txt = (links.nth(i).text_content(timeout=800) or "").strip()
                if txt:  # the TV insert child is labelled with the screen name
                    links.nth(i).click(); clicked = True; break
        ajax(page)
        page.screenshot(path=f"{OUT}/B_after_insert_blank_row.png")
        print(f"\nSTATE B (after Insert -> new blank row; clicked={clicked}) - cell background colours:")
        rows = {}
        for c in cell_colours(page, "B"):
            rows.setdefault(c['row'], []).append(c)
        for r in sorted(rows)[:4]:
            for c in rows[r]:
                yel = "  <-- YELLOW (mandatory)" if c['bg'] == "rgb(252, 249, 192)" else ""
                print(f"   row{c['row']} col{c['col']}  val={c['val']!r:12s} bg={c['bg']}{yel}")
    except Exception as e:
        print("  insert-row capture err:", str(e)[:90])

    b.close()
print(f"\nDONE (read-only; NOT saved). Screenshots in {OUT}/")
