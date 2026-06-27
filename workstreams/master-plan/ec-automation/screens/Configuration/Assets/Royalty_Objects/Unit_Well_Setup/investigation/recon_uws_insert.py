"""RC.0050 Unit - Well Setup: LIVE recon of the insert/delete gesture (READ-ONLY, no Save).
Gated nav -> Unit Agreement 3 (empty) -> GO -> inspect Insert submenu, the blank row cells
(+ mandatory/yellow), the perf-interval dd options, and the Delete submenu.
Local sandbox web sysadmin/sysadmin. ASCII output."""
from playwright.sync_api import sync_playwright
import os, json

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")
SCREEN = "Unit - Well Setup"
NAV_UA = "Unit Agreement 3"
SS = r"C:\tmp\wt-uws2\tmp\screens"; os.makedirs(SS, exist_ok=True)


def ajax(pg, t=20000):
    pg.wait_for_load_state("networkidle", timeout=t); pg.wait_for_timeout(900)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
    pg.set_default_timeout(30000)
    pg.goto(EC_URL, wait_until="domcontentloaded", timeout=40000)
    pg.fill("#username", EC_USER); pg.fill("#password", EC_PASS); pg.click("#kc-login")
    pg.wait_for_url("**/dashboard**", timeout=60000); ajax(pg)
    si = pg.locator('#menu\\:searchForm\\:searchTxt'); si.wait_for(state="visible", timeout=15000)
    si.clear(); si.type(SCREEN, delay=40); pg.wait_for_load_state("networkidle", timeout=10000); pg.wait_for_timeout(500)
    pg.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{SCREEN}']").first.click()
    ajax(pg)

    # nav fields
    nav = pg.evaluate("""() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
        const m=e.id.match(/nav:form:G:\\d+:R:\\d+:C:\\d+:(da_input|dd_input|in)$/); if(m) out.push({id:e.id,kind:m[1]}); }); return out; }""")
    print("NAV FIELDS:", [f["id"] for f in nav])
    dd = next((f["id"] for f in nav if f["kind"] == "dd_input"), None)
    print("NAV DD:", dd)
    if dd:
        ddp = dd[:-len("_input")]
        pg.locator(f'#{ddp.replace(":","\\:")}_button').first.click(); pg.wait_for_timeout(800)
        opts = pg.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
        print("NAV DD options:", [opts.nth(i).get_attribute("data-item-label").strip() for i in range(min(opts.count(),8))])
        row = pg.locator(f"xpath=//*[@id='{ddp}_panel']//tr[normalize-space(@data-item-label)='{NAV_UA}']").first
        (row if row.count() else opts.first).click(); pg.wait_for_timeout(400)
    for gid in ("go_button:form:B","button:form:B","navButton:form:B"):
        if pg.locator(f'#{gid.replace(":","\\:")}').count(): pg.locator(f'#{gid.replace(":","\\:")}').first.click(); print("GO:",gid); break
    ajax(pg)
    pg.screenshot(path=SS+r"\uws_recon_01_navd.png", full_page=True)

    # grid id + current rows
    gid = pg.evaluate("""() => { const t=[...document.querySelectorAll("[id$=':T_data']")].find(x=>x.id.includes('well_setup')||x.id.includes('setup')); return t? t.id : (document.querySelector("[id$=':T_data']")||{}).id; }""")
    print("GRID id:", gid)

    # INSERT toolbar: hover, dump submenu labels
    ins = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert') or contains(@class,'ui-icon-add')]]")
    print("insert parent count:", ins.count())
    if ins.count():
        ins.first.hover(); pg.wait_for_timeout(1000)
        subs = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        labels = []
        for i in range(subs.count()):
            try:
                if subs.nth(i).is_visible(): labels.append(subs.nth(i).text_content(timeout=800).strip())
            except Exception: pass
        print("INSERT submenu labels:", labels)
        # click first visible insert item
        for i in range(subs.count()):
            try:
                if subs.nth(i).is_visible(): subs.nth(i).click(); print("clicked insert:", subs.nth(i).text_content(timeout=500).strip()); break
            except Exception: pass
        ajax(pg)
        pg.screenshot(path=SS+r"\uws_recon_02_insert.png", full_page=True)
        # dump the (blank) grid row cells + mandatory(yellow) flags
        cells = pg.evaluate("""(gid) => { const Y='rgb(255, 255, 204)'; const out=[];
            document.querySelectorAll(`[id^='${gid.replace('_data','')}:'] input, [id^='${gid.replace('_data','')}:'] select, [id^='${gid.replace('_data','')}:'] textarea`).forEach(e=>{
              if(e.type==='hidden') return; const m=e.id.match(/T:(\\d+):C(\\d+)/); if(!m) return;
              out.push({id:e.id, row:+m[1], col:+m[2], val:e.value, mand:getComputedStyle(e).backgroundColor===Y}); });
            return out.slice(0,40); }""", gid or "well_setup:form:T_data")
        print("BLANK ROW cells:");
        for c in cells: print("   ", c)
        # perf-interval dd (C2) options
        c2 = next((c["id"] for c in cells if c["col"]==2 and c["id"].endswith("dd_input")), None)
        if c2:
            ddp2 = c2[:-len("_input")]
            try:
                pg.locator(f'#{ddp2.replace(":","\\:")}_button').first.click(); pg.wait_for_timeout(800)
                o2 = pg.locator(f"xpath=//*[@id='{ddp2}_panel']//tr[@data-item-label]")
                print("C2 perf-interval dd options (first 10):", [o2.nth(i).get_attribute("data-item-label").strip() for i in range(min(o2.count(),10))])
            except Exception as e: print("   c2 dd err", str(e)[:60])

    # DELETE toolbar submenu
    dele = pg.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-delete') or contains(@class,'ui-icon-minus') or contains(@class,'ui-icon-remove')]]")
    if dele.count():
        dele.first.hover(); pg.wait_for_timeout(800)
        subs = pg.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        dl = []
        for i in range(subs.count()):
            try:
                if subs.nth(i).is_visible(): dl.append(subs.nth(i).text_content(timeout=600).strip())
            except Exception: pass
        print("DELETE submenu labels:", dl)
    b.close()
print("DONE (read-only, nothing saved)")
