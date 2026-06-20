"""Deep recon of the 'Alarms' event-log insert row (EC Production > Production Operations > Event > Alarms).
Gated inline grid (PU/Area/Facility cascade + GO). Maps grid headers + EVERY cell in the blank Insert row
(id / tag / type / yellow-mandatory) so the build knows Time/Area/Type-of-Alarm/Reason/Report cell kinds.
READ-ONLY (nothing saved). py -X utf8 tmp/scripts/recon_alarms_row.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")
YELLOW = "rgb(252, 249, 192)"


def esc(i):
    return "#" + i.replace(":", "\\:")


def ajax(page, t=20000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", USER); page.fill("#password", PWD); page.click("#kc-login")
    page.wait_for_selector(esc("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Alarms", delay=45); ajax(page, 7000)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Alarms']").first.click(); ajax(page)
    mm = page.locator(esc("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible(): mm.first.click(); ajax(page)

    # fill the 3 mandatory cascade dds (first option) in order + GO
    for g in ("G:1", "G:2", "G:3"):
        ddp = f"nav:form:{g}:R:1:C:0:dd"
        try:
            page.locator(esc(ddp + "_button")).first.click(); page.wait_for_timeout(900)
            opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]").first
            opt.wait_for(state="visible", timeout=6000)
            print(f"  {g} <- {opt.get_attribute('data-item-label')}")
            opt.click(); ajax(page, 12000)
        except Exception as e:
            print(f"  {g} err: {str(e)[:60]}")
    page.locator(esc("button:form:B")).first.click(); ajax(page, 20000)

    # grid headers
    heads = page.evaluate("""() => [...document.querySelectorAll("[id^='alarms:form'] th, #alarms\\\\:form th")]
        .map(t=>(t.innerText||'').trim()).filter(Boolean).slice(0,12)""")
    print("\nGRID HEADERS:", heads)

    # click Insert (inline new row)
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(900)
    links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(links.count()):
        if links.nth(i).is_visible():
            print("  insert submenu ->", (links.nth(i).text_content(timeout=800) or "").strip())
            links.nth(i).click(); break
    ajax(page)

    # dump EVERY field in the blank row 0 (any input/select with id containing alarms:form:T:0:C)
    cells = page.evaluate("""(Y) => [...document.querySelectorAll("[id*='alarms:form:T:0:C'], [id*='alarms:form:T:0:c']")]
        .filter(e=>['INPUT','SELECT','TEXTAREA'].includes(e.tagName) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor===Y;
            return {id:e.id, tag:e.tagName, type:e.type||'', yellow:y}; })""", YELLOW)
    print("\nBLANK INSERT ROW cells (id | tag/type | yellow=mandatory):")
    for c in cells:
        suffix = c["id"].split(":")[-1]
        print(f"   {suffix:18s} {c['tag']:8s} {c['type']:8s} yellow={c['yellow']}   ({c['id']})")
    page.screenshot(path="tmp/recon_alarms_insert.png", full_page=False)
    b.close()
print("\nDONE (read-only).")
