# Deep-dive: HOW EC constructs the "Pick from EC Object" popup (pin/pinB -> dialog -> iframe -> grid -> callback).
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
    ec.open_object_screen(pg,"Meter"); pg.wait_for_timeout(1200)
    ec.select_dropdown(pg,"nav:form:G:0:R:1:C:1:dd","ECP Norway"); pg.wait_for_timeout(600)
    ec.click_go(pg); pg.wait_for_timeout(1500)
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    pin="tab:tabPanel:objectForm:form:G:0:R:5:C:1:pin"
    # (1) the pin input + its launch button - how the widget is wired
    wiring=pg.evaluate("""(pin)=>{
      const inp=document.getElementById(pin), btn=document.getElementById(pin+'B');
      return {pin_readonly: inp?inp.readOnly:null, pin_class:(inp&&inp.className||'').slice(0,50),
              btn_tag:btn?btn.tagName:null, btn_onclick:(btn&&btn.getAttribute('onclick')||'').slice(0,120),
              btn_class:(btn&&btn.className||'').slice(0,50)};}""", pin)
    print("(1) WIDGET WIRING:", wiring)
    # (2) open it, inspect the dialog wrapper + iframe URL
    pg.evaluate("(id)=>document.getElementById(id+'B').click()", pin); pg.wait_for_timeout(4000)
    dlg=pg.evaluate("""()=>{
      const d=document.getElementById('popupForm:popup');
      const ifr=document.getElementById('popupIFrame');
      return {dialog_class:(d&&d.className||''), title:(document.getElementById('popupForm:headerLabel')||{}).innerText||'',
              iframe_src:(ifr&&ifr.src||'')};}""")
    print("(2) DIALOG+IFRAME:", dlg)
    # (3) inside the iframe: the grid + a sample row's construction (how the value is carried)
    fr=None
    for f in pg.frames:
        if f.query_selector('[id="PopupList:form:T_data"]'): fr=f; break
    if fr:
        grid=fr.evaluate("""()=>{
          const tb=document.getElementById('PopupList:form:T_data'); const tr=tb.querySelector('tr');
          const cols=[...document.querySelectorAll('th')].map(t=>(t.innerText||'').trim()).filter(Boolean).slice(0,6);
          const firstRowHtml=tr?tr.outerHTML.slice(0,240):''; 
          const rowCount=tb.querySelectorAll('tr').length;
          return {cols, rowCount, firstRowHtml};}""")
        print("(3) IFRAME GRID cols:", grid["cols"])
        print("    rowCount:", grid["rowCount"])
        print("    first row HTML:", grid["firstRowHtml"])
    else:
        print("(3) iframe grid not found")
    b.close()
