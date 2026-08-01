#!/usr/bin/env python3
"""READ-ONLY: click 'New Object' on Contract Capacity and dump the resulting form's mandatory fields.
Nothing saved."""
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
    ec.open_object_screen(pg, "Contract Capacity")
    pg.wait_for_timeout(2000)
    ec.select_dropdown(pg, "nav:form:G:0:R:1:C:1:dd_input", "__FIRST__")
    ec.click_go(pg); ec.wait_ajax(pg); pg.wait_for_timeout(2000)
    ec._open_new_object(pg)
    pg.wait_for_timeout(1500)
    print(a("objectForm present: %d" % pg.locator('[id*="objectForm"]').count()))
    fields = pg.evaluate("""() => [...document.querySelectorAll('[id*="objectForm"][id$="_input"],'+
        '[id*="objectForm"][id$=":in"],[id*="objectForm"][id$="_in"]')]
        .map(e => { const y = getComputedStyle(e).backgroundColor === 'rgb(252, 249, 192)';
            const m = e.id.match(/^(.*:R:[0-9]+):C:[0-9]+:/); let lab='';
            if (m) { const lc = document.getElementById(m[1]+':C:0:la'); if (lc) lab=(lc.innerText||'').trim(); }
            return {id: e.id, mandatory: y, label: lab}; })""")
    for f in fields:
        print(a("   mand=%-5s %-56s %s" % (f["mandatory"], f["id"], f["label"])))
    br.close()
    print(a("NOTHING SAVED (read-only)"))
