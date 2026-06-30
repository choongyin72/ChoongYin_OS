"""B2 Part 1 (REAL, saves): add CLASS READ MAPPING to AUTOTEST_rCO2Rate with EXACT values
(Data / PWEL_DAY_DATA / THEOR_CO2_RATE), Save, assert DB attr == 'THEOR_CO2_RATE' exactly.
Then post-save: re-select, report attrMapping auto-populate + CLASS KEY enablement + (if enabled)
dump the class-key new-row cells (NO part-2 save yet). PRE-REQ: Var B1 exists."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'; CLS='PWEL_DAY_DATA'; ATTR='THEOR_CO2_RATE'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'; AM='tab:tabPanel:attrMapping:form:T'
def _opts(fr,base): return fr.evaluate("""(b)=>{const p=document.getElementById(b+'_dd_panel');if(!p)return[];return [...p.querySelectorAll('tr')].map(r=>r.getAttribute('data-item-label')||r.innerText.trim()).filter(Boolean);}""",base)
def type_pick(fr,pg,base,needle,exact=None):
    inp=fr.locator(cell(base+'_dd_input')); inp.click(); inp.fill(''); inp.type(needle,delay=60); pg.wait_for_timeout(1300)
    opts=_opts(fr,base); lab=next((o for o in opts if o.strip()==exact),None) if exact else next((o for o in opts if needle.lower() in o.lower()),None)
    if lab is None: print("   NO match %s exact=%s opts=%s"%(needle,exact,opts[:6])); return False
    fr.locator(f"xpath=//*[@id='{base}_dd_panel']//tr[normalize-space(@data-item-label)={chr(39)+lab+chr(39)}]").first.click(timeout=6000); pg.wait_for_timeout(500)
    print("   %s <- %s"%(base[-10:],lab)); return True
def flyout(fr,pg,rx):
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first; a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(900)
    it=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(rx,_re.I))
    for k in range(it.count()):
        x=it.nth(k)
        try:
            if x.is_visible(): x.click(timeout=4000); return True
        except Exception: continue
    return False
def select_var_readmap(fr,pg):
    fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    idx=fr.evaluate("""([g,n])=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`);if(e&&e.value.trim()===n)return i;}return -1;}""",[G,VAR])
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(500); fr.locator('body').press('Escape'); pg.wait_for_timeout(400)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1100)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login'); pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Variable Definitions',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Variable Definitions']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'variable_definition' in f.url.lower()][0]
    select_var_readmap(fr,pg)
    flyout(fr,pg,r"^\s*class read mapping"); pg.wait_for_timeout(1100)
    type_pick(fr,pg,f'{RM}:0:C1','Data'); type_pick(fr,pg,f'{RM}:0:C2','PWEL_DAY_DATA'); pg.wait_for_timeout(700)
    type_pick(fr,pg,f'{RM}:0:C4','THEOR_CO2',exact=ATTR)
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if save.count()>0: save.first.click(); wa(pg)
    print("Part1 saved; banner:", fr.evaluate("""()=>[...document.querySelectorAll('.ui-messages-error-detail,.ui-message-error-detail')].map(e=>e.innerText.trim()).filter(Boolean).slice(0,3)"""))
    # POST-SAVE inspect Part 2
    select_var_readmap(fr,pg)
    fr.locator(f"xpath=//*[@id='{RM}_data']/tr[1]/td[1]").click(); pg.wait_for_timeout(800)
    print("attrMapping rows post-save:", fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length",AM))
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first; a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(900)
    print("CLASS KEY state:", fr.evaluate("""()=>{const o=[];document.querySelectorAll('a.ui-menuitem-link').forEach(e=>{if(/class key read mapping/i.test(e.innerText)){const li=e.closest('li')||e;o.push({disabled:(li.className+e.className).includes('ui-state-disabled'),vis:e.getBoundingClientRect().width>0});}});return o;}"""))
    if flyout(fr,pg,r"^\s*class key read mapping"):
        pg.wait_for_timeout(1100)
        print("class-key NEW row cells:", fr.evaluate("""(g)=>{const tr=document.querySelectorAll(`[id='${g}_data'] tr`)[0];if(!tr)return[];return [...tr.querySelectorAll('input,button,span[id]')].map(e=>e.id.replace(`${g}:0:`,'')).filter(Boolean);}""",AM))
    b.close()  # part 2 not saved
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor(); cur.execute("""select m.cls_name,m.sql_syntax from calc_var_read_mapping m join calc_variable v on v.calc_var_signature=m.calc_var_signature where v.name=:1""",[VAR])
rows=[(r[0],(r[1].read() if hasattr(r[1],'read') else r[1])) for r in cur.fetchall()]; print("\nDB Part1:",rows)
print("RESULT Part1:", "PASS exact" if rows and rows[0]==(CLS,ATTR) else "CHECK: "+str(rows)); c.close()
