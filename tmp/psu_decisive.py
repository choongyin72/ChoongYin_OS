import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation");sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID="manageObject:form:T_data"
FIELDS=[{"label":"Production Sub Unit Code","value":"AUTOTEST_PSU_PROBE","kind":"text"},
        {"label":"Production Sub Unit Name","value":"AUTOTEST PSU Probe","kind":"text"},
        {"label":"Start Date","value":"2000-01-01","kind":"date"}]
def dump(pg,tag):
    info=pg.evaluate("""(grid)=>{const t=document.getElementById(grid);if(!t)return{f:0};
      const rows=[...t.querySelectorAll('tr')].map(r=>r.innerText.replace(/\s+/g,' ').trim()).filter(Boolean);
      return {f:1,n:rows.length,s:rows.slice(0,6)};}""",GRID)
    print(f"[{tag}] rows={info.get('n')} sample={info.get('s')}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Production Sub Unit");pg.wait_for_timeout(1200)
    try:
        ec.insertObjectRecord(pg,GRID,FIELDS)
        print("insert OK (persisted+GO done)")
    except Exception as e:
        print("insert ERR:",repr(e)[:120])
    pg.wait_for_timeout(1500); dump(pg,"after insert+GO, navdate=today")
    # set nav date to 2005 and GO
    sel="#nav\:form\:G\:0\:R\:1\:C\:0\:da_input"
    if pg.locator(sel).count():
        pg.fill(sel,"01-Jan-2005"); pg.keyboard.press("Tab"); ec.click_go(pg); pg.wait_for_timeout(1500)
        dump(pg,"navdate=2005")
    b.close()
