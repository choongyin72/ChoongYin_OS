"""URGENT self-clean: the mis-aimed probe set Methane(C1) MOL_PCT=0.2 (was NULL) on the oil target.
Restore: navigate the PO.0019 grid, clear Methane's MOL_PCT cell (C1_in) -> Save (handle confirm modal)
-> verify DB MOL_PCT(C1) = NULL. WT_PCT untouched (still 0.1)."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Stream Oil Component Analysis"
STREAM_NAME = "P1 Alloc S001 M OIL"
DATE = "2023-06-01"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def mol_c1():
    conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                            dsn=DB_DSN, tcp_connect_timeout=15)
    cur = conn.cursor()
    cur.execute("""SELECT MOL_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                   WHERE OBJECT_CODE='P1 ALLOC S001 OIL' AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')
                   AND COMPONENT_NO='C1'""", [DATE])
    r = cur.fetchone(); cur.close(); conn.close()
    return r[0] if r else None


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


print("DB before restore: MOL_PCT(C1) =", mol_c1())
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
    pick(page, "G:4", "P1 Facility Allocation")
    pick(page, "G:5", STREAM_NAME)
    if "*Spot" in opts(page, "G:7"):
        pick(page, "G:7", "*Spot")
    pick(page, "G:6", "Approved")
    page.click(css("go_button:form:B")); ajax(page, 18000)
    # Methane row -> its C1_in (mol%) cell
    cid = page.evaluate("""() => { let id=null; document.querySelectorAll('table tr').forEach(tr=>{
        const t=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').trim());
        if(t.includes('Methane')){ const i=tr.querySelector("input[id$=':C1_in']"); if(i) id=i.id; } }); return id; }""")
    print("Methane mol% cell:", cid, "current val:", page.locator(css(cid)).input_value())
    inp = page.locator(css(cid)); inp.click()
    page.keyboard.press("Control+A"); page.keyboard.press("Delete"); page.keyboard.press("Tab"); ajax(page, 14000)
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    try:
        sv.first.wait_for(state="visible", timeout=9000); sv.first.click(); ajax(page, 18000); print("Saved.")
    except Exception as e:
        print("save link not enabled:", str(e)[:60]); page.keyboard.press("Control+s"); ajax(page, 12000)
    # handle a possible confirmation modal
    modal_ok = page.locator("xpath=//*[contains(@id,'confirmation')]//a[normalize-space()='OK' or normalize-space()='Yes']")
    if modal_ok.count() and modal_ok.first.is_visible():
        modal_ok.first.click(); ajax(page, 12000); print("confirmation modal OK clicked")
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\oil_restore.png")
    b.close()
print("DB after restore: MOL_PCT(C1) =", mol_c1(), " (must be None)")
