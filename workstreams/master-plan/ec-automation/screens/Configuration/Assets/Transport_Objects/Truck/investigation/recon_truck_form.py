#!/usr/bin/env python3
"""Read-only: Truck New-Object form - dump ALL fields with labels + EC's full required-fields message."""
import sys
from pathlib import Path

EC = Path(r"C:\Projects\ChoongYin_OS\workstreams\master-plan\ec-automation")
sys.path.insert(0, str(EC / "py"))
import ec_object_iud as ec
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    br = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    pg = br.new_context(ignore_https_errors=True, viewport={"width": 1920, "height": 1080}).new_page()
    ec.login(pg, "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/", "sysadmin", "sysadmin")
    ec.open_object_screen(pg, "Truck")
    ec.click_go(pg)
    ec._open_new_object(pg)
    pg.wait_for_timeout(1500)

    print("--- ALL objectForm fields (label | id | yellow?) ---")
    data = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll("span.ECCell[id*=':objectForm:form:']").forEach(sp => {
            const label = (sp.textContent || '').trim();
            const cell = sp.closest("div[class*='tableCell']");
            const next = cell ? cell.nextElementSibling : null;
            const inp = next ? next.querySelector("input,textarea,select") : null;
            if (label && inp) {
                const bg = getComputedStyle(inp).backgroundColor;
                out.push([label, inp.id, bg]);
            }
        });
        return out; }""")
    for label, iid, bg in data:
        mark = "YELLOW" if "255, 255" in bg and "204" in bg or bg == "rgb(255, 255, 204)" else ""
        print(f"  {label[:38]:<40} {iid[-42:]:<44} {mark}")
    br.close()
