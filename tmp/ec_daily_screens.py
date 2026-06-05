
"""
Navigate to key daily/monthly production screens and build knowledge base.
Targets: Check Rules, Validation, Daily Status, Monthly Status, Allocation etc.
"""
from playwright.sync_api import sync_playwright
import json, os

EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\daily_monthly'
os.makedirs(SS_DIR, exist_ok=True)

# Key screens for Woodside Pluto daily work — grouped by area
TARGET_SCREENS = [
    # Check Rules & Validation
    ('Check/Validation', 'Maintain Check Rule'),
    ('Check/Validation', 'Check Rule'),
    ('Check/Validation', 'Validation Overview'),
    ('Check/Validation', 'Class Validation'),
    ('Check/Validation', 'Object Validation - Default'),
    # Daily Production Operations
    ('Daily Production', 'Daily Oil Stream Status'),
    ('Daily Production', 'Daily Gas Stream Status'),
    ('Daily Production', 'Daily Water Stream Status'),
    ('Daily Production', 'Daily Stream Status'),
    ('Daily Production', 'Daily Production Well Status 1'),
    ('Daily Production', 'Daily Production Well Status 2'),
    ('Daily Production', 'Daily Production Well Status 3'),
    ('Daily Production', 'Daily Tank Status'),
    ('Daily Production', 'Daily Tank Status - Mass'),
    ('Daily Production', 'Daily Dashboard'),
    ('Daily Production', 'Stream Component Analysis'),
    ('Daily Production', 'Stream Analysis'),
    # Monthly Production
    ('Monthly Production', 'Monthly Production Well Status'),
    ('Monthly Production', 'Monthly Allocated Production Well Data'),
    ('Monthly Production', 'Monthly Gas Injection Well Status'),
    ('Monthly Production', 'Monthly Water Injection Well Status'),
    # Allocation / HC Accounting
    ('Allocation', 'Daily Allocation'),
    ('Allocation', 'Daily Allocation - Single Date'),
    ('Allocation', 'Monthly Allocation'),
    ('Allocation', 'Daily Data Status Process'),
    ('Allocation', 'Allocation Network'),
    # Sub-daily
    ('Sub-Daily', 'Sub Daily Production Well Status 1 - by Well'),
    ('Sub-Daily', 'Sub Daily Production Well Status 1 - by Period'),
    ('Sub-Daily', 'Sub Daily Gas Injection Well Status'),
    # Well Management
    ('Well Mgmt', 'Well Finder'),
    ('Well Mgmt', 'Maintain Well Status'),
    ('Well Mgmt', 'Maintain Production Well Status'),
    ('Well Mgmt', 'Production Test Define'),
    ('Well Mgmt', 'Production Test Result'),
    # Configuration
    ('Config', 'Maintain Check Rules'),
    ('Config', 'Manage Well'),
    ('Config', 'Manage Stream'),
    ('Config', 'Manage Facility'),
    ('Config', 'Initiate Day'),
    ('Config', 'Production Day Table'),
    ('Config', 'Schedules'),
    ('Config', 'Business Actions'),
    ('Config', 'Adapter Configuration'),
    ('Config', 'Maintain Mappings'),
]

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
            if (t.length > 1 && t.length < 30) labels.push(t);
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
                if (t) cols.push(t.substring(0, 22));
            });
            r.datatables.push({id: dt.id.substring(0,40), cols: cols.slice(0,8),
                                rows: dt.querySelectorAll('tbody tr').length});
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
        if (t && t.length > 1) btns.add(t.substring(0,25));
    });
    r.action_buttons = [...btns].slice(0,5);
    return r;
}"""


def search_and_click(page, screen_name):
    """Search for a screen and click it if found."""
    # Use the search box
    si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
    try:
        si.fill(screen_name[:30], timeout=5000)
    except:
        # Search input not visible — navigate to dashboard first
        page.goto(EC_URL + 'xhtml/pages/dashboard.jsf', wait_until='networkidle', timeout=15000)
        si = page.locator("xpath=//input[@id='menu:searchForm:searchTxt']")
        si.fill(screen_name[:30], timeout=5000)

    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(300)

    # Try exact match first
    sel = (f"xpath=//*[self::label or self::span]"
           f"[contains(@class,'tv-link') and normalize-space(text())='{screen_name}']")
    el = page.locator(sel)
    if el.count() > 0:
        el.first.click()
        page.wait_for_load_state('networkidle', timeout=20000)
        page.wait_for_timeout(600)
        return True, 'exact'

    # Try partial match
    sel2 = (f"xpath=//*[self::label or self::span]"
            f"[contains(@class,'tv-link') and contains(normalize-space(text()),'{screen_name[:15]}')]")
    el2 = page.locator(sel2)
    if el2.count() > 0:
        found_text = el2.first.text_content()
        el2.first.click()
        page.wait_for_load_state('networkidle', timeout=20000)
        page.wait_for_timeout(600)
        return True, f'partial:{found_text.strip()[:25]}'

    return False, 'not_found'


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # LOGIN
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    print('Logged in\n')

    screen_db = {}

    print(f'Exploring {len(TARGET_SCREENS)} target screens...\n')

    for i, (section, screen) in enumerate(TARGET_SCREENS):
        ok, match_type = search_and_click(page, screen)
        if not ok:
            print(f'  {i+1:02d} NOT FOUND [{section}] {screen}')
            screen_db[f'{section}::{screen}'] = {
                'name': screen, 'section': section,
                'screen_type': 'NOT_FOUND', 'found': False
            }
            continue

        info = page.evaluate(ANALYZE_JS, [screen, section])
        info['found'] = True
        info['match_type'] = match_type
        screen_db[f'{section}::{screen}'] = info

        ss = os.path.join(SS_DIR, f'{i+1:02d}_{screen[:18].replace(" ","_").lower()}.png')
        page.screenshot(path=ss)

        stype = info.get('screen_type', '?')
        nav   = 'Y' if info.get('has_navigator') else 'N'
        dts   = info.get('datatable_count', 0)
        save  = 'S' if info.get('save_enabled')   else '-'
        ins   = '+' if info.get('insert_enabled')  else '-'
        dele  = 'D' if info.get('delete_enabled')  else '-'
        cols  = [c for dt in info.get('datatables', []) for c in dt.get('cols', [])[:3]]
        nav_l = [la for g in info.get('nav_labels', []) for la in g[:2]]
        btns  = info.get('action_buttons', [])[:2]
        label = info.get('screen_label', '')[:20]

        print(f'  {i+1:02d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}]'
              f' {screen[:25]:<25}|{stype:<18}|dt={dts}'
              f'|nav={nav_l[:3]}|cols={cols[:3]}|btns={btns}|"{label}"|{match_type}')

    ctx.close()
    browser.close()

# Save
with open(r'c:\tmp\ec_daily_monthly_kb.json', 'w', encoding='utf-8') as f:
    json.dump(screen_db, f, indent=2, ensure_ascii=False)

print(f'\n{"="*80}')
print(f'SCREENS CAPTURED: {len([v for v in screen_db.values() if v.get("found")])} / {len(screen_db)}')

# Summary by type
types: dict = {}
not_found = []
for key, v in screen_db.items():
    if not v.get('found'):
        not_found.append(v.get('name', ''))
        continue
    t = v.get('screen_type', '?')
    if t not in types:
        types[t] = []
    types[t].append({
        'n': v.get('name', ''),
        's': v.get('section', ''),
        'cols': [c for dt in v.get('datatables', []) for c in dt.get('cols', [])[:2]],
        'nav': [la for g in v.get('nav_labels', []) for la in g[:2]],
        'save': v.get('save_enabled', False),
        'ins':  v.get('insert_enabled', False),
    })

for t, screens in sorted(types.items()):
    print(f'\n--- {t} ({len(screens)}) ---')
    for s in screens:
        iud = ('S' if s['save'] else '-') + ('+' if s['ins'] else '-')
        print(f'  {iud} [{s["s"][:12]:<12}] {s["n"]:<30} nav={s["nav"][:2]} cols={s["cols"][:2]}')

if not_found:
    print(f'\n--- NOT FOUND ({len(not_found)}) ---')
    for n in not_found:
        print(f'  - {n}')
