from playwright.sync_api import sync_playwright
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':',r'\:')
BASE='tab:tabPanel:calc_group_conn_table:form:T:'
def rows(pg):
    out=[]
    for r in range(8):
        loc=pg.locator(cell(BASE+str(r)+':C0_da_input'))
        if loc.count()==0: break
        out.append((r, loc.input_value().strip()))
    return out
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    say("before: "+str(rows(pg)))
    # robust insert: try up to 3x
    added=False
    for attempt in range(3):
        ins=pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]")
        for i in range(ins.count()):
            if ins.nth(i).is_visible(): ins.nth(i).click(); break
        pg.wait_for_timeout(1300)
        ji=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Calculation Job']]")
        hit=False
        for i in range(ji.count()):
            if ji.nth(i).is_visible(): ji.nth(i).click(); hit=True; break
        if hit: added=True; say("insert ok on attempt "+str(attempt+1)); break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(600)
    if not added: say("INSERT FAILED after retries"); raise SystemExit
    pg.wait_for_timeout(1500)
    rr=rows(pg); say("after insert: "+str(rr))
    empt=[r for r,v in rr if not v]
    if not empt: say("no empty row?? abort"); raise SystemExit
    t=empt[0]; say("filling empty row index "+str(t))
    P=BASE+str(t)
    pg.locator(cell(P+':C0_da_input')).fill('2011-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell(P+':C2_dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='"+P+":C2_dd_panel']//tr[normalize-space(@data-item-label)='AUTOTEST Calc Test']").first.click()
    pg.wait_for_timeout(700)
    rr2=rows(pg); say("after fill: "+str(rr2))
    say("empty rows remaining: "+str([r for r,v in rr2 if not v]))
    pg.screenshot(path="C:/tmp/step_addfill.png", full_page=True); say("SHOT step_addfill - NOT saved yet")
