"""ECSR-35331 nav map - remaining screens (Liquid / Electrical / Tank). RELOADS the app between screens so
the search box is always available (the prior bug). Read-only, NO Save. Usage: py tmp/scripts/ecsr_nav_map2.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = "https://dev.non-prod.plp.wde.ecaas.cloud/"
USER, PWD = "quorum", os.environ.get("EC_WEB_PWD","")
DATE = "2026-05-12"
KW = ["rundown", "condensate", "electric", "tank", "lng", "power", "energy", "load"]


def ajax(page, t=30000):
    try: page.wait_for_load_state("networkidle", timeout=t)
    except Exception: pass
    page.wait_for_timeout(1000)


def esc(i): return "#" + i.replace(":", "\\:")


def dd_options(page, g):
    base = f"nav:form:G:{g}:R:1:C:0:dd"
    for trig in (base + "_btn", base + "_button"):
        if page.locator(esc(trig)).count():
            try: page.locator(esc(trig)).first.click(); break
            except Exception: pass
    else:
        try: page.locator(esc(base + "_input")).first.click()
        except Exception: pass
    page.wait_for_timeout(900)
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
    page.wait_for_timeout(700)
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
    return page.evaluate("""(kw) => { const s=new Set();
        document.querySelectorAll('tr').forEach(tr=>{const c=tr.querySelector('td,th'); if(!c)return;
        const t=(c.innerText||'').replace(/\\s+/g,' ').trim();
        if(t && kw.some(k=>t.toLowerCase().includes(k))) s.add(t.slice(0,60));}); return [...s]; }""", KW)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(3000)
    if page.locator("#username").count():
        page.fill("#username", USER); page.fill("#password", PWD)
        (page.locator("#kc-login").first.click() if page.locator("#kc-login").count() else page.press("#password", "Enter"))
        page.wait_for_timeout(4000); ajax(page)
    print("login:", page.title())

    for scr in ["Daily Liquid Stream Status", "Daily Electrical Stream Status", "Daily Tank Status - VCF Calc"]:
        print(f"\n########## {scr} ##########")
        try:
            page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); ajax(page, 15000)
            box = page.locator("#menu\\:searchForm\\:searchTxt")
            box.wait_for(timeout=20000); box.click(); box.fill(""); box.type(scr, delay=35); ajax(page, 8000)
            page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={repr(scr)}]").first.click()
            ajax(page)
            d = page.locator(esc("nav:form:G:0:R:1:C:0:da_input"))
            if d.count():
                d.click(); d.fill(""); d.type(DATE, delay=35); page.keyboard.press("Tab"); ajax(page, 7000)
            # navigator field structure
            fields = page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:G:']")]
                .filter(e=>e.tagName==='INPUT').map(e=>e.id).filter(id=>/da_input|dd_input$/.test(id))""")
            print("  nav fields:", fields)
            puo = dd_options(page, 1); print("  PU:", puo[:6])
            if "Pluto Scarborough" in puo: dd_pick(page, 1, "Pluto Scarborough")
            elif puo: dd_pick(page, 1, puo[0])
            aro = dd_options(page, 2); print("  Area:", aro[:10])
            if "Burrup LNG Park" in aro: dd_pick(page, 2, "Burrup LNG Park")
            elif aro: dd_pick(page, 2, aro[0])
            fco = dd_options(page, 3); print("  Facility Class 1:", fco)
            for fac in fco:
                if dd_pick(page, 3, fac):
                    go(page); h = hits(page)
                    if h: print(f"   [{fac}] -> {h}")
        except Exception as e:
            print("  err:", str(e)[:100])
    b.close()
print("\nDONE (read-only; no Save).")
