
"""
EC Overnight Screen Knowledge Base Builder
PLAN:
  1. Login to local EC
  2. Expand ALL treeview sections (3 passes to get sub-sub-items)
  3. Collect ALL visible tv-link labels with their text
  4. Save full tree inventory to JSON
  5. Navigate to EACH screen in sequence (clicking label directly)
  6. For each screen: analyze, screenshot, record in DB
  7. Save knowledge base + update ec-screen-knowledge-base.md
  8. Commit to GitHub
"""
from playwright.sync_api import sync_playwright
import json, os, time

EC_URL = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
SS_DIR = r'c:\Projects\ChoongYin_OS\docs\EC\screenshots\all_screens'
KB_PATH = r'c:\tmp\ec_full_screen_kb.json'
os.makedirs(SS_DIR, exist_ok=True)

TOP_LEVEL = {
    'Dashboard','Configuration','EC Production','EC Chemistry','EC Transport',
    'EC Sales','EC Revenue','System Messages','Reporting','Process Automation',
    'Messaging','Task List','EC Integration Service'
}

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
        if (i < 4) {
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
    const screenletIds = [];
    document.querySelectorAll('[class*=formScreenlet],[class*=tableScreenlet],[class*=buttonScreenlet]').forEach(s => {
        if (s.id) screenletIds.push(s.id.substring(0,50));
    });
    r.screenlet_ids = screenletIds.slice(0,10);
    return r;
}"""


def expand_all(page):
    """Click all collapsed togglers — repeat until no more."""
    total = 0
    for pass_num in range(6):
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
            page.wait_for_timeout(500)
        if n == 0:
            break
    return total


def get_all_labels(page):
    """Get all visible tv-link labels with section context."""
    return page.evaluate("""() => {
        const items = [];
        document.querySelectorAll("label[class*='tv-link'],span[class*='tv-link']").forEach(el => {
            if (!el.offsetParent) return;
            const text = el.textContent.trim();
            if (!text || text.length < 2) return;

            // Find depth and section by walking up the tree
            let depth = 0;
            let section = '';
            let li = el.closest('li');
            while (li) {
                depth++;
                const parentUl = li.parentElement;
                if (!parentUl) break;
                const parentLi = parentUl.closest('li');
                if (!parentLi) {
                    const lbl = li.querySelector('.ui-treenode-label');
                    section = lbl ? lbl.textContent.trim() : li.querySelector('label')?.textContent?.trim()||'?';
                    break;
                }
                li = parentLi;
            }
            items.push({text, section, depth, id: el.id||''});
        });
        return items;
    }""")


def click_label(page, screen_text):
    """Click a tv-link label in the treeview."""
    # Escape single quotes for XPath
    if "'" in screen_text:
        # Use concat for XPath with single quotes
        parts = screen_text.split("'")
        xpath_text = "concat('" + "',\"'\",'".join(parts) + "')"
        sel = (f"xpath=//*[self::label or self::span]"
               f"[contains(@class,'tv-link') and normalize-space(text())={xpath_text}]")
    else:
        sel = (f"xpath=//*[self::label or self::span]"
               f"[contains(@class,'tv-link') and normalize-space(text())='{screen_text}']")
    try:
        el = page.locator(sel)
        if el.count() > 0:
            el.first.click()
            page.wait_for_load_state('networkidle', timeout=15000)
            page.wait_for_timeout(500)
            return True
        return False
    except Exception as e:
        return False


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # ── LOGIN ────────────────────────────────────────────────────────────────
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', 'sysadmin')
    page.fill('#password', 'sysadmin')
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    print('=== LOGGED IN ===\n')

    # ── PHASE 1: EXPAND ENTIRE TREE ──────────────────────────────────────────
    print('PHASE 1: Expanding full treeview...')
    total_expanded = expand_all(page)
    print(f'  Total togglers clicked: {total_expanded}')
    page.screenshot(path=SS_DIR + r'\_00_full_tree.png')

    # Collect all labels
    all_labels = get_all_labels(page)
    print(f'  Total visible items: {len(all_labels)}')

    # Save tree inventory
    with open(r'c:\tmp\ec_tree_inventory.json', 'w', encoding='utf-8') as f:
        json.dump(all_labels, f, indent=2, ensure_ascii=False)

    # Filter to navigable screens (not top-level sections)
    seen_texts = set()
    navigable = []
    for item in all_labels:
        txt = item['text']
        if txt not in TOP_LEVEL and txt not in seen_texts and len(txt) > 2:
            seen_texts.add(txt)
            navigable.append(item)

    print(f'  Unique navigable screens: {len(navigable)}')
    print('\nFull screen list:')
    for item in navigable:
        print(f'  [{item["section"][:15]:<15}] d={item["depth"]} {item["text"]}')

    # ── PHASE 2: NAVIGATE TO EACH SCREEN ─────────────────────────────────────
    print(f'\nPHASE 2: Navigating to {len(navigable)} screens...\n')

    screen_db = {}
    success_count = 0
    fail_count = 0

    for i, item in enumerate(navigable):
        screen = item['text']
        section = item['section']

        # Click the label
        ok = click_label(page, screen)
        if not ok:
            print(f'  {i+1:03d} SKIP  [{section[:10]}] {screen}')
            fail_count += 1
            continue

        # Check if we're still on EC (not navigated to external)
        if 'energycomponents' not in page.url and page.url.startswith('http'):
            # Might have navigated away — go back
            page.go_back()
            page.wait_for_load_state('networkidle', timeout=10000)

        # Analyze
        info = page.evaluate(ANALYZE_JS, [screen, section])
        info['found'] = True
        screen_db[f'{section}::{screen}'] = info
        success_count += 1

        # Screenshot
        ss_name = f'{i+1:03d}_{screen[:15].replace(" ","_").replace("/","_").lower()}.png'
        page.screenshot(path=os.path.join(SS_DIR, ss_name))

        stype = info.get('screen_type', '?')
        nav   = 'Y' if info.get('has_navigator') else 'N'
        dts   = info.get('datatable_count', 0)
        save  = 'S' if info.get('save_enabled')   else '-'
        ins   = '+' if info.get('insert_enabled')  else '-'
        dele  = 'D' if info.get('delete_enabled')  else '-'
        cols  = [c for dt in info.get('datatables', []) for c in dt.get('cols', [])[:3]]
        nav_l = [la for g in info.get('nav_labels', []) for la in g[:2]]
        btns  = info.get('action_buttons', [])[:2]
        label = info.get('screen_label', '')[:22]

        print(f'  {i+1:03d}[{section[:10]:<10}]{save}{ins}{dele}[{nav}]'
              f' {screen[:25]:<25}|{stype[:16]:<16}|dt={dts}'
              f'|nav={nav_l[:2]}|cols={cols[:3]}|"{label}"')

        # Periodic save
        if (i+1) % 20 == 0:
            with open(KB_PATH, 'w', encoding='utf-8') as f:
                json.dump(screen_db, f, indent=2, ensure_ascii=False)
            print(f'  ... checkpoint saved ({success_count} screens)')

    ctx.close()
    browser.close()

# ── PHASE 3: SAVE KNOWLEDGE BASE ─────────────────────────────────────────────
print(f'\n{"="*80}')
print(f'PHASE 3: Saving knowledge base...')
with open(KB_PATH, 'w', encoding='utf-8') as f:
    json.dump(screen_db, f, indent=2, ensure_ascii=False)

print(f'Explored: {success_count} screens | Failed: {fail_count}')

# ── PHASE 4: GENERATE SUMMARY REPORT ─────────────────────────────────────────
print(f'\n{"="*80}')
print('COMPLETE SCREEN KNOWLEDGE BASE')
print(f'{"="*80}')

# Group by section + type
by_section: dict = {}
for key, v in screen_db.items():
    sec = v.get('section', 'Unknown')
    if sec not in by_section:
        by_section[sec] = []
    by_section[sec].append(v)

for sec, screens in sorted(by_section.items()):
    print(f'\n[{sec}] — {len(screens)} screens')
    for s in screens:
        stype = s.get('screen_type','?')
        iud = ('S' if s.get('save_enabled') else '-') + \
              ('+' if s.get('insert_enabled') else '-') + \
              ('D' if s.get('delete_enabled') else '-')
        nav_l = [la for g in s.get('nav_labels',[]) for la in g[:2]]
        cols = [c for dt in s.get('datatables',[]) for c in dt.get('cols',[])[:2]]
        print(f'  {iud} [{stype[:16]:<16}] {s.get("name",""):<30}'
              f' nav={nav_l[:2]} cols={cols[:2]}')

print(f'\nSaved to: {KB_PATH}')
