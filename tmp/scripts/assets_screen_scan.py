"""READ-ONLY scan of EC 'Configuration > Assets' screens on the LOCAL app.

For each leaf screen in the given sub-sections: navigate via the treeview search
box, wait for the screen, capture URL + DOM markers, and classify into
OV / TV / RUN-verify / OTHER. NO Save/Insert/Delete is ever clicked - markers
are read from the static DOM only.

Usage:
    py assets_screen_scan.py "Basic Objects" "Operation Mode" "Date Objects"
    py assets_screen_scan.py --all          # every Assets sub-section
Resumable: screens already in the output JSON are skipped.

Output: tmp/screen_scan/assets_scan.json (+ shots/ for OTHER/error screens)
"""
import json
import re
import sys
import time
import traceback
from pathlib import Path

from playwright.sync_api import sync_playwright

TMP = Path(r"c:/Projects/ChoongYin_OS/tmp")
OUTDIR = TMP / "screen_scan"
SHOTS = OUTDIR / "shots"
OUT_JSON = OUTDIR / "assets_scan.json"
INVENTORY = TMP / "ec_menu_inventory.txt"
EC_URL = "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/"

OUTDIR.mkdir(exist_ok=True)
SHOTS.mkdir(exist_ok=True)


def parse_assets_tree():
    """Return {subsection: [screen labels]} under '    + Assets' (incl. nested groups)."""
    lines = INVENTORY.read_text(encoding="utf-8").splitlines()
    sections, current = {}, None
    in_assets = False
    for ln in lines:
        if ln == "    + Assets":
            in_assets = True
            continue
        if in_assets and re.match(r"^    \+ ", ln):  # next sibling of Assets
            break
        if not in_assets:
            continue
        m_grp = re.match(r"^        \+ (.+)$", ln)
        m_leaf = re.match(r"^\s+- (.+)$", ln)
        if m_grp:
            current = m_grp.group(1).strip()
            sections[current] = []
        elif m_leaf and current:
            sections[current].append(m_leaf.group(1).strip())
    return sections


MARKER_JS = r"""() => {
    const vis = el => !!(el && el.offsetParent !== null);
    const out = {
        screenLabel: '', dataTables: [], navApplyBtn: false, navSelects: 0,
        navDateInputs: 0, insertMenu: false, deleteMenu: false, deleteDisabled: null,
        runButtons: [], groupsTree: false, tabs: 0, iframe: false,
        treeTable: false, editableCells: 0, formGrid: false, bodyHint: ''
    };
    const lab = document.querySelector("[id$='screenToolbar:form:screenLabel'], [id$='form:screenLabel']");
    if (lab) out.screenLabel = (lab.textContent || '').trim();
    document.querySelectorAll("tbody[id$=':form:T_data'], div[id$=':form:T'] tbody").forEach(t => {
        if (t.id) out.dataTables.push(t.id);
    });
    // navigator: visible apply/GO button id ending :form:B (excluding hidden defaultSubmit)
    document.querySelectorAll("button[id$=':form:B'], a[id$=':form:B']").forEach(b => {
        if (vis(b)) out.navApplyBtn = true;
    });
    // navigator panels usually sit in a 'nav' form with selects / date inputs
    document.querySelectorAll("[id*='nav'][id*=':form:'] select, [id*='nav'] .ui-selectonemenu").forEach(s => {
        if (vis(s)) out.navSelects++;
    });
    document.querySelectorAll("input[id$='_da_input']").forEach(d => {
        if (vis(d)) out.navDateInputs++;
    });
    const insertParent = document.querySelector("li.ui-menu-parent span.ui-icon-insert");
    out.insertMenu = vis(insertParent && insertParent.closest('li'));
    const delIcon = document.querySelector("li.ui-menu-parent span.ui-icon-delete, span.ui-icon-delete");
    if (delIcon) {
        const li = delIcon.closest('li, button, a');
        out.deleteMenu = vis(li);
        out.deleteDisabled = /ui-state-disabled|disabled/.test((li && li.className) || '');
    }
    document.querySelectorAll("button, a.ui-button, span.ui-button-text").forEach(b => {
        const t = (b.textContent || '').trim();
        if (/^run\b|run selected/i.test(t) && vis(b)) out.runButtons.push(t.substring(0, 40));
    });
    out.groupsTree = !!document.querySelector("[id*='groups'][id$=':form:T_data'], [id*='groups:form:T']");
    out.tabs = document.querySelectorAll(".ui-tabs .ui-tabs-nav li").length;
    out.iframe = !!document.querySelector("iframe");
    out.treeTable = !!document.querySelector(".ui-treetable");
    out.editableCells = document.querySelectorAll("input[id*=':C'][id$='_in']").length;
    out.formGrid = !!document.querySelector("[id*='objectForm'], [id*='updateAttributes']");
    const main = document.querySelector('.ui-layout-center, #content, body');
    out.bodyHint = (main ? main.textContent : '').replace(/\s+/g, ' ').trim().substring(0, 120);
    return out;
}"""


def classify(m, url):
    """Rule-based classification from captured markers. Returns (type, confidence, why).

    Ground truth from the pilot: the manage_object framework URL is the OV
    signature (grid stays empty until Apply Navigator, so DOM markers lie);
    insert/delete toolbar icons exist on nearly every screen (weak signal);
    heavy tab counts indicate master-detail screens (not our 3 types).
    """
    # NOTE: every EC screen carries a standard 7-tab footer (Record Status /
    # Revision Info / Approval Status / Hints & Tips / Validation / Trending /
    # Attachments) - tabs==7 means NO real tabs. Only tabPanel grids indicate
    # real master-detail structure.
    if "/manage_object" in url:
        sub = "groupmodel " if "groupmodel" in url else ""
        return "OV", "high", f"manage_object {sub}framework URL"
    if "/manage_table" in url or "/table_class" in url:
        return "TV", "high", "manage_table/table_class framework URL"
    if m["runButtons"] and m["groupsTree"]:
        return "RUN-verify", "high", "run button + groups tree"
    has_table = bool(m["dataTables"])
    if any("manageObject" in t for t in m["dataTables"]):
        return "OV", "medium", "manageObject grid on a custom URL (recon before reuse)"
    detail_grids = [t for t in m["dataTables"] if "tabPanel" in t]
    if len(detail_grids) >= 2:
        return "OTHER", "medium", f"master-detail: {len(detail_grids)} tab-panel grids"
    if has_table and m["insertMenu"] and not m["navApplyBtn"]:
        return "TV", "medium", "inline grid + insert, no navigator (verify vs T2 table_class)"
    if has_table and m["navApplyBtn"]:
        return "OV-variant", "medium", "navigator + grid on custom URL (recon before reuse)"
    if has_table:
        return "OTHER", "low", "grid only - no insert/navigator markers"
    return "OTHER", "low", "no known markers"


def load_results():
    if OUT_JSON.exists():
        return json.loads(OUT_JSON.read_text(encoding="utf-8"))
    return {}


def save_results(res):
    OUT_JSON.write_text(json.dumps(res, indent=1), encoding="utf-8")


def login(page):
    page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
    page.fill("#username", "sysadmin")
    page.fill("#password", "sysadmin")
    page.click("#kc-login")
    page.wait_for_url("**/dashboard**", timeout=60000)
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_timeout(1500)


def navigate(page, label, section):
    """Search the treeview, click the .tv-link whose ancestor chain matches section."""
    box = page.locator("[id$='searchForm:searchTxt']")
    # real keystrokes with delay (mirrors RF 'Type Text ... delay=60ms') - the
    # PrimeFaces search filters on keyup, so fill() does not trigger it reliably
    box.click()
    box.fill("")
    box.press_sequentially(label, delay=60)
    try:
        page.wait_for_load_state("networkidle", timeout=8000)
    except Exception:
        pass
    page.wait_for_timeout(700)
    links = page.locator(f".tv-link >> text=\"{label}\"")
    n = links.count()
    if n == 0:
        # fallback: substring match (some long labels render with extra markup)
        links = page.locator(".tv-link", has_text=label)
        n = links.count()
    target = None
    if n == 0:
        return False, "no search match"
    if n == 1:
        target = links.nth(0)
    else:
        for i in range(n):
            chain = links.nth(i).evaluate(
                """el => { const names=[]; let li=el.closest('li');
                   while(li){ const l=li.querySelector(':scope > .ui-treenode-content .ui-treenode-label, :scope > div .ui-treenode-label');
                     if(l) names.push(l.textContent.trim()); li=li.parentElement ? li.parentElement.closest('li') : null; }
                   return names; }"""
            )
            if section in chain:
                target = links.nth(i)
                break
        if target is None:
            target = links.nth(0)
    target.click()
    try:
        page.wait_for_load_state("networkidle", timeout=25000)
    except Exception:
        pass
    # grids load via AJAX after the page settles - give the standard datatable
    # a chance to appear before capturing markers (absence is also a signal,
    # so a quiet timeout here is fine)
    try:
        page.wait_for_selector("tbody[id$=':form:T_data']", state="attached", timeout=8000)
    except Exception:
        pass
    page.wait_for_timeout(1200)
    return True, "ok"


def main():
    sections_all = parse_assets_tree()
    if "--all" in sys.argv:
        wanted = list(sections_all)
    else:
        wanted = [a for a in sys.argv[1:] if not a.startswith("-")]
    results = load_results()
    todo = []
    for sec in wanted:
        if sec not in sections_all:
            print(f"!! unknown section: {sec}")
            continue
        for scr in sections_all[sec]:
            key = f"{sec} :: {scr}"
            if key not in results:
                todo.append((sec, scr, key))
    print(f"sections={len(wanted)} screens to scan={len(todo)} (already done={len(results)})")
    if not todo:
        return

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--ignore-certificate-errors"])
        ctx = b.new_context(ignore_https_errors=True, viewport={"width": 1680, "height": 1200})
        page = ctx.new_page()
        login(page)
        done = 0
        for sec, scr, key in todo:
            rec = {"section": sec, "screen": scr}
            try:
                ok, why = navigate(page, scr, sec)
                if not ok:
                    rec.update(status="nav-fail", type="ERROR", why=why)
                else:
                    url = page.url
                    m = page.evaluate(MARKER_JS)
                    typ, conf, why = classify(m, url)
                    rec.update(status="ok", url=url, label=m["screenLabel"],
                               type=typ, confidence=conf, why=why, markers=m)
                    if typ.startswith("OTHER") or conf == "low":
                        shot = SHOTS / (re.sub(r"[^A-Za-z0-9]+", "_", key)[:80] + ".png")
                        page.screenshot(path=str(shot))
                        rec["shot"] = shot.name
            except Exception as e:
                rec.update(status="error", type="ERROR", why=str(e)[:200])
                try:
                    shot = SHOTS / (re.sub(r"[^A-Za-z0-9]+", "_", key)[:80] + "_err.png")
                    page.screenshot(path=str(shot))
                    rec["shot"] = shot.name
                    # recover the session: go back to dashboard
                    page.goto(EC_URL, wait_until="domcontentloaded", timeout=30000)
                    page.wait_for_timeout(1500)
                except Exception:
                    try:
                        page = ctx.new_page()
                        login(page)
                    except Exception:
                        traceback.print_exc()
                        break
            results[key] = rec
            done += 1
            save_results(results)
            print(f"[{done}/{len(todo)}] {key} -> {rec.get('type')} ({rec.get('confidence', '-')})")
    print("scan finished (READ-ONLY)")


if __name__ == "__main__":
    main()
