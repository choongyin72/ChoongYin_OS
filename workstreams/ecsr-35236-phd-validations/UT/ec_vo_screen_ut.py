"""
ECSR-35236 SCREEN-based UT capture (plutodev EC Web App).
Drives the Validation Overview - Pluto Scarborough screen for the tank PHD group on the
demo date, captures BEFORE -> applies the scoping fix -> captures AFTER -> ROLLS BACK.

SAFETY: apply + rollback wrap the capture in try/finally; the rollback ALWAYS runs (even on
error) and the final state is DB-verified clean before exit. Run as ONE command.
plutodev is the sanctioned write-with-rollback env.
"""
import oracledb, os, time, json
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
SS = HERE / "screens"; SS.mkdir(exist_ok=True)
SQLDIR = HERE.parent / "sql"
APPLY = SQLDIR / "V1.1.8.0030.0001__ECSR-35236__PHD_check_rule_method_scope.sql"
ROLLBACK = SQLDIR / "ROLLBACK__ECSR-35236__PHD_check_rule_method_scope.sql"

EC_URL = "https://app-plutodev.woodside-pluto.tieto-og.cloud/"
EC_USER, EC_PASS = "sysadmin", "Sysadmin@01"
DB_DSN = "db.plutodev.woodside-pluto.tieto-og.cloud:1521/plutodev"
DB_USER, DB_PWD = "ECKERNEL_EC", "energy"

SCREEN = "Validation Overview - Pluto Scarborough"
DATE = "2026-06-06"
GROUP = "Daily Tank Status - VCF Calc - PHD Validations"   # V_PHD_TANK_DIP (rules 1147/1149)
VO_FROM = "nav:form:G:0:R:1:C:0:da_input"
VO_TO = "nav:form:G:0:R:1:C:1:da_input"
VO_GO = "navButton:form:B"
RUN_SELECTED = ("xpath=//*[self::button or self::a or contains(@class,'ui-button')]"
                "[.//*[normalize-space()='Run Selected Groups'] or normalize-space(.)='Run Selected Groups']")

results = {"date": DATE, "group": GROUP}


def run_sql(con, path):
    block = "\n".join(l for l in Path(path).read_text(encoding="utf-8").splitlines() if l.strip() != "/")
    con.cursor().execute(block); con.commit()


def rule_state(con):
    cur = con.cursor()
    out = {}
    for nm in ("PHD_TANK_DIP_GRS_MASS_VAL1", "PHD_TANK_DIP_STD_DENSITY_VAL1"):
        cur.execute("SELECT where_formula FROM tv_ctrl_check_rules WHERE check_name=:n", [nm])
        out[nm] = (cur.fetchone()[0] or "").strip()
    return out


def cframe(page):
    for fr in page.frames:
        try:
            if fr.query_selector(f'[id="{VO_FROM}"]'):
                return fr
        except Exception:
            pass
    return page.main_frame


def login(page):
    page.goto(EC_URL, wait_until="networkidle", timeout=45000); time.sleep(2)
    if page.locator('#username').count() and page.locator('#username').is_visible():
        page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
    elif page.locator('input[name="username"]').count():
        page.fill('input[name="username"]', EC_USER); page.fill('input[name="password"]', EC_PASS)
        page.click('input[type="submit"]')
    page.wait_for_load_state("networkidle", timeout=45000); time.sleep(3)
    print("  logged in")


def open_screen(page):
    si = page.locator('#menu\\:searchForm\\:searchTxt')
    si.wait_for(state="visible", timeout=20000)
    si.click(); si.fill(""); si.type(SCREEN[:24], delay=40)
    page.wait_for_load_state("networkidle", timeout=15000); time.sleep(1)
    page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and "
                 f"contains(normalize-space(.),'Validation Overview')]").first.click()
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(3)
    print("  screen opened")


def set_date_go(fr):
    fr.fill(f'[id="{VO_FROM}"]', DATE)
    fr.fill(f'[id="{VO_TO}"]', DATE)
    fr.page.keyboard.press("Escape")
    fr.click(f'[id="{VO_GO}"]')
    fr.page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)


def group_idx(fr):
    return fr.evaluate("""(desc) => { let r=-1;
        document.querySelectorAll('[id^="groups:form:T:"][id$=":C0_la"]').forEach(la=>{
            if((la.textContent||'').includes(desc)){const m=la.id.match(/groups:form:T:(\\d+):C0_la/); if(m) r=parseInt(m[1]);}});
        return r; }""", GROUP)


def summary_errors(fr, idx):
    txt = fr.evaluate(f"""() => {{ const e=document.querySelector('[id="groups:form:T:{idx}:C2_la"]'); return e? e.textContent:''; }}""")
    import re
    m = re.search(r"(\d+)\s+Errors", txt or "")
    return (int(m.group(1)) if m else None), (txt or "").strip()


def run_group_and_capture(page, fr, tag):
    set_date_go(fr)
    idx = group_idx(fr)
    if idx < 0:
        print(f"  [{tag}] group row not found"); return None, None
    fr.click(f'[id="groups:form:T:{idx}:C0_la"]'); time.sleep(0.6)
    # Run Selected Groups
    try:
        fr.click(RUN_SELECTED, timeout=10000)
    except Exception:
        fr.click(f"xpath=//*[normalize-space(.)='Run Selected Groups']", timeout=10000)
    page.wait_for_load_state("networkidle", timeout=90000); time.sleep(3)
    # GO to refresh summary
    fr.click(f'[id="{VO_GO}"]'); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2)
    idx = group_idx(fr)
    errs, summary = summary_errors(fr, idx)
    shot = str(SS / f"vo_tank_{tag}.png")
    page.screenshot(path=shot, full_page=True)
    print(f"  [{tag}] group errors={errs} | summary={summary[:70]} | shot={os.path.basename(shot)}")
    return errs, summary


con = oracledb.connect(user=DB_USER, password=DB_PWD, dsn=DB_DSN)
print("S0 (before):", rule_state(con))
applied = False
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        ctx = browser.new_context(viewport={"width": 1680, "height": 1000}, ignore_https_errors=True)
        page = ctx.new_page(); page.set_default_timeout(30000)
        login(page); open_screen(page)
        fr = cframe(page)
        print("  content frame resolved:", fr is not page.main_frame)

        # BEFORE (original rules)
        eb, sb = run_group_and_capture(page, fr, "before")
        results["before_errors"], results["before_summary"] = eb, sb

        # APPLY the scoping fix
        run_sql(con, APPLY); applied = True
        print("APPLIED:", rule_state(con))

        # AFTER (scoped rules)
        ea, sa = run_group_and_capture(page, fr, "after")
        results["after_errors"], results["after_summary"] = ea, sa

        ctx.close(); browser.close()
finally:
    if applied:
        run_sql(con, ROLLBACK)
        st = rule_state(con)
        clean = all("and " not in v.lower() for v in st.values())
        results["rolled_back_clean"] = clean
        print("ROLLBACK done. state:", st, "clean=", clean)
    con.close()

(HERE / "vo_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print("\nRESULT:", json.dumps(results, indent=2))
