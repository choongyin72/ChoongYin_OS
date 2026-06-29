"""LIVE DEMO (headed): full self-authored-calc cycle - create Process Diagram -> implement Step 1 as Equations
-> author INFO='...' in the editor -> connect -> Simulate-run -> self-clean. DB-verifies each phase. Reuses
every gesture proven on 2026-06-29 (incl. the canvas-coordinate editor nav + case-insensitive menu fix)."""
from playwright.sync_api import sync_playwright
import os, re, oracledb
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':', r'\:')
def wa(pg, t=20000): pg.wait_for_load_state('networkidle', timeout=t); pg.wait_for_timeout(1000)
def killpanels(pg): pg.evaluate("() => { var ps=document.querySelectorAll('.ui-autocomplete-panel,.ui-input-overlay'); for(var i=0;i<ps.length;i++){ps[i].style.display='none';} }")
def clickvis(pg, xp):
    loc=pg.locator(xp)
    for i in range(loc.count()):
        if loc.nth(i).is_visible(): loc.nth(i).click(); return True
    return False
def opensc(pg, name):
    s=pg.locator(r'#menu\:searchForm\:searchTxt'); s.click(); s.fill(''); s.type(name, delay=35); pg.wait_for_timeout(1300)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='"+name+"']").first.click(); wa(pg)
def db():
    return oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
def q1(sql):
    c=db();cur=c.cursor();cur.execute(sql);v=cur.fetchone()[0];c.close();return v
INS="xpath=//a[.//span[contains(@class,'ui-icon-insert')]]"
DEL="xpath=//a[.//span[contains(@class,'ui-icon-delete')]]"
SAVE="xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"
CODE='AUTOTEST_DEMO'; NAME='AUTOTEST Demo'; MSG='AUTOTEST DEMO equation'
CONN='tab:tabPanel:calc_group_conn_table:form:T:'
# JS: case-insensitive click of a menu leaf inside the insert submenu (the casing fix)
def menu_click(pg, label, marker1, marker2):
    js="""(a) => { var all=[].slice.call(document.querySelectorAll('*')); var menu=null;
      for(var i=0;i<all.length;i++){ var tx=(all[i].textContent||''); if(tx.indexOf(a.m1)>=0 && tx.indexOf(a.m2)>=0 && all[i].querySelectorAll('*').length<70){menu=all[i];break;} }
      if(!menu) return 'no-menu';
      var it=[].slice.call(menu.querySelectorAll('*')).filter(function(e){return e.children.length===0 && (e.textContent||'').trim().toUpperCase()===a.l.toUpperCase();});
      if(it.length){ (it[0].closest('a')||it[0]).click(); return 'ok'; } return 'no-item'; }"""
    return pg.evaluate(js, {"l":label,"m1":marker1,"m2":marker2})
with sync_playwright() as p:
    b=p.chromium.launch(headless=False, slow_mo=250, args=['--ignore-certificate-errors','--start-maximized','--remote-debugging-port=9222'])
    pg=b.new_context(ignore_https_errors=True, no_viewport=True).new_page()
    pg.goto('https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/', wait_until='domcontentloaded', timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**', timeout=60000); wa(pg); say("== logged in ==")

    say("\n===== 1. CREATE Process-Diagram calc =====")
    opensc(pg,'Create Calculation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(600)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    er=None
    for att in range(4):
        clickvis(pg, INS); pg.wait_for_timeout(900)
        clickvis(pg, "xpath=//a[contains(@class,'ui-menuitem-link')][.//span[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'public calculation')]]")
        pg.wait_for_timeout(1100)
        for r in range(25):
            loc=pg.locator(cell('calculation:form:T:'+str(r)+':C0_in'))
            if loc.count()==0: continue
            if not loc.input_value().strip(): er=r; break
        if er is not None: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    R='calculation:form:T:'+str(er)
    pg.locator(cell(R+':C0_in')).fill(CODE); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
    pg.locator(cell(R+':C1_in')).fill(NAME); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
    pg.locator(cell(R+':C2_da_input')).fill('2000-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell(R+':C4_dd_button')).click(); pg.wait_for_timeout(600)
    pg.locator("xpath=//*[@id='"+R+":C4_dd_panel']//tr[normalize-space(@data-item-label)='Day']").first.click(); pg.wait_for_timeout(400)
    pg.locator(cell(R+':C5_dd_button')).click(); pg.wait_for_timeout(600)
    pg.locator("xpath=//*[@id='"+R+":C5_dd_panel']//tr[normalize-space(@data-item-label)='Process Diagram']").first.click(); pg.wait_for_timeout(400)
    pg.locator(SAVE).first.click(); wa(pg); pg.wait_for_timeout(1000)
    say("DB calc exists = %d" % q1("select count(*) from calculation where object_code='%s'" % CODE))

    say("\n===== 2. MAINTAIN -> Implement Step 1 as Equations -> drill in =====")
    opensc(pg,'Maintain Calculation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='"+NAME+"']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    clickvis(pg, "xpath=//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'flowch')]"); wa(pg)
    for att in range(3):
        pg.mouse.click(1080,577); pg.wait_for_timeout(400); pg.mouse.click(1080,577,button='right'); pg.wait_for_timeout(900)
        ia=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[contains(normalize-space(.),'Implement as')]]")
        hv=False
        for i in range(ia.count()):
            if ia.nth(i).is_visible(): ia.nth(i).hover(); hv=True; break
        if hv:
            pg.wait_for_timeout(700)
            eq=pg.locator("xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Equations']]")
            done=False
            for i in range(eq.count()):
                if eq.nth(i).is_visible(): eq.nth(i).click(); done=True; break
            if done: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    pg.wait_for_timeout(800); pg.locator(SAVE).first.click(); wa(pg); pg.wait_for_timeout(1000)
    pg.mouse.dblclick(1080,577); wa(pg); say("Step 1 implemented as Equations + drilled in")

    say("\n===== 3. ADD equation row (+ -> Equations, case-insensitive) =====")
    BASE='maintab:tabPanel:equations:form:T:0'
    for att in range(4):
        clickvis(pg, INS); pg.wait_for_timeout(700)
        say("  menu_click: "+menu_click(pg,'Equations','Set Equations','Combination Set List'))
        pg.wait_for_timeout(1600)
        if pg.locator(cell(BASE+':C5_b')).count()>0: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    say("equation row present = "+str(pg.locator(cell(BASE+':C5_b')).count()>0))

    say("\n===== 4. AUTHOR equation INFO = '%s' (canvas right-click menu) =====" % MSG)
    pg.locator(cell(BASE+':C5_b')).click(); pg.wait_for_timeout(1400)              # open editor
    pg.mouse.click(610,397,button='right'); pg.wait_for_timeout(800)              # context menu
    pg.mouse.click(651,779); pg.wait_for_timeout(700)                            # Log messages
    pg.mouse.click(833,779); pg.wait_for_timeout(900)                            # Insert 'INFO'
    pg.mouse.click(640,396,button='right'); pg.wait_for_timeout(800)             # context menu
    pg.mouse.click(690,604); pg.wait_for_timeout(900)                            # Insert assignment -> INFO = ?
    pg.mouse.click(645,396); pg.wait_for_timeout(300)                            # select ?
    pg.mouse.click(645,396,button='right'); pg.wait_for_timeout(800)
    pg.mouse.move(700,508); pg.wait_for_timeout(600); pg.mouse.move(888,636); pg.wait_for_timeout(400)  # Operands submenu
    pg.mouse.click(888,636); pg.wait_for_timeout(900)                            # Insert constant text -> popup
    pg.mouse.click(957,483); pg.wait_for_timeout(300); pg.keyboard.type(MSG, delay=35); pg.wait_for_timeout(300)
    pg.mouse.click(888,519); pg.wait_for_timeout(900)                            # OK popup -> INFO = 'MSG'
    pg.screenshot(path="C:/tmp/demo_eq.png", full_page=True); say("SHOT demo_eq (equation authored)")
    pg.mouse.click(615,581); pg.wait_for_timeout(1200)                           # OK editor
    pg.locator(SAVE).first.click(); wa(pg); pg.wait_for_timeout(1500)
    say("DB equation persisted = %d" % q1("select count(*) from calc_equation where dbms_lob.instr(equation,'%s')>0" % MSG))

    say("\n===== 5. CONNECT as job on P1_DAY_ALLOC =====")
    opensc(pg,'Calculation Group Setup')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell('nav:form:G:0:R:1:C:1:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:0:R:1:C:1:dd_panel']//tr[contains(@data-item-label,'Allocation Network')]").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator("xpath=//*[@id='nav_model:form:T_data']//tr[contains(.,'P1_DAY_ALLOC')]").first.click(); wa(pg)
    clickvis(pg, "xpath=//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'job connection')]"); wa(pg)
    for att in range(4):
        clickvis(pg, INS); pg.wait_for_timeout(900)
        if clickvis(pg, "xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Calculation Job']]"): pass
        pg.wait_for_timeout(1300)
        tgt=None
        for r in range(8):
            loc=pg.locator(cell(CONN+str(r)+':C0_da_input'))
            if loc.count()==0: break
            if not loc.input_value().strip(): tgt=r
        if tgt is not None: break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    P=CONN+str(tgt)
    pg.locator(cell(P+':C0_da_input')).fill('2011-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell(P+':C2_dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='"+P+":C2_dd_panel']//tr[normalize-space(@data-item-label)='"+NAME+"']").first.click(); pg.wait_for_timeout(500)
    pg.locator(SAVE).first.click(); wa(pg); pg.wait_for_timeout(1500)
    say("DB connected = %d" % q1("select count(*) from tv_alloc_network_job_conn where ecdp_objects.GetObjCode(job_id)='%s'" % CODE))

    say("\n===== 6. SIMULATE-RUN via Daily Allocation =====")
    opensc(pg,'Daily Allocation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-27'); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell('nav:form:G:1:R:1:C:0:da_input')).fill('2026-06-27'); pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
    pg.locator(cell('nav:form:G:2:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:2:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='P1 Day Allocation']").first.click(); wa(pg)
    pg.locator(cell('nav:form:G:4:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    pg.locator("xpath=//*[@id='nav:form:G:4:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='"+NAME+"']").first.click(); wa(pg)
    killpanels(pg); pg.keyboard.press('Control+g'); wa(pg); killpanels(pg)
    LOG='dateStartJob:form:G:0:R:1:C:1:dd'; SIM='dateStartJob:form:G:0:R:1:C:2:cb'
    try:
        pg.locator(cell(LOG+'_button')).click(); pg.wait_for_timeout(600)
        pg.locator("xpath=//*[@id='"+LOG+"_panel']//tr[normalize-space(@data-item-label)='Full']").first.click(); wa(pg); killpanels(pg)
    except Exception: pass
    pg.locator(cell(SIM)).check(force=True); pg.wait_for_timeout(400); killpanels(pg)
    pg.get_by_role("button", name=re.compile("run calc", re.I)).first.click(force=True); pg.wait_for_timeout(2500)
    okb=pg.get_by_role("button", name=re.compile(r"^ok$", re.I))
    if okb.count()>0 and okb.first.is_visible(): okb.first.click(); wa(pg)
    pg.wait_for_timeout(7000); killpanels(pg); pg.keyboard.press('Control+g'); wa(pg); pg.wait_for_timeout(1500)
    pg.screenshot(path="C:/tmp/demo_runlog.png", full_page=True); say("SHOT demo_runlog (Simulate Success + log line)")

    say("\n===== 7. SELF-CLEAN =====")
    opensc(pg,'Calculation Group Setup')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2026-06-29'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell('nav:form:G:0:R:1:C:1:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:0:R:1:C:1:dd_panel']//tr[contains(@data-item-label,'Allocation Network')]").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    pg.locator("xpath=//*[@id='nav_model:form:T_data']//tr[contains(.,'P1_DAY_ALLOC')]").first.click(); wa(pg)
    clickvis(pg, "xpath=//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'job connection')]"); wa(pg)
    pg.locator(cell(CONN+'0:C0_da_input')).click(); pg.wait_for_timeout(300); pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
    for att in range(3):
        clickvis(pg, DEL); pg.wait_for_timeout(900)
        if clickvis(pg, "xpath=//a[contains(@class,'ui-menuitem-link')][.//span[normalize-space(.)='Calculation Job']]"): break
        pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
    pg.wait_for_timeout(700); pg.locator(SAVE).first.click(); wa(pg); pg.wait_for_timeout(1200)
    opensc(pg,'Create Calculation')
    pg.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
    pg.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(700)
    pg.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(); wa(pg)
    pg.locator(cell('button:form:B')).click(); wa(pg)
    rid=pg.evaluate("(c) => { var ins=document.querySelectorAll('input'); for(var i=0;i<ins.length;i++){ if((ins[i].value||'')===c) return ins[i].id; } return ''; }", CODE)
    if rid:
        pg.locator(cell(rid)).click(); wa(pg); pg.keyboard.press('Escape'); pg.wait_for_timeout(400)
        pg.locator(cell('deletebutton:form:B')).click(); pg.wait_for_timeout(1000)
        yn=pg.get_by_role("button", name="Yes")
        if yn.count()>0 and yn.first.is_visible(): yn.first.click(); wa(pg)
    pg.wait_for_timeout(1200)
    say("DB FINAL: calc=%d jobconn=%d eq=%d (all expect 0)" % (
        q1("select count(*) from calculation where object_code='%s'" % CODE),
        q1("select count(*) from tv_alloc_network_job_conn where ecdp_objects.GetObjCode(job_id)='%s'" % CODE),
        q1("select count(*) from calc_equation where dbms_lob.instr(equation,'%s')>0" % MSG)))
    say("== DEMO COMPLETE ==")
    pg.wait_for_timeout(3000)
    b.close()
