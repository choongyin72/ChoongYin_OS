"""B-Step3 (act, HEADED): add AUTOTEST_CALC_TEST as a Calculation Job on P1_DAY_ALLOC. Insert>'Calculation Job'
-> SCAN new row -> set Start Date + pick the calc in the Calculation Job dd -> Save. Guards: abort if unclear. Reversible (Step 5)."""
from playwright.sync_api import sync_playwright
import os, re
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS=os.path.join(os.path.dirname(__file__),'..','evidence'); HEADED=os.environ.get('EC_HEADED','1')=='1'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
def cell(s): return '#'+s.replace(':',r'\:')
GRID='tab:tabPanel:calc_group_conn_table:form:T'
with sync_playwright() as p:
    b=p.chromium.launch(headless=not HEADED, slow_mo=300 if HEADED else 0, args=['--ignore-certificate-errors','--start-maximized'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=HEADED, viewport=None if HEADED else {'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Calculation Group Setup',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Calculation Group Setup']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).click(); pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(700)
    pg.locator(cell('nav:form:G:0:R:1:C:1:dd_button')).click(); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[@id='nav:form:G:0:R:1:C:1:dd_panel']//tr[normalize-space(@data-item-label)='Allocation Network Calculation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator("xpath=//tbody[@id='nav_model:form:T_data']//tr[.//input[@value='P1_DAY_ALLOC'] or .//*[contains(text(),'P1_DAY_ALLOC')]]").first.click(); wa(pg)
    pg.locator("xpath=//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'job connection')]").first.click(); wa(pg)
    # Insert -> Calculation Job
    pg.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first.hover(); pg.wait_for_timeout(1000)
    cj=pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Calculation Job']")
    print("Insert>Calculation Job (visible):", cj.count())
    if cj.count()==0: print("ABORT: Calculation Job insert item not visible after hover"); 
    else:
        cj.first.click(); wa(pg)
        # SCAN the new row cells
        row=pg.evaluate("""(G)=>{const out=[];for(let c=0;c<5;c++){const e=document.getElementById(`${G}:0:C${c}_da_input`)||document.getElementById(`${G}:0:C${c}_in`)||document.getElementById(`${G}:0:C${c}:dd_button`)||document.querySelector(`[id^='${G}:0:C${c}'][id$='dd_button']`)||document.getElementById(`${G}:0:C${c}_cb`); out.push({c, id:e?e.id:'(none)', tag:e?e.tagName:''});}return out;}""", GRID)
        print("new job row cells:"); [print("   ",r) for r in row]
        # Start Date = C0 da_input
        sd=cell(f'{GRID}:0:C0_da_input')
        if pg.locator(sd).count()>0:
            pg.locator(sd).click(); pg.locator(sd).fill('2011-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
        # Calculation Job dd = C2 (scan options for AUTOTEST)
        ddb=pg.locator(f"xpath=//*[starts-with(@id,'{GRID}:0:C2')][contains(@id,'dd_button')]")
        print("job dd button count:",ddb.count())
        if ddb.count()>0:
            ddb.first.click(); pg.wait_for_timeout(1000)
            opts=pg.evaluate("""()=>[...document.querySelectorAll("[id$='dd_panel'] tr")].map(t=>t.getAttribute('data-item-label')).filter(x=>x&&/autotest/i.test(x))""")
            print("job dd AUTOTEST options:",opts)
            if opts:
                pg.locator(f"xpath=//*[contains(@id,'dd_panel')]//tr[normalize-space(@data-item-label)='{opts[0]}']").first.click(); wa(pg)
                sv=pg.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
                if sv.count()>0: sv.first.click()
                else: pg.keyboard.press('Control+s')
                wa(pg); pg.screenshot(path=os.path.join(SS,'buildB_09_jobadded.png')); print("RESULT: job connection added + saved")
            else: print("ABORT: AUTOTEST not in Calculation Job dd")
        else: print("ABORT: Calculation Job dd not found in new row")
    if HEADED: pg.wait_for_timeout(3000)
    b.close()
