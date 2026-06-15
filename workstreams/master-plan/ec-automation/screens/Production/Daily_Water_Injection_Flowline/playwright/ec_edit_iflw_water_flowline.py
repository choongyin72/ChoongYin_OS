"""EC N1 edit prototype (freestyle Playwright) — Daily Water Injection Flowline, by Flowline.
Edits On Strm[hr] (C2 = ON_STREAM_HRS) for P1 F003 WI on 2019-12-20, Saves, DB-verifies the value
persisted in IFLW_DAY_STATUS, then restores the cell to NULL (self-clean). Screenshots -> evidence/.
NEVER touches data beyond this one cell. Env: EC_HEADED=1 to watch; EC_URL / EC_DB_* override defaults.
"""
import os
import time
from pathlib import Path
import oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SCREEN = "Daily Water Injection Flowline, by Flowline"
SCOPE = {"date": "2019-12-20", "pu": "P1 Production Unit", "area": "P1 Area",
         "fcty": "P1 Facility 1", "flowline": "P1 F003 WI"}
GRID = "daily_flowline_status:form:T_data"
CELL_PREFIX = "daily_flowline_status:form:T"
SENTINEL = "18"
EVID = Path(__file__).resolve().parent.parent / "evidence"
EVID.mkdir(parents=True, exist_ok=True)


def db():
    return oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                            password=os.environ.get("EC_DB_PASS", "energy"),
                            dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)


def flowline_oid():
    con = db(); cur = con.cursor()
    cur.execute("SELECT OBJECT_ID FROM OV_FLOWLINE WHERE NAME=:n", {"n": SCOPE["flowline"]})
    oid = cur.fetchone()[0]; con.close(); return oid


def db_on_stream_hrs(oid):
    con = db(); cur = con.cursor()
    cur.execute("""SELECT ON_STREAM_HRS FROM IFLW_DAY_STATUS
                   WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')""",
                {"o": oid, "d": SCOPE["date"]})
    r = cur.fetchone(); con.close(); return r[0] if r else None


def db_restore_null(oid):
    con = db(); cur = con.cursor()
    cur.execute("""UPDATE IFLW_DAY_STATUS SET ON_STREAM_HRS=NULL
                   WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')""",
                {"o": oid, "d": SCOPE["date"]})
    con.commit(); con.close()


def get_frame(page):
    for _ in range(40):
        for fr in page.frames:
            try:
                if fr.evaluate("""()=>!!document.querySelector('[id="nav:form:G:0:R:1:C:0:da_input"]')"""):
                    return fr
            except Exception:
                pass
        time.sleep(0.5)
    return page


def pick(fr, g, label):
    fr.click(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]', timeout=6000); time.sleep(0.6)
    fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]', timeout=6000)
    time.sleep(1.2)


def main():
    oid = flowline_oid()
    print(f"flowline OBJECT_ID={oid}  baseline ON_STREAM_HRS={db_on_stream_hrs(oid)}")
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not HEADED, slow_mo=400 if HEADED else 0)
        page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
        page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000)
        page.fill('[id="username"]', os.environ.get("EC_USER", "sysadmin"))
        page.fill('[id="password"]', os.environ.get("EC_PASS", "sysadmin"))
        page.click('[id="kc-login"]')
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
        page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=20); time.sleep(1.3)
        page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
        fr = get_frame(page)
        fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]', SCOPE["date"])
        fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]', SCOPE["date"]); time.sleep(0.4)
        pick(fr, 2, SCOPE["pu"]); pick(fr, 3, SCOPE["area"]); pick(fr, 4, SCOPE["fcty"]); pick(fr, 5, SCOPE["flowline"])
        fr.click('[id="button:form:B"]', timeout=8000)
        page.wait_for_load_state("networkidle", timeout=30000)
        time.sleep(2.0)
        page.screenshot(path=str(EVID / "01_grid_loaded.png"))

        # find C2 input in row 0..n for the grid, edit -> Tab
        cell = None
        for idx in range(6):
            cid = f'{CELL_PREFIX}:{idx}:C2_in'
            if fr.evaluate(f"""()=>!!document.querySelector('[id="{cid}"]')"""):
                cell = cid; break
        assert cell, "C2 cell not found"
        fr.click(f'[id="{cell}"]'); fr.fill(f'[id="{cell}"]', ""); fr.type(f'[id="{cell}"]', SENTINEL, delay=60)
        fr.press(f'[id="{cell}"]', "Tab")
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.0)
        page.screenshot(path=str(EVID / "02_edited.png"))

        # Save (toolbar) — try frame then page
        sel = "xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"
        try:
            fr.click(sel, timeout=8000)
        except Exception:
            page.click(sel, timeout=8000)
        page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5)
        page.screenshot(path=str(EVID / "03_saved.png"))
        b.close()

    persisted = db_on_stream_hrs(oid)
    ok = str(persisted) == SENTINEL or (persisted is not None and float(persisted) == float(SENTINEL))
    print(f"DB ON_STREAM_HRS after save = {persisted}  ->  {'PASS' if ok else 'FAIL'}")
    db_restore_null(oid)
    print(f"restored; DB ON_STREAM_HRS now = {db_on_stream_hrs(oid)} (expect None)")
    print("DONE")


if __name__ == "__main__":
    main()
