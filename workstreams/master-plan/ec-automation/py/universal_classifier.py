"""Universal EC Screen Engine - Phase 1: CLASSIFIER (read-only, generic across families).

Opens a screen live, segments it into REGIONS (toolbar / navigator / grid / form) using the same
structural DOM signatures already proven in tmp/scripts/scan_ec_screen.py, then classifies every
field inside into a WIDGET PRIMITIVE (text / dropdown / date / checkbox / button / grid_cell) purely
from DOM shape - no family branching (no "if is_ov" logic), unlike the existing family-aware scan.
Never Saves. Never writes. Design: docs/universal_screen_engine_design.md.

Usage:
   SCREEN="Bank" py workstreams/master-plan/ec-automation/py/universal_classifier.py
"""
import json
import os
import sys
from playwright.sync_api import sync_playwright

EC_URL = os.environ.get("EC_URL", "https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/")
SCREEN = os.environ.get("SCREEN", "Bank")
HEADED = os.environ.get("EC_HEADED", "0") == "1"
YELLOW = "rgb(252, 249, 192)"


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)


def classify_dd(page, dd_input_id):
    """A dd_input field is either an autocomplete DROPDOWN (opens a small _panel with rows carrying
    data-item-label) or an EC-object PICKER POPUP (opens a separate modal/dialog instead). PrimeFaces
    does not render the _panel div into the DOM until the button is actually clicked once, so a pure
    static-DOM check cannot tell them apart (confirmed live on Bank's Country field - fell through to
    'popup_unconfirmed' even though it is a genuine dropdown). Fixed 2026-08-12: click-and-inspect
    probe - click the button, look at what rendered, then close it - still read-only (no Save, no
    data entered), same class of action as scan_ec_screen.py already does for gated nav dropdowns."""
    base = dd_input_id[: -len("_input")]
    try:
        btn = page.locator(css(base + "_button")).first
        btn.scroll_into_view_if_needed(timeout=5000)
        btn.click()
        # poll up to ~2.5s instead of a fixed 700ms - fixed 2026-08-12 after Contract screen showed
        # 7 dd fields deep in a long scrollable form returning 'unknown_after_probe' with the old
        # fixed wait (PrimeFaces panel/dialog render time varies with form depth/AJAX load).
        verdict = "unknown_after_probe"
        for _ in range(5):
            page.wait_for_timeout(500)
            verdict = page.evaluate(
                """(base) => {
                // Fixed 2026-08-12 (Contract screen, Message Contact fields): a server-filtered
                // type-to-search autocomplete's panel renders VISIBLE but EMPTY at click time (no
                // data-item-label rows until text is typed) - requiring option rows wrongly failed
                // this genuine dropdown. Visible ui-autocomplete-panel presence alone is sufficient;
                // a real EC-object-picker popup uses a DIFFERENT element (.ui-dialog) that becomes
                // visible instead - confirmed live these are distinct and never both fire together.
                const panel = document.getElementById(base + '_panel');
                const panelVisible = panel && panel.offsetParent && getComputedStyle(panel).display !== 'none';
                if (panelVisible && panel.className.includes('ui-autocomplete-panel')) return 'dropdown';
                const dlg = [...document.querySelectorAll('.ui-dialog')].find(d => d.offsetParent);
                if (dlg) return 'popup';
                return 'unknown_after_probe';
            }""",
                base,
            )
            if verdict != "unknown_after_probe":
                break
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        return verdict
    except Exception as e:
        return f"probe_err: {str(e)[:60]}"


def scan_grid_columns(page, grid_id):
    """Read-only: grid header labels + column index, plus a sample cell id template per column (from
    the first data row) so future code can build a locator to a specific row/column - e.g. to compare
    or validate a cell's value - without re-discovering the grid's structure each time. Never edits
    any cell.

    Fixed 2026-08-12: `grid_id` (the ':T_data' id) is the <tbody> itself, which has NO <th> - the
    header lives in a SIBLING table inside the enclosing '.ui-datatable' wrapper (PrimeFaces splits
    scrollable-table header/body into two tables). That wrapper's <thead> also contains "ghost"
    columns (ids containing '_ghost_', always empty label) used only for column-width sizing - the
    REAL header row's cell ids contain ':shc1:'. Confirmed live on Bank: 8 <th> total, 4 real
    (Code/Name/Start Date/End Date) + 4 ghost (empty label) - filtering by non-empty label is
    sufficient and simpler than matching ':shc1:' by name."""
    if not grid_id:
        return []
    return page.evaluate(
        """(gid) => {
        const grid = document.getElementById(gid);
        if (!grid) return [];
        const wrapper = grid.closest('.ui-datatable') || grid.closest('table')?.parentElement || grid;
        const allHeaders = [...wrapper.querySelectorAll('thead th')];
        const headers = allHeaders
            .map((th, rawIdx) => ({ rawIdx, label: (th.innerText || th.textContent || '').trim(), id: th.id || null }))
            .filter(h => h.label);   // drop ghost/sizing columns (always empty label)
        headers.forEach((h, i) => { h.index = i; delete h.rawIdx; });
        const bodyRows = grid.querySelectorAll('tr[data-ri]');
        let sampleCellIds = {};
        if (bodyRows.length) {
            [...bodyRows[0].querySelectorAll('td')].forEach((td, idx) => {
                const inputEl = td.querySelector('[id]');
                sampleCellIds[idx] = inputEl ? inputEl.id : (td.id || null);
            });
        }
        headers.forEach(h => { h.sample_cell_id = sampleCellIds[h.index] || null; });
        return headers;
    }""",
        grid_id,
    )


def classify_field_by_id(page, f):
    """Shared primitive classifier for any field dict from scan_region_fields(). Fixed 2026-08-12
    (Meter's 'Delivery Point Name'/'Delivery Stream Name'): a ':pin' id suffix is EC's OWN explicit
    popup-picker convention - confirmed live via DOM inspection, the field's parent div carries class
    'ECPopupCell' and its companion button id is '<field>B' (not '_button'). This is a reliable
    structural signature, NOT a heuristic - no click-probe needed for popups at all, unlike
    dropdown-vs-popup on a plain 'dd_input' field (classify_dd) where EC's markup doesn't
    pre-distinguish them and a probe is genuinely required."""
    if f["type"] == "checkbox":
        return "checkbox"
    if f["id"].endswith("da_input"):
        return "date"
    if f["id"].endswith("pin"):
        return "popup"
    if f["id"].endswith("dd_input"):
        return classify_dd(page, f["id"])
    return "text"


def scan_region_fields(page, id_prefix):
    """Generic field dump for any region prefix - id, type, value, mandatory(yellow), nearest label.
    Label lookup searches LEFTWARD from the field's own column for the nearest labeled cell in the
    same row (fixed 2026-08-12: a fixed 'always use C:0' lookup mislabels every column after the
    first label - e.g. objectdates' End Date at C:3 was reporting the C:1 row's 'Start Date' label
    because C:0 is the ONLY label cell it ever checked)."""
    return page.evaluate(
        """(sub) => [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id && e.id.includes(sub) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor==='"""
        + YELLOW
        + """';
            let lab='';
            const m=e.id.match(/^(.*:R:\\d+):C:(\\d+):/);
            if(m){ const rowPfx=m[1]; const myCol=parseInt(m[2],10);
                for(let c=myCol-1;c>=0 && !lab;c--){
                    const lc=document.getElementById(rowPfx+':C:'+c+':la')||document.getElementById(rowPfx+':C:'+c+':out')||document.querySelector("[id^='"+rowPfx+":C:"+c+"']");
                    if(lc){ const t=(lc.innerText||lc.value||'').trim(); if(t) lab=t; }
                }
            }
            if(!lab){ const r=e.closest('tr'); if(r){const c=[...r.querySelectorAll('td,th,label')].map(x=>(x.innerText||'').trim()).filter(Boolean); lab=c[0]||'';} }
            return {id:e.id, type:e.type||e.tagName.toLowerCase(), val:e.value, mandatory:y, label:lab}; })""",
        id_prefix,
    )


def has_popup_button(page, dd_input_id):
    """Distinguish an autocomplete dropdown (opens a small _panel with data-item-label rows) from an
    EC object-picker POPUP (opens a separate modal/dialog with its own search grid) - both pair a
    button with the field, but only the dropdown's panel has data-item-label option rows."""
    base = dd_input_id[: -len("_input")]
    return page.evaluate(
        """(base) => {
        const panel = document.getElementById(base + '_panel');
        if (panel && panel.querySelector('[data-item-label]')) return 'dropdown';
        const btn = document.getElementById(base + '_button') || document.getElementById(base);
        if (btn) return 'popup_or_dropdown_unresolved';
        return 'unknown';
    }""",
        base,
    )


def classify_screen(screen_name):
    result = {"screen": screen_name, "regions": {}, "unrecognized": []}
    with sync_playwright() as p:
        b = p.chromium.launch(headless=not HEADED, slow_mo=400 if HEADED else 0, args=["--ignore-certificate-errors"])
        page = b.new_context(ignore_https_errors=True, viewport={"width": 1900, "height": 1000}).new_page()
        page.goto(EC_URL, wait_until="domcontentloaded", timeout=45000)
        page.fill("#username", "sysadmin")
        page.fill("#password", "sysadmin")
        page.click("#kc-login")
        page.wait_for_selector(css("menu:searchForm:searchTxt"), timeout=60000)
        ajax(page)
        box = page.locator(css("menu:searchForm:searchTxt"))
        box.click()
        box.fill("")
        box.type(screen_name, delay=45)
        ajax(page, 7000)
        tv_link = page.locator(
            f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())='{screen_name}']"
        ).first
        tv_link.click()
        ajax(page)
        mm = page.locator(css("screenToolbar:form:minmaxMenu"))
        if mm.count() and mm.first.is_visible():
            mm.first.click()
            ajax(page)

        # --- readiness gate (never report an empty region as a fact) ---
        ready = False
        for _ in range(30):
            state = page.evaluate(
                """() => ({
                nav: document.querySelectorAll("[id^='nav:form:G:']").length,
                grid: document.querySelectorAll("[id$=':T_data']").length,
                form: document.querySelectorAll("[id*='objectForm']").length,
                go: ['go_button:form:B','button:form:B','navButton:form:B'].filter(i => document.getElementById(i)).length })"""
            )
            if state["nav"] or state["grid"] or state["form"] or state["go"]:
                ready = True
                break
            page.wait_for_timeout(1000)
        if not ready:
            result["unrecognized"].append("SCREEN_NEVER_RENDERED_NAV_GRID_FORM_OR_GO")
            b.close()
            return result
        page.wait_for_timeout(1200)

        # --- REGION 1: toolbar ---
        toolbar = page.evaluate(
            """() => { const out={}; const find=(...cs)=>{for(const c of cs){const e=document.querySelector('span.'+c)||document.querySelector('.'+c); if(e) return e;} return null;};
            const dis=e=>{const li=e&&e.closest('li,a'); return li? /ui-state-disabled|ui-submenu-state-disabled/.test(li.outerHTML):false;};
            const ins=find('ui-icon-insert','ui-icon-add'); const del=find('ui-icon-delete','ui-icon-remove','ui-icon-trash');
            if(ins) out.insert = dis(ins)?'DISABLED':'enabled';
            if(del) out.delete = dis(del)?'DISABLED':'enabled';
            return out; }"""
        )
        result["regions"]["toolbar"] = toolbar

        # --- REGION 2: navigator ---
        nav_fields_raw = page.evaluate(
            """() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
            const m=e.id.match(/nav:form:(G:\\d+):R:\\d+:C:\\d+:(da_input|dd_input|in)/); if(!m) return;
            const y=getComputedStyle(e).backgroundColor==='"""
            + YELLOW
            + """';
            out.push({id:e.id, grp:m[1], kind:m[2], mandatory:y}); });
            const go=['go_button:form:B','button:form:B','navButton:form:B'].filter(id=>document.getElementById(id));
            return {fields:[...new Map(out.map(o=>[o.id,o])).values()], go}; }"""
        )
        # gated nav: fill mandatory dds first-option + GO so grid/form render, same as scan_ec_screen.py.
        # Fixed 2026-08-12: a single upfront scan-then-fill-all pass misses 2ND-LEVEL cascade fields -
        # confirmed live on Contract, whose Contract Area dd is disabled/non-yellow until Business Unit
        # is chosen, so the ONE-SHOT scan (done before filling anything) never saw it as mandatory.
        # Now RE-SCANS the navigator after each fill and adds any newly-mandatory dd to the fill queue,
        # bounded to 5 rounds so a genuinely stuck cascade can't loop forever.
        filled_ids = set()
        any_filled = False
        for _round in range(5):
            current = page.evaluate(
                """() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
                const m=e.id.match(/nav:form:(G:\\d+):R:\\d+:C:\\d+:(dd_input)/); if(!m) return;
                const y=getComputedStyle(e).backgroundColor==='"""
                + YELLOW
                + """';
                const disabled = e.disabled || e.closest('.ui-state-disabled')!=null;
                out.push({id:e.id, grp:m[1], mandatory:y, disabled}); });
                return out; }"""
            )
            newly_mand = [f for f in current if f["mandatory"] and not f["disabled"] and f["id"] not in filled_ids]
            if not newly_mand:
                break
            for f in sorted(newly_mand, key=lambda x: x["grp"]):
                ddp = f["id"][: -len("_input")]
                try:
                    page.locator(css(ddp + "_button")).first.click()
                    page.wait_for_timeout(900)
                    opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]").first
                    opt.wait_for(state="visible", timeout=6000)
                    opt.click()
                    ajax(page, 12000)
                    filled_ids.add(f["id"])
                    any_filled = True
                except Exception:
                    filled_ids.add(f["id"])  # don't retry a field that failed to open/select
        if any_filled:
            go_id = nav_fields_raw["go"][0] if nav_fields_raw["go"] else "button:form:B"
            try:
                page.locator(css(go_id)).first.click()
                ajax(page, 20000)
            except Exception:
                pass

        # NOW classify each nav dd's primitive - fixed 2026-08-12: doing this BEFORE the cascade-fill
        # loop above probed a still-disabled dependent field (Contract Area, disabled until Business
        # Unit is chosen) - a disabled button's click is a no-op, so it always came back
        # 'unknown_after_probe' regardless of what it actually is. Classifying after fill means every
        # dd is at least enabled by the time it's probed (already-filled ones still have a working
        # button/panel to re-open).
        nav_out = []
        for f in nav_fields_raw["fields"]:
            if f["kind"] == "dd_input":
                primitive = classify_dd(page, f["id"])
            else:
                primitive = {"da_input": "date", "in": "text"}[f["kind"]]
            nav_out.append({"id": f["id"], "primitive": primitive, "mandatory": f["mandatory"]})
        result["regions"]["navigator"] = {"fields": nav_out, "go": nav_fields_raw["go"]}

        # --- REGION 3: grid ---
        grid_id = None
        for _ in range(20):
            grid_id = page.evaluate(
                """() => { const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.offsetParent||e.querySelector('tr'));
                return t.length? t[0].id : null; }"""
            )
            if grid_id:
                break
            page.wait_for_timeout(1000)

        # Fallback (2026-08-12, Contract finding): mandatory-yellow only marks fields required to
        # SAVE, not fields required to LIST/filter the grid - Contract Area is never yellow but the
        # grid stays empty without it. If the grid has zero rows, try filling any remaining
        # enabled-but-still-empty nav dropdown (regardless of color) once, then re-check.
        # KNOWN REMAINING GAP: this still picks the FIRST available option per dropdown (same
        # strategy as scan_ec_screen.py), which can land on a structurally-valid but data-empty
        # combination (confirmed live: BU='EC LNG Norway' + CA='NO LNG Europe ECLNG Norway' -> 0
        # rows). Column/primitive/mandatory facts are still correct even when this happens; only
        # sample_cell_id (which needs an actual row to sample) is unavailable in that case. Smarter
        # option-picking (prefer a combination known to have data) is future work, not fixed here.
        row_count = page.evaluate("(gid) => gid ? document.querySelectorAll('#'+gid.replace(/:/g,'\\\\:')+' tr[data-ri]').length : 0", grid_id) if grid_id else 0
        if grid_id and row_count == 0:
            leftover = page.evaluate(
                """() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:'][id$='dd_input']").forEach(e=>{
                const disabled = e.disabled || e.closest('.ui-state-disabled')!=null;
                if (!disabled && !e.value) out.push(e.id); });
                return out; }"""
            )
            filled_leftover = False
            for did in leftover:
                ddp = did[: -len("_input")]
                try:
                    page.locator(css(ddp + "_button")).first.click()
                    page.wait_for_timeout(900)
                    opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]").first
                    opt.wait_for(state="visible", timeout=6000)
                    opt.click()
                    ajax(page, 12000)
                    filled_leftover = True
                except Exception:
                    pass
            if filled_leftover:
                try:
                    go_id2 = nav_fields_raw["go"][0] if nav_fields_raw["go"] else "button:form:B"
                    page.locator(css(go_id2)).first.click()
                    ajax(page, 20000)
                except Exception:
                    pass

        columns = scan_grid_columns(page, grid_id)
        result["regions"]["grid"] = {"id": grid_id, "column_count": len(columns), "columns": columns}

        # --- REGION 4: form (row-select -> updateAttributes/objectdates; else Insert -> objectForm) ---
        form_fields = []
        try:
            sp = page.locator(f"xpath=//*[@id='{grid_id}']//tr//span[normalize-space(text())!='']").first
            if grid_id and sp.count():
                sp.click()
                ajax(page)
                page.wait_for_timeout(1200)
                for f in scan_region_fields(page, "updateAttributes:form"):
                    prim = classify_field_by_id(page, f)
                    form_fields.append({"id": f["id"], "primitive": prim, "mandatory": f["mandatory"], "label": f["label"], "source": "updateAttributes"})
                for f in scan_region_fields(page, "objectdates:form"):
                    form_fields.append({"id": f["id"], "primitive": "date", "mandatory": f["mandatory"], "label": f["label"], "source": "objectdates(delete=End Date)"})
        except Exception as e:
            result["unrecognized"].append(f"row_select_scan_err: {str(e)[:80]}")

        try:
            page.locator("xpath=//li[contains(@class,'ui-menu-parent')][.//span[contains(@class,'ui-icon-insert')]]").first.hover()
            page.wait_for_timeout(900)
            links = page.locator("xpath=//ul[contains(@class,'ui-menu-child')]//li//a")
            for i in range(links.count()):
                if links.nth(i).is_visible() and links.nth(i).text_content(timeout=800).strip() == "New Object":
                    links.nth(i).click()
                    break
            ajax(page)
            for f in scan_region_fields(page, "objectForm:form"):
                prim = classify_field_by_id(page, f)
                form_fields.append({"id": f["id"], "primitive": prim, "mandatory": f["mandatory"], "label": f["label"], "source": "objectForm(insert)"})
        except Exception as e:
            result["unrecognized"].append(f"insert_form_scan_err: {str(e)[:80]}")

        result["regions"]["form"] = {"fields": form_fields}
        b.close()
    return result


if __name__ == "__main__":
    out = classify_screen(SCREEN)
    print(json.dumps(out, indent=2))
