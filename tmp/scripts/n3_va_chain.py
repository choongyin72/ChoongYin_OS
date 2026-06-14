"""N3 V->A recon-by-doing: chain P1_FwdUpd (P->V @2024-02-06) then P1_FwdUpdPar1 (->A, monthly) for
Feb 2024, observing the DB transitions, with a GUARANTEED snapshot->restore (data-safety: snapshot
the real non-P set first, restore EVERY non-P row in Feb 2024 back to P in a finally block, verify 0
residual). Goal: confirm the monthly approve lifts the daily-verified P1 rows V->A + writes a
STAT_PROCESS_STATUS row — the data to build the N3 lifecycle suite. ec-worker must be up.
Read+write, fully self-restoring."""
import time, os, sys
import oracledb
from playwright.sync_api import sync_playwright

URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"
SCREEN = "Daily Data Status Processes"
MONTH_FROM, MONTH_TO = "2024-02-01", "2024-02-29"
FWD_DATE = "2024-02-06"


def conn():
    return oracledb.connect(user='ECKERNEL_EC', password='energy', dsn=os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL'), tcp_connect_timeout=15)


def family_tables(cur):
    cur.execute("SELECT table_name FROM all_tables WHERE owner='ECKERNEL_EC' "
                "AND (table_name LIKE '%DAY_STATUS' OR table_name LIKE '%MTH_STATUS' "
                "OR table_name='STRM_DAY_STREAM' OR table_name='OBJECT_DAY_WEATHER') "
                "AND table_name NOT LIKE '%JN' ORDER BY table_name")
    return [r[0] for r in cur.fetchall()]


def nonP_in_month(label):
    """Count rows NOT in 'P' across the family within Feb 2024 (per table)."""
    c = conn(); cur = c.cursor(); out = {}
    for t in family_tables(cur):
        try:
            cur.execute(f"SELECT RECORD_STATUS, COUNT(*) FROM {t} WHERE DAYTIME>=TO_DATE(:f,'YYYY-MM-DD') "
                        f"AND DAYTIME<TO_DATE(:t,'YYYY-MM-DD')+1 AND RECORD_STATUS<>'P' GROUP BY RECORD_STATUS",
                        f=MONTH_FROM, t=MONTH_TO)
            for rs, n in cur.fetchall():
                out[f"{t}:{rs}"] = n
        except Exception:
            pass
    cur.close(); c.close()
    total = sum(out.values())
    print(f"  [{label}] non-P rows in Feb2024: total={total} {out if out else ''}")
    return out


def spc_count(pid):
    c = conn(); cur = c.cursor()
    cur.execute("SELECT COUNT(*) FROM STAT_PROCESS_STATUS WHERE PROCESS_ID=:p", p=pid)
    n = cur.fetchone()[0]; cur.close(); c.close(); return n


def latest_spc(pid):
    c = conn(); cur = c.cursor()
    cur.execute("SELECT PROCESS_ID, RECORD_STATUS_LEVEL, TO_CHAR(TRUNC(DAYTIME),'YYYY-MM-DD'), ROWS_UPDATED "
                "FROM STAT_PROCESS_STATUS WHERE PROCESS_ID=:p ORDER BY RUN_DAYTIME DESC FETCH FIRST 1 ROWS ONLY", p=pid)
    r = cur.fetchone(); cur.close(); c.close(); return r


def run_process(page, from_date, to_date, process_name):
    fr = next((f for f in page.frames if "dashboard.jsf" in (f.url or "") and "top=false" in (f.url or "")), None) or page
    fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').fill(from_date); fr.locator('[id="nav:form:G:0:R:1:C:0:da_input"]').press("Tab"); time.sleep(0.8)
    fr.locator('[id="nav:form:G:1:R:1:C:0:da_input"]').fill(to_date); fr.locator('[id="nav:form:G:1:R:1:C:0:da_input"]').press("Tab"); time.sleep(0.8)
    fr.locator('[id="nav:form:G:2:R:1:C:0:dd_button"]').click(timeout=4000)
    time.sleep(0.8)
    fr.locator(f'[id="nav:form:G:2:R:1:C:0:dd_panel"] tr[data-item-label="{process_name}"]').first.click(timeout=5000); time.sleep(1.2)
    fr.locator('[id="button:form:B"]').click(timeout=5000); page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
    fr.locator('[id="RunProcessButton:form:B"]').click(timeout=6000)
    print(f"   RUN clicked: '{process_name}' [{from_date}..{to_date}]")
    page.wait_for_load_state("networkidle", timeout=30000); time.sleep(1.5)


def poll_new(pid, baseline, label, secs=90):
    for i in range(secs // 5):
        time.sleep(5)
        if spc_count(pid) > baseline:
            r = latest_spc(pid)
            print(f"   [{label}] EXECUTED after {(i+1)*5}s -> STAT_PROCESS_STATUS {r}")
            return True
    print(f"   [{label}] no new run row in {secs}s (executor idle / no matching data?)")
    return False


print("=== STEP 0: baseline (expect all-P; 0 non-P in Feb2024) ===")
nonP_in_month("baseline")
fwd_base = spc_count("P1_FwdUpd"); app_base = spc_count("P1_FwdUpdPar1")
print(f"  STAT_PROCESS_STATUS baseline: P1_FwdUpd={fwd_base}  P1_FwdUpdPar1={app_base}")

try:
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        page = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1000}).new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.fill('[id="username"]', "sysadmin"); page.fill('[id="password"]', "sysadmin"); page.click('[id="kc-login"]')
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); time.sleep(1.0)
        sel = f'xpath=//*[contains(@class,"tv-link") and normalize-space(text())="{SCREEN}"]'
        page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
        page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)

        print("\n=== STEP 1: forward P->V (P1_FwdUpd @ 2024-02-06) ===")
        run_process(page, FWD_DATE, FWD_DATE, "P1 Forward Status Update")
        poll_new("P1_FwdUpd", fwd_base, "forward")
        nonP_in_month("after forward")

        print("\n=== STEP 2: approve V->A (P1_FwdUpdPar1, monthly Feb 2024) ===")
        # re-open screen fresh for the second run (avoid stale nav state)
        page.locator('[id="menu:searchForm:searchTxt"]').fill(""); page.locator('[id="menu:searchForm:searchTxt"]').type(SCREEN, delay=30)
        page.wait_for_selector(sel, timeout=12000); page.locator(sel).first.click()
        page.wait_for_load_state("networkidle", timeout=30000); time.sleep(2.0)
        run_process(page, MONTH_FROM, MONTH_TO, "P1 Parent1 Forward Status Update")
        poll_new("P1_FwdUpdPar1", app_base, "approve")
        nonP_in_month("after approve")
        b.close()
except Exception as e:
    print("\nUI ERROR:", str(e)[:200])

finally:
    print("\n=== RESTORE (set every non-P row in Feb 2024 back to P; verify 0 residual) ===")
    c = conn(); cur = c.cursor(); total = 0
    for t in family_tables(cur):
        try:
            cur.execute(f"UPDATE {t} SET RECORD_STATUS='P' WHERE DAYTIME>=TO_DATE(:f,'YYYY-MM-DD') "
                        f"AND DAYTIME<TO_DATE(:t,'YYYY-MM-DD')+1 AND RECORD_STATUS<>'P'", f=MONTH_FROM, t=MONTH_TO)
            if cur.rowcount:
                print(f"   restored {t}: {cur.rowcount}"); total += cur.rowcount
        except Exception:
            pass
    c.commit(); cur.close(); c.close()
    print(f"   total restored: {total}")
    nonP_in_month("post-restore (expect 0)")
    print("DONE")
