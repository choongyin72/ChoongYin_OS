#!/usr/bin/env python3
"""READ-ONLY: apply the PROVEN scope (P3 Production Unit -> P3 Area -> Oper Route 1) to Collection Point's
3-level nav cascade, then dump the New-Object form's mandatory fields. Nothing saved."""
import os, sys
from pathlib import Path
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright
def a(s): return str(s).encode("ascii","replace").decode("ascii")

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width":1920,"height":1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/",
             os.environ.get("EC_USER","sysadmin"), os.environ.get("EC_PASS","sysadmin"))
    ec.open_object_screen(pg, "Collection Point")
    pg.wait_for_timeout(2000)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "P3 Production Unit")
    pg.wait_for_timeout(900)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:2:dd_input", "P3 Area")
    pg.wait_for_timeout(900)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:3:dd_input", "Oper Route 1")
    pg.wait_for_timeout(900)
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(2500)
    grid = pg.evaluate("""() => { const t=[...document.querySelectorAll("[id$=':T_data']")]
        .filter(e=>e.offsetParent||e.querySelector('tr')); return t.length? [t[0].id, t[0].querySelectorAll('tr').length] : null; }""")
    print(a("grid after GO: %s" % (grid,)))
    ec._open_new_object(pg); pg.wait_for_timeout(1500)
    fields = pg.evaluate("""() => [...document.querySelectorAll('[id*="objectForm"][id$="_input"],'+
        '[id*="objectForm"][id$=":in"],[id*="objectForm"][id$="_in"]')]
        .map(e => { const y = getComputedStyle(e).backgroundColor === 'rgb(252, 249, 192)';
            const m = e.id.match(/^(.*:R:\d+):C:\d+:/); let lab='';
            if (m) { const lc = document.getElementById(m[1]+':C:0:la'); if (lc) lab=(lc.innerText||'').trim(); }
            return {id: e.id, mandatory: y, label: lab}; })""")
    print(a("ALL objectForm fields:"))
    for f in fields:
        print(a("   mand=%-5s %-56s %s" % (f["mandatory"], f["id"], f["label"])))
    br.close()
    print(a("NOTHING SAVED (read-only)"))
