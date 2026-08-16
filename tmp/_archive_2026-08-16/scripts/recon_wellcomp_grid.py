"""RECON (read-only) WR.0010.01 grid map: fill PU/Area/Facility, identify the extra G:5/G:6 dropdowns
(Well Hookup? / Well), pick the well, Approved + *Spot, GO, dump the component grid to confirm the mol%
cell (expect C1_in like stream gas). No edits. Target well NAME 'P1 W260 GP Comp Gas' @ 2025-04-01."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Well Gas Component Analysis"
WELL_NAME = "P1 W260 GP Comp Gas"
DATE = "2025-04-01"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


cur = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                       dsn=DB_DSN, tcp_connect_timeout=15).cursor()
comps = cur.execute("""SELECT COMPONENT_NO, MOL_PCT, WT_PCT FROM ECKERNEL_EC.DV_WELL_COMP_ANALYSIS
                       WHERE OBJECT_CODE='P1_W260_GP_COMP_GAS' AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')
                       ORDER BY COMPONENT_NO""", [DATE]).fetchall()
print("target components (NO, MOL_PCT, WT_PCT):", comps)
cur.close()


def opts(page, group):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    try:
        page.click(css(pre + "_button")); page.wait_for_timeout(700)
        o = page.evaluate(f"""() => [...document.querySelectorAll("[id='{pre}_panel'] tr[data-item-label]")]
            .map(t=>t.getAttribute('data-item-label')).filter(x=>x&&x.trim())""")
        page.keyboard.press("Escape"); page.wait_for_timeout(250); return o
    except Exception:
        return []


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


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(css("menu:searchForm:searchTxt")); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    page.locator(f"xpath=//*[contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click(); ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")].map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    pick(page, "G:2", "P1 Production Unit")
    pick(page, "G:3", "P1 Area")
    pick(page, "G:4", "P1 Facility 1")
    # identify G:5 / G:6 (one is the Well dropdown containing the well name)
    g5 = opts(page, "G:5"); g6 = opts(page, "G:6")
    print("G:5 opts:", g5[:8])
    print("G:6 opts:", g6[:8])
    well_grp = "G:6" if any(WELL_NAME in o or "W260" in o for o in g6) else ("G:5" if any(WELL_NAME in o or "W260" in o for o in g5) else None)
    print("Well dropdown =", well_grp)
    # pick optional G:5 (hookup) if it has options and isn't the well group
    if well_grp == "G:6" and g5:
        try:
            pick(page, "G:5", g5[0]); print("  picked G:5 (hookup?)=", g5[0])
        except Exception:
            pass
    if well_grp:
        wn = next((o for o in (g6 if well_grp == "G:6" else g5) if WELL_NAME in o or "W260" in o), WELL_NAME)
        pick(page, well_grp, wn); print("  picked Well=", wn)
    pick(page, "G:7", "Approved")
    if "*Spot" in opts(page, "G:8"):
        pick(page, "G:8", "*Spot")
    for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
        loc = page.locator(css(go))
        if loc.count() and loc.first.is_visible():
            loc.first.click(); ajax(page, 18000); break
    rows = page.evaluate("""() => { const out=[];
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input[id^='component_set:form:T:']")].filter(i=>i.type!=='hidden');
          if(!ins.length) return;
          const cells=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').trim());
          out.push({label: cells.find(t=>t)||'', inputs: ins.map(i=>({id:i.id.split(':form:')[1], val:i.value, ro:i.readOnly}))});
        }); return out; }""")
    print(f"\ncomponent grid rows ({len(rows)}):")
    for r in rows[:12]:
        print("  ", r["label"][:20], "->", [(i["id"], i["val"], "ro" if i["ro"] else "EDIT") for i in r["inputs"]])
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\wellgas_grid.png", full_page=True)
    b.close()
print("DONE")
