"""
EC KB Rebuilder + Full Exploration
- Merge-safe: reads KB, merges new results, never overwrites with fewer entries
- Uses both tree expansion AND search to find screens
- Accumulates across all runs
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL   = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
KB_PATH  = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_final.json'
LOG_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_rebuild_log.txt'
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


def merge_save(screen_db, new_entries):
    """Merge-safe save: load existing file, merge, save — never reduces entry count."""
    existing = {}
    if os.path.exists(KB_PATH):
        try:
            with open(KB_PATH, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except:
            pass
    # Merge: prefer found=True over found=False
    merged = dict(existing)
    for k, v in new_entries.items():
        if k not in merged or (v.get('found') and not merged[k].get('found')):
            merged[k] = v
    with open(KB_PATH, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    return merged


def expand_all(page, passes=5):
    total = 0
    for _ in range(passes):
        n = page.evaluate("""() => {
            let c = 0;
            document.querySelectorAll('.ui-tree-toggler.ui-icon-triangle-1-e').forEach(t => {
                t.click(); c++;
            });
            return c;
        }""")
        total += n
        if n > 0:
            page.wait_for_load_state('networkidle', timeout=5000)
            page.wait_for_timeout(300)
        if n == 0: break
    return total


def is_on_ec(page):
    return any(x in page.url for x in ['xhtml', 'com.ec.', 'ap-f0a7g'])


def navigate_by_label(page, screen_text):
    if "'" in screen_text:
        parts = screen_text.split("'")
        xv = "concat('" + "',\"'\",'".join(parts) + "')"
        sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={xv}]"
    else:
        sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_text}']"
    try:
        el = page.locator(sel)
        if el.count() > 0 and el.first.is_visible():
            el.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(500)
            return is_on_ec(page)
    except:
        pass
    return False


def navigate_by_search(page, screen_text):
    try:
        si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
        si.wait_for(state='visible', timeout=5000)
        si.clear()
        si.type(screen_text[:35], delay=50)
        page.wait_for_load_state('networkidle', timeout=6000)
        page.wait_for_timeout(300)
        if "'" in screen_text:
            parts = screen_text.split("'")
            xv = "concat('" + "',\"'\",'".join(parts) + "')"
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={xv}]"
        else:
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_text}']"
        el = page.locator(sel)
        if el.count() > 0 and el.first.is_visible():
            el.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(500)
            if not is_on_ec(page):
                page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
                return False
            return True
    except:
        pass
    return False


# Load inventory
with open(INV_PATH, 'r', encoding='utf-8') as f:
    inventory = json.load(f)

# Load current KB
current_kb = {}
if os.path.exists(KB_PATH):
    try:
        with open(KB_PATH, 'r', encoding='utf-8') as f:
            current_kb = json.load(f)
    except:
        pass

already_found = sum(1 for v in current_kb.values() if v.get('found'))
print(f'Current KB: {len(current_kb)} entries | {already_found} already found')

# Build unique list of all screens
seen = set()
all_screens = []
for item in inventory:
    txt = item['text']
    if txt not in TOP_LEVEL and txt not in SKIP_SCREENS and txt not in seen and len(txt) > 2:
        seen.add(txt)
        all_screens.append({'text': txt, 'section': item.get('section','?')})

# Screens not yet found
to_explore = [s for s in all_screens
              if not current_kb.get(f'{s["section"]}::{s["text"]}', {}).get('found', False)]
print(f'Total screens: {len(all_screens)} | Not yet found: {len(to_explore)}\n')

session_db = {}  # results from THIS session only
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
    print('Logged in')

    # Expand tree
    n = expand_all(page)
    print(f'Tree expanded: {n} togglers\n')

    for i, item in enumerate(to_explore):
        screen  = item['text']
        section = item['section']
        key     = f'{section}::{screen}'

        if not is_on_ec(page):
            try:
                page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
                expand_all(page)
            except:
                pass

        # Try label click first (faster), then search fallback
        ok = navigate_by_label(page, screen)
        if not ok:
            ok = navigate_by_search(page, screen)

        if not ok:
            skip += 1
            session_db[key] = {'name':screen,'section':section,'found':False,'screen_type':'NOT_FOUND'}
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
        session_db[key] = info
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
        print(f'  {i+1:03d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}] {screen[:25]:<25}|{stype:<16}|dt={dts}|nav={nav_l[:2]}|cols={cols[:2]}|"{label}"')

        # Merge-safe checkpoint save every 25 screens
        if success % 25 == 0:
            merged = merge_save(current_kb, session_db)
            total = sum(1 for v in merged.values() if v.get('found'))
            print(f'  ... saved: {total} total found ({success} this run)')

    ctx.close()
    browser.close()

# Final merge-safe save
merged = merge_save(current_kb, session_db)
total_found = sum(1 for v in merged.values() if v.get('found'))
print(f'\n{"="*70}')
print(f'DONE: {total_found}/{len(all_screens)} total found | +{success} this run | {skip} skipped')
print(f'Saved to: {KB_PATH}')
_log.close()
