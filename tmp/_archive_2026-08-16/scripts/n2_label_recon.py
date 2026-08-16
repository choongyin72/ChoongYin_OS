"""N2 label recon: dump EXACT G:2 network labels + the G:4 calc-job labels they expose,
for the positive (Testing allocation RUN_NO) and negative (P1 Dashboard) scopes. Read-only,
no RUN clicked. So the RF suite picks dropdown options by the real labels."""
import time, json
from playwright.sync_api import sync_playwright
URL="https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"; SCREEN="Daily Allocation"

def opts(fr, g):
    try:
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.9)
        labels = fr.evaluate(f"""()=>[...document.querySelectorAll('[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label]')].map(e=>(e.getAttribute('data-item-label')||'')).filter(t=>t.trim())""")
        # close panel
        fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=2000); time.sleep(0.3)
        return labels
    except Exception as e:
        return [f"ERR {e}"]

def pick(fr, g, contains):
    labels = opts(fr, g)
    target = next((x for x in labels if contains.lower() in x.lower()), None)
    if not target:
        return None, labels
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_button"]').click(timeout=4000); time.sleep(0.7)
    fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:dd_panel"] tr[data-item-label="{target}"]').first.click(timeout=4000)
    time.sleep(1.3)
    return target, labels

with sync_playwright() as p:
    b=p.chromium.launch(headless=True); page=b.new_context(ignore_https_errors=True,viewport={"width":1680,"height":1000}).new_page()
    page.goto(URL,wait_until="domcontentloaded",timeout=60000)
    page.fill('[id="username"]',"sysadmin"); page.fill('[id="password"]',"sysadmin"); page.click('[id="kc-login"]')
    page.wait_for_selector('[id="menu:searchForm:searchTxt"]',timeout=60000)
    sel='xpath=//*[contains(@class,"tv-link") and normalize-space(text())="Daily Allocation"]'; fr=None
    for _ in range(3):
        page.fill('[id="menu:searchForm:searchTxt"]',""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN,delay=40)
        try: page.wait_for_selector(sel,timeout=12000)
        except Exception: pass
        time.sleep(0.6)
        try: page.locator(sel).first.click()
        except Exception: continue
        page.wait_for_load_state("networkidle",timeout=30000)
        for _ in range(25):
            fr=next((f for f in page.frames if "edit_daily_alloc" in f.url),None)
            if fr: break
            time.sleep(1.0)
        if fr: break
    if not fr: print("NOT LOADED"); b.close(); raise SystemExit
    time.sleep(2.0)

    for scope_name, date, net_contains in [("POSITIVE","2003-01-01","Testing allocation RUN_NO"),
                                           ("NEGATIVE","2021-10-01","P1 Dashboard")]:
        print(f"\n===== {scope_name}: date={date} net~='{net_contains}' =====")
        for g in (0,1):
            di=fr.locator(f'[id="nav:form:G:{g}:R:1:C:0:da_input"]'); di.fill(date); di.press("Tab"); time.sleep(1.0)
        all_nets = opts(fr, 2)
        print("  G:2 network labels (sample):", json.dumps([x for x in all_nets if any(k in x for k in ('RUN_NO','Testing','P1','AS2'))][:10]))
        net, _ = pick(fr, 2, net_contains)
        print("  picked G:2 network =", repr(net))
        opts(fr, 3)  # touch G:3
        jobs = opts(fr, 4)
        print("  G:4 calc-job labels =", json.dumps(jobs))
    b.close()
print("\nDONE")
