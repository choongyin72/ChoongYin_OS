"""DE-RISK PROBE (sandbox): prove the composition edit gesture end-to-end BEFORE building the RF suite.
Loads the grid (Approved + *Spot), edits Methane MOL_PCT 70.68 -> 70.50 via real keystrokes + Tab,
clicks Save, reads DB to confirm (a) C1=70.50 persisted and (b) C2/Ethane UNCHANGED (no normalize-on-
save), then REVERTS to 70.68 and re-confirms. Also checks OV_STREAM.OBJECT_ID == comp OBJECT_ID (so the
RF Object Id By Name path works). Self-cleaning (reverts). Mirrors the proven recon nav."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")
SCREEN = "Stream Gas Component Analysis"
CODE = "P1 S038_AGA3_1985_AGA8_Y_1"
DATE = "2011-11-01"
ORIG = "70.68"
SENTINEL = "70.50"


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


def read_mol(comp):
    conn = db(); cur = conn.cursor()
    cur.execute("""SELECT MOL_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                   WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND COMPONENT_NO=:n""",
                [CODE, DATE, comp])
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None


# OBJECT_ID match check
conn = db(); cur = conn.cursor()
ov = cur.execute("SELECT OBJECT_ID FROM ECKERNEL_EC.OV_STREAM WHERE NAME=:n FETCH FIRST 1 ROWS ONLY", [CODE]).fetchall()
comp_oid = cur.execute("""SELECT DISTINCT OBJECT_ID FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS WHERE OBJECT_CODE=:c""", [CODE]).fetchall()
cur.close(); conn.close()
print("OV_STREAM.OBJECT_ID:", ov, "| comp OBJECT_ID:", comp_oid,
      "| MATCH:", bool(ov and comp_oid and ov[0][0] == comp_oid[0][0]))
print("DB before: C1(Methane)=", read_mol("C1"), " C2(Ethane)=", read_mol("C2"))


def open_screen(page, name):
    box = page.locator(css("menu:searchForm:searchTxt"))
    if box.count() == 0 or not box.first.is_visible():
        mm = page.locator(css("screenToolbar:form:minmaxMenu"))
        if mm.count() and mm.first.is_visible():
            mm.first.click(); page.wait_for_timeout(800)
    box.click(); box.fill(""); box.type(name, delay=45); ajax(page, 8000)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link')"
                 f" and normalize-space(text())='{name}']").first.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)


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


def comp_cell(page, label):
    return page.evaluate("""(label) => { let id=null;
        document.querySelectorAll("table tr").forEach(tr=>{
          const tds=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').trim());
          if(tds.includes(label)){ const inp=tr.querySelector("input[id^='component_set:form:T:'][id$='C1_in']");
            if(inp) id=inp.id; } });
        return id; }""", label)


def set_cell(page, cell_id, value):
    inp = page.locator(css(cell_id))
    inp.click()
    page.keyboard.press("Control+A")
    page.keyboard.type(str(value), delay=60)
    page.keyboard.press("Tab")
    ajax(page, 14000)


def save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    if sv.count() and sv.first.is_visible():
        sv.first.click(); ajax(page, 18000); return "save-link"
    # fallback: any enabled Save
    sv2 = page.locator("xpath=//a[contains(@title,'Save') and not(contains(@class,'ui-state-disabled'))]")
    if sv2.count() and sv2.first.is_visible():
        sv2.first.click(); ajax(page, 18000); return "save-fallback"
    return None


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", EC_USER); page.fill("#password", EC_PASS); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)

    open_screen(page, SCREEN)
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")]
            .map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    pick(page, "G:2", "P1 Production Unit")
    pick(page, "G:3", "P1 Area")
    pick(page, "G:4", "P1 Facility 1")
    pick(page, "G:5", CODE)
    pick(page, "G:6", "Approved")
    pick(page, "G:7", "*Spot")
    for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
        loc = page.locator(css(go))
        if loc.count() and loc.first.is_visible():
            loc.first.click(); ajax(page, 18000); print("GO via", go); break

    mid = comp_cell(page, "Methane")
    eid = comp_cell(page, "Ethane")
    print("Methane cell:", mid, "| Ethane cell:", eid)
    print("UI Methane before:", page.locator(css(mid)).input_value() if mid else None)

    # EDIT Methane -> sentinel
    set_cell(page, mid, SENTINEL)
    sv = save(page)
    print("Saved via:", sv)
    print(">> DB after EDIT:  C1(Methane)=", read_mol("C1"), " C2(Ethane)=", read_mol("C2"),
          " (expect C1=70.5, C2=14.14 unchanged)")

    # REVERT Methane -> original
    mid2 = comp_cell(page, "Methane")  # re-resolve (grid may re-render)
    set_cell(page, mid2, ORIG)
    sv = save(page)
    print("Reverted via:", sv)
    print(">> DB after REVERT: C1(Methane)=", read_mol("C1"), " (expect 70.68)")
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\edit_probe.png")
    b.close()
print("DONE")
