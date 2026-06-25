"""Clean de-risk probe on the CORRECT oil cell (WT_PCT = C2_in). Edit Methane wt% 0.1->0.2 -> Save
(robust wait-for-enable) -> DB-verify WT_PCT(C1)=0.2 + guard WT_PCT(C2/Ethane)=0.1 unchanged -> revert
to 0.1 -> DB-verify. Targets C2_in explicitly (NOT 'first editable', which is the empty mol% C1)."""
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


def wt(comp):
    conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                            dsn=DB_DSN, tcp_connect_timeout=15)
    cur = conn.cursor()
    cur.execute("""SELECT WT_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
                   WHERE OBJECT_CODE='P1 ALLOC S001 OIL' AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')
                   AND COMPONENT_NO=:n""", [DATE, comp])
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


def methane_wt_cell(page):
    return page.evaluate("""() => { let id=null; document.querySelectorAll('table tr').forEach(tr=>{
        const t=[...tr.querySelectorAll('td,th')].map(c=>(c.innerText||'').trim());
        if(t.includes('Methane')){ const i=tr.querySelector("input[id$=':C2_in']"); if(i) id=i.id; } }); return id; }""")


def edit(page, cid, val):
    inp = page.locator(css(cid)); inp.click()
    page.keyboard.press("Control+A"); page.keyboard.press("Delete"); page.wait_for_timeout(150)
    page.keyboard.type(str(val), delay=70); page.keyboard.press("Tab"); ajax(page, 14000)


def save(page):
    sv = page.locator("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
    try:
        sv.first.wait_for(state="visible", timeout=9000); sv.first.click(); ajax(page, 18000); return True
    except Exception:
        return False


print("DB before: WT C1=", wt("C1"), " C2=", wt("C2"))
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
    pick(page, "G:2", "P1 Production Unit"); pick(page, "G:3", "P1 Area")
    pick(page, "G:4", "P1 Facility Allocation"); pick(page, "G:5", STREAM_NAME)
    if "*Spot" in opts(page, "G:7"):
        pick(page, "G:7", "*Spot")
    pick(page, "G:6", "Approved")
    page.click(css("go_button:form:B")); ajax(page, 18000)
    cid = methane_wt_cell(page)
    print("Methane WT cell (C2_in):", cid, "val:", page.locator(css(cid)).input_value())
    edit(page, cid, "0.2"); print("  saved EDIT:", save(page))
    print("  DB after EDIT: WT C1=", wt("C1"), "(exp 0.2)  C2=", wt("C2"), "(exp 0.1)")
    cid2 = methane_wt_cell(page)
    edit(page, cid2, "0.1"); print("  saved REVERT:", save(page))
    print("  DB after REVERT: WT C1=", wt("C1"), "(must be 0.1)")
    page.screenshot(path=r"c:\Projects\ChoongYin_OS\tmp\recon_comp\oil_probe.png")
    b.close()
print("DONE")
