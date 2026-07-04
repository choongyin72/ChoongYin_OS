"""RC.0054 recon v3 (READ-ONLY): map the COST + SCC blank-row cells + member dds.
Select group -> select a middle product row -> COSTS tab -> Insert Product Group Cost (dump
cells + Cost Type dd) -> SCC tab -> Insert Stream Calculation Category (dump cells + dd). No Save."""
from playwright.sync_api import sync_playwright
import os

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Product Group Setup"; GROUP = "ALL_GENERAL"
TOP = "nav:form:T_data"; MID = "prod_group_setup:form:T_data"
COST = "product_group_sub:tabPanel:prod_group_cost:form:T_data"
SCC = "product_group_sub:tabPanel:strm_calc_cat:form:T_data"
TAB1 = "product_group_sub:tabPanel:tab1_header"; TAB2 = "product_group_sub:tabPanel:tab2_header"


def _css(f): return "#" + f.replace(":", "\\:")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1800, "height": 1000}).new_page()
    pg.set_default_timeout(30000)

    def ajax(t=18000):
        try: pg.wait_for_load_state("networkidle", timeout=t)
        except Exception: pass
        pg.wait_for_timeout(1100)

    def cells(grid):
        base = grid.replace("_data", "")
        return pg.evaluate("""(b)=>{const o=[];document.querySelectorAll('[id^="'+b+':"]').forEach(e=>{
            if(e.tagName!=='INPUT'||e.type==='hidden')return;const m=e.id.match(/T:(\\d+):C(\\d+)/);if(!m)return;o.push(e.id);});return o;}""", base)

    def dd_opts(dd_input_id):
        ddp = dd_input_id[:-len("_input")]
        try:
            pg.locator(_css(ddp + "_button")).first.click(); pg.wait_for_timeout(800)
            o = pg.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
            v = [o.nth(i).get_attribute("data-item-label").strip() for i in range(min(o.count(),12))]
            pg.keyboard.press("Escape"); pg.wait_for_timeout(300); return v
        except Exception as e: return ["ERR " + str(e)[:40]]

    def insert(label):
        pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(700)
        pg.locator(f"xpath=//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='{label}']").first.click(); ajax()

    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=40000)
    pg.fill("#username", "sysadmin"); pg.fill("#password", "sysadmin"); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax()
    si = pg.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state="visible", timeout=15000)
    si.clear(); si.type(SCREEN, delay=40); pg.wait_for_load_state("networkidle", timeout=10000); pg.wait_for_timeout(500)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click(); ajax()
    pg.locator(f"xpath=//*[@id='{TOP}']//tr[.//*[normalize-space(text())='{GROUP}']]").first.click()
    for _ in range(12):
        if cells(MID): break
        pg.wait_for_timeout(1000)
    ajax()
    # select a middle product row
    try: pg.locator(_css(MID.replace("_data","") + ":0:C0_da_input")).first.click(); pg.wait_for_timeout(900)
    except Exception as e: print("midrow err", str(e)[:50])

    print("=== COSTS tab -> Insert Product Group Cost ===")
    try:
        pg.locator(_css(TAB1)).first.click(); ajax()
        insert("Product Group Cost")
        cc = cells(COST); print("COST blank cells:", cc)
        cdd = next((c for c in cc if c.endswith("dd_input")), None)
        print("COST first dd:", cdd, "opts:", dd_opts(cdd) if cdd else "n/a")
    except Exception as e: print("   cost err", str(e)[:80])

    print("\n=== SCC tab -> Insert Stream Calculation Category ===")
    try:
        pg.locator(_css(TAB2)).first.click(); ajax()
        insert("Stream Calculation Category")
        sc = cells(SCC); print("SCC blank cells:", sc)
        sdd = next((c for c in sc if c.endswith("dd_input")), None)
        print("SCC first dd:", sdd, "opts:", dd_opts(sdd) if sdd else "n/a")
    except Exception as e: print("   scc err", str(e)[:80])
    b.close()
print("DONE (read-only, nothing saved)")
