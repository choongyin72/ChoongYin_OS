"""Confirm the treeview breadcrumb for 'Contract Area' (folder placement). Search it, read the tv-link's
title/ancestor folder labels. READ-ONLY. Usage: py -X utf8 tmp/scripts/ca_treepath.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PWD", "sysadmin")


def esc(i):
    return "#" + i.replace(":", "\\:")


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1700, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(2500)
    page.fill("#username", USER); page.fill("#password", PWD)
    page.locator("#kc-login").first.click(); page.wait_for_timeout(3500)
    box = page.locator(esc("menu:searchForm:searchTxt"))
    box.click(); box.type("Contract Area", delay=40); page.wait_for_timeout(2500)
    # the search result tv-link + its title (EC often stores the full menu path in title=)
    info = page.evaluate("""() => {
        const links=[...document.querySelectorAll('.tv-link')].filter(e=>e.textContent.trim()==='Contract Area');
        return links.map(e=>{ let anc=[]; let n=e; for(let i=0;i<14&&n;i++){ n=n.parentElement;
            if(n){const l=n.querySelector(':scope > .ui-treenode-content .ui-treenode-label, :scope > .tv-folder, :scope > span.tv-link');
                if(l && l!==e){const t=(l.textContent||'').trim(); if(t&&!anc.includes(t)) anc.push(t);}}}
            return {text:e.textContent.trim(), title:e.getAttribute('title')||e.getAttribute('data-tooltip')||'',
                    parentTitle:(e.closest('[title]')||{}).title||'', ancestors:anc}; }); }""")
    print("Contract Area tv-link info:")
    for r in info:
        print("  text :", r["text"])
        print("  title:", r["title"])
        print("  ancestors(DOM, nearest-first):", r["ancestors"])
    b.close()
print("DONE")
