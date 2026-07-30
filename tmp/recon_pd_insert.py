import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Production Day Table"); pg.wait_for_timeout(1500)
    ins=pg.evaluate("""()=>{
      const par=[...document.querySelectorAll("li.ui-menu-parent, li[class*='ui-menu-parent']")]
        .find(li=>li.querySelector("[class*='ui-icon-insert']"));
      let items=[];
      if(par){items=[...par.querySelectorAll("ul[class*='ui-menu-child'] a")].map(a=>(a.innerText||'').trim()).filter(Boolean);}
      const t=document.getElementById('production_day:form:T_data');
      const tbl=t?t.closest('table'):null;
      const cols=tbl?[...tbl.querySelectorAll('th')].map(x=>(x.innerText||'').trim()).filter(Boolean).slice(0,8):[];
      const anyNewObj=[...document.querySelectorAll('a')].some(a=>/New Object/i.test(a.innerText||''));
      const editableCells=t?t.querySelectorAll('input,select').length:0;
      return {insert_submenu_items:items, gridCols:cols, hasNewObjectLink:anyNewObj, gridEditableInputs:editableCells};}""")
    print("insert submenu items:", ins["insert_submenu_items"])
    print("has 'New Object' link:", ins["hasNewObjectLink"])
    print("grid columns:", ins["gridCols"])
    print("grid editable inputs (inline-edit hint):", ins["gridEditableInputs"])
    b.close()
