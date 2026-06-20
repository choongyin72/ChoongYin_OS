"""LEARN (evidence-first, READ-ONLY) the EC table column-filter on the Business Function grid:
open -> turn filtering on (the 'tfo' toggle / hamburger 'Turn filtering on') -> capture the filter-input id
pattern -> filter by BF Code, then by Name -> confirm the grid narrows to the wanted row. Screenshots only;
filtering does NOT modify data. py -X utf8 tmp/scripts/learn_grid_filter.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")
OUT = "tmp/learn_grid_filter"
os.makedirs(OUT, exist_ok=True)


def esc(i):
    return "#" + i.replace(":", "\\:")


def ajax(page, t=20000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def grid_rows(page, grid):
    return page.evaluate("""(g)=>{const t=document.getElementById(g);if(!t)return[];const o=[];
        t.querySelectorAll('tr').forEach(tr=>{const c=[...tr.querySelectorAll('td')].map(td=>(td.textContent||'').trim());
        if(c.some(x=>x))o.push(c);});return o;}""", grid)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", USER); page.fill("#password", PWD); page.click("#kc-login")
    page.wait_for_selector(esc("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Business Function", delay=45); ajax(page, 7000)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Business Function']").first.click()
    ajax(page)

    grid = page.evaluate("""()=>{const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.querySelector('tr'));return t.length?t[0].id:null;}""")
    base = grid.replace("_data", "") if grid else None   # e.g. xxx:form:T
    print("grid id:", grid, " base:", base)
    rows0 = grid_rows(page, grid)
    print("rows on page (pre-filter):", len(rows0), " row0:", rows0[0][:4] if rows0 else None)
    page.screenshot(path=f"{OUT}/01_prefilter.png", full_page=False)

    # locate the filter-toggle (PW-04: a span whose id contains 'tfo')
    tfo = page.evaluate("""()=>[...document.querySelectorAll("[id*='tfo'],[id*='TFO']")].map(e=>({id:e.id,tag:e.tagName,cls:(e.className||'').slice(0,40),vis:e.offsetParent!==null})).slice(0,8)""")
    print("\n'tfo' filter-toggle candidates:")
    for t in tfo:
        print("  ", t)

    # try clicking the first visible tfo to TURN FILTERING ON
    turned = False
    for t in tfo:
        if t["vis"]:
            try:
                page.locator(esc(t["id"])).first.click(); ajax(page); turned = True
                print("clicked tfo ->", t["id"]); break
            except Exception as e:
                print("  tfo click err:", str(e)[:60])
    page.screenshot(path=f"{OUT}/02_filtering_on.png", full_page=False)

    # capture the filter inputs that appeared
    finputs = page.evaluate("""()=>[...document.querySelectorAll("input[id*='sfilter'],input[id*='filter']")]
        .filter(e=>e.offsetParent!==null && e.type!=='hidden')
        .map(e=>e.id).slice(0,20)""")
    print("\nfilter input ids (visible):")
    for f in finputs:
        print("  ", f)

    # pick a real BF Code from row0 to filter by, and the text filter input for column 0
    code_val = rows0[0][0] if rows0 else None
    ft0 = next((f for f in finputs if "sfilter0" in f and "ft_filter" in f), None) or next((f for f in finputs if "sfilter0" in f), None)
    print(f"\nfilter BF Code (col0) input: {ft0}  value to test: {code_val!r}")
    if ft0 and code_val:
        el = page.locator(esc(ft0)); el.click(); el.fill(code_val); el.press("Enter"); ajax(page)
        page.wait_for_timeout(800)
        rows1 = grid_rows(page, grid)
        print("rows after filtering BF Code =", code_val, "->", len(rows1), " (first:", rows1[0][:2] if rows1 else None, ")")
        page.screenshot(path=f"{OUT}/03_filtered_by_code.png", full_page=False)
        # clear + filter by NAME (col1) using row0's name
        el.fill(""); el.press("Enter"); ajax(page)
        name_val = rows0[0][1] if rows0 and len(rows0[0]) > 1 else None
        ft1 = next((f for f in finputs if "sfilter1" in f and "ft_filter" in f), None) or next((f for f in finputs if "sfilter1" in f), None)
        print(f"\nfilter Name (col1) input: {ft1}  value to test: {name_val!r}")
        if ft1 and name_val:
            e1 = page.locator(esc(ft1)); e1.click(); e1.fill(name_val); e1.press("Enter"); ajax(page); page.wait_for_timeout(800)
            rows2 = grid_rows(page, grid)
            print("rows after filtering Name =", name_val, "->", len(rows2), " (first:", rows2[0][:2] if rows2 else None, ")")
            page.screenshot(path=f"{OUT}/04_filtered_by_name.png", full_page=False)
    b.close()
print(f"\nDONE (read-only; filtering only, no data changed). Shots in {OUT}/")
