"""
EC Screen KB Builder v3
- Expand tree ONCE at start
- Click each label directly (no search, no going back to dashboard)
- Only re-expand if navigated away from EC
- Skip known external links
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL  = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR  = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\all_screens'
KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_v3.json'
LOG_PATH= r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_v3.txt'
INV_PATH= r'c:\Projects\ChoongYin_OS\docs\EC\ec_full_tree_inventory.json'

os.makedirs(SS_DIR, exist_ok=True)
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


def expand_all(page, max_passes=5):
    total = 0
    for _ in range(max_passes):
        n = page.evaluate("""() => {
            let c = 0;
            document.querySelectorAll('.ui-tree-toggler.ui-icon-triangle-1-e').forEach(t => {
                t.click(); c++;
            });
            return c;
        }""")
        total += n
        if n > 0:
            page.wait_for_load_state('networkidle', timeout=6000)
            page.wait_for_timeout(400)
        if n == 0:
            break
    return total


def is_on_ec(page):
    url = page.url
    return any(x in url for x in ['xhtml', 'com.ec.', 'dashboard', 'ap-f0a7g'])


def recover_to_ec(page):
    """Return to EC dashboard and re-expand tree."""
    try:
        page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=20000)
        page.wait_for_timeout(500)
        expand_all(page)
        return True
    except:
        return False


def click_tree_label(page, screen_text):
    """Click a tv-link label that is currently visible in the tree."""
    if "'" in screen_text:
        parts = screen_text.split("'")
        xpath_val = "concat('" + "',\"'\",'".join(parts) + "')"
        sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={xpath_val}]"
    else:
        sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_text}']"
    try:
        el = page.locator(sel)
        if el.count() > 0:
            visible = el.first.is_visible()
            if visible:
                el.first.click()
                page.wait_for_load_state('networkidle', timeout=20000)
                page.wait_for_timeout(600)
                return True
    except:
        pass
    return False


# Load inventory
with open(INV_PATH, 'r', encoding='utf-8') as f:
    inventory = json.load(f)

seen = set()
screens_to_explore = []
for item in inventory:
    txt = item['text']
    if txt not in TOP_LEVEL and txt not in SKIP_SCREENS and txt not in seen and len(txt) > 2:
        seen.add(txt)
        screens_to_explore.append({'text': txt, 'section': item.get('section','?')})

print(f'Screens to explore: {len(screens_to_explore)}\n')

screen_db = {}
success = 0
skip = 0
recover_count = 0

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # Login
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    print('Logged in')

    # Expand full tree
    n = expand_all(page)
    print(f'Tree expanded: {n} togglers clicked\n')

    for i, item in enumerate(screens_to_explore):
        screen  = item['text']
        section = item['section']

        # Recover if navigated away from EC
        if not is_on_ec(page):
            recover_count += 1
            recover_to_ec(page)

        # Click the label
        ok = click_tree_label(page, screen)
        if not ok:
            skip += 1
            # Re-expand and try once more
            expand_all(page)
            ok = click_tree_label(page, screen)
            if not ok:
                screen_db[f'{section}::{screen}'] = {'name':screen,'section':section,'found':False,'screen_type':'NOT_FOUND'}
                continue

        # Analyze — wait for page to fully settle
        if not is_on_ec(page):
            recover_to_ec(page)
            screen_db[f'{section}::{screen}'] = {'name':screen,'section':section,'found':False,'screen_type':'EXTERNAL'}
            continue

        try:
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(500)
            info = page.evaluate(ANALYZE_JS, [screen, section])
            # Verify we got the right screen
            if not info.get('screen_label') and not info.get('has_navigator') and info.get('datatable_count',0) == 0:
                # Page might not be loaded yet — wait more
                page.wait_for_timeout(1000)
                info = page.evaluate(ANALYZE_JS, [screen, section])
        except Exception:
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
                page.wait_for_timeout(800)
                info = page.evaluate(ANALYZE_JS, [screen, section])
            except:
                skip += 1; continue

        info['found'] = True
        screen_db[f'{section}::{screen}'] = info
        success += 1

        # Screenshot every 20th
        if success % 20 == 0:
            ss = os.path.join(SS_DIR, f'{i+1:03d}_{screen[:15].replace(" ","_").lower()}.png')
            try: page.screenshot(path=ss)
            except: pass

        stype = info.get('screen_type','?')
        nav   = 'Y' if info.get('has_navigator') else 'N'
        dts   = info.get('datatable_count',0)
        save  = 'S' if info.get('save_enabled') else '-'
        ins   = '+' if info.get('insert_enabled') else '-'
        dele  = 'D' if info.get('delete_enabled') else '-'
        cols  = [c for dt in info.get('datatables',[]) for c in dt.get('cols',[])[:2]]
        nav_l = [la for g in info.get('nav_labels',[]) for la in g[:2]]
        label = info.get('screen_label','')[:20]
        print(f'  {i+1:03d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}] {screen[:25]:<25}|{stype:<18}|dt={dts}|nav={nav_l[:2]}|cols={cols[:2]}|"{label}"')

        # Checkpoint every 50
        if success % 50 == 0:
            with open(KB_PATH,'w',encoding='utf-8') as f: json.dump(screen_db,f,indent=2)
            print(f'  ... checkpoint: {success} ok / {skip} skip / {recover_count} recovers')

    ctx.close()
    browser.close()

# Final save
with open(KB_PATH,'w',encoding='utf-8') as f: json.dump(screen_db,f,indent=2)

print(f'\n{"="*70}')
print(f'DONE: {success} navigated | {skip} skipped | {recover_count} recoveries | Total: {len(screen_db)}')

types={}
for v in screen_db.values():
    if v.get('found'):
        t=v.get('screen_type','?')
        if t not in types: types[t]=[]
        types[t].append({'n':v.get('name',''),'s':v.get('section',''),
            'cols':[c for dt in v.get('datatables',[]) for c in dt.get('cols',[])[:2]],
            'nav':[la for g in v.get('nav_labels',[]) for la in g[:2]],
            'save':v.get('save_enabled',False),'ins':v.get('insert_enabled',False)})

for t, screens in sorted(types.items()):
    print(f'\n--- {t} ({len(screens)}) ---')
    for s in screens:
        iud=('S' if s['save'] else '-')+('+' if s['ins'] else '-')
        print(f'  {iud} [{s["s"][:12]:<12}] {s["n"]:<30} nav={s["nav"][:2]} cols={s["cols"][:2]}')

_log.close()
