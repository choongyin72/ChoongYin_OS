"""Phase 1b Var B2 (v2 - working): add the READ MAPPING to AUTOTEST_rCO2Rate.
Proper master-select (click C0 + Escape -> row highlight), READ MAPPINGS tab, insert CLASS READ
MAPPING, fill dropdowns C1_dd=Data, C2_dd=PWEL_DAY_DATA, C4_dd=THEOR_CO2_RATE, then CLASS KEY READ
MAPPING (OBJECT_ID->dim1, DAYTIME->dim2) if not auto-populated. Save + DB-verify. PRE-REQ: Var B1 exists."""
from playwright.sync_api import sync_playwright
import os, re as _re, oracledb
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
VAR='AUTOTEST_rCO2Rate'
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
G='variable_definition_table:form:T'; RM='tab:tabPanel:readMapping:form:T'; AM='tab:tabPanel:attrMapping:form:T'
def _opts(fr,base):
    return fr.evaluate("""(b)=>{const pan=document.getElementById(b+'_dd_panel'); if(!pan)return [];
        return [...pan.querySelectorAll('tr')].map(r=>r.getAttribute('data-item-label')||r.innerText.trim()).filter(Boolean);}""", base)
def pick_dd(fr,pg,base,needle):
    """type-ahead autocomplete: type needle into <base>_dd_input, wait, click option containing needle (ci)."""
    inp=fr.locator(cell(base+'_dd_input')); inp.click(); inp.fill(''); inp.type(needle, delay=60); pg.wait_for_timeout(1400)
    opts=_opts(fr,base)
    lab=next((o for o in opts if needle.lower() in o.lower()), None)
    if lab is None:
        # fall back: button-open full list
        fr.locator(cell(base+'_dd_button')).click(); pg.wait_for_timeout(800); opts=_opts(fr,base)
        lab=next((o for o in opts if needle.lower() in o.lower()), None)
    if lab is None: print("   dd %s: NO match '%s'; options=%s" % (base[-14:], needle, opts[:6])); return False
    fr.locator(f"xpath=//*[@id='{base}_dd_panel']//tr[normalize-space(@data-item-label)={_q(lab)}]").first.click(timeout=6000); pg.wait_for_timeout(500)
    print("   dd %s <- %s" % (base[-14:], lab)); return True
def _q(s): return "'"+s+"'" if "'" not in s else '"'+s+'"'
def click_flyout(fr,pg,label_re):
    a=fr.locator("xpath=//a[.//span[contains(@class,'ui-icon-insert')]]").first
    a.scroll_into_view_if_needed(); a.hover(); pg.wait_for_timeout(1000)
    it=fr.locator("a.ui-menuitem-link").filter(has_text=_re.compile(label_re,_re.I))
    for k in range(it.count()):
        x=it.nth(k)
        try:
            if x.is_visible(): x.click(timeout=4000); return True
        except Exception: continue
    return False
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Variable Definitions',delay=40); pg.wait_for_timeout(900)
    pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Variable Definitions']").first.click(); wa(pg)
    fr=[f for f in pg.frames if 'variable_definition' in f.url.lower()][0]
    fr.locator(cell('nav:form:G:0:R:1:C:0:da_input')).fill('2003-01-01'); fr.locator('body').press('Tab'); pg.wait_for_timeout(500)
    fr.locator(cell('nav:form:G:1:R:1:C:0:dd_button')).click(); pg.wait_for_timeout(800)
    fr.locator("xpath=//*[@id='nav:form:G:1:R:1:C:0:dd_panel']//tr[normalize-space(@data-item-label)='Production Allocation']").first.click(timeout=8000); pg.wait_for_timeout(400)
    fr.locator(cell('button:form:B')).click(); wa(pg)
    idx=fr.evaluate("""([g,n])=>{const trs=document.querySelectorAll(`[id='${g}_data'] tr`);
        for(let i=0;i<trs.length;i++){const e=document.getElementById(`${g}:${i}:C0_in`); if(e&&e.value.trim()===n)return i;}return -1;}""", [G, VAR])
    print("var idx:", idx)
    # MASTER SELECT: click C0 then Escape -> row highlight (the key gesture)
    fr.locator(cell(f'{G}:{idx}:C0_in')).click(); pg.wait_for_timeout(500); fr.locator('body').press('Escape'); pg.wait_for_timeout(400)
    fr.locator("xpath=//a[contains(translate(.,'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'READ MAPPINGS')]").first.click(timeout=5000); pg.wait_for_timeout(1100)
    print("insert CLASS READ MAPPING:", click_flyout(fr,pg,r"^\s*class read mapping")); pg.wait_for_timeout(1200)
    # fill the new row 0 dropdowns
    pick_dd(fr,pg,f'{RM}:0:C1','Data')          # Class Type
    pick_dd(fr,pg,f'{RM}:0:C2','PWEL_DAY_DATA')  # Class Name
    pg.wait_for_timeout(800)
    pick_dd(fr,pg,f'{RM}:0:C4','CO2_RATE')       # Value Attribute (THEOR_CO2_RATE / Theor Co2 Rate)
    # class-key mapping: auto-populated?
    ak=fr.evaluate("(g)=>document.querySelectorAll(`[id='${g}_data'] tr`).length", AM)
    print("attrMapping rows after class set:", ak)
    if click_flyout(fr,pg,r"^\s*class key read mapping"):
        print("inserted a CLASS KEY READ MAPPING row"); pg.wait_for_timeout(900)
    save=fr.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    print("save enabled:", save.count()>0)
    if save.count()>0: save.first.click(); wa(pg)
    print("banner:", fr.evaluate("""()=>[...document.querySelectorAll(".ui-messages-error-detail,.ui-message-error-detail,.ui-messages-info-summary")].map(e=>e.innerText.trim()).filter(Boolean).slice(0,5)"""))
    b.close()
c=oracledb.connect(user=os.environ.get('EC_DB_USER','ECKERNEL_EC'),password=os.environ.get('EC_DB_PASS','energy'),dsn=os.environ.get('EC_DB_DSN','localhost:1521/ORCL'))
cur=c.cursor()
cur.execute("""select m.cls_name, m.sql_syntax from calc_var_read_mapping m
               join calc_variable v on v.calc_var_signature=m.calc_var_signature where v.name=:1""",[VAR])
rows=cur.fetchall()
print("\nDB VERIFY read mapping for %s:"%VAR, [(r[0], (r[1].read() if hasattr(r[1],'read') else r[1])) for r in rows])
print("RESULT:", "PASS (read mapping persisted)" if rows else "FAIL (no mapping row)")
c.close()
