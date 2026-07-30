"""READ-ONLY: resolve Disposition Type's treeview menu path (for RF/bundle folder placement)."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    sb = pg.locator('#menu\\:searchForm\\:searchTxt'); sb.fill(""); sb.type("Disposition Type", delay=40); pg.wait_for_timeout(1800)
    # dump each search-result label + its title/tooltip (EC sets full menu path on title)
    res = pg.evaluate("""()=>{const o=[];document.querySelectorAll('label.tv-link').forEach(e=>{o.push({text:(e.innerText||'').trim(),title:(e.getAttribute('title')||'').trim(),parentTitle:(e.closest('[title]')?e.closest('[title]').getAttribute('title'):'')});});return o;}""")
    for r in res: print(r)
    # also open it + read any breadcrumb / screen path hints
    lbl = pg.locator("xpath=//label[contains(@class,'tv-link') and normalize-space()='Disposition Type']").first
    if lbl.count():
        # walk up ancestors for tooltip/path text
        anc = lbl.evaluate("""el=>{let cur=el,out=[];for(let i=0;i<8 && cur;i++){const t=cur.getAttribute&&cur.getAttribute('title');if(t)out.push(t);cur=cur.parentElement;}return out;}""")
        print("ancestor titles:", anc)
    br.close()
