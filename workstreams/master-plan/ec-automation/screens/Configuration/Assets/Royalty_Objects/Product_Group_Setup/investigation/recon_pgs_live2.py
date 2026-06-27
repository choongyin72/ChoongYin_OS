"""RC.0054 live recon v2 (READ-ONLY) - hardcoded ids from v1. Select a first-page group,
load the middle grid, map middle cells + Product dd (via a discardable Insert), then activate
COSTS + SCC tabs and map their grids + member dds + per-tab Insert enablement. No Save."""
from playwright.sync_api import sync_playwright
import os

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Product Group Setup"
GROUP = "ALL_GENERAL"   # first-page, loaded in DOM
TOP = "nav:form:T_data"
MID = "prod_group_setup:form:T_data"
COST = "product_group_sub:tabPanel:prod_group_cost:form:T_data"
TAB1 = "product_group_sub:tabPanel:tab1_header"   # COSTS
TAB2 = "product_group_sub:tabPanel:tab2_header"   # STREAM CALC CATEGORY
SS = r"C:\tmp\wt-pgs\tmp\screens"; os.makedirs(SS, exist_ok=True)


def _css(f): return "#" + f.replace(":", "\\:")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1800, "height": 1000}).new_page()
    pg.set_default_timeout(30000)

    def ajax(t=18000):
        try: pg.wait_for_load_state("networkidle", timeout=t)
        except Exception: pass
        pg.wait_for_timeout(1100)

    def row_cells(grid_id, limit=26):
        base = grid_id.replace("_data", "")
        return pg.evaluate("""(b) => { const out=[]; document.querySelectorAll('[id^="'+b+':"]').forEach(e=>{
            if(e.tagName!=='INPUT'||e.type==='hidden') return; const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return;
            out.push(e.id); }); return out; }""", base)[:limit]

    def grids():
        return pg.evaluate("""() => [...document.querySelectorAll("[id$=':T_data']")].map(t=>t.id)""")

    def insert_submenu():
        try:
            pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
            pg.wait_for_timeout(900)
        except Exception: return []
        return pg.evaluate("""() => [...document.querySelectorAll("ul.ui-menu-child a")].filter(a=>a.offsetParent).map(a => {
            const li=a.closest('li'); return {label:(a.innerText||'').trim(),
              disabled:(li&&li.className.includes('ui-state-disabled'))||a.className.includes('ui-state-disabled')}; })""")

    def dd_opts(dd_input_id):
        ddp = dd_input_id[:-len("_input")]
        try:
            pg.locator(_css(ddp + "_button")).first.click(); pg.wait_for_timeout(800)
            o = pg.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
            vals = [o.nth(i).get_attribute("data-item-label").strip() for i in range(min(o.count(),12))]
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
            return vals
        except Exception as e: return ["ERR " + str(e)[:50]]

    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=40000)
    pg.fill("#username", "sysadmin"); pg.fill("#password", "sysadmin"); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax()
    si = pg.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state="visible", timeout=15000)
    si.clear(); si.type(SCREEN, delay=40); pg.wait_for_load_state("networkidle", timeout=10000); pg.wait_for_timeout(500)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click()
    ajax()

    print(f"=== select top group {GROUP} ===")
    pg.locator(f"xpath=//*[@id='{TOP}']//tr[.//*[normalize-space(text())='{GROUP}']]").first.click()
    # wait for middle grid to populate
    for _ in range(15):
        if len(row_cells(MID)) > 0: break
        pg.wait_for_timeout(1000)
    ajax()
    print("MIDDLE cells (existing rows):", row_cells(MID))
    print("INSERT submenu (middle active):")
    for s in insert_submenu(): print("   ", s)

    print("\n=== Insert > PRODUCT GROUP SETUP (discardable blank row) ===")
    try:
        pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(700)
        pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Product Group Setup']").first.click(); ajax()
        blank = row_cells(MID)
        print("MIDDLE blank-row cells:", blank)
        pdd = next((c for c in blank if c.endswith("dd_input")), None)
        print("Product dd cell:", pdd, "opts:", dd_opts(pdd) if pdd else "n/a")
    except Exception as e: print("   insert-setup err", str(e)[:70])

    # select a product row (existing) to scope the bottom tabs
    try:
        pg.locator(_css(MID.replace("_data","") + ":0:C0_in")).first.click(); pg.wait_for_timeout(900)
    except Exception:
        try: pg.locator(_css(MID.replace("_data","") + ":0:C0_da_input")).first.click(); pg.wait_for_timeout(900)
        except Exception as e: print("   midrow err", str(e)[:50])

    for tabid, name in ((TAB1, "COSTS"), (TAB2, "STREAM CALC CATEGORY")):
        print(f"\n=== activate tab {name} ({tabid}) ===")
        try:
            pg.locator(_css(tabid)).first.click(); ajax()
        except Exception as e:
            print("   tab err", str(e)[:60]); continue
        print("   grids now:", [g for g in grids() if g not in (TOP, MID)])
        print("   INSERT submenu:")
        for s in insert_submenu(): print("     ", s)
    pg.screenshot(path=SS+r"\pgs_recon2.png", full_page=True)
    b.close()
print("DONE (read-only)")
