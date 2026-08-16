"""RECON + de-risk probe (sandbox) for Stream Oil Component Analysis (PO.0019). Loads the grid for the
oil target, DOM-maps the editable WT_PCT cell (gas used C1=mol%; oil's wt% may be a DIFFERENT C{n}),
then edits one component's wt% -> Save -> DB-verify (changed + a 2nd component unchanged = no normalize)
-> revert. Self-cleaning. Mirrors the proven gas recon/probe."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREENS = ["Stream Oil Component Analysis", "Oil / Condensate Stream Component Analysis",
           "Oil Condensate Stream Component Analysis"]
CODE = "P1 ALLOC S001 OIL"
DATE = "2023-06-01"
COL = "WT_PCT"


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


def read_val(comp, col=COL):
    conn = db(); cur = conn.cursor()
    cur.execute(f"""SELECT {col} FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                    WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND COMPONENT_NO=:n""",
                [CODE, DATE, comp])
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None


conn = db(); cur = conn.cursor()
comps = cur.execute("""SELECT COMPONENT_NO, WT_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                       WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY COMPONENT_NO""",
                    [CODE, DATE]).fetchall()
ov = cur.execute("SELECT OBJECT_ID FROM ECKERNEL_EC.OV_STREAM WHERE NAME=:n FETCH FIRST 1 ROWS ONLY", [CODE]).fetchall()
nm = cur.execute("SELECT NAME FROM ECKERNEL_EC.OV_STREAM WHERE CODE=:c FETCH FIRST 1 ROWS ONLY", [CODE]).fetchall()
cur.close(); conn.close()
print("target components (COMPONENT_NO, WT_PCT):", comps)
print("OV_STREAM OBJECT_ID:", ov, " NAME-by-code:", nm)


def open_screen(page, names):
    box = page.locator(css("menu:searchForm:searchTxt"))
    for name in names:
        box.click(); box.fill(""); box.type(name, delay=45); ajax(page, 6000)
        link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{name}']")
        if link.count():
            link.first.click(); ajax(page); print("opened screen:", name)
            mm = page.locator(css("screenToolbar:form:minmaxMenu"))
            if mm.count() and mm.first.is_visible():
                mm.first.click(); ajax(page)
            return name
    print("SCREEN NOT FOUND among", names); return None


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


def opts(page, group):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    try:
        page.click(css(pre + "_button")); page.wait_for_timeout(700)
        o = page.evaluate(f"""() => [...document.querySelectorAll("[id='{pre}_panel'] tr[data-item-label]")]
            .map(t=>t.getAttribute('data-item-label')).filter(x=>x&&x.trim())""")
        page.keyboard.press("Escape"); page.wait_for_timeout(250); return o
    except Exception:
        return []


def dump_components(page):
    return page.evaluate("""() => { const rows=[];
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input[id^='component_set:form:T:']")].filter(i=>i.type!=='hidden');
          if(!ins.length) return;
          const cells=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').replace(/\\s+/g,' ').trim());
          rows.push({label: cells.find(t=>t)||'', inputs: ins.map(i=>({id:i.id, val:i.value, ro:i.readOnly}))});
        }); return rows; }""")


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)

    if not open_screen(page, SCREENS):
        b.close(); raise SystemExit("screen not found")
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")].map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    scope = {"G:2": "P1 Production Unit", "G:3": "P1 Area", "G:4": "P1 Facility 1"}
    for g, v in scope.items():
        try:
            pick(page, g, v)
        except Exception as e:
            print(f"  scope {g}={v} err {str(e)[:50]}")
    print("G:5 Stream opts:", opts(page, "G:5")[:12])
    try:
        pick(page, "G:5", CODE)
    except Exception as e:
        print("  stream pick err", str(e)[:60])
    status_opts = opts(page, "G:6"); print("G:6 Analysis Status:", status_opts)
    samp_opts = opts(page, "G:7"); print("G:7 Sampling:", samp_opts)
    if "*Spot" in samp_opts:
        pick(page, "G:7", "*Spot")
    loaded = None
    for st in status_opts:
        try:
            pick(page, "G:6", st)
        except Exception:
            continue
        for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
            loc = page.locator(css(go))
            if loc.count() and loc.first.is_visible():
                loc.first.click(); ajax(page, 18000); break
        rows = dump_components(page)
        ncell = sum(len(r["inputs"]) for r in rows)
        print(f"  status='{st}' rows={len(rows)} cells={ncell}")
        if ncell:
            loaded = st; break
    if not loaded:
        print("GRID NEVER LOADED"); b.close(); raise SystemExit
    rows = dump_components(page)
    print(f"\nGRID LOADED (status='{loaded}'). Component rows -> editable inputs:")
    for r in rows[:14]:
        print("  ", r["label"][:22], "->", [(i["id"].split(":form:")[1], i["val"], "ro" if i["ro"] else "EDIT") for i in r["inputs"]])
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\oil_grid.png", full_page=True)

    # identify the wt% (editable, populated) cell for Methane-equivalent: pick the first component row's
    # editable non-readonly input that has a value -> that column is WT_PCT
    target_label = rows[0]["label"]
    edit = next((i for i in rows[0]["inputs"] if not i["ro"]), None)
    print(f"\nDE-RISK PROBE on row '{target_label}': editable cell = {edit['id'] if edit else None} (val {edit['val'] if edit else None})")
    comp0 = comps[0][0]  # COMPONENT_NO of first row by DB order — may differ from UI order; report both
    print("  DB before:", comp0, "=", read_val(comp0))
    b.close()
print("DONE (recon; probe gesture wired but edit/save left to a follow-up once cell+component confirmed)")
