"""Stage A: create AUTOTEST_PROC_TEST (Process Diagram) -> Maintain Calc -> FLOWCHART -> Implement Step 1 as
Equations -> drill in -> EQUATIONS tab -> add equation row. Headed, CDP 9222, stays open for Stage B."""
from playwright.sync_api import sync_playwright
import os
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':', r'\:')
def wa(pg, t=20000): pg.wait_for_load_state('networkidle', timeout=t); pg.wait_for_timeout(1000)
def click_visible(pg, xp):
    loc=pg.locator(xp)
    for i in range(loc.count()):
        if loc.nth(i).is_visible(): loc.nth(i).click(); return True
    return False
def opensc(pg, name):
    s=pg.locator(r'#menu\:searchForm\:searchTxt'); s.click(); s.fill(''); s.type(name, delay=40); pg.wait_for_timeout(1400)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='"+name+"']").first.click(); wa(pg)
EC='https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
INS="xpath=//a[.//span[contains(@class,'ui-icon-insert')]]"
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, slow_mo=300, args=['--ignore-certificate-errors','--start-maximized','--remote-debugging-port=9222'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    pg.goto(EC, wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wa(pg); say("logged in")
    # 1) CREATE Process Diagram calc
    opensc(pg,'Create Calculation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(600)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    er=None
    for att in range(4):
        click_visible(pg, INS); pg.wait_for_timeout(1000)
        click_visible(pg, "xpath=//a[contains(@class,'ui-menuitem-link')][.//span[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'public calculation')]]")
        pg.wait_for_timeout(1200)
        for r in range(25):
            loc=pg.locator(cell('calculation:form:T:'+str(r)+':C0_in'))
            if loc.count()==0: continue
            if not loc.input_value().strip(): er=r; break
        if er is not None: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    if er is None: say("CREATE row failed"); pg.wait_for_timeout(3600000); b.close(); raise SystemExit
    R='calculation:form:T:'+str(er)
    pg.locator(cell(R+':C0_in')).fill('AUTOTEST_PROC_TEST'); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R+':C1_in')).fill('AUTOTEST Proc Test'); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R+':C2_da_input')).fill('2000-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell(R+':C4_dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='"+R+":C4_dd_panel']//tr[normalize-space(@data-item-label)='Day']").first.click(); pg.wait_for_timeout(500)
    pg.locator(cell(R+':C5_dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='"+R+":C5_dd_panel']//tr[normalize-space(@data-item-label)='Process Diagram']").first.click(); pg.wait_for_timeout(500)
    pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").first.click(); wa(pg); pg.wait_for_timeout(1200)
    say("created AUTOTEST_PROC_TEST (Process Diagram)")
    # 2) MAINTAIN CALCULATION -> flowchart
    opensc(pg,'Maintain Calculation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(600)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='AUTOTEST Proc Test']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg); say("maintain calc loaded")
    click_visible(pg, "xpath=//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'flowch')]"); wa(pg)
    # 3) right-click Step 1 -> Implement as -> Equations -> Save (retry)
    impl=False
    for att in range(3):
        pg.mouse.click(1080,577); pg.wait_for_timeout(400)
        pg.mouse.click(1080,577,button='right'); pg.wait_for_timeout(1000)
        ia=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[contains(normalize-space(.),'Implement as')]]")
        hovered=False
        for i in range(ia.count()):
            if ia.nth(i).is_visible(): ia.nth(i).hover(); hovered=True; break
        if hovered:
            pg.wait_for_timeout(800)
            eq=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Equations']]")
            for i in range(eq.count()):
                if eq.nth(i).is_visible(): eq.nth(i).click(); impl=True; break
        if impl: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    pg.wait_for_timeout(1000)
    if impl:
        pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]").first.click(); wa(pg); pg.wait_for_timeout(1200)
    say("Implement Step 1 as Equations: "+str(impl))
    # 4) drill in
    pg.mouse.dblclick(1080,577); wa(pg)
    # 5) add equation row: + -> EQUATIONS (retry)
    BASE='maintab:tabPanel:equations:form:T:0'
    added=False
    for att in range(4):
        click_visible(pg, INS); pg.wait_for_timeout(1000)
        em=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='EQUATIONS']]")
        for i in range(em.count()):
            if em.nth(i).is_visible(): em.nth(i).hover(); pg.wait_for_timeout(300); em.nth(i).click(); break
        pg.wait_for_timeout(1800)
        if pg.locator(cell(BASE+':C5_b')).count()>0: added=True; break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
    say("equation row added: "+str(added))
    pg.screenshot(path="C:/tmp/stageA.png", full_page=True); say("SHOT stageA - staying open (CDP 9222)")
    pg.wait_for_timeout(3600000)
    b.close()
