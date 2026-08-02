"""RC.0057 recon v2 (READ-ONLY): correct CASCADE nav = date + Unit Agreement 3 (G:1) ->
Tract TRACT_U3_T01 (G:2) -> GO, then inspect grid/insert/cells/perf-dd/delete. Local sandbox."""
from playwright.sync_api import sync_playwright
import os

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Tract - Well Setup"
UA = "Unit Agreement 3"; TRACT = "TRACT_U3_T01"
DATE_F = "nav:form:G:0:R:1:C:0:da_input"; UA_DD = "nav:form:G:1:R:1:C:0:dd"; TRACT_DD = "nav:form:G:2:R:1:C:0:dd"
SS = r"C:\tmp\wt-tws\tmp\screens"; os.makedirs(SS, exist_ok=True)


def ajax(pg, t=20000):
    try: pg.wait_for_load_state("networkidle", timeout=t)
    except Exception: pass
    pg.wait_for_timeout(900)


def _css(f): return "#" + f.replace(":", "\\:")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    pg.set_default_timeout(30000)
    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=40000)
    pg.fill("#username", os.environ.get("EC_USER", "sysadmin")); pg.fill("#password", os.environ.get("EC_PASS", "sysadmin")); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax(pg)
    si = pg.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state="visible", timeout=15000)
    si.clear(); si.type(SCREEN, delay=40); pg.wait_for_load_state("networkidle", timeout=10000); pg.wait_for_timeout(500)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click()
    ajax(pg)

    def select_dd(dd, v):
        it = f"xpath=//*[@id='{dd}_panel']//tr[normalize-space(@data-item-label)='{v}']"
        pg.locator(_css(dd + "_button")).first.click(); pg.locator(it).first.wait_for(state="visible", timeout=10000)
        pg.locator(it).first.click(); ajax(pg, 12000)

    pg.fill(_css(DATE_F), "2011-01-01"); pg.keyboard.press("Tab"); pg.wait_for_timeout(700)
    select_dd(UA_DD, UA)
    # now G:2 Tract dd should be populated - dump its options
    pg.locator(_css(TRACT_DD + "_button")).first.click(); pg.wait_for_timeout(700)
    topts = pg.locator(f"xpath=//*[@id='{TRACT_DD}_panel']//tr[@data-item-label]")
    print("TRACT DD options:", [topts.nth(i).get_attribute("data-item-label").strip() for i in range(min(topts.count(),8))])
    trow = pg.locator(f"xpath=//*[@id='{TRACT_DD}_panel']//tr[normalize-space(@data-item-label)='{TRACT}']").first
    (trow if trow.count() else topts.first).click(); ajax(pg, 12000)
    pg.locator(_css("button:form:B")).first.click(); ajax(pg)
    pg.screenshot(path=SS+r"\tws_recon2_navd.png", full_page=True)

    allt = pg.evaluate("""() => [...document.querySelectorAll("[id$=':T_data']")].map(x=>x.id)""")
    print("ALL :T_data grids:", allt)
    gid = next((t for t in allt if "well" in t.lower() or "setup" in t.lower()), allt[0] if allt else None)
    print("GRID id:", gid)

    ins = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert') or contains(@class,'ui-icon-add')]]")
    if ins.count():
        ins.first.hover(); pg.wait_for_timeout(900)
        subs = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        labels = [subs.nth(i).text_content(timeout=600).strip() for i in range(subs.count()) if subs.nth(i).is_visible()]
        print("INSERT submenu labels:", labels)
        for i in range(subs.count()):
            if subs.nth(i).is_visible(): subs.nth(i).click(); break
        ajax(pg)
        cells = pg.evaluate("""(gid) => { const out=[]; const base=gid.replace('_data','')+':';
            document.querySelectorAll('[id^="'+base+'"]').forEach(e=>{ if(e.tagName!=='INPUT'||e.type==='hidden') return;
              const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return; out.push(e.id); }); return out.slice(0,12); }""", gid)
        print("BLANK ROW cells:", cells)
        c2 = next((c for c in cells if ":C2_dd_input" in c), None)
        if c2:
            ddp2 = c2[:-len("_input")]
            try:
                pg.locator(_css(ddp2 + "_button")).first.click(); pg.wait_for_timeout(700)
                o2 = pg.locator(f"xpath=//*[@id='{ddp2}_panel']//tr[@data-item-label]")
                print("C2 perf dd options (first 15):", [o2.nth(i).get_attribute("data-item-label").strip() for i in range(min(o2.count(),15))])
            except Exception as e: print("   c2 err", str(e)[:60])

    dele = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
    if dele.count():
        dele.first.hover(); pg.wait_for_timeout(700)
        subs = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        print("DELETE submenu labels:", [subs.nth(i).text_content(timeout=500).strip() for i in range(subs.count()) if subs.nth(i).is_visible()])
    b.close()
print("DONE")
