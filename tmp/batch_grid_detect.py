"""For the Group-A (no-navigator) screens: detect grid id + GO/Refresh flavour in one login, so each can
be built with the right grid_id. Read-only. Emits tmp/group_a_flavour.json."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec

cfg = json.load(open(r"C:\Projects\ChoongYin_OS\tmp\ov_gm_55_nav_config.json", encoding="utf-8"))
group_a = [o for o in cfg if not o["nav"] and o["bf"] != "CO.1049"]  # no-navigator, minus Conversion Group (done)
URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
out = []
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, URL, "sysadmin", "sysadmin")
    for o in group_a:
        r = {"bf": o["bf"], "screen": o["screen"], "view": o["view"], "folder": o["folder"]}
        try:
            pg.goto(URL, wait_until="networkidle", timeout=60000); pg.wait_for_timeout(600)
            ec.open_object_screen(pg, o["screen"]); pg.wait_for_timeout(1200)
            info = pg.evaluate("""()=>{
              const mgr=document.getElementById('manage_object_nav_nav:form:T_data');
              const nav=document.getElementById('nav:form:T_data');
              return {mgr:!!mgr, nav:!!nav, go:!!document.getElementById('button:form:B')};}""")
            grid = "manage_object_nav_nav:form:T_data" if info["mgr"] else ("nav:form:T_data" if info["nav"] else "?")
            r["grid_id"] = grid; r["go"] = info["go"]
            r["flavour"] = "manage-object" if info["go"] else ("custom-URL" if grid == "nav:form:T_data" else "?")
        except Exception as e:
            r["error"] = repr(e)[:90]; r["flavour"] = "ERR"
        out.append(r)
        print("%-9s %-26s grid=%-38s go=%s -> %s" % (r["bf"], r["screen"][:26], r.get("grid_id", "?"), r.get("go", "?"), r.get("flavour", "?")))
    b.close()
Path(r"C:\Projects\ChoongYin_OS\tmp\group_a_flavour.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
mo = [x for x in out if x.get("flavour") == "manage-object"]; cu = [x for x in out if x.get("flavour") == "custom-URL"]
print("\nmanage-object: %d | custom-URL: %d | other: %d" % (len(mo), len(cu), len(out) - len(mo) - len(cu)))
