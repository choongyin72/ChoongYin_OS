"""ECSR-35331 item-1 live re-verify on ECAASDEV (read-only, NO Save). Login -> Daily Gas Stream Status ->
set Date 2026-05-12 -> cascade PU/Area/Facility -> GO -> read exact navigator values + the Train 1 LNG
Rundown row. Dumps dropdown options so we capture the exact Area name. Usage: py tmp/scripts/ecsr_drive.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = "https://dev.non-prod.plp.wde.ecaas.cloud/"
USER, PWD = "quorum", os.environ.get("EC_WEB_PWD","")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
OUT = "tmp/ecsr_recon"
os.makedirs(OUT, exist_ok=True)


def ajax(page, t=25000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(1200)


def esc(i):
    return "#" + i.replace(":", "\\:")


def dropdown(page, g, want=None):
    """Open nav dropdown G:g, return option labels; if want substr given, click the matching option."""
    base = f"nav:form:G:{g}:R:1:C:0:dd"
    # open: try the autocomplete dropdown trigger, else click the input
    opened = False
    for trig in (base + "_btn", base + "_button"):
        loc = page.locator(esc(trig))
        if loc.count():
            try:
                loc.first.click(); opened = True; break
            except Exception:
                pass
    if not opened:
        try:
            page.locator(esc(base + "_input")).first.click()
        except Exception:
            pass
    page.wait_for_timeout(1500)
    opts = []
    rows = page.locator(f"xpath=//*[@id='{base}_panel']//*[@data-item-label]")
    for i in range(min(rows.count(), 60)):
        lbl = rows.nth(i).get_attribute("data-item-label")
        if lbl:
            opts.append(lbl.strip())
    if want:
        tgt = page.locator(
            f"xpath=//*[@id='{base}_panel']//*[@data-item-label][contains(translate(@data-item-label,"
            f"'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'),'{want.upper()}')]")
        if tgt.count():
            tgt.first.click(); ajax(page, 12000)
        else:
            page.keyboard.press("Escape")
    return opts


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(3000)
    # login
    if page.locator("#username").count():
        page.fill("#username", USER); page.fill("#password", PWD)
        (page.locator("#kc-login").first.click() if page.locator("#kc-login").count()
         else page.press("#password", "Enter"))
        page.wait_for_timeout(4000); ajax(page)
    print("title:", page.title())
    # open screen
    box = page.locator("#menu\\:searchForm\\:searchTxt")
    box.click(); box.fill(""); box.type("Daily Gas Stream Status", delay=40); ajax(page, 9000)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Daily Gas Stream Status']").first.click()
    ajax(page)
    mm = page.locator("#screenToolbar\\:form\\:minmaxMenu")
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)

    # set date 2026-05-12
    d = page.locator(esc("nav:form:G:0:R:1:C:0:da_input"))
    if d.count():
        d.click(); d.fill(""); d.type("2026-05-12", delay=40); page.keyboard.press("Tab"); ajax(page, 8000)

    print("\n-- PU (G:1) options --");  pu = dropdown(page, 1, "pluto"); print("  ", pu[:20])
    print("-- Area (G:2) options --");  ar = dropdown(page, 2, "lng");   print("  ", ar[:30])
    print("-- Facility (G:3) options --"); fc = dropdown(page, 3, "train 1"); print("  ", fc[:30])

    # read the EXACT selected navigator values
    vals = page.evaluate("""() => {
        const g = i => (document.getElementById(i)||{}).value || '';
        return {date: g('nav:form:G:0:R:1:C:0:da_input'),
                pu:   g('nav:form:G:1:R:1:C:0:dd_input'),
                area: g('nav:form:G:2:R:1:C:0:dd_input'),
                fac:  g('nav:form:G:3:R:1:C:0:dd_input')}; }""")
    print("\n=== SELECTED NAVIGATOR ===", vals)
    page.screenshot(path=f"{OUT}/05_nav_filled.png")

    # GO
    for go in ("button:form:B", "go_button:form:B", "navButton:form:B"):
        loc = page.locator(esc(go))
        if loc.count():
            try:
                loc.first.click(); ajax(page, 30000); print("clicked GO:", go); break
            except Exception:
                pass
    page.screenshot(path=f"{OUT}/06_after_go.png", full_page=True)

    # find any row mentioning Rundown + its cell values
    rows = page.evaluate("""() => {
        const out = [];
        document.querySelectorAll('tr').forEach(tr => {
            const t = (tr.innerText||'').replace(/\\s+/g,' ').trim();
            if (/rundown/i.test(t)) out.push(t.slice(0,220));
        });
        return out.slice(0,10); }""")
    print("\n=== grid rows containing 'Rundown' ===")
    for r in rows:
        print("  ", r)

    b.close()
print(f"\nDONE (read-only; no Save). Screenshots in {OUT}/")
