import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC=Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation");sys.path.insert(0,str(EC/"py"))
import ec_object_iud as ec
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
GRID="manageObject:form:T_data"
with sync_playwright() as p:
    b=p.chromium.launch(headless=True,args=["--ignore-certificate-errors"])
    pg=b.new_context(ignore_https_errors=True,viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg,URL,"sysadmin","sysadmin")
    ec.open_object_screen(pg,"Production Sub Unit");pg.wait_for_timeout(1200)
    # nav Date value BEFORE go
    d1=pg.eval_on_selector("#nav\:form\:G\:0\:R\:1\:C\:0\:da_input","e=>e.value") if pg.locator("#nav\:form\:G\:0\:R\:1\:C\:0\:da_input").count() else "(no date field)"
    ec.click_go(pg);pg.wait_for_timeout(1500)
    # dump grid rows (first column texts) + row count + paginator
    info=pg.evaluate("""(grid)=>{
      const t=document.getElementById(grid);
      if(!t) return {found:false};
      const rows=[...t.querySelectorAll('tr')].map(r=>r.innerText.replace(/\s+/g,' ').trim()).filter(Boolean);
      const pager=document.querySelector("[id='"+grid.replace(':T_data','')+"_paginator']");
      return {found:true, rowcount:rows.length, sample:rows.slice(0,8), pager:pager?pager.innerText.replace(/\s+/g,' ').trim():'(none)'};}""",GRID)
    print("nav Date value:",repr(d1))
    print("grid found:",info.get("found"))
    print("grid rowcount:",info.get("rowcount"))
    print("pager:",info.get("pager"))
    print("sample rows:")
    for r in info.get("sample",[]): print("   ",r[:90])
    b.close()
