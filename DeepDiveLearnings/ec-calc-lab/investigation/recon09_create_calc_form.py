"""Phase-2 recon (READ-ONLY): open 'Create Calculation' + map the authoring form/wizard. Never saves."""
from playwright.sync_api import sync_playwright
import os
EC_URL=os.environ.get('EC_URL','https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
def wa(pg,t=15000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1200)
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=['--ignore-certificate-errors'])
    pg=b.new_context(ignore_https_errors=True,viewport={'width':1920,'height':1080}).new_page()
    pg.goto(EC_URL,wait_until='domcontentloaded',timeout=30000)
    pg.fill('#username','sysadmin'); pg.fill('#password','sysadmin'); pg.click('#kc-login')
    pg.wait_for_url('**/dashboard**',timeout=60000); wa(pg)
    si=pg.locator(r'#menu\:searchForm\:searchTxt'); si.wait_for(state='visible',timeout=10000)
    si.clear(); si.type('Create Calculation',delay=50); pg.wait_for_load_state('networkidle',timeout=8000); pg.wait_for_timeout(700)
    link=pg.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Create Calculation']")
    print("tv-link found:",link.count())
    if link.count()==0: 
        print("ALL tv-links:", pg.evaluate("()=>Array.from(document.querySelectorAll('.tv-link')).map(e=>e.textContent.trim())")[:20]); b.close(); raise SystemExit
    link.first.click(); wa(pg)
    lbl=pg.locator(r'#screenToolbar\:form\:screenLabel').text_content(timeout=5000) if pg.locator(r'#screenToolbar\:form\:screenLabel').count() else "(no label)"
    print("screen:",lbl)
    # dump visible form fields/labels + buttons (read-only map of the create form)
    fields=pg.evaluate("""() => {
       const labs=Array.from(document.querySelectorAll("label, .ui-outputlabel, th")).map(e=>e.textContent.trim()).filter(t=>t && t.length<40).slice(0,40);
       const inputs=Array.from(document.querySelectorAll("input[type='text'], select, [id$='_input'], [id$='dd_button']")).map(e=>e.id).filter(Boolean).slice(0,30);
       const btns=Array.from(document.querySelectorAll("button, a.ui-button, a[title]")).map(e=>(e.textContent||e.getAttribute('title')||'').trim()).filter(t=>t&&t.length<30).slice(0,25);
       return {labs, inputs, btns};
    }""")
    print("\nLABELS:", fields['labs'])
    print("\nINPUT IDS:", fields['inputs'])
    print("\nBUTTONS:", [x for x in dict.fromkeys(fields['btns'])])
    print("\nDONE (read-only; nothing saved).")
    b.close()
