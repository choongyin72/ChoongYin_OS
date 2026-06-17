"""RECON v2 (sandbox): load the Stream Gas Component Analysis grid for the LOCKED target
(P1 S038_AGA3_1985_AGA8_Y_1 @ 2011-11-01, SPOT, status P) and map the editable MOL_PCT cell.
Improvement over recon_comp_grid.py: (1) iterate the G:6 'Analysis Status' options until the grid
loads non-empty; (2) dump ALL grid inputs (any id pattern) with row-label + value, not just
':C{n}_in'. Read-only on EC (no Save). Outputs to tmp/recon_comp/grid2.*"""
import json
import os
import oracledb
from playwright.sync_api import sync_playwright

DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")
SCREEN = "Stream Gas Component Analysis"
CODE = "P1 S038_AGA3_1985_AGA8_Y_1"
DATE = "2011-11-01"
SAMPLING = "SPOT"
OUT = r"c:\Projects\ChoongYin_OS\tmp\recon_comp"
os.makedirs(OUT, exist_ok=True)


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


# target components (for cross-checking the grid)
conn = oracledb.connect(user="ECKERNEL_EC", password=os.environ.get("EC_DB_PWD", "energy"),
                        dsn=DB_DSN, tcp_connect_timeout=15)
cur = conn.cursor()
cur.execute("""SELECT COMPONENT_NO, MOL_PCT FROM ECKERNEL_EC.DV_STRM_COMP_ANALYSIS
               WHERE OBJECT_CODE=:c AND TRUNC(DAYTIME)=TO_DATE(:d,'YYYY-MM-DD') ORDER BY COMPONENT_NO""",
            [CODE, DATE])
comps = cur.fetchall()
print("target components:", comps)
cur.close()
conn.close()


def open_screen(page, name):
    box = page.locator(css("menu:searchForm:searchTxt"))
    if box.count() == 0 or not box.first.is_visible():
        mm = page.locator(css("screenToolbar:form:minmaxMenu"))
        if mm.count() and mm.first.is_visible():
            mm.first.click(); page.wait_for_timeout(800)
    box.click(); box.fill(""); box.type(name, delay=45); ajax(page, 8000)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link')"
                 f" and normalize-space(text())='{name}']").first.click()
    ajax(page)
    mm = page.locator(css("screenToolbar:form:minmaxMenu"))
    if mm.count() and mm.first.is_visible():
        mm.first.click(); ajax(page)


def opts(page, group):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    try:
        page.click(css(pre + "_button")); page.wait_for_timeout(700)
        o = page.evaluate(f"""() => [...document.querySelectorAll("[id='{pre}_panel'] tr[data-item-label]")]
            .map(t=>t.getAttribute('data-item-label')).filter(x=>x && x.trim())""")
        page.keyboard.press("Escape"); page.wait_for_timeout(250)
        return o
    except Exception:
        return []


def pick(page, group, value):
    pre = f"nav:form:{group}:R:1:C:0:dd"
    item = f"xpath=//*[@id='{pre}_panel']//tr[normalize-space(@data-item-label)='{value}']"
    page.click(css(pre + "_button"))
    try:
        page.locator(item).first.wait_for(state="visible", timeout=5000)
    except Exception:
        page.keyboard.press("Escape"); page.wait_for_timeout(1000); page.click(css(pre + "_button"))
        page.locator(item).first.wait_for(state="visible", timeout=6000)
    page.locator(item).first.click(); ajax(page, 10000)


def click_go(page):
    for go in ("go_button:form:B", "navButton:form:B", "button:form:B"):
        loc = page.locator(css(go))
        if loc.count() and loc.first.is_visible():
            loc.first.click(); ajax(page, 18000); return go
    return None


def dump_grid(page):
    """Return all inputs that sit inside a table row, with the row's first-cell text (component label)."""
    return page.evaluate("""() => {
        const rows=[];
        document.querySelectorAll("table tr").forEach(tr=>{
          const ins=[...tr.querySelectorAll("input,select,textarea")].filter(i=>i.type!=='hidden');
          if(!ins.length) return;
          const cells=[...tr.querySelectorAll("td,th")].map(c=>(c.innerText||'').replace(/\\s+/g,' ').trim());
          const label=cells.find(t=>t)||'';
          rows.push({label, inputs: ins.map(i=>({id:i.id, type:i.type, val:i.value, ro:i.readOnly, dis:i.disabled}))});
        });
        return rows;
    }""")


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", EC_USER); page.fill("#password", EC_PASS); page.click("#kc-login")
    page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000); ajax(page)

    # Stream Finder -> PU/Area/Facility
    open_screen(page, "Stream Finder")
    inp = page.locator(css("nav:form:G:0:R:1:C:1:in"))
    inp.click(); inp.fill(CODE); page.keyboard.press("Tab"); page.wait_for_timeout(400)
    page.click(css("navButton:form:B")); ajax(page, 15000)
    scope = page.evaluate("""() => {const want=["Production Unit","Area","Facility Class 1"]; const res={};
        document.querySelectorAll("tr").forEach(tr=>{const c=[...tr.querySelectorAll("td")];
          if(c.length>=2){const gv=e=>(e.querySelector('input')?.value||e.innerText||'').trim();
            const k=gv(c[0]),v=gv(c[1]); if(want.includes(k)&&v)res[k]=v;}}); return res;}""")
    print("Stream Finder scope:", scope)
    if not scope.get("Production Unit"):
        scope = {"Production Unit": "P1 Production Unit", "Area": "P1 Area",
                 "Facility Class 1": "P1 Facility 1"}
        print("  -> Stream Finder empty; using known P1 scope fallback:", scope)

    open_screen(page, SCREEN)
    for fid in page.evaluate("""() => [...document.querySelectorAll("[id^='nav:form:']")]
            .map(e=>e.id).filter(id=>/:da_input$/.test(id))"""):
        el = page.locator(css(fid)); el.click(); el.fill(DATE); page.keyboard.press("Tab"); page.wait_for_timeout(300)
    pick(page, "G:2", scope["Production Unit"])
    if scope.get("Area"):
        pick(page, "G:3", scope["Area"])
    if scope.get("Facility Class 1"):
        pick(page, "G:4", scope["Facility Class 1"])
    print("G:5 Stream options:", opts(page, "G:5")[:12])
    pick(page, "G:5", CODE)
    status_opts = opts(page, "G:6")
    print("G:6 Analysis Status options:", status_opts)
    sampling_opts = opts(page, "G:7")
    print("G:7 Sampling Method options:", sampling_opts)

    result = {"scope": scope, "status_opts": status_opts, "sampling_opts": sampling_opts, "tried": []}
    loaded = None
    # set sampling once (SPOT)
    if SAMPLING in sampling_opts:
        pick(page, "G:7", SAMPLING)
    elif sampling_opts:
        pick(page, "G:7", sampling_opts[0])
    for st in status_opts:
        try:
            pick(page, "G:6", st)
        except Exception as e:
            result["tried"].append({"status": st, "err": str(e)[:60]}); continue
        go = click_go(page)
        rows = dump_grid(page)
        ncell = sum(len(r["inputs"]) for r in rows)
        result["tried"].append({"status": st, "go": go, "rows_with_inputs": len(rows), "cells": ncell})
        print(f"  status='{st}' GO={go} rows_with_inputs={len(rows)} cells={ncell}")
        if ncell > 0:
            loaded = {"status": st, "rows": rows}
            page.screenshot(path=os.path.join(OUT, "grid2.png"), full_page=True)
            break

    result["loaded"] = loaded
    with open(os.path.join(OUT, "grid2.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    if loaded:
        print(f"\nGRID LOADED with status='{loaded['status']}' — rows:")
        for r in loaded["rows"][:20]:
            print("  ", r["label"][:24], "->", [(i["id"], i["val"], "ro" if i["ro"] else "") for i in r["inputs"]])
    else:
        print("\nGRID NEVER LOADED — see grid2.json tried[]")
    b.close()
print("DONE")
