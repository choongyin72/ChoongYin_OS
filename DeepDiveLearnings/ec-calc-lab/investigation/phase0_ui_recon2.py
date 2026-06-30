"""Phase 0 UI recon v2 (READ-ONLY): for each Calc-Objects screen, set the navigator + click GO,
then dump the GRID toolbar buttons (a > span.ui-icon-*) with disabled state = the delete gate.
Also dump grid id and the first blank-row insert behaviour is NOT triggered (no writes)."""
from playwright.sync_api import sync_playwright
import os, json
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SCREENS=['Database Object Types','Simple Object Types','Variable Definitions','Global Attributes']
def wa(pg,t=20000):
    pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(900)
def cell(s): return '#'+s.replace(':',r'\:')
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for name in SCREENS:
        print("\n==================== %s ====================" % name)
        si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
        si.clear(); si.type(name,delay=40); pg.wait_for_timeout(900)
        link=pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())=%s]" % json.dumps(name))
        if link.count()==0: print("   [!] no link"); continue
        link.first.click(); wa(pg)
        # set navigator (date) + GO if present
        d=pg.locator(cell('nav:form:G:0:R:1:C:0:da_input'))
        if d.count()>0:
            try: d.click(); d.fill('2003-01-01'); pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
            except Exception: pass
        go=pg.locator(cell('button:form:B'))
        if go.count()>0:
            try: go.click(); wa(pg)
            except Exception as e: print("   GO click note:",str(e)[:70])
        # dump grid toolbar icons in the content frame
        for fr in pg.frames:
            try:
                icons=fr.evaluate("""()=>[...document.querySelectorAll("a")].map(a=>{
                    const sp=a.querySelector("span[class*='ui-icon-']"); if(!sp) return null;
                    const cl=[...sp.classList].find(c=>c.startsWith('ui-icon-'))||'';
                    const r=a.getBoundingClientRect();
                    return {icon:cl, title:(a.getAttribute('title')||'').trim(),
                            disabled:a.className.includes('ui-state-disabled'), id:a.id||'', y:Math.round(r.y)};
                  }).filter(o=>o && /insert|trash|close|plus|minus|delete|disk|pencil/i.test(o.icon))""")
            except Exception: icons=[]
            if icons:
                print("   [frame %s] grid action icons:" % fr.url.split('/')[-1][:26])
                seen=set()
                for o in icons:
                    k=(o['icon'],o['id'])
                    if k in seen: continue
                    seen.add(k)
                    print("      %-9s %-20s title=%-16s id=%s" % ('DISABLED' if o['disabled'] else 'enabled', o['icon'], o['title'][:16], o['id']))
                g=fr.evaluate("""()=>{const e=document.querySelector("[id$='T_data']");return e?e.id:''}""")
                rows=fr.evaluate("""()=>document.querySelectorAll("[id$='T_data'] tr").length""")
                print("      grid id: %s  (rows visible: %s)" % (g,rows))
                break
    b.close()
print("\nDONE phase0_ui_recon2")
