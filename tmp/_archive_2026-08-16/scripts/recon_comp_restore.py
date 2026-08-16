"""URGENT self-clean: the edit probe left DV_STRM_COMP_ANALYSIS Methane(C1) MOL_PCT at 70.5; restore to
70.68. Robust gesture: clear cell -> type 70.68 -> Tab -> verify the input shows 70.68 -> wait for the
Save link to ENABLE -> click -> verify DB C1=70.68."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Stream Gas Component Analysis"
CODE = "P1 S038_AGA3_1985_AGA8_Y_1"
DATE = "2011-11-01"
TARGET = "70.68"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def read_mol(comp):
    conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                            dsn=DB_DSN, tcp_connect_timeout=15)
    cur = conn.cursor()
    cur.execute("""SELECT MOL_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                   WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') AND COMPONENT_NO=:n""",
                [CODE, DATE, comp])
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None


print("DB before restore: C1(Methane)=", read_mol("C1"))


def open_screen(page, name):
    box = page.locator(css("menu:searchForm:searchTxt"))
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


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
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
            loc.first.click(); ajax(page, 18000); break

    mid = comp_cell(page, "Methane")
    inp = page.locator(css(mid))
    print("UI Methane now:", inp.input_value())
    # robust clear + type
    inp.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.wait_for_timeout(200)
    page.keyboard.type(TARGET, delay=80)
    page.keyboard.press("Tab")
    ajax(page, 14000)
    staged = page.locator(css(comp_cell(page, "Methane"))).input_value()
    print("UI Methane staged:", staged)
    # wait for Save to enable, then click
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    try:
        sv.first.wait_for(state="visible", timeout=8000)
        sv.first.click(); ajax(page, 18000); print("Saved.")
    except Exception as e:
        print("SAVE LINK NOT ENABLED:", str(e)[:80])
        # try keyboard Ctrl+S
        page.keyboard.press("Control+s"); ajax(page, 18000); print("Tried Ctrl+S.")
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\restore.png")
    b.close()

print(">> DB after restore: C1(Methane)=", read_mol("C1"), " (must be 70.68)")
print("DONE")
