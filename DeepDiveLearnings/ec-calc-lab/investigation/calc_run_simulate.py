from playwright.sync_api import sync_playwright
import re
def say(m): print(m, flush=True)
def cell(s): return '#'+s.replace(':',r'\:')
def wa(pg,t=20000): pg.wait_for_load_state('networkidle',timeout=t); pg.wait_for_timeout(1000)
def killpanels(pg):
    pg.evaluate("() => { var ps=document.querySelectorAll('.ui-autocomplete-panel, .ui-input-overlay'); for (var i=0;i<ps.length;i++){ ps[i].style.display='none'; } }")
SIM='dateStartJob:form:G:0:R:1:C:2:cb'
with sync_playwright() as p:
    b=p.chromium.connect_over_cdp("http://localhost:9222")
    pg=b.contexts[0].pages[0]
    killpanels(pg); pg.wait_for_timeout(400)
    pg.keyboard.press('Control+g'); say("GO via Ctrl+g"); wa(pg)
    killpanels(pg); pg.wait_for_timeout(300)
    pg.locator(cell(SIM)).check(force=True); pg.wait_for_timeout(600)
    ticked=pg.locator(cell(SIM)).is_checked(); say("Simulate ticked: "+str(ticked))
    if not ticked: say("GUARD: not ticked -> abort"); raise SystemExit
    pg.screenshot(path="C:/tmp/run_ready.png", full_page=True); say("SHOT run_ready")
    killpanels(pg)
    pg.get_by_role("button", name=re.compile("run calc", re.I)).first.click(force=True); pg.wait_for_timeout(2500)
    okb=pg.get_by_role("button", name=re.compile(r"^ok$", re.I))
    if okb.count()>0 and okb.first.is_visible(): okb.first.click(); say("Run confirmed (OK)"); wa(pg)
    pg.wait_for_timeout(8000)
    killpanels(pg); pg.keyboard.press('Control+g'); wa(pg); pg.wait_for_timeout(2000)
    pg.screenshot(path="C:/tmp/run_result.png", full_page=True); say("SHOT run_result")
    body=pg.evaluate("() => document.body.innerText").lower()
    say("'simulate success' in result: "+str('simulate success' in body))
    say("'success': "+str('success' in body)+" | 'error': "+str('error' in body)+" | 'fail': "+str('fail' in body))
