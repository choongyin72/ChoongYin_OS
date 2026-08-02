"""Crack the SCC grid: select group -> select product -> SCC tab -> Insert 'Stream Calculation
Category' -> dump blank cells + category dd + comment cell. READ-ONLY (no Save)."""
import os
from playwright.sync_api import sync_playwright
EC_URL=os.environ.get("EC_URL","https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
TOP="nav:form:T_data"; MID="prod_group_setup:form:T_data"
SCC="product_group_sub:tabPanel:strm_calc_cat:form:T_data"; TAB2="product_group_sub:tabPanel:tab2_header"
def _css(f): return "#"+f.replace(":","\:")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1800,"height":1000}).new_page(); pg.set_default_timeout(30000)
    def ajax(t=18000):
        try: pg.wait_for_load_state("networkidle",timeout=t)
        except Exception: pass
        pg.wait_for_timeout(1100)
    def cells(g):
        base=g.replace("_data","")
        return pg.evaluate("""(b)=>{const o=[];document.querySelectorAll('[id^="'+b+':"]').forEach(e=>{if(e.tagName!=='INPUT'||e.type==='hidden')return;const m=e.id.match(/T:(\d+):C(\d+)/);if(!m)return;o.push(e.id);});return o;}""",base)
    pg.goto(EC_URL,wait_until="domcontentloaded",timeout=40000)
    pg.fill("#username", os.environ.get("EC_USER", "sysadmin")); pg.fill("#password", os.environ.get("EC_PASS", "sysadmin")); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**",timeout=60000); ajax()
    si=pg.locator('#menu\:searchForm\:searchTxt'); si.wait_for(state="visible",timeout=15000)
    si.clear(); si.type("Product Group Setup",delay=40); pg.wait_for_load_state("networkidle",timeout=10000); pg.wait_for_timeout(500)
    pg.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Product Group Setup']").first.click(); ajax()
    pg.locator(f"xpath=//*[@id='{TOP}']//tr[.//*[normalize-space(text())='ALL_GENERAL']]").first.click()
    for _ in range(12):
        if cells(MID): break
        pg.wait_for_timeout(1000)
    ajax()
    pg.locator(_css(MID.replace("_data","")+":0:C0_da_input")).first.click(); pg.wait_for_timeout(1000)
    print("clicked product row; activating SCC tab")
    pg.locator(_css(TAB2)).first.click(); ajax()
    # hover Insert, click Stream Calculation Category
    pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(1200)
    try:
        pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Stream Calculation Category']").first.click(timeout=12000); ajax()
        sc=cells(SCC); print("SCC blank cells:",sc)
        cdd=next((c for c in sc if c.endswith("dd_input")),None)
        if cdd:
            ddp=cdd[:-6]
            pg.locator(_css(ddp+"_button")).first.click(); pg.wait_for_timeout(800)
            o=pg.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
            print("SCC category dd:",cdd,"opts:",[o.nth(i).get_attribute("data-item-label").strip() for i in range(min(o.count(),10))])
    except Exception as e: print("SCC insert err",str(e)[:90])
    b.close()
print("DONE")
