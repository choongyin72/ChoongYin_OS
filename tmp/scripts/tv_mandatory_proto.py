"""THROWAWAY read-only prototype of the post-#54 TV-branch fix (NOT committed to PR #54). Proves the
robust mandatory-field detection: (UI) click Insert '+' -> read the PRISTINE blank row's yellow cells
BEFORE any fill; (DB) the base table's NOT NULL columns; robust set = union. Nothing saved.
Usage: SCREEN="Language" py tmp/scripts/tv_mandatory_proto.py"""
import os
import oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = os.environ.get("SCREEN", "Language")
YELLOW = "rgb(252, 249, 192)"


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


# --- DB: class -> base table -> NOT NULL columns (the true-required set) ---
conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)
cur = conn.cursor()
cand = [r[0] for r in cur.execute("""SELECT class_name FROM class_property_cnfg
        WHERE property_code='LABEL' AND lower(property_value)=:s""", [SCREEN.lower()]).fetchall()]
real = [c for c in cand if not any(x in c for x in ("_ROWSORT", "_TEST", "AUTOSAVE"))]
ctype, base = None, None
if real:
    row = cur.execute("SELECT class_type, db_object_name FROM class_cnfg WHERE class_name=:c", [real[0]]).fetchall()
    if row:
        ctype, base = row[0]
notnull = []
if base:
    notnull = [r[0] for r in cur.execute("""SELECT column_name FROM all_tab_columns
        WHERE owner='ECKERNEL_EC' AND table_name=:t AND nullable='N'
        AND column_name NOT IN ('RECORD_STATUS','CREATED_BY','CREATED_DATE','UPDATED_BY','UPDATED_DATE')
        ORDER BY column_id""", [base]).fetchall()]
cur.close(); conn.close()
print(f"SCREEN='{SCREEN}'  class={real}  type={ctype}  base={base}")
print(f"[DB] NOT NULL columns (excl. audit/status): {notnull}")

# --- UI: Insert '+' -> read the PRISTINE blank row's yellow cells ---
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1700, "height": 950}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin"); page.fill("#password", "sysadmin"); page.click("#kc-login")
    page.wait_for_selector("#menu\\:searchForm\\:searchTxt", timeout=60000); ajax(page)
    box = page.locator("#menu\\:searchForm\\:searchTxt"); box.click(); box.fill(""); box.type(SCREEN, delay=45); ajax(page, 7000)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click()
    ajax(page)
    mm = page.locator("#screenToolbar\\:form\\:minmaxMenu")
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)

    # click Insert '+' submenu child (the screen-label item) -> fresh blank row
    page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
    page.wait_for_timeout(900)
    links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
    for i in range(links.count()):
        if links.nth(i).is_visible() and (links.nth(i).text_content(timeout=800) or "").strip():
            links.nth(i).click(); break
    ajax(page)

    # read PRISTINE blank row (the row whose cells are all empty) - capture yellow BEFORE any fill
    cells = page.evaluate("""(Y) => { const rows={};
        document.querySelectorAll("[id^='table:form:T:'][id$='_in']").forEach(e=>{
          const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return;
          (rows[+m[1]] ||= []).push({col:+m[2], val:e.value, yellow:getComputedStyle(e).backgroundColor===Y}); });
        // the blank insert row = the one with all-empty values
        for (const r of Object.keys(rows)) { if (rows[r].every(c=>c.val==='')) return {row:+r, cells:rows[r]}; }
        return null; }""", YELLOW)
    b.close()

print(f"[UI] pristine blank insert row: {cells}")
if cells:
    ui_yellow = [c['col'] for c in cells['cells'] if c['yellow']]
    print(f"[UI] yellow (mandatory) columns on blank row: C{ui_yellow}")
print("\n=> ROBUST mandatory = DB-NOT-NULL  UNION  UI-yellow  (UI confirms which are user-facing-required & empty)")
print("DONE (read-only prototype; NOT saved, NOT committed to PR #54).")
