from playwright.sync_api import sync_playwright
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':',r'\:')
B0='tab:tabPanel:calc_group_conn_table:form:T:0'
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    # re-select row 0 (AUTOTEST)
    pg.locator(cell(B0+':C0_da_input')).click(); pg.wait_for_timeout(400); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    deleted=False
    for attempt in range(3):
        dl=pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-delete')]]")
        for i in range(dl.count()):
            if dl.nth(i).is_visible(): dl.nth(i).click(); break
        pg.wait_for_timeout(1200)
        ji=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Calculation Job']]")
        hit=False
        for i in range(ji.count()):
            if ji.nth(i).is_visible(): ji.nth(i).click(); hit=True; break
        if hit: deleted=True; say("delete submenu clicked on attempt "+str(attempt+1)); break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
    if not deleted: say("delete submenu never appeared"); 
    pg.wait_for_timeout(1200)
    yn=pg.get_by_role("button", name="Yes")
    if yn.count()>0 and yn.first.is_visible(): yn.first.click(); say("confirmed Yes"); pg.wait_for_timeout(800)
    pg.screenshot(path="C:/tmp/del_after2.png", full_page=True)
    n=0
    for r in range(8):
        if pg.locator(cell('tab:tabPanel:calc_group_conn_table:form:T:'+str(r)+':C0_da_input')).count()==0: break
        n+=1
    say("rows remaining: "+str(n)+" (expect 2 if AUTOTEST removed)")
