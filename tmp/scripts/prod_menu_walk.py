"""Business-domain dive 1: EC Production menu walk (read-only).
Expand the EC Production branch in the treeview, inventory sections + screens."""
import json
import os
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/biz_domains")
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=60000)
    page.fill('[id="username"]', "sysadmin")
    page.fill('[id="password"]', "sysadmin")
    page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000)
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(1)

    # expand "EC Production" root node
    root = page.locator('xpath=//*[contains(@class,"tv-link") or self::span or self::label][normalize-space(text())="EC Production"]')
    print("root matches:", root.count())
    root.first.click()
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(2)

    # iteratively expand all collapsed nodes under the Production subtree (up to 6 passes)
    for i in range(6):
        n = page.evaluate("""() => {
            const togglers = [...document.querySelectorAll('.ui-tree-toggler.ui-icon-triangle-1-e, .ui-treenode-collapsed > .ui-treenode-content .ui-tree-toggler')]
                .filter(e => e.offsetParent);
            togglers.slice(0, 25).forEach(t => t.click());
            return togglers.length; }""")
        print(f"pass {i}: clicked {min(n,25)} of {n} collapsed togglers")
        if n == 0:
            break
        page.wait_for_load_state("networkidle", timeout=20000)
        time.sleep(2.5)

    tree = page.evaluate("""() => {
        // dump the visible tree as indented text using DOM nesting depth
        const out = [];
        document.querySelectorAll('[id="menu:tvForm:treeView"] li, .ui-treenode').forEach(li => {
            const lbl = li.querySelector(':scope > .ui-treenode-content .ui-treenode-label, :scope > div .tv-link, :scope > span');
            if (!lbl || !lbl.offsetParent) return;
            let depth = 0, n = li.parentElement;
            while (n && n.id !== 'menu:tvForm:treeView') { if (n.tagName === 'UL' || n.classList.contains('ui-treenode-children')) depth++; n = n.parentElement; }
            out.push('  '.repeat(depth) + (lbl.textContent||'').trim());
        });
        return out; }""")
    print(f"tree nodes: {len(tree)}")
    (OUT / "production_tree.txt").write_text("\n".join(tree), encoding="utf-8")
    page.screenshot(path=str(OUT / "production_tree.png"), full_page=True)
    print("\n".join(tree[:60]))
    browser.close()
