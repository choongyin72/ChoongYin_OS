"""Trigger the Language Save confirmation modal and CAPTURE it (screenshot + DOM dump).
Does NOT confirm -> nothing persists. READ-ONLY effect (no committed change)."""
from playwright.sync_api import sync_playwright
from pathlib import Path

def _repo_root():
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]

SS = _repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_language'
SS.mkdir(parents=True, exist_ok=True)
EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'

def cell(r, c): return f'table:form:T:{r}:C{c}_in'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Language', delay=50); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(600)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Language']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)

    # insert a blank row + fill (no persist yet)
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(700)
    page.locator("xpath=(//ul[contains(@class,'ui-menu-child')]//li//a)[1]").first.click()
    page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(1000)
    # find blank C1 row
    blank = page.evaluate("""()=>{let r=-1;document.querySelectorAll('input[id^="table:form:T:"][id$=":C1_in"]').forEach(i=>{if((i.value||'').trim()===''){const m=i.id.match(/:T:(\\d+):C1_in/);if(m&&r<0)r=parseInt(m[1]);}});return r;}""")
    print('blank row:', blank)
    for col, val in [(1, 'ZZ'), (2, 'Autotest Lang')]:
        el = page.locator(f'[id="{cell(blank, col)}"]')
        el.click(); el.press('Control+a'); el.press('Delete'); el.type(val, delay=40); el.press('Tab')
        page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(400)

    # click Save -> expect the confirmation modal
    page.locator("xpath=//a[@title='Save [Ctrl+s]']").first.click()
    page.wait_for_timeout(2500)

    # capture screenshot
    page.screenshot(path=str(SS / 'confirm_dialog.png'), full_page=True)
    print('screenshot ->', SS / 'confirm_dialog.png')

    # dump any visible dialog + its buttons/links
    dump = page.evaluate("""()=>{
        const out={dialogs:[]};
        document.querySelectorAll('.ui-dialog, [id*="confirmation"], [id*="confirm"]').forEach(d=>{
            const vis = d.offsetParent!==null || (d.getBoundingClientRect && d.getBoundingClientRect().width>0);
            if(!vis) return;
            const btns=[];
            d.querySelectorAll('button, a').forEach(x=>{ if(x.offsetParent!==null) btns.push({id:x.id||'', text:(x.textContent||'').trim().substring(0,40), cls:(x.className||'').substring(0,60)}); });
            const titleEl = d.querySelector('.ui-dialog-title, [id$="_title"]');
            out.dialogs.push({ id:d.id, title:titleEl?titleEl.textContent.trim():'', text:(d.textContent||'').trim().substring(0,160), buttons:btns });
        });
        return out;
    }""")
    print('=== visible dialog(s) ===')
    import json
    print(json.dumps(dump, indent=2)[:2500])

    # DO NOT confirm -> close (nothing persists)
    ctx.close(); b.close()
print('done (not confirmed -> nothing persisted)')
