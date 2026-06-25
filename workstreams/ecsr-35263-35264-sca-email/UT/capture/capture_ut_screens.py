# -*- coding: utf-8 -*-
"""
Deterministic capture of the 11 MHM email-config screens for an ECSR-35264 UT doc.

Reproducible source for UT_ECSR-35264__<REPORT>.docx. Field-ids come from the
learn-once reference: workstreams/master-plan/ec-automation/docs/ec_messaging_screens.md
(consult that FIRST; do not trial-and-error screen locators).

Usage:   EC_USER=Sysadmin EC_PASS=*** py capture_ut_screens.py pluto|sca
Output:  <OUT_DIR>/<variant>/NN_<screen>.png   (OUT_DIR defaults to ./shots)

Credentials/URL are read from env (never hardcoded). On COPSDEV/plutodev:
  EC_URL  default https://app-plutodev.woodside-pluto.tieto-og.cloud/
  EC_USER / EC_PASS  (the Sysadmin web login)
SMTP is not configured on COPSDEV, so SEND/queueing is safe (no real mail).
"""
import os, sys
from playwright.sync_api import sync_playwright

URL = os.environ.get("EC_URL", "https://app-plutodev.woodside-pluto.tieto-og.cloud/")
U   = os.environ.get("EC_USER", "")
P   = os.environ.get("EC_PASS", "")
V   = (sys.argv[1] if len(sys.argv) > 1 else "pluto").lower()
OUT = os.path.join(os.environ.get("OUT_DIR", os.path.join(os.path.dirname(__file__), "shots")), V)
os.makedirs(OUT, exist_ok=True)

CFG = {
    "pluto": {"def": "R_BLP_DAILY_PROD_ALLOC_PLUTO", "set": "R_BLP_DAILY_PROD_ALLOC_PLU",
              "report": "Burrup LNG Park Daily Production Report (Pluto)",
              "outsubj": "Burrup LNG Park Daily Production Report 20 May"},
    "sca":   {"def": "R_BLP_DAILY_PROD_ALLOC_SCA", "set": "R_BLP_DAILY_PROD_ALLOC_SCA",
              "report": "Burrup LNG Park Daily Production Report (Scarborough)",
              "outsubj": "(Scarborough)"},
}[V]

# screen, primary text-filter id (or None), filter value, output name
CONFIG_SCREENS = [
    ("Maintain Message Type",      "manageObject:form:T:sfilter0_ft_filter", CFG["def"], "01_msgtype"),
    ("Freetext Message Template",  None,                                     CFG["def"], "03_freetext"),
    ("Maintain Contact Group Set", "manageObject:form:T:sfilter0_ft_filter", CFG["set"], "04_contactgroupset"),
    ("Distribution List",          "list:form:T:sfilter0_ft_filter",         CFG["set"], "06_distlist"),
    ("Message Distribution",       "manageObject:form:T:sfilter0_ft_filter", CFG["def"], "07_msgdistribution"),
    ("Report Administration",      "runable_reports:form:T:sfilter0_ft_filter", CFG["report"], "08_reportadmin"),
    ("Schedules",                  "schedule:form:T:sfilter0_ft_filter",     "ZWP_SEND_BPM_NOTIFICATIONS", "09_schedules"),
]


def open_screen(pg, name):
    b = pg.locator('[id="menu:searchForm:searchTxt"]'); b.click(); b.fill(""); b.type(name, delay=15)
    pg.wait_for_timeout(1400)
    lk = pg.locator(f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{name}"]')
    if not lk.count():
        return False
    lk.first.click(); pg.wait_for_load_state("networkidle", timeout=45000); pg.wait_for_timeout(2500)
    return True


def content_frame(pg, sel='[id^="nav:"],[id*="sfilter"],[id*=":form:T:"]'):
    for f in pg.frames:
        try:
            if f.locator(sel).count():
                return f
        except Exception:
            pass
    return pg


def set_fa_ec(fr, pg):
    """Set the Functional Area navigator dropdown to EC and click GO (if a navigator is present)."""
    nb = fr.locator('[id^="nav:"][id$="dd_button"]')
    if not nb.count():
        return
    bid = nb.first.get_attribute("id"); panel = bid[:-7] + "_panel"
    nb.first.click(); pg.wait_for_timeout(900)
    ec = fr.locator(f'xpath=//*[@id="{panel}"]//tr[normalize-space(@data-item-label)="EC"]')
    if ec.count():
        ec.first.click(); pg.wait_for_timeout(600)
    go = fr.locator('[id="button:form:B"]')
    if go.count():
        go.first.click(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2200)


def shoot(pg, name):
    pg.screenshot(path=os.path.join(OUT, name + ".png"), full_page=True)
    print(f"  {name}")


def run(pg):
    # --- standard config screens (FA=EC + GO, then text-filter + select row) ---
    for name, fid, val, outn in CONFIG_SCREENS:
        if not open_screen(pg, name):
            print(f"  !! {name} not found"); continue
        fr = content_frame(pg)
        set_fa_ec(fr, pg)
        if fid:
            flt = fr.locator(f'[id="{fid}"]')
            if flt.count():
                flt.first.click(); flt.first.fill(val); flt.first.press("Enter"); pg.wait_for_timeout(2600)
        row = fr.locator(f'xpath=//tr[.//text()[contains(.,"{val}")]]')
        if row.count():
            row.first.click(); pg.wait_for_timeout(1500)
        shoot(pg, outn)

    # --- Message Format (2): Message Type is a MANDATORY navigator dropdown set before GO ---
    if open_screen(pg, "Message Format"):
        fr = content_frame(pg)
        dds = fr.locator('[id^="nav:"][id$="dd_button"]')
        n = dds.count()
        if n >= 1:                                   # dd 0 = Functional Area -> EC
            bid = dds.nth(0).get_attribute("id"); pan = bid[:-7] + "_panel"
            dds.nth(0).click(); pg.wait_for_timeout(800)
            ec = fr.locator(f'xpath=//*[@id="{pan}"]//tr[normalize-space(@data-item-label)="EC"]')
            if ec.count():
                ec.first.click(); pg.wait_for_timeout(600)
        for i in range(1, n):                        # later dd = Message Type -> the def code
            bid = dds.nth(i).get_attribute("id"); pan = bid[:-7] + "_panel"
            dds.nth(i).click(); pg.wait_for_timeout(800)
            opt = fr.locator(f'xpath=//*[@id="{pan}"]//tr[contains(@data-item-label,"{CFG["def"]}") '
                             f'or .//text()[contains(.,"{CFG["def"]}")]]')
            if opt.count():
                opt.first.click(); pg.wait_for_timeout(800); break
        go = fr.locator('[id="button:form:B"]')
        if go.count():
            go.first.click(); pg.wait_for_load_state("networkidle"); pg.wait_for_timeout(2200)
        shoot(pg, "02_msgformat")

    # --- Actor Maintenance (5): FA=EC + GO ---
    if open_screen(pg, "Actor Maintenance"):
        fr = content_frame(pg)
        set_fa_ec(fr, pg)
        shoot(pg, "05_actormaint")

    # --- Outgoing Messages (10): no navigator; filter by Subject (sfilter2) ---
    if open_screen(pg, "Outgoing Messages"):
        fr = content_frame(pg, '[id="outmess:form:T:sfilter2_ft_filter"]')
        flt = fr.locator('[id="outmess:form:T:sfilter2_ft_filter"]')
        if flt.count():
            flt.first.click(); flt.first.fill(CFG["outsubj"]); flt.first.press("Enter"); pg.wait_for_timeout(2800)
        cell = fr.locator('[id="outmess:form:T:0:C1_in"]')
        if cell.count():
            cell.first.click(); pg.wait_for_timeout(1200)
        shoot(pg, "10_outgoing")
    # NOTE: section 11 (Preview) uses the verbatim rendered subject/body from MESSAGE_OUT
    # (see fetch_message_content.py) rather than a screenshot -- VIEW returns plain text
    # that the browser renders as an XML-parse error, so it is not a usable image.


with sync_playwright() as p:
    br = p.chromium.launch(headless=True)
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    pg.goto(URL, wait_until="domcontentloaded", timeout=60000); pg.wait_for_timeout(2500)
    if pg.locator("#username").count():
        pg.fill("#username", U); pg.fill("#password", P); pg.click("#kc-login")
    pg.wait_for_timeout(6000)
    run(pg)
    br.close()
print(f"DONE ({V}) -> {OUT}")
