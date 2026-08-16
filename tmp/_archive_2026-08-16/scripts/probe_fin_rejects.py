"""Diagnose the Financial Objects silent rejects + find leftovers.

A) For each suspect screen: replicate the suite's exact insert (code/name/date +
   known extras from the recon), Save, capture the EC banner text. Abandoned if
   rejected; if it unexpectedly SAVES, the object is immediately End=Start deleted.
B) DB sweep: list AUTOTEST_% leftovers in all 14 views (class-1 GO-timeout suites
   may have saved their object before failing).
"""
import json
import re
import time
from pathlib import Path

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
RECON = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/financial_objects_recon.json")
records = {r["screen"]: r for r in json.loads(RECON.read_text(encoding="utf-8"))}

SUSPECTS = ["Bank Account", "Cost Object Mapping", "DOA Credit Limit",
            "Product Description", "Sales Order", "VAT Code"]
EXTRA_VALUES = {"GL Account": "999999", "Sort Code": "000000",
                "Credit Limit": "1000", "VAT Code": "AT9", "Rate (Decimal)": "0.1"}

print("=== B) leftover sweep ===")
conn = oracledb.connect(user="ECKERNEL_EC", password="energy", dsn="localhost:1521/ORCL")
cur = conn.cursor()
leftovers = {}
for r in records.values():
    v = r.get("dbView")
    if not v:
        continue
    try:
        cur.execute("SELECT column_name FROM all_tab_columns WHERE table_name=:v "
                    "AND data_type LIKE '%CHAR%' AND column_id<=6 ORDER BY column_id", v=v)
        cols = [c[0] for c in cur.fetchall()]
        for col in cols:
            cur.execute(f"SELECT {col} FROM {v} WHERE {col} LIKE 'AUTOTEST%'")
            found = [x[0] for x in cur.fetchall()]
            if found:
                leftovers.setdefault(r["screen"], set()).update(found)
    except Exception:
        pass
for k, v in leftovers.items():
    print(f"  {k}: {sorted(v)}")
if not leftovers:
    print("  none")
cur.close()
conn.close()


def pick_rows(plan):
    vis = [f for f in plan if f.get("visible")]
    texts = [f for f in vis if f.get("kind") == "text"]
    code = next(f for f in texts if f.get("mandatory") and "code" in (f.get("label") or "").lower())
    name = next(f for f in texts if f.get("mandatory") and (f.get("label") or "").strip().lower()
                in ("name", code["label"].lower().replace("code", "name").strip()))
    date = next(f for f in vis if f.get("kind") == "date")
    extras = [f for f in vis if f.get("mandatory") and f["r"] not in (code["r"], name["r"])
              and f.get("kind") in ("text", "checkbox")]
    return code, name, date, extras


MSG_JS = r"""() => {
    const out = [];
    document.querySelectorAll('#ECNotificationArea, #ECClientNotificationArea, .ui-messages, .ui-message, .ui-growl-message').forEach(e => {
        const t = (e.textContent || '').trim();
        if (t) out.push(t.replace(/EC.jsMessage.clear\(\);?/g, '').trim().substring(0, 250));
    });
    return out.filter(Boolean).slice(0, 5);
}"""

print("\n=== A) banner probes ===")
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
    ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_timeout(1500)

    for label in SUSPECTS:
        rec = records[label]
        try:
            page.goto(rec["url"], wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=20000)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            page.hover("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]")
            item = page.locator("xpath=//li[contains(@class,'ui-menu-parent')]"
                                "[.//span[contains(@class,'ui-icon-insert')]]//ul//a[normalize-space(.)='New Object']")
            item.wait_for(state="visible", timeout=8000)
            item.click()
            page.wait_for_timeout(2000)
            code_f, name_f, date_f, extras = pick_rows(rec["insertPlan"])
            code = f"AUTOTEST_PROBE_{time.strftime('%H%M%S')}"
            for fid, val in [(code_f["id"], code), (name_f["id"], "Probe " + code)]:
                page.fill(f"[id='{fid}']", val)
                page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));e.dispatchEvent(new Event('blur',{bubbles:true}));}}", fid)
                page.wait_for_timeout(300)
            page.fill(f"[id='{date_f['id']}']", "2000-01-01")
            page.keyboard.press("Tab")
            page.wait_for_timeout(700)
            for f in extras:
                if f["kind"] == "checkbox":
                    page.check(f"[id='{f['id']}']")
                else:
                    page.fill(f"[id='{f['id']}']", EXTRA_VALUES.get(f.get("label"), "AUTOTEST"))
                    page.evaluate("(id)=>{const e=document.getElementById(id); if(e){e.dispatchEvent(new Event('change',{bubbles:true}));}}", f["id"])
                page.wait_for_timeout(300)
            page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(1500)
            msgs = page.evaluate(MSG_JS)
            print(f"  {label:22s}: {msgs if msgs else '(no banner captured)'}")
            shot = rf"c:/Projects/ChoongYin_OS/tmp/screen_scan/shots/finprobe_{re.sub(r'[^A-Za-z0-9]+','_',label)}.png"
            page.screenshot(path=shot)
        except Exception as e:
            print(f"  {label:22s}: PROBE ERR {str(e)[:120]}")
    ctx.close()
    b.close()
print("probe done")
