"""RECON v2 + de-risk probe for Stream Oil Component Analysis (PO.0019). Correct scope: PU=P1 Production
Unit, Area=P1 Area, Facility Class 1 = the *Allocation* facility (picked from G:4 opts by 'Alloc'),
Stream='P1 Alloc S001 M OIL' @ 2023-06-01. Loads grid, maps the editable WT_PCT cell, then edits one
component's wt% -> Save -> DB-verify (changed + a 2nd component unchanged) -> revert. Self-cleaning."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Stream Oil Component Analysis"
CODE = "P1 ALLOC S001 OIL"          # comp view OBJECT_CODE (for DB verify)
STREAM_NAME = "P1 Alloc S001 M OIL"  # OV_STREAM NAME (G:5 dropdown label)
DATE = "2023-06-01"
EDIT_LABEL = "Methane"   # -> COMPONENT_NO C1
GUARD_NO = "C2"          # Ethane
ORIG = "0.1"
SENT = "0.2"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def db():
    return oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                            dsn=DB_DSN, tcp_connect_timeout=15)


def read_wt(comp):
    conn = db(); cur = conn.cursor()
    cur.execute("""SELECT WT_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                   WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND COMPONENT_NO=:n""",
                [CODE, DATE, comp])
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None


def open_screen(page, name):
    box = page.locator(css("menu:searchForm:searchTxt"))
    box.click(); box.fill(""); box.type(name, delay=45); ajax(page, 7000)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{name}']").first.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)


def opts(page, group):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    page.click(css(pre + "_button")); page.wait_for_timeout(700)
    o = page.evaluate(f"""() => [...document.querySelectorAll("[id='{pre}_panel'] tr[data-item-label]")]
        .map(t=>t.getAttribute('data-item-label')).filter(x=>x&&x.trim())""")
    page.keyboard.press("Escape"); page.wait_for_timeout(250); return o


def pick(page, group, value):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    item = f"xpath=//*[@id='{pre}_panel']//tr[normalize-space(@data-item-label)='{value}']"
    page.click(css(pre + "_button"))
    try:
        page.locator(item).first.wait_for(state="visible", timeout=5000)
    except Exception:
        page.keyboard.press("Escape"); page.wait_for_timeout(1000); page.click(css(pre + "_button"))
        page.locator(item).first.wait_for(state="visible", timeout=6000)
    page.locator(item).first.click(); ajax(page, 10000)


def dump_components(page):
    return page.evaluate("""() => { const rows=[];
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input[id^='component_set:form:T:']")].filter(i=>i.type!=='hidden');
          if(!ins.length) return;
          const cells=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').replace(/\\s+/g,' ').trim());
          rows.push({label: cells.find(t=>t)||'', inputs: ins.map(i=>({id:i.id, val:i.value, ro:i.readOnly}))});
        }); return rows; }""")


def edit_cell(page, cid, val):
    inp = page.locator(css(cid)); inp.click()
    page.keyboard.press("Control+A"); page.keyboard.press("Delete"); page.wait_for_timeout(200)
    page.keyboard.type(str(val), delay=70); page.keyboard.press("Tab"); ajax(page, 14000)


def save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    try:
        sv.first.wait_for(state="visible", timeout=9000); sv.first.click(); ajax(page, 18000); return True
    except Exception:
        return False


print("DB before: C1(Methane)=", read_wt("C1"), " C2(Ethane)=", read_wt("C2"))
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    open_screen(page, SCREEN)
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")].map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    pick(page, "G:2", "P1 Production Unit")
    pick(page, "G:3", "P1 Area")
    g4 = opts(page, "G:4"); print("G:4 Facility opts:", g4)
    fac = next((o for o in g4 if "alloc" in o.lower()), None)
    print("  -> picking Facility:", fac)
    pick(page, "G:4", fac)
    g5 = opts(page, "G:5"); print("G:5 Stream opts:", g5[:15])
    pick(page, "G:5", STREAM_NAME if STREAM_NAME in g5 else next((o for o in g5 if "Alloc S001" in o), g5[0]))
    samp = opts(page, "G:7")
    if "*Spot" in samp:
        pick(page, "G:7", "*Spot")
    loaded = None
    for st in opts(page, "G:6"):
        try:
            pick(page, "G:6", st)
        except Exception:
            continue
        for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
            loc = page.locator(css(go))
            if loc.count() and loc.first.is_visible():
                loc.first.click(); ajax(page, 18000); break
        rows = dump_components(page)
        nc = sum(len(r["inputs"]) for r in rows if r["label"] != "Sum:")
        print(f"  status='{st}' component-cells={nc}")
        if nc:
            loaded = st; break
    if not loaded:
        print("GRID NEVER LOADED for the oil target"); b.close(); raise SystemExit
    rows = dump_components(page)
    print(f"\nGRID LOADED (status='{loaded}'):")
    for r in rows[:14]:
        print("  ", r["label"][:20], "->", [(i["id"].split(':form:')[1], i["val"], "ro" if i["ro"] else "EDIT") for i in r["inputs"]])
    trow = next((r for r in rows if r["label"] == EDIT_LABEL), None)
    cell = next((i for i in trow["inputs"] if not i["ro"]), None) if trow else None
    print(f"\nPROBE: '{EDIT_LABEL}' editable cell = {cell['id'] if cell else None} (val {cell['val'] if cell else None})")
    if cell:
        edit_cell(page, cell["id"], SENT)
        ok = save(page)
        print(f"  saved={ok}; DB after EDIT: C1={read_wt('C1')} (exp {SENT})  C2={read_wt('C2')} (exp {ORIG} unchanged)")
        trow2 = next((r for r in dump_components(page) if r["label"] == EDIT_LABEL), None)
        cell2 = next((i for i in trow2["inputs"] if not i["ro"]), None) if trow2 else None
        edit_cell(page, cell2["id"], ORIG)
        ok2 = save(page)
        print(f"  reverted={ok2}; DB after REVERT: C1={read_wt('C1')} (must be {ORIG})")
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\oil_grid2.png", full_page=True)
    b.close()
print("DONE")
