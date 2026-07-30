"""READ-ONLY: inspect the New-Object form DOM nesting (label cell C:0 vs input cell C:1)
to design a LABEL-DRIVEN xpath for the RF resolver (no hardcoded row index). Bank screen."""
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
    ec.login(pg, URL, "sysadmin", "sysadmin"); ec.open_object_screen(pg, "Bank"); ec.click_go(pg)
    ec._open_new_object(pg)
    # for the Code input (R0 C1 in), dump the ancestor chain ids/tags + the label cell (R0 C0) chain
    info = pg.evaluate("""()=>{
      const inp=document.getElementById('tab:tabPanel:objectForm:form:G:0:R:0:C:1:in');
      const lab=document.getElementById('tab:tabPanel:objectForm:form:G:0:R:0:C:0')||document.querySelector('[id^="tab:tabPanel:objectForm:form:G:0:R:0:C:0"]');
      function chain(el){const out=[];let c=el;for(let i=0;i<6&&c;i++){out.push(c.tagName.toLowerCase()+(c.id?('#'+c.id.slice(-24)):'')+'.'+((c.className||'').toString().split(' ')[0]));c=c.parentElement;}return out;}
      return {inp_id:inp?inp.id:null, inp_chain:inp?chain(inp):[], lab_id:lab?lab.id:null, lab_text:lab?(lab.innerText||'').trim():null, lab_chain:lab?chain(lab):[],
              // is label an ancestor-sibling of input? find common row container
              inp_html: inp&&inp.closest('tr')?inp.closest('tr').outerHTML.slice(0,400):(inp&&inp.parentElement?inp.parentElement.outerHTML.slice(0,400):'')};}""")
    import json
    print(json.dumps(info, indent=1)[:2000])
    br.close()
