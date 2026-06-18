"""LIVE DOM recon for Contract Area (OV) - the generic scan_ec_screen can't fill a mandatory navigator
dropdown. This: login -> open -> dump nav fields -> pick BU 'ECP Norway' -> GO -> grid id -> select row
-> updateAttributes + objectdates(End Date C:3) -> New Object -> objectForm ids/mandatory/labels.
READ-ONLY (never Saves). Usage: EC_HEADED=1 py -X utf8 tmp/scripts/recon_ca_live.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER = os.environ.get("EC_USER", "sysadmin")
PWD = os.environ.get("EC_PWD", "sysadmin")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
BU_LABEL = os.environ.get("CA_BU", "ECP Norway")
YELLOW = "rgb(252, 249, 192)"
OUT = "tmp/recon_contract_area"
os.makedirs(OUT, exist_ok=True)


def ajax(page, t=20000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def esc(i):
    return "#" + i.replace(":", "\\:")


def dump(page, sub):
    return page.evaluate("""(args) => { const [sub,Y]=args;
        return [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id && e.id.includes(sub) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor===Y; let lab='';
            const m=e.id.match(/^(.*:R:\\d+):C:\\d+:/);
            if(m){const lc=document.querySelector("[id^='"+m[1]+":C:0']"); if(lc) lab=(lc.innerText||lc.value||'').trim();}
            return {id:e.id, mandatory:y, label:lab}; }).slice(0,40); }""", [sub, YELLOW])


with sync_playwright() as p:
    b = p.chromium.launch(headless=not HEADED, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=60000); page.wait_for_timeout(2500)
    for u in ("#username", "input[name='username']"):
        if page.locator(u).count(): page.fill(u, USER); break
    for pw in ("#password", "input[name='password']"):
        if page.locator(pw).count(): page.fill(pw, PWD); break
    for btn in ("#kc-login", "input[type='submit']", "button[type='submit']"):
        if page.locator(btn).count():
            try: page.locator(btn).first.click(); break
            except Exception: pass
    page.wait_for_timeout(3000); ajax(page)
    print("after-login:", page.title())

    box = page.locator(esc("menu:searchForm:searchTxt"))
    box.click(); box.fill(""); box.type("Contract Area", delay=45); ajax(page, 8000)
    page.locator("xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='Contract Area']").first.click()
    ajax(page)
    mm = page.locator(esc("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible(): mm.first.click(); ajax(page)

    nav = page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:G:']")]
        .filter(e=>['INPUT','SELECT'].includes(e.tagName) && e.type!=='hidden').map(e=>e.id)""")
    print("\nNAV input ids:", nav)
    dd = next((i[:-len("_input")] for i in nav if i.endswith("dd_input")), "nav:form:G:0:R:1:C:0:dd")
    print("nav dd base:", dd)

    for trig in (dd+"_btn", dd+"_button"):
        if page.locator(esc(trig)).count():
            try: page.locator(esc(trig)).first.click(); break
            except Exception: pass
    page.wait_for_timeout(1200)
    target = page.locator(f"xpath=//*[@id='{dd}_panel']//*[normalize-space(@data-item-label)='{BU_LABEL}']")
    print(f"BU '{BU_LABEL}' option present:", target.count())
    if target.count():
        target.first.click(); ajax(page, 12000)

    for g in ("button:form:B", "go_button:form:B"):
        if page.locator(esc(g)).count():
            try: page.locator(esc(g)).first.click(); ajax(page, 25000); print("GO ->", g); break
            except Exception: pass
    page.screenshot(path=f"{OUT}/01_loaded.png", full_page=True)
    grid = page.evaluate("""() => { const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.querySelector('tr')); return t.length?t[0].id:null; }""")
    print("grid id:", grid)
    if grid:
        rc = page.locator(f"xpath=//*[@id='{grid}']/tr").count()
        print("grid row count:", rc)

    try:
        sp = page.locator(f"xpath=//*[@id='{grid}']//tr[1]//span[normalize-space(text())!='']").first
        if sp.count():
            print("selecting row span:", (sp.text_content() or '').strip())
            sp.click(); ajax(page); page.wait_for_timeout(800)
            print("\nUPDATE updateAttributes fields:")
            for f in dump(page, "updateAttributes:form")[:12]:
                print(f"   {f['id']:60s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
            print("DELETE objectdates fields (End Date should be C:3):")
            for f in dump(page, "objectdates:form"):
                print(f"   {f['id']:60s} {f['label'][:22]}")
    except Exception as e:
        print("row err:", str(e)[:90])

    try:
        page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
        page.wait_for_timeout(900)
        links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
        for i in range(links.count()):
            if links.nth(i).is_visible() and (links.nth(i).text_content(timeout=800) or "").strip() == "New Object":
                links.nth(i).click(); break
        ajax(page)
        page.screenshot(path=f"{OUT}/02_new_object.png", full_page=True)
        print("\nINSERT objectForm fields:")
        for f in dump(page, "objectForm:form"):
            print(f"   {f['id']:60s} mand={f['mandatory']!s:5s} {f['label'][:22]}")
    except Exception as e:
        print("insert err:", str(e)[:90])
    b.close()
print(f"\nDONE (read-only). Shots in {OUT}/")
