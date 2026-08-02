"""Find the MANDATORY (yellow) cells on Setup + Cost blank insert rows (silent-reject fix)."""
import os
from playwright.sync_api import sync_playwright
EC_URL=os.environ.get("EC_URL","https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
TOP="nav:form:T_data"; MID="prod_group_setup:form:T_data"
COST="product_group_sub:tabPanel:prod_group_cost:form:T_data"; TAB1="product_group_sub:tabPanel:tab1_header"
def _css(f): return "#"+f.replace(":","\:")
def yellow_cells(pg, grid):
    base=grid.replace("_data","")
    return pg.evaluate("""(b)=>{const Y=['rgb(255, 255, 204)','rgb(255, 255, 224)'];const o=[];
      document.querySelectorAll('[id^="'+b+':"]').forEach(e=>{if(!['INPUT','SELECT','TEXTAREA'].includes(e.tagName)||e.type==='hidden')return;
      const m=e.id.match(/T:(\d+):C(\d+)/);if(!m)return;const bg=getComputedStyle(e).backgroundColor;
      o.push({id:e.id.split(':').slice(-1)[0],mand:Y.includes(bg),bg});});return o.slice(0,14);}""",base)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1800,"height":1000}).new_page(); pg.set_default_timeout(30000)
    def ajax(t=16000):
        try: pg.wait_for_load_state("networkidle",timeout=t)
        except Exception: pass
        pg.wait_for_timeout(1000)
    def ins(label):
        pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(700)
        pg.locator(f"xpath=//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='{label}']").first.click(); ajax()
    pg.goto(EC_URL,wait_until="domcontentloaded",timeout=40000)
    pg.fill("#username", os.environ.get("EC_USER", "sysadmin")); pg.fill("#password", os.environ.get("EC_PASS", "sysadmin")); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**",timeout=60000); ajax()
    si=pg.locator('#menu\:searchForm\:searchTxt'); si.wait_for(state="visible",timeout=15000)
    si.clear(); si.type("Product Group Setup",delay=40); pg.wait_for_load_state("networkidle",timeout=10000); pg.wait_for_timeout(500)
    pg.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Product Group Setup']").first.click(); ajax()
    pg.locator(f"xpath=//*[@id='{TOP}']//tr[.//*[normalize-space(text())='ALL_GENERAL']]").first.click(); ajax()
    print("SETUP blank-row mandatory scan:")
    ins("Product Group Setup")
    for c in yellow_cells(pg, MID):
        if c['id'].startswith('C'): print("  ",c)
    # cost: select a product first
    pg.locator(_css(MID.replace("_data","")+":0:C2_in")).first.click(); pg.wait_for_timeout(900)
    pg.locator(_css(TAB1)).first.click(); ajax()
    print("COST blank-row mandatory scan:")
    ins("Product Group Cost")
    for c in yellow_cells(pg, COST):
        if c['id'].startswith('C'): print("  ",c)
    b.close()
