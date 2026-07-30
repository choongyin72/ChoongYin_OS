"""Probe Conversion Group's real grid id + GO presence (custom-URL OV vs manage-object), find where the
AUTOTEST row renders, then self-clean it (End=Start via the view; local sandbox). Read-mostly + 1 cleanup."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
import oracledb
EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation"); sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = b.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Conversion Group"); pg.wait_for_timeout(1500)
    grids = pg.evaluate("""()=>{const out=[];document.querySelectorAll('tbody[id$=\":T_data\"],tbody[id$=\"_data\"]').forEach(t=>{
        out.push({id:t.id, rows:t.querySelectorAll('tr').length});});
        return {grids:out, go:!!document.getElementById('button:form:B'),
                refresh:!!document.querySelector('a[title^=\"Refresh\"]')};}""")
    print("GO button:", grids["go"], "| Refresh toolbar:", grids["refresh"])
    print("grids (tbody ...:_data):")
    for g in grids["grids"]:
        print("   %-45s rows=%d" % (g["id"], g["rows"]))
    b.close()
# clean residual (authorized local-sandbox self-clean)
c = oracledb.connect(user='ECKERNEL_EC', password='energy', dsn='localhost:1521/ORCL'); cur = c.cursor()
try:
    cur.execute("update OV_CONVERSION_GROUP set OBJECT_END_DATE=OBJECT_START_DATE where CODE='AUTOTEST_CVG_001'")
    print("clean end=start rowcount:", cur.rowcount); c.commit()
except Exception as e:
    c.rollback(); print("clean ERR:", str(e)[:140])
cur.execute("select count(*) from ov_conversion_group where code like 'AUTOTEST%'")
print("residual now:", cur.fetchone()[0]); c.close()
