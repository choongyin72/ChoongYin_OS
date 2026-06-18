"""ECSR-35331 navigator MAP (read-only, NO Save). For each relevant daily-status screen, set Date/PU/Area,
sweep Facility Class 1 options, GO, and report which facility holds the defect streams (rundown/flare/
inlet/BOG/condensate/electrical/tank). Builds the per-item navigator table. Usage: py tmp/scripts/ecsr_nav_map.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = "https://dev.non-prod.plp.wde.ecaas.cloud/"
USER, PWD = "quorum", os.environ.get("EC_WEB_PWD","")
DATE = "2026-05-12"
OUT = "tmp/ecsr_recon"
os.makedirs(OUT, exist_ok=True)
KW = ["rundown", "flare", "inlet", "bog", "boil", "condensate", "electric", "tank", "lng", "vapour", "vapor"]


def ajax(page, t=30000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(1000)


def esc(i):
    return "#" + i.replace(":", "\\:")


def dd_options(page, g):
    base = f"nav:form:G:{g}:R:1:C:0:dd"
    for trig in (base + "_btn", base + "_button"):
        if page.locator(esc(trig)).count():
            try: page.locator(esc(trig)).first.click(); break
            except Exception: pass
    else:
        try: page.locator(esc(base + "_input")).first.click()
        except Exception: pass
    page.wait_for_timeout(1000)
    rows = page.locator(f"xpath=//*[@id='{base}_panel']//*[@data-item-label]")
    opts = [rows.nth(i).get_attribute("data-item-label").strip()
            for i in range(min(rows.count(), 60)) if rows.nth(i).get_attribute("data-item-label")]
    page.keyboard.press("Escape")
    return opts


def dd_pick(page, g, label):
    base = f"nav:form:G:{g}:R:1:C:0:dd"
    for trig in (base + "_btn", base + "_button"):
        if page.locator(esc(trig)).count():
            try: page.locator(esc(trig)).first.click(); break
            except Exception: pass
    else:
        try: page.locator(esc(base + "_input")).first.click()
        except Exception: pass
    page.wait_for_timeout(800)
    tgt = page.locator(f"xpath=//*[@id='{base}_panel']//*[@data-item-label={repr(label)}]")
    if tgt.count():
        tgt.first.click(); ajax(page, 12000); return True
    page.keyboard.press("Escape"); return False


def go(page):
    for g in ("button:form:B", "go_button:form:B", "navButton:form:B"):
        if page.locator(esc(g)).count():
            try: page.locator(esc(g)).first.click(); ajax(page, 30000); return True
            except Exception: pass
    return False


def hits(page):
    """stream-name lines in the grid matching any keyword."""
    return page.evaluate("""(kw) => {
        const seen = new Set();
        document.querySelectorAll('tr').forEach(tr => {
            const c = tr.querySelector('td,th'); if(!c) return;
            const t = (c.innerText||'').replace(/\\s+/g,' ').trim();
            if (t && kw.some(k => t.toLowerCase().includes(k))) seen.add(t.slice(0,60));
        });
        return [...seen]; }""", KW)


def open_screen(page, name):
    box = page.locator("#menu\\:searchForm\\:searchTxt")
    box.click(); box.fill(""); box.type(name, delay=35); ajax(page, 8000)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={repr(name)}]").first.click()
    ajax(page)
    mm = page.locator("#screenToolbar\\:form\\:minmaxMenu")
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)
    d = page.locator(esc("nav:form:G:0:R:1:C:0:da_input"))
    if d.count():
        d.click(); d.fill(""); d.type(DATE, delay=35); page.keyboard.press("Tab"); ajax(page, 7000)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(3000)
    if page.locator("#username").count():
        page.fill("#username", USER); page.fill("#password", PWD)
        (page.locator("#kc-login").first.click() if page.locator("#kc-login").count() else page.press("#password", "Enter"))
        page.wait_for_timeout(4000); ajax(page)
    print("login title:", page.title())

    SCREENS = ["Daily Gas Stream Status", "Daily Liquid Stream Status",
               "Daily Electrical Stream Status", "Daily Tank Status - VCF Calc"]
    for scr in SCREENS:
        print(f"\n########## {scr} ##########")
        try:
            open_screen(page, scr)
        except Exception as e:
            print("  open err:", str(e)[:90]); continue
        # navigator group labels (field count) + PU/Area current
        pu_opts = dd_options(page, 1)
        print("  PU options:", pu_opts[:6])
        if pu_opts:
            dd_pick(page, 1, "Pluto Scarborough") if "Pluto Scarborough" in pu_opts else dd_pick(page, 1, pu_opts[0])
        area_opts = dd_options(page, 2)
        print("  Area options:", area_opts[:10])
        if "Burrup LNG Park" in area_opts:
            dd_pick(page, 2, "Burrup LNG Park")
        elif area_opts:
            dd_pick(page, 2, area_opts[0])
        fac_opts = dd_options(page, 3)
        print("  Facility Class 1 options:", fac_opts)
        # sweep each facility, GO, report keyword stream hits
        for fac in fac_opts:
            if not dd_pick(page, 3, fac):
                continue
            go(page)
            h = hits(page)
            if h:
                print(f"   [{fac}] -> {h}")
    b.close()
print("\nDONE (read-only; no Save).")
