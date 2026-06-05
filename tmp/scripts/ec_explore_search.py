"""
EC Screen KB — Search-based navigation for remaining screens.
Uses sidebar search to find each screen individually.
Accumulates results.
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL   = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
KB_PATH  = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_v3.json'
LOG_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_search.txt'
INV_PATH = r'c:\Projects\ChoongYin_OS\docs\EC\ec_full_tree_inventory.json'

os.makedirs(r'c:\Projects\ChoongYin_OS\tmp\logs', exist_ok=True)

class Tee:
    def __init__(self, *files): self.files = files
    def write(self, obj): [f.write(obj) for f in self.files]; [f.flush() for f in self.files]
    def flush(self): [f.flush() for f in self.files]
_log = open(LOG_PATH, 'w', encoding='utf-8')
sys.stdout = Tee(sys.__stdout__, _log)

TOP_LEVEL = {
    'Dashboard','Configuration','EC Production','EC Chemistry','EC Transport',
    'EC Sales','EC Revenue','System Messages','Reporting','Process Automation',
    'Messaging','Task List','EC Integration Service'
}
SKIP_SCREENS = {'Documentation', 'Generation of BF Documentation'}

ANALYZE_JS = """(args) => {
    const [name, section] = args;
    const r = {name, section,
        url: window.location.href,
        screen_label: document.getElementById('screenToolbar:form:screenLabel')?.textContent?.trim()||''
    };
    const navForms = document.querySelectorAll('.ECFormScreenlet,.formScreenlet');
    r.has_navigator = navForms.length > 0;
    r.nav_labels = [];
    navForms.forEach(f => {
        const labels = [];
        f.querySelectorAll("[id$=':la']").forEach(la => {
            const t = la.textContent.trim();
            if (t.length > 1 && t.length < 35) labels.push(t);
        });
        if (labels.length) r.nav_labels.push(labels.slice(0,5));
    });
    const dts = document.querySelectorAll('.ui-datatable');
    r.datatable_count = dts.length;
    r.datatables = [];
    dts.forEach((dt, i) => {
        if (i < 3) {
            const cols = [];
            dt.querySelectorAll('thead th').forEach(th => {
                const t = th.textContent.trim(); if (t) cols.push(t.substring(0,25));
            });
            const filters = [];
            dt.querySelectorAll('input[id*=sfilter],input[id*=filter]').forEach(f =>
                filters.push(f.id.substring(0,50)));
            r.datatables.push({id:dt.id.substring(0,50), cols:cols.slice(0,10),
                                rows:dt.querySelectorAll('tbody tr').length, filters:filters.slice(0,5)});
        }
    });
    const saveBtn  = document.querySelector("a[title='Save [Ctrl+s]']");
    const insertLi = document.querySelector('li span.ui-icon-insert')?.closest('li');
    const deleteLi = document.querySelector('li span.ui-icon-delete')?.closest('li');
    r.save_enabled   = saveBtn  ? !saveBtn.className.includes('disabled')  : false;
    r.insert_enabled = insertLi ? !insertLi.className.includes('disabled') : false;
    r.delete_enabled = deleteLi ? !deleteLi.className.includes('disabled') : false;
    const hasForms = navForms.length > 0, hasTables = dts.length > 0;
    if      (hasForms && hasTables) r.screen_type = 'NAVIGATOR+TABLE';
    else if (hasForms)              r.screen_type = 'NAVIGATOR-ONLY';
    else if (hasTables)             r.screen_type = 'TABLE-ONLY';
    else                            r.screen_type = 'ACTION/EMPTY';
    const btns = new Set();
    document.querySelectorAll('.ECButtonScreenlet .ui-button,.buttonScreenlet .ui-button').forEach(b => {
        const t = b.textContent.replace('ui-button','').trim();
        if (t && t.length > 1) btns.add(t.substring(0,30));
    });
    r.action_buttons = [...btns].slice(0,6);
    return r;
}"""


def search_and_navigate(page, screen_name):
    """Use sidebar search to find and navigate to a screen."""
    try:
        si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
        si.wait_for(state='visible', timeout=8000)
        si.clear()
        si.type(screen_name[:35], delay=50)  # type() triggers PrimeFaces AJAX keyup
        page.wait_for_load_state('networkidle', timeout=8000)
        page.wait_for_timeout(400)

        # Try exact match
        if "'" in screen_name:
            parts = screen_name.split("'")
            xv = "concat('" + "',\"'\",'".join(parts) + "')"
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={xv}]"
        else:
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_name}']"

        el = page.locator(sel)
        if el.count() > 0 and el.first.is_visible():
            el.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(500)
            # Must be on EC app
            if any(x in page.url for x in ['xhtml','com.ec.','ap-f0a7g']):
                return True
            # Went external — back to dashboard
            page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
            return False
        return False
    except:
        return False


def ensure_ec(page):
    if not any(x in page.url for x in ['xhtml','com.ec.','ap-f0a7g','dashboard']):
        try:
            page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
        except:
            pass


# Load inventory
with open(INV_PATH, 'r', encoding='utf-8') as f:
    inventory = json.load(f)

# Load previous KB
screen_db = {}
if os.path.exists(KB_PATH):
    try:
        with open(KB_PATH, 'r', encoding='utf-8') as f:
            screen_db = json.load(f)
        already = sum(1 for v in screen_db.values() if v.get('found'))
        print(f'Loaded previous KB: {len(screen_db)} entries, {already} already found')
    except:
        pass

# Build list of screens not yet found
seen = set()
to_explore = []
for item in inventory:
    txt = item['text']
    if txt not in TOP_LEVEL and txt not in SKIP_SCREENS and txt not in seen and len(txt) > 2:
        seen.add(txt)
        key = f'{item.get("section","?")}::{txt}'
        if not screen_db.get(key, {}).get('found', False):
            to_explore.append({'text': txt, 'section': item.get('section','?')})

print(f'Screens not yet found: {len(to_explore)}\n')

success = 0
skip = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # Login
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    print('Logged in\n')

    for i, item in enumerate(to_explore):
        screen  = item['text']
        section = item['section']
        key     = f'{section}::{screen}'

        ensure_ec(page)
        ok = search_and_navigate(page, screen)

        if not ok:
            skip += 1
            screen_db[key] = {'name':screen,'section':section,'found':False,'screen_type':'NOT_FOUND'}
            if skip <= 10 or skip % 50 == 0:
                print(f'  SKIP [{section[:10]}] {screen}')
            continue

        try:
            page.wait_for_load_state('networkidle', timeout=10000)
            page.wait_for_timeout(400)
            info = page.evaluate(ANALYZE_JS, [screen, section])
        except Exception:
            try:
                page.wait_for_load_state('networkidle', timeout=8000)
                info = page.evaluate(ANALYZE_JS, [screen, section])
            except:
                skip += 1; continue

        info['found'] = True
        screen_db[key] = info
        success += 1

        stype = info.get('screen_type','?')
        nav   = 'Y' if info.get('has_navigator') else 'N'
        dts   = info.get('datatable_count',0)
        save  = 'S' if info.get('save_enabled') else '-'
        ins   = '+' if info.get('insert_enabled') else '-'
        dele  = 'D' if info.get('delete_enabled') else '-'
        nav_l = [la for g in info.get('nav_labels',[]) for la in g[:2]]
        cols  = [c for dt in info.get('datatables',[]) for c in dt.get('cols',[])[:2]]
        label = info.get('screen_label','')[:20]
        print(f'  {i+1:03d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}] {screen[:25]:<25}|{stype:<18}|dt={dts}|nav={nav_l[:2]}|cols={cols[:2]}|"{label}"')

        if success % 50 == 0:
            with open(KB_PATH,'w',encoding='utf-8') as f: json.dump(screen_db,f,indent=2)
            total_found = sum(1 for v in screen_db.values() if v.get('found'))
            print(f'  ... checkpoint: {total_found} total found ({success} this run / {skip} skipped)')

    ctx.close()
    browser.close()

# Final save
with open(KB_PATH,'w',encoding='utf-8') as f: json.dump(screen_db,f,indent=2)

total_found = sum(1 for v in screen_db.values() if v.get('found'))
print(f'\n{"="*70}')
print(f'DONE: {total_found}/670 total found | +{success} this run | {skip} skipped')
_log.close()
