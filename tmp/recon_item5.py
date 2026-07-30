# Classify Constant Standard + Stream Item: TABLE-style (inline) vs custom OV vs standard OV.
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
def classify(pg,scr):
    try:
        pg.goto(URL,wait_until="networkidle",timeout=45000); pg.wait_for_timeout(500)
        ec.open_object_screen(pg,scr); pg.wait_for_timeout(1500)
        info=pg.evaluate("""()=>{
          const par=[...document.querySelectorAll("li[class*='ui-menu-parent']")].find(li=>li.querySelector("[class*='ui-icon-insert']"));
          const items=par?[...par.querySelectorAll("ul[class*='ui-menu-child'] a")].map(a=>(a.innerText||'').trim()).filter(Boolean):[];
          const grids=[...document.querySelectorAll("[id$=':T_data']")].map(t=>t.id);
          const anyNewObj=[...document.querySelectorAll('a')].some(a=>/New Object/i.test(a.innerText||''));
          const delIcon=[...document.querySelectorAll("[class*='ui-icon-delete']")].length;
          return {insert_items:items, grids, hasNewObject:anyNewObj, delIcons:delIcon};}""")
        print(f"{scr}: insert_items={info['insert_items']} | grids={info['grids']} | NewObject={info['hasNewObject']} | delIcons={info['delIcons']}")
    except Exception as e:
        print(f"{scr}: {repr(e)[:90]}")
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    classify(pg,"Constant Standard")
    classify(pg,"Stream Item")
    b.close()
