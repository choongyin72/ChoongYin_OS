"""Dump the FULL raw ids (row+col+group) of every nav dropdown/date on Tract, before any
selection, to determine the real navigator shape (single group same-row cascade vs multi-group
per-field), plus confirm GO button id, grid id, and objectForm parent-dd location.
Read-only recon - no Save/Insert/Delete actions."""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Tract"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    tv_link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first
    tv_link.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    page.wait_for_timeout(1500)

    print("=== BEFORE any selection: all nav:form:G: fields (full id) + label ===")
    fields = page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:G:']")]
        .filter(e => e.id.match(/:(dd|da)_input$/))
        .map(e => {
            const row = e.closest('tr');
            const labelCell = row ? row.querySelector('td:first-child, label') : null;
            return {id: e.id, label: labelCell ? (labelCell.innerText||'').trim() : '(no label found)'};
        })""")
    for f in fields:
        print(f"  {f['id']:45s} label={f['label']}")

    print("\n=== fieldsets present + GO button candidates ===")
    extra = page.evaluate("""() => {
        const fs = [...document.querySelectorAll('fieldset[id^="nav:form:G:"]')].map(f => f.id);
        const go = ['go_button:form:B','button:form:B','navButton:form:B','nav:form:B']
            .filter(id=>document.getElementById(id));
        const anyBtn = [...document.querySelectorAll('button[id*="nav"]')].map(e=>e.id);
        return {fieldsets: fs, go, anyBtn};
    }""")
    print(extra)

    print("\n=== per-group tableRow structure (mandatory class + labels) ===")
    for gid in extra["fieldsets"]:
        rows = page.evaluate("""(gid) => [...document.querySelectorAll(`[id^="${gid}:FS"] .tableRow, [id="${gid}"] .tableRow`)]
            .map(r => [...r.querySelectorAll('.tableCell')].map(c => {
                const span = c.querySelector('span.ECCell');
                const inp = c.querySelector('input, select');
                return {
                    id: span ? span.id : null,
                    text: (span ? span.textContent : '').trim().slice(0,30),
                    cls: span ? span.className : '',
                    inputId: inp ? inp.id : null
                };
            }))""", gid)
        print(f"-- group {gid} --")
        for i, row in enumerate(rows):
            print(f"  tableRow[{i}]: {row}")

    print("\n=== grid id present? ===")
    grid = page.evaluate("""() => {
        const g = document.getElementById('manageObject:form:T_data');
        return {present: !!g};
    }""")
    print(grid)

    b.close()
