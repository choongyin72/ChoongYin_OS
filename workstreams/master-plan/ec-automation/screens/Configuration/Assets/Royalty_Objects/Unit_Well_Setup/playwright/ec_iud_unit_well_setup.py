"""EC IUD - Unit - Well Setup (Playwright reference, DEDICATED flow).

PARENT-CHILD setup screen (PC pattern): the navigator picks a form date + a Unit
Agreement + GO, then that agreement's WELL SETUP rows show in an inline TV-style
grid. This script adds one membership row (links a Perf Interval to the agreement)
and physically deletes it again:

  navigator: form date=2011-01-01, Unit Agreement='Unit Agreement 3' (UNIT_3, empty)
  member:    Perf Interval 108_WB1-1_PF1 - referenced only, the interval object
             itself is never modified
  oracle:    COUNT-DELTA on DV_UNIT_WELL_SETUP.PERF_INTERVAL_CODE
             (baseline -> +1 after insert -> baseline after delete)

Pre-flight verified 2026-06-27: UNIT_3 effective 2010-01-01 (open), 108_WB1-1_PF1
effective 2003-01-01 (open), UNIT_3 empty, member baseline 0 anywhere.
See unit_well_setup_sow.md for the analysis; README.md for run instructions.
"""
import json
import os

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOW_MO = int(os.environ.get("EC_SLOWMO", "400")) if HEADED else 0

UNIT_AGREEMENT = "Unit Agreement 3"
PERF_INTERVAL = "108_WB1-1_PF1"
FORM_DATE = "2011-01-01"
START_DATE = "2011-01-01"
GRID = "well_setup:form:T_data"
PREFIX = "well_setup:form:T"
NAV_DATE = "nav:form:G:0:R:1:C:0:da_input"
NAV_UA = "nav:form:G:1:R:1:C:0:dd"

BUNDLE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVIDENCE = os.path.join(BUNDLE, "evidence")
os.makedirs(EVIDENCE, exist_ok=True)
results = {}
n = [0]


def db_count():
    conn = oracledb.connect(user=os.environ.get("EC_DB_USER", "ECKERNEL_EC"),
                            password=os.environ.get("EC_DB_PASS", "energy"),
                            dsn=DB_DSN, tcp_connect_timeout=15)
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM DV_UNIT_WELL_SETUP WHERE PERF_INTERVAL_CODE = :c", c=PERF_INTERVAL)
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def _css(fid):
    return "#" + fid.replace(":", "\\:")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO,
                                args=["--ignore-certificate-errors"])
    ctx = browser.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080})
    page = ctx.new_page()

    def ss(label):
        n[0] += 1
        name = f"unit_well_setup_{n[0]:02d}_{label}.png"
        page.screenshot(path=os.path.join(EVIDENCE, name))
        print(f"  [SS] {name}")

    def ajax(t=15000):
        try:
            page.wait_for_load_state("networkidle", timeout=t)
        except Exception:
            pass
        page.wait_for_timeout(1200)

    def fill_date(fid, value):
        page.fill(_css(fid), value)
        page.keyboard.press("Tab")
        page.wait_for_timeout(700)

    def select_dd(dd, value):
        item = f"xpath=//*[@id='{dd}_panel']//tr[normalize-space(@data-item-label)='{value}']"
        page.click(_css(dd + "_button"))
        try:
            page.locator(item).first.wait_for(state="visible", timeout=6000)
        except Exception:
            page.keyboard.press("Escape")
            page.wait_for_timeout(1500)
            page.click(_css(dd + "_button"))
            page.locator(item).first.wait_for(state="visible", timeout=10000)
        page.locator(item).first.click()
        ajax(12000)

    def find_row(value):
        return page.evaluate(
            "(args) => { const [g, v] = args; const t=document.getElementById(g); if(!t) return -1;"
            " for (const e of t.querySelectorAll(\"input[id$='C2_dd_input']\")) {"
            "   if ((e.value||'')===v) { const m=e.id.match(/:T:(\\d+):/); if(m) return +m[1]; } }"
            " return -1; }", [GRID, value])

    def save():
        page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        ajax()

    def refresh():
        page.click("xpath=//a[@title='Refresh [Ctrl+r]']")
        ajax()

    print("=== LOGIN ===")
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=30000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    ajax()
    results["login"] = "PASS"

    print("=== NAVIGATE + NAVIGATOR ===")
    si = page.locator(_css("menu:searchForm:searchTxt"))
    si.clear()
    si.type("Unit - Well Setup", delay=60)
    ajax(8000)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link')"
                 " and normalize-space(text())='Unit - Well Setup']").first.click()
    ajax()
    fill_date(NAV_DATE, FORM_DATE)
    select_dd(NAV_UA, UNIT_AGREEMENT)
    page.click(_css("button:form:B"))
    ajax()
    results["navigate"] = "PASS"
    ss("loaded")

    base = db_count()
    print(f"=== CLEAN STATE === (DB baseline for {PERF_INTERVAL}: {base})")
    results["clean"] = "CLEAN" if find_row(PERF_INTERVAL) < 0 else "PRE-EXISTED"
    ss("clean_state")

    print("=== INSERT WELL SETUP ===")
    page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
    link = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                        "[.//span[contains(@class,'ui-icon-insert')]]"
                        "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Well Setup']")
    link.first.wait_for(state="visible", timeout=10000)
    link.first.click()
    ajax()
    row = find_row("")
    assert row >= 0, "no blank well-setup row appeared"
    select_dd(f"{PREFIX}:{row}:C2_dd", PERF_INTERVAL)
    row = find_row(PERF_INTERVAL)
    assert row >= 0, "well-setup row vanished after Perf Interval selection"
    fill_date(f"{PREFIX}:{row}:C0_da_input", START_DATE)
    ajax(12000)
    ss("insert_filled")
    save()
    refresh()
    ui_ok = find_row(PERF_INTERVAL) >= 0
    db_ok = db_count() == base + 1
    results["insert"] = "PASS" if (ui_ok and db_ok) else f"FAIL ui={ui_ok} db={db_count()} base={base}"
    ss("insert_result")
    print(f"  INSERT: {results['insert']}")

    print("=== DELETE WELL SETUP (physical) ===")
    if results["insert"] == "PASS":
        row = find_row(PERF_INTERVAL)
        # a SAVED row's start-date is a TEXT cell C0_in (new rows show calendar C0_da_input)
        page.click(_css(f"{PREFIX}:{row}:C0_in"))
        page.wait_for_timeout(800)
        page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete')]]")
        dlink = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                             "[.//span[contains(@class,'ui-icon-delete')]]"
                             "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='Well Setup']")
        dlink.first.wait_for(state="visible", timeout=10000)
        dlink.first.click()
        ajax()
        save()
        refresh()
        ui_gone = find_row(PERF_INTERVAL) < 0
        db_back = db_count() == base
        results["delete"] = "PASS (physical)" if (ui_gone and db_back) else \
            f"FAIL ui_gone={ui_gone} db={db_count()} base={base}"
    else:
        results["delete"] = "SKIP"
    ss("final_state")
    print(f"  DELETE: {results['delete']}")

    if HEADED:
        page.wait_for_timeout(4000)
    ctx.close()
    browser.close()

with open(os.path.join(EVIDENCE, "unit_well_setup_results.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("\nFINAL RESULTS")
ok_all = all(str(v).startswith(("PASS", "CLEAN")) for k, v in results.items() if k != "clean")
for k, v in results.items():
    print(f"  {k:<10}: {v}")
print(f"Overall: {'ALL PASS' if ok_all else 'SOME FAILURES'}")
raise SystemExit(0 if ok_all else 1)
