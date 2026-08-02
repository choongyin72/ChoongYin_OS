"""READ-ONLY: for each phase-A screen, open the New Object form (and the update
form via row select where rows exist) and capture row LABELS (:C:0:la),
mandatory flags ({mandatory:true} marker) and maxlength. Merge into
basic_objects_recon.json as insertPlan/updatePlan."""
import os
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/basic_objects_recon.json")
TARGETS = ["Production Unit", "Business Unit", "Country", "State", "County",
           "Region", "Object List", "Functional Area", "Regulatory Permits"]

PLAN_JS = r"""(formName) => {
    const rows = {};
    document.querySelectorAll("[id^='tab:tabPanel:" + formName + ":form:G:']").forEach(el => {
        const m = el.id.match(/G:(\d+):R:(\d+):C:(\d+):(la|in|da_input|dd_button|dd_input|cb)$/);
        if (!m) return;
        const key = `${m[1]}:${m[2]}`;
        rows[key] = rows[key] || {g: +m[1], r: +m[2]};
        const row = rows[key];
        if (m[4] === 'la') row.label = (el.textContent || '').trim();
        else {
            const mand = ((el.className || '') + (el.title || '')).includes('mandatory:true');
            if (m[4] === 'in') { row.kind = 'text'; row.id = el.id; row.mandatory = mand;
                                 row.maxlength = el.maxLength > 0 ? el.maxLength : null;
                                 row.visible = el.offsetParent !== null; }
            else if (m[4] === 'da_input') { row.kind = 'date'; row.id = el.id;
                                            row.visible = el.offsetParent !== null; }
            else if (m[4] === 'dd_button') { row.kind = 'dropdown'; row.ddPrefix = el.id.replace(/_button$/, '');
                                             row.visible = el.offsetParent !== null; }
            else if (m[4] === 'dd_input') { row.mandatory = row.mandatory || mand; }
            else if (m[4] === 'cb') { row.kind = 'checkbox'; row.id = el.id;
                                      row.checked = el.checked; row.visible = el.offsetParent !== null; }
        }
    });
    return Object.values(rows).sort((a, b) => a.g - b.g || a.r - b.r);
}"""

records = json.loads(RECON.read_text(encoding="utf-8"))
by_name = {r["screen"]: r for r in records}

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", os.environ.get("EC_USER", "sysadmin"))
    page.fill("#password", os.environ.get("EC_PASS", "sysadmin"))
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)

    for name in TARGETS:
        rec = by_name[name]
        page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
        try:
            page.wait_for_load_state("networkidle", timeout=20000)
        except Exception:
            pass
        page.wait_for_timeout(1500)

        if rec.get("firstCodes"):
            try:
                page.click(f"tbody[id='{rec['gridId']}'] tr >> nth=0")
                page.wait_for_timeout(1800)
                rec["updatePlan"] = page.evaluate(PLAN_JS, "updateAttributes")
                rec["datePlan"] = page.evaluate(PLAN_JS, "objectdates")
            except Exception as e:
                rec["updatePlanError"] = str(e)[:120]
        try:
            page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
            item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']")
            item.wait_for(state="visible", timeout=8000)
            item.click()
            page.wait_for_timeout(2000)
            rec["insertPlan"] = page.evaluate(PLAN_JS, "objectForm")
        except Exception as e:
            rec["insertPlanError"] = str(e)[:120]
        n_ins = len(rec.get("insertPlan") or [])
        n_upd = len(rec.get("updatePlan") or [])
        print(f"{name:22s} insertPlan={n_ins} updatePlan={n_upd}")
    ctx.close()
    b.close()

RECON.write_text(json.dumps(records, indent=1), encoding="utf-8")
print("merged ->", RECON)
