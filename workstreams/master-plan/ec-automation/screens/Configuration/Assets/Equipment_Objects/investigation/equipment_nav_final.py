"""
Phase 0g — DEFINITIVE navigator setter (click dd_button chevron -> click option in dd_panel),
then complete the scan: result-table id, row-select labeled forms, delete-button behaviour. READ-ONLY.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root():
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists(): return p
    return here.parents[5]


EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_equipment')
os.makedirs(SS_DIR, exist_ok=True)

def esc(i): return '#' + i.replace(':', '\\:')


def set_nav(page, group, want):
    btn = f'nav:form:{group}:R:1:C:0:dd_button'
    panel = f'nav:form:{group}:R:1:C:0:dd_panel'
    inp = f'nav:form:{group}:R:1:C:0:dd_input'
    page.locator(esc(btn)).first.click()
    page.wait_for_timeout(1000)
    opts = page.evaluate(f"""()=>{{const p=document.getElementById('{panel}');if(!p)return[];const s=[];p.querySelectorAll('li,td,div').forEach(x=>{{if(x.querySelectorAll('*').length<=1){{const t=(x.textContent||'').trim();if(t)s.push(t);}}}});return [...new Set(s)];}}""")
    print(f'  {group} options({len(opts)}): {opts[:14]}')
    opt = page.locator(esc(panel)).get_by_text(want, exact=True)
    if opt.count() == 0:
        opt = page.locator(esc(panel)).get_by_text(want)
    if opt.count() > 0:
        opt.first.click()
        page.wait_for_load_state('networkidle', timeout=12000); page.wait_for_timeout(900)
        got = page.evaluate(f"()=>{{const e=document.getElementById('{inp}');return e?e.value:'';}}")
        print(f'  {group} = "{got}"')
        return got
    print(f'  {group} "{want}" not found'); page.keyboard.press('Escape'); return ''


def labeled(page, form_id):
    return page.evaluate("""(fid)=>{const r=document.getElementById(fid)||document.querySelector('[id^="'+fid+'"]');if(!r)return[];const o=[];
        r.querySelectorAll('input:not([type=hidden]),textarea,select').forEach(e=>{if(!e.id||e.offsetParent===null||e.id.includes('statusarea'))return;
        const lid=e.id.replace(/:C:1:[a-z_]+$/,':C:0:la');const le=document.getElementById(lid);
        o.push({id:e.id,label:le?(le.textContent||'').trim().substring(0,32):'',type:e.type||e.tagName,ro:e.readOnly,val:(e.value||'').substring(0,24)});});return o;}""", form_id)


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
    print('Equipment loaded\n=== SET NAVIGATOR (dd_button -> panel option) ===')

    set_nav(page, 'G:1', 'Production Unit')   # EXACT value per screenshot (not "Production Unit 1")
    set_nav(page, 'G:2', 'Offshore area')
    set_nav(page, 'G:3', 'Offshore facility')
    set_nav(page, 'G:4', 'Compressor')

    print('\n=== FINAL nav values ===')
    for g,n in [('G:1','PU'),('G:2','Area'),('G:3','FC1'),('G:4','EqType')]:
        v=page.evaluate(f"()=>{{const e=document.getElementById('nav:form:{g}:R:1:C:0:dd_input');return e?e.value:'';}}")
        print(f'  {n}: "{v}"')
    page.screenshot(path=os.path.join(SS_DIR,'final_01_filters.png'), full_page=True)

    print('\n=== GO ===')
    page.locator('#button\\:form\\:B').first.click()
    page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(2000)
    page.screenshot(path=os.path.join(SS_DIR,'final_02_after_go.png'), full_page=True)
    msg=page.evaluate("""()=>{const n=document.getElementById('ECNotificationArea');return n?(n.textContent||'').replace(/EC\\.jsMessage\\.clear\\(\\);/,'').trim().substring(0,140):'';}""")
    print(f'Message: {msg or "(none)"}')

    # find result table
    info=page.evaluate("""()=>{const t=[];document.querySelectorAll('.ui-datatable').forEach(dt=>{const bd=dt.querySelector('tbody[id$="_data"]');let n=0,f='';if(bd){const tr=bd.querySelectorAll('tr');tr.forEach(r=>{if((r.textContent||'').trim())n++;});f=tr.length?(tr[0].textContent||'').trim().substring(0,60):'';}t.push({id:dt.id,body:bd?bd.id:'',rows:n,first:f});});return t;}""")
    print('\n=== Result tables ===')
    for t in info: print(f'  id={t["id"]} body={t["body"]} rows={t["rows"]} first="{t["first"]}"')

    # row select (read-only) using first row's first cell span
    body_id = info[0]['body'] if info and info[0]['rows'] else ''
    if body_id:
        print(f'\n=== ROW SELECT (read-only) from {body_id} ===')
        sp = page.locator(f'css={esc(body_id)} span').first
        if sp.count()>0:
            sp.click(); page.wait_for_load_state('networkidle', timeout=15000); page.wait_for_timeout(1500)
            page.screenshot(path=os.path.join(SS_DIR,'final_03_row_selected.png'), full_page=True)
            for fid in ['tab:tabPanel:updateAttributes:form','tab:tabPanel:objectdates:form']:
                print(f'\n  --- {fid} ---')
                for f in labeled(page, fid):
                    print(f'    {f["label"]:<26} -> {f["id"]} [{f["type"]}] ro={f["ro"]} val="{f["val"]}"')
            delbtn=page.evaluate("""()=>{const o=[];document.querySelectorAll('#screenToolbar\\\\:form\\\\:menuBar a').forEach(a=>{const i=a.querySelector('span[class*="ui-icon-"]');const ic=i?(i.className.match(/ui-icon-[a-z-]+/)||[''])[0]:'';if(ic.includes('delete')||ic.includes('trash'))o.push({icon:ic,disabled:a.classList.contains('ui-state-disabled'),li:a.closest('li')?a.closest('li').className.substring(0,55):'',onclick:(a.getAttribute('onclick')||'').substring(0,90)});});return o;}""")
            print(f'\n  DELETE button after row-select: {delbtn}')

    ctx.close(); b.close()
print('\nPhase 0g done.', SS_DIR)
