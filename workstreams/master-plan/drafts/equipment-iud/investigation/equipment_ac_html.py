"""Phase 0f — dump the FULL HTML of a navigator autocomplete + its panel after trigger click. READ-ONLY."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

def _repo_root():
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p/'.git').exists(): return p
    return here.parents[5]

EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width':1920,'height':1080})
    page = ctx.new_page()
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username','sysadmin'); page.fill('#password','sysadmin'); page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000); page.wait_for_load_state('networkidle', timeout=30000)
    si=page.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state='visible')
    si.clear(); si.type('Equipment', delay=60); page.wait_for_load_state('networkidle', timeout=8000); page.wait_for_timeout(500)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Equipment']").first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
    print('Equipment loaded')

    # FULL html of Equipment Type dd (G:4) and Production Unit dd (G:1)
    for g in ['G:1','G:4']:
        html = page.evaluate(f"""()=>{{const e=document.getElementById('nav:form:{g}:R:1:C:0:dd');return e?e.outerHTML:'(none)';}}""")
        print(f'\n===== {g} dd FULL HTML =====\n{html}')

    # Click the G:4 dropdown trigger button and capture whatever panel appears
    print('\n===== Click G:4 trigger, capture panels =====')
    esc='nav\\:form\\:G\\:4\\:R\\:1\\:C\\:0\\:dd'
    # try button inside dd span
    btns = page.evaluate("""()=>{
        const dd=document.getElementById('nav:form:G:4:R:1:C:0:dd');
        const out=[];
        if(dd) dd.querySelectorAll('button,a,span[class*="dropdown"]').forEach(x=>out.push({tag:x.tagName,cls:x.className,id:x.id||''}));
        return out;
    }""")
    print(f'  children buttons/triggers in G:4 dd: {btns}')

    page.locator(f'#{esc} button').first.click(timeout=4000)
    page.wait_for_timeout(1500)
    panels = page.evaluate("""()=>{
        const out=[];
        document.querySelectorAll('[class*="autocomplete-panel"],[id*="dd_panel"]').forEach(p=>{
            out.push({id:p.id||'', cls:p.className.substring(0,50), visible:p.offsetParent!==null,
                      items:p.querySelectorAll('li').length, sample:(p.textContent||'').trim().substring(0,80)});
        });
        return out;
    }""")
    print(f'  panels after trigger click: {panels}')
    page.screenshot(path=str(_repo_root()/'docs'/'EC'/'screenshots'/'iud_equipment'/'achtml_trigger.png'))

    ctx.close(); b.close()
print('Done.')
