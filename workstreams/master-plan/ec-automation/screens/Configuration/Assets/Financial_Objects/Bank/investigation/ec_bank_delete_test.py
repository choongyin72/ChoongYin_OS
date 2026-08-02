"""
Test Playwright native row click + delete hover for Bank Manage Object screen.
Determines the exact delete pattern for AUTOTEST_BNK_001.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import os


def _repo_root() -> Path:
    env = os.environ.get('REPO_ROOT')
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for parent in [here, *here.parents]:
        if (parent / '.git').exists():
            return parent
    return here.parents[5]


EC_URL    = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
SS_DIR    = str(_repo_root() / 'docs' / 'EC' / 'screenshots' / 'iud_bank')
TEST_CODE = 'AUTOTEST_BNK_001'
os.makedirs(SS_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = browser.new_context(ignore_https_errors=True, viewport={'width': 1920, 'height': 1080})
    page = ctx.new_page()

    # Login + navigate to Bank
    page.goto(EC_URL, wait_until='domcontentloaded', timeout=30000)
    page.fill('#username', os.environ.get("EC_USER", "sysadmin")); page.fill('#password', os.environ.get("EC_PASS", "sysadmin"))
    page.click('#kc-login')
    page.wait_for_url('**/dashboard**', timeout=60000)
    page.wait_for_load_state('networkidle', timeout=30000)
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state='visible'); si.clear(); si.type('Bank', delay=60)
    page.wait_for_load_state('networkidle', timeout=8000)
    page.wait_for_timeout(400)
    page.locator(
        "xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Bank']"
    ).first.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(1500)
    print('Bank screen loaded')

    # --- STEP 1: Native Playwright click on AUTOTEST span in the table ---
    print(f'\n[1] Clicking AUTOTEST row via Playwright native click')
    # Click the span containing the Bank Code
    code_span = page.locator(
        f"css=#manage_object_nav_nav\\:form\\:T_data span"
    ).filter(has_text=TEST_CODE).first
    print(f'  Span count: {page.locator(f"css=#manage_object_nav_nav\\:form\\:T_data span").filter(has_text=TEST_CODE).count()}')
    code_span.click()
    page.wait_for_load_state('networkidle', timeout=15000)
    page.wait_for_timeout(2500)  # Extra wait for toolbar to update
    page.screenshot(path=os.path.join(SS_DIR, 'del_01_after_native_click.png'))

    # --- STEP 2: Check delete button state after native click ---
    del_state = page.evaluate("""() => {
        const del_li = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete)');
        const del_a  = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete) > a');
        const del_ul = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete) > ul');
        return {
            li_cls: del_li ? del_li.className : 'not found',
            a_cls:  del_a  ? del_a.className  : 'not found',
            ul_found: !!del_ul,
            ul_items: del_ul ? del_ul.querySelectorAll('li a').length : 0,
            ul_html:  del_ul ? del_ul.outerHTML.substring(0,500) : 'no ul'
        };
    }""")
    print(f'\n[2] Delete button state after native row click:')
    print(f'  li_cls : {del_state["li_cls"]}')
    print(f'  a_cls  : {del_state["a_cls"]}')
    print(f'  ul_found: {del_state["ul_found"]}, items: {del_state["ul_items"]}')
    print(f'  ul_html: {del_state["ul_html"][:200]}')

    # --- STEP 3: Hover the delete LI to trigger submenu load ---
    print('\n[3] Hovering delete LI...')
    del_li = page.locator("css=li.ui-menu-parent:has(.ui-icon-delete)")
    if del_li.count() > 0:
        del_li.first.hover()
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SS_DIR, 'del_02_after_delete_hover.png'))

        del_state2 = page.evaluate("""() => {
            const del_ul = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete) > ul');
            const del_li = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete)');
            const items = del_ul ? Array.from(del_ul.querySelectorAll('li a')).map(a => ({
                text: a.textContent.trim(), cls: a.className.substring(0,80), visible: !!a.offsetParent
            })) : [];
            return {
                li_cls: del_li ? del_li.className : '',
                ul_found: !!del_ul, items: items
            };
        }""")
        print(f'  After hover - li_cls: {del_state2["li_cls"]}')
        print(f'  After hover - ul_found: {del_state2["ul_found"]}, items: {del_state2["items"]}')
    else:
        print('  Delete LI not found!')

    # --- STEP 4: Try clicking delete via keyboard Ctrl+D ---
    print('\n[4] Trying Ctrl+D...')
    page.keyboard.press('Control+d')
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(SS_DIR, 'del_03_after_ctrl_d.png'))

    # Check if any dialog appeared
    dialogs = page.evaluate("""() => {
        const dlgs = [];
        document.querySelectorAll('.ui-dialog[aria-hidden="false"], .ui-dialog:not([style*="display: none"])').forEach(d => {
            dlgs.push({id:d.id, text:d.textContent.trim().substring(0,200)});
        });
        return dlgs;
    }""")
    print(f'  Dialogs after Ctrl+D: {dialogs}')

    # Also check EC messages
    msgs = page.evaluate("""() => {
        const n = document.getElementById('ECNotificationArea');
        return n ? n.textContent.trim().substring(0,300) : '';
    }""")
    print(f'  EC messages: {msgs[:200] if msgs else "none"}')

    # --- STEP 5: Check if toolbar delete button changed ---
    del_after_ctrl_d = page.evaluate("""() => {
        const del_li = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete)');
        const del_ul = document.querySelector('li.ui-menu-parent:has(.ui-icon-delete) > ul.ui-menu-child');
        const items = del_ul ? Array.from(del_ul.querySelectorAll('li a')).map(a => ({
            text: a.textContent.trim(), dis: a.classList.contains('ui-state-disabled'),
            onclick: (a.getAttribute('onclick') || '').substring(0,200)
        })) : [];
        return {li_cls: del_li ? del_li.className : '', items};
    }""")
    print(f'\n[5] Delete state after Ctrl+D: {del_after_ctrl_d}')

    # --- STEP 6: Check if Save is now enabled (delete pending?) ---
    save_state = page.evaluate("""() => {
        const s = document.querySelector("a[title='Save [Ctrl+s]']");
        return s ? {disabled: s.classList.contains('ui-state-disabled'), cls: s.className.substring(0,60)} : {found:false};
    }""")
    print(f'\n[6] Save after Ctrl+D: {save_state}')

    # Full toolbar HTML now
    toolbar_final = page.evaluate("""() => {
        const t = document.getElementById('screenToolbar:form:menuBar');
        return t ? t.outerHTML.substring(0, 6000) : 'not found';
    }""")
    print(f'\n[7] Full toolbar HTML:\n{toolbar_final}')

    ctx.close()
    browser.close()
print('\nDone. Check screenshots:', SS_DIR)
