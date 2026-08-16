"""
EC Full Screen Knowledge Base — Final approach
Uses SEARCH BOX for each screen navigation (tree-state independent).
1. Login
2. Expand full tree once → collect all 545+ screen names
3. For each screen: search by name → click result → analyze → screenshot
4. Save KB to project logs folder
5. Commit to GitHub
"""
from playwright.sync_api import sync_playwright
import json, os, sys

EC_URL  = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR  = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\all_screens'
KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb.json'
LOG_PATH= r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_final.txt'
INV_PATH= r'c:\Projects\ChoongYin_OS\docs\EC\ec_full_tree_inventory.json'

os.makedirs(SS_DIR, exist_ok=True)
os.makedirs(r'c:\Projects\ChoongYin_OS\tmp\logs', exist_ok=True)

# Tee stdout to log file
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

# Screens to SKIP (external links or known problematic)
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
                const t = th.textContent.trim();
                if (t) cols.push(t.substring(0, 25));
            });
            const filters = [];
            dt.querySelectorAll('input[id*=sfilter],input[id*=filter]').forEach(f =>
                filters.push(f.id.substring(0,50)));
            r.datatables.push({
                id: dt.id.substring(0,50),
                cols: cols.slice(0,10),
                rows: dt.querySelectorAll('tbody tr').length,
                filters: filters.slice(0,5)
            });
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
    const slIds = [];
    document.querySelectorAll('[class*=formScreenlet],[class*=tableScreenlet],[class*=buttonScreenlet]').forEach(s => {
        if (s.id) slIds.push(s.id.substring(0,50));
    });
    r.screenlet_ids = slIds.slice(0,10);
    return r;
}"""


def search_navigate(page, screen_name):
    """Navigate to screen via search box. Returns True/False."""
    try:
        si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
        # Make sure search is visible
        si.wait_for(state='visible', timeout=8000)
        si.clear()
        si.type(screen_name[:35], delay=40)  # type() triggers PrimeFaces AJAX keyup
        page.wait_for_load_state('networkidle', timeout=8000)
        page.wait_for_timeout(300)

        # Find exact match
        if "'" in screen_name:
            parts = screen_name.split("'")
            xpath_val = "concat('" + "',\"'\",'".join(parts) + "')"
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={xpath_val}]"
        else:
            sel = f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_name}']"

        el = page.locator(sel)
        if el.count() > 0 and el.first.is_visible():
            el.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(400)
            # Verify navigation worked (not on external page)
            if 'energycomponents.com' in page.url or 'localhost' in page.url or page.url.startswith('https://ap-'):
                return True
            # Might have gone to external — go back to EC
            page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
            return False
        return False
    except Exception as e:
        return False


def ensure_on_ec(page):
    """Make sure we're on the EC app."""
    if 'xhtml' not in page.url and 'com.ec' not in page.url:
        try:
            page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
            page.wait_for_timeout(300)
        except:
            pass


# ── LOAD SCREEN LIST ─────────────────────────────────────────────────────────
# Load from previously saved inventory
with open(INV_PATH, 'r', encoding='utf-8') as f:
    inventory = json.load(f)

seen = set()
screens_to_explore = []
for item in inventory:
    txt = item['text']
    if txt not in TOP_LEVEL and txt not in SKIP_SCREENS and txt not in seen and len(txt) > 2:
        seen.add(txt)
        screens_to_explore.append({'text': txt, 'section': item.get('section','?'), 'depth': item.get('depth',1)})

print(f'Total screens to explore: {len(screens_to_explore)}\n')

# ── RUN EXPLORATION ──────────────────────────────────────────────────────────
screen_db = {}
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

    for i, item in enumerate(screens_to_explore):
        screen  = item['text']
        section = item['section']

        # Navigate via search
        ensure_on_ec(page)
        ok = search_navigate(page, screen)

        if not ok:
            skip += 1
            if skip <= 20 or skip % 50 == 0:
                print(f'  {i+1:03d} SKIP  [{section[:12]}] {screen}')
            screen_db[f'{section}::{screen}'] = {
                'name': screen, 'section': section, 'found': False,
                'screen_type': 'NOT_FOUND'
            }
            continue

        # Analyze
        try:
            page.wait_for_load_state('domcontentloaded', timeout=8000)
            page.wait_for_timeout(200)
            info = page.evaluate(ANALYZE_JS, [screen, section])
        except Exception as e:
            try:
                page.wait_for_load_state('networkidle', timeout=8000)
                info = page.evaluate(ANALYZE_JS, [screen, section])
            except:
                skip += 1
                continue

        info['found'] = True
        screen_db[f'{section}::{screen}'] = info
        success += 1

        # Screenshot every 10th screen to save disk space
        if success % 10 == 0:
            ss = os.path.join(SS_DIR, f'{i+1:03d}_{screen[:15].replace(" ","_").lower()}.png')
            try:
                page.screenshot(path=ss)
            except:
                pass

        # Print result
        stype = info.get('screen_type', '?')
        nav   = 'Y' if info.get('has_navigator') else 'N'
        dts   = info.get('datatable_count', 0)
        save  = 'S' if info.get('save_enabled')   else '-'
        ins   = '+' if info.get('insert_enabled')  else '-'
        dele  = 'D' if info.get('delete_enabled')  else '-'
        cols  = [c for dt in info.get('datatables', []) for c in dt.get('cols', [])[:3]]
        nav_l = [la for g in info.get('nav_labels', []) for la in g[:2]]
        label = info.get('screen_label', '')[:20]
        print(f'  {i+1:03d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}]'
              f' {screen[:25]:<25}|{stype:<18}|dt={dts}'
              f'|nav={nav_l[:2]}|cols={cols[:2]}|"{label}"')

        # Checkpoint save every 50 screens
        if success % 50 == 0:
            with open(KB_PATH, 'w', encoding='utf-8') as f:
                json.dump(screen_db, f, indent=2, ensure_ascii=False)
            print(f'  ... checkpoint: {success} ok / {skip} skipped')

    ctx.close()
    browser.close()

# Final save
with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(screen_db, f, indent=2, ensure_ascii=False)

print(f'\n{"="*70}')
print(f'COMPLETE: {success} navigated | {skip} skipped | Total: {len(screen_db)}')

# Summary by type
types: dict = {}
for v in screen_db.values():
    if v.get('found'):
        t = v.get('screen_type', '?')
        if t not in types: types[t] = []
        types[t].append({
            'n': v.get('name',''), 's': v.get('section',''),
            'cols': [c for dt in v.get('datatables',[]) for c in dt.get('cols',[])[:2]],
            'nav':  [la for g in v.get('nav_labels',[]) for la in g[:2]],
            'save': v.get('save_enabled',False),
            'ins':  v.get('insert_enabled',False),
        })

for t, screens in sorted(types.items()):
    print(f'\n--- {t} ({len(screens)}) ---')
    for s in screens:
        iud = ('S' if s['save'] else '-') + ('+' if s['ins'] else '-')
        print(f'  {iud} [{s["s"][:12]:<12}] {s["n"]:<30} nav={s["nav"][:2]} cols={s["cols"][:2]}')

_log.close()
