"""RECON (read-only) for Well Gas Component Analysis (WR.0010.01) Phase 1: (A) DB-resolve the well NAME +
hierarchy (PU/Area/Facility/well-hookup) for the target P1_W260_GP_COMP_GAS; (B) open the screen and dump
the OPTIONS of each of the 7 nav dropdowns (G:2..G:8) to map them (PU/Area/Facility/.../Well/Status/Sampling).
No edits."""
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = "Well Gas Component Analysis"
CODE = "P1_W260_GP_COMP_GAS"
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
oid = cur.execute("SELECT DISTINCT OBJECT_ID FROM ECKERNEL_EC.DV_WELL_COMP_ANALYSIS WHERE OBJECT_CODE=:c", [CODE]).fetchall()
print("comp OBJECT_ID:", oid)
# find the well in WELL_VERSION / OV_WELL with hierarchy
for v in ("WELL_VERSION", "OV_WELL"):
    cols = [c[0] for c in cur.execute("""SELECT column_name FROM all_tab_columns WHERE owner='ECKERNEL_EC'
            AND table_name=:t AND (column_name='NAME' OR column_name='CODE' OR column_name LIKE 'OP_%'
            OR column_name LIKE '%PRODUCTIONUNIT%' OR column_name LIKE '%AREA%' OR column_name LIKE '%FCTY%'
            OR column_name LIKE '%FACILITY%' OR column_name LIKE '%HOOKUP%') ORDER BY column_id""", [v]).fetchall()]
    if cols and oid:
        sel = ", ".join(cols)
        try:
            r = cur.execute(f"SELECT {sel} FROM ECKERNEL_EC.{v} WHERE OBJECT_ID=:o FETCH FIRST 1 ROWS ONLY", [oid[0][0]]).fetchall()
            print(f"\n{v} hierarchy for the well:")
            if r:
                for k, val in zip(cols, r[0]):
                    print(f"   {k} = {val}")
        except Exception as e:
            print(f"{v} err", str(e)[:60])
cur.close()

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
    # set the date fields then dump each dropdown's first options
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")].map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    print("\nNav dropdown OPTIONS (G:2..G:8):")
    for g in range(2, 9):
        pre = f"nav:form:G:{g}:R:1:C:0:dd"
        try:
            page.click(css(pre + "_button")); page.wait_for_timeout(600)
            o = page.evaluate(f"""() => [...document.querySelectorAll("[id='{pre}_panel'] tr[data-item-label]")]
                .map(t=>t.getAttribute('data-item-label')).filter(x=>x&&x.trim()).slice(0,6)""")
            page.keyboard.press("Escape"); page.wait_for_timeout(200)
            print(f"   G:{g} -> {o}")
        except Exception as e:
            print(f"   G:{g} err {str(e)[:40]}")
    b.close()
print("DONE")
