"""READ-ONLY deep dive of the 4 phase-B screens (Area, Sub Area, Production Sub
Unit, Object List Setup): navigator dropdown options, grid behaviour after
select + GO, full insert-form field plan, screenshots. NOTHING is saved.
Output: tmp/screen_scan/phase_b_recon.json + shots/phaseb_*.png"""
import os
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCAN = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
OUT = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/phase_b_recon.json")
SHOTS = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots")
TARGETS = ["Area", "Sub Area", "Production Sub Unit", "Object List Setup"]

scan = json.loads(SCAN.read_text(encoding="utf-8"))
URLMAP = {r["screen"]: r["url"] for r in scan.values()
          if r.get("section") == "Basic Objects" and r.get("url")}

PLAN_JS = r"""(formName) => {
    const rows = {};
    document.querySelectorAll("[id^='tab:tabPanel:" + formName + ":form:G:']").forEach(el => {
        const m = el.id.match(/G:(\d+):R:(\d+):C:(\d+):(la|in|da_input|dd_button|cb)$/);
        if (!m) return;
        const key = `${m[1]}:${m[2]}`;
        rows[key] = rows[key] || {g: +m[1], r: +m[2]};
        const row = rows[key];
        if (m[4] === 'la') row.label = (el.textContent || '').trim();
        else {
            const mand = ((el.className || '') + (el.title || '')).includes('mandatory:true');
            row.kind = m[4] === 'in' ? 'text' : m[4] === 'da_input' ? 'date'
                     : m[4] === 'dd_button' ? 'dropdown' : 'checkbox';
            row.mandatory = row.mandatory || mand;
            row.id = el.id;
            row.visible = el.offsetParent !== null;
        }
    });
    return Object.values(rows).sort((a, b) => a.g - b.g || a.r - b.r);
}"""

DD_JS = r"""() => {
    const out = [];
    document.querySelectorAll("button[id$=':dd_button']").forEach(e => {
        if (e.offsetParent !== null && !e.id.includes('statusarea')
            && !e.id.startsWith('tab:tabPanel')) {
            // navigator-region dropdowns only
            const lab = e.closest('tr, div');
            out.push({id: e.id.replace(/_button$/, ''),
                      near: lab ? (lab.textContent || '').trim().substring(0, 50) : ''});
        }
    });
    return out;
}"""

GRID_JS = r"""() => {
    const t = document.querySelector("tbody[id$=':form:T_data']");
    if (!t) return {gridId: null, firstCodes: []};
    const codes = [];
    t.querySelectorAll('tr').forEach(tr => {
        const td = tr.querySelector('td');
        if (td) { const v = (td.textContent || '').trim(); if (v && v !== 'No records found') codes.push(v); }
    });
    return {gridId: t.id, firstCodes: codes.slice(0, 5)};
}"""

TOOLBAR_JS = r"""() => {
    const out = [];
    document.querySelectorAll("li.ui-menu-parent").forEach(li => {
        const icon = li.querySelector('span[class*="ui-icon"]');
        const items = [];
        li.querySelectorAll('ul li a').forEach(a => items.push((a.textContent || '').trim()));
        out.push({icon: icon ? icon.className.replace(/ui-icon|ui-menuitem-icon|\s+/g, ' ').trim() : '',
                  items: items.slice(0, 8)});
    });
    return out;
}"""


def dd_options(page, dd_prefix):
    try:
        page.click(f"[id='{dd_prefix}_button']")
        page.wait_for_selector(f"[id='{dd_prefix}_panel'] li", state="visible", timeout=8000)
        page.wait_for_timeout(600)
        opts = [o.strip() for o in page.locator(f"[id='{dd_prefix}_panel'] li").all_text_contents()]
        page.keyboard.press("Escape")
        page.wait_for_timeout(400)
        return opts[:25]
    except Exception as e:
        return [f"<failed: {str(e)[:60]}>"]


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

    results = []
    for name in TARGETS:
        rec = {"screen": name, "url": URLMAP.get(name)}
        slug = re.sub(r"[^A-Za-z0-9]+", "_", name)
        try:
            page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            page.screenshot(path=str(SHOTS / f"phaseb_{slug}_1_landing.png"))
            rec["gridBefore"] = page.evaluate(GRID_JS)
            rec["toolbar"] = page.evaluate(TOOLBAR_JS)

            # navigator dropdowns + their options
            navdds = page.evaluate(DD_JS)
            rec["navDropdowns"] = []
            for dd in navdds:
                opts = dd_options(page, dd["id"])
                rec["navDropdowns"].append({**dd, "options": opts})

            # try: select first option of FIRST nav dd, then GO
            if navdds:
                first = navdds[0]["id"]
                try:
                    page.click(f"[id='{first}_button']")
                    page.wait_for_selector(f"[id='{first}_panel'] li", state="visible", timeout=8000)
                    page.locator(f"[id='{first}_panel'] li").nth(0).click()
                    page.wait_for_timeout(1200)
                    go = page.locator("[id='button:form:B']")
                    if go.count():
                        go.click()
                        try:
                            page.wait_for_load_state("networkidle", timeout=15000)
                        except Exception:
                            pass
                        page.wait_for_timeout(1500)
                    rec["gridAfterSelectGo"] = page.evaluate(GRID_JS)
                    page.screenshot(path=str(SHOTS / f"phaseb_{slug}_2_after_go.png"))
                except Exception as e:
                    rec["selectGoError"] = str(e)[:150]

            # insert form (abandoned)
            try:
                page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
                item = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a[normalize-space(.)='New Object']")
                item.wait_for(state="visible", timeout=6000)
                item.click()
                page.wait_for_timeout(2000)
                rec["insertPlan"] = page.evaluate(PLAN_JS, "objectForm")
                # options of mandatory insert dropdowns
                for f in rec["insertPlan"]:
                    if f.get("kind") == "dropdown" and f.get("visible") and f.get("mandatory"):
                        f["options"] = dd_options(page, f["id"].replace("_button", ""))
                page.screenshot(path=str(SHOTS / f"phaseb_{slug}_3_insert_form.png"))
            except Exception as e:
                rec["insertFormError"] = str(e)[:150]
        except Exception as e:
            rec["error"] = str(e)[:200]
        results.append(rec)
        nd = rec.get("navDropdowns") or []
        print(f"== {name}: navDDs={len(nd)} gridBefore={rec.get('gridBefore', {}).get('gridId')} "
              f"after={rec.get('gridAfterSelectGo', {}).get('firstCodes', '-')} ins={len(rec.get('insertPlan') or [])}")
        for d in nd:
            print(f"   nav dd {d['id']}: {d['options'][:8]}")
    ctx.close()
    b.close()

OUT.write_text(json.dumps(results, indent=1), encoding="utf-8")
print(f"-> {OUT}")
