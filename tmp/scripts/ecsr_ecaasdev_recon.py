"""ECSR-35331 read-only recon on the LIVE ECAASDEV web app. Logs in, opens 'Daily Gas Stream Status',
expands, and dumps the navigator fields + dropdown option labels (to read the exact PU/Area/Facility
values) + a screenshot. NO Save / NO writes. Usage: EC_HEADED=1 py tmp/scripts/ecsr_ecaasdev_recon.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = "https://dev.non-prod.plp.wde.ecaas.cloud/"
USER, PWD = "quorum", os.environ.get("EC_WEB_PWD","")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
OUT = "tmp/ecsr_recon"
os.makedirs(OUT, exist_ok=True)


def ajax(page, t=25000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(1200)


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)
    page.screenshot(path=f"{OUT}/01_landing.png")
    print("landing title:", page.title())

    # --- login (try Keycloak-style fields, fall back to generic) ---
    try:
        for u in ("#username", "input[name='username']", "#j_username"):
            if page.locator(u).count():
                page.fill(u, USER); break
        for pw in ("#password", "input[name='password']", "#j_password"):
            if page.locator(pw).count():
                page.fill(pw, PWD); break
        clicked = False
        for btn in ("#kc-login", "input[type='submit']", "button[type='submit']",
                    "xpath=//button[normalize-space()='LOG IN']", "xpath=//*[@value='LOG IN' or normalize-space(text())='LOG IN']"):
            loc = page.locator(btn)
            if loc.count():
                try:
                    loc.first.click(); clicked = True; break
                except Exception:
                    pass
        if not clicked:
            page.press("#password", "Enter")
        page.wait_for_timeout(4000); ajax(page)
    except Exception as e:
        print("login step note:", str(e)[:120])
    page.screenshot(path=f"{OUT}/02_after_login.png")
    print("after-login title:", page.title())

    # --- open the screen via the search box ---
    SCREEN = "Daily Gas Stream Status"
    try:
        box = None
        for s in ("#menu\\:searchForm\\:searchTxt", "input[id*='searchTxt']", "input[type='search']"):
            if page.locator(s).count():
                box = page.locator(s).first; break
        if box:
            box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 9000)
            link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']")
            if link.count():
                link.first.click(); ajax(page)
            else:
                print("screen link not found by exact text; search box value typed")
        else:
            print("search box not found")
    except Exception as e:
        print("open-screen note:", str(e)[:120])
    page.screenshot(path=f"{OUT}/03_screen_opened.png", full_page=True)

    # expand (hide treeview)
    mm = page.locator("#screenToolbar\\:form\\:minmaxMenu")
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    page.screenshot(path=f"{OUT}/04_expanded.png", full_page=True)

    # --- dump navigator fields + dropdown options ---
    nav = page.evaluate("""() => {
        const out = {fields: [], dropdowns: []};
        document.querySelectorAll("[id^='nav:form:G:']").forEach(e => {
            const m = e.id.match(/nav:form:(G:\\d+:R:\\d+:C:\\d+):(da_input|dd_input|in|_input)?/);
            if (e.tagName === 'INPUT' || e.tagName === 'SELECT')
                out.fields.push({id: e.id, val: e.value, ph: e.placeholder || ''});
        });
        // dropdown option panels currently in DOM
        document.querySelectorAll("[id*='_panel'] tr[data-item-label]").forEach(tr => {
            out.dropdowns.push({panel: tr.closest("[id*='_panel']")?.id, label: tr.getAttribute('data-item-label')});
        });
        return out; }""")
    print("\n=== navigator input fields ===")
    for f in nav["fields"][:25]:
        print(f"   {f['id']:55s} val={f['val']!r}  ph={f['ph']!r}")
    print("\n=== dropdown option labels currently loaded ===")
    for d in nav["dropdowns"][:40]:
        print(f"   {d['panel']}: {d['label']}")

    b.close()
print(f"\nDONE (read-only; no Save). Screenshots in {OUT}/")
