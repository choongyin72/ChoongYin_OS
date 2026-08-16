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
# R16: credentials via env vars (same lookup chain as every shipped *_iud.py bundle)
USER = os.environ.get("EC_USERNAME", os.environ.get("EC_USER", "sysadmin"))
PW = os.environ.get("EC_PASSWORD", os.environ.get("EC_PASS", "sysadmin"))
YELLOW = "rgb(252, 249, 192)"
# Optional hint (2026-08-12, Object List Setup finding): for a screen whose 1st-level cascade
# dropdown has a huge option count with a sparse valid-data fraction (confirmed: 295 List Class
# options, only 2 actually populated), blind cycling can't reliably find one in bounded attempts.
# A quick READ-ONLY DB check (same query style as tmp/scripts) can find a known-good value in
# seconds - this env var lets that value be supplied, tried FIRST, before falling back to blind
# cycling. Keeps the classifier itself DOM-only/generic by default; this is an opt-in assist, not a
# baked-in per-screen dependency.
NAV_HINT_OPTION = os.environ.get("NAV_HINT_OPTION")


def css(fid):
    return "#" + fid.replace(":", "\\:")


def ajax(page, t=15000):
    try:
        page.wait_for_load_state("networkidle", timeout=t)
    except Exception:
        pass
    page.wait_for_timeout(900)
    _dismiss_unsaved_changes_dialog(page)


def _dismiss_unsaved_changes_dialog(page):
    """EC's own genuine "Unsaved Changes" confirmation (real ids/labels confirmed live,
    2026-08-16, Universal Screen Engine open-items tracker #6b): fires whenever a field was
    changed but never Saved and the caller then attempts an action that would discard it
    (open_screen() navigating away, select_row() opening a different record's Update Attributes
    form, etc.) - not tied to one specific action, so a fix inside open_screen() alone was
    insufficient (confirmed live: the same dialog re-appeared on a later select_row() call after
    being dismissed once for navigation). Centralizing the check here in ajax() - the one
    function nearly every state-changing action already calls - means every caller is covered
    without hunting down and patching each action individually as new trigger points are found.

    Always clicks NO (confirmationForm:nobtn) - discard the unsaved change and let the caller's
    action proceed. Never CANCEL (would silently abort the caller's action, stranding it on the
    old state) and never YES (this function has no way to judge whether a half-filled form is
    safe to persist). A well-behaved caller should never hit this in the first place - every real
    IUD driver Saves/closes the record before moving on - this only guards callers (chiefly
    investigation/recon scripts) that intentionally leave a form dirty."""
    no_btn = page.locator(css("confirmationForm:nobtn"))
    if no_btn.count() and no_btn.first.is_visible():
        no_btn.first.click()
        try:
            page.wait_for_load_state("networkidle", timeout=8000)
        except Exception:
            pass
        page.wait_for_timeout(500)


def classify_dd(page, dd_input_id, cache=None):
    """A dd_input field is either an autocomplete DROPDOWN (opens a small _panel with rows carrying
    data-item-label) or an EC-object PICKER POPUP (opens a separate modal/dialog instead). PrimeFaces
    does not render the _panel div into the DOM until the button is actually clicked once, so a pure
    static-DOM check cannot tell them apart (confirmed live on Bank's Country field - fell through to
    'popup_unconfirmed' even though it is a genuine dropdown). Fixed 2026-08-12: click-and-inspect
    probe - click the button, look at what rendered, then close it - still read-only (no Save, no
    data entered), same class of action as scan_ec_screen.py already does for gated nav dropdowns.

    Fixed 2026-08-15 (Bank, engine.py re-probing): a field's dropdown-vs-popup classification is
    structural and never changes for the life of an open screen session, but `Engine._refresh_field_map()`
    calls this on EVERY refresh (construction, after New Object, after every Save, after every
    row-select) - so an unrelated optional field like Bank's Country got re-clicked and re-probed
    repeatedly within a single I-U-D run, visibly re-opening/closing its dropdown live even though the
    task never touches it (owner caught this happening live). Fix: an optional `cache` dict, keyed by
    `dd_input_id`, that the caller can supply and reuse across refreshes - `Engine` now owns one such
    cache per instance so each dropdown is probed at most once per open screen session. `cache=None`
    (default) preserves the original always-probe behavior for Phase 1's `classify_screen`, which has
    no equivalent long-lived session to cache across."""
    if cache is not None and dd_input_id in cache:
        return cache[dd_input_id]
    base = dd_input_id[: -len("_input")]
    try:
        btn = page.locator(css(base + "_button")).first
        btn.scroll_into_view_if_needed(timeout=5000)
        # Fixed 2026-08-13 (Price Object): this click had no explicit timeout, so a stuck/obscured
        # button (confirmed live: elementFromPoint at the button's center returned a different,
        # empty-id <span> sitting on top of it - likely a label/tooltip overlay during a busy
        # row-select-then-scan sequence) could block for Playwright's full 30s default. Observed 9
        # such stalls in one run (~270s wasted). Root cause not fully pinned down (a direct repro
        # via Insert form succeeded), so capping the wait instead of chasing an unproven fix - same
        # principle as the earlier row-select 5s cap: bound the cost of an optimistic action.
        btn.click(timeout=8000)
        # poll up to ~2.5s instead of a fixed 700ms - fixed 2026-08-12 after Contract screen showed
        # 7 dd fields deep in a long scrollable form returning 'unknown_after_probe' with the old
        # fixed wait (PrimeFaces panel/dialog render time varies with form depth/AJAX load).
        # Extended to ~7s (2026-08-12, Area's "System of Measurement" dd): confirmed live this
        # specific dropdown's panel genuinely takes ~6s to render (likely a larger/slower dataset),
        # exceeding the old 2.5s window even though nothing was actually wrong.
        verdict = "unknown_after_probe"
        for _ in range(14):
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
        # Reviewer note on #372 (2026-08-15): only cache a SETTLED verdict ('dropdown'/'popup'), not
        # 'unknown_after_probe' or a 'probe_err: ...' - those mean the probe itself didn't resolve
        # (e.g. a genuinely slow-rendering panel, or a transient click/scroll failure), and caching
        # them would wrongly lock the field into "unclassifiable" for the rest of the session even
        # though a later probe might succeed once the page settles.
        if cache is not None and verdict not in ("unknown_after_probe",) and not verdict.startswith("probe_err"):
            cache[dd_input_id] = verdict
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
                let cellId = inputEl ? inputEl.id : (td.id || null);
                // Fixed 2026-08-12 (Object List Setup, Object Code field): querySelector('[id]')
                // matches the FIRST id-bearing element in DOM order, which for a dropdown-in-grid
                // cell is the outer '<id>_dd' wrapper span, not the nested '<id>_dd_input' the user
                // actually types/reads from - confirmed live (typing into the wrapper did nothing;
                // the real target is the child input). If the resolved id ends in '_dd', prefer its
                // nested '_input' child when present, same convention as form-level dd_input fields.
                // Fixed 2026-08-14 (Financial Item Template, Phase 4 pilot): the SAME wrapper-vs-
                // nested-input gap exists for date-in-grid cells - '<id>_da' is a calendar widget
                // wrapper span, not itself an <input>; Playwright's input_value()/fill() throw
                // 'Node is not an <input>' when pointed at it directly. Confirmed live: the real
                // target is '<id>_da_input', identical convention to the dropdown case above.
                if (cellId && (cellId.endsWith('_dd') || cellId.endsWith('_da'))) {
                    const nested = document.getElementById(cellId + '_input');
                    if (nested) cellId = nested.id;
                }
                sampleCellIds[idx] = cellId;
            });
        }
        headers.forEach(h => { h.sample_cell_id = sampleCellIds[h.index] || null; });
        return headers;
    }""",
        grid_id,
    )


def classify_field_by_id(page, f, cache=None):
    """Shared primitive classifier for any field dict from scan_region_fields(). Fixed 2026-08-12
    (Meter's 'Delivery Point Name'/'Delivery Stream Name'): a ':pin' id suffix is EC's OWN explicit
    popup-picker convention - confirmed live via DOM inspection, the field's parent div carries class
    'ECPopupCell' and its companion button id is '<field>B' (not '_button'). This is a reliable
    structural signature, NOT a heuristic - no click-probe needed for popups at all, unlike
    dropdown-vs-popup on a plain 'dd_input' field (classify_dd) where EC's markup doesn't
    pre-distinguish them and a probe is genuinely required.

    `cache` is passed straight through to classify_dd() - see its docstring (2026-08-15 fix) for why
    it exists: lets a long-lived caller (Engine) avoid re-probing the same dropdown on every refresh."""
    if f["type"] == "checkbox":
        return "checkbox"
    if f["id"].endswith("da_input"):
        return "date"
    if f["id"].endswith("pin"):
        return "popup"
    if f["id"].endswith("dd_input"):
        return classify_dd(page, f["id"], cache=cache)
    return "text"


def scan_region_fields(page, id_prefix):
    """Generic field dump for any region prefix - id, type, value, mandatory(yellow), nearest label.
    Label lookup searches LEFTWARD from the field's own column for the nearest labeled cell in the
    same row (fixed 2026-08-12: a fixed 'always use C:0' lookup mislabels every column after the
    first label - e.g. objectdates' End Date at C:3 was reporting the C:1 row's 'Start Date' label
    because C:0 is the ONLY label cell it ever checked).

    Fixed 2026-08-13 (Daily Gas Stream Status navigator): some navigator layouts put each field in
    its OWN group (G:1/G:2/G:3, one dropdown per group) with the label ABOVE the field - same group
    and column, row R:0 vs the field's R:1 - not to its left at all (confirmed live via DOM
    inspection: `nav:form:G:1:R:0:C:0:la` = 'Production Unit', directly above
    `nav:form:G:1:R:1:C:0:dd_input`). Leftward search alone found nothing (there's no C:-1), so this
    adds an UPWARD fallback within the same group+column - tried only when leftward comes up empty,
    so it can't override the leftward match already proven correct for OV/OV-GM's field-groups."""
    return page.evaluate(
        """(sub) => [...document.querySelectorAll('input,select,textarea')]
        .filter(e=>e.id && e.id.includes(sub) && e.type!=='hidden')
        .map(e=>{ const y=getComputedStyle(e).backgroundColor==='"""
        + YELLOW
        + """';
            let lab='';
            const m=e.id.match(/^(.*:R:)(\\d+):C:(\\d+):/);
            if(m){ const grpPfx=m[1]; const myRow=parseInt(m[2],10); const myCol=parseInt(m[3],10);
                const rowPfx=grpPfx+myRow;
                for(let c=myCol-1;c>=0 && !lab;c--){
                    const lc=document.getElementById(rowPfx+':C:'+c+':la')||document.getElementById(rowPfx+':C:'+c+':out')||document.querySelector("[id^='"+rowPfx+":C:"+c+"']");
                    if(lc){ const t=(lc.innerText||lc.value||'').trim(); if(t) lab=t; }
                }
                for(let r=myRow-1;r>=0 && !lab;r--){
                    const lc=document.getElementById(grpPfx+r+':C:'+myCol+':la')||document.getElementById(grpPfx+r+':C:'+myCol+':out');
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
        page.fill("#username", USER)
        page.fill("#password", PW)
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
                go: ['go_button:form:B','button:form:B','navButton:form:B','buttongo:form:B'].filter(i => document.getElementById(i)).length })"""
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

        # --- REGION 2: navigator ---
        nav_fields_raw = page.evaluate(
            """() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:']").forEach(e=>{
            const m=e.id.match(/nav:form:(G:\\d+):R:\\d+:C:\\d+:(da_input|dd_input|in)/); if(!m) return;
            const y=getComputedStyle(e).backgroundColor==='"""
            + YELLOW
            + """';
            out.push({id:e.id, grp:m[1], kind:m[2], mandatory:y}); });
            const go=['go_button:form:B','button:form:B','navButton:form:B','buttongo:form:B'].filter(id=>document.getElementById(id));
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

        # --- REGION 1: toolbar ---
        # Fixed 2026-08-12 (Unit - Well Setup, PC): checking toolbar state BEFORE the nav cascade is
        # filled gives a technically-true-at-that-moment but MISLEADING reading for gated/PC screens,
        # where Insert genuinely IS disabled until a valid parent scope is selected - confirmed live,
        # Insert's <li> carries 'ui-submenu-state-disabled' before nav fill, and it's gone after GO.
        # Moved this whole check to AFTER the cascade-fill+GO sequence above, so it reads the screen's
        # settled/navigated state, matching how a real user would actually judge availability.
        toolbar = page.evaluate(
            """() => { const out={};
            // Fixed 2026-08-12 (Contract vs N1 comparison): 'ui-icon-insert' is NOT unique page-wide -
            // a personalization/settings menu elsewhere on the page can share the same icon class, and
            // document.querySelector (first DOM match) can grab THAT instead of the real toolbar icon,
            // giving a wrong reading (confirmed: Contract's real Insert <li> has no disabled class at
            // all, but the unscoped query matched something else that did). Scope the search to inside
            // the actual toolbar container only.
            const scope = document.querySelector('[id^="screenToolbar"]') || document;
            const find=(...cs)=>{for(const c of cs){const e=scope.querySelector('span.'+c)||scope.querySelector('.'+c); if(e) return e;} return null;};
            // Fixed 2026-08-12 (Daily Production Well Status 1, N1): closest('li,a') stops at the
            // NEARER <a> ancestor (span -> a -> li) and never reaches the <li> that actually carries
            // 'ui-submenu-state-disabled' - confirmed live, N1's Insert/Delete <li> genuinely IS
            // disabled (matching the documented N1 convention), but this check always missed it and
            // reported 'enabled'. closest('li') alone reaches the real disabling ancestor.
            // Fixed 2026-08-12 (Contract): testing li.outerHTML (not li.className) matches ANY
            // disabled marker ANYWHERE in the li's full subtree HTML, including nested sub-items
            // (e.g. Contract's Insert flyout has both "New Object" and "New Version" - "New Version"
            // can be legitimately disabled with no row selected while "New Object" itself is fully
            // available, but outerHTML-matching falsely flagged the WHOLE Insert action as disabled
            // because of that unrelated nested item). Test only the li's OWN class attribute.
            const dis=e=>{const li=e&&e.closest('li'); return li? /ui-state-disabled|ui-submenu-state-disabled/.test(li.className):false;};
            const ins=find('ui-icon-insert','ui-icon-add'); const del=find('ui-icon-delete','ui-icon-remove','ui-icon-trash');
            if(ins) out.insert = dis(ins)?'DISABLED':'enabled';
            if(del) out.delete = dis(del)?'DISABLED':'enabled';
            return out; }"""
        )
        result["regions"]["toolbar"] = toolbar

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
        def _poll_grid_id(rounds=20):
            gid = None
            for _ in range(rounds):
                gid = page.evaluate(
                    """() => { const t=[...document.querySelectorAll("[id$=':T_data']")].filter(e=>e.offsetParent||e.querySelector('tr'));
                    return t.length? t[0].id : null; }"""
                )
                if gid:
                    break
                page.wait_for_timeout(1000)
            return gid

        grid_id = _poll_grid_id()

        # Fallback (2026-08-12, Contract + Object List Setup finding): mandatory-yellow only marks
        # fields required to SAVE, not fields required to LIST/filter the grid - some nav fields are
        # never yellow but the grid stays empty without them. If the grid has zero rows, try filling
        # any remaining enabled-but-still-empty nav dropdown (regardless of color) once, then re-check.
        def _fill_leftover_enabled_dds():
            leftover = page.evaluate(
                """() => { const out=[]; document.querySelectorAll("[id^='nav:form:G:'][id$='dd_input']").forEach(e=>{
                const disabled = e.disabled || e.closest('.ui-state-disabled')!=null;
                if (!disabled && !e.value) out.push(e.id); });
                return out; }"""
            )
            any_now = False
            for did in leftover:
                ddp = did[: -len("_input")]
                try:
                    page.locator(css(ddp + "_button")).first.click()
                    page.wait_for_timeout(900)
                    opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]").first
                    opt.wait_for(state="visible", timeout=6000)
                    opt.click()
                    ajax(page, 12000)
                    any_now = True
                except Exception:
                    pass
            return any_now

        def _click_go():
            try:
                go_id2 = nav_fields_raw["go"][0] if nav_fields_raw["go"] else "button:form:B"
                page.locator(css(go_id2)).first.click()
                ajax(page, 20000)
            except Exception:
                pass

        def _row_count(gid):
            return page.evaluate("(gid) => gid ? document.querySelectorAll('#'+gid.replace(/:/g,'\\\\:')+' tr[data-ri]').length : 0", gid) if gid else 0

        if grid_id and _row_count(grid_id) == 0:
            if _fill_leftover_enabled_dds():
                _click_go()
                grid_id = _poll_grid_id(rounds=8) or grid_id

        # 2nd fallback (2026-08-12, Object List Setup finding): "pick the first available option" can
        # choose a 1st-level value (e.g. List Class 'ALLOC_NETWORK') that has ZERO valid combinations
        # downstream - its dependent dd then has no options at all, so filling it silently no-ops, and
        # the grid/tab element may not even RENDER at all (grid_id stays None, not just 0 rows) -
        # confirmed live: List Class 'FIN_WBS' has real data, the alphabetically-first option doesn't.
        # If grid_id is still missing OR has 0 rows, cycle through the FIRST mandatory dd's other
        # options (up to 8), re-filling every dependent dd fresh each time and RE-POLLING grid_id (not
        # just row count) after each GO, until a combination actually produces a rendered, non-empty
        # grid or attempts run out. Bounded and generic - not specific to this screen.
        if not grid_id or _row_count(grid_id) == 0:
            first_grp_dd = min(
                (f for f in nav_fields_raw["fields"] if f["kind"] == "dd_input"),
                key=lambda x: x["grp"], default=None,
            )
            if first_grp_dd:
                ddp = first_grp_dd["id"][: -len("_input")]
                found_populated = False
                tried = 0
                # try the hinted value first, if supplied and present among the real options
                if NAV_HINT_OPTION:
                    try:
                        page.locator(css(ddp + "_button")).first.click()
                        page.wait_for_timeout(900)
                        hint_opt = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label='{NAV_HINT_OPTION}']").first
                        hint_opt.wait_for(state="visible", timeout=6000)
                        hint_opt.click()
                        ajax(page, 12000)
                        tried += 1
                        _fill_leftover_enabled_dds()
                        _click_go()
                        candidate = _poll_grid_id(rounds=8)
                        if candidate and _row_count(candidate) > 0:
                            grid_id = candidate
                            found_populated = True
                        elif candidate:
                            grid_id = candidate
                    except Exception:
                        try:
                            page.keyboard.press("Escape")
                        except Exception:
                            pass
                for attempt in range(15 if not found_populated else 0):
                    try:
                        page.locator(css(ddp + "_button")).first.click()
                        page.wait_for_timeout(900)
                        opts = page.locator(f"xpath=//*[@id='{ddp}_panel']//tr[@data-item-label]")
                        opts.first.wait_for(state="visible", timeout=6000)
                        n = opts.count()
                        if attempt >= n:
                            page.keyboard.press("Escape")
                            break
                        opts.nth(attempt).click()
                        ajax(page, 12000)
                        tried += 1
                    except Exception:
                        break
                    _fill_leftover_enabled_dds()
                    _click_go()
                    candidate = _poll_grid_id(rounds=8)
                    if candidate and _row_count(candidate) > 0:
                        grid_id = candidate
                        found_populated = True
                        break
                    if candidate:
                        grid_id = candidate
                if not found_populated and tried > 0:
                    # Honest signal (2026-08-12, Object List Setup): a pure-DOM classifier with no DB
                    # assistance cannot reliably find a populated combination when the valid-data
                    # fraction of the option space is small (confirmed: 295 List Class options, only a
                    # handful actually have configured Object Lists) - a bounded retry is the right
                    # amount of effort, not a bug to keep chasing. Say so explicitly instead of a bare
                    # unexplained null.
                    result["unrecognized"].append(
                        f"grid_never_populated_after_{tried}_cascade_retry_attempts_on_first_nav_dd "
                        f"(likely sparse valid-combination space, not a classifier defect)"
                    )

        columns = scan_grid_columns(page, grid_id)
        result["regions"]["grid"] = {"id": grid_id, "column_count": len(columns), "columns": columns}

        # --- REGION 4: form (row-select -> updateAttributes/objectdates; else Insert -> objectForm) ---
        # Fixed 2026-08-12 (Object List Setup): this whole block is an OPTIMISTIC probe - "does this
        # screen use OV's click-a-row-to-edit modal-form pattern" - which PC/TV screens don't. It was
        # using Playwright's default 30s click timeout, burning ~30s on every PC/TV screen before
        # correctly falling through to an empty form region. A short explicit timeout is the right
        # amount of patience for a probe, not a wait for something expected to actually happen.
        form_fields = []
        try:
            sp = page.locator(f"xpath=//*[@id='{grid_id}']//tr//span[normalize-space(text())!='']").first
            if grid_id and sp.count():
                sp.click(timeout=5000)
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
            # Fixed 2026-08-12 (Daily Production Well Status 1, N1): contains(@class,'ui-icon-insert')
            # is a SUBSTRING match - it can accidentally hit an unrelated icon whose class merely
            # contains that text (confirmed live: hovering this on N1 opened a "system of measurement
            # override" personalization menu, not the record-insert menu, because some OTHER element's
            # class string happens to contain the substring). The toolbar-state check above already
            # uses an exact class match and correctly found only 1 real 'ui-icon-insert' icon on the
            # page - this xpath now matches the same way (exact class token, not substring).
            page.locator(
                "xpath=//li[contains(@class,'ui-menu-parent')]"
                "[.//span[contains(concat(' ',normalize-space(@class),' '),' ui-icon-insert ')]]"
            ).first.hover()
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
