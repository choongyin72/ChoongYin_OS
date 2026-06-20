"""Deep-dive (evidence-first): locate the EC table 'hamburger' column menu on the Business Function screen,
open it, and capture the EXACT menu items + their DOM ids/onclick. READ-ONLY (just opens the menu; does NOT
click any item, does NOT paste/save). Screenshots for proof. py -X utf8 tmp/scripts/recon_table_hamburger.py"""
import os
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
USER, PWD = os.environ.get("EC_USER", "sysadmin"), os.environ.get("EC_PASS", "sysadmin")
OUT = "tmp/recon_hamburger"
os.makedirs(OUT, exist_ok=True)


def esc(i):
    return "#" + i.replace(":", "\\:")


def ajax(page, t=20000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", USER); page.fill("#password", PWD); page.click("#kc-login")
    page.wait_for_selector(esc("menu:searchForm:searchTxt"), timeout=60000); ajax(page)
    box = page.locator(esc("menu:searchForm:searchTxt")); box.click(); box.type("Business Function", delay=45); ajax(page, 7000)
    page.locator("xpath=//*[contains(@class,'tv-link') and normalize-space(text())='Business Function']").first.click()
    ajax(page)
    page.screenshot(path=f"{OUT}/01_grid.png", full_page=False)

    # 1) Find the hamburger trigger: scan the first table header region for menu-toggle-ish elements
    cand = page.evaluate("""() => {
        const out=[];
        document.querySelectorAll("thead th, .ui-datatable-header, [class*='colMenu'], [class*='column-menu'], [class*='menuButton'], [class*='tableMenu'], th a, th span[class*='icon']").forEach(e=>{
            const cls=e.className||''; const t=(e.title||e.getAttribute('aria-label')||'').trim();
            if(/menu|hamburger|colMenu|gear|cog|option/i.test(cls+' '+t) || (e.tagName==='A' && e.closest('th'))){
                out.push({tag:e.tagName, id:e.id, cls:(''+cls).slice(0,60), title:t});
            }});
        return out.slice(0,25);
    }""")
    print("=== candidate hamburger/menu-toggle elements in header ===")
    for c in cand:
        print("  ", c)

    # 2) Find the menu container by its item text, and dump its items (text + id + onclick)
    menu = page.evaluate("""() => {
        const wanted=['filtering','scrollbar','Freeze','rows/page','clipboard','hide columns','personalis'];
        // find a UL/DIV that contains several of these texts
        let best=null,bestN=0;
        document.querySelectorAll('ul,div').forEach(c=>{
            const txt=c.innerText||''; const n=wanted.filter(w=>txt.includes(w)).length;
            if(n>bestN && n>=3 && c.querySelectorAll('a,li').length<40){best=c;bestN=n;}
        });
        if(!best) return {found:false};
        const items=[...best.querySelectorAll('li a, a, li')].map(a=>({
            text:(a.innerText||'').trim().slice(0,40), id:a.id||'',
            onclick:(a.getAttribute('onclick')||'').slice(0,70)
        })).filter(x=>x.text);
        return {found:true, containerId:best.id, containerCls:(best.className||'').slice(0,60),
                visible: best.offsetParent!==null, items:items.slice(0,15)};
    }""")
    print("\n=== menu container + items (by text match) ===")
    print("  found:", menu.get("found"), " containerId:", menu.get("containerId"),
          " cls:", menu.get("containerCls"), " visible:", menu.get("visible"))
    for it in (menu.get("items") or []):
        print(f"   text={it['text']!r:42s} id={it['id']!r} onclick={it['onclick']!r}")

    b.close()
print(f"\nDONE (read-only; menu not actioned). Shots in {OUT}/")
