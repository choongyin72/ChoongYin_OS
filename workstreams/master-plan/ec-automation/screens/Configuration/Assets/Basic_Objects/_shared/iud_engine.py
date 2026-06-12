"""Shared Playwright IUD engine for EC Manage-Object (OV / OV-GM) screens.

One engine, thin per-screen configs (the per-screen scripts in
../<Screen>/playwright/ pass a CFG dict). Mirrors the proven RF flow:
  login -> navigate -> [navigator dropdowns + GO] -> clean check
  -> INSERT (New Object, code/name/date + mandatory dropdowns, Save, GO)
  -> UPDATE (select row, rename, Save, GO)
  -> DELETE (End Date = Start Date true delete, Save, GO [+extra GO])
Each step is screenshot to the bundle's evidence/ folder; results go to a JSON
log; UI checks are backed by DB ground-truth checks (oracledb thin).
NEVER touches existing data - AUTOTEST_* codes only, deleted again at the end.
"""
import json
import os
import time

import oracledb
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
EC_USER = os.environ.get("EC_USER", "sysadmin")
EC_PASS = os.environ.get("EC_PASS", "sysadmin")
DB_DSN = os.environ.get("EC_DB_DSN", "localhost:1521/ORCL")
DB_USER = os.environ.get("EC_DB_USER", "ECKERNEL_EC")
DB_PASS = os.environ.get("EC_DB_PASS", "energy")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
SLOW_MO = int(os.environ.get("EC_SLOWMO", "400")) if HEADED else 0


def _css(fid):
    return "#" + fid.replace(":", "\\:")


class Engine:
    def __init__(self, cfg, evidence_dir, log_path):
        self.cfg = cfg
        self.evidence = evidence_dir
        self.log_path = log_path
        os.makedirs(evidence_dir, exist_ok=True)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.results = {}
        self.n = 0

    # ── helpers ──────────────────────────────────────────────────────────
    def ss(self, label):
        self.n += 1
        name = f"{self.cfg['slug']}_{self.n:02d}_{label}.png"
        self.page.screenshot(path=os.path.join(self.evidence, name))
        print(f"  [SS] {name}")

    def ajax(self, t=15000):
        try:
            self.page.wait_for_load_state("networkidle", timeout=t)
        except Exception:
            pass
        self.page.wait_for_timeout(1200)

    def rows(self):
        return self.page.evaluate(
            "(tid) => { const t=document.getElementById(tid); if(!t) return [];"
            " const out=[]; t.querySelectorAll('tr').forEach(tr=>{const c=[];"
            " tr.querySelectorAll('td').forEach(td=>c.push(td.textContent.trim()));"
            " if(c.some(x=>x)) out.push(c);}); return out; }",
            self.cfg["table_id"])

    def in_table(self, code, retries=3):
        # large custom grids repopulate slowly after save/refresh - retry the scan
        for i in range(retries):
            if any(r and r[0].strip() == code for r in self.rows()):
                return True
            if i < retries - 1:
                self.page.wait_for_timeout(3000)
        return False

    def fill(self, fid, value):
        el = self.page.locator(_css(fid))
        el.click()
        el.fill(value)
        self.page.evaluate(
            "(id) => { const e=document.getElementById(id); if(e){"
            "e.dispatchEvent(new Event('change',{bubbles:true}));"
            "e.dispatchEvent(new Event('blur',{bubbles:true}));} }", fid)
        self.page.wait_for_timeout(400)

    def fill_date(self, fid, value):
        el = self.page.locator(_css(fid))
        el.click()
        el.fill(value)
        self.page.keyboard.press("Tab")
        self.page.wait_for_timeout(600)
        self.page.evaluate(
            "(id) => { const e=document.getElementById(id); if(e){"
            "e.dispatchEvent(new Event('change',{bubbles:true}));"
            "e.dispatchEvent(new Event('blur',{bubbles:true}));} }", fid)
        self.page.wait_for_timeout(400)

    def select_dd(self, dd_prefix, value):
        """Same gesture as the RF 'Select EC Dropdown Option' keyword:
        open the panel, click tr[normalize-space(@data-item-label)=value];
        Escape + reopen once if the options are late (cascades/re-renders)."""
        item = (f"xpath=//*[@id='{dd_prefix}_panel']"
                f"//tr[normalize-space(@data-item-label)='{value}']")
        self.page.click(_css(dd_prefix + "_button"))
        try:
            self.page.locator(item).first.wait_for(state="visible", timeout=6000)
        except Exception:
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(1500)
            self.page.click(_css(dd_prefix + "_button"))
            self.page.locator(item).first.wait_for(state="visible", timeout=10000)
        self.page.locator(item).first.click()
        self.ajax(12000)

    def save(self):
        self.page.click("xpath=//a[@title='Save [Ctrl+s]' and not(contains(@class,'ui-state-disabled'))]")
        self.ajax()

    def go(self):
        """Apply Navigator (GO) where present; some custom-URL OV screens have no
        navigator - fall back to the toolbar Refresh."""
        go_btn = self.page.locator(_css("button:form:B"))
        if go_btn.count() and go_btn.first.is_visible():
            go_btn.first.click()
        else:
            self.page.click("xpath=//a[@title='Refresh [Ctrl+r]']")
        self.ajax()

    def select_row(self, code):
        self.page.click(
            f"xpath=//tbody[@id='{self.cfg['table_id']}']//span[normalize-space(text())='{code}']")
        self.ajax()
        self.page.wait_for_timeout(1000)

    def db_present(self, code):
        conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN,
                                tcp_connect_timeout=15)
        cur = conn.cursor()
        try:
            cur.execute(
                "SELECT column_name FROM all_tab_columns WHERE table_name=:v "
                "AND data_type LIKE '%CHAR%' ORDER BY column_id", v=self.cfg["db_view"])
            for (col,) in cur.fetchall():
                cur.execute(f'SELECT COUNT(*) FROM {self.cfg["db_view"]} WHERE "{col}" = :c', c=code)
                if cur.fetchone()[0]:
                    return True
            return False
        finally:
            cur.close()
            conn.close()

    # ── the IUD flow ─────────────────────────────────────────────────────
    def run(self):
        cfg = self.cfg
        code = os.environ.get("EC_CODE", f"AUTOTEST_{cfg['code_prefix']}_{time.strftime('%Y%m%d%H%M%S')}")
        name = f"{cfg['label']} {code}"
        name_upd = f"{cfg['label']} {code} UPD"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not HEADED, slow_mo=SLOW_MO,
                                        args=["--ignore-certificate-errors"])
            print(f"  [MODE] headed={HEADED} code={code}")
            ctx = browser.new_context(ignore_https_errors=True,
                                      viewport={"width": 1920, "height": 1080})
            self.page = ctx.new_page()

            print("=== LOGIN ===")
            self.page.goto(EC_URL, wait_until="domcontentloaded", timeout=30000)
            self.page.fill("#username", EC_USER)
            self.page.fill("#password", EC_PASS)
            self.page.click("#kc-login")
            self.page.wait_for_url("**/dashboard**", timeout=60000)
            self.ajax()
            self.results["login"] = "PASS"

            print(f"=== NAVIGATE TO {cfg['label']} ===")
            si = self.page.locator(_css("menu:searchForm:searchTxt"))
            si.clear()
            si.type(cfg["label"], delay=60)
            self.ajax(8000)
            self.page.locator(
                f"xpath=//*[self::label or self::span][contains(@class,'tv-link')"
                f" and normalize-space(text())='{cfg['label']}']").first.click()
            self.ajax()
            for dd, val in cfg.get("nav", []):
                print(f"  navigator: {val}")
                self.select_dd(dd, val)
            if cfg.get("nav"):
                self.go()
            self.results["navigate"] = "PASS"
            self.ss("loaded")

            print("=== CLEAN STATE ===")
            self.results["clean"] = "CLEAN" if not self.in_table(code) else "PRE-EXISTED"
            self.ss("clean_state")

            print("=== INSERT ===")
            self.page.hover("xpath=//li[contains(@class,'ui-menu-parent')]"
                            "[.//span[contains(@class,'ui-icon-insert')]]")
            item = self.page.locator(
                "xpath=//li[contains(@class,'ui-menu-parent')]"
                "[.//span[contains(@class,'ui-icon-insert')]]"
                "//ul[contains(@class,'ui-menu-child')]//a[normalize-space(.)='New Object']")
            item.first.wait_for(state="visible", timeout=10000)
            item.first.click()
            self.ajax()
            self.fill(cfg["ins_code"], code)
            self.fill(cfg["ins_name"], name)
            self.fill_date(cfg["ins_date"], cfg["start_date"])
            for dd, val in cfg.get("ins_dd", []):
                print(f"  insert dropdown: {val}")
                self.select_dd(dd, val)
            for dd in cfg.get("ins_dd_first", []):
                # mandatory reference dropdown on a throwaway record: first option
                item = f"css=[id='{dd}_panel'] tr[data-item-label]"
                self.page.click(_css(dd + "_button"))
                try:
                    self.page.locator(item).first.wait_for(state="visible", timeout=6000)
                except Exception:
                    self.page.keyboard.press("Escape")
                    self.page.wait_for_timeout(1500)
                    self.page.click(_css(dd + "_button"))
                    self.page.locator(item).first.wait_for(state="visible", timeout=10000)
                label = self.page.locator(item).first.get_attribute("data-item-label")
                print(f"  insert dropdown (first option): {label}")
                self.page.locator(item).first.click()
                self.ajax(12000)
            for fid, val, kind in cfg.get("ins_extra", []):
                # extra MANDATORY fields beyond the universal trio (text/checkbox)
                print(f"  insert extra ({kind}): {val}")
                if kind == "checkbox":
                    self.page.check(_css(fid))
                    self.page.wait_for_timeout(400)
                else:
                    self.fill(fid, val)
            self.ss("insert_filled")
            self.save()
            self.go()
            ui_ok = self.in_table(code)
            db_ok = self.db_present(code)
            self.results["insert"] = "PASS" if (ui_ok and db_ok) else f"FAIL ui={ui_ok} db={db_ok}"
            self.ss("insert_result")
            print(f"  INSERT: {self.results['insert']}")

            print("=== UPDATE ===")
            if self.results["insert"] == "PASS":
                self.select_row(code)
                loaded = self.page.evaluate(
                    "(id)=>{const e=document.getElementById(id);return e?e.value:null}",
                    cfg["upd_code"])
                assert loaded == code, f"row select failed: {loaded}"
                self.fill(cfg["upd_name"], name_upd)
                self.ss("update_filled")
                self.save()
                self.go()
                row = [r for r in self.rows() if r and r[0] == code]
                self.results["update"] = "PASS" if row and name_upd in str(row) else f"FAIL row={row}"
            else:
                self.results["update"] = "SKIP"
            self.ss("update_result")
            print(f"  UPDATE: {self.results['update']}")

            print("=== DELETE (End Date = Start Date true delete) ===")
            if self.results["insert"] == "PASS":
                self.select_row(code)
                self.fill_date(cfg["del_end"], cfg["end_date"])
                self.ss("delete_end_date_set")
                self.save()
                self.go()
                if cfg.get("extra_go_after_delete"):
                    self.go()   # versioned groupmodel grids redraw lazily
                ui_gone = not self.in_table(code)
                db_gone = not self.db_present(code)
                self.results["delete"] = ("PASS (true delete)" if (ui_gone and db_gone)
                                          else f"FAIL ui_gone={ui_gone} db_gone={db_gone}")
            else:
                self.results["delete"] = "SKIP"
            self.ss("final_state")
            print(f"  DELETE: {self.results['delete']}")

            if HEADED:
                self.page.wait_for_timeout(4000)
            ctx.close()
            browser.close()

        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        print("\nFINAL RESULTS")
        ok_all = True
        for k, v in self.results.items():
            ok = str(v).startswith(("PASS", "CLEAN"))
            if not ok and k != "clean":
                ok_all = False
            print(f"  {'OK ' if ok else 'XX '}{k:<10}: {v}")
        print(f"Overall: {'ALL PASS' if ok_all else 'SOME FAILURES'}")
        return 0 if ok_all else 1


def run_iud(cfg, bundle_dir):
    """Entry point for the thin per-screen scripts."""
    evidence = os.path.join(bundle_dir, "evidence")
    log = os.path.join(bundle_dir, "evidence", f"{cfg['slug']}_results.json")
    return Engine(cfg, evidence, log).run()
