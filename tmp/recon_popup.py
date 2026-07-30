# READ-ONLY recon of a "Pick from EC Object" popup on the LOCAL sandbox. Opens the New-Object form,
# locates a popup-backed field, clicks its picker, dumps the dialog structure. No Save.
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
    ec.open_object_screen(pg,"Contract Area Setup"); pg.wait_for_timeout(1500)
    ec._open_new_object(pg); pg.wait_for_timeout(1200)
    # 1) locate the 'Contract Area Name' field cell + dump its surrounding controls (buttons/icons)
    info=pg.evaluate("""() => {
      const lbl=[...document.querySelectorAll("span.ECCell, span[class*='ECCell']")].find(s=>/Contract Area Name/i.test(s.textContent||''));
      if(!lbl) return {found:false, labels:[...document.querySelectorAll('span')].map(s=>s.textContent.trim()).filter(t=>/Contract/i.test(t)).slice(0,10)};
      const cell=lbl.closest("div[class*='tableCell']");
      const valCell=cell? cell.nextElementSibling : null;
      const controls=valCell? [...valCell.querySelectorAll('input,button,a,span[onclick],span[class*=icon]')].map(e=>({tag:e.tagName,id:e.id,cls:(e.className||'').slice(0,50),title:e.title||'',type:e.type||''})) : [];
      return {found:true, controls};
    }""")
    print("field controls:", info)
    # 2) click the picker (button/icon) next to the field, then dump any dialog that opens
    clicked=pg.evaluate("""() => {
      const lbl=[...document.querySelectorAll("span[class*='ECCell']")].find(s=>/Contract Area Name/i.test(s.textContent||''));
      const cell=lbl && lbl.closest("div[class*='tableCell']"); const valCell=cell&&cell.nextElementSibling;
      if(!valCell) return 'no valcell';
      const btn=valCell.querySelector("button, a[href='#'], span[class*='icon'], .ui-button, [id*='button']");
      if(btn){ btn.click(); return 'clicked:'+(btn.id||btn.className); }
      return 'no button found';
    }""")
    print("picker click:", clicked)
    pg.wait_for_timeout(1500)
    dlg=pg.evaluate("""() => {
      const dlgs=[...document.querySelectorAll("div[role='dialog'], .ui-dialog, [id*='dialog'], [id*='opup'], [id*='POPUP']")].filter(d=>d.offsetParent!==null);
      return dlgs.slice(0,3).map(d=>({id:d.id, cls:(d.className||'').slice(0,60),
        inputs:[...d.querySelectorAll('input')].map(i=>({id:i.id,ph:i.placeholder||'',type:i.type})).slice(0,6),
        gridId:(d.querySelector("[id$=':T_data'], table[id]")||{}).id||'',
        buttons:[...d.querySelectorAll('button, a.ui-button, [id*=utton]')].map(x=>({id:x.id,txt:(x.textContent||'').trim().slice(0,20)})).slice(0,8)}));
    }""")
    print("visible dialog(s):", dlg)
    b.close()
