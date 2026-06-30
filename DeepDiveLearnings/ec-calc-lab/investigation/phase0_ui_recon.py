"""Phase 0 UI recon (READ-ONLY): open the 4 Calculation-Objects screens, dump each toolbar's
New/Delete buttons + enabled state (the delete-reversibility GATE), grid id, and whether a
navigator+GO is required. No writes, no row clicks that persist."""
from playwright.sync_api import sync_playwright
import os, json
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SCREENS=['Database Object Types','Simple Object Types','Variable Definitions','Global Attributes']
def wa(pg,t=20000):
    pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1000)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    for name in SCREENS:
        print("\n==================== %s ====================" % name)
        try:
            si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
            si.clear(); si.type(name,delay=40); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
            link=pg.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())=%s]" % json.dumps(name))
            if link.count()==0:
                print("   [!] no tv-link found for this exact name; available tv-links:")
                for t in pg.locator("xpath=//*[contains(@class,'tv-link')]").all_text_contents()[:12]: print("       -",t.strip())
                continue
            link.first.click(); wa(pg)
        except Exception as e:
            print("   [!] open failed:",str(e)[:120]); continue
        # toolbar buttons across all frames (config screens render in the dashboard frame)
        for fr in pg.frames:
            try:
                tb=fr.evaluate("""()=>[...document.querySelectorAll("a[title], button[title], a.ui-commandlink")].map(e=>{
                    const ic=e.querySelector("span[class*='ui-icon']"); const r=e.getBoundingClientRect();
                    return {id:e.id||'', title:(e.getAttribute('title')||'').trim(),
                            icon: ic?ic.className.replace('ui-icon','').trim():'',
                            disabled: e.className.includes('ui-state-disabled'), y:Math.round(r.y)};
                  }).filter(o=>o.y>=0 && o.y<160 && (o.title||o.icon))
                   .filter(o=>/new|insert|add|delete|remove|save/i.test(o.title+' '+o.icon))""")
            except Exception:
                tb=[]
            if tb:
                print("   [frame %s] action buttons:" % (fr.url.split('/')[-1][:30]))
                for t in tb[:14]:
                    print("      %-9s title=%-22s icon=%-22s id=%s" % ('DISABLED' if t['disabled'] else 'enabled', t['title'][:22], t['icon'][:22], t['id']))
                # grid id in this frame
                g=fr.evaluate("""()=>{const e=document.querySelector("[id$='T_data'],[id$=':T']");return e?e.id:''}""")
                if g: print("      grid id:",g)
                # navigator + GO presence
                nav=fr.evaluate("""()=>({nav:!!document.querySelector("[id^='nav:form']"),go:!!document.querySelector("[id='button:form:B']")})""")
                print("      navigator present:",nav)
                break
    b.close()
print("\nDONE phase0_ui_recon")
