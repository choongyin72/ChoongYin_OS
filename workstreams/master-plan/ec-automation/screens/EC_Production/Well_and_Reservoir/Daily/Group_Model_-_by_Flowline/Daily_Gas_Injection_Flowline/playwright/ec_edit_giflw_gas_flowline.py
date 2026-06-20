"""EC N1 EDIT prototype (freestyle Playwright) - Daily Gas Injection Flowline, by Flowline.
UPDATE-ONLY screen (New/Delete toolbar disabled; daily row batch-instantiated). Demos the full EDIT of
the cell On Strm[hr] (= ON_STREAM_HRS) for P1 F004 GI on 2019-12-20, DB-verifying IFLW_DAY_STATUS
(INJ_TYPE='GI') at each step:  SET (empty->18) -> CHANGE (18->24) -> CLEAR (->NULL). All three are
UPDATEs of the same pre-instantiated row (clear nulls the value; the record is NOT deleted). Null-original
so CLEAR restores the original (self-cleaning). Maximises + expands to full page (matches RF keywords).
Env: EC_HEADED=1 to watch, EC_HOLD=<s> to pause per step. NEVER touches data beyond this one cell.
"""
import os
import time
from pathlib import Path
import oracledb
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
HOLD = float(os.environ.get("EC_HOLD", "0"))
SCREEN = "Daily Gas Injection Flowline, by Flowline"
SCOPE = {"date": "2019-12-20", "pu": "P1 Production Unit", "area": "P1 Area",
         "fcty": "P1 Facility 1", "flowline": "P1 F004 GI"}
CELL = "daily_flowline_status:form:T:0:C2_in"
SAVE = "xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]"
GO = '[id="button:form:B"]'
SET_VALUE, CHANGE_VALUE = "18", "24"
EVID = Path(__file__).resolve().parent.parent / "evidence"
EVID.mkdir(parents=True, exist_ok=True)


def db():
    return oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                            password=os.environ.get("EC_DB_PASS", "energy"),
                            dsn=os.environ.get("EC_DB_DSN", "localhost:1521/ORCL"), tcp_connect_timeout=15)


def oid():
    c = db(); cur = c.cursor()
    cur.execute("SELECT OBJECT_ID FROM OV_FLOWLINE WHERE NAME=:n", {"n": SCOPE["flowline"]})
    r = cur.fetchone()[0]; c.close(); return r


def val(o):
    c = db(); cur = c.cursor()
    cur.execute("SELECT ON_STREAM_HRS FROM IFLW_DAY_STATUS WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')",
                {"o": o, "d": SCOPE["date"]})
    r = cur.fetchone(); c.close(); return (r[0] if r else "NO_ROW")


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
    fr.click(f'xpath=//*[@id="nav:form:G:{g}:R:1:C:0:dd_panel"]//tr[normalize-space(@data-item-label)="{label}"]', timeout=6000); time.sleep(1.0)


def save(page, fr):
    for sc in (fr, page):
        try:
            sc.click(SAVE, timeout=6000); page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1.5); return
        except Exception:
            pass


def reload_go(page, fr):
    fr.click(GO, timeout=8000); page.wait_for_load_state("networkidle", timeout=20000); time.sleep(1.5)


def set_cell(fr, v):
    fr.click(f'[id="{CELL}"]'); fr.press(f'[id="{CELL}"]', "Control+a"); fr.press(f'[id="{CELL}"]', "Delete")
    if v != "":
        fr.type(f'[id="{CELL}"]', str(v), delay=60)
    fr.press(f'[id="{CELL}"]', "Tab")


def main():
    o = oid(); print(f"OBJECT_ID={o}  baseline ON_STREAM_HRS={val(o)}")
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not HEADED, slow_mo=350 if HEADED else 0,
                              args=["--start-maximized", "--ignore-certificate-errors"])
        ctx = {"ignore_https_errors": True}
        if HEADED:
            ctx["no_viewport"] = True
        else:
            ctx["viewport"] = {"width": 1920, "height": 1080}
        page = b.new_context(**ctx).new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.fill('[id="username"]', os.environ.get("EC_USER", "sysadmin"))
        page.fill('[id="password"]', os.environ.get("EC_PASS", "sysadmin"))
        page.click('[id="kc-login"]')
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
        page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=20); time.sleep(1.3)
        page.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]').first.click()
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
        try:
            page.click('[id="screenToolbar:form:minmaxMenu"]', timeout=10000)
            page.wait_for_load_state("networkidle", timeout=15000); time.sleep(0.6)
        except Exception as e:
            print(f"expand skipped: {str(e)[:50]}")
        fr = get_frame(page)
        fr.fill('[id="nav:form:G:0:R:1:C:0:da_input"]', SCOPE["date"])
        fr.fill('[id="nav:form:G:1:R:1:C:0:da_input"]', SCOPE["date"]); time.sleep(0.4)
        pick(fr, 2, SCOPE["pu"]); pick(fr, 3, SCOPE["area"]); pick(fr, 4, SCOPE["fcty"]); pick(fr, 5, SCOPE["flowline"])
        reload_go(page, fr)
        page.screenshot(path=str(EVID / "01_grid_loaded.png"))
        set_cell(fr, SET_VALUE); save(page, fr); reload_go(page, fr)
        res["set"] = val(o); page.screenshot(path=str(EVID / "02_value_set.png"))
        print(f"  [SET] cell={SET_VALUE}, DB={res['set']} - holding {HOLD}s"); time.sleep(HOLD)
        set_cell(fr, CHANGE_VALUE); save(page, fr); reload_go(page, fr)
        res["change"] = val(o); page.screenshot(path=str(EVID / "03_value_changed.png"))
        print(f"  [CHANGE] cell={CHANGE_VALUE}, DB={res['change']} - holding {HOLD}s"); time.sleep(HOLD)
        set_cell(fr, ""); save(page, fr); reload_go(page, fr)
        res["clear"] = val(o); page.screenshot(path=str(EVID / "04_value_cleared.png"))
        print(f"  [CLEAR] cell cleared, DB={res['clear']} - holding {HOLD * 2}s (watch the empty cell)")
        time.sleep(HOLD * 2)
        b.close()
    print(f"SET    DB={res['set']} -> {'PASS' if str(res['set']) == SET_VALUE else 'FAIL'}")
    print(f"CHANGE DB={res['change']} -> {'PASS' if str(res['change']) == CHANGE_VALUE else 'FAIL'}")
    print(f"CLEAR  DB={res['clear']} -> {'PASS' if res['clear'] is None else 'FAIL'}  (update-to-null, not a record delete)")
    c = db(); cur = c.cursor()
    cur.execute("UPDATE IFLW_DAY_STATUS SET ON_STREAM_HRS=NULL WHERE OBJECT_ID=:o AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD')", {"o": o, "d": SCOPE["date"]})
    c.commit(); c.close()
    print(f"final DB (restored) = {val(o)}"); print("DONE")


if __name__ == "__main__":
    main()
